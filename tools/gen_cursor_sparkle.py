"""Sparkle cursor art (darryn 2026-11-08, draft E "Sparkle glint").

Writes game/gui/cursor/:
  sparkle_idle.png   44x44 honey sparkle, warm ink outline, white core (hotspot = centre 22,22)
  sparkle_hover.png  44x44 pink sparkle, berry outline (cross-faded in on hover)
  sparkle_twin.png   20x20 small cream sparkle that orbits the cursor on hover
  sparkle_mote.png   14x14 soft glint left behind when the mouse moves (trail)
Animation (twinkle, pulse, orbit, trail, smooth hover) is done live in
game/systems/lc_cursor.rpy, not baked into frames.

Run: uv run --with pillow python tools/gen_cursor_sparkle.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parents[1] / "game" / "gui" / "cursor"
SS = 8

HONEY = (245, 197, 104)
PINK = (255, 143, 184)
BERRY = (204, 0, 102)
INK = (59, 42, 48)
CREAM = (255, 243, 247)


def sparkle_points(cx, cy, R, fat=4.6, n=360):
    """Concave four-point sparkle (superellipse with exponent > 1)."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        c, s = math.cos(t), math.sin(t)
        x = R * math.copysign(abs(c) ** fat, c)
        y = R * math.copysign(abs(s) ** fat, s)
        pts.append(((cx + x) * SS, (cy + y) * SS))
    return pts


def sparkle(size, R, fill, outline, outline_w=1.6, core=True, shadow=True, glow=None):
    img = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    c = size / 2
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse(((c - R * 0.55) * SS, (c - R * 0.55) * SS, (c + R * 0.55) * SS, (c + R * 0.55) * SS),
                                  fill=glow + (120,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(SS * 3)))
    d = ImageDraw.Draw(img)
    pts = sparkle_points(c, c, R)
    d.polygon(pts, fill=fill + (255,))
    if outline:
        d.line(pts + [pts[0]], fill=outline + (255,), width=int(outline_w * SS), joint="curve")
    # inner highlight: smaller sparkle, lighter
    inner = sparkle_points(c, c, R * 0.5, fat=5.0)
    d.polygon(inner, fill=(255, 255, 255, 150))
    if core:
        r = 1.7
        d.ellipse(((c - r) * SS, (c - r) * SS, (c + r) * SS, (c + r) * SS), fill=(255, 255, 255, 255))
    if shadow:
        a = img.split()[3].filter(ImageFilter.GaussianBlur(SS * 1.4))
        sh = Image.new("RGBA", img.size, (20, 8, 16, 0))
        sh.putalpha(a.point(lambda v: int(v * 0.4)))
        base = Image.new("RGBA", img.size, (0, 0, 0, 0))
        base.alpha_composite(sh, (int(SS * 1.5), int(SS * 2)))
        base.alpha_composite(img)
        img = base
    return img.resize((size, size), Image.Resampling.LANCZOS)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sparkle(44, 14, HONEY, INK, glow=HONEY).save(OUT / "sparkle_idle.png")
    sparkle(44, 15, PINK, BERRY, glow=PINK).save(OUT / "sparkle_hover.png")
    sparkle(20, 6.5, CREAM, BERRY, outline_w=1.3, core=False, shadow=False).save(OUT / "sparkle_twin.png")
    sparkle(14, 5, (255, 236, 190), None, core=True, shadow=False, glow=HONEY).save(OUT / "sparkle_mote.png")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
