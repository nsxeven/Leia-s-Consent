# Leia's Consent — Chapter One: Something Different
# Playable production chunk: Scenes 7–13.
# Continues directly after Leia asks whether Julian saw anything during the towel incident.

label ch01_scene_07_did_he_see:

    $ enter_cinematic_mode()
    scene cg ch01_towel_did_he_see
    with dissolve

    $ ch01_towel_reassure_text = format_choice("ch01_towel_reassure", "He looked away pretty much immediately.")
    $ ch01_towel_honest_text = format_choice("ch01_towel_honest", "Maybe a little. You asked me to be honest.")
    $ ch01_towel_tease_text = format_choice("ch01_towel_tease", "Enough to know we should start using the curtains.")

    menu:
        "[ch01_towel_reassure_text]":
            $ apply_choice("ch01_towel_reassure")
            $ set_story_value("ch01_towel_followup", "reassured")
            mc "He looked away pretty much immediately."
            gf "That wasn't exactly what I asked."
            mc "I don't think he got much of a look."
            gf "...Okay."

        "[ch01_towel_honest_text]":
            $ apply_choice("ch01_towel_honest")
            $ set_story_value("ch01_towel_followup", "honest")
            mc "Maybe a little. You asked me to be honest."
            gf "[player_name]!"
            mc "What? You asked."
            gf "I was hoping you'd lie better."

        "[ch01_towel_tease_text]":
            $ apply_choice("ch01_towel_tease")
            $ set_story_value("ch01_towel_followup", "teased")
            mc "Enough to know we should start using the curtains."
            gf "Fuck you."
            mc "This is why honesty doesn't work in relationships."
            gf "You're enjoying this far too much."

    gf "I was standing in front of a floor-to-ceiling window. In a towel."
    mc "Accidentally."
    gf "I'm sure the distinction was very obvious from downstairs."

    mc "Seriously. He wasn't standing there staring. The moment he realised what was happening, he turned away."
    gf "He did?"
    mc "Yeah. Then he basically tried to pretend it never happened."

    "A beat passed behind the bathroom door."

    gf "Good."
    gf "Wait. Now I have to go downstairs."
    mc "You could fake your own death."
    gf "Would that get me out of dinner?"
    mc "Not after you've reminded us about the reservation fourteen times."

    gf "And don't tell him I asked."
    mc "I am not going downstairs and saying, 'By the way, Leia wants to know exactly how much of her you saw.'"
    gf "[player_name]."
    mc "Right. Not helping."

    $ exit_cinematic_mode()
    scene bg ch01_master_bedroom_curtains
    with dissolve

    "The bathroom door opened."

    $ grant_story_outfit("resort_dinner_dress", equip=True)
    $ set_story_value("ch01_dinner_bra_state", "sticky_bra_on")
    $ set_story_value("ch01_dinner_dress_state", "normal")
    with dissolve

    show leia_purple_dress neutral at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "She had changed into the dress she packed for dinner—elegant enough for the restaurant, fitted enough that I immediately forgot what I was about to say."

    gf "What?"
    mc "Nothing."
    gf "That was a very obvious something."
    mc "You look amazing."

    show leia_purple_dress smile
    with sprite_change
    gf "Better answer."

    scene bg ch01_villa_entry_day
    with dissolve
    show leia_purple_dress neutral at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "Julian was waiting near the door, looking at his phone with an intensity that suggested he had decided the screen was the safest place in the villa."

    with dissolve

    friend "Ready?"
    gf "Yeah."
    friend "Cool."

    "No grin. No comment. No attempt to make the situation funny."
    "Leia glanced at me. I gave her the smallest look I could manage: see?"

    gf "Julian?"
    friend "Yeah?"
    gf "Earlier..."

    friend "You don't have to explain anything."
    gf "I wasn't going to explain—"
    friend "Good. Then we're already on the same page."

    "His smile was smaller than usual. Not teasing. Just reassuring."

    friend "Bad timing. I looked away. That's it."
    gf "...Okay."
    friend "You really don't have to worry about it."

    gf "Thanks."
    friend "Of course."

    $ set_story_value("ch01_leia_julian_comfort", get_story_value("ch01_leia_julian_comfort", 0) + 1)
    $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)

    friend "Now can we go before we lose this reservation I've been hearing about all day?"
    gf "We are not losing it."
    mc "There she is."
    gf "Both of you. Shoes. Now."

    $ set_story_flag("ch01_scene_07_complete")


    jump ch01_scene_08_drive_to_dinner
