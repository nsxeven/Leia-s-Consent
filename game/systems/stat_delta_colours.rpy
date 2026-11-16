# Stat-change colours - colour stat changes by meaning, not sign
#
# Purpose: Wherever stat changes are shown (Insight/Full choice cards, review chips): LC_DELTA_UP
#   soft green = good for the couple (Love/Trust up, Temptation down), LC_DELTA_DOWN soft red =
#   toward NTR; Exhibitionism and Sharing keep their own route colour either way. The meaning comes
#   from lc_stat_model.delta_kind().
#
# Public API (call these from scenes/screens):
#   lc_delta_colour(stat, amount, palette="card")
#       colour for one change ('card' or 'review' palette), or None
#   lc_delta_colour_for_label(name, amount)   same, from a stat's display label
#   lc_choice_effect_markup(chips)            coloured markup for parsed caption chips
#   lc_choice_caption(caption)                menu caption with its [variable] substituted
#   define LC_DELTA_UP                        good change
#   define LC_DELTA_DOWN                      warning change
#   define LC_DELTA_EXHIBITIONISM             Exhibitionism colour
#   define LC_DELTA_SHARING                   Sharing colour
#   define LC_REVIEW_DELTA_INK                darker inks for paper (review, path stamps)
#
# Example:
#   $ line, chips = lc_ui_logic.parse_choice_caption(lc_choice_caption(item.caption))   (screen choice)
#
# Depends on: python-packages/lc_stat_model.py, python-packages/lc_ui_logic.py
# Hooks: none
# Load order: default (init 0)
# Docs: docs/STAT_MODEL.md   Tests: tests/test_stat_delta_colours.py

define LC_DELTA_UP = "#5aa874"
define LC_DELTA_DOWN = "#d4636e"
define LC_DELTA_EXHIBITIONISM = "#c2568c"
define LC_DELTA_SHARING = "#8a62b8"
# Review page (pixel font on paper) uses darker inks of the same meanings.
define LC_REVIEW_DELTA_INK = {"good": "#5f8a32", "bad": "#a8453f", "exhibitionism": "#a83a6e", "sharing": "#6e4a9a"}

init python:

    def lc_choice_caption(caption):
        """The menu caption with its [variable] filled in.

        Story menus pass the caption unsubstituted (e.g. "[ch01_x_text]"), so the
        stat line inside it only exists after substitution. Captions that are
        already plain text (and contain literal "[Love +1]" brackets) fail to
        substitute and are returned unchanged.
        """
        if not caption or "[" not in caption:
            return caption
        try:
            return renpy.substitute(caption, translate=False)
        except Exception:
            return caption

    def lc_delta_colour(stat, amount, palette="card"):
        """Colour for one stat change, by meaning (see the table above)."""
        import lc_stat_model
        kind = lc_stat_model.delta_kind(stat, amount)
        if kind is None:
            return None
        if palette == "review":
            return LC_REVIEW_DELTA_INK[kind]
        return {"good": LC_DELTA_UP, "bad": LC_DELTA_DOWN,
                "exhibitionism": LC_DELTA_EXHIBITIONISM, "sharing": LC_DELTA_SHARING}[kind]

    def lc_delta_colour_for_label(name, amount):
        import lc_stat_model
        return lc_delta_colour(lc_stat_model.stat_id_for_label(name), amount)

    def lc_choice_effect_markup(chips):
        return lc_ui_logic.effect_markup(chips, LC_DELTA_UP, LC_DELTA_DOWN, colour_for=lc_delta_colour_for_label)
