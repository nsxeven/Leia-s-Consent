# Chapter One — Day Two visual placeholders.
# Stable IDs are intentionally separate from final generated assets.

image bg ch01_d2_breakfast = Composite(
    (1920, 1080),
    (0, 0), Solid("#d8c9ad"),
    (0, 610), Transform(Solid("#c59b72"), xysize=(1920, 470)),
    (1020, 90), Transform(Solid("#8cc9d7"), xysize=(760, 450)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — VILLA BREAKFAST", size=46, color="#352f2b"),
)

image bg ch01_d2_cafe = Composite(
    (1920, 1080),
    (0, 0), Solid("#d8c2a1"),
    (0, 720), Transform(Solid("#8d6c50"), xysize=(1920, 360)),
    (1080, 120), Transform(Solid("#8fcbd7"), xysize=(650, 470)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — ISLAND CAFE / BRUNCH", size=46, color="#ffffff"),
)

image bg ch01_d2_island_day = Composite(
    (1920, 1080),
    (0, 0), Solid("#86cbd8"),
    (0, 620), Transform(Solid("#d8bd86"), xysize=(1920, 460)),
    (300, 180), Transform(Solid("#f0e2cb"), xysize=(430, 500)),
    (850, 220), Transform(Solid("#e7d7bc"), xysize=(620, 440)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — ISLAND SHOPS / PHOTO WALK", size=46, color="#ffffff"),
)

image bg ch01_d2_sunset = Composite(
    (1920, 1080),
    (0, 0), Solid("#b06e6e"),
    (0, 260), Transform(Solid("#d79072"), xysize=(1920, 430)),
    (0, 690), Transform(Solid("#4e8191"), xysize=(1920, 390)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — SUNSET WALK", size=46, color="#ffffff"),
)

image bg ch01_d2_dinner = Composite(
    (1920, 1080),
    (0, 0), Solid("#342c30"),
    (0, 690), Transform(Solid("#755742"), xysize=(1920, 390)),
    (320, 540), Transform(Solid("#9b724f"), xysize=(1280, 220)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — RECTANGULAR DINNER TABLE\nLEIA + MAYA TOGETHER / RYAN + JULIAN OPPOSITE", size=44, color="#ffffff"),
)

image bg ch01_d2_game_night = Composite(
    (1920, 1080),
    (0, 0), Solid("#27252e"),
    (0, 760), Transform(Solid("#5d514a"), xysize=(1920, 320)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY TWO — VILLA DRINKS / NEVER HAVE I EVER", size=46, color="#ffffff"),
)

image cg ch01_d2_photo_leia_maya = Composite(
    (1920, 1080),
    (0, 0), Solid("#6b8fa0"),
    (90, 70), Text("CG PLACEHOLDER\nDAY TWO PHOTO — LEIA + MAYA\nNEW FRIENDSHIP / RELAXED PAIRING", size=50, color="#ffffff"),
)

image cg ch01_d2_pool_top_accident = Composite(
    (1920, 1080),
    (0, 0), Solid("#277f9f"),
    (90, 70), Text("CG PLACEHOLDER\nDAY TWO POOL — BIKINI-TOP ACCIDENT\nFLOATING TOP / ROUTE-DEPENDENT COMPANY", size=50, color="#ffffff"),
)

image cg ch01_d2_dinner_reach = Composite(
    (1920, 1080),
    (0, 0), Solid("#5a3942"),
    (90, 70), Text("CG PLACEHOLDER\nDAY TWO DINNER — DELIBERATE REACH\nLOOSE NECKLINE / RYAN + JULIAN VIEWING ANGLE", size=50, color="#ffffff"),
)

image cg ch01_d2_julian_underwear_reveal = Composite(
    (1920, 1080),
    (0, 0), Solid("#393744"),
    (90, 70), Text("CG PLACEHOLDER\nNEVER HAVE I EVER — JULIAN DOWN TO UNDERWEAR\nREACTIONS CARRY THE REVEAL", size=50, color="#ffffff"),
)

# Maya is still awaiting final sprite production. Keep a transparent placeholder
# so Day Two remains fully playable in the meantime.
image maya = Composite(
    (560, 900),
    (0, 0), Solid("#00000000"),
    (170, 120), Transform(Solid("#8e6f7f"), xysize=(220, 220)),
    (115, 330), Transform(Solid("#675565"), xysize=(330, 500)),
    (150, 520), Text("MAYA\nSPRITE\nPLACEHOLDER", size=30, color="#ffffff", text_align=0.5),
)

transform ch01_d2_leia_left:
    xalign 0.16
    yalign 1.0

transform ch01_d2_maya_center:
    xalign 0.50
    yalign 1.0

transform ch01_d2_julian_right:
    xalign 0.84
    yalign 1.0

transform ch01_d2_maya_right:
    xalign 0.80
    yalign 1.0

transform ch01_d2_julian_left:
    xalign 0.20
    yalign 1.0
