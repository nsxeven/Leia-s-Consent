# Gallery data - the engine half: the helpers every Day pack's *_gallery.rpy uses
#
# Purpose: Each Day pack registers its Gallery tab and rows in its own *_gallery.rpy
#   (game/chapters/<day folder>/, init -2): one gallery_row per scene sequence (moment), pages =
#   the stable `cg <name>` images in display order. Unlocks follow the CGs the player has seen, so
#   story files need no unlock lines. This file defines the helpers (init -3) and, once every Day
#   has registered, puts the tabs in Day order and each Day's rows after the previous Day's
#   (init -1). Never rename a shipped entry id or an image name. Rules in systems/gallery.rpy;
#   guide: docs/DAY_PACK.md.
#
# Public API (call these from scenes/screens):
#   gallery_tab(tab_id, label, chapter, day, accent) -> None
#       register a Day's tab: (tab id, label, chapter, day number), tile tint
#   gallery_row(entry_id, tab, title, description, pages, mature=False, dream=False, route="All routes") -> None
#       build one entry (id, tab, title, description, pages, mature/dream/route)
#   GALLERY_TABS                              (tab id, label, chapter, day) rows in Day order
#   GALLERY_TABLE                             the gallery_row(...) entries in Day order
#   GALLERY_TAB_ACCENTS                       {tab id: card/preview tint}
#   GALLERY_PLACEHOLDER_IMAGES                CGs still shown as text placeholders (each Day pack
#       adds its own with GALLERY_PLACEHOLDER_IMAGES.update([...]))
#
# Internal (helpers for this file and its screens; do not call from scenes): _gallery_tab_rows,
#   _gallery_finish
#
# Example:
#   init -2 python:
#       gallery_tab("ch01_d2", "Day 2", "ch01", 2, accent="#70566f")
#       gallery_row("d2_morning", "ch01_d2", "Sleeping beauty", "Day Two, 11:00.",
#           [("ch01_d2_leia_sleeping", "Asleep"), ("ch01_d2_leia_waking", "Waking up")])
#
# Notes: To add an entry: add one gallery_row(...) to the Day's *_gallery.rpy (a new Day also
#   calls gallery_tab once), list text-placeholder CGs in GALLERY_PLACEHOLDER_IMAGES there (remove
#   them when final art lands), then run lint and the unit tests. A page is "image" or ("image",
#   "Page label"); mature=True masks the grid cover, dream=True marks a dream.
#
# Depends on: nothing at init (systems/gallery.rpy reads it)
# Hooks: none
# Load order: init -3 helpers; the Day packs register at init -2; init -1 orders tabs and rows by
#   Day, before systems/gallery.rpy builds the registry at init 0
# Docs: docs/DAY_PACK.md   Tests: tests/test_gallery_flags.py, tests/test_title_screen.py,
#   tests/test_hidden_pov.py

init -3 python:

    # (tab id, tab label, chapter, day). Chapter groups the counts; day is the sub-tab.
    GALLERY_TABS = ()
    GALLERY_TAB_ACCENTS = {}
    _gallery_tab_rows = []

    # Images that are still Composite text placeholders (final art pending).
    GALLERY_PLACEHOLDER_IMAGES = set([
        # Day 2
        "ch01_d2_photo_leia_maya",
        "ch01_d2_boutique_reveal_ryan", "ch01_d2_boutique_reveal_julian",
        "ch01_d2_pool_top_accident",
        "d2_cafe_stranger",
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

    def gallery_tab(tab_id, label, chapter, day, accent):
        _gallery_tab_rows.append((tab_id, label, chapter, day, accent))

    def gallery_row(entry_id, tab, title, description, pages, mature=False, dream=False, route="All routes"):
        GALLERY_TABLE.append(dict(
            id=entry_id, tab=tab, title=title, description=description,
            pages=pages, mature=mature, dream=dream, route=route,
        ))

    # Days whose Gallery rows have not moved into their Day pack yet.
    gallery_tab("ch01_d2", "Day 2", "ch01", 2, accent="#70566f")
    gallery_tab("ch01_d3", "Day 3", "ch01", 3, accent="#7c6258")
    gallery_tab("ch01_d4", "Day 4", "ch01", 4, accent="#556b78")
    gallery_tab("ch01_d5", "Day 5", "ch01", 5, accent="#5f7a6a")


    # --------------------------------------------------------------------- Day 2
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
        "A photo of Leia and Maya.",
        ["ch01_d2_photo_leia_maya"])
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

# load order: init -1: every Day pack has registered (init -2); systems/gallery.rpy builds at init 0.
init -1 python:

    def _gallery_finish():
        """Tabs in Day order (accents in the same order); each Day's rows after the previous
        Day's, in the order the Day registered them."""
        global GALLERY_TABS
        rows = sorted(_gallery_tab_rows, key=lambda row: row[3])
        GALLERY_TABS = tuple(row[:4] for row in rows)
        GALLERY_TAB_ACCENTS.clear()
        for row in rows:
            GALLERY_TAB_ACCENTS[row[0]] = row[4]
        position = dict((row[0], i) for i, row in enumerate(rows))
        GALLERY_TABLE.sort(key=lambda entry: position.get(entry["tab"], len(rows)))

    _gallery_finish()
