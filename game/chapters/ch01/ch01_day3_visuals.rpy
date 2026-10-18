# Chapter One — Day Three visual placeholders.
# Stable IDs are intentionally separate from final generated assets.
# Used by ch01_day3_lunch_walk (NTR lane cutout stand).

image bg ch01_d3_cutout_path = Composite(
    (1920, 1080),
    (0, 0), Solid("#9ccfd6"),
    (0, 700), Transform(Solid("#cdb98c"), xysize=(1920, 380)),
    (1120, 180), Transform(Solid("#e8d9a9"), xysize=(520, 560)),
    (90, 70), Text("BACKGROUND PLACEHOLDER\nDAY THREE — QUIET BEACH PATH / NOVELTY CUTOUT STAND", size=46, color="#ffffff"),
)

image cg ch01_d3_cutout_stranger = Composite(
    (1920, 1080),
    (0, 0), Solid("#6a4f5e"),
    (90, 70), Text("CG PLACEHOLDER\nDAY THREE CUTOUT STAND — LEIA + STRANGER (NTR LANE ONLY)\nNON-EXPLICIT / LEIA STUCK IN FRAME / CONSENT READS VISUALLY\nFINAL ART PENDING", size=48, color="#ffffff"),
)
