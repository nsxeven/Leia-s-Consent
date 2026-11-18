# Choice engine - stat effects, tags and display of every story choice
#
# Purpose: Owns CHOICE_EFFECTS / CHOICE_TAGS (stable choice id -> effects and behaviour tags), the
#   choice display mode (Immersive/Insight/Full/Developer), the caption formatter and apply_choice,
#   which applies effects, records history and shows feedback. Story files only supply the caption
#   text and the id; every Day pack registers its ids with CHOICE_EFFECTS.update(...) in its
#   *_registrations.rpy (init 1; docs/DAY_PACK.md).
#
# Public API (call these from scenes/screens):
#   CHOICE_EFFECTS                            {choice_id: [(group, stat, amount), ...]} (extended by
#       day files)
#   CHOICE_TAGS                               {choice_id: (tag, ...)} behaviour tags (encouraging,
#       nonchalant, ...)
#   CHOICE_MODES                              the display modes
#   STAT_LABELS                               {stat: player-facing name}
#   format_choice(choice_id, base_text)       caption for a menu item in the current display mode
#   apply_choice(choice_id)                   apply effects, record history, show feedback; returns
#       choice_id
#   current_choice_mode()                     the active display mode ('normal', 'insight', 'full',
#       'developer')
#   choice_mode_label()                       display name of the active mode
#   lc_track_text_v2(text)                    a Day's track card with the old stat-model headings
#       renamed to route names (LC_TRACK_HEADINGS_V2)
#   set_choice_display_mode(mode) -> None     set the global display mode
#   get_choice_effects(choice_id)             copy of a choice's effects (legacy stats folded to v2)
#   lc_choice_effective_effects(choice_id)    the effects apply_choice would apply now: the
#       registered ones through the choice_effects filter (Leia's side caps her gains)
#   get_choice_tags(choice_id)                behaviour tags of a choice
#   lc_choice_route_tag(choice_id)            Full Transparency route tag of a choice
#   choice_ids_with_prefix(prefix, choice_ids=None)
#       recorded choice ids starting with a prefix
#   choice_tag_count(tag, choice_ids=None)    how often a tag appears in the recorded history
#   choice_tag_counts(choice_ids=None)        counts for every tag in the history
#   choice_stance(choice_ids=None)            'encouraging' / 'protective' / 'neutral' / 'mixed'
#       summary
#   chapter_choice_ids(chapter_id)            recorded choice ids of one chapter prefix
#   chapter_stance(chapter_id)                choice_stance() for one chapter
#   chapter_nonchalant_count(chapter_id)      nonchalant choices in one chapter
#   choice_preview_text()                     live sample caption for the choice-mode screen
#   show_choice_feedback(choice_id, effects=None) -> None
#       post-choice toast (Insight/Full); effects = what apply_choice applied
#   clear_choice_feedback(serial) -> None     screen action: hide a toast by serial
#   maybe_show_status_choice_tutorial(choice_id) -> None
#       one-time onboarding after the first stat change
#
# Internal (helpers for this file and its screens; do not call from scenes): _choice_effect_text,
#   LCChoiceToastRuntime, lc_choice_feedback_sound
#
# Example:
#   $ ch01_outfit_bolder_text = format_choice("ch01_outfit_bolder", "Not at all. You'd look amazing in it.")
#   menu:
#       "[ch01_outfit_bolder_text]":
#           $ apply_choice("ch01_outfit_bolder")
#
# Depends on: systems/stats.rpy (change_stat), systems/day_review.rpy (lc_review_note_choice),
#   python-packages/lc_stat_model.py, python-packages/lc_ui_logic.py, screens/scrapbook_ui.rpy
#   (toast screens)
# Hooks: emits choice_effects (filter over a choice's effects, choice_id) wherever effects are
#   shown or applied, and choice_applied (choice_id, effects) after apply_choice moved the stats
#   (listener for both: systems/leia_side.rpy, the +2/day cap on Leia's side)
# Load order: init 0 for the tables and formatters (day files extend them at init 1-2); init 90 for
#   the feedback/apply block, kept from the retired load-order file so the init sequence is
#   unchanged
# Docs: docs/STAT_MODEL.md   Tests: tests/test_choice_scoring.py, tests/test_choice_path_tags.py,
#   tests/test_stat_runtime.py

