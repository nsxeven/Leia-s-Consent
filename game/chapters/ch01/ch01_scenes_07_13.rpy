# Leia's Consent — Chapter One: Something Different
# Playable production chunk: Scenes 7–13.
# Continues directly after Leia asks whether Julian saw anything during the towel incident.

label ch01_scene_07_did_he_see:

    scene bg ch01_master_bedroom_curtains
    with dissolve

    "I found her in the bathroom doorway, still half-turned toward the mirror, one hand pressed to her cheek."

    gf "[player_name]."
    mc "Yeah?"
    gf "Did he see?"

    $ enter_cinematic_mode()
    scene cg ch01_towel_did_he_see
    with dissolve

    "She watched my reflection instead of looking at me directly."

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
            gf "I was hoping you'd say no."

        "[ch01_towel_tease_text]":
            $ apply_choice("ch01_towel_tease")
            $ set_story_value("ch01_towel_followup", "teased")
            mc "Enough to know we should start using the curtains."
            gf "Fuck you."
            mc "That wasn't the reassurance I was aiming for."
            gf "You're enjoying this far too much."

    gf "I was standing in front of a floor-to-ceiling window. In a towel."
    mc "Accidentally."
    gf "I'm sure the distinction was very obvious from downstairs."

    mc "Seriously. He wasn't standing there staring. The moment he realised what was happening, he turned away."
    gf "He did?"
    mc "Yeah. Then he basically tried to pretend it never happened."

    "She stepped back into the bathroom and rested a hand against the half-open door. A beat passed."

    gf "Good."
    gf "Wait. Now I have to go downstairs."
    mc "You could fake your own death."
    gf "Would that get me out of dinner?"
    mc "Not after you've reminded us about the reservation fourteen times."

    gf "And don't tell him I asked."
    mc "I am not going downstairs and saying, 'By the way, [girlfriend_name] wants to know exactly how much of her you saw.'"
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

    "[friend_name] was waiting near the door, looking at his phone with an intensity that suggested he had decided the screen was the safest place in the villa."

    with dissolve

    friend "Ready?"
    gf "Yeah."
    friend "Cool."

    "No grin. No comment. No attempt to make the situation funny."
    "[girlfriend_name] glanced at me. I gave her the smallest look I could manage: see?"

    gf "[friend_name]?"
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


label ch01_scene_08_drive_to_dinner:

    $ set_story_value("ch01_default_car_seating", "ryan_driver_leia_front_julian_rear")

    $ enter_cinematic_mode()
    scene cg ch01_drive_to_dinner
    with dissolve

    "I drove. [girlfriend_name] took the passenger seat beside me without thinking about it, and [friend_name] climbed into the back."
    "It was our natural arrangement: [girlfriend_name] beside me, [friend_name] behind us, the two of them taking turns insulting my driving from different directions."

    gf "You know the speed limit applies on holiday too, right?"
    mc "I'm under it."
    friend "Technically true. Emotionally false."

    "[girlfriend_name] reached over and changed the song before the chorus."

    mc "I liked that one."
    gf "That's why I changed it."
    friend "For once, I'm with [girlfriend_name]."
    mc "Get out. Both of you."

    "She laughed and rested her hand on my thigh for a moment before turning the volume up."
    "Nothing about the drive felt unusual. That was what made the seating arrangement feel so ordinary—almost invisible."

    $ exit_cinematic_mode()

    scene bg ch01_car_day
    with dissolve

    gf "Okay, actual question. If we had to listen to one artist for the rest of this trip—"
    friend "No."
    gf "I haven't even said who."
    friend "Your question is already dangerous."

    "They immediately found something to disagree about, then somehow ended up taking the same side against me."
    "By the time the restaurant lights appeared ahead, the towel incident had disappeared beneath ordinary conversation."

    $ set_story_flag("ch01_driver_baseline_established")
    $ set_story_flag("ch01_scene_08_complete")


    jump ch01_scene_09_dinner


