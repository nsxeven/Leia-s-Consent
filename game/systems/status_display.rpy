# Player-facing status presentation helpers.
# These helpers decide what information is visible at each transparency level.

init python:

    STATUS_MODE_NOTES = {
        "normal": "A readable snapshot of what Ryan can reasonably perceive.",
        "insight": "Adds broad behavioral signals without revealing exact values.",
        "full": "Shows exact values and the route the story currently leans toward.",
        "developer": "Shows exact values together with internal stat keys.",
    }


    def status_band(value):
        value = clamp_stat(value)
        if value < 20:
            return "Very Low"
        if value < 40:
            return "Low"
        if value < 60:
            return "Moderate"
        if value < 80:
            return "High"
        return "Very High"


    def status_mode_note():
        # Notes are written with the default names; show the player's typed names.
        return gallery_customize_names(STATUS_MODE_NOTES.get(current_choice_mode(), STATUS_MODE_NOTES["normal"]))


    def _status_value(group_name, stat_name):
        return get_stat_group(group_name)[stat_name]


    def _status_row(group_name, stat_name, label, mode):
        value = _status_value(group_name, stat_name)
        detail = ""
        internal_key = ""

        if mode == "insight":
            detail = status_band(value)
        elif mode in ("full", "developer"):
            detail = "{} / 100".format(value)

        if mode == "developer":
            internal_key = "{}.{}".format(group_name, stat_name)

        return {
            "label": label,
            "value": value,
            "detail": detail,
            "internal_key": internal_key,
            "stat": stat_name,
            # Hover/focus explanation (systems/stat_tooltips.rpy), names filled in.
            "tooltip": lc_stat_tooltip(stat_name, mode),
        }


    def status_relationship_rows(mode=None):
        """Love and Trust: the two Love-family stats (every mode, one name each)."""
        mode = mode or current_choice_mode()
        return [
            _status_row("relationship", "love", STAT_LABELS["love"], mode),
            _status_row("relationship", "trust", STAT_LABELS["trust"], mode),
        ]


    def status_leia_rows(mode=None):
        """Exhibitionism (Love+Exhib / NTS) and Temptation (NTR), in every mode."""
        mode = mode or current_choice_mode()
        return [
            _status_row("partner", "exhibitionism", STAT_LABELS["exhibitionism"], mode),
            _status_row("relationship", "temptation", STAT_LABELS["temptation"], mode),
        ]


    def status_ryan_rows(mode=None):
        """Sharing: what the two of you have agreed to open up to (NTS). Ryan's
        column, because every step needs his yes as well as hers."""
        mode = mode or current_choice_mode()
        return [
            _status_row("relationship", "sharing", STAT_LABELS["sharing"], mode),
        ]


    # Stat that drives each lean; its bar fills the "Current lean" row.
    # Status colours by stat meaning (darryn 2026-11-09): glass bar art
    # gui/glass/stat_<stat>.png (tools/gen_glass_menu_ui.py), number tint, and
    # the softer phone bar tint. The stat icons use the same colours.
    LC_STAT_COLOUR = {
        "love": {"ink": "#FFAACD", "phone": "#EC689C"},
        "trust": {"ink": "#FFDE8C", "phone": "#DEA034"},
        "exhibitionism": {"ink": "#FFC4A0", "phone": "#E8766E"},
        "temptation": {"ink": "#EC6E82", "phone": "#C03458"},
        "sharing": {"ink": "#C8ACEC", "phone": "#926ECE"},
    }

    def lc_status_colour_stat(row):
        """Which stat's colour a Status row uses (the lean row: its route's)."""
        stat = row.get("bar_stat") or row.get("stat")
        return stat if stat in LC_STAT_COLOUR else "love"

    LC_LEAN_DRIVER = {
        "love": "love", "strained": "love", "undecided": "love",
        "love_exhib": "exhibitionism", "nts": "sharing", "ntr": "temptation",
    }


    def status_route_rows(mode=None):
        """Full / Developer only: one "Current lean" row, computed by the same
        resolvers the route checks use (lc_current_lean in systems/stats.rpy)."""
        mode = mode or current_choice_mode()
        if mode not in ("full", "developer"):
            return []

        lean = lc_current_lean()
        driver = LC_LEAN_DRIVER.get(lean, "love")
        value = lc_stat(driver)
        return [
            {
                "label": "Current lean: {}".format(lc_stat_model.LEAN_LABELS.get(lean, "Undecided")),
                "value": value,
                "detail": "{} {} / 100".format(STAT_LABELS[driver], value),
                "internal_key": "lc_current_lean() = {}".format(lean) if mode == "developer" else "",
                "stat": "lean",
                "bar_stat": driver,   # the lean bar wears its route's colour
                "tooltip": lc_stat_tooltip("lean", mode),
            },
        ]


    def leia_overview_text():
        """A short, intentionally non-spoilery behavioral summary of Leia."""
        relationship = renpy.store.relationship_stats
        name = renpy.store.girlfriend_name
        flat = lc_stats_flat()

        closeness = int(round((flat["love"] + flat["trust"]) / 2.0))
        exhibitionism = flat["exhibitionism"]
        temptation = flat["temptation"]

        if closeness >= 80:
            relationship_line = "{} seems deeply secure in the relationship and very comfortable leaning on you.".format(name)
        elif closeness >= 60:
            relationship_line = "{} seems close to you and generally secure in the relationship.".format(name)
        elif closeness >= 40:
            relationship_line = "{} seems settled with you, though there is still room for the relationship to deepen.".format(name)
        elif closeness >= 20:
            relationship_line = "{} seems somewhat guarded and may still be looking for more reassurance from the relationship.".format(name)
        else:
            relationship_line = "{} feels emotionally distant right now and is keeping much more of herself protected.".format(name)

        if exhibitionism >= 63:
            visibility_line = "She seems genuinely comfortable being noticed, as long as you're in on it."
        elif exhibitionism >= 36:
            visibility_line = "She is becoming more comfortable with being noticed, although it still depends heavily on the situation."
        elif exhibitionism >= 19:
            visibility_line = "She can enjoy a little attention, but she is not yet naturally drawn to being the center of it."
        else:
            visibility_line = "She remains quite private about how she presents herself and rarely seeks extra attention."

        if temptation >= 30:
            drift_line = "Lately her attention drifts somewhere you can't follow, and she keeps more of it to herself."
        elif temptation >= 18:
            drift_line = "Every so often she seems a little restless, as if part of her is somewhere else."
        else:
            drift_line = "She seems present and settled when she's with you."

        return "{} {} {}".format(
            relationship_line,
            visibility_line,
            drift_line,
        )
