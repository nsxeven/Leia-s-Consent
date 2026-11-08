# Hover / focus explanations for every stat row (Status screen, phone Status
# app, end-of-day review bars). Stat model v2 (darryn, 2026-11-08): five stats,
# one name each in every mode, and SHORT breakdowns.
#
# Owner decision (darryn): no numbers. Keep digits, thresholds and exact
# effects OUT of LC_STAT_TOOLTIPS (tests/test_stat_tooltips.py enforces this,
# and the word limits below).
#
# Wording per display mode (internal keys from CHOICE_MODES):
#   "normal"  = Immersive: how it feels, in-world. 12 words or fewer.
#   "insight" = Insight: what the stat means and what moves it. 20 or fewer.
#   "full"    = Full Transparency: meaning plus whether to keep it high or low
#               to lean toward or avoid Love / Love+Exhib / NTS / NTR. 30 or
#               fewer. Developer mode reuses this text.
#
# Names: write [girlfriend_name], [player_name], [friend_name], never the
# default names. lc_stat_tooltip() swaps them for the player's typed names.

init python:

    LC_STAT_TOOLTIP_MODES = ("normal", "insight", "full")

    # Modes without their own text borrow another mode's wording.
    LC_STAT_TOOLTIP_MODE_FALLBACK = {"developer": "full"}

    # stat id -> mode -> text. Stat ids match lc_stat_model.STAT_ORDER (the
    # _status_row(group, stat_id, ...) rows in status_display.rpy and
    # LC_REVIEW_STAT_ORDER in day_review.rpy) plus the Full "Current lean" row.
    LC_STAT_TOOLTIPS = {
        "love": {
            "normal": "How warm and close things feel between you two.",
            "insight": "How close and cared-for [girlfriend_name] feels with you. Attention raises it; brushing her off lowers it.",
            "full": "How close [girlfriend_name] feels to you. Keep it high for Love, Love+Exhib and NTS; let it fall and NTR opens up.",
        },
        "trust": {
            "normal": "Whether she feels safe telling you anything.",
            "insight": "How safe [girlfriend_name] feels being honest with you. Checking in raises it; accusing or dodging lowers it.",
            "full": "Honesty and consent between you. Keep it high to unlock agreed NTS steps and to repair NTR; low Trust feeds NTR.",
        },
        "exhibitionism": {
            "normal": "How she feels when eyes turn her way.",
            "insight": "How much you both enjoy [girlfriend_name] being seen. Playful public moments with you raise it.",
            "full": "Her comfort being seen, with you in on it. High leans Love+Exhib or NTS and sets how far she goes; keep it low for pure Love.",
        },
        "sharing": {
            "normal": "Whether there's room for someone else in your games.",
            "insight": "How open you both are to someone else joining in. Always agreed together first.",
            "full": "Agreed openness to someone else joining in, Maya first. Keep it high for NTS; keep it low to stay Love+Exhib. It never leads to NTR.",
        },
        "temptation": {
            "normal": "The small gaps that have opened between you.",
            "insight": "How far [girlfriend_name] drifts when you're absent, dismissive or controlling. Attention and honesty bring it down.",
            "full": "Drift, secrets and restlessness pulling her away from you. Keep it low to avoid NTR; high Temptation leads to NTR. Honest repair choices lower it.",
        },
        "lean": {
            "normal": "Where the story seems to be heading.",
            "insight": "Which way the story is leaning right now, from your choices so far.",
            "full": "The route the story would take right now, from the same check the game uses: Love, Love+Exhib, NTS or NTR.",
        },
    }

    # Word limits per mode (tests/test_stat_tooltips.py).
    LC_STAT_TOOLTIP_WORD_LIMITS = {"normal": 12, "insight": 20, "full": 30}

    # FUTURE NUMBERS GO HERE (keep LC_STAT_TOOLTIPS number-free).
    # Once darryn decides what the values mean, add exact thresholds / effects
    # per stat and mode, e.g.
    #     "temptation": {"full": "...", "developer": "..."},
    # lc_stat_tooltip() appends the sentence after the base text. Mostly for
    # "full" / "developer"; Immersive should stay number-free. Update
    # tests/test_stat_tooltips.py (it asserts this is empty) when you do.
    LC_STAT_TOOLTIP_NUMBERS = {}

    LC_STAT_TOOLTIP_NAME_TOKENS = (
        ("[girlfriend_name]", "girlfriend_name"),
        ("[player_name]", "player_name"),
        ("[friend_name]", "friend_name"),
    )


    def lc_stat_tooltip(stat_id, mode=None):
        """Player-facing explanation for one stat row, or None if unknown.

        The result already holds the player's typed names, so display it with
        `substitute False`.
        """
        mode = mode or current_choice_mode()
        entry = LC_STAT_TOOLTIPS.get(stat_id)
        if not entry:
            return None
        text_mode = LC_STAT_TOOLTIP_MODE_FALLBACK.get(mode, mode)
        text = entry.get(text_mode) or entry["normal"]
        numbers = LC_STAT_TOOLTIP_NUMBERS.get(stat_id, {})
        extra = numbers.get(mode) or numbers.get(text_mode)
        if extra:
            text = text + " " + extra
        # Typed default names (none today) follow the player's names first;
        # then the bracket tokens are filled in, so a renamed character can't
        # be rewritten a second time.
        text = gallery_customize_names(text)
        for token, field in LC_STAT_TOOLTIP_NAME_TOKENS:
            text = text.replace(token, str(getattr(store, field, "")))
        return text
