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
  python3 tools/pinegrow_session.py --host 127.0.0.1 --port 8090
  python3 tools/pinegrow_session.py --no-restore-on-exit
  python3 tools/pinegrow_session.py --file index-standalone-rebuilt.html
  python3 tools/pinegrow_session.py --file index.html
  python3 tools/pinegrow_session.py --enable-media
  python3 tools/pinegrow_session.py --enable-responsive-images
  python3 tools/pinegrow_session.py --enable-scripts --no-runtime-guard

What happens:
1. The detected/default HTML file is backed up under backups/pinegrow-session/, if backup does not already exist.
2. That HTML file is patched for Pinegrow edit mode.
3. Pinegrow opens the lighter local HTML file.
4. The preview server reads that same edited file, removes edit-mode patches in memory, and serves it as full mode.
5. Ctrl+C restores the patched HTML file from backup unless --no-restore-on-exit is used.

Important:
- Keep Pinegrow backups under backups/pinegrow-session/.
- Save in Pinegrow, then refresh the browser preview. The browser preview will include your saved edits.
"""

from __future__ import annotations

import argparse
import base64
import html
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
EDIT_CSS_HREF = "/assets-rebuilt/pinegrow-edit-mode.css"
START = "<!-- PINEGROW_EDIT_MODE_START -->"
END = "<!-- PINEGROW_EDIT_MODE_END -->"
PRELOADER_START = "<!-- PINEGROW_PRELOADER_HIDE_START -->"
PRELOADER_END = "<!-- PINEGROW_PRELOADER_HIDE_END -->"
DISABLED_SCRIPT_TYPE = "application/x-pinegrow-disabled-script"
MEDIA_PLACEHOLDER_ATTR = "data-pinegrow-disabled-media"
MEDIA_PLACEHOLDER_CLASS = "pinegrow-media-placeholder"
BACKUP_DIR = ROOT / "backups" / "pinegrow-session"

HEAVY_EXTERNAL_SCRIPT_PATTERNS = [
    "gsap",
    "scrolltrigger",
    "split-type",
    "splittext",
    "customease",
    "lenis",
    "webflow.js",
    "webflow.",
    "webflow.schunk",
]

HEAVY_INLINE_SCRIPT_PATTERNS = [
    "new SplitType",
    "SplitType(",
    "ScrollTrigger.create",
    "gsap.timeline",
    "gsap.registerPlugin",
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

EDIT_CSS_INJECTION = f'<link rel="stylesheet" href="{EDIT_CSS_HREF}" data-pinegrow-edit-mode="css">'

RUNTIME_GUARD_INJECTION = """<script data-pinegrow-edit-mode=\"runtime-guard\">
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
</script>"""

PRELOADER_HIDE_INJECTION = f"""{PRELOADER_START}
<style data-pinegrow-edit-mode=\"preloader-hide\">
  .preloader,
  .trigger {{
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
  }}
