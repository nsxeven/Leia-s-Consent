## Load-time hooks: how one system reacts to another without re-defining it.
##
## Purpose
##   A system that wants to add behaviour to another system's function registers
##   a named hook; the owning function calls its hook point. This replaces the old
##   load-order pattern where a later file captured `_orig = f` and re-defined `f`
##   (forbidden now: tests/test_structure_rules.py rejects duplicate defs).
##
## API (defined at init -100, so every system can register from its own init block)
##   lc_hook_add(event, fn)               register fn for event; adding the same fn
##                                        again is a no-op. Returns fn.
##   lc_hook_run(event, *args, **kw)      call every fn for event in registration
##                                        order. Exceptions are NOT swallowed: a hook
##                                        that must never break its caller wraps its
##                                        own body in try/except. Returns None.
##   lc_hook_filter(event, value, *args)  pass value through each fn in order
##                                        (value = fn(value, *args)) and return it.
##
## Events in use
##   "story_flag_set"   (flag_id, value)  after set_story_flag stores a flag
##                                        (systems/story_state.rpy); chapter_select.rpy
##                                        unlocks Chapter Select after Day Two.
##   "review_finished"  (day_id)          after lc_review_finish records a day
##                                        (systems/day_review.rpy); lc_tag_collection.rpy
##                                        unlocks that day's tags and stickers.
##   "review_titles"    filter, value = the automatic (ryan, leia) titles that
##                                        lc_review_titles returns (systems/day_review.rpy);
##                                        lc_tag_collection.rpy swaps in equipped tags.
##
## Example
##   init 10 python:
##       def my_system_on_flag(flag_id, value):
##           if flag_id == "ch01_day_02_complete" and value:
##               persistent.my_unlock = True
##       lc_hook_add("story_flag_set", my_system_on_flag)
##
## Save safety: hooks are functions, registered only at init. Ren'Py saves only
## store names that change after init, and _lc_hooks is only filled during init,
## so saves never reference a hook and old saves load unchanged. python_dict /
## python_list additionally keep the registry out of rollback tracking.
## Register hooks only at init (never from story code).
## Tests: tests/test_lc_hooks.py.

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
