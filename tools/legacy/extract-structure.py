#!/usr/bin/env python3
"""
Extracts the meaningful content hierarchy from index.html into LLM-friendly JSON.

Output: website-structure.json (hierarchical) + website-structure.txt (flat)

Only captures:
  - Sections with ids/headings
  - Text content (headings, paragraphs, list items)
  - Interactive elements (links, buttons, forms, tabs)
  - Structured data (product cards, feature lists)
  - Navigation, footer
Skips: SVG internals, script/style content, empty wrappers, styling-only divs.
"""

import json
import re
import sys
from pathlib import Path


def get_text(el):
    """Get trimmed text from a BeautifulSoup element."""
    text = el.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def is_container_tag(tag):
    return tag in ("div", "span", "section", "article", "main", "header", "footer", "nav", "aside")


def should_skip(el):
    if el.name in ("script", "style", "noscript", "svg", "path", "g", "defs", "use", "symbol", "clipPath", "mask"):
        return True
    if el.name == "meta":
        return True
    return False


def extract_structure(soup):
    """Extract content hierarchy, skipping non-content nodes."""
    result = {"page": {"title": "", "tagline": ""}, "sections": []}

    if soup.title:
        result["page"]["title"] = get_text(soup.title)

    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        result["page"]["tagline"] = meta["content"].strip()

    def extract(el, depth=0, in_table=False):
        """Recursively extract meaningful content."""
        if should_skip(el):
            return None

        tag = el.name
        tag_id = (el.get("id") or "").strip()
        classes = " ".join(el.get("class", [])) if el.get("class") else ""
        text = get_text(el)

        # Content-bearing tags
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if text:
                return {"tag": tag, "id": tag_id, "text": text[:500]}

        if tag == "p":
            if text:
                return {"tag": tag, "text": text[:500]}

        if tag == "li":
            if text:
                return {"tag": "li", "text": text[:500]}

        if tag == "a":
            href = el.get("href", "")
            if text and href and not href.startswith("#") and not href.startswith("javascript"):
                return {"tag": "a", "text": text[:200], "href": href[:200]}
            if text and (tag_id or "btn" in classes.lower() or "link" in classes.lower()):
                return {"tag": "a", "text": text[:200], "href": href[:200]}

        if tag == "img":
            alt = el.get("alt", "").strip()
            src = (el.get("src") or "").strip()
            if alt:
                return {"tag": "img", "alt": alt[:300], "src": src[:80]}

        if tag == "button":
            if text:
                return {"tag": "button", "text": text[:200], "type": el.get("type", "")}

        if tag == "input":
            input_type = el.get("type", "text")
            if input_type not in ("hidden", "submit"):
                return {
                    "tag": "input",
                    "type": input_type,
                    "name": (el.get("name") or "")[:100],
                    "placeholder": (el.get("placeholder") or "")[:200],
                }

        if tag == "label":
            if text:
                return {"tag": "label", "text": text[:300]}

        if tag == "textarea":
            return {"tag": "textarea", "name": (el.get("name") or "")[:100], "placeholder": (el.get("placeholder") or "")[:200]}

        if tag == "select":
            options = []
            for opt in el.find_all("option", recursive=False):
                opt_text = get_text(opt)
                if opt_text:
                    options.append(opt_text[:200])
            if options:
                return {"tag": "select", "name": (el.get("name") or "")[:100], "options": options}

        if tag == "form":
            children = extract_children(el, depth + 1)
            form_node = {
                "tag": "form",
                "name": el.get("name") or el.get("id") or "",
                "action": (el.get("action") or "")[:200],
            }
            if children:
                form_node["children"] = children
            return form_node

        # Table
        if tag == "table":
            children = extract_children(el, depth + 1, in_table=True)
            if children:
                return {"tag": "table", "children": children}

        if tag == "tr":
            cells = []
            for cell in el.find_all(["td", "th"], recursive=False):
                cell_text = get_text(cell)
                if cell_text:
                    cells.append(cell_text[:200])
            if cells:
                return {"tag": "tr", "cells": cells}

        # For content containers
        if is_container_tag(tag):
            # Always extract children first — never let an unrecognized wrapper
            # block traversal to meaningful content inside it
            children = extract_children(el, depth + 1, in_table)

            # Check if this container has substantial direct text content
            # (common in utility-class-driven HTML where <p> isn't used)
            direct_text = ""
            for c in el.children:
                if isinstance(c, str) and c.strip():
                    direct_text += c.strip() + " "
            direct_text = direct_text.strip()
            has_direct_text = len(direct_text) > 30

            # Define meaningful class patterns
            meaningful_classes = {
                "hero", "menu", "navbar", "nav", "footer", "header",
                "section", "container", "slide", "card", "tab",
                "form", "btn", "button", "link", "list", "grid",
                "wrap", "wrapper", "content", "title", "heading",
                "benefit", "feature", "product", "pricing",
                "overlay", "modal", "popup", "preloader",
                "design", "estimate", "shop", "intro",
            }

            has_meaningful_class = any(
                mc in classes.lower().replace("-", " ").replace("_", " ").split()
                for mc in meaningful_classes
            )

            meaningful = tag_id or has_meaningful_class or has_direct_text or depth == 0

            if meaningful:
                node = {"tag": tag}
                if tag_id and not tag_id.startswith("w-node-"):
                    node["id"] = tag_id
                if classes:
                    node["class"] = classes[:200]
                if has_direct_text and not children:
                    node["text"] = direct_text[:500]
                if children:
                    node["children"] = children
                return node

            # Transparent wrapper: pass children up
            if children:
                return children if len(children) > 1 else children[0]

            return None

        # Default: skip non-content elements
        return None

    def extract_children(parent, depth, in_table=False):
        """Extract meaningful children, collapsing empty wrappers."""
        if depth > 15:
            return None
        children = []
        for child in parent.children:
            if isinstance(child, str):
                continue
            extracted = extract(child, depth, in_table)
            if extracted is not None:
                children.append(extracted)

        # If only one child that is a container with same tag, merge upward
        if len(children) == 1 and isinstance(children[0], dict):
            c = children[0]
            if is_container_tag(c.get("tag", "")) and not c.get("id") and len(c.get("children", [])) >= 1:
                if not c.get("id") and not c.get("text"):
                    return c.get("children")

        return children if children else None

    # Extract sections in order
    section_selectors = [
        ("nav.navbar, .menu", "navigation"),
        ("#hero", "hero"),
        ("#intro", "intro"),
        ("#design-section, .design-container._1, #design-section ~ div.design-container", "design"),
        ("#design-2, .design-container._2", "design"),
        ("#estimate-section, .estimate-container", "estimate"),
        ("#shop-section, .shop-container", "shop"),
        ("#benefit, .section-benefit", "benefits"),
        ("#demo, #demo ~ section, section.gray.s-form", "cta"),
        ("#footer, section.linear-gradient:last-of-type", "footer"),
    ]

    seen_els = set()

    for selector, stype in section_selectors:
        elements = soup.select(selector)
        for el in elements:
            if el in seen_els:
                continue
            seen_els.add(el)
            el_id = (el.get("id") or "").strip()
            if el_id.startswith("w-node-"):
                el_id = ""
            children = extract_children(el, 0)
            if children:
                node = {"_type": stype}
                if el_id:
                    node["id"] = el_id
                tag = el.name
                if tag and tag != "div":
                    node["tag"] = tag

                # Get heading text for this section
                h = el.find(["h1", "h2", "h3"])
                if h:
                    ht = get_text(h)
                    if ht:
                        node["heading"] = ht[:300]

                node["children"] = children
                result["sections"].append(node)

    return result


