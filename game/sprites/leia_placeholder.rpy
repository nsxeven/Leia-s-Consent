# Placeholder Leia sprite used to prove the layered sprite pipeline.
# These displayables will be replaced by real ComfyUI-generated assets later.

# --- Pose bases ------------------------------------------------------------

image leia_placeholder_pose_p01 = Composite(
    (640, 900),
    (235, 80), Transform(Solid("#f0c7bd"), xysize=(170, 170)),
    (250, 245), Transform(Solid("#6f6179"), xysize=(140, 430)),
    (185, 285), Transform(Solid("#6f6179"), xysize=(55, 360)),
    (400, 285), Transform(Solid("#6f6179"), xysize=(55, 360)),
    (255, 665), Transform(Solid("#51485a"), xysize=(55, 205)),
    (330, 665), Transform(Solid("#51485a"), xysize=(55, 205)),
    (232, 25), Text("P01", size=28, color="#ffffff"),
)

image leia_placeholder_pose_p02 = Composite(
    (640, 900),
    (255, 80), Transform(Solid("#f0c7bd"), xysize=(170, 170)),
    (270, 245), Transform(Solid("#756276"), xysize=(140, 430)),
    (195, 305), Transform(Solid("#756276"), xysize=(65, 260), rotate=-15),
    (400, 300), Transform(Solid("#756276"), xysize=(65, 250), rotate=28),
    (275, 665), Transform(Solid("#564b58"), xysize=(55, 205)),
    (350, 665), Transform(Solid("#564b58"), xysize=(55, 205)),
    (252, 25), Text("P02", size=28, color="#ffffff"),
)

image leia_placeholder_pose_p03 = Composite(
    (640, 900),
    (220, 95), Transform(Solid("#f0c7bd"), xysize=(170, 170)),
    (235, 255), Transform(Solid("#655f72"), xysize=(140, 420)),
    (215, 330), Transform(Solid("#655f72"), xysize=(200, 50), rotate=18),
    (215, 390), Transform(Solid("#655f72"), xysize=(200, 50), rotate=-18),
    (240, 665), Transform(Solid("#4d4958"), xysize=(55, 205)),
    (315, 665), Transform(Solid("#4d4958"), xysize=(55, 205)),
    (217, 40), Text("P03", size=28, color="#ffffff"),
)

# --- Outfit overlays -------------------------------------------------------

image leia_placeholder_outfit_casual = Composite(
    (640, 900),
    (245, 295), Transform(Solid("#5f8fa8cc"), xysize=(150, 285)),
    (255, 485), Text("CASUAL", size=24, color="#ffffff"),
)

image leia_placeholder_outfit_pool_conservative = Composite(
    (640, 900),
    (250, 300), Transform(Solid("#4f8fbccc"), xysize=(140, 300)),
    (238, 475), Text("CLASSIC\nSWIM", size=22, color="#ffffff", text_align=0.5),
)

image leia_placeholder_outfit_pool_bolder = Composite(
    (640, 900),
    (255, 310), Transform(Solid("#d65f78dd"), xysize=(130, 105)),
    (265, 460), Transform(Solid("#d65f78dd"), xysize=(110, 125)),
    (245, 500), Text("BOLDER\nSWIM", size=22, color="#ffffff", text_align=0.5),
)

image leia_placeholder_outfit_date = Composite(
    (640, 900),
    (245, 295), Transform(Solid("#8d627fcc"), xysize=(150, 315)),
    (267, 500), Text("DATE", size=24, color="#ffffff"),
)

image leia_placeholder_outfit_after_hours = Composite(
    (640, 900),
    (245, 315), Transform(Solid("#3d3548dd"), xysize=(150, 270)),
    (255, 485), Text("AFTER\nHOURS", size=22, color="#ffffff", text_align=0.5),
)

# --- Expression overlays ---------------------------------------------------

image leia_placeholder_expr_neutral = Composite(
    (640, 900),
    (255, 155), Text("NEUTRAL", size=23, color="#27212c"),
)

image leia_placeholder_expr_smile = Composite(
    (640, 900),
    (270, 155), Text("SMILE", size=23, color="#27212c"),
)

image leia_placeholder_expr_teasing = Composite(
    (640, 900),
    (255, 155), Text("TEASING", size=23, color="#27212c"),
)

image leia_placeholder_expr_embarrassed = Composite(
    (640, 900),
    (225, 155), Text("EMBARRASSED", size=21, color="#27212c"),
)

image leia_placeholder_expr_annoyed = Composite(
    (640, 900),
    (258, 155), Text("ANNOYED", size=23, color="#27212c"),
)

# --- Layered character -----------------------------------------------------
# `config.adjust_attributes["leia"]` injects exactly one pose, outfit, and
# expression based on save-game state each time Leia is shown/refreshed.

layeredimage leia:
    xalign 0.34
    yalign 1.0

    group pose:
        attribute pose_p01 default:
            "leia_placeholder_pose_p01"
        attribute pose_p02:
            "leia_placeholder_pose_p02"
        attribute pose_p03:
            "leia_placeholder_pose_p03"

    group outfit:
        attribute outfit_casual default:
            "leia_placeholder_outfit_casual"
        attribute outfit_pool_conservative:
            "leia_placeholder_outfit_pool_conservative"
        attribute outfit_pool_bolder:
            "leia_placeholder_outfit_pool_bolder"
        attribute outfit_date:
            "leia_placeholder_outfit_date"
        attribute outfit_after_hours:
            "leia_placeholder_outfit_after_hours"

    group expression:
        attribute expr_neutral default:
            "leia_placeholder_expr_neutral"
        attribute expr_smile:
            "leia_placeholder_expr_smile"
        attribute expr_teasing:
            "leia_placeholder_expr_teasing"
        attribute expr_embarrassed:
            "leia_placeholder_expr_embarrassed"
        attribute expr_annoyed:
            "leia_placeholder_expr_annoyed"
