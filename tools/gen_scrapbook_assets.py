#!/usr/bin/env python3
"""Regenerate the pixel-art scrapbook UI.

Draws at the mockup's 640x360 grid (see the reference Pillow scripts) and
nearest-neighbour upscales 3x so Ren'Py can show the PNGs 1:1 on a 1920x1080
screen without filtering. Layout numbers match those scripts; the game
composites photos, handwriting and stat bars on top in Ren'Py.
"""
import os
import random

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "images", "ui", "scrapbook")
NIGHT_PHOTO = os.path.join(ROOT, "game", "images", "backgrounds", "villa", "villa_master_night.webp")
SCALE = 3

INK = (59, 42, 48, 255)
UP = (95, 138, 50, 255)
DN = (168, 69, 63, 255)


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def new(w, h, color=(0, 0, 0, 0)):
    return Image.new("RGBA", (w, h), color)


def rect(d, x, y, w, h, c):
    if w <= 0 or h <= 0:
        return
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=c)


def frame9(d, x, y, w, h, outline, face, hi=None, lo=None):
    rect(d, x + 1, y, w - 2, 1, outline)
    rect(d, x + 1, y + h - 1, w - 2, 1, outline)
    rect(d, x, y + 1, 1, h - 2, outline)
    rect(d, x + w - 1, y + 1, 1, h - 2, outline)
    rect(d, x + 1, y + 1, w - 2, h - 2, face)
    if hi:
        rect(d, x + 1, y + 1, w - 2, 1, hi)
        rect(d, x + 1, y + 1, 1, h - 2, hi)
    if lo:
        rect(d, x + 1, y + h - 2, w - 2, 1, lo)
        rect(d, x + w - 2, y + 1, 1, h - 2, lo)


def up(im, scale=SCALE):
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def save(im, name):
    path = os.path.join(OUT, name)
    im.save(path)
    print(name, im.size)


