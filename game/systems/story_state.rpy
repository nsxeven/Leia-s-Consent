# Story state - flags and values that carry choices into later scenes
#
# Purpose: Save-specific story flags (booleans) and values (anything) by stable key; later days read
#   them instead of recomputing (e.g. ch01_d2_end_route). Keys are save data: never rename one.
#   set_story_flag emits the story_flag_set hook.
#
# Public API (call these from scenes/screens):
#   set_story_flag(flag_id, value=True)       set a flag (default True); returns the value
#   has_story_flag(flag_id) -> bool           True when a flag is set
#   get_story_flag(flag_id)                   same as has_story_flag (older name, still used)
#   clear_story_flag(flag_id) -> None         remove a flag
#   set_story_value(key, value)               store a value; returns it
#   get_story_value(key, default=None)        read a value (default if missing, never creates it)
#   has_story_value(key) -> bool              True when a key exists
#   clear_story_value(key) -> None            remove a value
#   resolve_story_outcome(key, options, weights=None)
#       pick a weighted outcome once, then always return it
#   story_state_summary()                     dev: compact text snapshot
#   debug_reset_story_state() -> None         dev: clear flags and values
#
# Example:
#   $ set_story_flag("prologue_started")
#   $ d3_end = get_story_value("ch01_d2_end_route", "love")
#
# Depends on: game/defaults.rpy (story_flags, story_values), systems/lc_hooks.rpy
# Hooks: emits story_flag_set (flag_id, value)
# Load order: init 0; get_story_flag at init 998, kept from the retired load-order file (nothing
#   reads it during init)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_behaviour_freeze.py, tests/test_save_names.py

init python:

    def set_story_flag(flag_id, value=True):
        """Set a boolean story flag for this save and return its new value.

        Afterwards runs the "story_flag_set" hooks (systems/lc_hooks.rpy) with the
        value as passed; Chapter Select's Day Two unlock is one of them.
        """
        renpy.store.story_flags[flag_id] = bool(value)
        result = renpy.store.story_flags[flag_id]
        lc_hook_run("story_flag_set", flag_id, value)
        return result


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


# get_story_flag(flag_id): boolean getter paired with set_story_flag(). Older story
# code reads has_story_flag(); newer route code assigns get_story_flag() to a local.
# load order: init 998, kept from the retired systems/zz_story_state_flag_getter.rpy
# so the init sequence is unchanged; nothing reads it during init.
init 998 python:
    def get_story_flag(flag_id):
        return has_story_flag(flag_id)
