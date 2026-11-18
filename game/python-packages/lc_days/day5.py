"""Day Five: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day5/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day5"]).
CHAPTER = {
    "number": 5, "number_word": "Five", "day": 5, "day_word": "Five",
    "review_day": "ch01_d5",
    "title": 'The Water',
    "routes": {
        "love": "Nobody's Cove",
        "love_exhib": 'Still Me',
        "nts": 'Her Biggest Fan',
        "ntr": 'Reasonable Doubt',
        "repair": 'The Second Try',
    },
}

# "Likes watching" key: an exhibition ending shows the NTS title when it is set (lc_chapters).
NTS_VARIANT_KEY = "ch01_d5_exhib_variant"


# ---------------------------------------------------------------- stat model (lc_stat_model)
# Route / her-own-call thresholds (lc_stat_model.THRESHOLDS).
STAT_THRESHOLDS = {
    "d5_bolder_swim": 41,              # was 24
    "d5_comfortable": 63,              # was 34
    "d5_comfortable_after_brief": 54,  # was 30
}

# Gate choices (lc_stat_model.CHOICE_GATES): gates may move up to 5; hard gates may move three stats.
STAT_CHOICE_GATES = {
    "ch01_d5_ntr_snorkel_stay": "soft",
    "ch01_d5_ntr_bunk_apart": "soft",
    "ch01_d5_ntr_u_ask_gently": "soft",
    "ch01_d5_ntr_c_go_to_her": "soft",
    "ch01_d5_ntr_gate_fine_hard": "hard",
    "ch01_d5_ntr_u_fine_hard": "hard",
    "ch01_d5_ntr_u_press_hard": "hard",
    "ch01_d5_ntr_c_accuse_hard": "hard",
    "ch01_d5_ntr_c_fine_hard": "hard",
}

# Route value the branch writes (lc_stat_model.CHOICE_ROUTE_FLAGS): "locks", "stays_open",
# "may_lead" or "lean".
STAT_ROUTE_FLAGS = {
    "ch01_d5_ntr_snorkel_stay": "may_lead",
    "ch01_d5_ntr_bunk_apart": "may_lead",
    "ch01_d5_ntr_gate_fine_hard": "stays_open",
    "ch01_d5_ntr_c_go_to_her": "stays_open",
    "ch01_d5_ntr_u_fine_hard": "locks",
    "ch01_d5_ntr_u_press_hard": "locks",
    "ch01_d5_ntr_c_accuse_hard": "locks",
    "ch01_d5_ntr_c_fine_hard": "locks",
}

# Repair beats (lc_stat_model.REPAIR_CHOICES): the only choices allowed to pair Temptation down
# with Love/Trust up.
STAT_REPAIR_CHOICES = frozenset((
    "ch01_d5_invite_read_aloud",
    "ch01_d5_ntr_c_go_to_her",
    "ch01_d5_ntr_pack_help",
    "ch01_d5_ntr_react_boundary",
    "ch01_d5_ntr_u_ask_gently",
))


# ---------------------------------------------------------------- UI (lc_ui_logic)
# Night images whose names carry no night token (lc_ui_logic.NIGHT_EXCEPTIONS).
UI_NIGHT_EXCEPTIONS = (
    # Day 5: sunset deck
    "ch01_d5_ntr_deck_alone",
)

# Journal day number and its started / complete flags (lc_ui_logic.DAY_FLAGS).
UI_DAY_FLAG = (5, "ch01_day_05_started", "ch01_day_05_complete")
