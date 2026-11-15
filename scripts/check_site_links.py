#!/usr/bin/env python3
"""
check_site_links.py: Validates all website links and asset references in HTML files.
Zero external dependencies (uses standard library only).

Validates:
- Local assets: <img src>, <link href>, <script src>, <source src>, <video src>.
- Internal navigation: <a href="page.html"> or clean URLs like <a href="/about">.
- In-page anchors: <a href="#id"> verifies element with id="id" exists in target.
- Dead placeholders: Detects and flags href="#" dead ends.
- External URLs: Verifies protocol/syntax, with optional --online flag for live HTTP checks.
- Optional --allow-planned: Treats unbuilt planned pages as warnings rather than fatal errors during drafting.
"""

import sys
import os
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


class HTMLReferenceExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.declared_ids = set()

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        # Record element IDs for anchor validation
        if "id" in attr_dict:
            self.declared_ids.add(attr_dict["id"])
        if tag == "a" and "name" in attr_dict:
            self.declared_ids.add(attr_dict["name"])

        line_num, _ = self.getpos()

        # Check links
        if tag == "a" and "href" in attr_dict:
            self.references.append({
                "type": "link",
                "tag": tag,
                "target": attr_dict["href"],
                "line": line_num
            })

        # Check assets (images, stylesheets, scripts, videos, audio)
        for attr, ref_type in [("src", "asset"), ("href", "stylesheet")]:
            if attr in attr_dict:
                if tag in ("img", "script", "source", "video", "audio", "iframe") and attr == "src":
                    self.references.append({
                        "type": ref_type,
                        "tag": tag,
                        "target": attr_dict[attr],
                        "line": line_num
                    })
                elif tag == "link" and attr_dict.get("rel") in ("stylesheet", "icon", "shortcut icon") and attr == "href":
                    self.references.append({
                        "type": ref_type,
                        "tag": tag,
                        "target": attr_dict[attr],
                        "line": line_num
                    })