</style>
<script data-pinegrow-edit-mode=\"preloader-hide\">
(function () {{
  function hidePinegrowPreloader() {{
    document.querySelectorAll(".preloader, .trigger").forEach(function (el) {{
      el.style.setProperty("display", "none", "important");
      el.style.setProperty("visibility", "hidden", "important");
      el.style.setProperty("pointer-events", "none", "important");
    }});
    document.body.style.position = "";
    document.body.style.top = "";
    document.body.style.left = "";
    document.body.style.right = "";
    document.body.style.width = "";
  }}
  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", hidePinegrowPreloader);
  }} else {{
    hidePinegrowPreloader();
  }}
}})();
</script>
{PRELOADER_END}"""


class EditOptions:
    def __init__(
        self,
        *,
        disable_scripts: bool = True,
        disable_media_assets: bool = True,
        lighten_responsive_images: bool = True,
        inject_edit_css: bool = True,
        inject_runtime_guard: bool = True,
    ) -> None:
        self.disable_scripts = disable_scripts
        self.disable_media_assets = disable_media_assets
        self.lighten_responsive_images = lighten_responsive_images
        self.inject_edit_css = inject_edit_css
        self.inject_runtime_guard = inject_runtime_guard


def pick_default_html() -> str:
    for candidate in DEFAULT_HTML_CANDIDATES:
        if (ROOT / candidate).exists():
            return candidate
    raise SystemExit(
        "No default HTML file found. Tried: " + ", ".join(DEFAULT_HTML_CANDIDATES) +
        ". Use --file path/to/page.html if your work file has another name."
    )


def backup_path(path: Path) -> Path:
    try:
        rel = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        rel = path.name
    safe_name = rel.replace("/", "__")
    return BACKUP_DIR / f"{safe_name}.pinegrow-full.bak"


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
        if f'type="{DISABLED_SCRIPT_TYPE}"' in tag or f"type='{DISABLED_SCRIPT_TYPE}'" in tag:
            return tag
        if is_heavy_external_script(tag) or is_heavy_inline_script(tag):
            open_tag = re.match(r"<script\b[^>]*>", tag, flags=re.I | re.S)
            if not open_tag:
                return tag
            opener = open_tag.group(0)
            original_type = ""
            type_match = re.search(r"\stype\s*=\s*(['\"])(.*?)\1", opener, flags=re.I | re.S)
            if type_match:
                original_type = type_match.group(2)
                opener = re.sub(
                    r"\stype\s*=\s*(['\"])(.*?)\1",
                    f' type="{DISABLED_SCRIPT_TYPE}" data-original-type="{html.escape(original_type, quote=True)}"',
                    opener,
                    count=1,
                    flags=re.I | re.S,
                )
            else:
                opener = opener[:-1] + f' type="{DISABLED_SCRIPT_TYPE}" data-original-type="">'
            opener = opener[:-1] + ' data-pinegrow-disabled-script="true">'
            return opener + tag[open_tag.end():]
        return tag

    return re.sub(r"<script\b[^>]*>.*?</script>", replace_script, document, flags=re.I | re.S)


def lighten_images(document: str) -> str:
    document = re.sub(r"\s+srcset\s*=\s*(['\"]).*?\1", "", document, flags=re.I | re.S)
    document = re.sub(r"\s+sizes\s*=\s*(['\"]).*?\1", "", document, flags=re.I | re.S)
    document = re.sub(r'\s+loading\s*=\s*([\'"])eager\1', ' loading="lazy"', document, flags=re.I)
    return document


def encode_media_tag(tag: str) -> str:
    encoded = base64.b64encode(tag.encode("utf-8")).decode("ascii")
    tag_name_match = re.match(r"<\s*([a-z0-9:-]+)", tag, flags=re.I)
    tag_name = tag_name_match.group(1).lower() if tag_name_match else "media"
    label = "Video disabled for Pinegrow" if tag_name == "video" else "Embed disabled for Pinegrow"
    return (
        f'<div class="{MEDIA_PLACEHOLDER_CLASS}" {MEDIA_PLACEHOLDER_ATTR}="{encoded}" '
        f'data-pinegrow-media-tag="{tag_name}">{label}</div>'
    )


def disable_media(document: str) -> str:
    if MEDIA_PLACEHOLDER_ATTR in document:
        return document
    document = re.sub(r"<video\b[^>]*>.*?</video>", lambda m: encode_media_tag(m.group(0)), document, flags=re.I | re.S)
    document = re.sub(r"<iframe\b[^>]*>.*?</iframe>", lambda m: encode_media_tag(m.group(0)), document, flags=re.I | re.S)
    return document


def inject_edit_guard(document: str, options: EditOptions) -> str:
    if START in document and END in document:
        return document
    parts = [START]
    if options.inject_edit_css:
        parts.append(EDIT_CSS_INJECTION)
    if options.inject_runtime_guard:
        parts.append(RUNTIME_GUARD_INJECTION)
    parts.append(END)
    injection = "\n".join(parts)
    if re.search(r"</head>", document, flags=re.I):
        return re.sub(r"</head>", injection + "\n</head>", document, count=1, flags=re.I)
    return injection + "\n" + document


def inject_preloader_hide(document: str) -> str:
    if PRELOADER_START in document and PRELOADER_END in document:
        return document
    if re.search(r"</head>", document, flags=re.I):
        return re.sub(r"</head>", PRELOADER_HIDE_INJECTION + "\n</head>", document, count=1, flags=re.I)
    return PRELOADER_HIDE_INJECTION + "\n" + document


def patch_to_edit(path: Path, options: EditOptions | None = None) -> None:
    options = options or EditOptions()
    backup = backup_path(path)
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

    document = path.read_text(encoding="utf-8", errors="replace")
    document = strip_edit_guard(document)
    document = strip_preloader_hide(document)
    document = reenable_disabled_scripts(document)
    document = restore_disabled_media(document)
    if options.disable_scripts:
        document = disable_heavy_scripts(document)
    if options.disable_media_assets:
        document = disable_media(document)
    if options.lighten_responsive_images:
        document = lighten_images(document)
    document = inject_edit_guard(document, options)
    document = inject_preloader_hide(document)
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


def strip_preloader_hide(document: str) -> str:
    pattern = re.escape(PRELOADER_START) + r".*?" + re.escape(PRELOADER_END)
    return re.sub(pattern, "", document, flags=re.S)


def reenable_disabled_scripts(document: str) -> str:
    # Backward compatibility with the older comment-based disabler.
    document = re.sub(
        r"<!-- PINEGROW_DISABLED_SCRIPT_START\s*\n?(.*?)\n?\s*PINEGROW_DISABLED_SCRIPT_END -->",
        lambda m: m.group(1),
        document,
        flags=re.S,
    )

    def restore_opener(match: re.Match[str]) -> str:
        opener = match.group(0)
        original_type_match = re.search(r"\sdata-original-type\s*=\s*(['\"])(.*?)\1", opener, flags=re.I | re.S)
        original_type = html.unescape(original_type_match.group(2)) if original_type_match else ""
        opener = re.sub(r"\sdata-pinegrow-disabled-script\s*=\s*(['\"]).*?\1", "", opener, flags=re.I | re.S)
        opener = re.sub(r"\sdata-original-type\s*=\s*(['\"]).*?\1", "", opener, flags=re.I | re.S)
        if original_type:
            opener = re.sub(
                r"\stype\s*=\s*(['\"])" + re.escape(DISABLED_SCRIPT_TYPE) + r"\1",
                f' type="{html.escape(original_type, quote=True)}"',
                opener,
                count=1,
                flags=re.I | re.S,
            )
        else:
            opener = re.sub(
                r"\stype\s*=\s*(['\"])" + re.escape(DISABLED_SCRIPT_TYPE) + r"\1",
                "",
                opener,
                count=1,
                flags=re.I | re.S,
            )
        return opener

    return re.sub(r"<script\b[^>]*>", restore_opener, document, flags=re.I | re.S)


def restore_disabled_media(document: str) -> str:
    pattern = (
        r'<div\b[^>]*\s' + re.escape(MEDIA_PLACEHOLDER_ATTR) +
        r'\s*=\s*([\'"])(.*?)\1[^>]*>.*?</div>'
    )

    def restore(match: re.Match[str]) -> str:
        try:
            return base64.b64decode(match.group(2)).decode("utf-8")
        except Exception:
            return match.group(0)

    return re.sub(pattern, restore, document, flags=re.I | re.S)


def build_full_preview_from_patched(document: str) -> str:
    document = strip_edit_guard(document)
    document = strip_preloader_hide(document)
    document = reenable_disabled_scripts(document)
    document = restore_disabled_media(document)
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
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--file", action="append", dest="files", default=[], help="HTML file to patch. Can be repeated. Default auto-detects index-standalone-rebuilt.html, then index-standalone.html, then index.html.")
    parser.add_argument("--no-restore-on-exit", action="store_true", help="Leave HTML files in Pinegrow edit mode after Ctrl+C.")
    parser.add_argument("--enable-scripts", action="store_true", help="Keep heavy Webflow/GSAP/SplitType scripts active in Pinegrow edit mode.")
    parser.add_argument("--enable-media", action="store_true", help="Keep videos and iframes active in Pinegrow edit mode.")
    parser.add_argument("--enable-responsive-images", action="store_true", help="Keep image srcset/sizes attributes and eager loading in Pinegrow edit mode.")
    parser.add_argument("--no-edit-css", action="store_true", help="Do not inject assets-rebuilt/pinegrow-edit-mode.css. Preloader hiding still stays active.")
    parser.add_argument("--no-runtime-guard", action="store_true", help="Do not inject the JS runtime guard/stubs. Preloader hiding still stays active.")
    args = parser.parse_args()

    options = EditOptions(
        disable_scripts=not args.enable_scripts,
        disable_media_assets=not args.enable_media,
        lighten_responsive_images=not args.enable_responsive_images,
        inject_edit_css=not args.no_edit_css,
        inject_runtime_guard=not args.no_runtime_guard,
    )
    targets = resolve_targets(args.files)
    default_html = str(targets[0].relative_to(ROOT))

    print("Patching files for Pinegrow edit mode...")
    print("  preloader hide: always on")
    print(f"  disable scripts: {'yes' if options.disable_scripts else 'no'}")
    print(f"  disable media: {'yes' if options.disable_media_assets else 'no'}")
    print(f"  lighten responsive images: {'yes' if options.lighten_responsive_images else 'no'}")
    print(f"  edit CSS: {'yes' if options.inject_edit_css else 'no'}")
    print(f"  runtime guard: {'yes' if options.inject_runtime_guard else 'no'}")
    for path in targets:
        patch_to_edit(path, options)
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
