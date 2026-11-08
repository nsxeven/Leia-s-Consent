"""Build undistorted Trip Group phone portraits from the existing selfies.

darryn 2026-11-08: zoom in on the three faces, no blurred fill. Each selfie uses a
square crop (uniform scale, no stretch) chosen so all faces sit inside the circle:
trio selfies (shifted toward Julian, darryn): faces span x 400-1260, y 0-630 of 1920x1080, so the square is
(430, 0, 1470, 1040). A selfie without an entry falls back to a centred
full-height square.
Run: python tools/gen_phone_group_avatars.py
"""
from pathlib import Path
from PIL import Image, ImageDraw

GAME = Path(__file__).resolve().parents[1] / "game"
OUTPUT = GAME / "gui/phone/sprite_match"
SIZE = 128
SCALE = 4


# Square crop boxes (left, top, right, bottom) per source file name.
CROPS = {
    "CH1D1_CG_PoolSelfie_Trio_White.webp": (430, 0, 1470, 1040),
    "CH1D1_CG_PoolSelfie_Trio_Blue.webp": (430, 0, 1470, 1040),
}


def render_avatar(source):
    original = Image.open(source).convert("RGB")
    box = CROPS.get(Path(source).name)
    if box is None:
        side = min(original.size)
        left = (original.width - side) // 2
        box = (left, 0, left + side, side)
    assert box[2] - box[0] == box[3] - box[1], box
    canvas = original.crop(box)
    scaled = canvas.resize((SIZE * SCALE, SIZE * SCALE), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", scaled.size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((3 * SCALE, 3 * SCALE, (SIZE - 3) * SCALE - 1,
                  (SIZE - 3) * SCALE - 1), fill=255)
    scaled.putalpha(mask)
    outline = ImageDraw.Draw(scaled)
    outline.ellipse((2 * SCALE, 2 * SCALE, (SIZE - 2) * SCALE - 1,
                     (SIZE - 2) * SCALE - 1), outline="#6b8298", width=2 * SCALE)
    return scaled.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def main():
    for color in ("White", "Blue"):
        source = GAME / f"images/cg/ch01/CH1D1_CG_PoolSelfie_Trio_{color}.webp"
        target = OUTPUT / f"avatar_group_trio_{color.lower()}.png"
        render_avatar(source).save(target)
        print(target)
    four = GAME / "images/cg/ch01/CH1D2_CG_GroupSelfie_Four.webp"
    if four.exists():
        target = OUTPUT / "avatar_group_four.png"
        render_avatar(four).save(target)
        print(target)


if __name__ == "__main__":
    main()
