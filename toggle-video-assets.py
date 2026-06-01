#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

BASE = Path(__file__).resolve().parent
HTML_FILE = BASE / "index-standalone-rebuilt.html"
MANIFEST_FILE = BASE / "index-standalone.video-assets.json"

VIDEO_BLOCK_RE = re.compile(
    r'<div\b(?=[^>]*\bclass="[^"]*\bvideo-1\b[^"]*\bw-background-video\b[^"]*")[\s\S]*?</video></div>'
)
PLACEHOLDER_RE = re.compile(
    r'<div data-video-placeholder="true" data-video-index="(\d+)" class="video-1 w-background-video w-background-video-atom"></div>'
)


def normalize_enabled_video_markup(html: str) -> str:
    """Undo the older lightweight toggle format if the file is currently using it."""
    html = html.replace("data-disabled-poster-url=", "data-poster-url=")
    html = html.replace("data-disabled-video-urls=", "data-video-urls=")
    html = html.replace("<source data-disabled-src=", "<source src=")
    html = html.replace(' data-disabled-autoplay=""', ' autoplay=""')
    html = html.replace(
        ' data-disabled-style="background-image:url(&quot;assets/',
        ' style="background-image:url(&quot;assets/',
    )
    html = re.sub(r"<video\s+preload=\"none\"", "<video", html)
    return html


def status(html: str) -> str:
    if PLACEHOLDER_RE.search(html):
        return "off"
    if VIDEO_BLOCK_RE.search(html):
        return "on"
    return "unknown"


def turn_off(html: str) -> tuple[str, int]:
    html = normalize_enabled_video_markup(html)
    blocks = VIDEO_BLOCK_RE.findall(html)
    if not blocks:
        return html, 0

    MANIFEST_FILE.write_text(
        json.dumps({"blocks": blocks}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    def replacement(match: re.Match[str]) -> str:
        idx = len(replacement.seen)
        replacement.seen.append(idx)
        return (
            f'<div data-video-placeholder="true" data-video-index="{idx}" '
            'class="video-1 w-background-video w-background-video-atom"></div>'
        )

    replacement.seen = []  # type: ignore[attr-defined]
    return VIDEO_BLOCK_RE.sub(replacement, html), len(blocks)


def turn_on(html: str) -> tuple[str, int]:
    if not MANIFEST_FILE.exists():
        return normalize_enabled_video_markup(html), 0

    data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    blocks = data.get("blocks", [])

    def replacement(match: re.Match[str]) -> str:
        idx = int(match.group(1))
        try:
            return blocks[idx]
        except IndexError:
            return match.group(0)

    next_html, count = PLACEHOLDER_RE.subn(replacement, html)
    return next_html, count


def main() -> int:
    if not HTML_FILE.exists():
        print(f"Missing {HTML_FILE}", file=sys.stderr)
        return 1

    command = sys.argv[1].lower() if len(sys.argv) > 1 else "toggle"
    if command not in {"toggle", "on", "off", "status"}:
        print("Usage: ./toggle-video-assets.py [toggle|on|off|status]", file=sys.stderr)
        return 2

    html = HTML_FILE.read_text(encoding="utf-8")
    current = status(html)

    if command == "status":
        print(f"video assets: {current}")
        return 0

    target_off = command == "off" or (command == "toggle" and current != "off")
    next_html, changed = turn_off(html) if target_off else turn_on(html)

    HTML_FILE.write_text(next_html, encoding="utf-8")
    print("video assets: off" if target_off else "video assets: on")
    print(f"video blocks changed: {changed}")
    print(f"manifest: {MANIFEST_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
