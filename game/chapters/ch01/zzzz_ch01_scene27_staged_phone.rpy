init 998 python:
    config.label_overrides["ch01_scene_27_late_photo_drop"] = "ch01_scene_27_late_photo_drop_staged"

    def ch01_offer_movie_photo_reply():
        # Wait for the existing staged group exchange to finish before offering
        # Ryan a turn; otherwise Leia's timed first response would auto-pick it.
        phone_offer_reply("group", "ch01_movie_photo_reply", [
            {"id": "nice", "text": "Okay, that one's good. Thanks for sending it.",
             "followups": [("julian", "Glad you like it. I almost forgot it was still on my phone.")]},
            {"id": "tease", "text": "You waited until after the movie to send this?",
             "followups": [("julian", "I know, I know. I only found it when I went to charge my phone.")]},
            {"id": "leia", "text": "I think [girlfriend_name] likes this one more than you do.",
             "followups": [("leia", "I do! Okay, I keep opening it again, I think you might be right.")]},
        ], "nice")

label ch01_scene_27_late_photo_drop_staged:
    "The movie had been over for several minutes before any of us bothered to stand."
    friend "I'm done. If I stay here another ten minutes I'm sleeping on this sofa."
    gf "Weak."
    friend "You fell asleep in a car."
    gf "That was tactical."
    "[friend_name] gathered his empty glass and headed toward the hallway."
    friend "Goodnight, children."
    mc "Goodnight, grandpa."
    gf "Night."

    $ lc_sfx("phone_notify")
    "A moment later my phone lit up."

    # Respect the pool-photo stop choice. The deleted solo capture must not
    # reappear disguised as an "unsent favourite"; the existing group selfie
    # is the only late photo on that path.
    $ ch01_late_group_only = get_story_value("ch01_photo_outcome") == "stopped"
    $ ch01_late_pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
    $ ch01_late_photo_asset = (
        ("ch01_photo_group_blue" if ch01_late_pool_outfit == "pool_bolder" else "ch01_photo_group_white")
        if ch01_late_group_only
        else ("ch01_photo_late_favourite_blue" if ch01_late_pool_outfit == "pool_bolder" else "ch01_photo_late_favourite_white")
    )
    python:
        phone_add_message(
            "group",
            "julian",
            text=("Almost forgot our first group selfie." if ch01_late_group_only else "Forgot this one. Photographer of the year strikes again."),
            message_id="ch01_trip_group_late_pool_photo",
            attachment_id=ch01_late_photo_asset,
            attachment_label=("First group selfie" if ch01_late_group_only else "Unsent pool favorite"),
            mark_unread=True,
            notify=True,
            notification_title="Trip Group",
        )
        set_story_value("ch01_late_pool_photo_asset", ch01_late_photo_asset)
        set_story_flag("ch01_late_pool_photo_shared")
        set_story_flag("ch01_late_photo_followup_pending")
        clear_story_flag("ch01_late_photo_phone_session_active")
        set_story_value("ch01_late_photo_followup_stage", 0)
        set_story_value("ch01_late_photo_force_complete_on_open", False)

    $ lc_sfx("phone_vibrate")
    "[girlfriend_name] glanced down when her own phone buzzed against the sofa cushion. Her thumbs started moving a second later."
    "Whatever she sent stayed in the Trip Group for me to discover on the Phone."

    $ set_story_flag("ch01_scene_27_complete")
    jump ch01_scene_28_ryan_leia_alone
