# Chapter 1 Phone sequencing revision.
# Keeps story replies diegetic: late-photo replies arrive only while the actual
# Trip Group thread is open, closing early produces one Leia notification, and
# the next Trip Group open catches the thread up without additional notifications.
# Breakfast uses the same mechanism but waits quietly for the Trip Group thread.

init 1000 python:
    if "ch01_phone_sequence_overlay" not in config.overlay_screens:
        config.overlay_screens.append("ch01_phone_sequence_overlay")

    # Maya is now a real Messages contact rather than a temporary narration-only role.
    renpy.store.PHONE_THREAD_ORDER = ("leia", "julian", "maya", "group")

    def ch01_phone_thread_is_open(thread_id):
        """True only when the Phone is showing the requested conversation thread.

        Merely opening the handset or the Messages list must not advance staged
        story replies.
        """
        screen = renpy.get_screen("phone_screen")
        if screen is None:
            return False

        scope = getattr(screen, "scope", None) or {}
        return (
            scope.get("phone_app") == "thread"
            and scope.get("phone_thread") == thread_id
        )

    def ch01_late_photo_deliver_step(step):
        if not has_story_flag("ch01_late_photo_followup_pending"):
            return None

        if step == 1:
            phone_add_message(
                "group",
                "leia",
                text="Okay this one's actually good.",
                message_id="ch01_trip_group_late_photo_leia_react",
                mark_unread=True,
                notify=False,
            )
        elif step == 2:
            phone_add_message(
                "group",
                "julian",
                text="Actually?",
                message_id="ch01_trip_group_late_photo_julian_reply",
                mark_unread=True,
                notify=False,
            )
        elif step == 3:
            phone_add_message(
                "group",
                "leia",
                text="Don't ruin it.",
                message_id="ch01_trip_group_late_photo_leia_reply",
                mark_unread=True,
                notify=False,
            )

        current_stage = get_story_value("ch01_late_photo_followup_stage", 0)
        set_story_value("ch01_late_photo_followup_stage", max(current_stage, step))

        if step >= 3:
            clear_story_flag("ch01_late_photo_followup_pending")
            clear_story_flag("ch01_late_photo_phone_session_active")
            set_story_value("ch01_late_photo_force_complete_on_open", False)

        renpy.restart_interaction()
        return None

    def ch01_late_photo_begin_phone_session():
        set_story_flag("ch01_late_photo_phone_session_active")
        renpy.restart_interaction()
        return None

    def ch01_late_photo_finish_all():
        # Stable message IDs make this safe even if one or two steps already landed.
        for step in (1, 2, 3):
            if get_story_value("ch01_late_photo_followup_stage", 0) < step:
                ch01_late_photo_deliver_step(step)
        clear_story_flag("ch01_late_photo_followup_pending")
        clear_story_flag("ch01_late_photo_phone_session_active")
        set_story_value("ch01_late_photo_force_complete_on_open", False)
        renpy.restart_interaction()
        return None

    def ch01_late_photo_closed_early():
        clear_story_flag("ch01_late_photo_phone_session_active")
        set_story_value("ch01_late_photo_force_complete_on_open", True)
        phone_show_notification("Trip Group", "Okay this one's actually good.")
        renpy.restart_interaction()
        return None

    def ch01_breakfast_begin_phone_session():
        set_story_flag("ch01_breakfast_phone_session_active")
        renpy.restart_interaction()
        return None

    def ch01_breakfast_deliver_leia_reply():
        if not has_story_flag("ch01_breakfast_reply_pending"):
            return None

        phone_add_message(
            "group",
            "leia",
            text="No promises.",
            message_id="ch01_trip_group_breakfast_leia_reply",
            mark_unread=True,
            notify=False,
        )
        clear_story_flag("ch01_breakfast_reply_pending")
        clear_story_flag("ch01_breakfast_phone_session_active")
        renpy.restart_interaction()
        return None

    def ch01_breakfast_phone_closed_early():
        # Unlike the late-photo chain, this reply should not generate another
        # outside-the-Phone notification. It simply waits for the next thread open.
        clear_story_flag("ch01_breakfast_phone_session_active")
        renpy.restart_interaction()
        return None


screen ch01_phone_sequence_overlay():
    zorder 320

    $ _ch01_phone_open = renpy.get_screen("phone_screen") is not None
    $ _ch01_group_thread_open = ch01_phone_thread_is_open("group")

    if has_story_flag("ch01_late_photo_followup_pending"):
        if _ch01_group_thread_open:
            if not has_story_flag("ch01_late_photo_phone_session_active"):
                timer 0.05 action Function(ch01_late_photo_begin_phone_session)
            elif get_story_value("ch01_late_photo_force_complete_on_open", False):
                timer 0.05 action Function(ch01_late_photo_finish_all)
            else:
                $ _ch01_late_stage = get_story_value("ch01_late_photo_followup_stage", 0)
                if _ch01_late_stage == 0:
                    timer 0.80 action Function(ch01_late_photo_deliver_step, 1)
                elif _ch01_late_stage == 1:
                    timer 0.90 action Function(ch01_late_photo_deliver_step, 2)
                elif _ch01_late_stage == 2:
                    timer 0.90 action Function(ch01_late_photo_deliver_step, 3)
        elif not _ch01_phone_open and has_story_flag("ch01_late_photo_phone_session_active"):
            # Leaving the chat for the Messages list simply pauses the sequence.
            # Closing the handset itself triggers Leia's follow-up notification.
            timer 0.05 action Function(ch01_late_photo_closed_early)

    if has_story_flag("ch01_breakfast_reply_pending"):
        if _ch01_group_thread_open:
            if not has_story_flag("ch01_breakfast_phone_session_active"):
                timer 0.05 action Function(ch01_breakfast_begin_phone_session)
            else:
                timer 1.00 action Function(ch01_breakfast_deliver_leia_reply)
        elif not _ch01_phone_open and has_story_flag("ch01_breakfast_phone_session_active"):
            timer 0.05 action Function(ch01_breakfast_phone_closed_early)
