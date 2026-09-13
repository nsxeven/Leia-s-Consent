# Chapter One visual placeholders.
# Keep these stable image names when replacing placeholders with final assets.

image bg ch01_resort_arrival = Composite(
    (1920, 1080),
    (0, 0), Solid("#4b9ca8"),
    (0, 650), Transform(Solid("#d9c89b"), xysize=(1920, 430)),
    (0, 0), Transform(Solid("#79cce2"), xysize=(1920, 390)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-01 — RESORT ISLAND ARRIVAL", size=46, color="#ffffff"),
)

image bg ch01_villa_exterior = Composite(
    (1920, 1080),
    (0, 0), Solid("#73bfd1"),
    (250, 210), Transform(Solid("#f2eadc"), xysize=(1420, 650)),
    (340, 300), Transform(Solid("#b9e4ec"), xysize=(1240, 230)),
    (0, 820), Transform(Solid("#d9c89b"), xysize=(1920, 260)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-02 — PRIVATE BEACHFRONT VILLA", size=46, color="#24383d"),
)

image bg ch01_villa_living = Composite(
    (1920, 1080),
    (0, 0), Solid("#e8dfd2"),
    (70, 190), Transform(Solid("#bfe5eb"), xysize=(1780, 500)),
    (110, 700), Transform(Solid("#c9aa82"), xysize=(1700, 300)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-03 — VILLA LIVING ROOM", size=46, color="#3b3632"),
)

image bg ch01_villa_pool = Composite(
    (1920, 1080),
    (0, 0), Solid("#8fd2e2"),
    (0, 500), Transform(Solid("#2d9fc2"), xysize=(1920, 360)),
    (0, 860), Transform(Solid("#e2cf9d"), xysize=(1920, 220)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-04 — PRIVATE POOL + BEACH VIEW", size=46, color="#ffffff"),
)

image bg ch01_master_bedroom = Composite(
    (1920, 1080),
    (0, 0), Solid("#ddd4ca"),
    (840, 80), Transform(Solid("#9bd4e5"), xysize=(980, 730)),
    (120, 650), Transform(Solid("#f4f0e8"), xysize=(820, 300)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-05 — MASTER BEDROOM / GLASS WALL", size=46, color="#3d3936"),
    (900, 170), Text("FLOOR-TO-CEILING GLASS\nPOOL + OCEAN VIEW", size=34, color="#ffffff", text_align=0.5),
)

image bg ch01_master_bedroom_curtains = Composite(
    (1920, 1080),
    (0, 0), Solid("#ddd4ca"),
    (840, 80), Transform(Solid("#bcdce2"), xysize=(980, 730)),
    (840, 80), Transform(Solid("#f4f1eb88"), xysize=(450, 730)),
    (1370, 80), Transform(Solid("#f4f1eb88"), xysize=(450, 730)),
    (120, 650), Transform(Solid("#f4f0e8"), xysize=(820, 300)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-06 — LIGHT CURTAINS DRAWN", size=46, color="#3d3936"),
)

image bg ch01_julian_bedroom = Composite(
    (1920, 1080),
    (0, 0), Solid("#d6cec5"),
    (930, 110), Transform(Solid("#9bd4e5"), xysize=(820, 690)),
    (150, 680), Transform(Solid("#ece7df"), xysize=(720, 270)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-07 — JULIAN'S ADJACENT BEDROOM", size=46, color="#3d3936"),
)

transform ch01_leia_left:
    xalign 0.18
    yalign 1.0

transform ch01_julian_right:
    xalign 0.82
    yalign 1.0

