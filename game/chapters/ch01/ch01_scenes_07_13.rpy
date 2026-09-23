# Leia's Consent — Chapter One: Something Different
# Playable production chunk: Scenes 7–13.
# Continues directly after Leia asks whether Julian saw anything during the towel incident.

label ch01_scene_07_did_he_see:

    scene bg ch01_master_bedroom_curtains

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

    "The bathroom door opened."

    $ grant_story_outfit("resort_dinner_dress", equip=True)
    $ set_story_value("ch01_dinner_bra_state", "sticky_bra_on")
    $ set_story_value("ch01_dinner_dress_state", "normal")
    $ set_leia_sprite("p03", "embarrassed")
    show leia at ch01_leia_left
    with dissolve

    "She had changed into the dress she packed for dinner—elegant enough for the restaurant, fitted enough that I immediately forgot what I was about to say."

    gf "What?"
    mc "Nothing."
    gf "That was a very obvious something."
    mc "You look amazing."

    $ set_leia_expression("smile")
    gf "Better answer."

    hide leia
    scene bg ch01_villa_entry_evening
    with dissolve

    "Julian was waiting near the door, looking at his phone with an intensity that suggested he had decided the screen was the safest place in the villa."

    show leia at ch01_leia_left
    $ set_leia_sprite("p03", "embarrassed")
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

    $ set_leia_expression("smile")
    gf "Thanks."
    friend "Of course."

    $ set_story_value("ch01_leia_julian_comfort", get_story_value("ch01_leia_julian_comfort", 0) + 1)
    $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)

    friend "Now can we go before we lose this reservation I've been hearing about all day?"
    gf "We are not losing it."
    mc "There she is."
    gf "Both of you. Shoes. Now."

    $ set_story_flag("ch01_scene_07_complete")

    hide leia

    jump ch01_scene_08_drive_to_dinner


label ch01_scene_08_drive_to_dinner:

    $ set_story_value("ch01_default_car_seating", "ryan_driver_leia_front_julian_rear")

    $ enter_cinematic_mode()
    scene cg ch01_drive_to_dinner
    with dissolve

    "I drove. Leia took the passenger seat beside me without thinking about it, and Julian climbed into the back."
    "It was our natural arrangement: Leia beside me, Julian behind us, the two of them taking turns insulting my driving from different directions."

    gf "You know the speed limit applies on holiday too, right?"
    mc "I'm under it."
    friend "Technically true. Emotionally false."

    "Leia reached over and changed the song before the chorus."

    mc "I liked that one."
    gf "That's why I changed it."
    friend "For once, I'm with Leia."
    mc "Get out. Both of you."

    "She laughed and rested her hand on my thigh for a moment before turning the volume up."
    "Nothing about the drive felt unusual. That was what made the seating arrangement feel so ordinary—almost invisible."

    $ exit_cinematic_mode()

    scene bg ch01_car_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p02", "smile")
    with dissolve

    gf "Okay, actual question. If we had to listen to one artist for the rest of this trip—"
    friend "No."
    gf "I haven't even said who."
    friend "Your question is already dangerous."

    "They immediately found something to disagree about, then somehow ended up taking the same side against me."
    "By the time the restaurant lights appeared ahead, the towel incident had disappeared beneath ordinary conversation."

    $ set_story_flag("ch01_driver_baseline_established")
    $ set_story_flag("ch01_scene_08_complete")

    hide leia

    jump ch01_scene_09_dinner