def flatten(structure):
    """Flatten the tree into a list of entries with hierarchy paths."""
    flat = []

    def walk(node, path_parts):
        if isinstance(node, list):
            for child in node:
                walk(child, path_parts)
            return
        if not isinstance(node, dict):
            return
        tag = node.get("tag", "")
        tag_id = node.get("id", "")
        heading = node.get("heading", "")
        text = node.get("text", "")
        stype = node.get("_type", "")

        label = f"{tag}#{tag_id}" if tag_id else tag
        if stype:
            label += f" [{stype}]"
        if heading:
            label += f" = {heading}"

        entry = {
            "path": " > ".join(path_parts + [label]),
            "type": stype or tag,
        }
        if heading:
            entry["heading"] = heading[:300]
        if text:
            entry["text"] = text[:500]

        # Collect all leaf text
        leaf_texts = extract_leaf_texts(node)
        if leaf_texts:
            entry["content"] = leaf_texts

        flat.append(entry)

        for child in node.get("children", []):
            walk(child, path_parts + [label])

    def extract_leaf_texts(node):
        """Get all text from leaf nodes (headings, paragraphs, links, list items)."""
        if isinstance(node, list):
            texts = []
            for child in node:
                texts.extend(extract_leaf_texts(child))
            return texts
        if not isinstance(node, dict):
            return []
        texts = []
        if node.get("text") and node.get("tag") in ("p", "li", "a", "button", "h1", "h2", "h3", "h4", "h5", "h6"):
            texts.append(node["text"])
        for child in node.get("children", []):
            texts.extend(extract_leaf_texts(child))
        return texts

    for section in structure.get("sections", []):
        walk(section, [])

    return flat


