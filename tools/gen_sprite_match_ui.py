#!/usr/bin/env python3
"""Rebuild the sprite-matched phone chrome and the scrapbook material pass.

Idempotent: phone art, preference controls, stat emblems and the book
backgrounds are drawn from this file. Paper frames, tabs, nameplates,
polaroids, the ticket and the less common stat emblems are refined from
the pristine copies in tools/sprite_match/pristine (the pre-pass art from
main). Running this script again overwrites the same outputs and does not
restack the grain.

Native day-review fills (game/images/ui/scrapbook/bar_fill_*.png) are never
opened for writing. Love stays pink, Trust teal, Boredom lavender,
Acceptance gold, Secrecy gray, and the other stat fills stay byte-identical.

Decorative phone glyphs with no screen (camera, notes, maps, music,
browser, calendar, a calls app) are not generated.

Usage:
    python3 tools/gen_sprite_match_ui.py
"""

from __future__ import annotations

import hashlib
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
PRISTINE = ROOT / "tools" / "sprite_match" / "pristine"
PHONE = GAME / "gui" / "phone" / "sprite_match"
GUI = GAME / "gui" / "scrapbook"
SCRAP = GAME / "images" / "ui" / "scrapbook"
WALLPAPER = GAME / "images" / "backgrounds" / "villa" / "villa_pool_day.webp"
FONT_HAND = GAME / "fonts" / "PatrickHand-Regular.ttf"

# Preference rails. Sampled from the pre-pass art so a second run does not
# drift the way a "read the file we just wrote" gradient would.
SLIDER_BARS = {
    "bar_pink.png": (204, 0, 102),
    "bar_teal.png": (79, 133, 146),
    "bar_purple.png": (118, 105, 154),
    "bar_gold.png": (192, 142, 44),
    "bar_grey.png": (122, 110, 102),
    "bar_love.png": (201, 64, 110),
    "bar_track.png": (217, 201, 168),
}

# Clothed sprites only. Boxes are head-and-shoulders, not full bodies.
AVATAR_SOURCES = {
    "leia": (GAME / "images/sprites/leia/PRO/Base_Casual.png", (230, 20, 680, 470)),
    "ryan": (GAME / "images/sprites/ryan/Base_Casual.png", (300, 15, 680, 395)),
    "julian": (GAME / "images/sprites/julian/BASE_BlackTeeGreyShorts.png", (220, 0, 740, 520)),
}


def rgb(value):
    value = value.strip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(round(x * (1 - t) + y * t) for x, y in zip(a, b))


def grad(w, h, top, bot):
    image = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(image)
    a = rgb(top)
    b = rgb(bot)
    for y in range(h):
        t = round(y / max(1, h - 1) * 47) / 47
        draw.line((0, y, w, y), fill=mix(a, b, t) + (255,))
    return image


def stat_fill_hashes():
    hashes = {}
    for path in sorted(SCRAP.glob("bar_fill_*.png")):
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not hashes:
        raise SystemExit("no bar_fill_*.png found; refusing to run")
    return hashes