label ch01_scene_09_dinner:

    scene bg ch01_restaurant_evening
    show leia at ch01_leia_left
    $ set_leia_sprite("p02", "smile")
    with fade

    "Dinner started exactly the way I expected: Leia taking photos of the food, Julian pretending to object, and me being ordered to move my glass out of every shot."

    gf "You're ruining the composition."
    mc "It's a glass of water."
    friend "Move it. Respect the artist."
    mc "You two became unbearable very quickly."

    "Somewhere between the starters and the main course, Julian told her a story from university that I had heard at least twenty times."
    "Leia had not."

    gf "No. There is no way he actually said that to the lecturer."
    friend "Ask him."
    mc "I refuse to validate this story."
    gf "That means it's true."

    "She laughed hard enough to lean forward over the table, and Julian laughed because she was laughing."
    "There was nothing strange about it. If anything, I was glad they were finally getting comfortable around each other."

    "Then Leia reached for her drink while still looking at Julian."

    $ enter_cinematic_mode()
    hide leia
    scene cg ch01_dinner_spill
    with dissolve

    "Her fingers caught the glass badly. Cold liquid tipped across the front of her dress before any of us could stop it."

    gf "Oh, shit."
    friend "Napkins."
    mc "Here."

    "The three of us attacked the spill with enough napkins to alarm the waiter."
    "Most of the drink came off the fabric. The problem was what had gotten underneath it."

    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    show leia at ch01_leia_left
    $ set_leia_sprite("p03", "embarrassed")
    with dissolve

    "A few minutes later, Leia leaned close to me while Julian was distracted by the menu."

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
            $ set_leia_expression("embarrassed")
            gf "[player_name]."
            mc "What? You asked."
            gf "I said my bra was falling off. I did not ask you to make it worse."
            mc "You smiled."
            gf "Shut up."

        "[ch01_bra_cover_text]":
            $ apply_choice("ch01_bra_cover")
            $ set_story_value("ch01_bra_response", "cautious")
            mc "Take it off if you need to, but maybe keep your jacket nearby."
            gf "Fair. Let me fix this before it falls out on its own."

    gf "I'm going to the bathroom. If Julian asks, I spilled a drink. That's all he needs to know."
    mc "Understood."

    hide leia
    "Leia disappeared toward the restroom with her handbag tucked under one arm."

    $ set_story_value("ch01_dinner_bra_state", "removed_hidden_in_bag")
    $ set_story_value("ch01_dinner_dress_state", "post_spill_braless")
    $ set_story_flag("ch01_sticky_bra_removed")

    friend "She okay?"
    mc "Yeah. Wardrobe malfunction."
    friend "Do I want details?"
    mc "No."
    friend "Excellent."

    $ enter_cinematic_mode()
    scene cg ch01_dinner_return_braless
    with dissolve

    "When Leia came back, the dress looked almost the same. Almost."
    "Without the adhesive bra underneath, the fabric sat more naturally against her chest and moved with her instead of holding a fixed shape."
    "Under the restaurant lighting, small changes in posture made the difference easier to notice than she probably realised."

    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    show leia at ch01_leia_left
    $ set_leia_sprite("p02", "smile")
    with dissolve

    "She caught me looking."

    gf "Don't."
    mc "I didn't say anything."
    gf "Your face did."

    "Julian looked between us, clearly aware that he had missed part of a conversation, and wisely chose not to ask."

    "A little later, a man passing our table slowed just enough to smile at Leia."

    stranger "Sorry—just wanted to say your dress looks amazing on you."

    "Leia blinked, caught off guard."

    gf "Oh. Thank you."

    "He gave her a polite nod and kept walking. Nothing dramatic. Just enough attention to make Leia glance down at herself and then at me."

    $ ch01_stranger_proud_text = format_choice("ch01_stranger_proud", "Yeah. She looks incredible.")
    $ ch01_stranger_territorial_text = format_choice("ch01_stranger_territorial", "Thanks. We've got it from here.")
    $ ch01_stranger_encourage_text = format_choice("ch01_stranger_encourage", "See? Told you you had nothing to worry about.")

    menu:
        "[ch01_stranger_proud_text]":
            $ apply_choice("ch01_stranger_proud")
            $ set_story_value("ch01_stranger_response", "proud")
            mc "Yeah. She looks incredible."
            $ set_leia_expression("embarrassed")
            gf "Okay, you don't have to join in."
            mc "I agree with the man."
            gf "You're impossible."

        "[ch01_stranger_territorial_text]":
            $ apply_choice("ch01_stranger_territorial")
            $ set_story_value("ch01_stranger_response", "territorial")
            mc "Thanks. We've got it from here."
            "The stranger was already moving on, but Leia noticed my tone."
            gf "He was just being nice."
            mc "I know."

        "[ch01_stranger_encourage_text]":
            $ apply_choice("ch01_stranger_encourage")
            $ set_story_value("ch01_stranger_response", "encouraged_risk")
            mc "See? Told you you had nothing to worry about."
            $ set_leia_expression("embarrassed")
            gf "That is not what I was worried about."
            mc "Still looked good."
            gf "You're enjoying this."
            mc "Maybe a little."
            "Her cheeks coloured, but she did not reach for her jacket."

    $ set_story_flag("ch01_scene_09_complete")

    jump ch01_scene_10_after_dinner_drinks


