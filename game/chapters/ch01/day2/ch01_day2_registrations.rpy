# Day Two pack - registrations: the mall-scene choice rows that used to sit in
#   systems/choice_engine.rpy, and the story-key ledger. Most Day Two choice rows are registered
#   next to their scenes (ch01_day2_scenes_01_15.rpy and the other Day Two files, init 1).
#
# Where every kind of content goes: docs/DAY_PACK.md. Scoring rules: docs/STAT_MODEL.md.
# Load order: init 1 (the engine tables exist at init <= 0).

init 1 python:

    CHOICE_EFFECTS.update({
        "ch01_d2_mall_go_to_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_leave_to_maya": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_mall_reveal_affection": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_reveal_open": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d2_mall_reveal_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_mall_reveal_flat": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
    })

    CHOICE_TAGS.update({
        "ch01_d2_mall_go_to_leia": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_leave_to_maya": ("neutral", "nonchalant", "dismissive", "withdrawal", "ntr-seed"),
        "ch01_d2_mall_reveal_affection": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_reveal_open": ("encouraging", "participating", "open", "exhibitionism-seed"),
        "ch01_d2_mall_reveal_tease": ("encouraging", "playful", "attentive"),
        "ch01_d2_mall_reveal_flat": ("neutral", "nonchalant", "distracted"),
    })

# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
