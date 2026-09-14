# Scene 27 Phone-chat presentation revision.
# Julian's notification is the only interruption. Leia/Julian's follow-up replies
# live inside Trip Group so the player discovers the exchange by opening the chat.

init 90 python:
    config.label_overrides["ch01_scene_27_late_photo_drop"] = "ch01_scene_27_late_photo_drop_chat_v2"


label ch01_scene_27_late_photo_drop_chat_v2:

    "The movie had been over for several minutes before any of us bothered to stand."

    friend "I'm done. If I stay here another ten minutes I'm sleeping on this sofa."
    gf "Weak."
    friend "You fell asleep in a car."
    gf "That was tactical."

    "Julian gathered his empty glass and headed toward the hallway."

    friend "Goodnight, children."
    mc "Goodnight, grandpa."
    gf "Night."

    hide julian
    with dissolve

    "A moment later my phone lit up."

    python:
        phone_add_message(
            "group",
            "julian",
            text="Forgot this one. Photographer of the year strikes again.",
            message_id="ch01_trip_group_late_pool_photo",
            attachment_id="ch01_photo_late_favourite",
            attachment_label="Unsent pool favourite",
            mark_unread=True,
            notify=True,
            notification_title="Trip Group",
        )
        set_story_value("ch01_late_pool_photo_asset", "ch01_photo_late_favourite")
        set_story_flag("ch01_late_pool_photo_shared")

        # The rest of this exchange is deliberately silent outside the Phone.
        # Opening Trip Group reveals the complete reaction chain under the one
        # notification that started the conversation.
        phone_add_message(
            "group",
            "leia",
            text="Okay this one's actually good.",
            message_id="ch01_trip_group_late_photo_leia_react",
            mark_unread=True,
            notify=False,
        )
        phone_add_message(
            "group",
            "julian",
            text="Actually?",
            message_id="ch01_trip_group_late_photo_julian_reply",
            mark_unread=True,
            notify=False,
        )
        phone_add_message(
            "group",
            "leia",
            text="Don't ruin it.",
            message_id="ch01_trip_group_late_photo_leia_reply",
            mark_unread=True,
            notify=False,
        )

    "Leia glanced down when her own phone buzzed against the sofa cushion. Her thumbs started moving a second later."
    "Whatever followed stayed in the Trip Group, waiting for me to open it."

    $ set_story_flag("ch01_scene_27_complete")
    jump ch01_scene_28_ryan_leia_alone
