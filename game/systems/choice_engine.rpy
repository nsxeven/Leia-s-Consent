# Central choice-effect system.
# Story files provide the visible choice text and a stable choice ID.
# Effects live here so gameplay, Insight mode, Full Cheat mode, and developer tools all read the same data.

init python:

    CHOICE_MODES = ("normal", "insight", "full", "developer")

    CHOICE_MODE_LABELS = {
        "normal": "Normal",
        "insight": "Insight",
        "full": "Full Cheat",
        "developer": "Developer",
    }

    STAT_LABELS = {
        "love": "Love",
        "trust": "Trust",
        "boredom": "Boredom",
        "momentum": "Momentum",
        "curiosity": "Curiosity",
        "temptation": "Temptation",
        "exhibitionism": "Exhibitionism",
        "boundary_looseness": "Boundary Looseness",
        "secrecy": "Secrecy",
        "jealousy": "Jealousy",
        "acceptance": "Acceptance",
    }

    # Static definitions. Add future story choices here with stable IDs.
    CHOICE_EFFECTS = {
        "dev_encourage_curiosity": [
            ("partner", "curiosity", 5),
            ("player", "acceptance", 3),
            ("relationship", "momentum", 1),
        ],
        "dev_be_protective": [
            ("relationship", "trust", 3),
            ("player", "jealousy", 3),
            ("partner", "boundary_looseness", -2),
        ],
    }


    def current_choice_mode():
        """Return a valid global choice-display mode."""
        mode = getattr(renpy.store.persistent, "choice_display_mode", "normal")
        if mode not in CHOICE_MODES:
            return "normal"
        return mode


    def choice_mode_label():
        return CHOICE_MODE_LABELS[current_choice_mode()]


    def set_choice_display_mode(mode):
        """Set the global display preference used by all future choices."""
        if mode not in CHOICE_MODES:
            raise ValueError("Unknown choice display mode: {}".format(mode))

        renpy.store.persistent.choice_display_mode = mode
        renpy.save_persistent()
        renpy.restart_interaction()


    def get_choice_effects(choice_id):
        """Return a copy of the effects for a stable choice ID."""
        if choice_id not in CHOICE_EFFECTS:
            raise ValueError("Unknown choice ID: {}".format(choice_id))
        return list(CHOICE_EFFECTS[choice_id])


    def apply_choice(choice_id):
        """Apply the real effects for a choice and record the selection."""
        for group_name, stat_name, amount in get_choice_effects(choice_id):
            change_stat(group_name, stat_name, amount)

        renpy.store.last_choice_id = choice_id
        renpy.store.choice_history.append(choice_id)
        return choice_id


    def _choice_effect_text(choice_id, exact=False):
        parts = []

        for group_name, stat_name, amount in get_choice_effects(choice_id):
            label = STAT_LABELS.get(stat_name, stat_name.replace("_", " ").title())

            if exact:
                parts.append("{} {:+d}".format(label, amount))
            else:
                arrow = "↑" if amount > 0 else "↓" if amount < 0 else "→"
                parts.append("{} {}".format(label, arrow))

        return " • ".join(parts)


    def format_choice(choice_id, base_text):
        """Return the player-facing text for a choice under the active display mode."""
        mode = current_choice_mode()

        if mode == "normal":
            return base_text

        if mode == "insight":
            return "{}\n[{}]".format(base_text, _choice_effect_text(choice_id, exact=False))

        if mode == "full":
            return "{}\n[{}]".format(base_text, _choice_effect_text(choice_id, exact=True))

        return "{}\n[{}]  [ID: {}]".format(
            base_text,
            _choice_effect_text(choice_id, exact=True),
            choice_id,
        )


    def choice_preview_text():
        """Safe live preview used by the choice-mode screen."""
        base_text = "Encourage {}'s curiosity".format(renpy.store.girlfriend_name)
        return format_choice("dev_encourage_curiosity", base_text)
