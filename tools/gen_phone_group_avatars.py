"""Build undistorted Trip Group phone portraits from the existing selfies.

The entire 1920x1080 image sits inside a 1920x1920 square, centered vertically:
source rectangle (0, 0, 1920, 1080), canvas placement (0, 420). No crop or stretch.
The same circular alpha and border are applied to both swimsuit variants.
Run: python tools/gen_phone_group_avatars.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

GAME = Path(__file__).resolve().parents[1] / "game"
OUTPUT = GAME / "gui/phone/sprite_match"
SIZE = 128
SCALE = 4


def render_avatar(source):
    original = Image.open(source).convert("RGB")
    # A square canvas holds the entire image at native aspect ratio, even for
    # a future four-person selfie with different source dimensions.
    side = max(original.size)
    top = (side - original.height) // 2
    background = original.resize((side, side), Image.Resampling.LANCZOS).filter(
        ImageFilter.GaussianBlur(round(side * 95 / 1920)))
    canvas = Image.new("RGB", (side, side))
    canvas.paste(background)
    canvas.paste(original, ((side - original.width) // 2, top))
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
