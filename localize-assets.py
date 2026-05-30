#!/usr/bin/env python3
"""
Downloads all external assets from index.html AND embedded CSS to a local
assets/ directory and rewrites everything to serve them locally.
"""

import hashlib
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path
from collections import OrderedDict

ASSET_DIR = Path("assets")
HTML_FILE = Path("index.html")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Domains to localize
REMOTE_DOMAINS = [
    "cdn.prod.website-files.com",
    "d3e54v103j8qbb.cloudfront.net",
    "r2.vidzflow.com",
]


def is_remote_url(url):
    parsed = urllib.parse.urlparse(url)
    return any(domain in parsed.netloc for domain in REMOTE_DOMAINS)


def url_to_local_path(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lstrip("/")
    if not path:
        path = "index.html"
    path_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    stem, ext = os.path.splitext(path)
    if not ext:
        ext = ".bin"
    safe_stem = stem.replace("/", "_").replace("%", "_")
    filename = f"{safe_stem}_{path_hash}{ext}"
    return f"/{ASSET_DIR / filename}"


def ensure_dir(path):
    os.makedirs(path.parent, exist_ok=True)


def download_file(url, local_path):
    lp = Path(str(local_path).lstrip("/"))
    if lp.exists():
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            ensure_dir(lp)
            with open(lp, "wb") as f:
                f.write(data)
        print(f"  OK   {lp.name}")
        return True
    except Exception as e:
        print(f"  FAIL {url[:80]}  {e}")
        return False


def extract_urls_from_html(html):
    urls = set()
    pats = [
        (r'(?:src|href|data-src|data-poster-url)=["\']([^"\']+)["\']', False),
        (r'data-video-urls=["\']([^"\']+)["\']', True),
        (r'content=["\'][^"\']*?(https?://[^"\']+)["\']', False),
        (r'srcset=["\']([^"\']+)["\']', True),
    ]
    for pat, is_multi in pats:
        for match in re.finditer(pat, html):
            if is_multi:
                for url in re.split(r'[\s,]+', match.group(1)):
                    url = url.strip().split()[0] if url.strip() else ""
                    if url and is_remote_url(url):
                        urls.add(url)
            else:
                url = match.group(1).strip()
                if url and is_remote_url(url):
                    urls.add(url)
    # inline CSS url() and background-image
    for m in re.finditer(r'url\((?:&quot;|["\'])?(https?://[^"\'\)&]+)(?:&quot;|["\'])?\)', html):
        u = m.group(1).strip()
        if is_remote_url(u):
            urls.add(u)
    # style attributes with background-image
    for m in re.finditer(r'background-image:\s*url\((?:&quot;|["\'])?([^"\'\)&]+)', html):
        u = m.group(1).strip()
        if is_remote_url(u):
            urls.add(u)
    return urls


def extract_urls_from_css(css_text):
    urls = set()
    for m in re.finditer(r'url\(["\']?(https?://[^"\'\)]+)["\']?\)', css_text):
        u = m.group(1).strip()
        if is_remote_url(u):
            urls.add(u)
    for m in re.finditer(r'@import\s+["\'](https?://[^"\']+)["\']', css_text):
        u = m.group(1).strip()
        if is_remote_url(u):
            urls.add(u)
    return urls


def rewrite_html(html, url_map):
    def repl_srcset(m):
        parts = []
        for part in m.group(2).split(","):
            part = part.strip()
            if not part:
                continue
            tokens = part.split()
            url = tokens[0]
            if url in url_map:
                tokens[0] = url_map[url]
            parts.append(" ".join(tokens))
        return f'srcset="{", ".join(parts)}"'

    def repl_video(m):
        urls_str = m.group(2)
        parts = [url_map.get(u.strip(), u.strip()) for u in urls_str.split(",")]
        return f'data-video-urls="{",".join(parts)}"'

    def repl_attr(m):
        url = m.group(2)
        if url in url_map:
            return f'{m.group(1)}="{url_map[url]}"'
        return m.group(0)

    def repl_bg(m):
        url = m.group(1)
        if url in url_map:
            return f'background-image:url("{url_map[url]}")'
        return m.group(0)

    html = re.sub(r'(data-video-urls)=["\']([^"\']+)["\']', repl_video, html)
    html = re.sub(r'(srcset)=["\']([^"\']+)["\']', repl_srcset, html)
    html = re.sub(r'(content=["\'][^"\']*?)(https?://[^"\']+)(["\'])',
                  lambda m: m.group(1) + url_map.get(m.group(2), m.group(2)) + m.group(3), html)
    html = re.sub(r'(src|href|data-src|data-poster-url)=["\']([^"\']+)["\']', repl_attr, html)
    html = re.sub(r'background-image:\s*url\((?:&quot;|["\'])?([^"\'\)&]+)', repl_bg, html)
    return html


def rewrite_css(css_text, url_map):
    def repl(m):
        url = m.group(1)
        if url in url_map:
            return f'url("{url_map[url]}")'
        return m.group(0)
    return re.sub(r'url\(["\']?(https?://[^"\'\)]+)["\']?\)', repl, css_text)


def extract_urls_from_js(js_text):
    urls = set()
    for m in re.finditer(r'["\'](https?://(?:cdn\.prod\.website-files\.com|d3e54v103j8qbb\.cloudfront\.net)[^"\']+)["\']', js_text):
        u = m.group(1).strip()
        if is_remote_url(u):
            urls.add(u)
    return urls


def rewrite_js(js_text, url_map):
    def repl(m):
        url = m.group(1)
        if url in url_map:
            return f'"{url_map[url]}"'
        return m.group(0)
    return re.sub(r'["\'](https?://(?:cdn\.prod\.website-files\.com|d3e54v103j8qbb\.cloudfront\.net)[^"\']+)["\']', repl, js_text)


def process_nested_assets(url_map):
    """Scan downloaded CSS/JS files for embedded remote URLs, download, rewrite."""
    print("\n--- Scanning CSS files for embedded URLs ---")
    all_new_urls = OrderedDict()

    for css_path in sorted(ASSET_DIR.glob("*.css")):
        text = css_path.read_text("utf-8", errors="replace")
        new_urls = extract_urls_from_css(text)
        if new_urls:
            for u in new_urls:
                all_new_urls.setdefault(u, url_to_local_path(u))
            print(f"  Found {len(new_urls)} URLs in {css_path.name}")

    print("\n--- Scanning JS files for embedded URLs ---")
    for js_path in sorted(ASSET_DIR.glob("*.js")):
        text = js_path.read_text("utf-8", errors="replace")
        new_urls = extract_urls_from_js(text)
        if new_urls:
            for u in new_urls:
                all_new_urls.setdefault(u, url_to_local_path(u))
            print(f"  Found {len(new_urls)} URLs in {js_path.name}")

    if all_new_urls:
        print(f"\n--- Downloading {len(all_new_urls)} new assets ---")
        for url, local in all_new_urls.items():
            if download_file(url, local):
                url_map[url] = str(local)

    # Rewrite CSS files
    print("\n--- Rewriting CSS files ---")
    for css_path in sorted(ASSET_DIR.glob("*.css")):
        text = css_path.read_text("utf-8", errors="replace")
        new_text = rewrite_css(text, url_map)
        if new_text != text:
            css_path.write_text(new_text, encoding="utf-8")
            print(f"  Updated {css_path.name}")

    # Rewrite JS files
    print("\n--- Rewriting JS files ---")
    for js_path in sorted(ASSET_DIR.glob("*.js")):
        text = js_path.read_text("utf-8", errors="replace")
        new_text = rewrite_js(text, url_map)
        if new_text != text:
            js_path.write_text(new_text, encoding="utf-8")
            print(f"  Updated {js_path.name}")


def main():
    print("=" * 60)
    print("Asset Localizer for makedesign.tech")
    print("=" * 60)

    if not HTML_FILE.exists():
        print(f"ERROR: {HTML_FILE} not found.")
        return

    html = HTML_FILE.read_text(encoding="utf-8")
    print(f"Read {len(html)} bytes from {HTML_FILE}")

    urls = extract_urls_from_html(html)
    print(f"Found {len(urls)} remote asset URLs in HTML")

    # Download HTML assets
    url_map = {}
    total = len(urls)
    print(f"\n--- Downloading {total} assets ---")
    for i, url in enumerate(sorted(urls), 1):
        local_str = url_to_local_path(url)
        url_map[url] = local_str
        local_path = Path(local_str.lstrip("/"))
        if not local_path.exists():
            print(f"  [{i}/{total}] ", end="")
        download_file(url, local_str)

    # Process CSS/JS for embedded URLs
    process_nested_assets(url_map)

    # Rewrite HTML
    print("\n--- Rewriting HTML ---")
    new_html = rewrite_html(html, url_map)
    new_html = re.sub(r'\s+integrity="[^"]+"', '', new_html)
    HTML_FILE.write_text(new_html, encoding="utf-8")
    print(f"Updated {HTML_FILE}")

    # Stats
    total_files = sum(1 for _ in ASSET_DIR.rglob("*") if _.is_file())
    total_size = sum(f.stat().st_size for f in ASSET_DIR.rglob("*") if f.is_file())
    print(f"\nAssets: {total_files} files, {total_size / 1024 / 1024:.1f} MB")

    # Check for remaining remote refs
    remaining = set()
    for ext, text in [("html", HTML_FILE.read_text("utf-8", errors="replace"))]:
        for m in re.finditer(r'(cdn\.prod\.website-files\.com|d3e54v103j8qbb\.cloudfront\.net)', text):
            line_start = max(0, m.start() - 60)
            remaining.add(text[line_start:m.end() + 40].strip())

    css_remaining = set()
    js_remaining = set()
    for css_path in ASSET_DIR.glob("*.css"):
        text = css_path.read_text("utf-8", errors="replace")
        for m in re.finditer(r'(cdn\.prod\.website-files\.com|d3e54v103j8qbb\.cloudfront\.net)', text):
            line_start = max(0, m.start() - 60)
            css_remaining.add(text[line_start:m.end() + 40].strip())
    for js_path in ASSET_DIR.glob("*.js"):
        text = js_path.read_text("utf-8", errors="replace")
        for m in re.finditer(r'(cdn\.prod\.website-files\.com|d3e54v103j8qbb\.cloudfront\.net)', text):
            line_start = max(0, m.start() - 60)
            js_remaining.add(text[line_start:m.end() + 40].strip())

    print(f"\nRemaining remote refs in HTML: {len(remaining)}")
    for r in list(remaining)[:10]:
        print(f"  {r}")
    print(f"Remaining remote refs in CSS: {len(css_remaining)}")
    for r in list(css_remaining)[:10]:
        print(f"  {r}")
    print(f"Remaining remote refs in JS: {len(js_remaining)}")
    for r in list(js_remaining)[:10]:
        print(f"  {r}")

    print("\nDone!")


if __name__ == "__main__":
    main()