init python:

    CHOICE_MODES = ("normal", "insight", "full", "developer")

    CHOICE_MODE_LABELS = {
        "normal": "Normal",
        "insight": "Insight",
        "full": "Full Transparency",
        "developer": "Developer",
    }

    import lc_stat_model

    # One display name per stat, in every mode and on every screen.
    STAT_LABELS = dict(lc_stat_model.STAT_LABELS)

    # Static definitions. Add future story choices here with stable IDs.
    # Stat model v2 scoring rule (tests/test_choice_scoring.py enforces it for
    # every CHOICE_EFFECTS entry): stats are love / trust / sharing / temptation
    # ("relationship") and exhibitionism ("partner"); at most two stats per
    # choice (hard gates three), one route stat (Exhibitionism, Sharing or
    # Temptation), Temptation up never with another stat going up, +-1 ordinary,
    # +-2 strong, +-3 key beat, gates up to +-5. Neutral banter has no stats.
    CHOICE_EFFECTS = {
        "dev_encourage_curiosity": [
            ("partner", "exhibitionism", 3),
        ],
        "dev_be_protective": [
            ("relationship", "trust", 3),
        ],
        "ch01_d2_mall_go_to_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_leave_to_maya": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_mall_reveal_affection": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_reveal_open": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d2_mall_reveal_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_mall_reveal_flat": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
    }

    # Behavioral metadata is deliberately separate from stat effects. Later scenes
    # can react to patterns such as encouragement/protectiveness/nonchalance without
    # checking a long list of specific choice IDs.
    CHOICE_TAGS = {
        "dev_encourage_curiosity": ("encouraging", "participating", "open"),
        "dev_be_protective": ("protective", "cautious"),
        "ch01_d2_mall_go_to_leia": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_leave_to_maya": ("neutral", "nonchalant", "dismissive", "withdrawal", "ntr-seed"),
        "ch01_d2_mall_reveal_affection": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_reveal_open": ("encouraging", "participating", "open", "exhibitionism-seed"),
        "ch01_d2_mall_reveal_tease": ("encouraging", "playful", "attentive"),
        "ch01_d2_mall_reveal_flat": ("neutral", "nonchalant", "distracted"),
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
        """Return a copy of the effects for a stable choice ID.

        Old-style tuples (retired stats such as boredom or curiosity) are folded
        onto the five v2 stats, so a stale entry can never crash a save; the
        scoring test still fails on them.
        """
        if choice_id not in CHOICE_EFFECTS:
            raise ValueError("Unknown choice ID: {}".format(choice_id))
        return lc_stat_model.fold_legacy_effects(CHOICE_EFFECTS[choice_id])


    def lc_choice_effective_effects(choice_id):
        """The effects apply_choice would apply right now: get_choice_effects passed through the
        choice_effects hook filter (systems/leia_side.rpy cuts Leia-side gains to her +2 a day).
        Same length and order as get_choice_effects, so labels can show which stat was cut."""
        return lc_hook_filter("choice_effects", get_choice_effects(choice_id), choice_id)


    def lc_choice_route_tag(choice_id):
        """Full Transparency route tag ('Love', 'Love+Exhib', 'NTS', 'NTR', 'Repair',
        'May lead to NTR', 'Locks NTR', 'NTR stays open', 'Neutral', ...).

        Derived from the choice's effects plus the route value its branch writes
        (lc_stat_model.CHOICE_ROUTE_FLAGS), never hand-typed, so tag and chips
        can't disagree.
        """
        return lc_stat_model.choice_route_tag(choice_id, get_choice_effects(choice_id))


    def get_choice_tags(choice_id):
        """Return immutable behavioral tags for a stable choice ID."""
        return tuple(CHOICE_TAGS.get(choice_id, ()))


    # Track cards (Insight / Full / Developer): a Day's *_track_text() passes its card through
    # lc_track_text_v2 so the old stat-model headings read as route names.
    # Old heading -> route name. "SHARED EXHIBITION (NTS)" was the Love +
    # Exhibitionism track (nobody else joins in), so it no longer says NTS.
    LC_TRACK_HEADINGS_V2 = (
        ("TRACK: SHARED EXHIBITION (NTS)", "TRACK: LOVE + EXHIBITIONISM"),
        ("TRACK: DISTANCE, REPAIRED (NTR pressure)", "TRACK: NTR, REPAIRED"),
        ("TRACK: DISTANCE, UNRESOLVED (NTR pressure)", "TRACK: NTR, UNRESOLVED"),
        ("TRACK: DISTANCE, CONFIRMED (NTR pressure)", "TRACK: NTR, CONFIRMED"),
        ("TRACK: DISTANCE (NTR pressure)", "TRACK: NTR"),
    )

    def lc_track_text_v2(text):
        if not text:
            return text
        for old, new in LC_TRACK_HEADINGS_V2:
            if text.startswith(old):
                return new + text[len(old):]
        return text


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


    def chapter_nonchalant_count(chapter_id):
        """Count dismissive/nonchalant choices for route-pressure checks."""
        return choice_tag_count("nonchalant", chapter_choice_ids(chapter_id))


    def _choice_effect_text(choice_id, exact=False, effects=None):
        """Stat line of a choice. effects: what is (or was) really applied; default = the
        effective effects now. A gain the choice_effects filter cut is labelled
        "<Stat> (capped)" with the amount that really applies (docs/LEIA_SIDE.md)."""
        parts = []
        registered = get_choice_effects(choice_id)
        if effects is None:
            effects = lc_choice_effective_effects(choice_id)
        if len(effects) != len(registered):
            registered = effects

        for (_g, _s, meant), (group_name, stat_name, amount) in zip(registered, effects):
            label = STAT_LABELS.get(stat_name, stat_name.replace("_", " ").title())
            if amount != meant:
                label += lc_stat_model.CAPPED_SUFFIX

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
            effects = _choice_effect_text(choice_id, exact=False)
            return "{}\n[{}]".format(base_text, effects) if effects else base_text

        if mode == "full":
            # {#lcpath=<id>} is an invisible comment tag: the choice card reads it to
            # draw the path stamp (systems/choice_path_tags.rpy).
            import lc_ui_logic
            effects = _choice_effect_text(choice_id, exact=True)
            text = "{}\n[{}]".format(base_text, effects) if effects else base_text
            return lc_ui_logic.choice_mark(choice_id) + text

        tags = get_choice_tags(choice_id)
        tag_text = " • Tags: {}".format(", ".join(tags)) if tags else ""
        return "{}\n[{}]  [ID: {}]  [Route: {}]{}".format(
            base_text,
            _choice_effect_text(choice_id, exact=True) or "no stats",
            choice_id,
            lc_choice_route_tag(choice_id),
            tag_text,
        )


    def choice_preview_text():
        """Safe live preview used by the choice-mode screen."""
        base_text = "Encourage {}'s curiosity".format(renpy.store.girlfriend_name)
        return format_choice("dev_encourage_curiosity", base_text)



# Choice runtime: apply_choice() plus the transient post-choice toast
# (LCChoiceToastRuntime, show/clear_choice_feedback, the gain/loss sound) and the
# one-time Status tutorial after the first stat-changing story choice. Feedback
# never resurrects after rollback. The toast is drawn by choice_feedback_overlay
# (screens/scrapbook_ui.rpy, registered in screens/gameplay_toasts.rpy).
# load order: init 90, kept from the retired screens/zz_day1_ui_qol_patch.rpy so
# the init sequence is unchanged (tests/test_lc_rpy_model.py pins it).
init 90 python:

    class LCChoiceToastRuntime(renpy.python.NoRollback):
        def __init__(self):
            self.payload = None
            self.serial = 0


    # Underscore-prefixed runtime object is deliberately transient UI state.
    # Its contents should not be restored by rollback or treated as story state.
    if not hasattr(renpy.store, "_lc_choice_toast_runtime"):
        renpy.store._lc_choice_toast_runtime = LCChoiceToastRuntime()


    def clear_choice_feedback(serial):
        runtime = renpy.store._lc_choice_toast_runtime
        payload = runtime.payload
        if payload and payload.get("serial") == serial:
            runtime.payload = None
        return None


    def show_choice_feedback(choice_id, effects=None):
        """Show mode-safe post-choice feedback as transient, non-rollback UI.

        effects: what apply_choice applied (a capped Leia-side gain shows as capped)."""
        if not get_choice_effects(choice_id):
            return None
        if effects is None:
            effects = lc_choice_effective_effects(choice_id)

        mode = current_choice_mode()

        if mode == "normal":
            title = "CHOICE"
            body = "Your response has been remembered."
        elif mode == "insight":
            title = "CHOICE IMPACT"
            body = _choice_effect_text(choice_id, exact=False, effects=effects)
        elif mode == "full":
            title = "STAT CHANGES"
            body = _choice_effect_text(choice_id, exact=True, effects=effects)
        else:
            title = "DEBUG CHOICE"
            tags = get_choice_tags(choice_id)
            tag_text = ", ".join(tags) if tags else "none"
            body = "{}\nID: {}\nTags: {}".format(
                _choice_effect_text(choice_id, exact=True, effects=effects),
                choice_id,
                tag_text,
            )

        runtime = renpy.store._lc_choice_toast_runtime
        runtime.serial += 1
        runtime.payload = {
            "serial": runtime.serial,
            "title": title,
            "body": body,
        }
        lc_choice_feedback_sound(effects, mode)
        return None


    def lc_choice_feedback_sound(effects, mode):
        """ui/gain when the choice's net stat change is positive, ui/loss when negative.

        Silent in Immersive (normal) mode, where stat directions stay hidden, and
        when every amount is zero. Queued so the choice's "pick" tap isn't cut off.
        """
        if mode == "normal":
            return None
        amounts = [amount for _group, _stat, amount in effects]
        if not any(amounts):
            return None
        path = lc_audio_path("ui", "gain" if sum(amounts) > 0 else "loss")
        if path:
            renpy.music.queue(path, channel="ui", clear_queue=True)
        return path


    def maybe_show_status_choice_tutorial(choice_id):
        """One-time player onboarding after the first real stat-changing story choice."""
        if choice_id.startswith("dev_"):
            return None
        if not getattr(renpy.store, "phone_unlocked", False):
            return None
        if getattr(renpy.store.persistent, "status_choice_tutorial_seen", False):
            return None
        if not any(amount != 0 for _group, _stat, amount in get_choice_effects(choice_id)):
            return None

        # Persistent UI onboarding intentionally survives rollback/new saves.
        renpy.store.persistent.status_choice_tutorial_seen = True
        renpy.save_persistent()
        renpy.show_screen("status_choice_tutorial")
        return None


    def apply_choice(choice_id):
        """Apply effects, record the choice, show transient feedback and onboarding.

        The only apply_choice (init 90, after the effect tables are registered).
        Keep the day-review snapshot here so the recap can list each choice.
        """
        review_before = lc_review_stats()
        effects = lc_choice_effective_effects(choice_id)
        for group_name, stat_name, amount in effects:
            change_stat(group_name, stat_name, amount)

        renpy.store.last_choice_id = choice_id
        renpy.store.choice_history.append(choice_id)
        lc_hook_run("choice_applied", choice_id, effects)
        lc_review_note_choice(choice_id, review_before)
        show_choice_feedback(choice_id, effects)
        maybe_show_status_choice_tutorial(choice_id)
        return choice_id
