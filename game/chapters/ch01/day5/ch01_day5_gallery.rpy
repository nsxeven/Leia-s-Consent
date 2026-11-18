# Day Five pack - Gallery rows (the Day 5 tab).
#
# One gallery_row(...) per scene sequence; pages are the stable `cg <name>` images in display
#   order. Unlocks follow the CGs the player has seen. API and rules: systems/gallery_data.rpy;
#   guide: docs/DAY_PACK.md. Never rename a shipped entry id or an image name.
# Load order: init -2 (systems/gallery_data.rpy defines the helpers at init -3 and orders the
#   tabs and rows by Day at init -1).

init -2 python:

    gallery_tab("ch01_d5", "Day 5", "ch01", 5, accent="#5f7a6a")

    # CGs that are still text placeholders (final art pending): remove a name when its art lands.
    GALLERY_PLACEHOLDER_IMAGES.update([
        "ch01_d5_snorkel_surface", "ch01_d5_cove_lunch_bee", "ch01_d5_photo_three",
        "ch01_d5_love_cove_swim", "ch01_d5_love_cove_secret",
        "ch01_d5_exhib_cove_01", "ch01_d5_exhib_cove_02", "ch01_d5_exhib_cove_watching",
        "ch01_d5_ntr_cove_talk", "ch01_d5_ntr_deck_alone", "ch01_d5_sunset_deck",
        "ch01_d5_love_night_01", "ch01_d5_exhib_night_01", "ch01_d5_ntr_night_01",
        "ch01_d5_invitation",
    ])

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


# Title screen reel (systems/title_screen.rpy): this Day's rows that may show by default.
# load order: init 1, after the reel's table (init 0).
init 1 python:
    LC_TITLE_SAFE_GALLERY = LC_TITLE_SAFE_GALLERY + (
        "d5_snorkel", "d5_cove_lunch", "d5_sunset_deck", "d5_invitation",
    )
