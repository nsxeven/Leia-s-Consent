# Final Handoff Check

## Cited Files

- `game/script.rpy`
- `game/systems/story_state.rpy`

## Jump Target (from script.rpy)

```
prologue_name_setup
```

## Functions Defined in story_state.rpy

1. `set_story_flag(flag_id, value=True)`
2. `has_story_flag(flag_id)`
3. `clear_story_flag(flag_id)`
4. `set_story_value(key, value)`
5. `get_story_value(key, default=None)`
6. `has_story_value(key)`
7. `clear_story_value(key)`
8. `resolve_story_outcome(key, options, weights=None)`
9. `story_state_summary()`
10. `debug_reset_story_state()`

---

*Note: story_state.rpy contains only Python helper functions; the jump target is defined in script.rpy.*