def material(src: Path, dest: Path):
    """One gentle grain pass from a pristine source. Never reads dest."""
    old = Image.open(src).convert("RGBA")
    size = old.size
    image = old.resize(((size[0] + 1) // 2, (size[1] + 1) // 2), Image.Resampling.NEAREST)
    pixels = image.load()
    rng = random.Random(41)
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if not a:
                continue
            noise = rng.choice((-1, 0, 0, 0, 1))
            vary = round(2 * math.sin(x / max(1, image.width) * math.pi) - 3 * y / max(1, image.height)) + noise
            pixels[x, y] = (
                max(0, min(255, r + vary)),
                max(0, min(255, g + vary)),
                max(0, min(255, b + vary)),
                a,
            )
    image.resize(size, Image.Resampling.NEAREST).save(dest)


def book(dest: Path, bounds, size):
    """Physical notebook page. `bounds` is (x, y, w, h) in full-resolution pixels."""
    width, height = size
    image = grad((width + 1) // 2, (height + 1) // 2, "#51444D", "#302D3B")
    draw = ImageDraw.Draw(image)
    w, h = image.size
    rng = random.Random(22)
    for _ in range(90):
        y = rng.randrange(h)
        x = rng.randrange(w)
        draw.line((x, y, min(w, x + rng.randrange(20, 140)), y), fill=(85, 65, 71, 255))
    x, y, bw, bh = [q // 2 for q in bounds]
    mid = x + bw // 2
    for k in range(7, 0, -1):
        draw.rounded_rectangle((x + k, y + k, x + bw + k, y + bh + k), 3, fill=mix(rgb("#292432"), rgb("#352C36"), k / 8))
    draw.rounded_rectangle((x, y, x + bw, y + bh), 4, fill="#65505D", outline="#2B2732", width=1)
    draw.line((x + 4, y + 2, x + bw - 4, y + 2), fill="#AD8595")
    draw.line((x + 2, y + 5, x + 2, y + bh - 5), fill="#917081")
    for xx in range(x + 7, x + bw - 5, 8):
        draw.line((xx, y + 4, xx + 3, y + 4), fill="#C6A795")
        draw.line((xx, y + bh - 3, xx + 3, y + bh - 3), fill="#9B7D76")
    for off, color in ((6, "#9B897D"), (5, "#E2D0BA"), (3, "#BAAA97")):
        draw.rectangle((x + 7, y + 7 + off, x + bw - 7, y + bh - 6 + off), fill=color)
    for x0, x1 in ((x + 7, mid - 1), (mid + 1, x + bw - 7)):
        paper = grad(x1 - x0, y + bh - 7 - (y + 6), "#FFF6E6", "#EEDFC9")
        pp = paper.load()
        for yy in range(paper.height):
            for xx in range(paper.width):
                r, g, b, a = pp[xx, yy]
                edge = min(xx, paper.width - 1 - xx)
                shade = round(11 * math.exp(-edge / 6))
                vary = rng.choice((-1, 0, 0, 0, 1)) - shade
                pp[xx, yy] = (r + vary, g + vary, b + vary, a)
        image.alpha_composite(paper, (x0, y + 6))
    draw = ImageDraw.Draw(image)
    for dx in range(-9, 10):
        shade = int(95 * math.exp(-abs(dx) / 3))
        draw.line((mid + dx, y + 7, mid + dx, y + bh - 8), fill=(235 - shade, 220 - shade, 201 - shade, 255))
    draw.polygon(
        [(mid + 9, y + 5), (mid + 14, y + 5), (mid + 14, y + bh + 4), (mid + 11, y + bh + 1), (mid + 9, y + bh + 4)],
        fill="#B66783",
    )
    draw.line((mid + 10, y + 7, mid + 10, y + bh), fill="#DF9FB1")
    draw.line((mid + 14, y + 7, mid + 14, y + bh), fill="#7D4B65")
    image.resize((width, height), Image.Resampling.NEAREST).save(dest)


def refine_scrapbook():
    if not PRISTINE.is_dir():
        raise SystemExit("missing tools/sprite_match/pristine; the material pass needs those sources")
    book(GUI / "bg_game_menu.png", (36, 30, 1650, 954), (1920, 1080))
    book(SCRAP / "spread.png", (90, 24, 1740, 954), (1920, 1080))

    gui_src = PRISTINE / "gui" / "scrapbook"
    for pattern in ("frame_*.png", "tab_*.png", "name_*.png"):
        for src in sorted(gui_src.glob(pattern)):
            material(src, GUI / src.name)
    for path in sorted(GUI.glob("tab_*.png")):
        image = Image.open(path).convert("RGBA")
        draw = ImageDraw.Draw(image)
        w, h = image.size
        draw.line((7, h - 4, w - 5, h - 4), fill="#997A86", width=2)
        draw.line((w - 5, 8, w - 5, h - 6), fill="#A28D93", width=2)
        image.save(path)

    scrap_src = PRISTINE / "images" / "ui" / "scrapbook"
    for name in ("polaroid.png", "tag.png", "ticket.png", "continue.png", "continue_hover.png"):
        src = scrap_src / name
        if src.is_file():
            material(src, SCRAP / name)
    for name in ("icon_spark.png", "icon_eye.png", "icon_flame.png", "icon_chevron.png", "icon_drop.png", "icon_gate.png"):
        src = scrap_src / name
        if src.is_file():
            material(src, SCRAP / name)

    ticket = Image.open(SCRAP / "ticket.png").convert("RGBA")
    draw = ImageDraw.Draw(ticket)
    w, h = ticket.size
    for y in range(10, h - 6, 10):
        draw.line((w - 54, y, w - 54, y + 4), fill="#A7858A", width=2)
    for y in range(12, h - 8, 16):
        draw.rectangle((0, y, 3, y + 4), fill="#DBC0B5")
        draw.rectangle((w - 4, y, w - 1, y + 4), fill="#DBC0B5")
    draw.line((8, 5, w - 8, 5), fill="#FAE5DD", width=2)
    ticket.save(SCRAP / "ticket.png")

    redraw_checks()
    redraw_sliders()
    redraw_stat_icons()


def redraw_checks():
    for on in (False, True):
        dest = GUI / ("check_on.png" if on else "check_off.png")
        width, height = 36, 30
        image = Image.new("RGBA", ((width + 1) // 2, (height + 1) // 2))
        draw = ImageDraw.Draw(image)
        w, h = image.size
        draw.rounded_rectangle((0, 3, w - 1, h - 3), radius=6, fill="#B96C8C" if on else "#B5AAAB", outline="#7D6A77")
        draw.line((5, 4, w - 6, 4), fill="#E8ADBF" if on else "#D6CBC9")
        cx = w - 7 if on else 6
        draw.ellipse((cx - 4, 4, cx + 4, h - 5), fill="#FFF8EA", outline="#E4D9CD")
        image.resize((width, height), Image.Resampling.NEAREST).save(dest)


def redraw_sliders():
    for name, base in SLIDER_BARS.items():
        width, height = 48, 24
        image = Image.new("RGBA", ((width + 1) // 2, (height + 1) // 2))
        draw = ImageDraw.Draw(image)
        w, h = image.size
        for y in range(h):
            t = y / (h - 1)
            vary = round(22 * (1 - t) - 17 * t)
            color = tuple(max(0, min(255, channel + vary)) for channel in base)
            draw.line((0, y, w, y), fill=color + (255,))
        draw.line((0, 0, w - 1, 0), fill=tuple(min(255, channel + 45) for channel in base))
        draw.line((0, h - 1, w - 1, h - 1), fill=tuple(max(0, channel - 38) for channel in base))
        image.resize((width, height), Image.Resampling.NEAREST).save(GUI / name)

    width, height = 21, 39
    image = Image.new("RGBA", ((width + 1) // 2, (height + 1) // 2))
    draw = ImageDraw.Draw(image)
    w, h = image.size
    for y in range(1, h - 1):
        vary = round(22 - 38 * y / h)
        draw.line((1, y, w - 2, y), fill=tuple(max(0, min(255, channel + vary)) for channel in (211, 184, 198)))
    draw.rounded_rectangle((0, 0, w - 1, h - 1), 1, outline="#705B6F")
    draw.line((2, 1, w - 3, 1), fill="#FFF2E5")
    draw.line((1, 2, 1, h - 3), fill="#EAD3D4")
    for y in (h // 2 - 2, h // 2, h // 2 + 2):
        draw.line((3, y, w - 4, y), fill="#977C92")
        draw.point((3, y - 1), fill="#F3DBDF")
    image.resize((width, height), Image.Resampling.NEAREST).save(GUI / "slider_thumb.png")


# Cohesive 20-pixel silhouettes, 2x nearest-scaled; one dark outline.
STAT_PALETTE = {
    "love": ("#F4B6CD", "#C85B82"), "trust": ("#B2DDD9", "#5B9C9F"),
    "boredom": ("#D2C5E3", "#9182AD"), "momentum": ("#B9D89A", "#71944F"),
    "curiosity": ("#F7DCA8", "#BD9063"), "temptation": ("#EEB5C6", "#A65D87"),
    "exhibitionism": ("#E7A9C5", "#AA5D88"),
    "boundary_looseness": ("#D7CBB8", "#948572"),
    "secrecy": ("#D8D2D0", "#90868B"), "jealousy": ("#F3B6A0", "#BD6A62"),
    "acceptance": ("#F8DEAB", "#C4A160"), "sharing": ("#E2BCD3", "#AA7798"),
    "distance": ("#C1D2DE", "#7992AC"),
}

def redraw_stat_icons():
    for name, (top, bot) in STAT_PALETTE.items():
        mask = Image.new("L", (20, 20))
        d = ImageDraw.Draw(mask)
        if name == "love":
            d.ellipse((3, 4, 10, 11), fill=255); d.ellipse((9, 4, 16, 11), fill=255)
            d.polygon([(3, 9), (16, 9), (15, 13), (10, 18), (4, 13)], fill=255)
        elif name == "trust":
            d.polygon([(10, 2), (17, 5), (16, 13), (10, 18), (4, 13), (3, 5)], fill=255)
        elif name == "boredom":
            d.line((4, 5, 15, 5, 4, 15, 15, 15), fill=255, width=3)
        elif name == "momentum":
            d.polygon([(3, 10), (10, 3), (17, 10), (13, 10), (13, 17), (7, 17), (7, 10)], fill=255)
        elif name == "curiosity":
            d.ellipse((5, 2, 14, 11), fill=255); d.rectangle((8, 11, 11, 14), fill=255)
            d.rectangle((7, 15, 12, 16), fill=255)
        elif name == "temptation":
            d.polygon([(10, 2), (16, 11), (15, 15), (12, 18), (7, 18), (4, 14), (5, 10)], fill=255)
        elif name == "exhibitionism":
            d.polygon([(2, 10), (6, 5), (10, 3), (14, 5), (18, 10), (14, 15), (10, 17), (6, 15)], fill=255)
        elif name == "boundary_looseness":
            d.rectangle((3, 4, 5, 17), fill=255); d.rectangle((14, 4, 16, 17), fill=255)
            d.rectangle((4, 4, 15, 6), fill=255); d.line((7, 8, 11, 13), fill=255, width=2)
        elif name == "secrecy":
            d.arc((5, 2, 14, 13), 180, 360, fill=255, width=3)
            d.rounded_rectangle((4, 9, 16, 17), 1, fill=255)
        elif name == "jealousy":
            d.polygon([(10, 2), (13, 7), (16, 5), (17, 12), (14, 17), (6, 17), (3, 12), (6, 7), (7, 11)], fill=255)
        elif name == "acceptance":
            d.ellipse((3, 3, 17, 17), fill=255)
        elif name == "sharing":
            d.ellipse((2, 5, 11, 15), fill=255); d.ellipse((9, 5, 18, 15), fill=255)
        elif name == "distance":
            d.ellipse((2, 5, 8, 11), fill=255); d.ellipse((12, 9, 18, 15), fill=255)
            d.rectangle((3, 12, 8, 17), fill=255); d.rectangle((12, 3, 17, 8), fill=255)
        outer = mask.filter(ImageFilter.MaxFilter(3))
        image = Image.new("RGBA", (20, 20))
        ink = Image.new("RGBA", (20, 20), "#3B2A30")
        ink.putalpha(outer); image.alpha_composite(ink)
        fill = grad(20, 20, top, bot)
        fill.putalpha(mask); image.alpha_composite(fill)
        d = ImageDraw.Draw(image)
        if name == "trust":
            d.line((7, 10, 9, 12, 13, 7), fill="#FFF8E9", width=2)
        elif name == "curiosity":
            d.line((8, 17, 11, 17), fill="#3B2A30")
        elif name == "exhibitionism":
            d.ellipse((7, 7, 12, 12), fill="#3B2A30")
            d.rectangle((9, 8, 10, 9), fill="#FFF8E9")
        elif name == "secrecy":
            d.rectangle((9, 12, 10, 15), fill="#3B2A30")
        elif name == "acceptance":
            d.point((7, 8), fill="#3B2A30"); d.point((13, 8), fill="#3B2A30")
            d.arc((6, 7, 14, 14), 15, 165, fill="#3B2A30", width=1)
        image.resize((40, 40), Image.Resampling.NEAREST).save(SCRAP / f"icon_{name}.png")

def build_camera_icon():
    """Pixel camera for the Full Transparency CG stamp on choice cards."""
    image = Image.new("RGBA", (14, 11), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    d.rectangle((4, 0, 8, 2), fill="#3B2A30")
    d.rectangle((0, 2, 13, 10), fill="#3B2A30")
    d.rectangle((1, 3, 12, 9), fill="#FFF8E9")
    d.ellipse((4, 4, 9, 9), fill="#3B2A30")
    d.rectangle((6, 6, 7, 7), fill="#FFF8E9")
    d.point((11, 4), fill="#CC0066")
    image.resize((28, 22), Image.Resampling.NEAREST).save(SCRAP / "icon_camera.png")


def draw_app_icon(name, top, bot):
    image = grad(48, 48, top, bot)
    mask = Image.new("L", (48, 48))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 47, 47), 11, fill=255)
    image.putalpha(mask)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, 46, 46), 10, outline=rgb(bot) + (255,), width=1)
    draw.line((11, 2, 36, 2), fill=(255, 255, 255, 130))
    white = "#FFFDF4"
    if name == "messages":
        draw.rounded_rectangle((8, 9, 40, 32), 8, fill="#13865C")
        draw.rounded_rectangle((7, 8, 39, 31), 8, fill=white)
        draw.polygon([(12, 28), (10, 37), (22, 29)], fill=white)
        for x in (17, 24, 31):
            draw.ellipse((x - 1, 18, x + 1, 20), fill="#43BA76")
    elif name == "photos":
        draw.polygon([(9, 12), (29, 8), (34, 31), (13, 35)], fill="#DF99AE", outline="#FAF8EE")
        draw.rectangle((17, 15, 39, 37), fill=white, outline="#BCC2CE")
        draw.rectangle((19, 17, 37, 33), fill="#74C4DA")
        draw.ellipse((29, 19, 33, 23), fill="#FFE8A2")
        draw.polygon([(19, 32), (24, 23), (30, 29), (33, 25), (37, 32)], fill="#6DAD87")
    elif name == "settings":
        points = []
        for k in range(48):
            angle = k * math.pi / 24
            radius = 18 if k % 4 in (0, 1) else 14
            points.append((24 + int(math.cos(angle) * radius), 24 + int(math.sin(angle) * radius)))
        draw.polygon(points, fill="#5D6C85", outline="#DCE4EE")
        draw.ellipse((14, 14, 34, 34), fill="#D3DCE7", outline="#F4F7F7")
        draw.ellipse((18, 18, 30, 30), fill="#62718B")
        draw.arc((19, 19, 29, 29), 180, 300, fill="#32455F", width=2)
    elif name == "status":
        for x, bar_h in ((11, 10), (20, 18), (29, 27)):
            draw.rounded_rectangle((x, 38 - bar_h, x + 6, 38), 1, fill=white)
    elif name == "delivery":
        draw.rectangle((7, 17, 29, 32), fill=white)
        draw.polygon([(29, 22), (36, 22), (41, 29), (41, 34), (29, 34)], fill="#D7E3E8")
        draw.rectangle((32, 24, 36, 28), fill="#698DAA")
        draw.ellipse((11, 29, 19, 37), fill="#3E526E")
        draw.ellipse((31, 29, 39, 37), fill="#3E526E")
        draw.ellipse((13, 31, 17, 35), fill="#B9CCD8")
        draw.ellipse((33, 31, 37, 35), fill="#B9CCD8")
    elif name == "shop":
        draw.rounded_rectangle((12, 18, 36, 38), 3, fill=white)
        draw.arc((16, 10, 32, 24), 200, 340, fill=white, width=3)
        draw.rectangle((22, 22, 26, 26), fill="#C45B3E")
    elif name == "wallet":
        draw.rounded_rectangle((8, 14, 40, 36), 4, fill=white)
        draw.rectangle((8, 14, 40, 22), fill="#F4E2B0")
        draw.rounded_rectangle((24, 24, 40, 34), 2, fill="#3E526E")
        draw.ellipse((32, 26, 36, 30), fill="#F6D56A")
    else:
        raise SystemExit("no glyph for %s" % name)
    return image.resize((96, 96), Image.Resampling.NEAREST).resize((80, 80), Image.Resampling.NEAREST)


def wallpaper():
    if not WALLPAPER.is_file():
        raise SystemExit("missing villa wallpaper %s" % WALLPAPER)
    image = Image.open(WALLPAPER).convert("RGB")
    image = ImageOps.fit(image, (305, 510), centering=(0.66, 0.5)).filter(ImageFilter.GaussianBlur(0.5))
    image = image.convert("RGBA")
    shade = Image.new("RGBA", image.size)
    shade_draw = ImageDraw.Draw(shade)
    for y in range(510):
        shade_draw.line((0, y, 305, y), fill=(15, 25, 48, round(130 - 60 * math.sin(y / 510 * math.pi))))
    return Image.alpha_composite(image, shade)


def status_glyphs(draw, ink):
    for k in range(4):
        draw.rectangle((243 + k * 3, 23 - k * 2, 244 + k * 3, 26), fill=ink)
    draw.arc((258, 17, 270, 27), 200, 340, fill=ink, width=1)
    draw.arc((260, 20, 268, 27), 200, 340, fill=ink, width=1)
    draw.point((264, 25), fill=ink)
    draw.rounded_rectangle((276, 18, 291, 26), 2, outline=ink)
    draw.rectangle((278, 20, 287, 24), fill=ink)
    draw.rectangle((292, 21, 293, 23), fill=ink)


def build_handset(kind, wall):
    """325x520 handset, nearest-scaled to the 540x1040 screen used by phone_screen."""
    image = Image.new("RGBA", (325, 520))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((2, 67, 5, 90), 1, fill="#8C8E9D")
    draw.rounded_rectangle((2, 101, 5, 128), 1, fill="#6C7184")
    draw.rounded_rectangle((320, 95, 323, 139), 1, fill="#A5A5B2")
    draw.rounded_rectangle((4, 0, 320, 519), 29, fill="#1F2330", outline="#7D7B89")
    draw.rounded_rectangle((5, 1, 319, 518), 28, outline="#C3BCC4")
    draw.rounded_rectangle((7, 2, 317, 517), 27, outline="#424856")
    draw.rounded_rectangle((8, 3, 316, 516), 26, fill="#0E1420")
    screen = wall.copy() if kind == "home" else Image.new("RGBA", (305, 510), "#F3F5F8")
    mask = Image.new("L", screen.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 304, 509), 22, fill=255)
    screen.putalpha(mask)
    image.alpha_composite(screen, (10, 5))
    draw = ImageDraw.Draw(image)
    if kind == "home":
        draw.rounded_rectangle((24, 445, 300, 497), 16, fill="#C3D0DC", outline="#D7E3E8")
        draw.line((40, 446, 284, 446), fill="#EAF0EE")
    draw.rounded_rectangle((137, 13, 187, 25), 6, fill="#080E19")
    draw.ellipse((178, 16, 184, 22), fill="#1E2D46")
    draw.ellipse((180, 17, 182, 19), fill="#42566F")
    ink = "#F4F8FD" if kind == "home" else "#303B51"
    status_glyphs(draw, ink)
    draw.rounded_rectangle((121, 504, 204, 506), 1, fill="#EEF2F6" if kind == "home" else "#202F46")
    final = image.resize((650, 1040), Image.Resampling.NEAREST).resize((540, 1040), Image.Resampling.NEAREST)
    if kind == "thread":
        draw = ImageDraw.Draw(final)
        draw.rectangle((18, 72, 522, 186), fill="#FCFDFE")
        draw.line((18, 186, 522, 186), fill="#D5DCE7")
        draw.rounded_rectangle((24, 908, 516, 968), 28, fill="#FFFFFF", outline="#CFD8E4")
        draw.ellipse((460, 916, 504, 960), fill="#428FD0")
        draw.polygon([(468, 940), (492, 930), (484, 950), (480, 940)], fill="#FFFFFF")
    return final


def circle_crop(image, box, size=128):
    crop = image.crop(box).convert("RGBA")
    fitted = ImageOps.fit(crop, (size, size), centering=(0.5, 0.42))
    mask = Image.new("L", (size, size))
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    fitted.putalpha(mask)
    return fitted


def draw_disc(fill, glyph, glyph_fill="#3B2A30"):
    image = Image.new("RGBA", (128, 128))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 127, 127), fill=fill)
    font = ImageFont.truetype(str(FONT_HAND), 72)
    draw.text((64, 58), glyph, font=font, fill=glyph_fill, anchor="mm")
    return image


def build_avatars():
    faces = {}
    for name, (path, box) in AVATAR_SOURCES.items():
        if not path.is_file():
            raise SystemExit("missing sprite %s" % path)
        face = circle_crop(Image.open(path), box)
        face.save(PHONE / f"avatar_{name}.png")
        faces[name] = face
    draw_disc("#E7C4A8", "M", "#6A3A28").save(PHONE / "avatar_maya.png")
    draw_disc("#D5DDE6", "•", "#5C6B7A").save(PHONE / "avatar_system.png")

    group = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Ryan is drawn last so the glasses stay visible over the other two.
    spots = (("julian", (0, 32)), ("leia", (56, 44)), ("ryan", (30, 2)))
    for name, (x, y) in spots:
        small = faces[name].resize((72, 72), Image.Resampling.LANCZOS)
        group.alpha_composite(small, (x, y))
    mask = Image.new("L", (128, 128))
    ImageDraw.Draw(mask).ellipse((0, 0, 127, 127), fill=255)
    group.putalpha(mask)
    group.save(PHONE / "avatar_group.png")


def build_hud():
    def phone(fill_screen):
        image = Image.new("RGBA", (114, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((16, 8, 98, 140), 16, fill="#1C2230", outline="#C9CED8")
        draw.rounded_rectangle((22, 16, 92, 132), 12, fill=fill_screen)
        draw.rounded_rectangle((48, 20, 66, 26), 3, fill="#0C121C")
        draw.rounded_rectangle((40, 124, 74, 128), 2, fill="#D7DEE8")
        draw.rounded_rectangle((30, 48, 84, 78), 8, fill="#FFFFFF")
        draw.polygon([(36, 70), (34, 84), (52, 72)], fill="#FFFFFF")
        draw.ellipse((44, 58, 48, 62), fill="#43BA76")
        draw.ellipse((54, 58, 58, 62), fill="#43BA76")
        draw.ellipse((64, 58, 68, 62), fill="#43BA76")
        return image

    phone("#E7F6EE").save(PHONE / "hud_idle.png")
    hover = phone("#F4FFFB")
    ImageDraw.Draw(hover).rounded_rectangle((14, 6, 100, 142), 18, outline="#FFFFFF")
    hover.save(PHONE / "hud_hover.png")


def build_chrome():
    PHONE.mkdir(parents=True, exist_ok=True)
    colors = {
        "messages": ("#5ED87E", "#139D61"),
        "photos": ("#F8ECD8", "#C6D9E8"),
        "settings": ("#B6C0D1", "#74859F"),
        "status": ("#E3A4C3", "#AB5D8C"),
        "delivery": ("#87C4D7", "#4A819F"),
        "shop": ("#F4B183", "#D4784A"),
        "wallet": ("#8E9AAF", "#2C3E50"),
    }
    for name, (top, bot) in colors.items():
        draw_app_icon(name, top, bot).save(PHONE / f"{name}.png")

    wall = wallpaper()
    for kind in ("home", "thread", "app"):
        build_handset(kind, wall).save(PHONE / f"phone_{kind}.png")

    incoming = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    draw = ImageDraw.Draw(incoming)
    draw.rounded_rectangle((2, 4, 69, 69), 16, fill="#E4E9EF")
    draw.rounded_rectangle((2, 2, 69, 66), 16, fill="#FFFFFF")
    draw.line((16, 6, 54, 6), fill="#F7F9FC")
    incoming.save(PHONE / "bubble_in.png")

    outgoing = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    draw = ImageDraw.Draw(outgoing)
    draw.rounded_rectangle((2, 4, 69, 69), 16, fill="#C5E6D4")
    draw.rounded_rectangle((2, 2, 69, 66), 16, fill="#DDF6E8")
    draw.line((16, 6, 54, 6), fill="#F4FFF8")
    outgoing.save(PHONE / "bubble_out.png")

    card = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((2, 2, 69, 69), 16, fill="#FFFFFF", outline="#D5DCE7")
    card.save(PHONE / "card.png")

    # Soft pixel-edged row focus, using the same rounded 9-slice shape as cards.
    row_hover = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    row_draw = ImageDraw.Draw(row_hover)
    row_draw.rounded_rectangle((2, 2, 69, 69), 16, fill="#E7F2FA", outline="#A5C7DD", width=2)
    row_draw.line((16, 6, 54, 6), fill="#FFFFFF")
    row_hover.save(PHONE / "row_hover.png")

    key = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    draw = ImageDraw.Draw(key)
    draw.rounded_rectangle((2, 4, 69, 69), 16, fill="#2E74B0")
    draw.rounded_rectangle((2, 2, 69, 66), 16, fill="#3D8FD4")
    draw.line((16, 6, 54, 6), fill="#8EBEF0")
    key.save(PHONE / "key.png")

    # White rounded pill for the selected setting's "On" badge (9-slice).
    pill = Image.new("RGBA", (48, 32), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, 47, 31), 15, fill="#FFFFFF")
    pill.save(PHONE / "pill_white.png")

    badge = Image.new("RGBA", (36, 28), (0, 0, 0, 0))
    ImageDraw.Draw(badge).rounded_rectangle((0, 0, 35, 27), 12, fill="#E4466A")
    badge.save(PHONE / "badge.png")

    chevron = Image.new("RGBA", (36, 36), (0, 0, 0, 0))
    draw = ImageDraw.Draw(chevron)
    draw.line((22, 8, 12, 18, 22, 28), fill="#4287C2", width=3)
    chevron.save(PHONE / "chevron.png")

    dot = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    ImageDraw.Draw(dot).ellipse((2, 2, 13, 13), fill="#3D8FD4")
    dot.save(PHONE / "dot.png")

    build_avatars()
    build_hud()
    build_camera_icon()


def main():
    before = stat_fill_hashes()
    refine_scrapbook()
    build_chrome()
    after = stat_fill_hashes()
    if before != after:
        changed = [name for name in before if before[name] != after.get(name)]
        raise SystemExit("stat fills changed: %s" % ", ".join(changed))
    print("sprite-match UI written; %d stat fills unchanged" % len(before))


if __name__ == "__main__":
    main()
