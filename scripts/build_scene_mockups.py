#!/usr/bin/env python3
"""Place the team's transparent can renders into the poster scene photos.

Each scene in assets/scene-*.jpg shows an older deck-era can. This script
covers that can with a new render (bottom-aligned, slightly larger so no old
edge shows), patches the old reflection on table scenes, adds a soft new
reflection or contact shadow, and exports a square crop for the Shop hover
reveal as assets/scene-<can>-web.webp.

Run: python3 scripts/build_scene_mockups.py "<Drive>/Group 1 - (VIVE)/Mockups"
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# can: (scene, old can box x0, y0, x1, y1, surface, cover, reflection patch depth, light)
# cover: new can width relative to the old can, so no old edge shows.
# light: brightness and blue tint that match the can to the room.
SCENES = {
    "classic": ("beach", (300, 305, 537, 905), "sand", 1.14, 0, (1.0, 0.0)),
    "glow": ("living-room", (310, 362, 535, 922), "table", 1.08, 60, (0.9, 0.08)),
    "focus": ("office", (316, 342, 544, 925), "table", 1.08, 52, (0.97, 0.0)),
}
OUT = 800


def load_can(src: Path, name: str) -> Image.Image:
    im = Image.open(src / f"VIVE {name.title()} (Transparent).png").convert("RGBA")
    return im.crop(im.getchannel("A").getbbox())


def patch_reflection(scene: Image.Image, box, depth: int) -> None:
    """Cover the old can's reflection with table texture from beside it."""
    x0, _, x1, y1 = box
    pad = 24
    w = x1 - x0 + 2 * pad
    src_x = x1 + pad + 8 if x1 + pad + 8 + w <= scene.width else x0 - pad - 8 - w
    patch = scene.crop((src_x, y1 - 6, src_x + w, y1 + depth))
    mask = Image.new("L", patch.size, 0)
    ImageDraw.Draw(mask).rectangle((10, 0, w - 10, patch.height), fill=255)
    scene.paste(patch, (x0 - pad, y1 - 6), mask.filter(ImageFilter.GaussianBlur(8)))


def place(scene: Image.Image, can: Image.Image, box, surface: str, cover: float, light) -> None:
    x0, _, x1, y1 = box
    w = round((x1 - x0) * cover)
    h = round(can.height * w / can.width)
    can = can.resize((w, h), Image.LANCZOS)
    bright, tint = light
    a = can.getchannel("A")
    rgb = ImageEnhance.Brightness(can.convert("RGB")).enhance(bright)
    if tint:
        rgb = Image.blend(rgb, Image.new("RGB", rgb.size, (40, 60, 200)), tint)
    can = rgb.convert("RGBA")
    can.putalpha(a)
    left = round((x0 + x1) / 2 - w / 2)
    top = y1 + 3 - h

    if surface == "sand":
        shadow = Image.new("L", scene.size, 0)
        ImageDraw.Draw(shadow).ellipse((left - 10, y1 - 14, left + w + 70, y1 + 22), fill=120)
        dark = Image.new("RGB", scene.size, (70, 48, 24))
        scene.paste(dark, (0, 0), shadow.filter(ImageFilter.GaussianBlur(14)))
    else:
        refl = can.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, w, 50)).filter(ImageFilter.GaussianBlur(2))
        fade = Image.linear_gradient("L").resize((w, 50))
        fade = fade.point(lambda v: int((255 - v) * 0.16))
        alpha = Image.composite(fade, Image.new("L", fade.size, 0), refl.getchannel("A"))
        refl.putalpha(alpha)
        scene.alpha_composite(refl, (left, y1 + 3))

    scene.alpha_composite(can, (left, top))


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    for name, (scene_name, box, surface, cover, depth, light) in SCENES.items():
        scene = Image.open(ASSETS / f"scene-{scene_name}.jpg").convert("RGBA")
        if depth:
            patch_reflection(scene, box, depth)
        place(scene, load_can(src, name), box, surface, cover, light)
        side = scene.width
        cy = (box[1] + box[3]) / 2
        top = max(0, min(scene.height - side, round(cy - side / 2)))
        out = scene.crop((0, top, side, top + side)).resize((OUT, OUT), Image.LANCZOS).convert("RGB")
        path = ASSETS / f"scene-{name}-web.webp"
        out.save(path, "WEBP", quality=84, method=6)
        print(f"{path.name}: {out.size}, {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
