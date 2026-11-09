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

    $ enter_cinematic_mode()
    scene cg ch01_d2_breakfast_02
    with dissolve
    call screen lc_breakfast_julian_pov
    $ exit_cinematic_mode()
    scene bg ch01_d2_breakfast
    with dissolve

    "Maya's name appeared in the notification."
    "[girlfriend_name] saw it before I put the phone down."

    gf "Oh. Maya."
    mc "What? What's that face?"
    gf "Nothing! No face. That's just my face. It's a nice name."
    friend "That was the loudest 'nothing' I've ever heard, and I've known you two for four years."

    python:
        phone_offer_reply("maya", "ch01_d2_maya_lunch_reply", [
            {"id": "alive", "text": "Alive. Barely. Lunch works, I'll send you where we are.",
             "followups": [("maya", "Look at you, being organised 👍")]},
            {"id": "leia", "text": "[girlfriend_name] says hi.",
             "followups": [("maya", "Hi [girlfriend_name]! 👋")]},
            {"id": "buying", "text": "Depends. Are you buying?",
             "followups": [("maya", "In your dreams. See you at lunch.")]},
        ], "alive")

    $ set_story_flag("ch01_d2_maya_meetup_confirmed")
    jump ch01_day2_scene_04_jealousy_callback


label ch01_day2_scene_08_maya_julian_v2:

    "Maya's attention eventually shifted to [friend_name]."

    maya "So you're the rich one. [player_name] told me."
    friend "He— okay, wow. It's not really— it's more of a family thing. Can we talk about literally anything else?"
    maya "No, relax, the sunglasses are your personality. The money's just supporting cast."

    "[friend_name] went a little red, laughed, and shook his head. [girlfriend_name] leaned toward me."

    gf "They get along. Like, really get along."
    mc "She only insults people she likes."
    gf "That explains you."

    "A bee wandered close to the table."
    "[friend_name] stopped mid-sentence and leaned sharply away from it."

    maya "...Are you scared of bees?"
    friend "No. No. Is it gone? It's gone, right?"
    maya "You moved six inches without using your feet."
    friend "I respect bees. I just respect them from a reasonable distance. Is that a crime?"
    gf "Oh my God, you're actually scared of bees."

    "The bee left. The information did not."

    $ set_story_flag("ch01_d2_julian_bee_fear_seeded")
    $ set_story_flag("ch01_d2_scene_08_complete")
    jump ch01_day2_scene_09_photo_walk


label ch01_day2_scene_13_girls_upstairs_v2:

    scene bg ch01_master_bedroom
    with dissolve

    "Upstairs, [girlfriend_name] laid both bikinis across the bed while Maya changed beside her."
    "Both were two-piece tie bikinis. The difference was coverage: one familiar and safer, the other cut noticeably smaller."

    maya "Oh, you brought options. Okay, I see you."
    gf "One is comfortable, and one requires a lot of confidence. Like, a lot."
    maya "Okay, but which one do you want to wear? Not which one you should. Which one you want."

    "Yesterday [girlfriend_name] had asked me that question. Today she had to answer it herself."

    if lc_stat("exhibitionism") >= LC_T["d2_pool_outfit_bold"]:
        $ set_story_value("ch01_d2_pool_outfit", "pool_bolder")
        gf "The smaller one. I think. Yeah. The smaller one, before I talk myself out of it."
        maya "Then wear the smaller one."
        gf "That's it? That's your advice?"
        maya "That's it. You already knew. I just say it back to people, it's a whole service."
    else:
        $ set_story_value("ch01_d2_pool_outfit", "pool_conservative")
        gf "I think the more covered one today? Yesterday was a lot. I want a normal pool day."
        maya "Then that one. Normal pool day. Done."
        gf "Wait, that's it? You're surprisingly reasonable."
        maya "Don't spread that around. I have a reputation."

    $ grant_story_outfit(get_story_value("ch01_d2_pool_outfit"), equip=True)
    $ set_story_flag("ch01_d2_scene_13_complete")
    jump ch01_day2_scene_14_tie_foreshadow


label ch01_day2_scene_14_tie_foreshadow_v2:

    if get_story_value("ch01_d2_pool_outfit") == "pool_bolder":
        "[girlfriend_name] changed into the bolder tie bikini while still talking to Maya, fastening the top with less attention than the knot deserved."
        maya "Hey, double-knot that."
        gf "It's fine, it's a bikini, not a parachute."
        maya "Famous last words."
        gf "It's held up so far."
        maya "So far you haven't had me talking at you the whole time you tied it."
    else:
        "[girlfriend_name] changed into the more covered tie bikini while Maya borrowed the mirror and most of the counter space."
        "She tied the top while answering Maya, gave the knot one quick tug, and moved on."
        maya "Double-knot that, though."
        gf "This is the safe one! It's been to, like, three beaches."
        maya "A knot doesn't know that."
        gf "It's fine. I tugged it. Look, tugged."

    # Either bikini can come loose during the later pool commotion. Route choice
    # changes how much skin it normally shows, not whether it uses ties.
    $ set_story_flag("ch01_d2_bikini_tie_loose")
    $ set_story_flag("ch01_d2_scene_14_complete")
    jump ch01_day2_scene_15_pool_group