def pixelize_photo(path, w, h, box=None, colors=48):
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    ratio = max(w / float(im.width), h / float(im.height))
    im = im.resize((max(w, int(round(im.width * ratio))), max(h, int(round(im.height * ratio)))), Image.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    im = im.crop((left, top, left + w, top + h))
    return im.quantize(colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGBA")


def paint_night_sky(w, h):
    im = new(w, h)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / float(h)
        col = (
            int(18 + 20 * (1 - t)),
            int(28 + 30 * (1 - t)),
            int(58 + 28 * (1 - t)),
            255,
        )
        rect(d, 0, y, w, 1, col)
    d.ellipse((w - 78, 18, w - 58, 38), fill=hexc("#f4efe2"))
    for i, c in enumerate(["#1d4e73", "#1a6288", "#2480a4"]):
        rect(d, 0, h // 2 + i * 8, w, 8, hexc(c))
    for x in range(0, w, 7):
        rect(d, x, h // 2 + 10, 3, 1, hexc("#d5f2f8"))
    rect(d, 0, h // 2 + 28, w, h, hexc("#c4a56a"))
    # A couple of palm masses, so the window still reads if the photo is missing.
    for base in (18, 46, 78):
        rect(d, base, h // 2 + 8, 2, 28, hexc("#3a2a18"))
        d.polygon(
            [(base - 10, h // 2 + 16), (base + 1, h // 2 - 2), (base + 12, h // 2 + 16)],
            fill=hexc("#2c4a28"),
        )
    return im


def build_night():
    random.seed(3)
    W, H = 640, 360
    im = new(W, H, hexc("#1d1726"))
    d = ImageDraw.Draw(im)
    px = im.load()
    for x in range(W):
        c = hexc("#1d1726") if (x // 6) % 2 == 0 else hexc("#1a1422")
        rect(d, x, 0, 1, H, c)
    rect(d, 0, 312, W, 48, hexc("#140f1a"))
    rect(d, 0, 312, W, 1, hexc("#2a2233"))

    WX, WY, WW, WH = 120, 34, 400, 214
    try:
        bg = pixelize_photo(NIGHT_PHOTO, WW, WH, box=(705, 262, 1250, 555), colors=48)
    except Exception as exc:
        print("night photo fallback:", exc)
        bg = paint_night_sky(WW, WH)
    im.alpha_composite(bg, (WX, WY))

    px = im.load()
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    for y in range(262, 360):
        for x in range(90, 550):
            t = 1 - (y - 262) / 98.0
            edge = min(x - 90, 550 - x) / 60.0
            a = max(0, min(1, t * min(1, edge))) * 0.35
            if a * 16 > bayer[y % 4][x % 4] + 2:
                r, g, b, _ = px[x, y]
                px[x, y] = (min(255, r + 18), min(255, g + 20), min(255, b + 34), 255)

    d = ImageDraw.Draw(im)
    FO, W1, W2, W3, W0 = hexc("#120c0e"), hexc("#4a3026"), hexc("#6b4634"), hexc("#8a5e44"), hexc("#33201a")

    def wood(x, y, w, h):
        rect(d, x, y, w, h, FO)
        rect(d, x + 1, y + 1, w - 2, h - 2, W1)
        rect(d, x + 1, y + 1, w - 2, 1, W3)
        rect(d, x + 1, y + 1, 1, h - 2, W2)
        rect(d, x + 1, y + h - 2, w - 2, 1, W0)
        rect(d, x + w - 2, y + 1, 1, h - 2, W0)

    wood(WX - 8, WY - 8, WW + 16, 8)
    wood(WX - 8, WY + WH, WW + 16, 8)
    wood(WX - 8, WY - 8, 8, WH + 16)
    wood(WX + WW, WY - 8, 8, WH + 16)
    wood(WX + WW // 2 - 3, WY, 6, WH)
    wood(WX, WY + 86, WW, 5)

    gl = new(W, H)
    gd = ImageDraw.Draw(gl)
    for gx, gy in ((WX + 30, WY + 70), (WX + WW // 2 + 24, WY + 70)):
        for i in range(22):
            gd.point((gx + i, gy - i), fill=(220, 230, 255, 46))
            gd.point((gx + i + 4, gy - i), fill=(220, 230, 255, 26))
    im.alpha_composite(gl)
    d = ImageDraw.Draw(im)

    rect(d, WX - 20, WY + WH + 8, WW + 40, 10, FO)
    rect(d, WX - 19, WY + WH + 9, WW + 38, 8, W2)
    rect(d, WX - 19, WY + WH + 9, WW + 38, 1, W3)
    rect(d, WX - 19, WY + WH + 16, WW + 38, 1, W0)
    rect(d, WX - 14, WY + WH + 18, WW + 28, 3, hexc("#0d090b"))
    rect(d, WX - 52, 16, WW + 104, 4, FO)
    rect(d, WX - 51, 17, WW + 102, 2, hexc("#9a7a52"))
    rect(d, WX - 51, 17, WW + 102, 1, hexc("#c9a86e"))
    for fx in (WX - 58, WX + WW + 50):
        rect(d, fx, 14, 8, 8, FO)
        rect(d, fx + 1, 15, 6, 6, hexc("#b08d5c"))
        d.point((fx + 2, 16), fill=hexc("#e2c48a"))

    folds = [hexc("#3a1e2c"), hexc("#4b2638"), hexc("#5c3045"), hexc("#43233a")]

    def curtain(x0, w, side):
        for y in range(20, 290):
            if y < 200:
                k = max(0, (y - 40) / 160.0)
            else:
                k = max(0, 1 - (y - 200) / 70.0)
            pinch = int(w * 0.42 * (k * k * (3 - 2 * k)))
            span = w - pinch
            for x in range(span):
                xx = x0 + x if side == 0 else x0 + w - 1 - x
                d.point((xx, y), fill=folds[(x // 4) % 4])
            ex = x0 + span - 1 if side == 0 else x0 + pinch
            d.point((ex, y), fill=hexc("#2a1420"))
        for x in range(w):
            d.point((x0 + x, 289), fill=hexc("#2a1420"))

    curtain(WX - 50, 58, 0)
    curtain(WX + WW - 8, 58, 1)
    for tx in (WX - 50, WX + WW + 16):
        rect(d, tx, 197, 34, 5, FO)
        rect(d, tx + 1, 198, 32, 3, hexc("#b08d5c"))
        rect(d, tx + 1, 198, 32, 1, hexc("#d9b77c"))

    # Empty title card. Ren'Py draws the day name into it.
    CW, CH = 280, 52
    cx, cy = (W - CW) // 2, WY + WH + 22
    rect(d, cx + 2, cy + 3, CW, CH, (0, 0, 0, 120))
    frame9(d, cx, cy, CW, CH, hexc("#2a1d1a"), hexc("#efe3cc"), hexc("#fbf3e2"), hexc("#cdb895"))
    for _ in range(110):
        d.point((cx + 3 + random.randrange(CW - 6), cy + 3 + random.randrange(CH - 6)), fill=hexc("#e2d3b6"))
    rect(d, cx + CW // 2 - 2, cy - 3, 5, 5, FO)
    rect(d, cx + CW // 2 - 1, cy - 2, 3, 3, hexc("#cc0066"))
    d.point((cx + CW // 2 - 1, cy - 2), fill=hexc("#ff6fae"))

    arr = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    dd = np.hypot(xx - 320, (yy - 150) * 1.15) / 400.0
    f = 1.0 - (1.0 - 0.62) * np.minimum(1, dd)
    q = np.round(f * 8 + bayer[yy % 4, xx % 4] / 16.0 - 0.5) / 8.0
    arr[..., :3] = np.minimum(255, arr[..., :3] * q[..., None])
    im = Image.fromarray(arr.astype(np.uint8), "RGBA")
    save(up(im), "night.png")


def build_spread():
    random.seed(7)
    W, H = 640, 360
    im = new(W, H, hexc("#4a2e22"))
    d = ImageDraw.Draw(im)
    planks = [hexc("#4a2e22"), hexc("#52331f"), hexc("#472b20"), hexc("#4e3124")]
    for i, y in enumerate(range(0, H, 26)):
        rect(d, 0, y, W, 26, planks[i % 4])
        rect(d, 0, y, W, 1, hexc("#2a1913"))
        rect(d, 0, y + 1, W, 1, hexc("#5e3c2b"))
        for k in range(70):
            gx = random.randrange(W)
            gy = y + 3 + random.randrange(21)
            gl = random.randrange(6, 26)
            rect(d, gx, gy, gl, 1, hexc("#3d251b") if k % 3 else hexc("#5a3828"))
        jx = random.randrange(40, 600)
        rect(d, jx, y + 1, 1, 25, hexc("#2a1913"))

    BX, BY, BW, BH = 30, 8, 580, 318
    rect(d, BX + 3, BY + 5, BW, BH, (10, 5, 5, 150))
    frame9(d, BX, BY, BW, BH, hexc("#1e0f14"), hexc("#5a2533"), hexc("#74324a"), hexc("#3e1823"))
    for x in range(BX + 4, BX + BW - 4, 4):
        d.point((x, BY + 3), fill=hexc("#b98a6a"))
        d.point((x, BY + BH - 4), fill=hexc("#b98a6a"))

    paper = hexc("#efe4cd")
    shade = hexc("#e3d5b8")
    for (x0, y0, x1, y1) in ((38, 14, 318, 320), (322, 14, 602, 320)):
        rect(d, x0, y1, x1 - x0, 2, hexc("#d8c8a6"))
        rect(d, x0, y1 + 2, x1 - x0, 1, hexc("#c9b590"))
        rect(d, x0, y0, x1 - x0, y1 - y0, paper)
        for _ in range(420):
            d.point((random.randrange(x0 + 2, x1 - 2), random.randrange(y0 + 2, y1 - 2)), fill=shade)
    for k, c in enumerate(["#c9b896", "#d6c6a6", "#dfd0b2", "#e7dbc2", "#ebe0c8"]):
        rect(d, 318 - 1 - k, 14, 1, 306, hexc(c))
        rect(d, 322 + k, 14, 1, 306, hexc(c))
    rect(d, 318, 14, 4, 306, hexc("#b39f7d"))
    rect(d, 319, 14, 2, 306, hexc("#9c8866"))
    rect(d, 323, 14, 5, 316, hexc("#8a0045"))
    rect(d, 324, 14, 3, 316, hexc("#cc0066"))
    rect(d, 324, 14, 1, 316, hexc("#e84a94"))
    rect(d, 325, 328, 1, 3, planks[0])
    d.point((324, 330), fill=planks[0])
    d.point((326, 330), fill=planks[0])

    arr = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    dd = np.hypot(xx - 60, (yy + 40) * 1.25) / 720.0
    f = 1.05 - (1.05 - 0.78) * np.minimum(1, dd)
    q = np.round(f * 10 + bayer[yy % 4, xx % 4] / 16.0 - 0.5) / 10.0
    arr[..., :3] = np.minimum(255, arr[..., :3] * q[..., None])
    im = Image.fromarray(arr.astype(np.uint8), "RGBA")
    save(up(im), "spread.png")


def build_polaroid():
    im = new(108, 86)
    d = ImageDraw.Draw(im)
    frame9(d, 0, 0, 108, 86, hexc("#6b5a48"), hexc("#fbf6ea"), hexc("#ffffff"), hexc("#ddd3c0"))
    rect(d, 5, 5, 98, 64, hexc("#2a2230"))
    rect(d, 5, 5, 98, 1, (0, 0, 0, 70))
    save(up(im), "polaroid.png")


def build_tape():
    w, h = 30, 9
    im = new(w, h)
    d = ImageDraw.Draw(im)
    rect(d, 0, 0, w, h, (228, 214, 160, 210))
    d.line((1, 1, w - 2, 1), fill=(255, 250, 225, 150))
    px = im.load()
    for y in range(h):
        if y % 2 == 0:
            px[0, y] = (0, 0, 0, 0)
            px[w - 1, y] = (0, 0, 0, 0)
    save(up(im), "tape_top.png")

    def corner(flip):
        im = new(24, 24)
        d = ImageDraw.Draw(im)
        pts = [(0, 8), (8, 0), (23, 15), (15, 23)] if not flip else [(15, 0), (23, 8), (8, 23), (0, 15)]
        d.polygon(pts, fill=(228, 214, 160, 215))
        return im

    save(up(corner(False)), "tape_corner.png")
    save(up(corner(True)), "tape_corner_flip.png")


def build_ticket():
    im = new(124, 36)
    d = ImageDraw.Draw(im)
    frame9(d, 0, 0, 124, 36, hexc("#7a3a4c"), hexc("#f3c9cf"), hexc("#fbe1e4"), hexc("#d9a5ae"))
    for y in range(2, 34, 3):
        d.point((92, y), fill=hexc("#7a3a4c"))
    save(up(im), "ticket.png")


def build_tag():
    w, h = 124, 40
    im = new(w, h)
    d = ImageDraw.Draw(im)
    poly = [(8, 0), (w - 1, 0), (w - 1, h - 1), (8, h - 1), (0, h - 9), (0, 8)]
    d.polygon(poly, fill=hexc("#e6cf9f"), outline=hexc("#5a4030"))
    d.line((9, 1, w - 2, 1), fill=hexc("#f3e2b8"))
    d.ellipse((4, 14, 11, 21), fill=hexc("#b08a3a"))
    d.ellipse((5, 15, 10, 20), fill=hexc("#d9b25a"))
    d.ellipse((6, 16, 9, 19), fill=hexc("#3a2a20"))
    save(up(im), "tag.png")


def build_diamond():
    im = new(7, 7)
    d = ImageDraw.Draw(im)
    for ox, oy in (
        (0, -2), (-1, -1), (0, -1), (1, -1),
        (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
        (-1, 1), (0, 1), (1, 1), (0, 2),
    ):
        d.point((3 + ox, 3 + oy), fill=hexc("#cc0066"))
    save(up(im), "diamond.png")


def build_bubble():
    rows = ["#######", "#.....#", "#.....#", "#######", ".#.....", "#......"]
    im = new(7, 6)
    d = ImageDraw.Draw(im)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                d.point((x, y), fill=hexc("#7a6266"))
    save(up(im), "bubble.png")


def build_mark():
    rows = ["..#..", ".###.", "#####", ".###.", "..#.."]
    im = new(5, 5)
    d = ImageDraw.Draw(im)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                d.point((x, y), fill=hexc("#7a6266"))
    save(up(im), "mark.png")


def sprite(d, x, y, rows, color):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "#":
                d.point((x + i, y + j), fill=color)


ICONS = {
    "heart": ["..#.#..", ".#####.", "#######", ".#####.", "..###..", "...#..."],
    "shield": [".#####.", "#.....#", "#.....#", ".#...#.", "..#.#..", "...#..."],
    "zzz": ["####...", "...#...", "..#....", ".####..", "....#..", "....###"],
    "face": [".#####.", "#.....#", "#.#.#.#", "#.....#", "#.###.#", ".#####."],
    "lock": ["..###..", ".#...#.", ".#...#.", "#######", "###.#.#", "###.#.#", "#######"],
    "spark": ["...#...", ".#.#.#.", "..###..", "#######", "..###..", ".#.#.#.", "...#..."],
    "eye": [".#####.", "#.....#", "#.#.#.#", "#.....#", ".#####."],
    "flame": ["...#...", "..#.#..", ".#.#.#.", ".#####.", "..###..", "...#..."],
    "chevron": ["#...#..", "##..##.", ".####..", "..##...", "...#..."],
    "drop": ["...#...", "..###..", ".#####.", ".#####.", "..###..", "...#..."],
    "gate": ["#.#.#.#", "#.#.#.#", "#######", "#..#..#", "#..#..#", "#######"],
}


def build_icons():
    plates = {
        "heart": ("#f1b7c6", "#cc0066"),
        "shield": ("#b9d0d2", "#3f6470"),
        "zzz": ("#d3cbe0", "#5a4f72"),
        "face": ("#efd796", "#8a6420"),
        "lock": ("#d6cfc8", "#5a504a"),
        "spark": ("#f3d2b0", "#8a4e28"),
        "eye": ("#f0c4da", "#8a3058"),
        "flame": ("#f0c2b4", "#8a3828"),
        "chevron": ("#c9d6b8", "#3e5a28"),
        "drop": ("#e4c6d4", "#6a3050"),
        "gate": ("#d5d0c4", "#5a5348"),
    }
    for name, rows in ICONS.items():
        plate, ink = plates[name]
        im = new(13, 13)
        d = ImageDraw.Draw(im)
        frame9(d, 0, 0, 13, 13, hexc(ink), hexc(plate))
        iw, ih = len(rows[0]), len(rows)
        sprite(d, 1 + (11 - iw) // 2, 1 + (11 - ih) // 2, rows, hexc(ink))
        save(up(im), "icon_{}.png".format(name))


def build_arrows():
    up_rows = ["...#...", "..###..", ".#####.", "#######"]
    down_rows = up_rows[::-1]
    mid = ["..#..", "...#.", "#####", "...#.", "..#.."]
    small_up = ["..#..", ".###.", "#####"]
    small_down = small_up[::-1]

    def draw(rows, color, name):
        im = new(len(rows[0]), len(rows))
        d = ImageDraw.Draw(im)
        sprite(d, 0, 0, rows, color)
        save(up(im), name)

    draw(up_rows, UP, "arrow_up.png")
    draw(down_rows, DN, "arrow_down.png")
    draw(mid, hexc("#7a6266"), "arrow_mid.png")
    draw(small_up, UP, "tick_up.png")
    draw(small_down, DN, "tick_down.png")


def build_bars():
    fills = {
        "love": ("#c9406e", "#e57a9e"),
        "trust": ("#4f8592", "#7fb0bb"),
        "boredom": ("#76699a", "#a497c4"),
        "curiosity": ("#c46a32", "#e39a62"),
        "exhibitionism": ("#c45284", "#e484ae"),
        "jealousy": ("#c45a42", "#e48a74"),
        "acceptance": ("#c08e2c", "#e3b955"),
        "momentum": ("#6a8a3e", "#9ab86a"),
        "temptation": ("#a85078", "#d484a4"),
        "secrecy": ("#7a6e66", "#a59a90"),
        "boundary_looseness": ("#8a8070", "#b4aa98"),
    }

    def fill_image(body, hi, w=16, h=7):
        im = new(w, h)
        d = ImageDraw.Draw(im)
        rect(d, 0, 0, w, h, hexc(body))
        rect(d, 0, 0, w, 2, hexc(hi))
        return im

    track = new(16, 7)
    td = ImageDraw.Draw(track)
    rect(td, 0, 0, 16, 7, hexc("#d9c9a8"))
    rect(td, 0, 0, 16, 1, hexc("#cbb994"))
    save(up(track), "bar_track.png")
    save(up(fill_image("#8fc04e", "#bfe486")), "bar_gain.png")
    save(up(fill_image("#fff6d8", "#fffdf2")), "bar_flash.png")

    loss = new(200, 7)
    ld = ImageDraw.Draw(loss)
    rect(ld, 0, 0, 200, 7, hexc("#f0d6cc"))
    for x in range(200):
        for y in range(7):
            if (x + y) % 2 == 0:
                ld.point((x, y), fill=DN)
    save(up(loss), "bar_loss.png")

    for stat, (body, hi) in fills.items():
        save(up(fill_image(body, hi)), "bar_fill_{}.png".format(stat))


def build_chips_and_chrome():
    def chip(outline, name):
        im = new(18, 13)
        d = ImageDraw.Draw(im)
        frame9(d, 0, 0, 18, 13, outline, hexc("#f7efdc"))
        save(up(im), name)

    chip(UP, "chip_up.png")
    chip(DN, "chip_down.png")

    def button(face, hi, lo, name):
        im = new(104, 22)
        d = ImageDraw.Draw(im)
        frame9(d, 0, 0, 104, 22, hexc("#2a0a18"), face, hi, lo)
        save(up(im), name)

    button(hexc("#cc0066"), hexc("#ec5c9c"), hexc("#8a0045"), "continue.png")
    button(hexc("#e24b8c"), hexc("#ffd0e4"), hexc("#a01458"), "continue_hover.png")

    key = new(48, 16)
    d = ImageDraw.Draw(key)
    frame9(d, 0, 0, 48, 16, hexc("#1a0f0c"), hexc("#3a2a24"), hexc("#55413a"), hexc("#24170f"))
    save(up(key), "keycap.png")

    # Double-line stamp frame, 9-slice. Center is paper so text sits in it.
    stamp = new(28, 22)
    d = ImageDraw.Draw(stamp)
    rect(d, 0, 0, 28, 22, hexc("#efe4cd"))
    d.rectangle((0, 0, 27, 21), outline=hexc("#a83a5a"))
    d.rectangle((2, 2, 25, 19), outline=hexc("#a83a5a"))
    # A few broken-ink gaps so the border feels stamped, not ruled.
    for x, y in ((4, 0), (18, 0), (9, 21), (22, 2), (0, 8), (27, 14)):
        d.point((x, y), fill=hexc("#efe4cd"))
    save(up(stamp), "stamp.png")

    dots = new(240, 1)
    dd = ImageDraw.Draw(dots)
    for x in range(0, 240, 3):
        dd.point((x, 0), fill=hexc("#7a6266"))
    save(up(dots), "rule_dots.png")

    rule = new(8, 1, hexc("#d9cbb0"))
    save(up(rule), "rule.png")

    # Arrow used inside the continue button.
    rows = ["#...", "##..", "###.", "####", "###.", "##..", "#..."]
    im = new(4, 7)
    d = ImageDraw.Draw(im)
    sprite(d, 0, 0, rows, hexc("#fff3f7"))
    save(up(im), "continue_arrow.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    build_night()
    build_spread()
    build_polaroid()
    build_tape()
    build_ticket()
    build_tag()
    build_diamond()
    build_bubble()
    build_mark()
    build_icons()
    build_arrows()
    build_bars()
    build_chips_and_chrome()


if __name__ == "__main__":
    main()