def generate_llm_view(structure):
    """Generate a clean structured text view for LLM consumption."""
    lines = ["# PAGE STRUCTURE OVERVIEW"]
    lines.append(f"Title: {structure['page']['title']}")
    if structure['page'].get('tagline'):
        lines.append(f"Tagline: {structure['page']['tagline']}")
    lines.append("")

    def render(node, indent=0):
        if isinstance(node, list):
            for child in node:
                render(child, indent)
            return
        prefix = "  " * indent
        tag = node.get("tag", "")
        tag_id = node.get("id", "")
        heading = node.get("heading", "")
        text = node.get("text", "")
        stype = node.get("_type", "")
        cls = node.get("class", "")

        parts = [f"<{tag}>"]
        if tag_id:
            parts.append(f"#{tag_id}")
        if stype:
            parts.append(f"[{stype}]")

        content = parts[0]
        if heading:
            content += f" HEADING: \"{heading}\""
        elif text and len(text) < 100:
            content += f" \"{text}\""

        lines.append(prefix + content)

        if text and len(text) >= 100:
            lines.append(prefix + f"  text: \"{text[:200]}...\"")

        # Show direct children text inline
        for child in node.get("children", []):
            if isinstance(child, list):
                continue
            child_text = child.get("text", "")
            child_tag = child.get("tag", "")
            child_id = child.get("id", "")
            if child_text and child_tag in ("p", "li", "a", "button", "label"):
                label = f"<{child_tag}>"
                if child_id:
                    label += f" #{child_id}"
                lines.append(prefix + f"  {label} \"{child_text[:200]}\"")
            elif child_tag == "img":
                alt = child.get("alt", "")
                if alt:
                    lines.append(prefix + f"  <img> alt=\"{alt[:200]}\"")
            elif child_tag == "form":
                lines.append(prefix + f"  <form> {child.get('name', '')}")
                for field in child.get("children", []):
                    if field.get("tag") in ("input", "textarea"):
                        ft = field.get("type", field.get("tag", ""))
                        fn = field.get("name", "")
                        fp = field.get("placeholder", "")
                        label = f"    [{ft}] \"{fn}\""
                        if fp:
                            label += f" placeholder=\"{fp}\""
                        lines.append(prefix + label)

        # Recurse for all children (structural, headings, lists from transparent wrappers, etc.)
        for child in node.get("children", []):
            if isinstance(child, list):
                for c in child:
                    render(c, indent + 1)
            elif child.get("tag") in ("div", "span", "section", "article", "main", "nav", "header", "footer", "aside", "h1", "h2", "h3", "h4", "h5", "h6"):
                render(child, indent + 1)

    for section in structure.get("sections", []):
        render(section)
        lines.append("")

    return "\n".join(lines)


def main():
    html_path = Path("index.html")
    if not html_path.exists():
        print(f"ERROR: {html_path} not found")
        sys.exit(1)

    print(f"Extracting structure from {html_path}...")

    from bs4 import BeautifulSoup
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    structure = extract_structure(soup)

    # Write hierarchical JSON
    json_path = Path("website-structure.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    print(f"Written {json_path} ({json_path.stat().st_size / 1024:.1f} KB)")

    # Write flat section list
    flat = flatten(structure)
    flat_path = Path("website-sections.json")
    with open(flat_path, "w", encoding="utf-8") as f:
        json.dump(flat, f, indent=2, ensure_ascii=False)
    print(f"Written {flat_path} ({flat_path.stat().st_size / 1024:.1f} KB, {len(flat)} sections)")

    # Write LLM-friendly text view
    text_path = Path("website-structure.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(generate_llm_view(structure))
    print(f"Written {text_path} ({text_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