label ch01_scene_10_after_dinner_drinks:

    scene bg ch01_restaurant_bar
    show leia at ch01_leia_left
    $ set_leia_sprite("p02", "smile")
    with dissolve

    "We should have left after dessert. Instead, Julian noticed the bar."

    friend "One drink."
    mc "For you two. I'm driving."
    gf "Responsible [player_name] is very attractive."
    friend "Responsible [player_name] is ruining my attempt to make this a group activity."
    mc "Someone has to get both of you home."

    "One drink became another for Leia and Julian. I stayed with water and watched the two of them become progressively more entertained by things that were not remotely funny."

    gf "No, explain it again. Why did you think that haircut looked good?"
    friend "It was 2019. Nobody knew anything."
    mc "I told him. Repeatedly."
    friend "You had no vision."

    "Leia leaned into my shoulder while laughing, then pointed across the table at Julian."

    gf "Show me the photo."
    friend "Absolutely not."
    gf "[player_name] has it, doesn't he?"
    mc "Several."
    friend "This friendship is over."

    "The alcohol did not transform anything between them. It simply removed some of the formality that had still been there earlier in the day."
    "Leia interrupted him more easily. Julian teased her without checking my reaction first. They were beginning to act like friends instead of two people connected through me."

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
    show leia at ch01_leia_left
    $ set_leia_sprite("p02", "smile")
    with fade

    "The shop was only a short walk away. Leia still insisted on hooking both hands around my arm as though the pavement had become personally untrustworthy."

    gf "I'm not drunk."
    mc "Nobody said you were."
    friend "That statement usually means somebody is drunk."
    gf "Traitor."

    "My phone started ringing."
    "The name on the screen belonged to a female friend from back home—someone I had not expected to hear from on this trip."

    mc "Hang on."

    "I stopped. Leia and Julian kept moving at an easy pace a few steps ahead while I answered."

    phone_friend "[player_name]? I just saw your posts. You're on the island too?"
    mc "Apparently. Since when are you here?"
    phone_friend "Yesterday. We should meet tomorrow if you're free."
    mc "Yeah, maybe. I'll text you."

    "Ahead of me, Leia turned around to check why I had stopped."
    "She tried to walk backward while doing it."

    $ enter_cinematic_mode()
    hide leia
    scene cg ch01_trip_catch
    with dissolve

    "Her heel caught the edge of the path."
    "Julian reacted before I did, catching her around the waist and upper body before she hit the ground."
    "In the scramble, one of his hands landed against the side of her breast for a split second."
    "Both of them realised at almost exactly the same time."

    gf "Julian!"
    friend "I was catching you!"

    "Leia's face went bright red. She smacked his shoulder with the back of her hand, more embarrassed than angry."

    gf "Watch your hands!"
    friend "I didn't exactly submit a landing plan!"
    gf "...Thank you for catching me."
    friend "You're welcome. Please walk forwards now."

    $ exit_cinematic_mode()
    scene bg ch01_island_walk_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p03", "embarrassed")
    with dissolve

    "I had seen enough from the corner of my eye to understand why both of them suddenly looked awkward."

    $ ch01_catch_ignore_text = format_choice("ch01_catch_ignore", "Say nothing. It was obviously an accident.")
    $ ch01_catch_check_text = format_choice("ch01_catch_check", "You okay, babe?")
    $ ch01_catch_joke_text = format_choice("ch01_catch_joke", "Subtle, Julian. Very subtle.")
    $ ch01_catch_boundary_text = format_choice("ch01_catch_boundary", "Careful, mate.")

    menu:
        "[ch01_catch_ignore_text]":
            $ apply_choice("ch01_catch_ignore")
            $ set_story_value("ch01_catch_response", "ignored")
            "I let it go. Leia was upright, Julian looked mortified, and there was nothing useful to add."

        "[ch01_catch_check_text]":
            $ apply_choice("ch01_catch_check")
            $ set_story_value("ch01_catch_response", "checked_leia")
            mc "You okay, babe?"
            gf "I'm fine. The floor attacked me."
            mc "Obviously."

        "[ch01_catch_joke_text]":
            $ apply_choice("ch01_catch_joke")
            $ set_story_value("ch01_catch_response", "joked")
            mc "Subtle, Julian. Very subtle."
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

    "I finished the call and caught up with them."

    jump ch01_scene_11b_female_friend


