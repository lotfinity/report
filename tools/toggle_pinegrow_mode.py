#!/usr/bin/env python3
"""
Reversibly patch local HTML files for Pinegrow editing.

This is different from tools/report_server.py:
- report_server.py rewrites HTML only while serving to your browser.
- this script rewrites the actual local HTML file so Pinegrow's internal canvas is lighter.

Usage from repo root:
  python3 tools/toggle_pinegrow_mode.py edit
  python3 tools/toggle_pinegrow_mode.py full
  python3 tools/toggle_pinegrow_mode.py status

Default target is index.html. You can pass more files:
  python3 tools/toggle_pinegrow_mode.py edit index.html privacy-policy.html

Safety:
- First edit run creates index.html.pinegrow-full.bak
- full mode restores from that backup
- edit mode is idempotent; running it twice will not double-inject
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


def patch_to_edit(path: Path) -> str:
    backup = path.with_name(path.name + ".pinegrow-full.bak")
    if not backup.exists():
        backup.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

    document = path.read_text(encoding="utf-8", errors="replace")
    document = disable_heavy_scripts(document)
    document = inject_edit_guard(document)
    path.write_text(document, encoding="utf-8")
    return f"edit mode enabled: {path.relative_to(ROOT)}"


def restore_full(path: Path) -> str:
    backup = path.with_name(path.name + ".pinegrow-full.bak")
    if not backup.exists():
        return f"no backup found, unchanged: {path.relative_to(ROOT)}"
    path.write_text(backup.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return f"full mode restored: {path.relative_to(ROOT)}"


def get_status(path: Path) -> str:
    if not path.exists():
        return f"missing: {path.relative_to(ROOT)}"
    document = path.read_text(encoding="utf-8", errors="replace")
    backup = path.with_name(path.name + ".pinegrow-full.bak")
    if START in document and SCRIPT_DISABLED_START in document:
        mode = "edit"
    else:
        mode = "full/original-looking"
    return f"{path.relative_to(ROOT)}: {mode}, backup={'yes' if backup.exists() else 'no'}"


def resolve_targets(names: list[str]) -> list[Path]:
    if not names:
        names = ["index.html"]
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Toggle actual HTML files between Pinegrow edit mode and full mode.")
    parser.add_argument("mode", choices=["edit", "full", "status"])
    parser.add_argument("files", nargs="*", help="HTML files to patch. Default: index.html")
    args = parser.parse_args()

    targets = resolve_targets(args.files)
    for path in targets:
        if args.mode == "edit":
            print(patch_to_edit(path))
        elif args.mode == "full":
            print(restore_full(path))
        else:
            print(get_status(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
