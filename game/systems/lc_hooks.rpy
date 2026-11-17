# Hooks - how one system reacts to another without re-defining it
#
# Purpose: A system that adds behaviour to another system's function registers a named hook; the
#   owning function calls its hook point. This replaces the old pattern of a later file capturing
#   `_orig = f` and re-defining f (tests/test_structure_rules.py rejects duplicate defs). Exceptions
#   are not swallowed: a hook that must never break its caller wraps its own body.
#
# Public API (call these from scenes/screens):
#   lc_hook_add(event, fn)                    register fn for event (once per fn); returns fn
#   lc_hook_run(event, *args, **kw) -> None   call every fn for event in registration order
#   lc_hook_filter(event, value, *args)       value = fn(value, *args) through every fn; returns
#       value
#
# Example:
#   init 10 python:
#       def my_system_on_flag(flag_id, value):
#           if flag_id == "ch01_day_02_complete" and value:
#               persistent.my_unlock = True
#       lc_hook_add("story_flag_set", my_system_on_flag)
#
# Notes: Save safety: register hooks only at init. Ren'Py saves only store names changed after
#   init and _lc_hooks is filled during init, so saves never reference a hook; python_dict /
#   python_list keep the registry out of rollback.
#
# Depends on: nothing
# Hooks: events in use: story_flag_set (flag_id, value) after set_story_flag
#   (systems/story_state.rpy; listener systems/chapter_select.rpy); review_finished (day_id) after
#   lc_review_finish (systems/day_review.rpy; listeners systems/lc_tag_collection.rpy and
#   systems/discovery.rpy); phone_closed () at the end of lc_phone_close
#   (screens/phone_sweetheart.rpy; listener systems/feed.rpy); review_titles
#   filter over the (ryan, leia) titles lc_review_titles returns (listener
#   systems/lc_tag_collection.rpy); choice_effects filter and choice_applied (choice_id, effects)
#   from systems/choice_engine.rpy (listener systems/leia_side.rpy, Leia's +2/day cap);
#   discovery_strip filter over the Moments strip items (systems/discovery.rpy; listener
#   systems/leia_side.rpy, which also listens to review_finished)
# Load order: init -100, so every system can register from its own init block
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_lc_hooks.py

init -100 python:

    _lc_hooks = python_dict()  # internal: event -> python_list of hook functions

    def lc_hook_add(event, fn):
        """Register fn for event (once per fn). Returns fn."""
        hooks = _lc_hooks.setdefault(event, python_list())
        if fn not in hooks:
            hooks.append(fn)
        return fn

    def lc_hook_run(event, *args, **kw):
        """Call every hook for event in registration order; exceptions propagate."""
        for fn in tuple(_lc_hooks.get(event, ())):
            fn(*args, **kw)
        return None

    def lc_hook_filter(event, value, *args):
        """Pass value through each hook for event in order and return the result."""
        for fn in tuple(_lc_hooks.get(event, ())):
            value = fn(value, *args)
        return value