label ch01_scene_11b_female_friend:

    scene bg ch01_island_walk_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p02", "neutral")

    gf "Who was that?"
    mc "A friend from back home. She saw the posts and realised we're both here."
    gf "She?"

    "Julian made a heroic attempt to become interested in a sign across the road."

    mc "Yes. She."
    gf "And she wants to meet you?"
    mc "Tomorrow, maybe."
    gf "How do you know her?"
    mc "We've been friends a while."
    gf "Have you ever dated?"

    friend "I'm going to walk slightly over there."
    gf "Nobody asked you."
    friend "Exactly why I'm leaving."

    "Leia's tone was playful, but only just. The questions were real."

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
            $ set_leia_expression("embarrassed")
            gf "No."
            mc "That was fast."
            gf "I'm not jealous. I'm curious."
            friend "Those are famously different things."
            gf "Julian."
            friend "Walking away again."

        "[ch01_friend_boundary_text]":
            $ apply_choice("ch01_friend_boundary")
            $ set_story_value("ch01_female_friend_response", "asserted_boundary")
            mc "She's my friend. I don't want us policing who the other can see."
            gf "I'm not saying you can't see her."
            mc "I know. I'm just saying I want us to trust each other about this stuff."
            "Leia held my gaze for a moment, then nodded."
            gf "Okay. That's fair."

    $ set_story_flag("ch01_female_friend_meetup_seeded")
    $ set_story_flag("ch01_scene_11b_complete")

    jump ch01_scene_12_shop_and_drive_back


label ch01_scene_12_shop_and_drive_back:

    scene bg ch01_shop_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p02", "smile")
    with dissolve

    "The shop reset the mood almost immediately."
    "Leia filled the basket with snacks according to a system neither Julian nor I understood, while Julian contributed increasingly questionable bottles from the drinks aisle."

    gf "Put that back."
    friend "Why?"
    gf "Because the label has a skull on it."
    friend "That's branding."
    mc "That's a warning."

    "By the time we paid, Leia was carrying exactly one packet of chips and acting as if she had personally completed the supply run."

    gf "I want to lie down."
    mc "We're walking thirty metres to the car."
    gf "Then I want to lie down in the car."

    $ set_story_value("ch01_return_car_seating", "ryan_driver_julian_front_leia_rear")

    $ enter_cinematic_mode()
    scene cg ch01_drive_back_seating
    with dissolve

    "Leia climbed into the rear seat so she could stretch out. Julian took the front passenger seat beside me."
    "It was the first time that day our positions had changed: Julian beside me, Leia behind us."

    gf "Wake me up when we're home."
    mc "We're ten minutes away."
    gf "Exactly. That's ten minutes of sleep."

    "Within a few minutes, her breathing had settled into the slow rhythm of somebody who had actually committed to the plan."

    $ exit_cinematic_mode()
    scene bg ch01_car_night
    with dissolve

    "The car became quiet enough that Julian lowered his voice."

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
    "Behind us, Leia shifted in her sleep and pulled her arms closer around herself."

    $ set_story_flag("ch01_scene_12_complete")


    jump ch01_scene_13_back_at_villa


