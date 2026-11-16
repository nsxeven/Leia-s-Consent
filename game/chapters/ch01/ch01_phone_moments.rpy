# Chapter One — diegetic Phone story moments.
#
# Keep Phone beats separate from visible scene dialogue where possible so the
# handset feels like a living background system rather than an exposition stop.
# Stable message IDs + story flags make these moments rollback/load safe.

init python:

    if "ch01_phone_story_triggers" not in config.overlay_screens:
        config.overlay_screens.append("ch01_phone_story_triggers")


    # Pool-photo delivery is defined once, in the init 50 block below.
    # This block is responsible only for the story trigger/timing.



screen ch01_phone_story_triggers():

    # Scene 7 starts immediately after the towel incident. Waiting until Ryan
    # has answered Leia's question makes Julian's unrelated photo drop land
    # naturally during the couple's getting-ready window without adding any
    # on-screen narration or dialogue.
    if (
        phone_unlocked
        and has_story_flag("ch01_scene_06_complete")
        and has_story_value("ch01_towel_followup")
        and not has_story_flag("ch01_pool_photos_shared_to_group")
    ):
        timer 0.10 action Function(ch01_share_pool_photos_to_trip_group)


# Pool-photo Capture inventory + Phone delivery (folded from the retired
# ch01_photo_route_phone_patch.rpy in clean-up PR 3).
#
# Scene 5 stores ch01_pool_capture_count (1–3). This block is the single
# implementation that maps that count + selected swimsuit to actual Capture
# assets and sends the earned photos to Trip Group. The trigger/timing is
# ch01_phone_story_triggers above.
# load order: init 50, kept from that file so the init sequence is unchanged.
init 50 python:

    def ch01_pool_capture_assets():
        """Return the actual saved Capture photos earned during Scene 5."""
        outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
        suffix = "b" if outfit == "pool_bolder" else "a"
        count = int(get_story_value("ch01_pool_capture_count", 1))
        count = max(0, min(3, count))
        # Zero is intentional: the early-stop branch deletes the only
        # solo photograph. Do not resurrect it by coercing 0 to 1.
        return ["ch01_photo_capture_{:02d}_{}".format(i, suffix) for i in range(1, count + 1)]


    def ch01_share_pool_photos_to_trip_group():
        """Julian sends every earned Capture; attachments persist in Photos."""
        if has_story_flag("ch01_pool_photos_shared_to_group"):
            return None

        assets = ch01_pool_capture_assets()
        for index, asset_id in enumerate(assets):
            final = index == len(assets) - 1
            phone_add_message(
                "group",
                "julian",
                text=("Am I the best photographer or what?" if final else ""),
                message_id="ch01_trip_group_pool_capture_{:02d}".format(index + 1),
                attachment_id=asset_id,
                attachment_label="{} pool photo {:02d}".format(renpy.store.girlfriend_name, index + 1),
                mark_unread=True,
                notify=final,
                notification_title="Trip Group",
            )
            # phone_add_message() automatically indexes image attachments in Photos.

        if len(assets) == 3:
            phone_offer_reply("group", "ch01_pool_photo_reply", [
                {"id": "good", "text": "Yeah bro, these are good.",
                 "followups": [("julian", "Glad you like them. I had about four more with my thumb over the lens.")]},
                {"id": "wedding", "text": "Wow, you're my wedding photographer now?",
                 "followups": [("julian", "Please don't book me yet. Half the shots before these were blurry.")]},
                {"id": "last", "text": "Wait, that last one is my favorite.",
                 "followups": [("leia", "Oh, that's your favorite? I thought you'd pick the first one, wait, now I'm looking again.")]},
            ], "good")

        set_story_value("ch01_pool_phone_solo_photo_count", len(assets))
        set_story_value("ch01_pool_phone_attachment_count", len(assets))
        set_story_flag("ch01_pool_photos_shared_to_group")
        return None


# Capture assets are defined in ch01_scenes_04_06_visuals.rpy.


# Phone attachment aliases for Chapter 1 CG placeholders (folded from the retired
# zz_ch01_phone_photo_aliases.rpy in clean-up PR 3; image statements run at init 500
# wherever they live).
# Story scene CGs use the `cg ...` image namespace, while Phone attachments store
# stable asset IDs without that prefix. These aliases let the Phone render the
# same image instead of falling back to the Photos app icon.

image ch01_photo_group = "cg ch01_photo_group_white"
# Outfit-aware group shots can also be delivered to the late Trip Group thread.
image ch01_photo_group_white = "cg ch01_photo_group_white"
image ch01_photo_group_blue = "cg ch01_photo_group_blue"
image ch01_photo_support_a = "cg ch01_photo_capture_02_a"
image ch01_photo_support_b = "cg ch01_photo_capture_02_b"
image ch01_photo_more_a = "cg ch01_photo_capture_02_a"
image ch01_photo_more_b = "cg ch01_photo_capture_02_b"
image ch01_photo_more_second_a = "cg ch01_photo_capture_03_a"
image ch01_photo_more_second_b = "cg ch01_photo_capture_03_b"

# Actual pool Capture photographs used by Messages and persistent Photos.
image ch01_photo_capture_01_a = "cg ch01_photo_capture_01_a"
image ch01_photo_capture_02_a = "cg ch01_photo_capture_02_a"
image ch01_photo_capture_03_a = "cg ch01_photo_capture_03_a"
image ch01_photo_capture_01_b = "cg ch01_photo_capture_01_b"
image ch01_photo_capture_02_b = "cg ch01_photo_capture_02_b"
image ch01_photo_capture_03_b = "cg ch01_photo_capture_03_b"


# Chapter 1 Phone sequencing (folded from the retired zz_ch01_phone_sequence_revision.rpy
# in clean-up PR 3).
# Keeps story replies diegetic: late-photo replies arrive only while the actual
# Trip Group thread is open, closing early produces one Leia notification, and
# the next Trip Group open catches the thread up without additional notifications.
# Breakfast uses the same mechanism but waits quietly for the Trip Group thread.
# The generic open-thread reply timers stay here with the Chapter 1 timers: they live in
# the same overlay screen, and splitting it would change that screen and the overlay order.
# load order: init 998, kept from that file: PHONE_THREAD_ORDER below still overwrites the
# systems/phone_state.rpy value, and ch01_phone_sequence_overlay still registers after
# ch01_phone_story_triggers (init 0, above), so the overlay order is unchanged.
init 998 python:
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
            ch01_offer_movie_photo_reply()

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

    if _ch01_group_thread_open and not has_story_flag("ch01_late_photo_followup_pending"):
        # Reuse the staged late-photo conversation's open-thread timer cadence.
        # Leaving the chat pauses a pending send/reaction; reopening resumes it.
        $ _ch01_reply_steps = getattr(renpy.store, "phone_reply_delivery", {}).get("group", ())
        if _ch01_reply_steps:
            if _ch01_reply_steps[0][0] == "player":
                timer 0.55 action Function(phone_deliver_reply_step, "group")
            else:
                timer 0.90 action Function(phone_deliver_reply_step, "group")

    if has_story_flag("ch01_breakfast_reply_pending"):
        if _ch01_group_thread_open:
            if not has_story_flag("ch01_breakfast_phone_session_active"):
                timer 0.05 action Function(ch01_breakfast_begin_phone_session)
            else:
                timer 1.00 action Function(ch01_breakfast_deliver_leia_reply)
        elif not _ch01_phone_open and has_story_flag("ch01_breakfast_phone_session_active"):
            timer 0.05 action Function(ch01_breakfast_phone_closed_early)
