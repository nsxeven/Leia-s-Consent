"""Day Four: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/day4/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["day4"]).
CHAPTER = {
    "number": 4, "number_word": "Four", "day": 4, "day_word": "Four",
    "review_day": "ch01_d4",
    "title": 'Blue Hour',
    "routes": {
        "love": 'Badly, Slowly',
        "love_exhib": 'One Slow Heartbeat',
        "nts": 'Watching Her Decide',
        "ntr": 'The Hairclip',
        "repair": 'Back in Her Hair',
    },
}

# "Likes watching" key: an exhibition ending shows the NTS title when it is set (lc_chapters).
NTS_VARIANT_KEY = "ch01_d4_exhib_variant"


# ---------------------------------------------------------------- stat model (lc_stat_model)
# Route / her-own-call thresholds (lc_stat_model.THRESHOLDS).
STAT_THRESHOLDS = {
    "d4_brief_reveal": 45,             # was 26
}

# Gate choices (lc_stat_model.CHOICE_GATES): gates may move up to 5; hard gates may move three stats.
STAT_CHOICE_GATES = {
    "ch01_d4_ntr_text_fine_soft": "soft",
    "ch01_d4_ntr_fine_soft2": "soft",
    "ch01_d4_ntr_gate_reconnect": "soft",
    "ch01_d4_ntr_gate_accuse_hard": "hard",
    "ch01_d4_ntr_gate_withdraw_hard": "hard",
}

# Route value the branch writes (lc_stat_model.CHOICE_ROUTE_FLAGS): "locks", "stays_open",
# "may_lead" or "lean".
STAT_ROUTE_FLAGS = {
    "ch01_d4_ntr_text_fine_soft": "may_lead",
    "ch01_d4_ntr_fine_soft2": "may_lead",
    "ch01_d4_ntr_gate_accuse_hard": "stays_open",
    "ch01_d4_ntr_gate_withdraw_hard": "locks",
}

# Repair beats (lc_stat_model.REPAIR_CHOICES): the only choices allowed to pair Temptation down
# with Love/Trust up.
STAT_REPAIR_CHOICES = frozenset((
    "ch01_d4_ntr_ask_gently",
    "ch01_d4_ntr_compliment",
    "ch01_d4_ntr_gate_reconnect",
    "ch01_d4_ntr_react_boundary",
    "ch01_d4_ntr_text_join",
))


# ---------------------------------------------------------------- UI (lc_ui_logic)
# Night images whose names carry no night token (lc_ui_logic.NIGHT_EXCEPTIONS).
UI_NIGHT_EXCEPTIONS = (
    # Day 4: terrace at night
    "ch01_d4_exhib_watching",
    "ch01_d4_exhib_terrace_01",
    "ch01_d4_exhib_terrace_02",
    "ch01_d4_ntr_terrace_talk",
)

# Journal day number and its started / complete flags (lc_ui_logic.DAY_FLAGS).
UI_DAY_FLAG = (4, "ch01_day_04_started", "ch01_day_04_complete")