label ch01_scene_09_dinner:

    scene bg ch01_restaurant_evening
    with fade

    $ enter_cinematic_mode()
    scene cg ch01_dinner_arrival
    with dissolve

    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    show ryan_casual at prologue_other_enter_left, leia_body_idle
    show leia_purple_dress smile at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "Dinner started exactly the way I expected: [girlfriend_name] taking photos of the food, [friend_name] pretending to object, and me being ordered to move my glass out of every shot."

    gf "You're ruining the composition."
    mc "It's a glass of water."
    friend "Move it. Respect the artist."
    mc "You two became unbearable very quickly."

    "Somewhere between the starters and the main course, [friend_name] told her a story from university that I had heard at least twenty times."
    "[girlfriend_name] had not."

    gf "No. There is no way he actually said that to the lecturer."
    friend "Ask him."
    mc "I refuse to validate this story."
    gf "That means it's true."

    "She laughed hard enough to lean forward over the table, and [friend_name] laughed because she was laughing."
    "[girlfriend_name] lifted her phone and looked between the three of us."

    gf "We still don't have a proper dinner photo."
    friend "You have approximately four hundred photos from today."
    gf "Of food and the pool. I want one of us."
    mc "There are three of us. That's what selfies are for."
    hide ryan
    gf "No. I want one where nobody's arm looks six feet long."

    "She stood and glanced around for someone to ask."

    # Dry stranger approaches from screen-left (pre-spill sprite state).
    show stranger_casual_dry at ch01_stranger_approach_left, leia_body_idle
    pause 1.1

    "At exactly the wrong moment, a tall, broad-shouldered guest in fitted white shorts stepped past our table with a drink in one hand."

    # DinnerPhotoAsk_01 begins as the stranger enters Leia's path, before the
    # actual collision. Keep this beat on the CG; the dry sprite is retired here
    # and the wet sprite takes over after the impact CG.
    hide stranger_casual_dry
    $ enter_cinematic_mode()
    scene cg ch01_dinner_photo_ask
    with dissolve

    "[girlfriend_name] turned straight into him."

    scene cg ch01_dinner_spill_01
    with dissolve

    "The collision knocked his drink from its path, liquid hanging in the air for a split second before it came down across both of them."

    # The impact beat is over. Return to the restaurant for the immediate
    # apology using the post-spill wet sprite state.
    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    show stranger_casual_wet at ch01_stranger_collision_close, leia_body_idle
    show leia_purple_dress_wet flustered at ch01_leia_collision_close, leia_body_idle
    with sprite_enter_exit

    gf "Oh my God—I'm so sorry."
    stranger "No, that was me. Are you okay?"
    $ enter_cinematic_mode()
    scene cg ch01_dinner_spill_02
    with dissolve

    "The wet white fabric clung far more closely than it had a few seconds earlier, making his muscular build—and more than he probably intended—hard to miss."
    "[girlfriend_name] followed his glance downward."
    "For a beat, she forgot to look away."

    scene cg ch01_dinner_spill_03
    with dissolve

    "Then her eyes came back up."

    scene cg ch01_dinner_spill_04
    with dissolve

    "A second later they dipped again, quick enough that she might have hoped nobody noticed."

    # The look sequence is complete. Resume the same wet post-spill staging.
    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    show stranger_casual_wet at ch01_stranger_collision_close, leia_body_idle
    show leia_purple_dress_wet flustered at ch01_leia_collision_close, leia_body_idle
    with sprite_enter_exit

    # Ryan breaks the moment; both ease back to their normal dialogue slots.
    show stranger_casual_wet at ch01_stranger_collision_reset, leia_body_idle
    show leia_purple_dress_wet flustered at ch01_leia_collision_reset, leia_body_idle
    mc "[girlfriend_name]."
    gf "What?"
    mc "Your dress."

    "She looked down at herself and whatever she'd been thinking vanished immediately."
    "The front of her dress was soaked through."

    gf "Shit."
    stranger "Seriously, I'm sorry. Can I get you another drink? Or—"
    gf "No, no. It's okay. I walked into you."
    stranger "Then we're both terrible at walking."

    "That finally made her laugh. He apologized once more, accepted that nobody was injured, and continued toward his own table with considerably less dignity than he'd arrived with."

    # Give the narration a beat, then let him physically leave toward screen-left.
    show stranger_casual_wet at ch01_stranger_exit_left, leia_body_idle
    pause 1.9

    $ set_story_flag("ch01_dinner_stranger_collision")
    $ set_story_flag("ch01_leia_stranger_second_glance")

    hide stranger_casual_wet
    hide leia_purple_dress
    with sprite_enter_exit

    scene bg ch01_restaurant_evening
    with dissolve
    show ryan_casual at prologue_other_enter_left, leia_body_idle
    show leia_purple_dress_wet flustered at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "[friend_name] pushed the remaining napkins across the table without commenting on where [girlfriend_name] had been looking."
    friend "Successful photo mission?"
    show leia_purple_dress_wet angry
    with sprite_change
    gf "Not one word."
    mc "We didn't even get the photo."
    gf "I hate both of you."

    "Most of the drink came off the fabric. The problem was what had gotten underneath it."

    "A few minutes later, [girlfriend_name] leaned close to me while [friend_name] was distracted by the menu."

    show leia_purple_dress_wet flustered
    with sprite_change
    gf "Babe."
    mc "Mm?"
    gf "My sticky bra is literally giving up."
    mc "Giving up?"
    gf "As in one side is barely attached anymore. I think the drink got under it."
    gf "I might have to take it off."

    $ ch01_bra_reassure_text = format_choice("ch01_bra_reassure", "Do whatever makes you comfortable. You'll be fine.")
    $ ch01_bra_playful_text = format_choice("ch01_bra_playful", "If you're comfortable with it... that's kind of hot.")
    $ ch01_bra_cover_text = format_choice("ch01_bra_cover", "Take it off if you need to, but maybe keep your jacket nearby.")

    menu:
        "[ch01_bra_reassure_text]":
            $ apply_choice("ch01_bra_reassure")
            $ set_story_value("ch01_bra_response", "reassuring")
            mc "Do whatever makes you comfortable. You'll be fine."
            gf "You say that because you're not the one wearing adhesive underwear."
            mc "True. I remain tragically underqualified."

        "[ch01_bra_playful_text]":
            $ apply_choice("ch01_bra_playful")
            $ set_story_value("ch01_bra_response", "playful_open")
            mc "If you're comfortable with it... that's kind of hot."
            show leia_purple_dress_wet shy
            with sprite_change
            gf "[player_name]."
            mc "What? You asked."
            gf "I said my bra was falling off. I did not ask you to make it worse."
            mc "You smiled."
            gf "Shut up."

        "[ch01_bra_cover_text]":
            $ apply_choice("ch01_bra_cover")
            $ set_story_value("ch01_bra_response", "cautious")
            mc "Take it off if you need to, but maybe keep your jacket nearby."
            show leia_purple_dress_wet neutral
            with sprite_change
            gf "Fair. Let me fix this before it falls out on its own."

    gf "I'm going to the bathroom. If [friend_name] asks, I spilled a drink. That's all he needs to know."
    mc "Understood."

    "[girlfriend_name] disappeared toward the restroom with her handbag tucked under one arm."
    hide leia_purple_dress_wet
    with sprite_enter_exit

    # Canonical staging: Ryan remains LEFT. Leia is hidden while physically absent.
    # Julian may occupy RIGHT once a Julian sprite asset exists; do not substitute Ryan/Leia for him.
    $ set_story_value("ch01_dinner_bra_state", "removed_hidden_in_bag")
    $ set_story_value("ch01_dinner_dress_state", "post_spill_braless")
    $ set_story_flag("ch01_sticky_bra_removed")

    friend "She okay?"
    mc "Yeah. Wardrobe malfunction."
    friend "Do I want details?"
    mc "No."
    friend "Excellent."

    $ enter_cinematic_mode()
    scene cg ch01_dinner_restroom_return_01
    with dissolve

    "On her way back from the restroom, another man slowed as he passed her in the corridor."

    passerby "Excuse me—just had to say that dress looks incredible on you."

    "[girlfriend_name] blinked, caught off guard."
    gf "Oh. Thank you."

    "She gave a small, slightly flustered smile and kept walking."

    scene cg ch01_dinner_restroom_return_02
    with dissolve

    "By the time she was closer to the table the compliment still sat on her expression."
    "Without the adhesive bra underneath, the fabric sat more naturally against her chest and moved with her instead of holding a fixed shape."
    "Under the restaurant lighting, small changes in posture made the difference easier to notice than she probably realised."

    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    show leia_purple_dress_no_bra shy at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "She caught me looking."

    show leia_purple_dress_no_bra skeptical
    with sprite_change
    gf "Don't."
    mc "I didn't say anything."
    gf "Your face did."

    "[friend_name] looked between us, clearly aware that he had missed part of a conversation, and wisely chose not to ask."

    # The corridor compliment already happened; keep a light table-side beat so the
    # existing response menu still has a natural moment to fire.
    "A moment later the same man passed near our table and gave [girlfriend_name] another polite nod."
    gf "Oh—thank you again."

    $ ch01_stranger_proud_text = format_choice("ch01_stranger_proud", "Yeah. She looks incredible.")
    $ ch01_stranger_territorial_text = format_choice("ch01_stranger_territorial", "Thanks. We've got it from here.")
    $ ch01_stranger_encourage_text = format_choice("ch01_stranger_encourage", "See? Told you you had nothing to worry about.")

    menu:
        "[ch01_stranger_proud_text]":
            $ apply_choice("ch01_stranger_proud")
            $ set_story_value("ch01_stranger_response", "proud")
            mc "Yeah. She looks incredible."
            gf "Okay, you don't have to join in."
            mc "I agree with the man."
            gf "You're impossible."

        "[ch01_stranger_territorial_text]":
            $ apply_choice("ch01_stranger_territorial")
            $ set_story_value("ch01_stranger_response", "territorial")
            mc "Thanks. We've got it from here."
            gf "He was just being nice."
            mc "I know."

        "[ch01_stranger_encourage_text]":
            $ apply_choice("ch01_stranger_encourage")
            $ set_story_value("ch01_stranger_response", "encouraged_risk")
            mc "See? Told you you had nothing to worry about."
            gf "That is not what I was worried about."
            mc "Still looked good."
            gf "You're enjoying this."
            mc "Maybe a little."
            "Her cheeks coloured, but she did not reach for her jacket."

    "He kept walking. Nothing dramatic. [girlfriend_name] glanced down at herself and back at me."

    show leia_purple_dress_no_bra flustered
    with sprite_change
    gf "Why is everyone looking at me today?"
    mc "Today?"
    gf "What does that mean?"
    mc "You just normally don't notice."
    "She looked at me as if deciding whether that was a compliment or a problem."

    $ set_story_flag("ch01_scene_09_complete")

    jump ch01_scene_10_after_dinner_drinks


