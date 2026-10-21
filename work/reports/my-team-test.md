# Inspection Report: Leia's Consent Game Files

## Jump Target (game/script.rpy)
The startup jump target is `prologue_name_setup`. The file defines `label start` which jumps to this label.

## Functions Defined (game/systems/story_state.rpy)
The following 10 functions are defined in the `init python:` block:

1. `set_story_flag(flag_id, value=True)` — Set a boolean story flag
2. `has_story_flag(flag_id)` — Check if a story flag is true
3. `clear_story_flag(flag_id)` — Remove a story flag
4. `set_story_value(key, value)` — Store an arbitrary story value
5. `get_story_value(key, default=None)` — Read a stored story value
6. `has_story_value(key)` — Check if a story value exists
7. `clear_story_value(key)` — Remove a stored story value
8. `resolve_story_outcome(key, options, weights=None)` — Resolve and cache an outcome
9. `story_state_summary()` — Return developer-facing state snapshot
10. `debug_reset_story_state()` — Reset all flags and values

---
*Sources:* `game/script.rpy`, `game/systems/story_state.rpy`
