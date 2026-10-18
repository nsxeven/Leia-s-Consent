init 1001 python:
    config.label_overrides["ch01_scene_27_late_photo_drop"] = "ch01_scene_27_late_photo_drop_staged"

label ch01_scene_27_late_photo_drop_staged:
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
        set_story_flag("ch01_late_photo_followup_pending")
        clear_story_flag("ch01_late_photo_phone_session_active")
        set_story_value("ch01_late_photo_followup_stage", 0)
        set_story_value("ch01_late_photo_force_complete_on_open", False)

    "Leia glanced down when her own phone buzzed against the sofa cushion. Her thumbs started moving a second later."
    "Whatever she sent stayed in the Trip Group for me to discover on the Phone."

    $ set_story_flag("ch01_scene_27_complete")
    jump ch01_scene_28_ryan_leia_alone
