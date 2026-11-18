# Day Two pack - Gallery rows (the Day 2 tab).
#
# One gallery_row(...) per scene sequence; pages are the stable `cg <name>` images in display
#   order. Unlocks follow the CGs the player has seen. API and rules: systems/gallery_data.rpy;
#   guide: docs/DAY_PACK.md. Never rename a shipped entry id or an image name.
# Load order: init -2 (systems/gallery_data.rpy defines the helpers at init -3 and orders the
#   tabs and rows by Day at init -1).

init -2 python:

    gallery_tab("ch01_d2", "Day 2", "ch01", 2, accent="#70566f")

    # CGs that are still text placeholders (final art pending): remove a name when its art lands.
    GALLERY_PLACEHOLDER_IMAGES.update([
        "ch01_d2_boutique_reveal_ryan", "ch01_d2_boutique_reveal_julian",
        "ch01_d2_pool_top_accident",
        "d2_cafe_stranger",
        "ch01_d2_love_pool_oral_01", "ch01_d2_love_pool_oral_02",
        "ch01_d2_dinner_reach", "ch01_d2_julian_underwear_reveal",
        "ch01_d2_love_bedroom_01", "ch01_d2_love_bedroom_02",
        "ch01_d2_exhib_bed_open_01", "ch01_d2_exhib_bed_open_02", "ch01_d2_exhib_bed_open_03", "ch01_d2_exhib_bed_open_04",
        "ch01_d2_ntr_dream_strangers", "ch01_d2_ntr_dream_julian_pool", "ch01_d2_ntr_dream_nhie", "ch01_d2_ntr_dream_wrong_room",
    ])

    gallery_row("d2_morning", "ch01_d2", "Sleeping beauty",
        "Day Two, 11:00. Julian's alarm text goes off; Leia does not.",
        [("ch01_d2_leia_sleeping", "Asleep"), ("ch01_d2_leia_waking", "Waking up")])
    gallery_row("d2_breakfast", "ch01_d2", "Breakfast",
        "A morning table, a message, and one very suspicious glance.",
        [("ch01_d2_breakfast_01", "Easy rhythm"), ("ch01_d2_breakfast_02", "Maya's message"),
         ("ch01_d2_breakfast_03", "Pout softening"), ("ch01_d2_breakfast_04", "Caught")])
    gallery_row("d2_breakfast_pov", "ch01_d2", "Julian's view",
        "A glance that should probably have stayed a glance.",
        [("ch01_d2_breakfast_julian_pov", "Julian's POV")], mature=True)
    gallery_row("d2_meet_maya", "ch01_d2", "Meeting Maya",
        "Maya arrives at the café; the first conversation turns into a new friendship.",
        [("ch01_d2_maya_reveal", "At the door"), ("ch01_d2_maya_cafe_01", "At the table"),
         ("ch01_d2_maya_cafe_02", "Getting along")])
    gallery_row("d2_photo_leia_maya", "ch01_d2", "Leia and Maya",
        "Maya's selfie with Leia, then the new Trip Group picture with all four.",
        [("ch01_d2_photo_leia_maya", "Leia and Maya"), ("ch01_d2_photo_group", "Trip Group")])
    gallery_row("d2_mall_arrival", "ch01_d2", "Island mall",
        "Julian's quick shirt stop leads Leia and Maya past a boutique window and inside.",
        [("ch01_d2_mall_arrival", "Arriving"), ("ch01_d2_mall_boutique_window", "At the window"),
         ("ch01_d2_shop_dresses", "Red or black?")])
    gallery_row("d2_boutique", "ch01_d2", "Boutique",
        "Maya pushes Leia to try on the cutout mini, then talks her out of the changing room.",
        [("ch01_d2_boutique_changing_room", "The dress"), ("ch01_d2_changing_room_02", "On"),
         ("ch01_d2_changing_room_03", "A size too small"), ("ch01_d2_changing_room_capture", "Selfie"),
         ("ch01_d2_changing_room_04", "Maya?"), ("ch01_d2_shop_showoff", "Facing the mirror")])
    gallery_row("d2_boutique_malfunction", "ch01_d2", "Wardrobe malfunction",
        "A stranger compliments Maya, and Maya lets go of the one thing she promised to hold.",
        [("ch01_d2_shop_showoff_02", "The compliment"), ("ch01_d2_shop_showoff_03", "Showing off"),
         ("ch01_d2_shop_showoff_04", "Everyone saw"), ("ch01_d2_shop_showoff_05", "Covered (sort of)")], mature=True)
    gallery_row("d2_boutique_pov", "ch01_d2", "A stranger's view",
        "Somebody by the racks stopped pretending to look at shirts.",
        [("ch01_d2_shop_showoff_stranger_pov", "A stranger's POV")], mature=True)
    gallery_row("d2_cafe_stranger", "ch01_d2", "The café counter",
        "Leia waits for his frappuccino, and a stranger leans in.",
        ["d2_cafe_stranger"],
        route="Leia's errand (every lane)")
    gallery_row("d2_pool_top_accident", "ch01_d2", "The bee",
        "An accident in the pool: Leia hides behind Julian's shoulders.",
        ["ch01_d2_pool_top_accident"])
    gallery_row("d2_sunset_love", "ch01_d2", "Sunset (private)",
        "A private moment at sunset.",
        [("ch01_d2_love_pool_oral_01", "Sunset 1"), ("ch01_d2_love_pool_oral_02", "Sunset 2")],
        mature=True, route="Love lane")
    gallery_row("d2_dinner_reach", "ch01_d2", "The reach",
        "Leia leans across the table instead of asking for the dish.",
        ["ch01_d2_dinner_reach"],
        route="NTR-risk lane (soft gate) or Exhibitionism lane (low-cut dress)")
    gallery_row("d2_julian_underwear", "ch01_d2", "Sunglasses loophole",
        "Julian sits back down in his underwear and the room goes quiet.",
        ["ch01_d2_julian_underwear_reveal"])
    gallery_row("d2_bedroom_love", "ch01_d2", "Curtains drawn",
        "The bedroom, curtains drawn.",
        [("ch01_d2_love_bedroom_01", "Bedroom 1"), ("ch01_d2_love_bedroom_02", "Bedroom 2")],
        mature=True, route="Love ending")
    gallery_row("d2_bedroom_open", "ch01_d2", "Curtains open",
        "The bedroom, curtains open.",
        [("ch01_d2_exhib_bed_open_01", "Open 1"), ("ch01_d2_exhib_bed_open_02", "Open 2"),
         ("ch01_d2_exhib_bed_open_03", "Open 3"), ("ch01_d2_exhib_bed_open_04", "Open 4")],
        mature=True, route="Exhibitionism ending (or Love with open curtains)")
    gallery_row("d2_ntr_nightmare", "ch01_d2", "The nightmare",
        "A nightmare after a hard night. A dream is not evidence.",
        [("ch01_d2_ntr_dream_strangers", "Strangers"), ("ch01_d2_ntr_dream_julian_pool", "Julian at the pool"),
         ("ch01_d2_ntr_dream_nhie", "Never Have I Ever"), ("ch01_d2_ntr_dream_wrong_room", "The wrong room")],
        mature=True, dream=True, route="NTR-risk lane")


# Title screen reel (systems/title_screen.rpy): this Day's rows that may show by default.
# load order: init 1, after the reel's table (init 0).
init 1 python:
    LC_TITLE_SAFE_GALLERY = LC_TITLE_SAFE_GALLERY + (
        "d2_photo_leia_maya", "d2_boutique",
    )
