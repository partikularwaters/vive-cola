#!/usr/bin/env python3
"""
check_repo_links.py: Validates internal Markdown links across the repository.
Zero external dependencies (uses standard library only).

Checks:
- Markdown links [text](target) and images ![alt](target).
- Local file existence for relative paths.
- Headings/anchors (#anchor-name) in local targets.
- Flags references to deleted paths (such as obsolete subdirectories).
"""

import sys
import os
import re
import urllib.parse
from pathlib import Path


def slugify_heading(heading_text: str) -> str:
    """GitHub-style markdown heading slugifier."""
    text = heading_text.strip().lower()
    # Remove HTML tags if present
    text = re.sub(r"<[^>]+>", "", text)
    # Remove punctuation except hyphens and spaces
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace spaces with hyphens
    text = re.sub(r"\s+", "-", text)
    return text


def extract_headings(file_path: Path) -> set:
    """Extracts all heading slugs from a markdown file."""
    headings = set()
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return headings

    for line in content.splitlines():
        match = re.match(r"^#{1,6}\s+(.+)$", line)
        if match:
            heading_text = match.group(1).strip()
            headings.add(slugify_heading(heading_text))
    return headings


def check_markdown_file(file_path: Path, repo_root: Path) -> list:
    """Parses a markdown file and validates all internal links."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [{"file": str(file_path), "line": 0, "link": "", "error": f"Failed to read file: {e}"}]

    # Regex for markdown links: [text](target) and images ![alt](target)
    # Excludes pure external links (http/https/mailto) from filesystem checks
    link_pattern = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")

    lines = content.splitlines()
    for line_num, line in enumerate(lines, start=1):
        for match in link_pattern.finditer(line):
            text, target = match.groups()
            target = target.strip()

            # Skip empty targets
            if not target:
                issues.append({
                    "file": str(file_path.relative_to(repo_root)),
                    "line": line_num,
                    "target": target,
                    "error": "Empty link target"
                })
                continue

            # Skip external URLs (checked by site link checker if needed)
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue

            # Parse path and anchor
            parsed = urllib.parse.urlparse(target)
            url_path = urllib.parse.unquote(parsed.path)
            fragment = parsed.fragment

            if url_path:
                # Resolve relative to the markdown file's directory
                resolved_target = (file_path.parent / url_path).resolve()
                try:
                    resolved_target.relative_to(repo_root)
                except ValueError:
                    issues.append({
                        "file": str(file_path.relative_to(repo_root)),
                        "line": line_num,
                        "target": target,
                        "error": f"Link targets path outside repository: {url_path}"
                    })
                    continue

                if not resolved_target.exists():
                    issues.append({
                        "file": str(file_path.relative_to(repo_root)),
                        "line": line_num,
                        "target": target,
                        "error": f"Target file does not exist: {url_path}"
                    })
                    continue

                # If fragment exists and target is markdown, verify heading
                if fragment and resolved_target.suffix.lower() == ".md":
                    headings = extract_headings(resolved_target)
                    if fragment.lower() not in headings:
                        issues.append({
                            "file": str(file_path.relative_to(repo_root)),
                            "line": line_num,
                            "target": target,
                            "error": f"Heading anchor '#{fragment}' not found in {resolved_target.name}"
                        })
            elif fragment:
                # Same-file fragment: check heading in current file
                headings = extract_headings(file_path)
                if fragment.lower() not in headings:
                    issues.append({
                        "file": str(file_path.relative_to(repo_root)),
                        "line": line_num,
                        "target": target,
                        "error": f"In-page heading anchor '#{fragment}' not found in {file_path.name}"
                    })

    return issues


def main():
    repo_root = Path(__file__).resolve().parent.parent
    if len(sys.argv) > 1 and sys.argv[1] not in ("-h", "--help"):
        target_dir = Path(sys.argv[1]).resolve()
    else:
        target_dir = repo_root

    print(f"Checking internal repository links in: {target_dir}")
    print("=" * 60)

    # Collect all Markdown files, skipping git and node_modules
    md_files = []
    for root, dirs, files in os.walk(target_dir):
        # Exclude hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        for f in files:
            if f.endswith(".md"):
                md_files.append(Path(root) / f)

    total_files = len(md_files)
    all_issues = []

    for md_file in sorted(md_files):
        issues = check_markdown_file(md_file, repo_root)
        if issues:
            all_issues.extend(issues)

    if not all_issues:
        print(f"SUCCESS: Scanned {total_files} Markdown files. All internal links and anchors are valid.")
        sys.exit(0)
    else:
        print(f"FAILED: Found {len(all_issues)} link issue(s) across {total_files} files:\n")
        for issue in all_issues:
            print(f"  [{issue['file']}:{issue['line']}] -> {issue['target']}")
            print(f"    Error: {issue['error']}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
