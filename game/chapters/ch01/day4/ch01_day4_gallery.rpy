# Day Four pack - Gallery rows (the Day 4 tab).
#
# One gallery_row(...) per scene sequence; pages are the stable `cg <name>` images in display
#   order. Unlocks follow the CGs the player has seen. API and rules: systems/gallery_data.rpy;
#   guide: docs/DAY_PACK.md. Never rename a shipped entry id or an image name.
# Load order: init -2 (systems/gallery_data.rpy defines the helpers at init -3 and orders the
#   tabs and rows by Day at init -1).

init -2 python:

    gallery_tab("ch01_d4", "Day 4", "ch01", 4, accent="#556b78")

    # CGs that are still text placeholders (final art pending): remove a name when its art lands.
    GALLERY_PLACEHOLDER_IMAGES.update([
        "ch01_d4_photo_candid", "ch01_d4_photo_pose", "ch01_d4_photo_swap", "ch01_d4_photo_maya_julian",
        "ch01_d4_love_night_01", "ch01_d4_love_night_02",
        "ch01_d4_exhib_watching", "ch01_d4_exhib_terrace_01", "ch01_d4_exhib_terrace_02",
        "ch01_d4_ntr_terrace_talk",
    ])

    # Added after the 31-entry proposal (written before Day Four landed). Delete this block to drop them.
    gallery_row("d4_market_photo", "ch01_d4", "Market photo",
        "A photo at the market. The page follows the photo style chosen.",
        [("ch01_d4_photo_candid", "Candid"), ("ch01_d4_photo_pose", "Pose"), ("ch01_d4_photo_swap", "Swap")])
    gallery_row("d4_photo_hunt", "ch01_d4", "The judges' table",
        "Maya judges the photo hunt.",
        ["ch01_d4_photo_maya_julian"])
    gallery_row("d4_love_night", "ch01_d4", "Lamplight",
        "A slow night in lamplight.",
        [("ch01_d4_love_night_01", "Slow dance"), ("ch01_d4_love_night_02", "Curtains drawn")],
        mature=True, route="Love lane (page 2 also on Exhibitionism)")
    gallery_row("d4_exhib_terrace", "ch01_d4", "The terrace",
        "Leia decides how far to go on the terrace.",
        [("ch01_d4_exhib_watching", "Watching"), ("ch01_d4_exhib_terrace_01", "Wrap, 1"), ("ch01_d4_exhib_terrace_02", "Wrap, 2")],
        mature=True, route="Exhibitionism lane")
    gallery_row("d4_ntr_terrace_talk", "ch01_d4", "The talk",
        "A quiet talk on the terrace.",
        ["ch01_d4_ntr_terrace_talk"],
        route="NTR lane")


# Title screen reel (systems/title_screen.rpy): this Day's rows that may show by default.
# load order: init 1, after the reel's table (init 0).
init 1 python:
    LC_TITLE_SAFE_GALLERY = LC_TITLE_SAFE_GALLERY + (
        "d4_market_photo", "d4_photo_hunt",
    )