label ch01_scene_10_after_dinner_drinks:

    scene bg ch01_restaurant_bar
    with dissolve
    show ryan_casual at prologue_other_enter_left, leia_body_idle
    show leia_purple_dress_no_bra shy at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "We should have left after dessert. Instead, [friend_name] noticed the bar."

    friend "One drink."
    mc "For you two. I'm driving."
    show leia_purple_dress_no_bra smile
    with sprite_change
    gf "Responsible [player_name] is very attractive."
    friend "Responsible [player_name] is ruining my attempt to make this a group activity."
    mc "Someone has to get both of you home."

    "One drink became another for [girlfriend_name] and [friend_name]. I stayed with water and watched the two of them become progressively more entertained by things that were not remotely funny."

    gf "No, explain it again. Why did you think that haircut looked good?"
    friend "It was 2019. Nobody knew anything."
    mc "I told him. Repeatedly."
    friend "You had no vision."

    "[girlfriend_name] leaned into my shoulder while laughing, then pointed across the table at [friend_name]."

    gf "Show me the photo."
    friend "Absolutely not."
    gf "[player_name] has it, doesn't he?"
    mc "Several."
    friend "This friendship is over."

    "Whatever awkwardness had lingered over dinner seemed to fade as they traded stories."

    $ set_story_value("ch01_leia_buzz_state", "lightly_buzzed")
    $ set_story_value("ch01_leia_julian_comfort", get_story_value("ch01_leia_julian_comfort", 0) + 1)
    $ set_story_flag("ch01_scene_10_complete")

    gf "If we're going back, we need snacks."
    mc "Need?"
    gf "Need. And more drinks because you haven't had any yet."
    mc "I'm not drinking until we're back at the villa."
    friend "Then supply run."

    jump ch01_scene_11_walk_and_catch


