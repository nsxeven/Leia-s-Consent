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
        "ch01_outfit_bolder": [
            ("partner", "curiosity", 3),
            ("player", "acceptance", 3),
            ("relationship", "trust", 1),
        ],
        "ch01_outfit_comfort": [
            ("relationship", "trust", 2),
            ("relationship", "love", 1),
        ],
        "ch01_outfit_conservative": [
            ("player", "jealousy", 1),
            ("relationship", "trust", 1),
        ],
    }

    # Behavioral metadata is deliberately separate from stat effects. Later scenes
    # can react to patterns such as encouragement/protectiveness without checking
    # a long list of specific choice IDs.
    CHOICE_TAGS = {
        "dev_encourage_curiosity": ("encouraging", "participating", "open"),
        "dev_be_protective": ("protective", "cautious"),
        "ch01_outfit_bolder": ("encouraging", "open", "supportive"),
        "ch01_outfit_comfort": ("neutral", "comfort-first", "supportive"),
        "ch01_outfit_conservative": ("protective", "cautious", "respectful"),
    }

    STANCE_TAGS = ("encouraging", "neutral", "protective")


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


    def get_choice_tags(choice_id):
        """Return immutable behavioral tags for a stable choice ID."""
        return tuple(CHOICE_TAGS.get(choice_id, ()))


    def apply_choice(choice_id):
        """Apply the real effects for a choice and record the selection."""
        for group_name, stat_name, amount in get_choice_effects(choice_id):
            change_stat(group_name, stat_name, amount)

        renpy.store.last_choice_id = choice_id
        renpy.store.choice_history.append(choice_id)
        return choice_id


    def choice_ids_with_prefix(prefix, choice_ids=None):
        """Return recorded choices whose stable IDs begin with a chapter/event prefix."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        return [choice_id for choice_id in source if choice_id.startswith(prefix)]


    def choice_tag_count(tag, choice_ids=None):
        """Count how often a behavioral tag appears in the selected choice history."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        return sum(1 for choice_id in source if tag in get_choice_tags(choice_id))


    def choice_tag_counts(choice_ids=None):
        """Return counts for every behavioral tag represented in the selected history."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        counts = {}
        for choice_id in source:
            for tag in get_choice_tags(choice_id):
                counts[tag] = counts.get(tag, 0) + 1
        return counts


    def choice_stance(choice_ids=None):
        """Summarize encouraging/neutral/protective behavior without creating hard routes."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        counts = {tag: choice_tag_count(tag, source) for tag in STANCE_TAGS}
        highest = max(counts.values()) if counts else 0

        if highest <= 0:
            return "neutral"

        leaders = [tag for tag, count in counts.items() if count == highest]
        if len(leaders) != 1:
            return "mixed"
        return leaders[0]


    def chapter_choice_ids(chapter_id):
        """Convention: real chapter choice IDs begin with e.g. 'ch01_'."""
        prefix = chapter_id if chapter_id.endswith("_") else chapter_id + "_"
        return choice_ids_with_prefix(prefix)


    def chapter_stance(chapter_id):
        return choice_stance(chapter_choice_ids(chapter_id))


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

        tags = get_choice_tags(choice_id)
        tag_text = " • Tags: {}".format(", ".join(tags)) if tags else ""
        return "{}\n[{}]  [ID: {}]{}".format(
            base_text,
            _choice_effect_text(choice_id, exact=True),
            choice_id,
            tag_text,
        )


    def choice_preview_text():
        """Safe live preview used by the choice-mode screen."""
        base_text = "Encourage {}'s curiosity".format(renpy.store.girlfriend_name)
        return format_choice("dev_encourage_curiosity", base_text)
