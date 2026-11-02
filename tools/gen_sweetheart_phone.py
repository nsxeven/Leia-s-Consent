#!/usr/bin/env python3
"""Sweetheart phone pixel assets.

Drawn at the mockup's 1x logical grid (the 640x360 phone language) and saved at
3x nearest-neighbour so Ren'Py can display them 1:1 at 1920x1080 without
resampling. Button PNGs from the approved set are copied unchanged.
"""

from __future__ import annotations

import math
import random
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "game" / "gui" / "phone" / "sweetheart"
ICONS = ROOT / "game" / "gui" / "phone" / "icons"
BUTTON_SRC = Path("/tmp/sweetheart_assets/phone_concepts_v2/sweetheart/button/assets")
S = 3  # logical pixel -> screen pixel


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def blank(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    return im, d


def scale(im):
    return im.resize((im.width * S, im.height * S), Image.NEAREST)


def save(im, name, logical=True):
    OUT.mkdir(parents=True, exist_ok=True)
    final = scale(im) if logical else im
    path = OUT / name
    final.save(path)
    return path


def rect(d, x, y, w, h, fill):
    if w <= 0 or h <= 0:
        return
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=fill)


def rr(d, x, y, w, h, r, fill=None, outline=None):
    d.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=r, fill=fill, outline=outline)


def ell(d, x, y, w, h, fill=None, outline=None):
    d.ellipse((x, y, x + w - 1, y + h - 1), fill=fill, outline=outline)


def sprite(d, x, y, rows, cmap):
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row):
            if ch in cmap:
                d.point((x + xx, y + yy), fill=cmap[ch])


BAYER = [
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
]

# Day bezel colours sampled from the approved phone_btn_day_idle.png
# (same PINKP family the mockup bezel uses). Night values are the sweetheart script.
BZ = {
    "day": dict(
        f=hexc("#f3c9cf"),
        o=hexc("#7a3a4c"),
        h=hexc("#fbe1e4"),
        l=hexc("#d9a5ae"),
        glass=hexc("#5a2a3c"),
        btn=hexc("#7a3a4c"),
    ),
    "night": dict(
        f=hexc("#8a4a62"),
        o=hexc("#2a1020"),
        h=hexc("#b26e86"),
        l=hexc("#6a3448"),
        glass=hexc("#1a0c16"),
        btn=hexc("#2a1020"),
    ),
}


ICOL = {
    "MESSAGES": ("#3f7f9a", "#6aa6bd", "#1f3e4c"),
    "PHOTOS": ("#fbf6ea", "#ffffff", "#9b8a7a"),
    "SHOP": ("#cc0066", "#ec5c9c", "#6a0035"),
    "WALLET": ("#5f8a32", "#8fc04e", "#2f4a1a"),
    "DELIVERY": ("#e9a83b", "#f6cf6a", "#7a4a14"),
    "STATUS": ("#6a4f8a", "#9a7fba", "#2b2236"),
    "SETTINGS": ("#8a7f86", "#b5a5ab", "#3e353a"),
}
ACC = hexc("#cc0066")
CREAM = hexc("#fbf6ea")
INKX = hexc("#3b2a30")