label ch01_scene_11_walk_and_catch:

    scene bg ch01_island_walk_night
    with fade
    show ryan_casual at prologue_other_enter_left, leia_body_idle
    show leia_purple_dress_no_bra shy at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "The shop was only a short walk away. [girlfriend_name] still insisted on hooking both hands around my arm as though the pavement had become personally untrustworthy."

    show leia_purple_dress_no_bra pout
    with sprite_change
    gf "I'm not drunk."
    mc "Nobody said you were."
    friend "That statement usually means somebody is drunk."
    gf "Traitor."

    "My phone started ringing."
    "The name on the screen belonged to a female friend from back home—someone I had not expected to hear from on this trip."

    mc "Hang on."

    "I stopped. [girlfriend_name] and [friend_name] kept moving at an easy pace a few steps ahead while I answered."

    phone_friend "[player_name]? I just saw your posts. You're on the island too?"
    mc "Apparently. Since when are you here?"
    phone_friend "Yesterday. We should meet tomorrow if you're free."
    mc "Yeah, maybe. I'll text you."

    "Ahead of me, [girlfriend_name] turned around to check why I had stopped."
    "She tried to walk backward while doing it."

    $ enter_cinematic_mode()
    scene cg ch01_trip_catch
    with dissolve

    "Her heel caught the edge of the path."
    "[friend_name] reacted before I did, catching her around the waist and upper body before she hit the ground."
    "In the scramble, one of his hands landed against the side of her breast for a split second."
    "Both of them realised at almost exactly the same time."

    scene cg ch01_trip_catch_followup
    with dissolve

    mc "Maya, I'll call you back. [girlfriend_name] just tripped."
    phone_friend "Is she okay?"
    mc "Yeah. [friend_name] caught her. Talk tomorrow."
    phone_friend "Okay. Text me."
    "I ended the call and hurried toward them."

    gf "[friend_name]!"
    friend "I was catching you!"

    "[girlfriend_name]'s face went bright red. She smacked his shoulder with the back of her hand, more embarrassed than angry."

    gf "Watch your hands!"
    friend "I didn't exactly submit a landing plan!"
    gf "...Thank you for catching me."
    friend "You're welcome. Please walk forwards now."

    $ exit_cinematic_mode()
    scene bg ch01_island_walk_night
    with dissolve
    show ryan_casual at prologue_other_enter_left, leia_body_idle
    show leia_purple_dress_no_bra flustered at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "I had seen enough from the corner of my eye to understand why both of them suddenly looked awkward."

    $ ch01_catch_ignore_text = format_choice("ch01_catch_ignore", "Say nothing. It was obviously an accident.")
    $ ch01_catch_check_text = format_choice("ch01_catch_check", "You okay, babe?")
    $ ch01_catch_joke_text = format_choice("ch01_catch_joke", "Subtle, {}. Very subtle.".format(friend_name))
    $ ch01_catch_boundary_text = format_choice("ch01_catch_boundary", "Careful, mate.")

    menu:
        "[ch01_catch_ignore_text]":
            $ apply_choice("ch01_catch_ignore")
            $ set_story_value("ch01_catch_response", "ignored")
            "I let it go. [girlfriend_name] was upright, [friend_name] looked mortified, and there was nothing useful to add."

        "[ch01_catch_check_text]":
            $ apply_choice("ch01_catch_check")
            $ set_story_value("ch01_catch_response", "checked_leia")
            mc "You okay, babe?"
            gf "I'm fine. The floor attacked me."
            mc "Obviously."

        "[ch01_catch_joke_text]":
            $ apply_choice("ch01_catch_joke")
            $ set_story_value("ch01_catch_response", "joked")
            mc "Subtle, [friend_name]. Very subtle."
            friend "Fuck off."
            gf "[player_name]!"
            mc "Too soon?"
            gf "Yes."

        "[ch01_catch_boundary_text]":
            $ apply_choice("ch01_catch_boundary")
            $ set_story_value("ch01_catch_response", "boundary")
            mc "Careful, mate."
            friend "Yeah. I know. Sorry."
            gf "It was an accident."

    $ set_story_flag("ch01_accidental_catch_complete")
    $ set_story_flag("ch01_scene_11_complete")

    jump ch01_scene_11b_female_friend


