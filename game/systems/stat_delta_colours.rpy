# Stat-change colours by MEANING, not sign (darryn 2026-11-08, stat model v2).
# Wherever stat changes are shown (Insight / Full choice cards, end-of-day
# review chips and numbers):
#   LC_DELTA_UP   (soft green) = good for the couple: Love/Trust up, Temptation down
#   LC_DELTA_DOWN (soft red)   = warning: Love/Trust down, Temptation up (toward NTR)
#   Exhibitionism and Sharing are directions, not good or bad: they keep their own
#   route colour either way (pink = Love+Exhib, purple = NTS).
# The meaning comes from lc_stat_model.delta_kind(). Slightly deeper than true
# pastel so the text stays readable on the cream cards.

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
