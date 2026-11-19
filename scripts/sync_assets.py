#!/usr/bin/env python3
"""Copy the team's source assets into the website's own assets/ folder.

The team keeps its working files (posters, video, mascot, team photos, and
merch mockups) outside this repository. The website must carry its own web
copies so it deploys standalone. This script is the one mechanical path from
those source files to assets/: every output, its source, and its recipe are
listed in ASSETS below, so nobody copies or resizes files by hand.

It records each source's size and modified time in assets/asset-sources.json.
A later run rebuilds only the outputs whose source changed, whose recipe
changed, or whose output file is missing.

Usage:
  python3 scripts/sync_assets.py            # rebuild what is stale
  python3 scripts/sync_assets.py --check    # list stale outputs, exit 1 if any
  python3 scripts/sync_assets.py --force    # rebuild everything
  python3 scripts/sync_assets.py --source /path/to/ponce-advertising

The source root defaults to $VIVE_SOURCE, then to the team folder below.
Needs Pillow, ffmpeg (video), and macOS qlmanage (PDF posters).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

SITE = Path(__file__).resolve().parent.parent
LOCK = SITE / "assets" / "asset-sources.json"
DEFAULT_SOURCE = Path.home() / "client-work/pineapple/training/ponce-advertising"

# Each entry: output path (relative to the site root), source path (relative
# to the source root), and a recipe. Recipes:
#   ("fit", N)          longest side at most N px, keep transparency, WebP
#   ("height", N)       height exactly N px, WebP
#   ("square", N)       center-crop to a square, then N x N px, WebP
#   ("pdf", N)          rasterize page 1 of a PDF, trim light export lines off
#                       its edges, then N px tall, WebP
#   ("video", N)        H.264 MP4 at most N px wide, AAC audio, fast start
#   ("frame", seconds)  one video frame as WebP, for the <video> poster
#   ("cutout-square", N) cut the product out of its background (cutout.swift),
#                       then center it on an N x N light studio square. For
#                       mockups exported with a fake transparency checkerboard.
#   ("portrait", n)     team photo on a PORTRAIT canvas with the face at the
#                       same size and spot in every photo (face found by
#                       scripts/face_boxes.swift, macOS Vision). A photo with
#                       no transparency is cut out first by scripts/cutout.swift.
#                       n is a version; bump it to force a rebuild.
#   ("vivi-icon", N)    VIVI's head (arms and shirt masked off) on a rounded
#                       deep blue tile, N x N PNG. A .ico output holds 16, 32, and
#                       48 px.
#   ("vivi-touch-icon", N) the same head on a square deep blue tile with no rounded
#                       corners, because iOS rounds home-screen icons itself.
ASSETS: list[tuple[str, str, tuple]] = [
    # Home: John Madrid's Christmas poster (v3 is the final export)
    ("assets/seasonal/christmas-madrid-full.webp", "[Madrid] John Madrid v3.pdf", ("pdf", 2000)),
    ("assets/seasonal/christmas-madrid-thumb.webp", "[Madrid] John Madrid v3.pdf", ("pdf", 900)),
    # Home: the VIVE ad
    ("assets/video/vive-ad.mp4", "video-recordings/VIVE.mp4", ("video", 1920)),
    ("assets/video/vive-ad-poster.webp", "video-recordings/VIVE.mp4", ("frame", 43.0)),
    # Mascot: VIVI
    ("assets/mascot/vivi-pointing.webp", "Mascot/VIVI pointing.png", ("fit", 720)),
    ("assets/mascot/vivi-running.webp", "Mascot/Vivi Running.png", ("fit", 720)),
    ("assets/mascot/vivi-dizzy.webp", "Mascot/VIVI Dizzy.png", ("fit", 720)),
    # Favicon and app icons: VIVI on deep blue
    ("favicon.ico", "Mascot/VIVI pointing.png", ("vivi-icon", 48)),
    ("assets/icons/favicon-32.png", "Mascot/VIVI pointing.png", ("vivi-icon", 32)),
    ("assets/icons/icon-512.png", "Mascot/VIVI pointing.png", ("vivi-icon", 512)),
    ("assets/icons/apple-touch-icon.png", "Mascot/VIVI pointing.png", ("vivi-touch-icon", 180)),
    # About Us: transparent team cutouts
    ("assets/team/venson-sanchez.webp", "About Us Picture/Venson.png", ("portrait", 2)),
    ("assets/team/ayanna-yarra.webp", "About Us Picture/Aya.png", ("portrait", 2)),
    ("assets/team/czar-bambao.webp", "About Us Picture/Czar.png", ("portrait", 2)),
    ("assets/team/louie-latoreno.webp", "About Us Picture/Louie.png", ("portrait", 2)),
    ("assets/team/warren-gumapac.webp", "About Us Picture/Warren.png", ("portrait", 2)),
    ("assets/team/john-madrid.webp", "About Us Picture/Madrid.png", ("portrait", 2)),
    # Shop: merch mockups
    ("assets/merch/baseball-jersey.webp", "vive-mockups/Merch/VIVE Jersey.jpg", ("cutout-square", 900)),
    ("assets/merch/running-set.webp", "vive-mockups/Merch/VIVE-singlet-and-shorts.jpg", ("square", 900)),
    ("assets/merch/jacket.webp", "vive-mockups/Merch/Vive Bomber jacket.jpg", ("square", 900)),
    ("assets/merch/tote-bag.webp", "vive-mockups/Merch/Playful VIVE Tote in Sunlit Studio.png", ("square", 900)),
    ("assets/merch/coasters.webp", "vive-mockups/Merch/VIVE Coasters.jpg", ("square", 900)),
    ("assets/merch/cap.webp", "vive-mockups/Merch/VIVE Cap.jpg", ("square", 900)),
    ("assets/merch/notebook.webp", "vive-mockups/Merch/VIVE-A5-Notebook.jpg", ("square", 900)),
    ("assets/merch/pens.webp", "vive-mockups/Merch/VIVE-pens.jpg", ("square", 900)),
    ("assets/merch/stickers.webp", "vive-mockups/Merch/Sticker VIVE.png", ("square", 900)),
    ("assets/merch/tumbler.webp", "vive-mockups/Merch/VIVE-tumblr.jpg", ("square", 900)),
    ("assets/merch/mug.webp", "vive-mockups/Merch/VIVE-mug.jpg", ("square", 900)),
    ("assets/merch/keychain.webp", "vive-mockups/Merch/I Need More V!VE Keychain.png", ("square", 900)),
    ("assets/merch/scarf.webp", "vive-mockups/Merch/shawl.png", ("square", 900)),
]

WEBP = {"quality": 82, "method": 6}

# Team portrait framing: canvas size, face width, and face top, in pixels.
# A 42% face width keeps cutouts that touch their photo's side edges (Venson,
# Louie) wide enough to hide those edges, and every body reaches the bottom.
# Bump the recipe number in ASSETS after changing these to force a rebuild.
PORTRAIT = {"size": (1000, 1250), "face_w": 420, "face_top": 250}


def save_webp(im: Image.Image, out: Path) -> None:
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    im.save(out, "WEBP", **WEBP)


def fit(src: Path, out: Path, n: int) -> None:
    im = Image.open(src)
    im.thumbnail((n, n), Image.LANCZOS)
    save_webp(im, out)


def height(im: Image.Image, out: Path, n: int) -> None:
    im = im.resize((round(im.width * n / im.height), n), Image.LANCZOS)
    save_webp(im.convert("RGB"), out)


def square(src: Path, out: Path, n: int) -> None:
    im = Image.open(src).convert("RGB")
    s = min(im.size)
    left, top = (im.width - s) // 2, (im.height - s) // 2
    im = im.crop((left, top, left + s, top + s)).resize((n, n), Image.LANCZOS)
    save_webp(im, out)


def pdf(src: Path, out: Path, n: int) -> None:
    # qlmanage renders page 1 with the longest side at the given size
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["qlmanage", "-t", "-s", str(round(n * 1.2)), "-o", tmp, str(src)],
                       check=True, capture_output=True)
        png = next(Path(tmp).glob("*.png"))
        height(trim_light_edges(Image.open(png).convert("RGB")), out, n)


def trim_light_edges(im: Image.Image, depth: float = .01, lift: int = 25) -> Image.Image:
    """Drop thin light lines that PDF exports leave on an edge. A row or column
    within the outer 1% counts as an edge line when it is at least `lift`
    levels brighter than the artwork just inside it."""
    g = im.convert("L")
    w, h = g.size

    def mean_row(y):
        return sum(g.crop((0, y, w, y + 1)).getdata()) / w

    def mean_col(x):
        return sum(g.crop((x, 0, x + 1, h)).getdata()) / h

    def cut(n, mean, inward):
        limit = max(1, int(n * depth))
        ref = mean(inward(limit))
        k = 0
        while k < limit and mean(inward(k)) > ref + lift:
            k += 1
        return k

    top = cut(h, mean_row, lambda k: k)
    bottom = cut(h, mean_row, lambda k: h - 1 - k)
    left = cut(w, mean_col, lambda k: k)
    right = cut(w, mean_col, lambda k: w - 1 - k)
    return im.crop((left, top, w - right, h - bottom))


def video(src: Path, out: Path, n: int) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
                    "-vf", f"scale='min({n},iw)':-2", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", str(out)], check=True)


def frame(src: Path, out: Path, t: float) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "f.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(src),
                        "-frames:v", "1", "-vf", "scale='min(1920,iw)':-2", str(png)], check=True)
        save_webp(Image.open(png).convert("RGB"), out)


def cutout_square(src: Path, out: Path, n: int) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        cut = Path(tmp) / "cutout.png"
        subprocess.run(["swift", str(SITE / "scripts" / "cutout.swift"), str(src), str(cut)],
                       check=True, capture_output=True)
        item = Image.open(cut).convert("RGBA")
        item = item.crop(item.getchannel("A").getbbox())
        item.thumbnail((round(n * .84), round(n * .84)), Image.LANCZOS)
        # Same light studio ground as the team's other mockup photos
        canvas = Image.new("RGBA", (n, n), (244, 244, 242, 255))
        canvas.alpha_composite(item, ((n - item.width) // 2, (n - item.height) // 2))
        save_webp(canvas.convert("RGB"), out)


def portrait(src: Path, out: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        im = Image.open(src)
        if im.mode != "RGBA" or im.getchannel("A").getextrema()[0] == 255:
            cut = Path(tmp) / "cutout.png"
            subprocess.run(["swift", str(SITE / "scripts" / "cutout.swift"), str(src), str(cut)],
                           check=True, capture_output=True)
            src = cut
        place_portrait(src, out)


def place_portrait(src: Path, out: Path) -> None:
    res = subprocess.run(["swift", str(SITE / "scripts" / "face_boxes.swift"), str(src)],
                         check=True, capture_output=True, text=True)
    box = json.loads(res.stdout.strip().splitlines()[-1])
    if box.get("x") is None:
        raise RuntimeError(f"no face found in {src}")
    cw, ch = PORTRAIT["size"]
    k = PORTRAIT["face_w"] / box["w"]
    im = Image.open(src).convert("RGBA")
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    face_cx = (box["x"] + box["w"] / 2) * k
    face_top = box["y"] * k
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    # paste() with the image as its own mask also handles offsets off the canvas
    canvas.paste(im, (round(cw / 2 - face_cx), round(PORTRAIT["face_top"] - face_top)), im)
    save_webp(canvas, out)


# Icon tile color: the site's --deep blue. Brand navy (#2B3990) would hide
# the navy stripes of VIVI's headband. After changing it, delete the icon
# entries from asset-sources.json so the next run rebuilds them.
ICON_TILE = (29, 39, 102)


def vivi_head(src: Path) -> Image.Image:
    """VIVI's V-shaped head with the headband and face, cut from the pointing
    pose. Masks are in the 671 px wide layout of that pose."""
    import numpy as np
    im = Image.open(src).convert("RGBA")
    a = np.array(im).astype(int)
    k = im.width / 671
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    y, x = yy / k, xx / k
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    drop = (y > 300) & (b > r + 30)                       # navy shirt below the headband
    drop |= (y > 290) & (x < 55 + .38 * (y - 45) - 1)     # pointing arm, left of the V
    drop |= (x > 452) & (y > 460)                         # hand on the hip
    drop |= y > 548
    drop |= (y > 405) & (x < 300) & (y > 405 + (x - 195) * 140 / 105)   # neckline
    drop |= (y > 415) & (x >= 300) & (y > 415 + (440 - x) * 130 / 140)
    drop |= (y > 405) & (x < 195)
    drop |= (y > 380) & (r > 230) & (g > 230) & (b > 230)  # white shirt trim
    a[..., 3] = np.where(drop, 0, a[..., 3])
    head = Image.fromarray(a.astype("uint8"))
    return head.crop(head.getbbox())


def vivi_icon(src: Path, out: Path, n: int, rounded: bool = True) -> None:
    S = 512
    tile = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle((0, 0, S - 1, S - 1), 112 if rounded else 0, fill=ICON_TILE)
    head = vivi_head(src)
    h = 448
    w = round(head.width * h / head.height)
    if w > 468:
        w, h = 468, round(head.height * 468 / head.width)
    tile.alpha_composite(head.resize((w, h), Image.LANCZOS), ((S - w) // 2, (S - h) // 2))
    if out.suffix == ".ico":
        tile.save(out, sizes=[(16, 16), (32, 32), (48, 48)])
    elif rounded:
        tile.resize((n, n), Image.LANCZOS).save(out, optimize=True)
    else:
        tile.convert("RGB").resize((n, n), Image.LANCZOS).save(out, optimize=True)


def build(recipe: tuple, src: Path, out: Path) -> None:
    kind, arg = recipe
    out.parent.mkdir(parents=True, exist_ok=True)
    if kind == "fit":
        fit(src, out, arg)
    elif kind == "square":
        square(src, out, arg)
    elif kind == "pdf":
        pdf(src, out, arg)
    elif kind == "video":
        video(src, out, arg)
    elif kind == "frame":
        frame(src, out, arg)
    elif kind == "cutout-square":
        cutout_square(src, out, arg)
    elif kind == "portrait":
        portrait(src, out)
    elif kind == "vivi-icon":
        vivi_icon(src, out, arg)
    elif kind == "vivi-touch-icon":
        vivi_icon(src, out, arg, rounded=False)
    else:
        raise ValueError(f"unknown recipe {kind}")


def fingerprint(src: Path, recipe: tuple) -> dict:
    st = src.stat()
    return {"source": None, "size": st.st_size, "mtime": int(st.st_mtime), "recipe": list(recipe)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path, default=Path(os.environ.get("VIVE_SOURCE", DEFAULT_SOURCE)))
    ap.add_argument("--check", action="store_true", help="report stale outputs and exit 1 if any")
    ap.add_argument("--force", action="store_true", help="rebuild every output")
    args = ap.parse_args()

    if not args.source.is_dir():
        print(f"Source folder not found: {args.source}", file=sys.stderr)
        return 2
    for tool in ("ffmpeg", "qlmanage"):
        if not shutil.which(tool) and not args.check:
            print(f"Warning: {tool} not found; outputs that need it will fail.", file=sys.stderr)

    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    stale, missing_src, built = [], [], 0

    for out_rel, src_rel, recipe in ASSETS:
        src, out = args.source / src_rel, SITE / out_rel
        if not src.exists():
            missing_src.append(src_rel)
            continue
        fp = fingerprint(src, recipe)
        fp["source"] = src_rel
        if args.force or not out.exists() or lock.get(out_rel) != fp:
            stale.append(out_rel)
            if not args.check:
                print(f"build  {out_rel}  <-  {src_rel}")
                build(recipe, src, out)
                lock[out_rel] = fp
                built += 1

    for src_rel in missing_src:
        print(f"MISSING SOURCE  {src_rel}", file=sys.stderr)

    if args.check:
        for out_rel in stale:
            print(f"stale  {out_rel}")
        print(f"{len(stale)} stale, {len(ASSETS) - len(stale) - len(missing_src)} current, {len(missing_src)} missing sources")
        return 1 if stale or missing_src else 0

    # Keep only entries the manifest still lists
    lock = {k: v for k, v in sorted(lock.items()) if any(k == a[0] for a in ASSETS)}
    LOCK.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"{built} built, {len(ASSETS) - built - len(missing_src)} already current, {len(missing_src)} missing sources")
    return 1 if missing_src else 0


if __name__ == "__main__":
    sys.exit(main())