def app_icon(k):
    im, d = blank(24, 24)
    base, hi, ol = [hexc(c) for c in ICOL[k]]
    rr(d, 1, 2, 24, 24, 6, fill=(0, 0, 0, 90))
    rr(d, 0, 0, 24, 24, 6, fill=base, outline=ol)
    rect(d, 5, 1, 14, 1, hi)
    rect(d, 2, 3, 1, 9, hi)
    rect(d, 5, 22, 14, 1, (0, 0, 0, 50))
    if k == "MESSAGES":
        rr(d, 4, 5, 16, 12, 5, fill=CREAM)
        d.polygon([(6, 14), (5, 20), (11, 16)], fill=CREAM)
        rect(d, 6, 16, 12, 1, hexc("#cfe0e6"))
        for i in range(3):
            rect(d, 7 + i * 4, 10, 2, 2, base)
    elif k == "PHOTOS":
        rr(d, 4, 5, 16, 14, 2, fill=hexc("#b9d0d2"), outline=hexc("#7a6266"))
        ell(d, 13, 7, 5, 5, fill=hexc("#e9c46a"))
        d.polygon([(5, 17), (9, 11), (12, 15), (14, 13), (18, 17)], fill=hexc("#5f8a32"))
        rect(d, 5, 17, 14, 1, hexc("#3e5a2a"))
        rect(d, 6, 20, 12, 1, hexc("#d6c6a6"))
    elif k == "SHOP":
        d.arc((8, 3, 15, 12), 180, 360, fill=CREAM, width=2)
        rr(d, 5, 8, 14, 12, 2, fill=CREAM)
        rect(d, 6, 18, 12, 1, hexc("#e3c7cf"))
        sprite(d, 9, 11, [" ## ## ", "#######", " ##### ", "  ###  ", "   #   "], {"#": ACC})
    elif k == "WALLET":
        rect(d, 7, 4, 11, 7, hexc("#e9c46a"))
        rect(d, 7, 6, 11, 1, hexc("#b38a2a"))
        rr(d, 4, 9, 16, 11, 2, fill=hexc("#7a4a2e"), outline=hexc("#3a2016"))
        rect(d, 12, 12, 8, 5, hexc("#5a331f"))
        rect(d, 15, 14, 2, 2, hexc("#e9c46a"))
    elif k == "DELIVERY":
        rect(d, 3, 7, 11, 9, CREAM)
        rect(d, 3, 15, 11, 1, hexc("#d6c6a6"))
        rect(d, 7, 7, 2, 9, hexc("#e6cf9f"))
        d.polygon([(14, 10), (18, 10), (21, 13), (21, 16), (14, 16)], fill=hexc("#a83a5a"))
        rect(d, 16, 11, 2, 2, hexc("#c9dde0"))
        for wx in (5, 15):
            ell(d, wx, 15, 5, 5, fill=INKX)
            d.point((wx + 2, 17), fill=hexc("#b5a5ab"))
    elif k == "STATUS":
        for i, hh in enumerate((5, 9, 13)):
            rect(d, 11 + i * 3, 19 - hh, 2, hh, CREAM)
        sprite(
            d,
            3,
            6,
            [" ## ## ", "#######", "#######", " ##### ", "  ###  ", "   #   "],
            {"#": hexc("#ec5c9c")},
        )
        rect(d, 3, 19, 18, 1, hexc("#d3cbe0"))
    elif k == "SETTINGS":
        cx, cy = 12, 12
        for dx, dy in ((0, -8), (0, 7), (-8, 0), (7, 0), (-6, -6), (5, -6), (-6, 5), (5, 5)):
            rect(d, cx + (dx - 1 if dx == 0 else dx), cy + (dy if dy else -1), 2, 2, hexc("#3e353a"))
        ell(d, cx - 7, cy - 7, 15, 15, fill=hexc("#4e4448"))
        ell(d, cx - 6, cy - 6, 13, 13, fill=hexc("#d6cfc8"))
        ell(d, cx - 3, cy - 3, 7, 7, fill=base)
        ell(d, cx - 2, cy - 2, 5, 5, fill=hexc("#4e4448"))
    return im


