# DRAFT / NOT FOR PUBLICATION

Source inspection occurred on game/script.rpy and game/systems/story_state.rpy. The startup jump target is prologue_name_setup. No game source changes were made. No runtime testing occurred.

The following functions were identified in the init python block within game/systems/story_state.rpy:

1. set_story_flag(flag_id, value=True)
2. has_story_flag(flag_id)
3. clear_story_flag(flag_id)
4. set_story_value(key, value)
5. get_story_value(key, default=None)
6. has_story_value(key)
7. clear_story_value(key)
8. resolve_story_outcome(key, options, weights=None)
9. story_state_summary()
10. debug_reset_story_state()

These functions manage story flags and values. The inspection confirms the technical structure without modifying any files or executing the game.
