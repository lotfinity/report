#!/usr/bin/env python3
"""
One-command Pinegrow workflow for heavy Webflow/static exports.

Default work-file detection:
  1. index-standalone-rebuilt.html
  2. index-standalone.html
  3. index.html

Goal:
- Patch the real local HTML work file into lightweight edit mode so Pinegrow's internal canvas is faster.
- Run a preview server that reads the CURRENT edited patched HTML file, removes the Pinegrow edit toggles in memory,
  re-enables disabled scripts in memory, and serves a live full-preview version.
- This means edits you save in Pinegrow are visible in the external preview server without restoring from backup.

Usage from repo root:
  python3 tools/pinegrow_session.py

Optional:
  python3 tools/pinegrow_session.py --port 8090
  python3 tools/pinegrow_session.py --host 0.0.0.0 --port 8090
  python3 tools/pinegrow_session.py --no-restore-on-exit
  python3 tools/pinegrow_session.py --file index-standalone-rebuilt.html
  python3 tools/pinegrow_session.py --file index.html

What happens:
1. The detected/default HTML file is backed up to <file>.pinegrow-full.bak, if backup does not already exist.
2. That HTML file is patched for Pinegrow edit mode.
3. Pinegrow opens the lighter local HTML file.
4. The preview server reads that same edited file, removes edit-mode patches in memory, and serves it as full mode.
5. Ctrl+C restores the patched HTML file from backup unless --no-restore-on-exit is used.

Important:
- Do not commit *.pinegrow-full.bak files.
- Save in Pinegrow, then refresh the browser preview. The browser preview will include your saved edits.
"""

from __future__ import annotations

import argparse
import mimetypes
import os
import re
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML_CANDIDATES = [
    "index-standalone-rebuilt.html",
    "index-standalone.html",
    "index.html",
]
EDIT_CSS_HREF = "/assets/pinegrow-edit-mode.css"
START = "<!-- PINEGROW_EDIT_MODE_START -->"
END = "<!-- PINEGROW_EDIT_MODE_END -->"
SCRIPT_DISABLED_START = "<!-- PINEGROW_DISABLED_SCRIPT_START"
SCRIPT_DISABLED_END = "PINEGROW_DISABLED_SCRIPT_END -->"

HEAVY_EXTERNAL_SCRIPT_PATTERNS = [
    "gsap",
    "scrolltrigger",
    "split-type",
    "lenis",
    "webflow.js",
]

HEAVY_INLINE_SCRIPT_PATTERNS = [
    "new SplitType",
    "SplitType(",
    "ScrollTrigger.create",
    "gsap.timeline",
    "gsap.set",
    "CustomEase.create",
    "loaderDuration",
    "preloader_progress-bar",
    "preloader_numbers",
    "document.body.style.position = 'fixed'",
    "document.body.style.position = \"fixed\"",
    "window.scrollTo(0, 0)",
    "lenis.stop",
    "lenis.start",
    "data-lenis-toggle",
]

INJECTION = f"""{START}
<link rel=\"stylesheet\" href=\"{EDIT_CSS_HREF}\" data-pinegrow-edit-mode=\"css\">
<script data-pinegrow-edit-mode=\"runtime-guard\">
(function () {{
  window.__PINEGROW_EDIT_MODE__ = true;

  const noop = function () {{ return this; }};
  window.gsap = window.gsap || {{
    timeline: function () {{ return {{ to: noop, from: noop, fromTo: noop, set: noop, play: noop, pause: noop, progress: noop }}; }},
    set: noop,
    to: noop,
    from: noop,
    fromTo: noop,
    registerPlugin: noop
  }};
  window.ScrollTrigger = window.ScrollTrigger || {{ create: noop, refresh: noop, killAll: noop }};
  window.CustomEase = window.CustomEase || {{ create: function () {{ return \"none\"; }} }};
  window.SplitType = window.SplitType || function () {{ return {{ revert: noop }}; }};

  window.addEventListener(\"DOMContentLoaded\", function () {{
    document.documentElement.classList.add(\"pinegrow-edit-mode\");
    document.documentElement.classList.remove(\"w-mod-ix\");
    document.querySelectorAll(\"[text-split], [text-split-delay]\").forEach(function (el) {{
      el.style.opacity = \"1\";
    }});
    document.querySelectorAll(\".preloader\").forEach(function (el) {{
      el.style.display = \"none\";
    }});
    document.body.style.position = \"\";
    document.body.style.top = \"\";
    document.body.style.left = \"\";
    document.body.style.right = \"\";
    document.body.style.width = \"\";
  }});
}})();
</script>
{END}"""


def pick_default_html() -> str:
    for candidate in DEFAULT_HTML_CANDIDATES:
        if (ROOT / candidate).exists():
            return candidate
    raise SystemExit(
        "No default HTML file found. Tried: " + ", ".join(DEFAULT_HTML_CANDIDATES) +
        ". Use --file path/to/page.html if your work file has another name."
    )


def backup_path(path: Path) -> Path:
    return path.with_name(path.name + ".pinegrow-full.bak")


def is_heavy_external_script(tag: str) -> bool:
    src_match = re.search(r"\bsrc\s*=\s*(['\"])(.*?)\1", tag, flags=re.I | re.S)
    if not src_match:
        return False
    src = src_match.group(2).lower()
    return any(pattern in src for pattern in HEAVY_EXTERNAL_SCRIPT_PATTERNS)


