# Reusable story-state helpers.
# These bridge choices/stats and later story reactions without hard-coding chapter logic.

init python:

    def set_story_flag(flag_id, value=True):
        """Set a boolean story flag for this save and return its new value."""
        renpy.store.story_flags[flag_id] = bool(value)
        return renpy.store.story_flags[flag_id]


    def has_story_flag(flag_id):
        """Return whether a story flag is currently true."""
        return bool(renpy.store.story_flags.get(flag_id, False))


    def clear_story_flag(flag_id):
        """Remove a story flag entirely from this save."""
        renpy.store.story_flags.pop(flag_id, None)


    def set_story_value(key, value):
        """Store an arbitrary save-specific story value."""
        renpy.store.story_values[key] = value
        return value


    def get_story_value(key, default=None):
        """Read a stored story value without creating it."""
        return renpy.store.story_values.get(key, default)


    def has_story_value(key):
        return key in renpy.store.story_values


    def clear_story_value(key):
        renpy.store.story_values.pop(key, None)


    def resolve_story_outcome(key, options, weights=None):
        """Resolve an outcome once, store it, and always return the stored result afterwards.

        Example:
            resolve_story_outcome(
                "ch01_pool_outfit",
                ["pool_conservative", "pool_bolder"],
                [60, 40],
            )

        Ren'Py's rollback-aware RNG is only consulted the first time the key is resolved.
        Save/load and revisiting the label therefore cannot reroll the result.
        """
        if key in renpy.store.story_values:
            return renpy.store.story_values[key]

        options = list(options)
        if not options:
            raise ValueError("resolve_story_outcome requires at least one option")

        if weights is None:
            result = renpy.random.choice(options)
        else:
            weights = list(weights)
            if len(weights) != len(options):
                raise ValueError("Outcome options and weights must have the same length")
            if any(weight < 0 for weight in weights):
                raise ValueError("Outcome weights cannot be negative")

            total = float(sum(weights))
            if total <= 0:
                raise ValueError("Outcome weights must total more than zero")

            roll = renpy.random.random() * total
            cumulative = 0.0
            result = options[-1]
            for option, weight in zip(options, weights):
                cumulative += float(weight)
                if roll < cumulative:
                    result = option
                    break

        renpy.store.story_values[key] = result
        return result


    def story_state_summary():
        """Compact developer-facing snapshot for notifications/tests."""
        true_flags = sorted(key for key, value in renpy.store.story_flags.items() if value)
        values = sorted(renpy.store.story_values.items())
        return "Flags: {} | Values: {}".format(
            ", ".join(true_flags) if true_flags else "None",
            ", ".join("{}={}".format(key, value) for key, value in values) if values else "None",
        )


    def debug_reset_story_state():
        renpy.store.story_flags = {}
        renpy.store.story_values = {}
        renpy.store.modified_save = True
        renpy.notify("Story flags and resolved outcomes reset.")
        return None
