# Day One UI/QOL patch.
# - Choice feedback is transient and does not resurrect after rollback.
# - Long/multiline menu choices are visually centered.
# - Status + Settings are accessible as Phone-native surfaces.
# - The first real stat-changing story choice teaches the player where Status lives.

style choice_button_text:
    text_align 0.5
    xalign 0.5
    line_spacing 4


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


    def show_choice_feedback(choice_id):
        """Show mode-safe post-choice feedback as transient, non-rollback UI."""
        effects = get_choice_effects(choice_id)
        if not effects:
            return None

        mode = current_choice_mode()

        if mode == "normal":
            title = "CHOICE"
            body = "Your response has been remembered."
        elif mode == "insight":
            title = "CHOICE IMPACT"
            body = _choice_effect_text(choice_id, exact=False)
        elif mode == "full":
            title = "STAT CHANGES"
            body = _choice_effect_text(choice_id, exact=True)
        else:
            title = "DEBUG CHOICE"
            tags = get_choice_tags(choice_id)
            tag_text = ", ".join(tags) if tags else "none"
            body = "{}\nID: {}\nTags: {}".format(
                _choice_effect_text(choice_id, exact=True),
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

        This init-90 definition replaces the choice engine's apply_choice.
        Keep the day-review snapshot here so the recap can list each choice.
        """
        review_before = lc_review_stats()
        for group_name, stat_name, amount in get_choice_effects(choice_id):
            change_stat(group_name, stat_name, amount)

        renpy.store.last_choice_id = choice_id
        renpy.store.choice_history.append(choice_id)
        lc_review_note_choice(choice_id, review_before)
        show_choice_feedback(choice_id)
        maybe_show_status_choice_tutorial(choice_id)
        return choice_id


    def lc_phone_current_app():
        """Read the active Phone app safely so extra app buttons only appear on Home."""
        phone = renpy.get_screen("phone_screen")
        if phone is None:
            return None
        scope = getattr(phone, "scope", None)
        if isinstance(scope, dict):
            return scope.get("phone_app", "home")
        return "home"


    def lc_mark_status_intro_seen():
        renpy.store.persistent.status_page_intro_seen = True
        renpy.save_persistent()
        renpy.restart_interaction()
        return None


    if "lc_phone_extra_apps" not in config.overlay_screens:
        config.overlay_screens.append("lc_phone_extra_apps")

