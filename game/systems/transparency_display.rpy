# Player-facing transparency / gameplay information helpers.
# The underlying game rules never change; only the amount of information shown does.

init python:

    PLAYER_TRANSPARENCY_MODES = ("normal", "insight", "full")

    PLAYER_TRANSPARENCY_INFO = {
        "normal": {
            "label": "Immersive",
            "tagline": "Story-first experience",
            "description": "Focus on dialogue, behaviour, and reactions. Hidden mechanics stay hidden.",
            "choices": "No mechanical effects are shown before a choice.",
            "status": "Approximate bars only; internal-only traits stay hidden.",
            "wardrobe": "See whether Leia is comfortable, without exact requirements.",
            "routes": "No route or eligibility information is revealed.",
        },
        "insight": {
            "label": "Insight",
            "tagline": "Gentle guidance",
            "description": "See broad signals about how choices and relationship dynamics are shifting without exact numbers.",
            "choices": "Directional effects such as Curiosity ↑ or Trust ↓.",
            "status": "Broad descriptions such as Low, Moderate, or High.",
            "wardrobe": "General comfort-path hints without exact thresholds.",
            "routes": "Subtle progression signals where appropriate.",
        },
        "full": {
            "label": "Full Transparency",
            "tagline": "Exact mechanics",
            "description": "See exact mechanics and optionally switch route direction through the Route Explorer.",
            "choices": "Exact numerical stat changes before choosing.",
            "status": "Exact values, hidden traits, and route tendencies.",
            "wardrobe": "Exact stat thresholds and wear requirements.",
            "routes": "Exact eligibility plus an optional route switch for upcoming early-chapter branches.",
        },
        "developer": {
            "label": "Developer",
            "tagline": "Internal debugging",
            "description": "Shows exact mechanics together with internal IDs, keys, and debug-only information.",
            "choices": "Exact changes plus internal choice IDs.",
            "status": "Exact values plus internal stat keys.",
            "wardrobe": "Thresholds, current values, PASS/FAIL state, and path IDs.",
            "routes": "Internal route/debug information where available.",
        },
    }


    def transparency_mode_info(mode=None):
        mode = mode or current_choice_mode()
        return PLAYER_TRANSPARENCY_INFO.get(mode, PLAYER_TRANSPARENCY_INFO["normal"])


    def transparency_mode_label(mode=None):
        return transparency_mode_info(mode)["label"]


    def set_player_transparency_mode(mode):
        """Set one of the three player-facing transparency preferences."""
        if mode not in PLAYER_TRANSPARENCY_MODES:
            raise ValueError("Unknown player transparency mode: {}".format(mode))

        first_full_selection = (
            mode == "full"
            and not getattr(renpy.store.persistent, "full_transparency_notice_seen", False)
        )

        if first_full_selection:
            renpy.store.persistent.full_transparency_notice_seen = True

        set_choice_display_mode(mode)

        if first_full_selection:
            renpy.notify("Full Transparency may reveal relationship trends before the story makes them obvious.")

        return mode


    def transparency_visibility_rows(mode=None):
        info = transparency_mode_info(mode)
        return (
            ("Choices", info["choices"]),
            ("Status", info["status"]),
            ("Wardrobe", info["wardrobe"]),
            ("Routes", info["routes"]),
        )


    def transparency_choice_preview(mode=None):
        mode = mode or current_choice_mode()
        base_text = "Encourage {}'s curiosity".format(renpy.store.girlfriend_name)

        if mode == "normal":
            return base_text
        if mode == "insight":
            return "{}\n[{}]".format(base_text, _choice_effect_text("dev_encourage_curiosity", exact=False))
        if mode == "full":
            return "{}\n[{}]".format(base_text, _choice_effect_text("dev_encourage_curiosity", exact=True))

        return "{}\n[{}]  [ID: dev_encourage_curiosity]".format(
            base_text,
            _choice_effect_text("dev_encourage_curiosity", exact=True),
        )


    def transparency_status_preview(mode=None):
        mode = mode or current_choice_mode()
        curiosity = renpy.store.partner_stats["curiosity"]

        if mode == "normal":
            return "Curiosity — approximate bar only"
        if mode == "insight":
            return "Curiosity — {}".format(status_band(curiosity))
        if mode == "full":
            return "Curiosity — {} / 100".format(curiosity)

        return "Curiosity — {} / 100  [partner.curiosity]".format(curiosity)


    def transparency_wardrobe_preview(mode=None):
        mode = mode or current_choice_mode()
        name = renpy.store.girlfriend_name
        base = "After Hours Dress\n{} isn't comfortable wearing this yet.".format(name)

        if mode == "normal":
            return base

        details = outfit_requirement_text("after_hours_dress", mode)
        if details:
            return "{}\n\n{}".format(base, details)
        return base
