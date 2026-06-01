#!/usr/bin/env python3
"""
Serve a heavy Webflow/static export in two modes:

  edit mode: strips/neutralizes heavy animation/runtime code in memory
  full mode: serves the original files untouched

Usage:
  python3 tools/report_server.py --port 8090 --mode edit
  python3 tools/report_server.py --port 8091 --mode full

Then open:
  http://127.0.0.1:8090/       # edit-safe preview
  http://127.0.0.1:8091/       # real full preview

You can also override per request:
  http://127.0.0.1:8090/?mode=full
  http://127.0.0.1:8090/?mode=edit
"""

from __future__ import annotations

import argparse
import html
import mimetypes
import os
import re
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]

EDIT_CSS_HREF = "/assets/pinegrow-edit-mode.css"

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

EDIT_MODE_SCRIPT = r"""
<script data-pinegrow-edit-mode="runtime-guard">
(function () {
  window.__PINEGROW_EDIT_MODE__ = true;

  // Make common animation libraries harmless if inline code still references them.
  const noop = function () { return this; };
  const chain = new Proxy(function () {}, {
    get() { return chain; },
    apply() { return chain; }
  });

  window.gsap = window.gsap || {
    timeline: function () { return { to: noop, from: noop, fromTo: noop, set: noop, play: noop, pause: noop, progress: noop }; },
    set: noop,
    to: noop,
    from: noop,
    fromTo: noop,
    registerPlugin: noop
  };
  window.ScrollTrigger = window.ScrollTrigger || { create: noop, refresh: noop, killAll: noop };
  window.CustomEase = window.CustomEase || { create: function () { return "none"; } };
  window.SplitType = window.SplitType || function () { return { revert: noop }; };

  window.addEventListener("DOMContentLoaded", function () {
    document.documentElement.classList.add("pinegrow-edit-mode");
    document.documentElement.classList.remove("w-mod-ix");
    document.querySelectorAll("[text-split], [text-split-delay]").forEach(function (el) {
      el.style.opacity = "1";
    });
    document.querySelectorAll(".preloader").forEach(function (el) {
      el.style.display = "none";
    });
    document.body.style.position = "";
    document.body.style.top = "";
    document.body.style.left = "";
    document.body.style.right = "";
    document.body.style.width = "";
  });
})();
</script>
"""

BANNER = r"""
<div data-pinegrow-edit-mode="banner" style="position:fixed;z-index:2147483647;right:12px;bottom:12px;background:#111;color:#fff;font:12px/1.4 system-ui,-apple-system,Segoe UI,sans-serif;padding:8px 10px;border-radius:8px;opacity:.78;pointer-events:none">
  Pinegrow edit mode: animations disabled
</div>
"""


def is_heavy_external_script(tag: str) -> bool:
    src_match = re.search(r"\bsrc\s*=\s*(['\"])(.*?)\1", tag, flags=re.I | re.S)
    if not src_match:
        return False
    src = src_match.group(2).lower()
    return any(pattern in src for pattern in HEAVY_EXTERNAL_SCRIPT_PATTERNS)


def is_heavy_inline_script(tag: str) -> bool:
    # External script tags are handled separately.
    if re.search(r"\bsrc\s*=", tag, flags=re.I):
        return False
    lowered = tag.lower()
    return any(pattern.lower() in lowered for pattern in HEAVY_INLINE_SCRIPT_PATTERNS)


def strip_heavy_scripts(document: str) -> str:
    def replace_script(match: re.Match[str]) -> str:
        tag = match.group(0)
        if is_heavy_external_script(tag) or is_heavy_inline_script(tag):
            summary = html.escape(tag[:120].replace("\n", " "))
            return f"<!-- pinegrow-edit-mode stripped script: {summary}... -->"
        return tag

    return re.sub(r"<script\b[^>]*>.*?</script>", replace_script, document, flags=re.I | re.S)


def inject_edit_mode(document: str) -> str:
    if "data-pinegrow-edit-mode" in document:
        return document

    css_link = f'<link rel="stylesheet" href="{EDIT_CSS_HREF}" data-pinegrow-edit-mode="css">'

    if "</head>" in document.lower():
        document = re.sub(r"</head>", css_link + "\n" + EDIT_MODE_SCRIPT + "\n</head>", document, count=1, flags=re.I)
    else:
        document = css_link + "\n" + EDIT_MODE_SCRIPT + "\n" + document

    if "</body>" in document.lower():
        document = re.sub(r"</body>", BANNER + "\n</body>", document, count=1, flags=re.I)
    else:
        document += BANNER

    return document


def transform_html(document: str, mode: str) -> str:
    if mode != "edit":
        return document
    document = strip_heavy_scripts(document)
    document = inject_edit_mode(document)
    return document


class ReportHandler(SimpleHTTPRequestHandler):
    server_version = "ReportEditServer/1.0"

    def translate_path(self, path: str) -> str:
        parsed = urlparse(path)
        clean = unquote(parsed.path).lstrip("/")
        if clean == "" or clean.endswith("/"):
            clean = clean + "index.html"
        return str((ROOT / clean).resolve())

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        mode = query.get("mode", [self.server.mode])[0]
        if mode not in {"edit", "full"}:
            mode = self.server.mode

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
            body = transform_html(raw, mode).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        ctype = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve this report with optional Pinegrow edit mode.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--mode", choices=["edit", "full"], default=os.environ.get("REPORT_MODE", "edit"))
    args = parser.parse_args()

    os.chdir(ROOT)
    server = ThreadingHTTPServer((args.host, args.port), ReportHandler)
    server.mode = args.mode

    print(f"Serving {ROOT}")
    print(f"Default mode: {args.mode}")
    print(f"Open: http://{args.host}:{args.port}/")
    print(f"Edit mode override: http://{args.host}:{args.port}/?mode=edit")
    print(f"Full mode override: http://{args.host}:{args.port}/?mode=full")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
