# Stat-change colours (darryn 2026-11-06): wherever choice stats are shown
# (Insight / Full visibility), gains are a soft green and losses a soft red.
# Used by the choice cards (screens/zzzzzzzz_scrapbook_ui.rpy, screen choice).

define LC_DELTA_UP = "#5aa874"
define LC_DELTA_DOWN = "#d4636e"

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

    def lc_choice_effect_markup(chips):
        return lc_ui_logic.effect_markup(chips, LC_DELTA_UP, LC_DELTA_DOWN)
