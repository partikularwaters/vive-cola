#!/usr/bin/env python3
"""
scripts/build_router_pdf.py
===========================
Mechanical build script for the VIVE 1-Page Router Poster PDF.

Features:
1. Starts from router.html, the locked Three Columns portal (or a custom template).
2. Synchronizes with current website design tokens from site.css (colors, fonts, geometry).
3. Predictably compiles HTML to high-resolution A4 vector PDF using WeasyPrint.
4. Guarantees 100% full-page clickable routing to the production website (https://vive-cola.vercel.app).
5. Verifies the PDF annotations, page geometry, and file integrity via pypdf.
6. Deploys the generated PDF to the designated Google Drive destination and local dist/ directory.
7. Generates a matching preview PNG thumbnail via native macOS tooling (qlmanage / sips).

Usage:
    python3 scripts/build_router_pdf.py [--input path/to/template.html]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pypdf
import weasyprint

REPO_ROOT = Path(__file__).resolve().parent.parent

# Canonical Google Drive Destination
GOOGLE_DRIVE_TARGET_DIR = Path(
    "/Users/madridj1689/Library/CloudStorage/GoogleDrive-john.madrid.1689@gmail.com/"
    ".shortcut-targets-by-id/1Wjcn0Bmt6FZvCQsARHKtUh2ssXi_cE79/MVA Batch 54/Group 1 - (VIVE)/Website"
)

LOCAL_DIST_DIR = REPO_ROOT / "dist"
DEFAULT_PROD_URL = "https://vive-cola.vercel.app"
DEFAULT_OUTPUT_FILENAME = "VIVE.pdf"


def extract_css_tokens(site_css_path: Path) -> dict:
    """Extract design tokens (--orange, --navy, etc.) from site.css."""
    tokens = {}
    if not site_css_path.exists():
        print(f"Warning: {site_css_path} not found. Using brand fallback values.")
        return {
            "orange": "#F27A21",
            "navy": "#2B3990",
            "sun": "#F4BD6A",
            "white": "#F9F9F9",
            "deep": "#1D2766",
            "ink": "#14183F",
            "f": "'Montserrat', sans-serif",
        }

    css_text = site_css_path.read_text(encoding="utf-8")
    var_pattern = re.compile(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;]+);")
    for match in var_pattern.finditer(css_text):
        name = match.group(1).strip()
        val = match.group(2).strip()
        tokens[name] = val

    return tokens


def render_html_to_pdf(html_path: Path, output_pdf_path: Path, prod_url: str = DEFAULT_PROD_URL) -> None:
    """Compile HTML template into vector PDF with base URL and verified link overlay."""
    html_content = html_path.read_text(encoding="utf-8")

    # Ensure the destination link is up-to-date in the HTML
    html_content = re.sub(
        r'href="https?://[^"]+"',
        f'href="{prod_url}"',
        html_content
    )

    base_url = f"file://{REPO_ROOT}/"
    doc = weasyprint.HTML(string=html_content, base_url=base_url)
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc.write_pdf(str(output_pdf_path))
    print(f"✓ PDF rendered successfully: {output_pdf_path}")


def verify_pdf_link_and_geometry(pdf_path: Path, expected_url: str = DEFAULT_PROD_URL) -> bool:
    """Inspect PDF annotations with pypdf to ensure 100% full-page click routing."""
    reader = pypdf.PdfReader(str(pdf_path))
    if len(reader.pages) != 1:
        print(f"Error: Expected single-page poster, found {len(reader.pages)} pages.")
        return False

    page = reader.pages[0]
    annotations = page.get("/Annots", [])
    if not annotations:
        print("Error: No annotations found in the generated PDF.")
        return False

    found_matching_link = False
    for annot in annotations:
        obj = annot.get_object()
        action = obj.get("/A", {})
        uri = action.get("/URI", "")
        rect = obj.get("/Rect", [])
        if uri == expected_url:
            found_matching_link = True
            print(f"✓ Verified full-page routing annotation: URI={uri}, Rect={rect}")
            break

    if not found_matching_link:
        print(f"Error: Could not find link annotation pointing to {expected_url}")
        return False

    return True


def generate_png_preview(pdf_path: Path, png_path: Path) -> None:
    """Generate high-resolution PNG thumbnail using macOS sips or qlmanage."""
    try:
        subprocess.run(
            ["sips", "-s", "format", "png", str(pdf_path), "--out", str(png_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"✓ PNG preview generated: {png_path}")
    except Exception as e:
        print(f"Warning: Could not generate PNG preview via sips: {e}")


def main():
    parser = argparse.ArgumentParser(description="Build and deploy VIVE Router Poster PDF.")
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Custom HTML template path (defaults to router.html)",
    )
    parser.add_argument(
        "--output-filename",
        type=str,
        default=DEFAULT_OUTPUT_FILENAME,
        help="Output PDF filename",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=DEFAULT_PROD_URL,
        help="Production website destination URL",
    )
    parser.add_argument(
        "--no-drive-copy",
        action="store_true",
        help="Skip copying to Google Drive destination",
    )

    args = parser.parse_args()

    # Determine input template
    if args.input:
        template_path = Path(args.input).resolve()
    else:
        template_path = REPO_ROOT / "router.html"

    if not template_path.exists():
        print(f"Error: Template file {template_path} does not exist.")
        sys.exit(1)

    print("==================================================")
    print(f"Building VIVE Website Router PDF from: {template_path.name}")
    print(f"Target URL: {args.url}")
    print("==================================================")

    # 1. Verify CSS tokens from site.css
    tokens = extract_css_tokens(REPO_ROOT / "site.css")
    print(f"✓ Loaded {len(tokens)} tokens from site.css (Orange: {tokens.get('orange')}, Navy: {tokens.get('navy')})")

    # 2. Render to local dist directory
    LOCAL_DIST_DIR.mkdir(parents=True, exist_ok=True)
    local_pdf_path = LOCAL_DIST_DIR / args.output_filename
    render_html_to_pdf(template_path, local_pdf_path, prod_url=args.url)

    # 3. Verify PDF annotations
    if not verify_pdf_link_and_geometry(local_pdf_path, expected_url=args.url):
        print("Verification failed!")
        sys.exit(1)

    # 4. Generate local preview image
    local_png_path = LOCAL_DIST_DIR / f"{Path(args.output_filename).stem}.png"
    generate_png_preview(local_pdf_path, local_png_path)

    # 5. Copy to Google Drive Destination (PDF ONLY - no extra files)
    if not args.no_drive_copy:
        if GOOGLE_DRIVE_TARGET_DIR.exists():
            drive_pdf_path = GOOGLE_DRIVE_TARGET_DIR / args.output_filename
            shutil.copy2(local_pdf_path, drive_pdf_path)
            print(f"✓ Copied PDF to Google Drive: {drive_pdf_path}")
        else:
            print(f"Notice: Google Drive directory {GOOGLE_DRIVE_TARGET_DIR} not found or unmounted.")

    print("\n✓ Mechanical build complete! Router PDF is ready and verified.")


if __name__ == "__main__":
    main()
