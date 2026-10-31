#!/usr/bin/env python3
"""Generate pixel-art scrapbook UI assets for Leia's Consent.

Drawn at 640x360 logical pixels and saved at 3x nearest-neighbour so a
1920x1080 Ren'Py window shows them 1:1. Game art is not touched.
Palette and geometry follow the approved mockup kit.
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "game" / "gui" / "scrapbook"
FONT_DIR = ROOT / "game" / "fonts"
S = 3
W, H = 640, 360

PAPER = (239, 228, 205, 255)
PSH = (227, 213, 184, 255)
PEDGE = (216, 200, 166, 255)
RULE = (217, 203, 176, 255)
INK = (59, 42, 48, 255)
INK2 = (122, 98, 102, 255)
ACC = (204, 0, 102, 255)
ACC_D = (138, 0, 69, 255)
ACC_L = (236, 92, 156, 255)
ACC_T = (255, 243, 247, 255)
LEATH = (90, 37, 51, 255)
LEATH_H = (116, 50, 74, 255)
LEATH_L = (62, 24, 35, 255)
LEATH_O = (30, 15, 20, 255)
STITCH = (185, 138, 106, 255)
KRAFT = (230, 207, 159, 255)
KRAFT_O = (90, 64, 48, 255)
KRAFT_H = (243, 226, 184, 255)
PINKP = (243, 201, 207, 255)
PINKP_O = (122, 58, 76, 255)
PINKP_H = (251, 225, 228, 255)
PINKP_L = (217, 165, 174, 255)
TAPE = (228, 214, 160, 220)
TAPE_P = (236, 150, 186, 215)
KEY_O = (26, 15, 12, 255)
KEY_F = (58, 42, 36, 255)
KEY_H = (85, 65, 58, 255)
KEY_L = (36, 23, 15, 255)
NIGHT = (43, 34, 54, 255)
NIGHT_HI = (59, 48, 72, 255)
NIGHT_LO = (29, 23, 38, 255)
NIGHT_EDGE = (14, 10, 18, 255)
UP = (95, 138, 50, 255)
DN = (168, 69, 63, 255)
TRACK = (217, 201, 168, 255)
TRACK2 = (203, 185, 148, 255)
PL = [(74, 46, 34, 255), (82, 51, 31, 255), (71, 43, 32, 255), (78, 49, 36, 255)]
TAB_COLS = [
    (233, 196, 106, 255),
    (185, 208, 210, 255),
    (211, 203, 224, 255),
    (241, 183, 198, 255),
    (239, 215, 150, 255),
    (207, 224, 180, 255),
    (230, 207, 159, 255),
    (214, 207, 200, 255),
]
STICKY = (246, 229, 141, 255)
STICKY_HI = (255, 243, 176, 255)
STICKY_EDGE = (201, 176, 74, 255)

HEART = ["..#.#..", "#.#.#.#", "#######", ".#####.", "..###..", "...#...", "......."]
# 7px icons used on badges are the 6-7 row forms from the kit, padded.
HEART7 = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#...", "......."]
SHIELD = ["#######", "#.....#", "#.....#", "#.....#", ".#...#.", "..#.#..", "...#..."]
PLAY = ["#......", "##.....", "###....", "####...", "###....", "##.....", "#......"]
UPA = ["..#..", ".###.", "#####"]
DNA = ["#####", ".###.", "..#.."]
EYE = [".#####.", "#..#..#", "#.###.#", "#..#..#", ".#####.", ".......", "......."]
QI = {
    "back": ["...#...", "..##...", ".######", "#######", ".######", "..##...", "...#..."],
    "log": ["#######", "#.....#", "#.###.#", "#.....#", "#.###.#", "#.....#", "#######"],
    "skip": ["#..#...", "##.##..", "#######", "#######", "##.##..", "#..#...", "......."],
    "auto": ["..###..", ".#...#.", "#..#..#", "#..##.#", "#.....#", ".#...#.", "..###.."],
    "save": ["######.", "#.##.##", "#.##..#", "#.....#", "#.###.#", "#.###.#", "#######"],
    "qsave": [".......", "..#....", ".###...", "#####..", "..#....", "..#.###", "..#.###"],
    "qload": ["..#.###", "..#.###", "..#....", "#####..", ".###...", "..#....", "......."],
    "prefs": ["..#.#..", ".#####.", "##...##", ".#.#.#.", "##...##", ".#####.", "..#.#.."],
    "hide": EYE,
}


def new(w, h, color=(0, 0, 0, 0)):
    return Image.new("RGBA", (w, h), color)


def rect(d, x, y, w, h, color):
    if w <= 0 or h <= 0:
        return
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=color)


def frame9(d, x, y, w, h, outline, fill, hi=None, lo=None):
    if w < 4 or h < 4:
        return
    rect(d, x + 1, y + 1, w - 2, h - 2, fill)
    d.line((x + 1, y, x + w - 2, y), fill=outline)
    d.line((x + 1, y + h - 1, x + w - 2, y + h - 1), fill=outline)
    d.line((x, y + 1, x, y + h - 2), fill=outline)
    d.line((x + w - 1, y + 1, x + w - 1, y + h - 2), fill=outline)
    if hi:
        d.line((x + 1, y + 1, x + w - 2, y + 1), fill=hi)
        d.line((x + 1, y + 2, x + 1, y + h - 2), fill=hi)
    if lo:
        d.line((x + 2, y + h - 2, x + w - 2, y + h - 2), fill=lo)
        d.line((x + w - 2, y + 2, x + w - 2, y + h - 2), fill=lo)


def speckle(im, x0, y0, x1, y1, n, color):
    px = im.load()
    rng = random.Random(n + x0 * 13 + y0)
    for _ in range(max(0, n)):
        x = rng.randrange(x0, max(x0 + 1, x1))
        y = rng.randrange(y0, max(y0 + 1, y1))
        px[x, y] = color


def sprite(d, x, y, rows, color):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "#":
                d.point((x + i, y + j), fill=color)


def upscale(im, factor=S):
    return im.resize((im.width * factor, im.height * factor), Image.NEAREST)


def save(im, name, scale=True):
    OUT.mkdir(parents=True, exist_ok=True)
    out = upscale(im) if scale else im
    path = OUT / name
    out.save(path)
    print("wrote", path.relative_to(ROOT), out.size)


def font(path, size):
    return ImageFont.truetype(str(path), size)


def silkscreen(size=8, bold=False):
    name = "Silkscreen-Bold.ttf" if bold else "Silkscreen-Regular.ttf"
    return font(FONT_DIR / name, size)


def table(im, seed=7):
    d = ImageDraw.Draw(im)
    rng = random.Random(seed)
    for i, y in enumerate(range(0, H, 26)):
        rect(d, 0, y, W, 26, PL[i % 4])
        rect(d, 0, y, W, 1, (42, 25, 19, 255))
        rect(d, 0, y + 1, W, 1, (94, 60, 43, 255))
        for k in range(70):
            gx = rng.randrange(W)
            gy = y + 3 + rng.randrange(21)
            gl = rng.randrange(6, 26)
            rect(d, gx, gy, gl, 1, (61, 37, 27, 255) if k % 3 else (90, 56, 40, 255))
        jx = rng.randrange(40, 600)
        rect(d, jx, y + 1, 1, 25, (42, 25, 19, 255))


def lightmap(im, cx=200, cy=-40, r=720, hi=1.05, lo=0.72):
    arr = np.asarray(im).astype(np.float32)
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    dd = np.hypot(xx - cx, (yy - cy) * 1.25) / r
    f = hi - (hi - lo) * np.minimum(1, dd)
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    b = bayer[yy % 4, xx % 4] / 16.0 - 0.5
    factor = (np.round(f * 10 + b) / 10)[..., None]
    arr[..., :3] = np.minimum(255, arr[..., :3] * factor)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def book_open(im, bx=12, by=10, bw=550, bh=318):
    d = ImageDraw.Draw(im)
    rect(d, bx + 3, by + 5, bw, bh, (10, 5, 5, 150))
    frame9(d, bx, by, bw, bh, LEATH_O, LEATH, LEATH_H, LEATH_L)
    for x in range(bx + 4, bx + bw - 4, 4):
        d.point((x, by + 3), fill=STITCH)
        d.point((x, by + bh - 4), fill=STITCH)
    g = bx + bw // 2
    pages = ((bx + 8, by + 6, g - 2, by + bh - 6), (g + 2, by + 6, bx + bw - 8, by + bh - 6))
    for x0, y0, x1, y1 in pages:
        rect(d, x0, y1, x1 - x0, 2, PEDGE)
        rect(d, x0, y0, x1 - x0, y1 - y0, PAPER)
        speckle(im, x0, y0, x1, y1, 380 * (x1 - x0) * (y1 - y0) // (280 * 306), PSH)
    d = ImageDraw.Draw(im)
    for k, c in enumerate(["#c9b896", "#d6c6a6", "#dfd0b2", "#e7dbc2", "#ebe0c8"]):
        col = tuple(int(c[i : i + 2], 16) for i in (1, 3, 5)) + (255,)
        rect(d, g - 2 - 1 - k, pages[0][1], 1, pages[0][3] - pages[0][1], col)
        rect(d, g + 2 + k, pages[0][1], 1, pages[0][3] - pages[0][1], col)
    rect(d, g - 2, pages[0][1], 4, pages[0][3] - pages[0][1], (179, 159, 125, 255))
    rect(d, g - 1, pages[0][1], 2, pages[0][3] - pages[0][1], (156, 136, 102, 255))


def pixel_photo(w, h, kind="club"):
    paths = {
        "club": ROOT / "game/images/cg/ch01/CH1D1_CG_DinnerArrival_01.webp",
        "pool": ROOT / "game/images/backgrounds/villa/villa_pool_evening.webp",
        "beach": ROOT / "game/images/backgrounds/villa/villa_frontdoor_evening.webp",
    }
    boxes = {
        "club": (520, 80, 1500, 980),
        "pool": (200, 80, 1700, 980),
        "beach": (0, 200, 1920, 1000),
    }
    src = paths.get(kind)
    if src and src.exists():
        im = Image.open(src).convert("RGB")
        if kind in boxes:
            im = im.crop(boxes[kind])
        im = im.resize((w, h), Image.LANCZOS)
        return im.quantize(28, dither=Image.Dither.NONE).convert("RGBA")
    return new(w, h, (42, 34, 48, 255))


def polaroid(im, x, y, w, h, photo, ph=None):
    d = ImageDraw.Draw(im)
    ph = ph or (h - 22)
    rect(d, x + 2, y + 3, w, h, (20, 10, 5, 90))
    frame9(d, x, y, w, h, (107, 90, 72, 255), (251, 246, 234, 255), (255, 255, 255, 255), (221, 211, 192, 255))
    rect(d, x + 4, y + 4, w - 8, ph, (42, 34, 48, 255))
    if photo is not None:
        im.alpha_composite(photo.resize((w - 8, ph), Image.NEAREST), (x + 4, y + 4))


def stamp(im, x, y, w, h, label, seed=1):
    d = ImageDraw.Draw(im)
    d.rectangle((x, y, x + w - 1, y + h - 1), outline=(168, 58, 90, 255))
    d.rectangle((x + 2, y + 2, x + w - 3, y + h - 3), outline=(168, 58, 90, 255))
    f = silkscreen(8, True)
    bb = d.textbbox((0, 0), label, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((x + (w - tw) // 2 - bb[0], y + (h - th) // 2 - bb[1]), label, font=f, fill=(168, 58, 90, 255))
    rng = random.Random(seed)
    px = im.load()
    for _ in range(18):
        px_ = x + rng.randrange(w)
        py_ = rng.choice([y, y + h - 1])
        if px[px_, py_][:3] == (168, 58, 90):
            px[px_, py_] = PAPER


def closed_journal(im):
    d = ImageDraw.Draw(im)
    rng = random.Random(4)
    bx, by, bw, bh = 178, 20, 258, 318
    rect(d, bx + 4, by + 6, bw + 4, bh, (10, 5, 5, 150))
    rect(d, bx + 6, by + 4, bw + 3, bh - 4, (42, 25, 19, 255))
    for k, c in enumerate([(239, 228, 205), (216, 200, 166), (239, 228, 205), (201, 181, 144)]):
        rect(d, bx + bw - 1 + k, by + 6, 1, bh - 8, c + (255,))
    frame9(d, bx, by, bw, bh, LEATH_O, LEATH, LEATH_H, LEATH_L)
    px = im.load()
    for i in range(900):
        x = bx + 3 + rng.randrange(bw - 6)
        y = by + 3 + rng.randrange(bh - 6)
        px[x, y] = (83, 33, 46, 255) if i % 2 else (98, 41, 58, 255)
    d = ImageDraw.Draw(im)
    rect(d, bx + 1, by + 1, 10, bh - 2, (74, 29, 42, 255))
    rect(d, bx + 11, by + 1, 1, bh - 2, LEATH_O)
    rect(d, bx + 12, by + 1, 1, bh - 2, LEATH_H)
    for y in range(by + 20, by + bh - 10, 60):
        rect(d, bx + 2, y, 8, 2, (58, 21, 32, 255))
        rect(d, bx + 2, y + 2, 8, 1, LEATH_H)
    for x in range(bx + 18, bx + bw - 8, 4):
        d.point((x, by + 7), fill=STITCH)
        d.point((x, by + bh - 8), fill=STITCH)
    for y in range(by + 8, by + bh - 8, 4):
        d.point((bx + 17, y), fill=STITCH)
        d.point((bx + bw - 8, y), fill=STITCH)

    def corner(x, y, fx, fy):
        for j in range(9):
            for i in range(9 - j):
                px_ = x + (i if fx > 0 else -i)
                py_ = y + (j if fy > 0 else -j)
                c = (201, 168, 110, 255) if (i + j) < 7 else (138, 106, 58, 255)
                if i == 0 or j == 0:
                    c = (226, 196, 138, 255)
                d.point((px_, py_), fill=c)

    corner(bx + bw - 2, by + 1, -1, 1)
    corner(bx + bw - 2, by + bh - 2, -1, -1)
    corner(bx + 13, by + 1, 1, 1)
    corner(bx + 13, by + bh - 2, 1, -1)

    lx, ly, lw, lh = bx + 20, by + 34, bw - 56, 52
    rect(d, lx + 2, ly + 3, lw, lh, (0, 0, 0, 120))
    frame9(d, lx, ly, lw, lh, (42, 29, 26, 255), (239, 227, 204, 255), (251, 243, 226, 255), (205, 184, 149, 255))
    speckle(im, lx + 3, ly + 3, lx + lw - 3, ly + lh - 3, 90, (226, 211, 182, 255))
    d = ImageDraw.Draw(im)
    sx, sy, sw, sh = lx + 7, ly + 7, lw - 14, lh - 14
    d.rectangle((sx, sy, sx + sw - 1, sy + sh - 1), outline=(168, 58, 90, 255))
    d.rectangle((sx + 2, sy + 2, sx + sw - 3, sy + sh - 3), outline=(168, 58, 90, 255))
    f16 = silkscreen(16, True)
    t1 = "LEIA'S CONSENT"
    bb = d.textbbox((0, 0), t1, font=f16)
    d.text((sx + (sw - (bb[2] - bb[0])) // 2, sy + 4), t1, font=f16, fill=(168, 58, 90, 255))
    f8 = silkscreen(8)
    s8 = "A SUMMER JOURNAL"
    bb = d.textbbox((0, 0), s8, font=f8)
    d.text((sx + (sw - (bb[2] - bb[0])) // 2, sy + sh - 12), s8, font=f8, fill=(138, 74, 92, 255))

    ph = pixel_photo(122, 80, "club")
    px0, py0 = bx + (bw - 130) // 2 + 4, by + 112
    polaroid(im, px0, py0, 130, 104, ph, ph=80)
    tape_corner_at(im, px0 - 8, py0 - 8, False, TAPE)
    tape_corner_at(im, px0 + 130 - 16, py0 - 8, True, TAPE_P)
    stamp(im, bx + 26, by + bh - 44, 46, 22, "18+", seed=5)
    d = ImageDraw.Draw(im)
    d.text((bx + 78, by + bh - 38), "ADULTS", font=f8, fill=(201, 138, 156, 255))
    d.text((bx + 78, by + bh - 28), "ONLY", font=f8, fill=(201, 138, 156, 255))
    ex = bx + bw - 30
    rect(d, ex, by - 2, 7, bh + 4, (26, 10, 16, 255))
    rect(d, ex + 1, by - 2, 5, bh + 4, (58, 22, 38, 255))
    rect(d, ex + 2, by - 2, 1, bh + 4, (90, 42, 64, 255))
    rect(d, bx + 60, by + bh - 2, 5, 16, ACC_D)
    rect(d, bx + 61, by + bh - 2, 3, 16, ACC)
    return px0, py0


def tape_corner_at(im, x, y, flip, col):
    t = new(24, 24)
    td = ImageDraw.Draw(t)
    pts = [(0, 8), (8, 0), (23, 15), (15, 23)] if not flip else [(15, 0), (23, 8), (8, 23), (0, 15)]
    td.polygon(pts, fill=col)
    im.alpha_composite(t, (x, y))


def menu_props(im):
    d = ImageDraw.Draw(im)
    polaroid(im, 22, 196, 88, 74, pixel_photo(80, 52, "pool"), ph=52)
    polaroid(im, 64, 236, 88, 74, pixel_photo(80, 52, "beach"), ph=52)
    tape = new(28, 9, TAPE)
    td = ImageDraw.Draw(tape)
    td.line((1, 1, 26, 1), fill=(255, 250, 225, 120))
    im.alpha_composite(tape, (52, 192))
    tape_corner_at(im, 136, 232, True, TAPE)
    # ticket
    x, y = 34, 84
    rect(d, x + 2, y + 3, 124, 36, (20, 10, 5, 80))
    frame9(d, x, y, 124, 36, PINKP_O, PINKP, PINKP_H, PINKP_L)
    for yy in range(y + 2, y + 35, 3):
        d.point((x + 92, yy), fill=PINKP_O)
    f = silkscreen(8, True)
    d.text((x + 8, y + 4), "VILLA TRIP", font=f, fill=(106, 35, 56, 255))
    d.text((x + 8, y + 18), "DAY ONE", font=silkscreen(8), fill=(138, 74, 92, 255))
    d.text((x + 100, y + 16), "01", font=silkscreen(8), fill=(138, 74, 92, 255))
    tape_corner_at(im, x + 110, y - 8, True, TAPE)


def say_strip(theme="day", cg=False):
    if cg:
        w, h = 560, 36
        rules = [15, 29]
        op = 0.74 if theme == "day" else 0.82
    else:
        w, h = 552, 74
        rules = [24, 39, 54, 69]
        op = 1.0
    im = new(w, h)
    d = ImageDraw.Draw(im)
    if theme == "day":
        fill, edge, hi, lo, spk, rule, marg = PAPER, (42, 29, 26, 255), (251, 243, 226, 255), (205, 184, 149, 255), PSH, RULE, (236, 191, 200, 255)
    else:
        fill, edge = (43, 34, 54, 255), (14, 10, 18, 255)
        hi, lo = (59, 48, 72, 255), (29, 23, 38, 255)
        spk, rule, marg = (37, 29, 47, 255), (58, 48, 70, 255), (90, 42, 68, 255)
    frame9(d, 0, 0, w, h, edge, fill, hi, lo)
    rng = random.Random(11 if not cg else 5)
    px = im.load()
    for x in range(3, w - 3):
        if rng.random() < 0.07:
            px[x, 0] = (0, 0, 0, 0)
            px[x, 1] = edge
    speckle(im, 2, 2, w - 2, h - 2, int(w * h / (220 if cg else 180)), spk)
    d = ImageDraw.Draw(im)
    for y in rules:
        if 0 <= y + 2 < h:
            rect(d, 4, y + 2, w - 8, 1, rule)
    mx = 14 if cg else 16
    rect(d, mx, 3, 1, h - 6, marg)
    rect(d, mx + 2, 3, 1, h - 6, marg)
    if cg and op < 1:
        arr = np.array(im)
        face = np.zeros(arr.shape[:2], bool)
        face[1 : h - 1, 1 : w - 1] = True
        mask = arr[..., 3] > 0
        arr[..., 3] = np.where(face & mask, (arr[..., 3] * op).astype(np.uint8), arr[..., 3])
        im = Image.fromarray(arr, "RGBA")
    return im


def make_frame(w, h, outline, fill, hi, lo, name):
    im = new(w, h)
    frame9(ImageDraw.Draw(im), 0, 0, w, h, outline, fill, hi, lo)
    save(im, name)


def make_tabs():
    for i, col in enumerate(TAB_COLS):
        hi = tuple(min(255, c + 30) for c in col[:3]) + (255,)
        make_frame(28, 20, (59, 42, 48, 255), col, hi, (0, 0, 0, 40), "tab_%d.png" % i)
    make_frame(28, 20, (42, 10, 24, 255), ACC, ACC_L, ACC_D, "tab_pink.png")


def make_icons():
    mapping = {
        "icon_heart.png": (HEART7, ACC),
        "icon_up.png": (["..#..", ".###.", "#####", ".....", ".....", ".....", "....."], UP),
        "icon_down.png": ([".....", ".....", ".....", ".....", "#####", ".###.", "..#.."], DN),
        "icon_play.png": (PLAY, ACC_T),
        "ctc.png": (["#####", ".###.", "..#.."], ACC),
    }
    for name, rows in QI.items():
        mapping["icon_%s.png" % name] = (rows, (205, 185, 168, 255))
    for name, (rows, col) in mapping.items():
        im = new(7, 7)
        sprite(ImageDraw.Draw(im), 0, 0, rows, col)
        save(im, name)


def make_tapes():
    for name, col in (("tape_h.png", TAPE), ("tape_pink_h.png", TAPE_P)):
        im = new(30, 9, col)
        d = ImageDraw.Draw(im)
        px = im.load()
        for j in range(9):
            if j % 2 == 0:
                px[0, j] = (0, 0, 0, 0)
                px[29, j] = (0, 0, 0, 0)
        d.line((1, 1, 28, 1), fill=(255, 250, 225, 140))
        save(im, name)
    for name, flip, col in (
        ("tape_corner.png", False, TAPE),
        ("tape_corner_flip.png", True, TAPE),
        ("tape_corner_pink.png", False, TAPE_P),
        ("tape_corner_pink_flip.png", True, TAPE_P),
    ):
        im = new(24, 24)
        tape_corner_at(im, 0, 0, flip, col)
        save(im, name)
    skip = new(98, 15, (236, 150, 186, 235))
    px = skip.load()
    for j in range(15):
        if j % 2 == 0:
            px[0, j] = (0, 0, 0, 0)
            px[97, j] = (0, 0, 0, 0)
    save(skip, "skip_tape.png")


def make_bits():
    make_frame(24, 24, (42, 29, 26, 255), PAPER, (251, 243, 226, 255), (205, 184, 149, 255), "frame_paper.png")
    make_frame(24, 24, (42, 29, 26, 255), (251, 243, 226, 255), (255, 255, 255, 255), (205, 184, 149, 255), "frame_paper_hi.png")
    make_frame(24, 24, NIGHT_EDGE, NIGHT, NIGHT_HI, NIGHT_LO, "frame_night.png")
    make_frame(24, 24, (107, 90, 72, 255), (244, 234, 214, 255), (251, 246, 234, 255), (221, 211, 192, 255), "frame_card.png")
    make_frame(24, 24, ACC_D, (251, 243, 226, 255), (255, 255, 255, 255), (224, 201, 176, 255), "frame_card_on.png")
    make_frame(24, 24, (42, 10, 24, 255), ACC, ACC_L, ACC_D, "frame_pink.png")
    make_frame(24, 24, (42, 10, 24, 255), (224, 32, 126, 255), (255, 134, 189, 255), ACC_D, "frame_pink_hover.png")
    make_frame(24, 24, (42, 10, 24, 255), ACC_D, (106, 0, 53, 255), (160, 16, 90, 255), "frame_pink_press.png")
    make_frame(24, 24, (42, 29, 34, 255), (110, 90, 98, 255), (134, 114, 122, 255), (85, 68, 75, 255), "frame_pink_off.png")
    make_frame(20, 18, KEY_O, KEY_F, KEY_H, KEY_L, "frame_keycap.png")
    make_frame(20, 18, (42, 10, 24, 255), ACC, ACC_L, ACC_D, "frame_keycap_on.png")
    make_frame(24, 20, KRAFT_O, KRAFT, KRAFT_H, (176, 138, 58, 255), "frame_kraft.png")
    make_frame(24, 24, (42, 29, 26, 255), STICKY, STICKY_HI, STICKY_EDGE, "frame_sticky.png")
    make_frame(24, 24, PINKP_O, PINKP, PINKP_H, PINKP_L, "frame_ticket.png")
    make_frame(20, 16, UP, (247, 239, 220, 255), (255, 255, 255, 255), UP, "chip_up.png")
    make_frame(20, 16, DN, (247, 239, 220, 255), (255, 255, 255, 255), DN, "chip_down.png")
    make_frame(28, 22, (107, 90, 72, 255), (251, 246, 234, 255), (255, 255, 255, 255), (221, 211, 192, 255), "frame_polaroid.png")
    # name tabs
    for name, fill, edge, hi, lo in (
        ("leia", PINKP, PINKP_O, PINKP_H, PINKP_L),
        ("ryan", (201, 221, 224, 255), (47, 74, 82, 255), (226, 238, 240, 255), (159, 188, 194, 255)),
        ("maya", (239, 215, 150, 255), (106, 74, 20, 255), (248, 232, 187, 255), (205, 178, 106, 255)),
        ("julian", (211, 226, 189, 255), (62, 90, 42, 255), (230, 240, 216, 255), (169, 192, 138, 255)),
        ("neutral", PAPER, INK, (251, 243, 226, 255), (205, 184, 149, 255)),
    ):
        make_frame(28, 18, edge, fill, hi, lo, "name_%s.png" % name)

    # choice note, torn left edge in the cap
    for name, fill, hi in (
        ("frame_choice.png", PAPER, (251, 243, 226, 255)),
        ("frame_choice_hi.png", (251, 243, 226, 255), (255, 255, 255, 255)),
    ):
        im = new(40, 28)
        d = ImageDraw.Draw(im)
        frame9(d, 0, 0, 40, 28, (42, 29, 26, 255), fill, hi, (205, 184, 149, 255))
        for yy in range(4, 24, 6):
            rect(d, 0, yy, 3, 3, (0, 0, 0, 0))
            d.point((3, yy), fill=(42, 29, 26, 255))
            d.point((3, yy + 2), fill=(42, 29, 26, 255))
        save(im, name)

    # checkbox
    for name, on in (("check_off.png", False), ("check_on.png", True)):
        im = new(12, 10)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 1, 8, 9), outline=INK)
        if on:
            for a, b in ((2, 5), (3, 6), (4, 7), (5, 6), (6, 5), (7, 4), (8, 3), (9, 2), (10, 1)):
                d.point((a, b), fill=ACC)
                d.point((a, b - 1), fill=ACC)
        save(im, name)

    # ink loop, 9-slice friendly
    im = new(64, 18)
    d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 18, 16), outline=(168, 58, 90, 255))
    d.ellipse((45, 1, 62, 16), outline=(168, 58, 90, 255))
    d.line((10, 1, 53, 1), fill=(168, 58, 90, 255))
    d.line((10, 16, 53, 16), fill=(168, 58, 90, 255))
    # clear the inner caps so the middle stays hollow
    rect(d, 8, 2, 48, 14, (0, 0, 0, 0))
    d.line((8, 1, 55, 1), fill=(168, 58, 90, 255))
    d.line((8, 16, 55, 16), fill=(168, 58, 90, 255))
    save(im, "ink_loop.png")

    # slider pieces
    im = new(16, 8)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 15, 7), fill=INK)
    rect(d, 1, 1, 14, 6, TRACK)
    rect(d, 1, 1, 14, 1, TRACK2)
    save(im, "bar_track.png")
    for name, col, hi in (
        ("bar_pink.png", ACC, ACC_L),
        ("bar_teal.png", (79, 133, 146, 255), (127, 176, 187, 255)),
        ("bar_purple.png", (118, 105, 154, 255), (164, 151, 196, 255)),
        ("bar_gold.png", (192, 142, 44, 255), (227, 185, 85, 255)),
        ("bar_grey.png", (122, 110, 102, 255), (165, 154, 144, 255)),
        ("bar_love.png", (201, 64, 110, 255), (229, 122, 158, 255)),
    ):
        im = new(16, 8)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 15, 7), fill=INK)
        rect(d, 1, 1, 14, 6, col)
        rect(d, 1, 1, 14, 2, hi)
        save(im, name)
    im = new(7, 13)
    d = ImageDraw.Draw(im)
    rect(d, 0, 0, 7, 13, INK)
    rect(d, 1, 1, 5, 11, (251, 246, 234, 255))
    rect(d, 1, 1, 5, 1, (255, 255, 255, 255))
    rect(d, 3, 3, 1, 7, ACC)
    save(im, "slider_thumb.png")

    im = new(8, 40)
    d = ImageDraw.Draw(im)
    rect(d, 2, 0, 3, 40, TRACK2)
    save(im, "vscroll_bar.png")
    im = new(8, 24)
    d = ImageDraw.Draw(im)
    rect(d, 1, 0, 5, 24, ACC)
    rect(d, 2, 0, 1, 24, ACC_L)
    save(im, "vscroll_thumb.png")

    # wax seal
    im = new(32, 32)
    d = ImageDraw.Draw(im)
    cx = cy = 16
    for r, c in ((13, (90, 0, 48, 255)), (12, ACC_D), (10, ACC), (7, (176, 0, 90, 255))):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
    for a in range(0, 360, 40):
        px_ = cx + round(13 * math.cos(math.radians(a)))
        py_ = cy + round(13 * math.sin(math.radians(a)))
        d.ellipse((px_ - 2, py_ - 2, px_ + 2, py_ + 2), fill=ACC_D)
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), outline=ACC_D)
    sprite(d, cx - 3, cy - 3, HEART7, (255, 208, 228, 255))
    save(im, "wax_seal.png")

    # empty slot corners marker
    im = new(28, 20)
    d = ImageDraw.Draw(im)
    ink = INK2
    for i in range(8):
        d.point((i, 0), fill=ink)
        d.point((0, i), fill=ink)
    save(im, "photo_corner.png")

    # noted / notify slips are frames; a small camera-less qsave icon already exists
    save(say_strip("day"), "say_day.png")
    save(say_strip("night"), "say_night.png")
    save(say_strip("day", cg=True), "say_cg_day.png")
    save(say_strip("night", cg=True), "say_cg_night.png")


def make_backgrounds():
    menu = new(W, H)
    table(menu, seed=5)
    menu_props(menu)
    px0, py0 = closed_journal(menu)
    menu = lightmap(menu, cx=300, cy=110, r=430, hi=1.06, lo=0.55)
    big = upscale(menu)
    # handwritten caption at full resolution
    hd = ImageDraw.Draw(big)
    caveat = font(FONT_DIR / "Caveat[wght].ttf", 34)
    hd.text(((px0 + 65) * S, (py0 + 96) * S), "just us.", font=caveat, fill=(70, 52, 96, 255), anchor="ms")
    OUT.mkdir(parents=True, exist_ok=True)
    big.convert("RGB").save(OUT / "bg_main_menu.png")
    print("wrote game/gui/scrapbook/bg_main_menu.png", big.size)

    game = new(W, H)
    table(game, seed=7)
    book_open(game)
    game = lightmap(game, cx=200, cy=-20, r=900, hi=1.04, lo=0.92)
    big = upscale(game)
    big.convert("RGB").save(OUT / "bg_game_menu.png")
    print("wrote game/gui/scrapbook/bg_game_menu.png", big.size)

    wood = new(W, H)
    table(wood, seed=21)
    wood = lightmap(wood, cx=320, cy=150, r=380, hi=1.05, lo=0.45)
    upscale(wood).convert("RGB").save(OUT / "bg_table.png")
    print("wrote game/gui/scrapbook/bg_table.png")

    # phone sticker case, drawn at native pixels (the handset is 690x1070)
    case = new(230, 357)
    d = ImageDraw.Draw(case)
    frame9(d, 0, 0, 230, 357, LEATH_O, LEATH, LEATH_H, LEATH_L)
    # hollow the screen
    rect(d, 14, 18, 202, 322, (0, 0, 0, 0))
    d.rectangle((14, 18, 215, 339), outline=LEATH_O)
    for x in range(8, 222, 4):
        d.point((x, 6), fill=STITCH)
        d.point((x, 350), fill=STITCH)
    tape_corner_at(case, 4, 4, False, TAPE)
    tape_corner_at(case, 202, 4, True, TAPE_P)
    tape_corner_at(case, 18, 300, False, TAPE)
    f = silkscreen(8)
    d.text((150, 8), "LEIA", font=f, fill=PINKP)
    big = upscale(case)
    big.save(OUT / "phone_case.png")
    print("wrote game/gui/scrapbook/phone_case.png", big.size)


def main():
    random.seed(1)
    make_tabs()
    make_icons()
    make_tapes()
    make_bits()
    make_backgrounds()
    print("done")


if __name__ == "__main__":
    sys.exit(main())
