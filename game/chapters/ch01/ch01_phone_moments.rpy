# Chapter One — diegetic Phone story moments.
#
# Keep Phone beats separate from visible scene dialogue where possible so the
# handset feels like a living background system rather than an exposition stop.
# Stable message IDs + story flags make these moments rollback/load safe.

init python:

    if "ch01_phone_story_triggers" not in config.overlay_screens:
        config.overlay_screens.append("ch01_phone_story_triggers")


    def ch01_share_pool_photos_to_trip_group():
        """Julian sends the earlier pool photos while Leia and Ryan get ready.

        The group photo is always available. If Scene 5 produced a separate
        favourite solo shot, Julian sends that as well and uses it for the
        notification-bearing message. On the stop branch, the group photo is
        the keeper and carries the caption itself.
        """
        if has_story_flag("ch01_pool_photos_shared_to_group"):
            return None

        selected_photo = get_story_value(
            "ch01_selected_photo_asset",
            "ch01_photo_group",
        )

        if selected_photo != "ch01_photo_group":
            phone_add_message(
                "group",
                "julian",
                text="",
                message_id="ch01_trip_group_pool_photo_group",
                attachment_id="ch01_photo_group",
                attachment_label="Pool photo — the three of us",
                mark_unread=True,
                notify=False,
            )

            phone_add_message(
                "group",
                "julian",
                text="Am I the best photographer or what?",
                message_id="ch01_trip_group_pool_photo_favourite",
                attachment_id=selected_photo,
                attachment_label="Leia's favourite pool photo",
                mark_unread=True,
                notify=True,
                notification_title="Trip Group",
            )
        else:
            phone_add_message(
                "group",
                "julian",
                text="Am I the best photographer or what?",
                message_id="ch01_trip_group_pool_photo_group",
                attachment_id="ch01_photo_group",
                attachment_label="Pool photo — the three of us",
                mark_unread=True,
                notify=True,
                notification_title="Trip Group",
            )

        set_story_flag("ch01_pool_photos_shared_to_group")
        return None


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