def check_external_url(url: str, timeout: int = 5) -> tuple:
    """Sends an HTTP HEAD request to check if an external URL is reachable."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0 Safari/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return True, response.status
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return True, f"HTTP {e.code} (auth/bot protected)"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def check_html_file(file_path: Path, repo_root: Path, all_html_files: dict, online_check: bool, allow_planned: bool) -> dict:
    results = {
        "file": str(file_path.relative_to(repo_root)),
        "errors": [],
        "warnings": [],
        "checked_assets": 0,
        "checked_links": 0,
        "checked_external": 0,
    }

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        results["errors"].append({"line": 0, "target": "", "error": f"Failed to read file: {e}"})
        return results

    parser = HTMLReferenceExtractor()
    try:
        parser.feed(content)
    except Exception as e:
        results["errors"].append({"line": 0, "target": "", "error": f"HTML parse error: {e}"})
        return results

    for ref in parser.references:
        target = ref["target"].strip()
        line = ref["line"]
        ref_type = ref["type"]

        # 1. Detect dead '#' placeholder links
        if target == "#":
            results["warnings"].append({
                "line": line,
                "target": target,
                "warning": "Dead placeholder link (href=\"#\"). Wire to a real page or platform root."
            })
            continue

        # 2. Check external URLs
        if target.startswith(("http://", "https://")):
            results["checked_external"] += 1
            if online_check:
                is_ok, detail = check_external_url(target)
                if not is_ok:
                    results["errors"].append({
                        "line": line,
                        "target": target,
                        "error": f"External link unreachable: {detail}"
                    })
            continue

        if target.startswith(("mailto:", "tel:", "javascript:")):
            continue

        # 3. Parse internal URL / path
        parsed = urllib.parse.urlparse(target)
        url_path = urllib.parse.unquote(parsed.path)
        fragment = parsed.fragment

        # Check local assets (src, stylesheet href)
        if ref_type in ("asset", "stylesheet"):
            results["checked_assets"] += 1
            if url_path.startswith("/"):
                asset_path = (repo_root / url_path.lstrip("/")).resolve()
            else:
                asset_path = (file_path.parent / url_path).resolve()

            if not asset_path.exists():
                results["errors"].append({
                    "line": line,
                    "target": target,
                    "error": f"Asset file missing on disk: {url_path}"
                })
            continue

        # Check internal navigation links (<a href>)
        results["checked_links"] += 1
        if url_path:
            if url_path.startswith("/"):
                clean = url_path.strip("/")
                if clean == "":
                    target_file = (repo_root / "index.html").resolve()
                elif (repo_root / f"{clean}.html").exists():
                    target_file = (repo_root / f"{clean}.html").resolve()
                else:
                    target_file = (repo_root / clean).resolve()
            else:
                target_file = (file_path.parent / url_path).resolve()

            if not target_file.exists():
                msg = f"Target page not found: {url_path}"
                if allow_planned and url_path in ("about.html", "product.html", "shop.html", "/about", "/product", "/shop"):
                    results["warnings"].append({
                        "line": line,
                        "target": target,
                        "warning": f"Target page is currently planned/unbuilt: {url_path}"
                    })
                else:
                    results["errors"].append({
                        "line": line,
                        "target": target,
                        "error": msg
                    })
            elif fragment:
                target_rel = str(target_file.relative_to(repo_root))
                target_ids = all_html_files.get(target_rel, set())
                if fragment not in target_ids:
                    results["errors"].append({
                        "line": line,
                        "target": target,
                        "error": f"Anchor '#{fragment}' not found in {target_file.name}"
                    })
        elif fragment:
            if fragment not in parser.declared_ids:
                results["errors"].append({
                    "line": line,
                    "target": target,
                    "error": f"In-page anchor '#{fragment}' not found in {file_path.name}"
                })

    return results


def main():
    repo_root = Path(__file__).resolve().parent.parent
    online_check = "--online" in sys.argv
    allow_planned = "--allow-planned" in sys.argv

    print(f"Checking website links and assets in: {repo_root}")
    if online_check:
        print("Mode: Live external network checks enabled.")
    if allow_planned:
        print("Mode: Planned pages permitted as warnings.")
    print("=" * 60)

    html_files = list(repo_root.glob("*.html"))

    if not html_files:
        print("No HTML files found at repository root.")
        sys.exit(1)

    all_html_files = {}
    for hf in html_files:
        p = HTMLReferenceExtractor()
        try:
            p.feed(hf.read_text(encoding="utf-8"))
            all_html_files[str(hf.relative_to(repo_root))] = p.declared_ids
        except Exception:
            pass

    total_errors = 0
    total_warnings = 0
    total_assets = 0
    total_links = 0
    total_external = 0

    for hf in sorted(html_files):
        res = check_html_file(hf, repo_root, all_html_files, online_check, allow_planned)
        total_assets += res["checked_assets"]
        total_links += res["checked_links"]
        total_external += res["checked_external"]

        print(f"\n[{res['file']}]")
        print(f"  Assets checked: {res['checked_assets']}")
        print(f"  Internal links checked: {res['checked_links']}")
        print(f"  External links checked: {res['checked_external']}")

        if res["warnings"]:
            total_warnings += len(res["warnings"])
            for w in res["warnings"]:
                print(f"  ⚠ Warning [line {w['line']}]: {w['target']} -> {w['warning']}")

        if res["errors"]:
            total_errors += len(res["errors"])
            for e in res["errors"]:
                print(f"  ✗ ERROR [line {e['line']}]: {e['target']} -> {e['error']}")

    print("\n" + "=" * 60)
    print(f"SUMMARY: {len(html_files)} page(s) checked.")
    print(f"  Total assets: {total_assets} verified")
    print(f"  Total internal links: {total_links} verified")
    print(f"  Total external links: {total_external} checked")
    print(f"  Warnings: {total_warnings}")
    print(f"  Errors: {total_errors}")

    if total_errors > 0:
        print("\nResult: FAILED (resolve broken assets or page links above).")
        sys.exit(1)
    else:
        print("\nResult: PASSED (all asset paths and internal pages resolve cleanly).")
        sys.exit(0)


if __name__ == "__main__":
    main()
