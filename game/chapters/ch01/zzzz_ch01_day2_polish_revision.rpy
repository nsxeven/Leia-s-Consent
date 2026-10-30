# Day Two presentation/continuity polish based on playtest feedback.

init 998 python:
    config.label_overrides["ch01_day2_scene_03_maya_message"] = "ch01_day2_scene_03_maya_message_v2"
    config.label_overrides["ch01_day2_scene_08_maya_julian"] = "ch01_day2_scene_08_maya_julian_v2"
    config.label_overrides["ch01_day2_scene_13_girls_upstairs"] = "ch01_day2_scene_13_girls_upstairs_v2"
    config.label_overrides["ch01_day2_scene_14_tie_foreshadow"] = "ch01_day2_scene_14_tie_foreshadow_v2"

    # Both Day One/Day Two pool options are two-piece tie bikinis. The bolder
    # version shows more skin; the classic version simply has more coverage.
    OUTFIT_DEFINITIONS["pool_conservative"]["name"] = "Classic Tie Bikini"
    OUTFIT_DEFINITIONS["pool_conservative"]["description"] = "A two-piece tie bikini with fuller coverage and a familiar, comfortable fit."
    OUTFIT_DEFINITIONS["pool_bolder"]["name"] = "Bolder Tie Bikini"
    OUTFIT_DEFINITIONS["pool_bolder"]["description"] = "A more revealing two-piece tie bikini with less coverage and a bolder resort cut."


label ch01_day2_scene_03_maya_message_v2:

    "My phone buzzed beside the coffee."

    python:
        phone_add_message(
            "maya",
            "maya",
            text="You people alive? I'm near the resort around lunch. Still meeting?",
            message_id="ch01_d2_maya_lunch_checkin",
            mark_unread=True,
            notify=True,
            notification_title="Maya",
        )

    "Maya's name appeared in the notification."
    "[girlfriend_name] saw it before I put the phone down."

    gf "Oh."
    mc "What?"
    gf "Nothing."
    friend "That was the loudest 'nothing' I've ever heard."

    $ set_story_flag("ch01_d2_maya_meetup_confirmed")
    jump ch01_day2_scene_04_jealousy_callback


label ch01_day2_scene_08_maya_julian_v2:

    "Maya's attention eventually shifted to [friend_name]."

    maya "So you're the rich one."
    friend "Apparently that's my entire personality now."
    maya "No, the sunglasses are your personality. The money is supporting cast."

    "[friend_name] laughed and shook his head. [girlfriend_name] leaned toward me."

    gf "They get along."
    mc "She insults people she likes."
    gf "That explains you."

    "A bee wandered close to the table."
    "[friend_name] stopped mid-sentence and leaned sharply away from it."

    maya "...Are you scared of bees?"
    friend "No."
    maya "You moved six inches without using your feet."
    friend "I respect bees. From a distance."
    gf "Oh my God."

    "The bee left. The information did not."

    $ set_story_flag("ch01_d2_julian_bee_fear_seeded")
    $ set_story_flag("ch01_d2_scene_08_complete")
    jump ch01_day2_scene_09_photo_walk


label ch01_day2_scene_13_girls_upstairs_v2:

    scene bg ch01_master_bedroom
    with dissolve

    "Upstairs, [girlfriend_name] laid both bikinis across the bed while Maya changed beside her."
    "Both were two-piece tie bikinis. The difference was coverage: one familiar and safer, the other cut noticeably smaller."

    maya "You brought options."
    gf "One is comfortable. One requires confidence."
    maya "Which one do you want to wear?"

    "Yesterday [girlfriend_name] had asked me that question. Today she had to answer it herself."

    if partner_stats["exhibitionism"] >= 22 or partner_stats["curiosity"] >= 27:
        $ set_story_value("ch01_d2_pool_outfit", "pool_bolder")
        gf "The smaller one."
        maya "Then wear the smaller one."
        gf "Very nuanced advice."
        maya "I charge by the hour."
    else:
        $ set_story_value("ch01_d2_pool_outfit", "pool_conservative")
        gf "I think the more covered one today."
        maya "Then that one."
        gf "You're surprisingly reasonable."
        maya "Don't spread that around."

    $ grant_story_outfit(get_story_value("ch01_d2_pool_outfit"), equip=True)
    $ set_story_flag("ch01_d2_scene_13_complete")
    jump ch01_day2_scene_14_tie_foreshadow


label ch01_day2_scene_14_tie_foreshadow_v2:

    if get_story_value("ch01_d2_pool_outfit") == "pool_bolder":
        "[girlfriend_name] changed into the bolder tie bikini while still talking to Maya, fastening the top with less attention than the knot deserved."
        maya "Double-knot that."
        gf "It's fine."
        maya "Famous last words."
        gf "It survived yesterday."
        maya "Yesterday you weren't distracted by my excellent conversation."
    else:
        "[girlfriend_name] changed into the more covered tie bikini while Maya borrowed the mirror and most of the counter space."
        "She tied the top while answering Maya, gave the knot one quick tug, and moved on."
        maya "Double-knot that."
        gf "This is the safe one."
        maya "A knot doesn't know that."
        gf "It's fine."

    # Either bikini can come loose during the later pool commotion. Route choice
    # changes how much skin it normally shows, not whether it uses ties.
    $ set_story_flag("ch01_d2_bikini_tie_loose")
    $ set_story_flag("ch01_d2_scene_14_complete")
    jump ch01_day2_scene_15_pool_group
