# Player-facing status presentation helpers.
# These helpers decide what information is visible at each transparency level.

init python:

    STATUS_MODE_NOTES = {
        "normal": "A readable snapshot of what Ryan can reasonably perceive.",
        "insight": "Adds broad behavioural signals without revealing exact values.",
        "full": "Shows the complete numerical state for route planning.",
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
        return STATUS_MODE_NOTES.get(current_choice_mode(), STATUS_MODE_NOTES["normal"])


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
        }


    def status_relationship_rows(mode=None):
        mode = mode or current_choice_mode()
        rows = [
            _status_row("relationship", "love", "Affection", mode),
            _status_row("relationship", "trust", "Trust", mode),
            _status_row("relationship", "boredom", "Boredom", mode),
        ]

        if mode in ("insight", "full", "developer"):
            rows.append(_status_row("relationship", "momentum", "Momentum", mode))

        return rows


    def status_leia_rows(mode=None):
        mode = mode or current_choice_mode()

        if mode == "normal":
            return [
                _status_row("partner", "curiosity", "Curiosity", mode),
                _status_row("partner", "exhibitionism", "Comfort Being Seen", mode),
                _status_row("partner", "boundary_looseness", "Boundary Flexibility", mode),
            ]

        if mode == "insight":
            return [
                _status_row("partner", "curiosity", "Curiosity", mode),
                _status_row("partner", "temptation", "Temptation", mode),
                _status_row("partner", "exhibitionism", "Comfort Being Seen", mode),
                _status_row("partner", "boundary_looseness", "Boundary Flexibility", mode),
            ]

        return [
            _status_row("partner", "curiosity", "Curiosity", mode),
            _status_row("partner", "temptation", "Temptation", mode),
            _status_row("partner", "exhibitionism", "Exhibitionism", mode),
            _status_row("partner", "boundary_looseness", "Boundary Flexibility", mode),
            _status_row("partner", "secrecy", "Secrecy", mode),
        ]


    def status_ryan_rows(mode=None):
        mode = mode or current_choice_mode()
        return [
            _status_row("player", "jealousy", "Jealousy", mode),
            _status_row("player", "acceptance", "Acceptance", mode),
        ]


    def status_route_rows(mode=None):
        mode = mode or current_choice_mode()
        if mode not in ("full", "developer"):
            return []

        rows = [
            {
                "label": "NTS Tendency",
                "value": nts_score(),
                "detail": "{} / 100".format(nts_score()),
                "internal_key": "nts_score()" if mode == "developer" else "",
            },
            {
                "label": "NTR Tendency",
                "value": ntr_score(),
                "detail": "{} / 100".format(ntr_score()),
                "internal_key": "ntr_score()" if mode == "developer" else "",
            },
        ]
        return rows


    def leia_overview_text():
        """A short, intentionally non-spoilery behavioural summary of Leia."""
        relationship = renpy.store.relationship_stats
        partner = renpy.store.partner_stats
        name = renpy.store.girlfriend_name

        closeness = int(round((relationship["love"] + relationship["trust"]) / 2.0))
        curiosity = partner["curiosity"]
        exhibitionism = partner["exhibitionism"]
        boundaries = partner["boundary_looseness"]

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

        if curiosity >= 75:
            curiosity_line = "Her curiosity is becoming difficult to ignore, and she is increasingly willing to explore unfamiliar ideas."
        elif curiosity >= 50:
            curiosity_line = "She has a noticeable curious streak and seems increasingly willing to consider new experiences."
        elif curiosity >= 30:
            curiosity_line = "Small signs of curiosity are beginning to show, even if she is still cautious about acting on them."
        else:
            curiosity_line = "She is still fairly reserved and tends to prefer situations she already understands and trusts."

        if exhibitionism >= 70:
            visibility_line = "She also seems genuinely comfortable being noticed and drawing attention to herself."
        elif exhibitionism >= 40:
            visibility_line = "She is becoming more comfortable with being noticed, although it still depends heavily on the situation."
        elif exhibitionism >= 20:
            visibility_line = "She can enjoy a little attention, but she is not yet naturally drawn to being the centre of it."
        else:
            visibility_line = "She remains quite private about how she presents herself and rarely seeks extra attention."

        if boundaries >= 70:
            boundary_line = "Her comfort zone has expanded considerably, and ideas that once felt too far may now feel discussable."
        elif boundaries >= 45:
            boundary_line = "Her boundaries are becoming more flexible, provided she feels safe and involved in the decision."
        elif boundaries >= 20:
            boundary_line = "She may entertain small steps outside her usual comfort zone, but clear reassurance still matters."
        else:
            boundary_line = "For now, she still prefers familiar boundaries and a strong sense of control over what happens next."

        return "{} {} {} {}".format(
            relationship_line,
            curiosity_line,
            visibility_line,
            boundary_line,
        )
