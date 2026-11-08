"""Stat icons, line style (darryn 2026-11-09, draft D): thin rounded outline in
each stat's Status colour with a soft tint inside. Symbols: Love heart, Trust
shield + tick, Exhibitionism eye, Temptation flame, Sharing swap arrows.

Writes game/images/ui/scrapbook/icon_<stat>.png (40x40) for the five live stats.
Colours = STAT_BARS in gen_glass_menu_ui.py / LC_STAT_COLOUR in status_display.rpy.
Run: uv run --with pillow python tools/gen_stat_icons.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "game" / "images" / "ui" / "scrapbook"
SS = 8
N = 40
COL = {
    "love": ((255, 170, 205), (232, 98, 152)),
    "trust": ((255, 222, 140), (232, 170, 70)),
    "exhibitionism": ((255, 196, 160), (232, 118, 120)),
    "temptation": ((236, 110, 130), (178, 40, 80)),
    "sharing": ((200, 172, 236), (140, 104, 200)),
}
LINE = 2.6   # stroke width in icon px


def P(pts):
    return [(x * SS, y * SS) for x, y in pts]


def heart(cx, cy, r, n=200):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * r / 16, cy + y * r / 16 + r * 0.12))
    return pts


def flame(cx, base, h, w, n=200):
    """Flame: round belly, tip leaning slightly right."""
    pts = []
    for i in range(n + 1):
        t = i / n                       # 0 -> 1 around the outline
        a = 2 * math.pi * t
        # belly circle for the lower half, tapered to a tip above
        y = base - (h * 0.42) * (1 - math.cos(a)) / 2 * 1.0
        r = w * math.sin(a / 2) ** 1.0
        x = cx + (r if t < 0.5 else -r) * 0
        pts.append((x, y))
    # build explicitly instead: left edge up to tip, right edge down
    left, right = [], []
    for i in range(n + 1):
        k = i / n                       # 0 bottom .. 1 tip
        y = base - h * k
        bulge = math.sin(math.pi * min(1.0, k * 1.25 + 0.15)) * w * (1 - k) ** 0.35
        lean = 3.0 * k ** 2
        left.append((cx - bulge + lean, y))
        right.append((cx + bulge + lean, y))
    bottom = [(cx + w * 0.62 * math.cos(math.pi * j / 20), base - 0.2 + w * 0.35 * math.sin(math.pi * j / 20)) for j in range(21)]
    return right[::-1][:-1] + left + bottom[::-1][:0] or left


def shapes(stat, d, width):
    """Draw outline strokes (and inner fill mask on `fill`)."""
    w = int(width * SS)
    if stat == "love":
        pts = heart(20, 20, 14.5)
        return pts, []
    if stat == "trust":
        pts = [(20, 4), (33, 8.5), (32.4, 21), (20, 36), (7.6, 21), (7, 8.5)]
        return pts, [[(13.5, 20), (18, 24.5), (26.5, 14.5)]]
    if stat == "exhibitionism":
        top = [(4 + 32 * i / 40, 20 - 11 * math.sin(math.pi * i / 40)) for i in range(41)]
        bot = [(36 - 32 * i / 40, 20 + 11 * math.sin(math.pi * i / 40)) for i in range(41)]
        return top + bot, []
    if stat == "temptation":
        return flame_outline(), []
    if stat == "sharing":
        return None, [[(8, 14), (31, 14)], [(25.5, 8.5), (31, 14), (25.5, 19.5)],
                      [(32, 26), (9, 26)], [(14.5, 20.5), (9, 26), (14.5, 31.5)]]


def flame_outline():
    pts = []
    n = 120
    # right side: from bottom centre up to the tip
    for i in range(n + 1):
        k = i / n
        y = 35 - 31 * k
        r = 11.5 * math.sin(math.pi * (0.5 + 0.5 * k)) ** 0.8 if k > 0.0 else 11.5
        r = 11.5 * (1 - k) ** 0.75 * (1 + 0.15 * math.sin(math.pi * k))
        bottom_round = math.sqrt(max(0.0, 1 - ((1 - k * 3.2) if k < 0.3125 else 0) ** 2))
        r *= bottom_round if k < 0.3125 else 1
        lean = 3.2 * k ** 1.8
        pts.append((20 + r + lean, y))
    left = []
    for i in range(n + 1):
        k = 1 - i / n
        y = 35 - 31 * k
        r = 11.5 * (1 - k) ** 0.75 * (1 + 0.15 * math.sin(math.pi * k))
        bottom_round = math.sqrt(max(0.0, 1 - ((1 - k * 3.2) if k < 0.3125 else 0) ** 2))
        r *= bottom_round if k < 0.3125 else 1
        # small notch: left side dips in a little below the tip (flame lick)
        notch = 2.2 * math.exp(-((k - 0.62) / 0.08) ** 2)
        lean = 3.2 * k ** 1.8
        left.append((20 - r + lean + notch, y))
    return pts + left


def grad(top, bot):
    g = Image.new("RGBA", (N * SS, N * SS)); d = ImageDraw.Draw(g)
    for y in range(N * SS):
        k = y / (N * SS - 1)
        d.line((0, y, N * SS, y), fill=tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)) + (255,))
    return g


def icon(stat):
    top, bot = COL[stat]
    outline, strokes = shapes(stat, None, LINE)
    stroke_m = Image.new("L", (N * SS, N * SS)); sd = ImageDraw.Draw(stroke_m)
    fill_m = Image.new("L", (N * SS, N * SS)); fd = ImageDraw.Draw(fill_m)
    w = int(LINE * SS)
    if outline:
        fd.polygon(P(outline), fill=255)
        sd.line(P(outline + outline[:2]), fill=255, width=w, joint="curve")
    for s in strokes:
        sd.line(P(s), fill=255, width=w, joint="curve")
        for x, y in (s[0], s[-1]):
            r = LINE / 2
            sd.ellipse(((x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS), fill=255)
    if stat == "exhibitionism":
        # iris + pupil highlight
        fd.ellipse((14 * SS, 14 * SS, 26 * SS, 26 * SS), fill=255)
        sd.ellipse((15.2 * SS, 15.2 * SS, 24.8 * SS, 24.8 * SS), fill=255)
    if stat == "temptation":
        # inner flame lick
        inner = [(20 + 1.4 + 5.2 * (1 - k) ** 0.8 * math.sin(math.pi * (0.15 + 0.85 * k)) * (1 if s > 0 else -1) + 1.2 * k, 33 - 13 * k)
                 for s in (1, -1) for k in ([i / 30 for i in range(31)] if s > 0 else [1 - i / 30 for i in range(31)])]
        sd.line(P(inner + inner[:1]), fill=255, width=int(LINE * 0.8 * SS), joint="curve")
    out = Image.new("RGBA", (N * SS, N * SS))
    soft = Image.new("RGBA", out.size, top + (255,)); soft.putalpha(fill_m.point(lambda v: 70 if v else 0))
    out.alpha_composite(soft)
    g = grad(top, bot); g.putalpha(stroke_m); out.alpha_composite(g)
    if stat == "exhibitionism":
        hl = Image.new("RGBA", out.size); ImageDraw.Draw(hl).ellipse((21 * SS, 16 * SS, 24 * SS, 19 * SS), fill=(255, 255, 255, 235))
        out.alpha_composite(hl)
    return out.resize((N, N), Image.Resampling.LANCZOS)


def main():
    for stat in COL:
        icon(stat).save(OUT / f"icon_{stat}.png")
    print("wrote", len(COL), "line icons to", OUT)


if __name__ == "__main__":
    main()
