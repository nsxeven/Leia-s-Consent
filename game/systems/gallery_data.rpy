# Gallery data table: THE ONE PLACE to add or change gallery entries.
#
# Unit = one entry per scene sequence ("moment"), with variant pages. The
# unlock is derived from Ren'Py's own seen-image list (renpy.seen_image), so no
# story script calls unlock_gallery(): the moment a scene shows one of an
# entry's `cg <name>` images, the entry unlocks and that page becomes viewable.
# See systems/gallery.rpy for the rules and docs/BUILD_HANDOFF.md ("Gallery").
#
# TO ADD AN ENTRY (for example the Day Five CGs):
#   1. If it is a new day, add one row to GALLERY_TABS.
#   2. Add one gallery_row(...) call to GALLERY_TABLE below. `pages` lists the
#      stable image names exactly as the script shows them (`cg <name>`), in
#      the order the pages should appear. Variant pages (blue/white, a/b,
#      Ryan present/absent) are just extra pages.
#   3. If the CG is still a Composite text placeholder, add its name to
#      GALLERY_PLACEHOLDER_IMAGES (remove it again when final art lands).
#   4. No unlock lines are needed. Run `lint` and the gallery QA check.
# NEVER rename an entry id once shipped (ids are stored in persistent data).
# Never rename an image: point the same stable name at the new art instead.
#
# gallery_row fields: id, tab, title, description, pages, and optionally
#   mature=True   adult scene: the grid shows a masked cover and an 18+ badge
#   dream=True    dream/nightmare sequence ("not evidence" in canon)
#   route=...     free text shown after unlock ("All routes", "Love lane", ...)
# A page is either "image_name" or ("image_name", "Page label").

