# Day One pack - Gallery rows (the Day 1 tab).
#
# One gallery_row(...) per scene sequence; pages are the stable `cg <name>` images in display
#   order. Unlocks follow the CGs the player has seen. API and rules: systems/gallery_data.rpy;
#   guide: docs/DAY_PACK.md. Never rename a shipped entry id or an image name.
# Load order: init -2 (systems/gallery_data.rpy defines the helpers at init -3 and orders the
#   tabs and rows by Day at init -1).

init -2 python:

    gallery_tab("ch01_d1", "Day 1", "ch01", 1, accent="#8f5d75")

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
    gallery_row("d1_dress_reveal", "ch01_d1", "The dress",
        "Leia steps out in the dress she packed for dinner.",
        ["ch01_dress_reveal"])
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
    gallery_row("d1_sticky_bra", "ch01_d1", "Giving up",
        "Leia leans in to whisper that her sticky bra is giving up.",
        ["ch01_dinner_sticky_bra"])
    gallery_row("d1_dinner_restroom", "ch01_d1", "Back from the restroom",
        "On her way back from the restroom, another man slows in the corridor.",
        [("ch01_dinner_restroom_return_01", "Return 1"), ("ch01_dinner_restroom_return_02", "Return 2")])
    gallery_row("d1_walk_back", "ch01_d1", "Walk to the shop",
        "Leia hangs on Ryan's arm, then Maya calls.",
        [("ch01_walk_back_01", "On my arm"), ("ch01_walk_back_call", "Maya calling")])
    gallery_row("d1_trip_catch", "ch01_d1", "The catch",
        "Leia's heel catches on the path and Julian catches her.",
        [("ch01_trip_catch", "The catch"), ("ch01_trip_catch_followup", "Realizing"), ("ch01_trip_catch_aftermath", "Aftermath")])
    gallery_row("d1_drive_back", "ch01_d1", "Drive back",
        "The ride home: Julian up front, Leia in the back seat.",
        ["ch01_drive_back_seating"])
    gallery_row("d1_julian_carry", "ch01_d1", "Carried home",
        "Leia is carried inside.",
        [("ch01_julian_carry", "The carry"), ("ch01_carry_walk", "To the door"), ("ch01_carry_dress_shift", "Dress shift"),
         ("ch01_sofa_half_asleep_night", "Back to sleep")])
    gallery_row("d1_night_pool", "ch01_d1", "Night pool",
        "Julian's eyes drift toward Leia by the pool at night.",
        ["ch01_night_pool_attention"])
    gallery_row("d1_julian_drink", "ch01_d1", "A drink for the driver",
        "Back downstairs after changing, Julian hands Ryan a whisky.",
        ["ch01_villa_night_julian_drink"])
    gallery_row("d1_movie_night", "ch01_d1", "Movie night",
        "Movie night on the couch, with or without the blanket.",
        [("ch01_movie_cuddle_blanket", "With the blanket"), ("ch01_movie_blanket_hand", "Under the blanket"), ("ch01_movie_no_blanket", "No blanket")])
    gallery_row("d1_movie_risk", "ch01_d1", "One turn of the head",
        "Blanket off, Leia nods, and Ryan's hand finds her backside while Julian watches the movie.",
        [("ch01_movie_ass_grab_01", "The risk"), ("ch01_movie_ass_grab_02", "The squeeze")])
    gallery_row("d1_movie_glance", "ch01_d1", "The glance",
        "Back on the sofa, Leia checks where everyone's eyes are.",
        [("ch01_movie_micro_test_glance", "The glance")])
    gallery_row("d1_lounge_micro_test", "ch01_d1", "Lounge",
        "A moment in the lounge when nothing accidental forces the decision.",
        [("ch01_lounge_micro_test", "Her choice")],
        mature=True)
    gallery_row("d1_dream", "ch01_d1", "The dream",
        "Ryan's dream at the end of the day. A dream is not evidence.",
        [("ch01_dream_dinner_beside", "Beside her"), ("ch01_dream_dinner_grab", "The grab"), ("ch01_dream_dinner_rub", "She lets him")],
        mature=True, dream=True)
    gallery_row("d1_wake_up", "ch01_d1", "Waking up",
        "Ryan wakes from the dream. Leia is asleep beside him, exactly where she'd been.",
        ["ch01_dream_wake_night"])