label ch01_scene_11b_female_friend:

    scene bg ch01_island_walk_night
    show ryan_casual at prologue_other_enter_left, leia_body_idle
    show leia_purple_dress_no_bra skeptical at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    show leia_purple_dress_no_bra skeptical
    with sprite_change
    gf "Who was that?"
    mc "A friend from back home. She saw the posts and realised we're both here."
    gf "She?"

    "[friend_name] made a heroic attempt to become interested in a sign across the road."

    mc "Yes. She."
    gf "And she wants to meet you?"
    mc "Tomorrow, maybe."
    gf "How do you know her?"
    mc "We've been friends a while."
    gf "Have you ever dated?"
    mc "No. We've always been friends."

    friend "I'm going to walk slightly over there."
    gf "Nobody asked you."
    friend "Exactly why I'm leaving."

    "[girlfriend_name]'s tone was playful, but only just. The questions were real."

    $ ch01_friend_reassure_text = format_choice("ch01_friend_reassure", "She's just a friend. You've got nothing to worry about.")
    $ ch01_friend_tease_text = format_choice("ch01_friend_tease", "Wait. Are you jealous?")
    $ ch01_friend_boundary_text = format_choice("ch01_friend_boundary", "She's my friend. I don't want us policing who the other can see.")

    menu:
        "[ch01_friend_reassure_text]":
            $ apply_choice("ch01_friend_reassure")
            $ set_story_value("ch01_female_friend_response", "reassured")
            mc "She's just a friend. You've got nothing to worry about."
            gf "I wasn't worried."
            mc "You asked five questions in ten seconds."
            gf "I was gathering information."
            mc "Very calmly."
            gf "Exactly."

        "[ch01_friend_tease_text]":
            $ apply_choice("ch01_friend_tease")
            $ set_story_value("ch01_female_friend_response", "teased_jealousy")
            mc "Wait. Are you jealous?"
            gf "No."
            mc "That was fast."
            gf "I'm not jealous. I'm curious."
            friend "Those are famously different things."
            gf "[friend_name]."
            friend "Walking away again."

        "[ch01_friend_boundary_text]":
            $ apply_choice("ch01_friend_boundary")
            $ set_story_value("ch01_female_friend_response", "asserted_boundary")
            mc "She's my friend. I don't want us policing who the other can see."
            gf "I'm not saying you can't see her."
            mc "I know. I'm just saying I want us to trust each other about this stuff."
            "[girlfriend_name] held my gaze for a moment, then nodded."
            gf "Okay. That's fair."

    $ set_story_flag("ch01_female_friend_meetup_seeded")
    $ set_story_flag("ch01_scene_11b_complete")

    jump ch01_scene_12_shop_and_drive_back


