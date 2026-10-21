# Chapter 1 Scene 13 revision.
# Temporary source-level override while Scenes 7–13 are still in draft QA.
# Leia now remains asleep when the trio reaches the villa, so she never consciously
# chooses Julian to carry her. The existing carry CG placeholders are reused.

init 999 python:
    _ch01_scene13_previous_label_callback = config.label_callback

    def _ch01_scene13_label_callback(name, abnormal):
        if _ch01_scene13_previous_label_callback is not None:
            _ch01_scene13_previous_label_callback(name, abnormal)

        if name == "ch01_scene_13_back_at_villa":
            renpy.jump("ch01_scene_13_back_at_villa_asleep_revision")

    config.label_callback = _ch01_scene13_label_callback


label ch01_scene_13_back_at_villa_asleep_revision:

    scene bg ch01_villa_night
    with fade

    "When I parked, [girlfriend_name] didn't move."
    "She was still curled across the back seat, completely asleep."

    mc "[girlfriend_name]."
    "Nothing."
    mc "Babe. We're home."

    "She made a small sound, pulled herself tighter into the seat, and stayed asleep."

    friend "She's gone."
    mc "Helpful."

    "I opened the rear door and tried to lift her without waking her properly."
    "It lasted about three seconds. Sleeping [girlfriend_name] had somehow become twice as difficult to carry as awake [girlfriend_name]."

    friend "Want help?"
    mc "Yeah. I'll get the door."

    $ enter_cinematic_mode()
    scene cg ch01_julian_carry
    with dissolve

    "[friend_name] carefully slipped one arm behind her back and the other beneath her knees, lifting her into a proper princess carry."
    "[girlfriend_name] barely reacted. Her head settled against his shoulder and she kept sleeping."

    mc "Show-off."
    friend "She's dead weight. That's your problem, not mine."
    mc "Just don't drop her."
    friend "Open the door."

    "I walked ahead with the keys while [friend_name] followed more slowly."
    "Without the sticky bra beneath her dress, the neckline was less secure than it had been when we left the villa."

    scene cg ch01_carry_dress_shift
    with dissolve

    "As [girlfriend_name] relaxed against his supporting arm, the dress shifted lower on one side."
    "From where [friend_name] was carrying her, he could see the problem. With one arm behind her back and the other under her knees, he had no free hand to fix it without risking dropping her."

    friend "Uh... [player_name]?"
    mc "What?"
    friend "Her dress is slipping."

    "I turned. From my angle, [girlfriend_name]'s body and [friend_name]'s supporting arm hid whatever he could see. All I could tell was that [friend_name] looked deeply uncomfortable about having to announce it."

    $ exit_cinematic_mode()
    scene bg ch01_villa_night
    with dissolve

    $ ch01_carry_brush_text = format_choice("ch01_carry_brush", "We're almost inside. Just keep going.")
    $ ch01_carry_lookaway_text = format_choice("ch01_carry_lookaway", "Then keep your eyes off her and bring her inside.")
    $ ch01_carry_fix_text = format_choice("ch01_carry_fix", "Wait. Hold on—I'll fix it.")
    $ ch01_carry_joke_text = format_choice("ch01_carry_joke", "Careful. Don't enjoy the view too much.")

    menu:
        "[ch01_carry_brush_text]":
            $ apply_choice("ch01_carry_brush")
            $ set_story_value("ch01_carry_response", "brushed_off")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            $ set_story_value("ch01_leia_wake_reason", "voices_at_door")
            mc "We're almost inside. Just keep going."
            friend "Right. Just letting you know."
            "[friend_name] adjusted the angle of his supporting arm slightly, keeping [girlfriend_name] closer against him so the neckline would not shift any farther."

        "[ch01_carry_lookaway_text]":
            $ apply_choice("ch01_carry_lookaway")
            $ set_story_value("ch01_carry_response", "look_away")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) - 1)
            $ set_story_value("ch01_leia_wake_reason", "voices_at_door")
            mc "Then keep your eyes off her and bring her inside."
            friend "I'm not trying to look."
            mc "I know. Just saying."
            friend "Fair."

        "[ch01_carry_fix_text]":
            $ apply_choice("ch01_carry_fix")
            $ set_story_value("ch01_carry_response", "ryan_fixed")
            $ set_story_value("ch01_leia_wake_reason", "ryan_fixed_dress")
            mc "Wait. Hold on—I'll fix it."
            "I stepped back and carefully pulled the neckline securely into place."
            "The movement finally woke her. [girlfriend_name]'s eyes opened halfway."
            gf "Mm...?"
            mc "Hey. We're home."
            gf "Why am I moving?"
            friend "Long story."
            mc "You refused to wake up."
            gf "I was sleeping."
            mc "Exactly."
            friend "Can we finish this conversation inside?"
            gf "...Why are you carrying me?"
            friend "Because your boyfriend needed the keys."
            mc "And because you're apparently made of concrete when you're asleep."
            gf "Rude."

        "[ch01_carry_joke_text]":
            $ apply_choice("ch01_carry_joke")
            $ set_story_value("ch01_carry_response", "joked_about_view")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            $ set_story_value("ch01_leia_wake_reason", "voices_at_door")
            mc "Careful. Don't enjoy the view too much."
            friend "I hate this conversation."
            mc "You're the one who called me back."
            friend "Because I'm trying to be a good person. Open the door."

    "I unlocked the villa and held the door while [friend_name] carried her inside."

    if get_story_value("ch01_leia_wake_reason") == "voices_at_door":
        "The voices finally did what the drive home hadn't. [girlfriend_name] stirred against [friend_name]'s shoulder as we crossed the doorway."
        gf "Mm... we're home?"
        mc "Finally."
        gf "Why is [friend_name] carrying me?"
        friend "Because you wouldn't wake up."
        mc "I tried first. Sleeping you weighs approximately twice as much."
        gf "That's not how bodies work."
        friend "You weren't there."
        gf "I was literally there."
        mc "Not spiritually."

    scene bg ch01_villa_living_night
    with dissolve

    "[friend_name] lowered her onto the sofa. [girlfriend_name] sat there blinking for a second while her brain caught up with the room."

    friend "Your girlfriend is a logistical problem."
    mc "You volunteered."
    friend "A mistake I will reflect on privately."

    gf "I can hear both of you now."
    mc "Welcome back."
    gf "Barely."

    "[friend_name] laughed, gathered the bags from the doorway, and headed toward the kitchen."
    "The night had changed almost nothing—and, in a handful of small ways, more than any of us realised yet."

    $ set_story_flag("ch01_scene_13_complete")
    $ set_story_flag("ch01_scenes_07_13_complete")

    jump ch01_scene_13b_night_pool