label ch01_scene_13_back_at_villa:

    scene bg ch01_villa_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p03", "neutral")
    with fade

    "Leia woke when I parked, but only technically."

    gf "We're home?"
    mc "We're home."
    gf "Carry me."
    mc "You can walk."
    gf "Counterpoint: no."

    "I tried anyway. She wrapped both arms around my neck while I attempted to lift her, and immediately started laughing when I had to put her back down."

    gf "Wow. Strong boyfriend."
    mc "You are actively making this harder."
    friend "Want help?"
    mc "Please. Before she destroys what remains of my dignity."

    $ enter_cinematic_mode()
    hide leia
    scene cg ch01_julian_carry
    with dissolve

    "Julian slipped one arm behind her back and the other beneath her knees, lifting her into a proper princess carry."

    gf "See? Easy."
    mc "I dislike both of you."
    friend "Open the door, hero."

    "I walked ahead with the keys while Julian followed more slowly."
    "Without the sticky bra beneath her dress, the neckline was less secure than it had been when we left the villa."

    scene cg ch01_carry_dress_shift
    with dissolve

    "As Leia relaxed against his arm, the dress shifted lower on one side."
    "From where Julian was carrying her, he could see the problem. With one arm supporting her back and the other under her knees, he had no free hand to fix it without risking dropping her."

    friend "Uh... [player_name]?"
    mc "What?"
    friend "Her dress is slipping."

    "I turned. From my angle, Leia's body and Julian's supporting arm hid whatever he could see. All I could tell was that Julian looked deeply uncomfortable about having to announce it."

    $ exit_cinematic_mode()
    scene bg ch01_villa_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p03", "neutral")
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
            mc "We're almost inside. Just keep going."
            friend "Right. Just letting you know."
            "Julian adjusted the angle of his supporting arm slightly, keeping Leia closer against him so the neckline would not shift any farther."

        "[ch01_carry_lookaway_text]":
            $ apply_choice("ch01_carry_lookaway")
            $ set_story_value("ch01_carry_response", "look_away")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) - 1)
            mc "Then keep your eyes off her and bring her inside."
            friend "I'm not trying to look."
            mc "I know. Just saying."
            friend "Fair."

        "[ch01_carry_fix_text]":
            $ apply_choice("ch01_carry_fix")
            $ set_story_value("ch01_carry_response", "ryan_fixed")
            mc "Wait. Hold on—I'll fix it."
            "I stepped back, pulled the neckline securely into place, and checked that the fabric would stay there."
            friend "Yeah. That's probably easier."
            mc "Good catch."

        "[ch01_carry_joke_text]":
            $ apply_choice("ch01_carry_joke")
            $ set_story_value("ch01_carry_response", "joked_about_view")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            mc "Careful. Don't enjoy the view too much."
            friend "I hate this conversation."
            mc "You're the one who called me back."
            friend "Because I'm trying to be a good person. Open the door."

    "I unlocked the villa and held the door while Julian carried her inside."

    scene bg ch01_villa_living_night
    with dissolve

    "Once Leia was safely on the sofa, Julian stepped away and exhaled as if he had just completed a much more dangerous journey than the walk from the car."

    friend "Your girlfriend is a logistical problem."
    mc "You volunteered."
    friend "A mistake I will reflect on privately."

    "Leia made a quiet sound from the sofa without opening her eyes."

    gf "I can hear both of you."
    mc "Apparently not asleep."
    gf "Barely alive."

    "Julian laughed, gathered the bags from the doorway, and headed toward the kitchen."
    "The night had changed almost nothing—and, in a handful of small ways, more than any of us realised yet."

    $ set_story_flag("ch01_scene_13_complete")
    $ set_story_flag("ch01_scenes_07_13_complete")

    scene black
    with fade

    centered "{size=46}CHAPTER ONE{/size}\n{size=30}Scenes 7–13 complete{/size}\n\n{size=22}Current development build ends here{/size}"

    return