label ch01_scene_12_shop_and_drive_back:

    scene bg ch01_shop_night
    with dissolve
    show ryan_casual at prologue_other_enter_left, leia_body_idle
    show leia_purple_dress_no_bra smile at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "The shop reset the mood almost immediately."
    "[girlfriend_name] filled the basket with snacks according to a system neither [friend_name] nor I understood, while [friend_name] contributed increasingly questionable bottles from the drinks aisle."

    show leia_purple_dress_no_bra skeptical
    with sprite_change
    gf "Put that back."
    friend "Why?"
    gf "Because the label has a skull on it."
    friend "That's branding."
    mc "That's a warning."

    "[girlfriend_name] dropped two bags of chips into the basket."

    friend "Those are terrible."
    gf "You booked a private villa and somehow still have the taste buds of a child."
    friend "Ask [player_name] what he ate after lectures."
    mc "Don't."
    gf "What did he eat?"
    friend "Instant noodles. Dry."
    gf "No."
    mc "Once."
    friend "For an entire semester."
    gf "[player_name]!"
    mc "We were students."
    gf "Water was free."

    "She was laughing hard enough that another shopper glanced over."

    mc "Fine. Ask him about the sunglasses phase."
    friend "There was no phase."
    mc "He wore them indoors."
    show leia_purple_dress_no_bra smile
    with sprite_change
    gf "Oh, I need photos."
    friend "You need a better boyfriend."
    gf "No, this one comes with useful historical records."

    "She bumped her shoulder lightly against mine and kept walking."

    friend "I regret introducing you two."
    gf "Four years too late."
    mc "Historically successful terrible dare, remember?"
    friend "I take it back."

    "By the time we paid, [girlfriend_name] was carrying exactly one packet of chips and acting as if she had personally completed the supply run."

    gf "I want to lie down."
    mc "We're walking thirty metres to the car."
    gf "Then I want to lie down in the car."

    $ set_story_value("ch01_return_car_seating", "ryan_driver_julian_front_leia_rear")

    $ enter_cinematic_mode()
    scene cg ch01_drive_back_seating
    with dissolve

    "[girlfriend_name] climbed into the rear seat so she could stretch out. [friend_name] took the front passenger seat beside me."
    "It was the first time that day our positions had changed: [friend_name] beside me, [girlfriend_name] behind us."

    gf "Wake me up when we're home."
    mc "We're ten minutes away."
    gf "Exactly. That's ten minutes of sleep."

    "Within a few minutes, her breathing had settled into the slow rhythm of somebody who had actually committed to the plan."

    $ exit_cinematic_mode()
    scene bg ch01_car_night
    with dissolve

    "The car became quiet enough that [friend_name] lowered his voice."

    friend "Hey. About earlier."
    mc "The fall?"
    friend "Yeah. I didn't mean to... you know."
    mc "I know."
    friend "I just don't want you thinking I was taking advantage of the situation."
    friend "She tripped. I caught her. My hand ended up where it shouldn't have. That's it."

    $ ch01_julian_reassure_text = format_choice("ch01_julian_reassure", "I know. Don't worry about it.")
    $ ch01_julian_honest_text = format_choice("ch01_julian_honest", "It bothered me for a second, but I know it was an accident.")
    $ ch01_julian_joke_text = format_choice("ch01_julian_joke", "Next time, catch her with less enthusiasm.")

    menu:
        "[ch01_julian_reassure_text]":
            $ apply_choice("ch01_julian_reassure")
            $ set_story_value("ch01_julian_apology_response", "trusted")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            mc "I know. Don't worry about it."
            friend "Good."
            mc "You looked more traumatised than she did."
            friend "Because I enjoy continuing to be alive."

        "[ch01_julian_honest_text]":
            $ apply_choice("ch01_julian_honest")
            $ set_story_value("ch01_julian_apology_response", "honest_discomfort")
            mc "It bothered me for a second, but I know it was an accident."
            friend "That's fair."
            mc "Just... be careful."
            friend "Of course."

        "[ch01_julian_joke_text]":
            $ apply_choice("ch01_julian_joke")
            $ set_story_value("ch01_julian_apology_response", "joked")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            mc "Next time, catch her with less enthusiasm."
            friend "Next time I'm letting gravity deal with her."
            mc "Please don't."
            friend "Fine. Professional catching only."

    "For a moment it was just the two of us again—the same easy friendship we'd had long before this trip."
    "Behind us, [girlfriend_name] shifted in her sleep and pulled her arms closer around herself."

    $ set_story_flag("ch01_scene_12_complete")


    jump ch01_scene_13_back_at_villa


label ch01_scene_13_back_at_villa:

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
    $ set_story_flag("ch01_scene_13_complete")
    $ set_story_flag("ch01_scenes_07_13_complete")

    jump ch01_scene_13b_night_pool
