# Chapter One visual placeholders.
# Keep these stable image names when replacing placeholders with final assets.

image bg ch01_resort_arrival = Composite(
    (1920, 1080),
    (0, 0), Solid("#4b9ca8"),
    (0, 650), Transform(Solid("#d9c89b"), xysize=(1920, 430)),
    (0, 0), Transform(Solid("#79cce2"), xysize=(1920, 390)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nBG-CH1-01 — RESORT ISLAND ARRIVAL", size=46, color="#ffffff"),
)

image bg ch01_villa_exterior = At("images/backgrounds/chapter 1/ch01_villa_arrival.webp", prologue_bg_blur)

image bg ch01_villa_living = At("images/backgrounds/villa/villa_living_day.webp", prologue_bg_blur)

image bg ch01_villa_pool = At("images/backgrounds/villa/villa_pool_day.webp", prologue_bg_blur)

image bg ch01_master_bedroom = At("images/backgrounds/villa/villa_master_day.webp", prologue_bg_blur)

image bg ch01_master_bedroom_curtains = At("images/backgrounds/villa/villa_master_curtains_day.webp", prologue_bg_blur)

image cg ch01_pre_pool_towel_curtains = Composite(
    (1920, 1080),
    (0, 0), Solid("#d9d0c7"),
    (0, 0), Transform(Solid("#9bd4e5"), xysize=(1920, 1080)),
    (90, 70), Text("CG PLACEHOLDER\\nCH01-PRE-POOL-TOWEL — LEIA DRAWS SHEER CURTAIN\\nTOWEL / MASTER BEDROOM / DAY", size=52, color="#ffffff"),
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

