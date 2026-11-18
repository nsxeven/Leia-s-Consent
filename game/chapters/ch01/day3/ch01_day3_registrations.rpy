# Day Three pack - registrations: choice effects (the effective, stat-model-v2 scoring) and
#   tags, and the story-key ledger.
#
# Where every kind of content goes: docs/DAY_PACK.md. Scoring rules: docs/STAT_MODEL.md.
# Load order: init 1 (the engine tables exist at init <= 0).

init 1 python:
    # Day Three's two menus. Ordinary scale (+/-1..2), same as Day Two's
    # mid-day choices and Day Four's non-gate choices. Not a route lock:
    # the lane is already set, and Day Four still reads that lane.
    CHOICE_EFFECTS.update({
        "ch01_d3_ntr_enjoy": [
            ("relationship", "love", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d3_ntr_talk": [
            ("relationship", "love", 2),
            ("relationship", "temptation", -3),
        ],
        "ch01_d3_ntr_withdraw": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 2),
        ],
        "ch01_d3_dessert_chocolate": [
            ("relationship", "trust", 1),
        ],
        "ch01_d3_dessert_recommended": [],  # Neutral: no stats
        "ch01_d3_dessert_surprise": [
            ("relationship", "love", 1),
        ],
    })

    CHOICE_TAGS.update({
        "ch01_d3_ntr_enjoy": ("supportive", "attentive", "repair"),
        "ch01_d3_ntr_talk": ("supportive", "attentive", "honest", "repair"),
        "ch01_d3_ntr_withdraw": ("neutral", "nonchalant", "dismissive", "withdrawal"),
        "ch01_d3_dessert_chocolate": ("supportive", "attentive"),
        "ch01_d3_dessert_recommended": ("neutral", "trusting"),
        "ch01_d3_dessert_surprise": ("encouraging", "playful", "lighthearted"),
    })

# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