def is_heavy_inline_script(tag: str) -> bool:
    if re.search(r"\bsrc\s*=", tag, flags=re.I):
        return False
    lowered = tag.lower()
    return any(pattern.lower() in lowered for pattern in HEAVY_INLINE_SCRIPT_PATTERNS)


def disable_heavy_scripts(document: str) -> str:
    def replace_script(match: re.Match[str]) -> str:
        tag = match.group(0)
        if SCRIPT_DISABLED_START in tag:
            return tag
        if is_heavy_external_script(tag) or is_heavy_inline_script(tag):
            return f"{SCRIPT_DISABLED_START}\n{tag}\n{SCRIPT_DISABLED_END}"
        return tag

    return re.sub(r"<script\b[^>]*>.*?</script>", replace_script, document, flags=re.I | re.S)


def inject_edit_guard(document: str) -> str:
    if START in document and END in document:
        return document
    if re.search(r"</head>", document, flags=re.I):
        return re.sub(r"</head>", INJECTION + "\n</head>", document, count=1, flags=re.I)
    return INJECTION + "\n" + document


def patch_to_edit(path: Path) -> None:
    backup = backup_path(path)
    if not backup.exists():
        backup.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

    document = path.read_text(encoding="utf-8", errors="replace")
    document = disable_heavy_scripts(document)
    document = inject_edit_guard(document)
    path.write_text(document, encoding="utf-8")


def restore_full(path: Path) -> bool:
    backup = backup_path(path)
    if not backup.exists():
        return False
    path.write_text(backup.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return True


def strip_edit_guard(document: str) -> str:
    pattern = re.escape(START) + r".*?" + re.escape(END)
    return re.sub(pattern, "", document, flags=re.S)


def reenable_disabled_scripts(document: str) -> str:
    # Convert:
    # <!-- PINEGROW_DISABLED_SCRIPT_START
    # <script>...</script>
    # PINEGROW_DISABLED_SCRIPT_END -->
    # back into just the script tag, in memory only.
    pattern = re.escape(SCRIPT_DISABLED_START) + r"\s*\n?(.*?)\n?\s*" + re.escape(SCRIPT_DISABLED_END)
    return re.sub(pattern, lambda m: m.group(1), document, flags=re.S)


def build_full_preview_from_patched(document: str) -> str:
    document = strip_edit_guard(document)
    document = reenable_disabled_scripts(document)
    document = document.replace(' class="pinegrow-edit-mode"', ' class=""')
    return document


def resolve_targets(names: list[str]) -> list[Path]:
    if not names:
        names = [pick_default_html()]
    targets = []
    for name in names:
        p = (ROOT / name).resolve()
        try:
            p.relative_to(ROOT)
        except ValueError:
            raise SystemExit(f"Refusing path outside repo: {name}")
        if not p.exists():
            raise SystemExit(f"File not found: {name}")
        targets.append(p)
    return targets


class LiveFullPreviewHandler(SimpleHTTPRequestHandler):
    server_version = "PinegrowLivePreviewServer/1.0"

    def translate_path(self, path: str) -> str:
        parsed = urlparse(path)
        clean = unquote(parsed.path).lstrip("/")
        if clean == "" or clean.endswith("/"):
            clean = self.server.default_html
        return str((ROOT / clean).resolve())

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self) -> None:
        file_path = Path(self.translate_path(self.path))
        try:
            file_path.relative_to(ROOT)
        except ValueError:
            self.send_error(403, "Forbidden")
            return

        if not file_path.exists() or not file_path.is_file():
            self.send_error(404, "Not found")
            return

        suffix = file_path.suffix.lower()
        if suffix in {".html", ".htm"}:
            raw = file_path.read_text(encoding="utf-8", errors="replace")
            full_preview = build_full_preview_from_patched(raw)
            data = full_preview.encode("utf-8")
            ctype = "text/html; charset=utf-8"
        else:
            data = file_path.read_bytes()
            ctype = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch the detected work file for Pinegrow and serve live full preview from patched edited files.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--file", action="append", dest="files", default=[], help="HTML file to patch. Can be repeated. Default auto-detects index-standalone-rebuilt.html, then index-standalone.html, then index.html.")
    parser.add_argument("--no-restore-on-exit", action="store_true", help="Leave HTML files in Pinegrow edit mode after Ctrl+C.")
    args = parser.parse_args()

    targets = resolve_targets(args.files)
    default_html = str(targets[0].relative_to(ROOT))

    print("Patching files for Pinegrow edit mode...")
    for path in targets:
        patch_to_edit(path)
        print(f"  Pinegrow edit file: {path.relative_to(ROOT)}")
        print(f"  backup: {backup_path(path).relative_to(ROOT)}")

    os.chdir(ROOT)
    server = ThreadingHTTPServer((args.host, args.port), LiveFullPreviewHandler)
    server.default_html = default_html

    print("")
    print("Pinegrow can now open the local project with lighter HTML files.")
    print("The browser preview reads the same edited HTML and re-enables scripts in memory.")
    print(f"Default preview file: {default_html}")
    print(f"Open full live preview: http://{args.host}:{args.port}/")
    print("Save in Pinegrow, then refresh the browser preview.")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()
        if not args.no_restore_on_exit:
            print("Restoring full HTML files...")
            for path in targets:
                if restore_full(path):
                    print(f"  restored: {path.relative_to(ROOT)}")
                else:
                    print(f"  no backup found: {path.relative_to(ROOT)}")
        else:
            print("Leaving files in Pinegrow edit mode because --no-restore-on-exit was used.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
