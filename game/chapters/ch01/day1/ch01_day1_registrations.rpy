# Day One pack - registrations: choice effects and tags, Full Transparency camera counts, the
#   review's choice styles and moment stickers, the Day One route helpers and the story-key
#   ledger.
#
# Where every kind of content goes: docs/DAY_PACK.md. Scoring rules: docs/STAT_MODEL.md.
# Load order: init 1 (the engine tables exist at init <= 0).

init 1 python:
    import lc_stat_model

    # Stat effects per choice id: [(group, stat, amount), ...] (systems/choice_engine.rpy).
    CHOICE_EFFECTS.update({
        "ch01_outfit_bolder": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_outfit_comfort": [
            ("relationship", "trust", 1),
        ],
        "ch01_outfit_conservative": [
            ("relationship", "love", 1),
        ],
        "ch01_outfit_rush": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_photo_support": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_photo_more": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_photo_exit": [
            ("relationship", "trust", 2),
        ],
        "ch01_photo_rush": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_towel_laugh": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_towel_boundary": [
            ("relationship", "trust", 1),
        ],
        "ch01_towel_forget": [
            ("relationship", "trust", 1),
        ],
        "ch01_towel_reassure": [
            ("relationship", "trust", 1),
        ],
        "ch01_towel_honest": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_towel_tease": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_towel_shrug": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_bra_reassure": [
            ("relationship", "trust", 2),
        ],
        "ch01_bra_playful": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_bra_cover": [
            ("relationship", "trust", 1),
        ],
        "ch01_bra_distracted": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_stranger_proud": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_stranger_territorial": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_stranger_encourage": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_catch_ignore": [],  # Neutral: no stats
        "ch01_catch_check": [
            ("relationship", "trust", 1),
        ],
        "ch01_catch_joke": [
            ("partner", "exhibitionism", 1),
        ],
        "ch01_catch_boundary": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_friend_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_friend_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_friend_boundary": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_julian_reassure": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_julian_honest": [
            ("relationship", "trust", 1),
        ],
        "ch01_julian_joke": [],  # Neutral: no stats
        "ch01_julian_fine": [
            ("relationship", "temptation", 1),
        ],
        "ch01_carry_brush": [],  # Neutral: no stats
        "ch01_carry_lookaway": [
            ("relationship", "temptation", 1),
        ],
        "ch01_carry_fix": [
            ("relationship", "trust", 1),
        ],
        "ch01_carry_joke": [
            ("partner", "exhibitionism", 1),
        ],
        # Upstairs talk before movie night (scene 14a): say it, enjoy it, or a slip.
        "ch01_upstairs_honest": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_upstairs_liked": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_upstairs_swallow": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_upstairs_snap": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],

        # Movie-night / Day 1 continuation. Open choices raise Exhibitionism
        # (often with Love); dismissive choices raise Temptation and cost Love
        # or Trust, the pressure that can later feed the NTR route.
        "ch01_movie_stop": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_movie_subtle": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_movie_tease_presence": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_movie_dismiss_concern": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_can_tell_behave": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_can_tell_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_can_tell_push": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_can_tell_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_fidget_cover": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_fidget_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_fidget_push": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_fidget_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_private_apologize": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_private_playful": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_private_curiosity": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_private_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_noblanket_behave": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_noblanket_test": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_noblanket_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_noblanket_phone": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_watch_claim": [
            ("relationship", "love", 2),
        ],
        "ch01_watch_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_watch_check": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_watch_ignore": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_micro_warn": [
            ("relationship", "trust", 1),
        ],
        "ch01_micro_silent": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_micro_open": [
            ("partner", "exhibitionism", 3),
        ],
        "ch01_micro_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_philosophy_couple": [
            ("relationship", "trust", 1),
        ],
        "ch01_philosophy_trust": [
            ("relationship", "trust", 2),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_philosophy_jealousy_fun": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_philosophy_dont_care": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_looking_enjoy": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_looking_harmless": [
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_looking_boundary": [
            ("relationship", "trust", 1),
        ],
        "ch01_looking_dont_care": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 2),
        ],
        "ch01_julian_change_subject": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_julian_let_play": [],  # Neutral: no stats
        "ch01_julian_put_spot": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_julian_dont_care": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_compliment_affirm": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_compliment_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_compliment_enjoy": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_compliment_shrug": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_alone_apologize": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_alone_curiosity": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_alone_open": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_alone_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_private_claim": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_private_open": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_private_jealous": [
            ("relationship", "love", 1),
        ],
        "ch01_private_indifferent": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
    })

    # Behaviour tags per choice id (systems/choice_engine.rpy).
    CHOICE_TAGS.update({
        "ch01_outfit_bolder": ("encouraging", "open", "supportive"),
        "ch01_outfit_comfort": ("neutral", "comfort-first", "supportive"),
        "ch01_outfit_conservative": ("protective", "cautious", "respectful"),
        "ch01_outfit_rush": ("neutral", "nonchalant", "distracted"),
        "ch01_photo_support": ("encouraging", "supportive"),
        "ch01_photo_more": ("encouraging", "participating", "open"),
        "ch01_photo_exit": ("protective", "comfort-first", "supportive"),
        "ch01_photo_rush": ("neutral", "nonchalant", "dismissive"),
        "ch01_towel_laugh": ("encouraging", "lighthearted"),
        "ch01_towel_boundary": ("protective", "respectful"),
        "ch01_towel_forget": ("protective", "honest", "cautious"),
        "ch01_towel_reassure": ("neutral", "supportive", "reassuring"),
        "ch01_towel_honest": ("neutral", "honest", "supportive"),
        "ch01_towel_tease": ("encouraging", "lighthearted", "open"),
        "ch01_towel_shrug": ("neutral", "nonchalant", "dismissive"),
        "ch01_bra_reassure": ("neutral", "supportive", "comfort-first"),
        "ch01_bra_playful": ("encouraging", "participating", "open", "playful"),
        "ch01_bra_cover": ("protective", "cautious", "respectful"),
        "ch01_bra_distracted": ("neutral", "nonchalant", "distracted"),
        "ch01_stranger_proud": ("encouraging", "supportive", "open", "attentive"),
        "ch01_stranger_territorial": ("protective", "possessive", "cautious", "attentive"),
        "ch01_stranger_encourage": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_catch_ignore": ("neutral", "trusting"),
        "ch01_catch_check": ("neutral", "supportive", "protective", "attentive"),
        "ch01_catch_joke": ("encouraging", "lighthearted", "open"),
        "ch01_catch_boundary": ("protective", "cautious", "respectful"),
        "ch01_friend_reassure": ("neutral", "honest", "supportive", "attentive"),
        "ch01_friend_tease": ("encouraging", "lighthearted", "playful"),
        "ch01_friend_boundary": ("neutral", "honest", "boundary-setting"),
        "ch01_julian_reassure": ("encouraging", "trusting", "open"),
        "ch01_julian_honest": ("protective", "honest", "respectful"),
        "ch01_julian_joke": ("encouraging", "lighthearted", "trusting"),
        "ch01_julian_fine": ("neutral", "nonchalant", "withdrawal"),
        "ch01_carry_brush": ("encouraging", "trusting", "open"),
        "ch01_carry_lookaway": ("protective", "possessive", "cautious"),
        "ch01_carry_fix": ("neutral", "protective", "supportive"),
        "ch01_carry_joke": ("encouraging", "lighthearted", "open", "playful"),
        "ch01_upstairs_honest": ("neutral", "honest", "attentive", "supportive"),
        "ch01_upstairs_liked": ("encouraging", "open", "honest", "attentive"),
        "ch01_upstairs_swallow": ("neutral", "nonchalant", "withdrawal"),
        "ch01_upstairs_snap": ("neutral", "defensive"),

        "ch01_movie_stop": ("protective", "attentive", "supportive", "consent-first"),
        "ch01_movie_subtle": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_movie_tease_presence": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_movie_dismiss_concern": ("neutral", "nonchalant", "dismissive"),
        "ch01_can_tell_behave": ("protective", "attentive", "supportive"),
        "ch01_can_tell_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_can_tell_push": ("encouraging", "participating", "open", "risk-testing"),
        "ch01_can_tell_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_fidget_cover": ("neutral", "supportive", "attentive"),
        "ch01_fidget_tease": ("encouraging", "playful", "open"),
        "ch01_fidget_push": ("encouraging", "open", "risk-testing"),
        "ch01_fidget_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_private_apologize": ("neutral", "supportive", "attentive", "consent-first"),
        "ch01_private_playful": ("encouraging", "open", "playful", "attentive"),
        "ch01_private_curiosity": ("encouraging", "participating", "open", "honest", "attentive"),
        "ch01_private_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_noblanket_behave": ("neutral", "attentive", "supportive"),
        "ch01_noblanket_test": ("encouraging", "open", "risk-testing"),
        "ch01_noblanket_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_noblanket_phone": ("neutral", "nonchalant", "distracted"),
        "ch01_watch_claim": ("protective", "possessive", "attentive", "playful"),
        "ch01_watch_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_watch_check": ("neutral", "supportive", "attentive"),
        "ch01_watch_ignore": ("neutral", "nonchalant", "distracted"),
        "ch01_micro_warn": ("protective", "attentive", "respectful"),
        "ch01_micro_silent": ("neutral", "trusting", "observant"),
        "ch01_micro_open": ("encouraging", "participating", "open", "risk-testing"),
        "ch01_micro_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_philosophy_couple": ("protective", "possessive", "boundary-setting"),
        "ch01_philosophy_trust": ("neutral", "honest", "trusting", "open"),
        "ch01_philosophy_jealousy_fun": ("encouraging", "open", "playful", "possessive"),
        "ch01_philosophy_dont_care": ("neutral", "nonchalant", "dismissive"),
        "ch01_looking_enjoy": ("encouraging", "open", "playful", "attentive"),
        "ch01_looking_harmless": ("neutral", "trusting", "open"),
        "ch01_looking_boundary": ("protective", "boundary-setting", "attentive"),
        "ch01_looking_dont_care": ("neutral", "nonchalant", "dismissive"),
        "ch01_julian_change_subject": ("protective", "attentive", "boundary-setting"),
        "ch01_julian_let_play": ("neutral", "trusting", "open"),
        "ch01_julian_put_spot": ("encouraging", "open", "playful", "participating"),
        "ch01_julian_dont_care": ("neutral", "nonchalant", "dismissive"),
        "ch01_compliment_affirm": ("neutral", "supportive", "attentive", "possessive"),
        "ch01_compliment_tease": ("encouraging", "playful", "possessive", "attentive"),
        "ch01_compliment_enjoy": ("encouraging", "participating", "open", "attentive"),
        "ch01_compliment_shrug": ("neutral", "nonchalant", "dismissive", "distracted"),
        "ch01_alone_apologize": ("neutral", "supportive", "attentive", "consent-first"),
        "ch01_alone_curiosity": ("neutral", "honest", "attentive", "open"),
        "ch01_alone_open": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_alone_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_private_claim": ("protective", "possessive", "attentive", "supportive"),
        "ch01_private_open": ("encouraging", "open", "honest", "attentive"),
        "ch01_private_jealous": ("protective", "possessive", "honest"),
        "ch01_private_indifferent": ("neutral", "nonchalant", "dismissive"),
    })

    # CGs a choice shows (Full Transparency camera stamp, systems/choice_path_tags.rpy):
    # (min, max) = total CGs of that sequence the player sees by picking this option.
    LC_CHOICE_CG_COUNT.update({
        # Day 1 pool photos (ch01_scenes_04_06.rpy): capture 01 is already shown.
        "ch01_photo_support": (2, 2),   # + capture 02
        "ch01_photo_more": (3, 3),      # + captures 02 and 03
        "ch01_photo_exit": (1, 2),      # capture 02 only if her Exhibitionism carries her on
        "ch01_photo_rush": (1, 1),      # rushed: she stops after capture 01 (choice-sense pass)
    })

    # Review choice styles: how Ryan played the day sets both review tags (systems/day_review.rpy).
    LC_CHOICE_STYLE.update({
        # Day 1
        "ch01_outfit_conservative": "protective", "ch01_outfit_comfort": "supportive", "ch01_outfit_bolder": "showoff",
        "ch01_photo_exit": "protective", "ch01_photo_support": "supportive", "ch01_photo_more": "showoff",
        "ch01_towel_boundary": "protective", "ch01_towel_laugh": "playful", "ch01_towel_forget": "detached",
        "ch01_towel_reassure": "supportive", "ch01_towel_honest": "honest", "ch01_towel_tease": "playful",
        "ch01_bra_cover": "protective", "ch01_bra_reassure": "supportive", "ch01_bra_playful": "playful",
        "ch01_stranger_territorial": "protective", "ch01_stranger_proud": "showoff", "ch01_stranger_encourage": "showoff",
        "ch01_catch_boundary": "protective", "ch01_catch_check": "supportive", "ch01_catch_ignore": "detached",
        "ch01_catch_joke": "playful",
        "ch01_friend_reassure": "supportive", "ch01_friend_tease": "playful", "ch01_friend_boundary": "honest",
        "ch01_julian_reassure": "supportive", "ch01_julian_honest": "honest", "ch01_julian_joke": "playful",
        "ch01_carry_lookaway": "protective", "ch01_carry_fix": "protective", "ch01_carry_brush": "supportive",
        "ch01_carry_joke": "playful",
        "ch01_upstairs_honest": "honest", "ch01_upstairs_liked": "showoff", "ch01_upstairs_swallow": "detached",
        "ch01_upstairs_snap": "detached",
        "ch01_movie_stop": "protective", "ch01_movie_subtle": "showoff", "ch01_movie_tease_presence": "playful",
        "ch01_movie_dismiss_concern": "detached",
        "ch01_can_tell_behave": "protective", "ch01_can_tell_tease": "playful", "ch01_can_tell_push": "showoff",
        "ch01_can_tell_dismiss": "detached",
        "ch01_private_apologize": "supportive", "ch01_private_playful": "playful", "ch01_private_curiosity": "honest",
        "ch01_private_dismiss": "detached",
        "ch01_noblanket_behave": "protective", "ch01_noblanket_test": "showoff", "ch01_noblanket_tease": "playful",
        "ch01_noblanket_phone": "detached",
        "ch01_watch_claim": "protective", "ch01_watch_tease": "playful", "ch01_watch_check": "supportive",
        "ch01_watch_ignore": "detached",
        "ch01_micro_warn": "protective", "ch01_micro_silent": "showoff", "ch01_micro_open": "showoff",
        "ch01_micro_dismiss": "detached",
        "ch01_philosophy_couple": "protective", "ch01_philosophy_trust": "honest",
        "ch01_philosophy_jealousy_fun": "showoff", "ch01_philosophy_dont_care": "detached",
        "ch01_julian_change_subject": "protective", "ch01_julian_let_play": "showoff", "ch01_julian_put_spot": "playful",
        "ch01_julian_dont_care": "detached",
        "ch01_compliment_affirm": "supportive", "ch01_compliment_tease": "protective", "ch01_compliment_enjoy": "showoff",
        "ch01_compliment_shrug": "detached",
        "ch01_alone_curiosity": "honest", "ch01_alone_open": "showoff", "ch01_alone_dismiss": "detached",
        "ch01_alone_apologize": "supportive",
        "ch01_private_claim": "protective", "ch01_private_open": "showoff", "ch01_private_jealous": "honest",
        "ch01_private_indifferent": "detached",
        "ch01_dream_curiosity": "honest", "ch01_dream_withdraw": "detached", "ch01_dream_ground": "supportive",
        # Choice-sense pass slips (honest mistakes).
        "ch01_outfit_rush": "detached", "ch01_photo_rush": "detached", "ch01_towel_shrug": "detached",
        "ch01_bra_distracted": "detached", "ch01_julian_fine": "detached",
    })

    # Moment stickers: up to two per day, in this priority order (systems/day_review.rpy).
    # "Asked First": the scene-20 flag set when Ryan promised to ask and did.
    LC_MOMENT_STICKERS = LC_MOMENT_STICKERS + (
        ("Asked First", lambda day_id, ids: day_id == "ch01_d1" and bool(getattr(store, "ch01_grab_promised_to_ask", False))),
        ("Told the Truth", lambda day_id, ids: "ch01_towel_honest" in ids),
        ("Wardrobe Rescue", lambda day_id, ids: "ch01_carry_fix" in ids),
        ("Eyes on Me", lambda day_id, ids: "ch01_watch_claim" in ids),
        ("Let Her Decide", lambda day_id, ids: "ch01_micro_silent" in ids),
        ("Proud of Her", lambda day_id, ids: "ch01_stranger_proud" in ids),
        ("Kept His Cool", lambda day_id, ids: "ch01_julian_reassure" in ids),
        ("Missed It", lambda day_id, ids: sum(1 for c in ("ch01_noblanket_phone", "ch01_watch_ignore", "ch01_compliment_shrug") if c in ids) >= 2),
    )

    # ---- Day One route helpers (rules: lc_days/day1.py, published on lc_stat_model)
    def lc_d1_route_pressure():
        """Day 1 end state ('ntr_seeded' / 'nts_seeded' / 'mixed'). Story and Full readout share it."""
        return lc_stat_model.d1_route_pressure(lc_stats_flat(), lc_route_explorer_for_lane())

    def lc_d1_love_bedtime(pressure):
        return lc_stat_model.d1_love_bedtime(pressure, lc_stats_flat())

# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