init -2 python:

    # (tab id, tab label, chapter, day). Chapter groups the counts; day is the sub-tab.
    GALLERY_TABS = (
        ("prologue", "Prologue", "prologue", 0),
        ("ch01_d1", "Day 1", "ch01", 1),
        ("ch01_d2", "Day 2", "ch01", 2),
        ("ch01_d3", "Day 3", "ch01", 3),
        ("ch01_d4", "Day 4", "ch01", 4),
        ("ch01_d5", "Day 5", "ch01", 5),
    )

    # Images that are still Composite text placeholders (final art pending).
    GALLERY_PLACEHOLDER_IMAGES = set([
        # Day 1
        "ch01_trip_catch", "ch01_drive_back_seating", "ch01_carry_dress_shift",
        "ch01_night_pool_attention", "ch01_movie_cuddle_blanket", "ch01_movie_no_blanket",
        "ch01_lounge_micro_test",
        "ch01_dream_towel_replay", "ch01_dream_towel_shift", "ch01_dream_towel_curtain",
        "ch01_dream_stranger_behind", "ch01_dream_stranger_look", "ch01_dream_stranger_reach",
        # Day 2
        "ch01_d2_photo_leia_maya",
        "ch01_d2_boutique_changing_room", "ch01_d2_boutique_reveal_ryan", "ch01_d2_boutique_reveal_julian",
        "ch01_d2_boutique_slip_ryan", "ch01_d2_boutique_slip_julian",
        "ch01_d2_pool_top_accident",
        "ch01_d2_love_pool_oral_01", "ch01_d2_love_pool_oral_02",
        "ch01_d2_dinner_reach", "ch01_d2_julian_underwear_reveal",
        "ch01_d2_love_bedroom_01", "ch01_d2_love_bedroom_02",
        "ch01_d2_exhib_bed_open_01", "ch01_d2_exhib_bed_open_02", "ch01_d2_exhib_bed_open_03", "ch01_d2_exhib_bed_open_04",
        "ch01_d2_ntr_dream_strangers", "ch01_d2_ntr_dream_julian_pool", "ch01_d2_ntr_dream_nhie", "ch01_d2_ntr_dream_wrong_room",
        # Day 3
        "ch01_d3_cutout_stranger",
        # Day 4
        "ch01_d4_photo_candid", "ch01_d4_photo_pose", "ch01_d4_photo_swap", "ch01_d4_photo_maya_julian",
        "ch01_d4_love_night_01", "ch01_d4_love_night_02",
        "ch01_d4_exhib_watching", "ch01_d4_exhib_terrace_01", "ch01_d4_exhib_terrace_02",
        "ch01_d4_ntr_terrace_talk",
        # Day 5 (ch01_d5_photo_private is a phone attachment only and is not mapped)
        "ch01_d5_snorkel_surface", "ch01_d5_cove_lunch_bee", "ch01_d5_photo_three",
        "ch01_d5_love_cove_swim", "ch01_d5_love_cove_secret",
        "ch01_d5_exhib_cove_01", "ch01_d5_exhib_cove_02", "ch01_d5_exhib_cove_watching",
        "ch01_d5_ntr_cove_talk", "ch01_d5_ntr_deck_alone", "ch01_d5_sunset_deck",
        "ch01_d5_love_night_01", "ch01_d5_exhib_night_01", "ch01_d5_ntr_night_01",
        "ch01_d5_invitation",
    ])

    GALLERY_TABLE = []

    def gallery_row(entry_id, tab, title, description, pages, mature=False, dream=False, route="All routes"):
        GALLERY_TABLE.append(dict(
            id=entry_id, tab=tab, title=title, description=description,
            pages=pages, mature=mature, dream=dream, route=route,
        ))

    # ------------------------------------------------------------------ Prologue
    gallery_row("pro_party_meet", "prologue", "The party",
        "The party where Ryan first notices Leia.",
        [("prologue_party_arrival", "Arrival"), ("prologue_party_couch", "On the couch")])
    gallery_row("pro_first_kiss", "prologue", "First kiss",
        "Their first kiss, a moment at a time.",
        [("prologue_first_kiss_01", "Moment 1"), ("prologue_first_kiss_02", "Moment 2"), ("prologue_first_kiss_03", "Moment 3")])
    gallery_row("pro_four_years_on", "prologue", "Four years on",
        "Four years later, packing for the trip.",
        [("prologue_present_stare", "The stare"), ("prologue_packing_banter", "Packing")])
    gallery_row("pro_departure", "prologue", "Departure",
        "Setting off for the villa.",
        ["prologue_departure"])

    # --------------------------------------------------------------------- Day 1
    gallery_row("d1_arrival", "ch01_d1", "Villa arrival",
        "Arriving at the villa.",
        ["ch01_villa_arrival"])
    gallery_row("d1_swimsuit_choice", "ch01_d1", "Which swimsuit?",
        "Leia decides what to wear to the pool.",
        [("ch01_swimsuit_choice", "The choice"), ("ch01_bedroom_window", "Bedroom window"),
         ("ch01_swimsuit_choice_blue", "Blue swimsuit"), ("ch01_swimsuit_choice_white", "White swimsuit")])
    gallery_row("d1_pool_sunscreen", "ch01_d1", "Sunscreen at the pool",
        "Sunscreen, and a hand that pulls Leia into the water. Blue or white swimsuit, depending on the choice.",
        [("ch01_sunscreen_blue", "Sunscreen (blue)"), ("ch01_sunscreen_white", "Sunscreen (white)"),
         ("ch01_sunscreen_apply_blue", "Applying (blue)"), ("ch01_sunscreen_apply_white", "Applying (white)"),
         ("ch01_pool_hand_pull_blue", "Hand pull (blue)"), ("ch01_pool_hand_pull_white", "Hand pull (white)")])
    gallery_row("d1_pool_photos", "ch01_d1", "Pool photography",
        "Julian takes photos by the pool. The pages follow the swimsuit and the shots that were taken.",
        [("ch01_photo_group_blue", "Group (blue)"), ("ch01_photo_group_white", "Group (white)"),
         ("ch01_photo_awkward_a", "Awkward (a)"), ("ch01_photo_awkward_b", "Awkward (b)"),
         ("ch01_photo_capture_01_a", "Capture 1 (a)"), ("ch01_photo_capture_01_b", "Capture 1 (b)"),
         ("ch01_photo_capture_02_a", "Capture 2 (a)"), ("ch01_photo_capture_02_b", "Capture 2 (b)"),
         ("ch01_photo_capture_03_a", "Capture 3 (a)"), ("ch01_photo_capture_03_b", "Capture 3 (b)")])
    gallery_row("d1_towel", "ch01_d1", "The towel",
        "A towel shifts at the poolside.",
        [("ch01_towel_call_down", "Called down"), ("ch01_towel_shift_01", "Shift 1"), ("ch01_towel_shift_02", "Shift 2"),
         ("ch01_towel_shift_03", "Shift 3"), ("ch01_towel_realization", "Realization")])
    gallery_row("d1_towel_did_he_see", "ch01_d1", "Did he see?",
        "Leia wonders what Julian saw.",
        ["ch01_towel_did_he_see"])
    gallery_row("d1_drive_to_dinner", "ch01_d1", "Drive to dinner",
        "On the way to dinner.",
        ["ch01_drive_to_dinner"])
    gallery_row("d1_dinner_arrival", "ch01_d1", "Dinner",
        "Arriving at the restaurant.",
        ["ch01_dinner_arrival"])
    gallery_row("d1_dinner_spill", "ch01_d1", "The spill",
        "A stranger, a photo, and a spilled drink.",
        [("ch01_dinner_photo_ask", "The photo ask"), ("ch01_dinner_spill_01", "Impact"), ("ch01_dinner_spill_02", "Aftermath"),
         ("ch01_dinner_spill_03", "The glance"), ("ch01_dinner_spill_04", "A second glance")])
    gallery_row("d1_dinner_restroom", "ch01_d1", "Back from the restroom",
        "On her way back from the restroom, another man slows in the corridor.",
        [("ch01_dinner_restroom_return_01", "Return 1"), ("ch01_dinner_restroom_return_02", "Return 2")])
    gallery_row("d1_trip_catch", "ch01_d1", "The catch",
        "Leia's heel catches on the path and Julian catches her.",
        ["ch01_trip_catch"])
    gallery_row("d1_drive_back", "ch01_d1", "Drive back",
        "The ride home: Julian up front, Leia in the back seat.",
        ["ch01_drive_back_seating"])
    gallery_row("d1_julian_carry", "ch01_d1", "Carried home",
        "Leia is carried inside.",
        [("ch01_julian_carry", "The carry"), ("ch01_carry_dress_shift", "Dress shift")])
    gallery_row("d1_night_pool", "ch01_d1", "Night pool",
        "Julian's eyes drift toward Leia by the pool at night.",
        ["ch01_night_pool_attention"])
    gallery_row("d1_movie_night", "ch01_d1", "Movie night",
        "Movie night on the couch, with or without the blanket.",
        [("ch01_movie_cuddle_blanket", "With the blanket"), ("ch01_movie_no_blanket", "No blanket")])
    gallery_row("d1_lounge_micro_test", "ch01_d1", "Lounge",
        "A moment in the lounge when nothing accidental forces the decision.",
        ["ch01_lounge_micro_test"])
    gallery_row("d1_dream", "ch01_d1", "The dream",
        "Leia's dream at the end of the day. A dream is not evidence.",
        [("ch01_dream_towel_replay", "Towel replay"), ("ch01_dream_towel_shift", "Towel shift"), ("ch01_dream_towel_curtain", "Curtain"),
         ("ch01_dream_stranger_behind", "Behind her"), ("ch01_dream_stranger_look", "The look"), ("ch01_dream_stranger_reach", "The reach")],
        dream=True)

    # --------------------------------------------------------------------- Day 2
    gallery_row("d2_photo_leia_maya", "ch01_d2", "Leia and Maya",
        "A photo of Leia and Maya.",
        ["ch01_d2_photo_leia_maya"])
    gallery_row("d2_boutique", "ch01_d2", "Boutique",
        "Maya pushes Leia to try on the cutout mini. Pages depend on who is there.",
        [("ch01_d2_boutique_changing_room", "Changing room"), ("ch01_d2_boutique_reveal_ryan", "Reveal (Ryan)"),
         ("ch01_d2_boutique_reveal_julian", "Reveal (Julian)"), ("ch01_d2_boutique_slip_ryan", "Slip (Ryan)"),
         ("ch01_d2_boutique_slip_julian", "Slip (Julian)")])
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

    # --------------------------------------------------------------------- Day 3
    gallery_row("d3_cutout_stranger", "ch01_d3", "The cutout stand",
        "Leia chooses to stay in the novelty cutout stand on the beach path.",
        ["ch01_d3_cutout_stranger"],
        route="NTR lane (Leia chose it)")

    # --------------------------------------------------------------------- Day 4
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

    # --------------------------------------------------------------------- Day 5
    # Day 5 CGs come from 07_cg_checklist.md (16 ids). `ch01_d5_photo_private` is only ever shown as a phone
    # attachment (never by a show/scene statement), so it cannot unlock by seen-image and is left unmapped.
    gallery_row("d5_snorkel", "ch01_d5", "Snorkel",
        "Leia surfaces from the reef, laughing.",
        ["ch01_d5_snorkel_surface"])
    gallery_row("d5_cove_lunch", "ch01_d5", "Cove lunch",
        "Lunch in the cove, and the group photo. The bee page appears only if the bee was filmed.",
        [("ch01_d5_cove_lunch_bee", "The bee"), ("ch01_d5_photo_three", "Group photo")])
    gallery_row("d5_love_cove", "ch01_d5", "The secret cove",
        "A swim and a quiet photo in a cove of their own.",
        [("ch01_d5_love_cove_swim", "The swim"), ("ch01_d5_love_cove_secret", "On the rock")],
        mature=True, route="Love lane (also the Exhibition 'just us' opt-out)")
    gallery_row("d5_exhib_cove", "ch01_d5", "Cove, in the sun",
        "Leia decides how far to go on the rocks. Pages depend on her call and on whether Ryan likes watching.",
        [("ch01_d5_exhib_cove_watching", "Watching"), ("ch01_d5_exhib_cove_01", "On the rock, 1"), ("ch01_d5_exhib_cove_02", "On the rock, 2")],
        mature=True, route="Exhibitionism lane")
    gallery_row("d5_ntr_cove_talk", "ch01_d5", "The talk on the rock",
        "A serious talk in the cove, with the hairclip in her hands.",
        ["ch01_d5_ntr_cove_talk"],
        route="NTR lane (repaired)")
    gallery_row("d5_ntr_deck_alone", "ch01_d5", "At the rail",
        "Leia alone at the stern rail, her back to him.",
        ["ch01_d5_ntr_deck_alone"],
        route="NTR lane (unresolved or confirmed)")
    gallery_row("d5_sunset_deck", "ch01_d5", "Sunset on the deck",
        "The last of the sunset across the stern.",
        ["ch01_d5_sunset_deck"],
        route="Love, Exhibition and NTR repaired")
    gallery_row("d5_love_night", "ch01_d5", "Lantern light",
        "Night on the boat, the lantern turned down low.",
        ["ch01_d5_love_night_01"],
        mature=True, route="Love lane (also the Exhibition 'just us' opt-out)")
    gallery_row("d5_exhib_night", "ch01_d5", "Under the stars",
        "Night on the deck cushions under a blanket.",
        ["ch01_d5_exhib_night_01"],
        mature=True, route="Exhibitionism lane")
    gallery_row("d5_ntr_night", "ch01_d5", "The hairclip",
        "Leia sets the hairclip down beside the lantern.",
        ["ch01_d5_ntr_night_01"],
        mature=True, route="NTR lane (repaired)")
    gallery_row("d5_invitation", "ch01_d5", "The invitation",
        "A printed invitation pinned to a post on the dawn pier.",
        ["ch01_d5_invitation"])