def sunset(w=214, h=340):
    im, d = blank(w, h)
    sky = [hexc(c) for c in ("#f8e6da", "#f2d0cf", "#e2aab6", "#c87c96", "#9a4d6c", "#6c2c48")]
    hz = int(h * 0.62)
    for yy in range(hz):
        f = yy / hz * (len(sky) - 1)
        i = int(f)
        fr = f - i
        for xx in range(w):
            c = sky[min(i + 1, len(sky) - 1)] if BAYER[yy % 4][xx % 4] / 16 < fr else sky[i]
            d.point((xx, yy), fill=c)
    cx, cy, r = w // 2 + 30, hz - 14, 26
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=hexc("#fbe7b0"))
    for k, yy in enumerate(range(cy - 6, cy + r, 5)):
        rect(d, cx - r, yy, 2 * r + 1, 1 + k // 2, sky[4])
    sea = [hexc(c) for c in ("#5a2533", "#4a1e2c", "#3b2a30", "#2a1d26")]
    for yy in range(hz, h):
        f = (yy - hz) / max(1, (h - hz)) * (len(sea) - 1)
        i = int(f)
        fr = f - i
        for xx in range(w):
            c = sea[min(i + 1, 3)] if BAYER[yy % 4][xx % 4] / 16 < fr else sea[i]
            d.point((xx, yy), fill=c)
    rnd = random.Random(9)
    for _ in range(40):
        yy = hz + rnd.randrange(2, 60)
        xx = cx + rnd.randrange(-30, 30) - yy // 3
        rect(d, xx, yy, rnd.randrange(3, 9), 1, hexc("#f39ab8"))
    palm = hexc("#1a0f0c")
    bx, by = 38, h
    for t in range(0, 150):
        xx = bx + int(10 * math.sin(t / 60))
        rect(d, xx, by - t, 5 if t < 90 else 4, 1, palm)
    tx = bx + int(10 * math.sin(150 / 60)) + 2
    ty = by - 150
    for ang, ln in ((-160, 46), (-130, 40), (-100, 30), (-60, 36), (-25, 44), (10, 40), (170, 34)):
        a = math.radians(ang)
        for s in range(ln):
            xx = tx + int(s * math.cos(a))
            yy = ty + int(s * math.sin(a)) + int((s / ln) ** 2 * 14)
            th = max(1, 3 - s * 3 // ln)
            rect(d, xx, yy, 2, th, palm)
            if s % 4 == 0 and s > 6:
                rect(d, xx, yy + th, 1, 3, palm)
    return im


def hearts(color, w=214, h=340):
    im, d = blank(w, h)
    rnd = random.Random(4)
    col = hexc(color)
    for _ in range(14):
        hx = rnd.choice([rnd.randrange(3, 14), rnd.randrange(w - 16, w - 8)])
        hy = rnd.randrange(60, h - 46)
        sprite(d, hx, hy, [".#.#.", "#####", ".###.", "..#.."], {"#": col})
    return im


def bezel(mode):
    # 2px logical side-button padding. Body is 230x356, the current handset.
    w, h = 234, 356
    im, d = blank(w, h)
    b = BZ[mode]
    x, y, bw, bh = 2, 0, 230, 356
    rr(d, x + 3, y + 4, bw, bh, 21, fill=(0, 0, 0, 120))
    rect(d, x - 2, y + 70, 2, 22, b["btn"])
    rect(d, x - 2, y + 96, 2, 14, b["btn"])
    rect(d, x + bw, y + 86, 2, 34, b["btn"])
    rr(d, x, y, bw, bh, 21, fill=b["f"], outline=b["o"])
    rr(d, x + 1, y + 1, bw - 2, bh - 2, 20, outline=b["h"])
    d.line((x + bw - 2, y + 20, x + bw - 2, y + bh - 20), fill=b["l"])
    d.line((x + 20, y + bh - 2, x + bw - 20, y + bh - 2), fill=b["l"])
    sx, sy, sw, sh, rad = x + 8, y + 8, bw - 16, bh - 16, 14
    mask = Image.new("L", im.size, 255)
    ImageDraw.Draw(mask).rounded_rectangle((sx, sy, sx + sw - 1, sy + sh - 1), radius=rad, fill=0)
    r, g, bch, a = im.split()
    a = ImageChops.multiply(a, mask)
    im = Image.merge("RGBA", (r, g, bch, a))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((sx - 1, sy - 1, sx + sw, sy + sh), radius=rad + 1, outline=b["glass"])
    return im


def round_patch(w, h, rad, fill, outline=None, lip=None):
    im, d = blank(w, h)
    if lip:
        rr(d, 0, 1, w, h - 1, rad, fill=lip)
        rr(d, 0, 0, w, h - 1, rad, fill=fill)
    else:
        rr(d, 0, 0, w, h, rad, fill=fill, outline=outline)
    return im


def tail(outgoing, face, edge):
    im, d = blank(8, 8)
    if outgoing:
        rect(d, 0, 2, 6, 5, face)
        for px, py in ((6, 4), (6, 5), (7, 5), (6, 6), (7, 6)):
            d.point((px, py), fill=face)
        rect(d, 0, 7, 6, 1, edge)
        rect(d, 6, 7, 2, 1, edge)
    else:
        rect(d, 2, 2, 6, 5, face)
        for px, py in ((1, 4), (1, 5), (0, 5), (1, 6), (0, 6)):
            d.point((px, py), fill=face)
        rect(d, 2, 7, 6, 1, edge)
        rect(d, 0, 7, 2, 1, edge)
    return im


CHEV = ["...#", "..##", ".##.", "##..", ".##.", "..##", "...#"]
WIFI = [".#####.", "#.....#", "..###..", ".#...#.", "...#..."]
SEND = ["...#...", "..###..", ".#####.", "...#...", "...#...", "...#...", "...#..."]
PEOPLE = [
    "..##....##..",
    ".####..####.",
    ".####..####.",
    "..##....##..",
    "............",
    ".####..####.",
    "######.#####",
    "######.#####",
]


def chevron(color):
    im, d = blank(7, 7)
    sprite(d, 0, 0, CHEV, {"#": hexc(color)})
    return im


def glyphs(color):
    """Signal + wifi + battery, one strip. Transparent background."""
    im, d = blank(40, 14)
    c = hexc(color)
    for i in range(4):
        rect(d, i * 2, 12 - (i + 1) * 2, 1, (i + 1) * 2, c)
    sprite(d, 12, 4, WIFI, {"#": c})
    rect(d, 24, 3, 12, 7, c)
    rect(d, 25, 4, 10, 5, (0, 0, 0, 0))
    rect(d, 26, 5, 7, 3, c)
    rect(d, 36, 5, 1, 3, c)
    return im


def island():
    im, d = blank(44, 10)
    rr(d, 0, 0, 44, 10, 5, fill=hexc("#120a0e"))
    ell(d, 34, 2, 6, 6, fill=hexc("#2a2a3a"))
    d.point((36, 4), fill=hexc("#6a7a9a"))
    return im


def avatar_disc(fill, outline):
    im, d = blank(12, 12)
    ell(d, 0, 0, 12, 12, fill=hexc(fill), outline=hexc(outline))
    return im


def group_disc():
    im, d = blank(18, 18)
    ell(d, 0, 0, 18, 18, fill=hexc("#e6cf9f"), outline=hexc("#5a4030"))
    sprite(d, 3, 5, PEOPLE, {"#": hexc("#5a4030")})
    return im


def badge(fill, outline, size=13):
    im, d = blank(size, size)
    ell(d, 0, 0, size, size, fill=hexc(fill), outline=hexc(outline))
    return im


def dock():
    im, d = blank(200, 34)
    rr(d, 0, 0, 200, 34, 11, fill=(250, 244, 232, 150), outline=(250, 244, 232, 190))
    return im


def banner(mode):
    b = BZ[mode]
    # Day banner uses the blush header inside the pink rim. Night uses the plum header.
    inner = hexc("#fdf3ef") if mode == "day" else hexc("#301e2c")
    line = hexc("#e9c6c8") if mode == "day" else hexc("#4a2c40")
    im, d = blank(232, 48)
    rr(d, 2, 3, 232, 48, 12, fill=(0, 0, 0, 120))
    rr(d, 0, 0, 232, 48, 12, fill=b["f"], outline=b["o"])
    rr(d, 1, 1, 230, 46, 11, outline=b["h"])
    rr(d, 4, 4, 224, 40, 9, fill=inner, outline=line)
    rect(d, 106, 40, 20, 2, line)
    return im


def search_field(mode):
    if mode == "day":
        fill, edge, mut = hexc("#f4dedd"), hexc("#e9c6c8"), hexc("#8a5f69")
    else:
        fill, edge, mut = hexc("#301e2c"), hexc("#4a2c40"), hexc("#b58a9e")
    im, d = blank(196, 15)
    rr(d, 0, 0, 196, 15, 7, fill=fill)
    ell(d, 6, 3, 7, 7, outline=mut)
    d.line((12, 9, 14, 11), fill=mut)
    return im


def input_field(mode):
    if mode == "day":
        return round_patch(40, 17, 8, hexc("#fffbf5"), hexc("#d7aab1"))
    return round_patch(40, 17, 8, hexc("#301e2c"), hexc("#5c3852"))


def plus_btn(mode):
    mut = hexc("#8a5f69") if mode == "day" else hexc("#b58a9e")
    line = hexc("#e9c6c8") if mode == "day" else hexc("#4a2c40")
    im, d = blank(15, 15)
    ell(d, 0, 0, 15, 15, fill=line)
    rect(d, 7, 3, 1, 9, mut)
    rect(d, 3, 7, 9, 1, mut)
    return im


def send_btn(mode):
    acc = hexc("#a8305e") if mode == "day" else hexc("#f08ab0")
    im, d = blank(15, 15)
    ell(d, 0, 0, 15, 15, fill=acc)
    sprite(d, 4, 3, SEND, {"#": hexc("#faf4e8")})
    return im


def compose_icon(color):
    im, d = blank(12, 12)
    c = hexc(color)
    d.rectangle((1, 1, 9, 9), outline=c)
    d.line((6, 6, 11, 1), fill=c, width=2)
    return im


def card(mode):
    if mode == "day":
        return round_patch(24, 24, 6, hexc("#fffbf5"), hexc("#e9c6c8"))
    return round_patch(24, 24, 6, hexc("#301e2c"), hexc("#4a2c40"))


def berry_key():
    return round_patch(24, 16, 6, hexc("#a8305e"), hexc("#5e1634"))


def photo_mask():
    """Square mask; Ren'Py scales it with nearest off because photos are smooth.
    Generated large so cover-fit photos keep soft corners."""
    im, d = blank(320, 180)
    d.rounded_rectangle((0, 0, 319, 179), radius=18, fill=(255, 255, 255, 255))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    save(bezel("day"), "bezel_day.png")
    save(bezel("night"), "bezel_night.png")
    save(sunset(), "wallpaper.png")
    save(hearts("#f3dcdc"), "hearts_day.png")
    save(hearts("#3a2436"), "hearts_night.png")
    save(island(), "island.png")
    save(dock(), "dock.png")
    save(group_disc(), "avatar_group.png")
    for who, fill, outline in (
        ("leia", "#f3c9cf", "#7a3a4c"),
        ("julian", "#d3e2bd", "#3e5a2a"),
        ("maya", "#efd796", "#6a4a14"),
        ("ryan", "#c9dde0", "#2f4a52"),
        ("system", "#e7d5da", "#8a5f69"),
    ):
        save(avatar_disc(fill, outline), "avatar_%s.png" % who)
    save(badge("#a8305e", "#5e1634", 13), "badge_day.png")
    save(badge("#a8305e", "#f8c9da", 13), "badge_night.png")
    save(badge("#a8305e", "#6a0035", 11), "badge_small.png")
    for mode, acc, txt in (
        ("day", "#a8305e", "#4a2633"),
        ("night", "#f08ab0", "#f3e2ea"),
    ):
        save(chevron(acc), "chevron_%s.png" % mode)
        save(glyphs(txt), "glyphs_%s.png" % mode)
        save(glyphs("#5a2533"), "glyphs_wallpaper.png")
        save(banner(mode), "banner_%s.png" % mode)
        save(search_field(mode), "search_%s.png" % mode)
        save(input_field(mode), "field_%s.png" % mode)
        save(plus_btn(mode), "plus_%s.png" % mode)
        save(send_btn(mode), "send_%s.png" % mode)
        save(compose_icon(acc), "compose_%s.png" % mode)
        save(card(mode), "card_%s.png" % mode)
    save(glyphs("#5a2533"), "glyphs_wallpaper.png")
    # Bubbles: day and night incoming differ. Outgoing berry is shared, but the
    # night edge is a touch deeper so each theme gets its own patch.
    bubbles = {
        "in_day": ("#fffbf5", "#d7aab1"),
        "out_day": ("#a8305e", "#5e1634"),
        "in_night": ("#40293a", "#120a10"),
        "out_night": ("#a8305e", "#4a1028"),
    }
    for name, (face, edge) in bubbles.items():
        save(round_patch(20, 16, 5, hexc(face), lip=hexc(edge)), "bubble_%s.png" % name)
        save(tail(name.startswith("out"), hexc(face), hexc(edge)), "tail_%s.png" % name)
    save(berry_key(), "key_berry.png")
    # Photo mask stays 1x-large; not a pixel asset.
    photo_mask().save(OUT / "photo_mask.png")

    icon_files = {
        "MESSAGES": "messages.png",
        "PHOTOS": "photos.png",
        "SHOP": "shop.png",
        "WALLET": "wallet.png",
        "DELIVERY": "delivery.png",
        "STATUS": "status.png",
        "SETTINGS": "settings.png",
    }
    for key, filename in icon_files.items():
        icon = app_icon(key)
        save(icon, "icon_%s.png" % key.lower())
        scale(icon).save(ICONS / filename)
    # Square fallback so nothing still points at the glossy 256px phone.
    phone = app_icon("MESSAGES")
    scale(phone).save(ICONS / "phone.png")

    for name in (
        "phone_btn_day_idle.png",
        "phone_btn_day_hover.png",
        "phone_btn_night_idle.png",
        "phone_btn_night_hover.png",
    ):
        shutil.copyfile(BUTTON_SRC / name, OUT / name)

    # Contact sheet for a quick visual check.
    sheet = Image.new("RGBA", (900, 420), hexc("#2a1a24"))
    x = 16
    for key in icon_files:
        im = scale(app_icon(key))
        sheet.alpha_composite(im, (x, 16))
        x += 90
    sheet.alpha_composite(scale(bezel("day")).resize((234, 356), Image.NEAREST), (16, 110))
    sheet.alpha_composite(scale(sunset()).resize((140, 220), Image.NEAREST), (280, 140))
    sheet.alpha_composite(scale(banner("day")), (440, 150))
    sheet.alpha_composite(scale(banner("night")), (440, 220))
    sheet.save("/tmp/sw_preview.png")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
