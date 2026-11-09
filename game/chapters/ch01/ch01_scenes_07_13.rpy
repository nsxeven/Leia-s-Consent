# Leia's Consent — Chapter One: Something Different
# Playable production chunk: Scenes 7–13.
# Continues directly after Leia asks whether Julian saw anything during the towel incident.

label ch01_scene_07_did_he_see:

    scene bg ch01_master_bedroom_curtains
    with dissolve
    $ lc_amb("room_tone")
    $ lc_bgm("cozy_home")
    $ cast(ryan="pool", leia="towel", julian="pool")

    "I found her in the bathroom doorway, still half-turned toward the mirror, one hand pressed to her cheek."

    gf "[player_name]? Come here a sec."
    mc "Yeah? What's up?"
    gf "Did he see? Like, actually see. Don't give me the nice-boyfriend version."

    $ enter_cinematic_mode()
    scene cg ch01_towel_did_he_see
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    "She watched my reflection instead of looking at me directly."

    $ ch01_towel_reassure_text = format_choice("ch01_towel_reassure", "He looked away pretty much immediately.")
    $ ch01_towel_honest_text = format_choice("ch01_towel_honest", "Maybe a little. You asked me to be honest.")
    $ ch01_towel_tease_text = format_choice("ch01_towel_tease", "Enough to know we should start using the curtains.")
    $ ch01_towel_shrug_text = format_choice("ch01_towel_shrug", "It was like a second. It's not a big deal.")

    menu:
        "[ch01_towel_reassure_text]":
            $ apply_choice("ch01_towel_reassure")
            $ set_story_value("ch01_towel_followup", "reassured")
            mc "He looked away pretty much immediately."
            gf "That's not what I asked, though. I asked if he saw, not how fast he looked away."
            mc "I really don't think he got much of a look. It was like a second."
            gf "A second. Okay. I can live with a second. I think."

        "[ch01_towel_honest_text]":
            $ apply_choice("ch01_towel_honest")
            $ set_story_value("ch01_towel_followup", "honest")
            mc "Maybe a little. You asked me to be honest."
            gf "[player_name]! I know I said be honest, but you could've lied a little."
            mc "You told me not to do the nice version!"
            gf "I was hoping the not-nice version would also be no."

        "[ch01_towel_tease_text]":
            $ apply_choice("ch01_towel_tease")
            $ set_story_value("ch01_towel_followup", "teased")
            mc "Enough to know we should start using the curtains."
            gf "Fuck you. That's not— okay, it's a little funny. It's not funny."
            mc "Sorry. That sounded better in my head."
            gf "You're enjoying this way too much, and I'm having a crisis here."

        "[ch01_towel_shrug_text]":
            $ apply_choice("ch01_towel_shrug")
            $ set_story_value("ch01_towel_followup", "brushed_off")
            mc "It was like a second, babe. It's not a big deal."
            gf "It's a big deal to me. Kind of. A little bit."
            mc "Yeah. No, I know. Sorry."
            "She went back to watching my reflection instead of me."

    gf "I was standing in front of a giant glass door in a towel, yelling about dinner. Who does that?"
    mc "It was an accident, though. You were just trying to hurry us up."
    gf "Oh, I'm sure that was super clear from downstairs."

    mc "Seriously. He wasn't standing there staring. The moment he realized what was happening, he turned away."
    gf "Wait, he did? Like, right away?"
    mc "Right away. Then he stared at the pool like he'd never seen water before."

    "She stepped back into the bathroom and leaned on the half-open door, thinking about it."

    gf "Good. That's... yeah. Good."
    gf "Wait, no, now I have to go downstairs and sit across from him at dinner like nothing happened."
    mc "You could fake your own death."
    gf "Would that get me out of dinner? Because I'm kind of considering it."
    mc "Not after you've reminded us about the reservation fourteen times."

    gf "And don't tell him I asked. Seriously. Don't make it a thing."
    mc "I am not going downstairs and saying, 'By the way, [girlfriend_name] wants to know exactly how much of her you saw.'"
    gf "[player_name], I swear to God."
    mc "Sorry. Yeah. Not helping. Got it."

    $ exit_cinematic_mode()
    scene bg ch01_master_bedroom_curtains
    with dissolve
    $ cast(ryan="casual", julian="pool")

    $ lc_sfx("door_open")
    "The bathroom door opened."

    $ grant_story_outfit("resort_dinner_dress", equip=True)
    $ set_story_value("ch01_dinner_bra_state", "sticky_bra_on")
    $ set_story_value("ch01_dinner_dress_state", "normal")

    # Dress reveal CG holds through her first exchange; sprites return at the door.
    $ enter_cinematic_mode()
    scene cg ch01_dress_reveal at lc_push_in
    with dissolve
    $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)

    "She had changed into the dress she packed for dinner—elegant enough for the restaurant, fitted enough that I immediately forgot what I was about to say."

    gf "What? Why are you looking at me like that? Is it too much?"
    mc "No. I just... forgot what I was going to say."
    gf "That's a weird answer. Is that a good weird answer?"
    mc "You look amazing. That's the answer."
    gf "See, you should've led with that."

    $ exit_cinematic_mode()
    # Dressed for dinner from here on (darryn): Julian's swim shorts are pool-only.
    scene bg ch01_villa_entry_day
    with dissolve
    $ lc_amb("villa_day")
    $ lc_bgm("sunny_island")
    $ cast(ryan="casual", leia="purple_dress", julian="evening")

    "[friend_name] was waiting near the door, looking at his phone with an intensity that suggested he had decided the screen was the safest place in the villa."

    with dissolve

    friend "Hey. You guys ready? I already started the car so the seats don't cook us."
    gf "Yeah."
    friend "Cool."

    "He didn't make a single joke, which from him was somehow louder than any joke would have been."
    "[girlfriend_name] glanced at me. I gave her the smallest look I could manage: see?"

    gf "[friend_name]?"
    friend "Yeah?"
    gf "About earlier, on the balcony. I just—"

    friend "Hey, no, you don't have to explain anything. It's fine."
    gf "I wasn't going to explain, I was going to— okay, I don't know what I was going to do."
    friend "Then we're good. That's the whole conversation. We can just be done with it."

    "His smile was smaller than usual, the kind you give somebody to let them off the hook."

    friend "It was bad timing, I looked at the pool, and the pool and I had a really nice moment together. That's all that happened."
    gf "You and the pool had a moment."
    friend "A really special one. You don't have to worry about it, seriously."

    gf "Thanks, [friend_name]. Really."
    friend "Of course. It's already gone, I've forgotten the whole thing."

    $ set_story_value("ch01_leia_julian_comfort", get_story_value("ch01_leia_julian_comfort", 0) + 1)
    $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)

    friend "Now can we go before we lose this reservation I've been hearing about all day?"
    gf "We're not going to lose it, I called them twice."
    mc "We're only late because somebody said \"two minutes\" about an hour ago."
    gf "I'm ignoring that. Both of you, shoes, now, we're leaving."

    $ set_story_flag("ch01_scene_07_complete")


    jump ch01_scene_08_drive_to_dinner


label ch01_scene_08_drive_to_dinner:

    $ set_story_value("ch01_default_car_seating", "ryan_driver_leia_front_julian_rear")

    $ enter_cinematic_mode()
    scene cg ch01_drive_to_dinner
    with dissolve
    $ lc_amb("car_day")
    $ lc_bgm("sunny_island")

    "I drove. [girlfriend_name] took the passenger seat beside me without thinking about it, and [friend_name] climbed into the back."
    "It was our natural arrangement: [girlfriend_name] beside me, [friend_name] behind us, the two of them taking turns insulting my driving from different directions."

    gf "You know the speed limit applies on holiday too, right?"
    mc "I'm under it! I'm like two under it."
    friend "You're under it now because she said something. Thirty seconds ago you were not under it."

    $ lc_sfx("radio_static")
    "[girlfriend_name] reached over and changed the song before the chorus."

    mc "Hey, I liked that one."
    gf "I know, that's why I changed it. You've played it like six times since we landed."
    friend "Sorry, man, I'm with her on this one. I know all the words now, and I didn't want to know them."
    mc "You can both walk to dinner."

    $ lc_sfx("leia_laugh")
    "She laughed and rested her hand on my thigh for a moment before turning the volume up."
    "None of us thought twice about who sat where. It was just how we'd always done it."

    $ exit_cinematic_mode()

    scene bg ch01_car_day
    with dissolve
    $ cast(ryan="casual", leia="purple_dress", julian="evening")

    gf "Okay, actual question. If we had to listen to one artist for the rest of this trip—"
    friend "No. I already know where this is going, and the answer's no."
    gf "I haven't even said who! You don't know who I was going to say."
    friend "It's the boy band. It's always the boy band. You did this on the way to the airport."

    "They immediately found something to disagree about, then somehow ended up taking the same side against me."
    "By the time the restaurant lights appeared ahead, the towel incident had disappeared beneath ordinary conversation."

    $ set_story_flag("ch01_driver_baseline_established")
    $ set_story_flag("ch01_scene_08_complete")


    jump ch01_scene_09_dinner


label ch01_scene_09_dinner:

    # Arrival opens on the DinnerArrival CG (travel = fade) and holds it for
    # its own lines; it used to flash past with no text (added in ce959ce).
    $ cast()
    $ enter_cinematic_mode()
    scene cg ch01_dinner_arrival
    with fade
    $ lc_amb("restaurant")  # darryn's restaurant recording, a little lower (LC_AUDIO_GAIN)
    $ lc_bgm("lounge_piano")

    "The restaurant gave us a table out on the terrace, close enough to the water that we could hear it under the piano."
    "The food came out faster than any of us expected. [girlfriend_name] ended up with her chin in both hands, listening to [friend_name] explain why he'd ordered the one dish he couldn't pronounce."
    friend "In my defense, the waiter looked really proud of it, and I didn't want to point at something else and hurt his feelings. So if it's bad, that's on me."
    gf "That's the nicest dumb reason anyone's ever had for ordering food."

    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    $ cast(ryan="casual", leia="purple_dress", julian="evening")
    $ face("leia", "smile")

    "After that, dinner went exactly the way I expected: [girlfriend_name] taking photos of every new plate, [friend_name] pretending to object, and me being ordered to move my glass out of every shot."

    gf "Babe, move your glass. You're ruining the composition."
    mc "It's a glass of water. People drink water at dinner."
    friend "Just move it, man. She's been lining this up since the bread came."
    mc "When did you two start teaming up on me? That was fast."

    "Somewhere between the starters and the main course, [friend_name] told her a story from college that I had heard at least twenty times."
    "[girlfriend_name] had not."

    gf "No. No way. There's no way he actually said that to a professor, to his face."
    friend "Ask him! He was there, he was sitting right next to me. Ask him."
    mc "I'm not getting involved in this story."
    gf "That means it's true! Oh my God, it's true."

    $ lc_sfx("leia_laugh")
    "She laughed hard enough to lean forward over the table, and [friend_name] laughed because she was laughing."
    "[girlfriend_name] lifted her phone and looked between the three of us."

    gf "We still don't have a proper dinner photo."
    friend "You've taken like four hundred photos today, though. I watched you do it."
    gf "Of food and the pool. I want one of us."
    mc "There are three of us. That's what selfies are for."
    # Ryan steps out of frame before the stranger enters from the left.
    $ cast_remove("ryan")
    gf "No. I want one where nobody's arm looks six feet long."

    "She stood and glanced around for someone to ask."

    # Hand-choreographed collision: automatic staging pauses until cast_resume.
    $ cast_hold()
    # Dry stranger approaches from screen-left (pre-spill sprite state).
    show stranger_casual_dry at ch01_stranger_approach_left, leia_body_idle
    pause 1.1

    "At exactly the wrong moment, a tall, broad-shouldered guest in fitted white shorts stepped past our table with a drink in one hand."

    # DinnerPhotoAsk_01 begins as the stranger enters Leia's path, before the
    # actual collision. Keep this beat on the CG; the dry sprite is retired here
    # and the wet sprite takes over after the impact CG.
    $ enter_cinematic_mode()
    scene cg ch01_dinner_photo_ask
    with dissolve

    # First collision (DinnerPhotoAsk): shake + darryn's thump.
    $ lc_sfx("thump")
    "[girlfriend_name] turned straight into him." with lc_shake("m")

    scene cg ch01_dinner_spill_01
    with dissolve

    # Impact beat: screen shake on the collision line (same as the prologue dare).
    $ lc_sfx("body_bump")
    $ lc_sfx("drink_spill")
    "The collision knocked his drink from its path, liquid hanging in the air for a split second before it came down across both of them." with lc_shake("m")

    $ lc_sfx_loop("dripping")  # darryn: drips through the post-collision conversation
    # The impact beat is over. Return to the restaurant for the immediate
    # apology using the post-spill wet sprite state.
    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    show stranger_casual_wet at ch01_stranger_collision_close, leia_body_idle
    show leia_purple_dress_wet flustered at ch01_leia_collision_close, leia_body_idle
    with sprite_enter_exit

    $ lc_sfx("leia_gasp")  # shock right after the spill
    gf "Oh my God—I'm so sorry."
    stranger "No, that was me. Are you okay?"
    $ enter_cinematic_mode()
    scene cg ch01_dinner_spill_02
    with dissolve

    "The wet white fabric clung far more closely than it had a few seconds earlier, making his muscular build—and more than he probably intended—hard to miss."
    "[girlfriend_name] followed his glance downward."
    "For a second, she forgot to look away."

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
    mc "[girlfriend_name]. Babe."
    gf "What? What's wrong?"
    mc "Your dress. Look down."

    "She looked down at herself and whatever she'd been thinking vanished immediately."
    "The front of her dress was soaked through."

    gf "Oh no. Shit. This is going to stain."
    stranger "Seriously, I'm sorry. Can I get you another drink? Or— you were looking for someone to take a photo, right? I could do it. Least I can do."
    "[girlfriend_name]'s phone was still in her hand. She looked down at it, then up at him, and for a second she didn't answer."
    $ lc_duck(0.5)
    think "It's a photo. It's literally just a photo. Why is she taking so long?"
    "Her thumb was already on the screen when she glanced down at the front of her dress, still dripping onto the terrace."
    $ lc_unduck()
    gf "No, no, it's okay. I'm literally dripping, I'm not taking a photo like this. And I walked into you, so that one's on me."
    stranger "Then we're both terrible at walking."

    $ lc_sfx("leia_laugh")
    "That finally made her laugh. He apologized once more, accepted that nobody was injured, and continued toward his own table with considerably less dignity than he'd arrived with."

    # Give the narration a beat, then let him physically leave toward screen-left.
    show stranger_casual_wet at ch01_stranger_exit_left, leia_body_idle
    pause 1.9

    $ set_story_flag("ch01_dinner_stranger_collision")
    $ set_story_flag("ch01_leia_stranger_second_glance")

    # The stranger has walked off-screen; Ryan steps back in on the left while
    # Leia stays in her slot (no scene reset, which made her blink).
    hide stranger_casual_wet
    $ cast(ryan="casual", leia="purple_dress_wet", julian="evening")
    $ face("leia", "flustered")
    # Leia's hand-placed sprite becomes her normal right slot (same spot, no blink).
    $ cast_resume(leia="leia_purple_dress_wet")

    "[friend_name] pushed a stack of napkins across the table without commenting on where [girlfriend_name] had been looking."
    friend "So, uh. How'd the photo go?"
    $ face("leia", "angry")
    gf "Don't. Not one word, I mean it."
    mc "We didn't even get the photo."
    $ lc_sfx("leia_angry_laugh")
    gf "I hate both of you so much right now."

    "Most of the drink came off the fabric. The problem was what had gotten underneath it."

    "A few minutes later, [girlfriend_name] leaned close to me while [friend_name] was distracted by the menu."

    # The lean-in CG lands on her first whispered line, not on the narration.
    $ enter_cinematic_mode()
    scene cg ch01_dinner_sticky_bra
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    gf "Babe. Babe, come here."
    mc "Mm? What's up?"
    gf "My sticky bra is literally giving up."
    mc "Giving up how? What does that mean?"
    gf "As in one side is barely attached anymore. I think the drink got under it."
    gf "I think I have to take it off. In the bathroom. Is that insane?"

    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    $ cast(ryan="casual", leia="purple_dress_wet", julian="evening")
    $ face("leia", "flustered")

    $ ch01_bra_reassure_text = format_choice("ch01_bra_reassure", "Do whatever makes you comfortable. You'll be fine.")
    $ ch01_bra_playful_text = format_choice("ch01_bra_playful", "If you're comfortable with it... that's kind of hot.")
    $ ch01_bra_cover_text = format_choice("ch01_bra_cover", "Take it off if you need to. I'll keep an eye out.")
    $ ch01_bra_distracted_text = format_choice("ch01_bra_distracted", "Hm? Yeah, go for it.")

    menu:
        "[ch01_bra_reassure_text]":
            $ apply_choice("ch01_bra_reassure")
            $ set_story_value("ch01_bra_response", "reassuring")
            mc "Do whatever makes you comfortable. You'll be fine."
            gf "You say that because you're not the one wearing adhesive underwear."
            mc "That's true. I know nothing about adhesive underwear."

        "[ch01_bra_playful_text]":
            $ apply_choice("ch01_bra_playful")
            $ set_story_value("ch01_bra_response", "playful_open")
            mc "If you're comfortable with it... that's kind of hot."
            $ face("leia", "shy")
            gf "[player_name]! We're in a restaurant."
            mc "What? You asked what I thought."
            gf "I said my bra was falling off. I did not ask you to make it worse."
            mc "You're smiling, though."
            gf "Shut up. This is my stressed face."

        "[ch01_bra_cover_text]":
            $ apply_choice("ch01_bra_cover")
            $ set_story_value("ch01_bra_response", "cautious")
            mc "Take it off if you need to. I'll keep an eye out."
            $ face("leia", "neutral")
            gf "Thank you. Let me go fix this before it falls off on its own."

        "[ch01_bra_distracted_text]":
            $ apply_choice("ch01_bra_distracted")
            $ set_story_value("ch01_bra_response", "distracted")
            mc "Hm? Yeah, go for it."
            "I said it to the menu. I was still trying to work out what half the dishes were."
            $ face("leia", "skeptical")
            gf "Wow. Thanks for the support."
            mc "Sorry. No, yeah, go. You'll be fine."

    gf "I'm going to the bathroom. If [friend_name] asks, I spilled a drink. That's all he needs to know."
    mc "Spilled a drink. Got it."

    "[girlfriend_name] disappeared toward the restroom with her handbag tucked under one arm."
    $ lc_sfx_loop_stop(1.5)
    $ cast_remove("leia")

    # Canonical staging: Ryan remains LEFT. Leia is hidden while physically absent.
    # Julian may occupy RIGHT once a Julian sprite asset exists; do not substitute Ryan/Leia for him.
    $ set_story_value("ch01_dinner_bra_state", "removed_hidden_in_bag")
    $ set_story_value("ch01_dinner_dress_state", "post_spill_braless")
    $ set_story_flag("ch01_sticky_bra_removed")

    friend "Is she okay? She kind of ran."
    mc "She's fine. Just a wardrobe thing, from the drink."
    friend "Okay. Is this a thing where I want details, or a thing where I really don't want details?"
    mc "You really don't."
    friend "Great. Perfect. I'm going to go look at the dessert menu, then."

    $ enter_cinematic_mode()
    scene cg ch01_dinner_restroom_return_01
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    "On her way back from the restroom, another man slowed as he passed her in the corridor."

    $ lc_sfx("cat_call")  # darryn: as the passerby compliments her
    passerby "Excuse me—just had to say that dress looks incredible on you."

    "[girlfriend_name] blinked, caught off guard."
    gf "Oh! Um. Thank you. That's really nice."

    "She gave a small, slightly flustered smile and kept walking."

    scene cg ch01_dinner_restroom_return_02
    with dissolve

    "By the time she got back to the table, she was still half-smiling about it."
    "Without the adhesive bra underneath, the fabric sat more naturally against her chest and moved with her instead of holding a fixed shape."
    "Under the restaurant lighting, small changes in posture made the difference easier to notice than she probably realized."

    $ exit_cinematic_mode()
    scene bg ch01_restaurant_evening
    with dissolve
    $ cast(ryan="casual", leia="purple_dress_no_bra", julian="evening")
    $ face("leia", "shy")

    "She caught me looking."

    $ face("leia", "skeptical")
    # Day One echo E7: the bra answer (scene 8).
    if get_story_value("ch01_bra_response") == "distracted":
        gf "Oh, now you're paying attention."
        mc "I was paying attention before."
        gf "You told the menu to go for it, babe. I watched you."
    else:
        if get_story_value("ch01_bra_response") == "playful_open":
            gf "Don't. You already said 'kind of hot' once tonight, you don't get another one."
        else:
            gf "Don't. I can see you thinking it."
        mc "I didn't say anything."
        gf "You didn't have to. Your face is saying it really loudly."

    "[friend_name] looked between us, clearly aware that he had missed part of a conversation, and wisely chose not to ask."

    # The corridor compliment already happened; keep a light table-side beat so the
    # existing response menu still has a natural moment to fire.
    "A moment later the same man passed near our table and gave [girlfriend_name] another polite nod."
    passerby "Still stands, by the way."
    gf "Oh—thank you again."

    $ ch01_stranger_proud_text = format_choice("ch01_stranger_proud", "Yeah. She looks incredible.")
    $ ch01_stranger_territorial_text = format_choice("ch01_stranger_territorial", "Thanks. We've got it from here.")
    $ ch01_stranger_encourage_text = format_choice("ch01_stranger_encourage", "See? Told you you had nothing to worry about.")

    menu:
        "[ch01_stranger_proud_text]":
            $ apply_choice("ch01_stranger_proud")
            $ set_story_value("ch01_stranger_response", "proud")
            mc "Yeah. She looks incredible."
            gf "Babe, you don't have to join in. Now there's two of you."
            mc "What? He's right. I agree with the man."
            gf "You're impossible, you know that?"

        "[ch01_stranger_territorial_text]":
            $ apply_choice("ch01_stranger_territorial")
            $ set_story_value("ch01_stranger_response", "territorial")
            mc "Thanks. We've got it from here."
            gf "He was just being nice."
            mc "I know. I just... I know."

        "[ch01_stranger_encourage_text]":
            $ apply_choice("ch01_stranger_encourage")
            $ set_story_value("ch01_stranger_response", "encouraged_risk")
            mc "See? Told you you had nothing to worry about."
            gf "That is not what I was worried about."
            mc "You still look really good, though. That part's true."
            gf "You're enjoying this, aren't you? A little bit."
            mc "Maybe a little."
            "Her cheeks colored, but she did not cover up."

    "He kept walking. Nothing dramatic. [girlfriend_name] glanced down at herself and back at me."

    $ face("leia", "flustered")
    gf "Why is everyone looking at me today?"
    mc "Wait, today?"
    gf "What's that supposed to mean?"
    mc "People look at you all the time. You just don't usually notice."
    "She looked at me as if deciding whether that was a compliment or a problem."

    $ set_story_flag("ch01_scene_09_complete")

    jump ch01_scene_10_after_dinner_drinks


label ch01_scene_10_after_dinner_drinks:

    scene bg ch01_restaurant_bar
    with dissolve
    $ lc_bgm("lounge_piano")  # BGM plan: the lounge piano carries on at the bar
    $ lc_amb("restaurant")  # darryn's restaurant recording, a little lower (LC_AUDIO_GAIN)
    $ cast(ryan="casual", leia="purple_dress_no_bra", julian="evening")
    $ face("leia", "shy")

    "We should have left after dessert. Instead, [friend_name] noticed the bar."

    $ lc_sfx("glass_clink")
    friend "Okay, hear me out. One drink. Just one, at the bar, and then we go."
    mc "For you two. I'm driving."
    $ face("leia", "smile")
    gf "Responsible [player_name] is very attractive."
    friend "Responsible [player_name] is ruining my attempt to make this a group activity."
    mc "Someone has to get both of you home."

    "One drink became another for [girlfriend_name] and [friend_name]. I stayed with water and watched the two of them become progressively more entertained by things that were not remotely funny."

    gf "No, explain it again. Why did you think that haircut looked good?"
    friend "It was 2019. Nobody knew anything."
    mc "I told him. I told him so many times."
    friend "You did, and I didn't listen, and that one's on me. I'll own that."

    $ lc_sfx("leia_laugh")
    "[girlfriend_name] leaned into my shoulder while laughing, then pointed across the table at [friend_name]."

    gf "Wait, there's a photo? Show me the photo."
    friend "No. Absolutely not. I've worked really hard to make sure that photo doesn't exist."
    gf "[player_name] has it, doesn't he?"
    mc "I have a few. There's a folder."
    friend "You kept a folder? Of my haircut? That's actually so mean."

    "Whatever awkwardness had lingered over dinner seemed to fade as they traded stories."

    $ set_story_value("ch01_leia_buzz_state", "lightly_buzzed")
    $ set_story_value("ch01_leia_julian_comfort", get_story_value("ch01_leia_julian_comfort", 0) + 1)
    $ set_story_flag("ch01_scene_10_complete")

    gf "If we're going back, we need snacks."
    mc "We need snacks?"
    gf "Need. And more drinks because you haven't had any yet."
    mc "I'm not drinking until we're back at the villa."
    friend "There's a shop on the way back to the car. We could just walk over and grab stuff."

    jump ch01_scene_11_walk_and_catch


label ch01_scene_11_walk_and_catch:

    $ enter_cinematic_mode()
    scene cg ch01_walk_back_01
    with fade
    $ lc_amb("street_night")
    $ lc_bgm("warm_night")

    "The shop was only a short walk away. [girlfriend_name] still insisted on hooking both hands around my arm as though the pavement had become personally untrustworthy."

    gf "I'm not drunk, for the record. I'm just holding on."
    mc "Nobody said you were."
    friend "That statement usually means somebody is drunk."
    gf "Whose side are you even on? You're supposed to be on my side."

    scene cg ch01_walk_back_call
    with dissolve

    $ lc_duck(0.35)  # music dips for the call
    $ lc_sfx_loop("phone_ring", fadein=0.0)  # darryn's ringtone, rings until Ryan answers
    "My phone started ringing." with lc_shake("s")
    "The name on the screen belonged to a female friend from back home—someone I had not expected to hear from on this trip."

    $ lc_sfx_loop_stop(0.25)
    $ lc_unduck()
    mc "Hang on, sorry. Two seconds."

    "I stopped. [girlfriend_name] and [friend_name] kept moving at an easy pace a few steps ahead while I answered."

    phone_friend "[player_name]? I just saw your posts. You're on the island too?"
    mc "Apparently. Since when are you here?"
    phone_friend "Yesterday. We should meet tomorrow if you're free."
    mc "Yeah, maybe. I'll text you."

    "Ahead of me, [girlfriend_name] turned around to check why I had stopped."
    "She tried to walk backward while doing it."

    scene cg ch01_trip_catch
    with dissolve

    $ lc_sfx("stumble")
    $ lc_sfx("leia_gasp")  # darryn: she gasps as she trips, before the catch
    "Her heel caught the edge of the path." with lc_shake("m")
    $ lc_sfx("catch_thud")
    "[friend_name] reacted before I did, catching her around the waist and upper body before she hit the ground."
    "In the scramble, one of his hands landed against the side of her breast for a split second."
    "Both of them realized at almost exactly the same time."

    scene cg ch01_trip_catch_followup
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    mc "Maya, I'll call you back. [girlfriend_name] just tripped."
    phone_friend "Is she okay?"
    mc "Yeah. [friend_name] caught her. Talk tomorrow."
    phone_friend "Go, go. Text me later."
    "I ended the call and hurried toward them."

    scene cg ch01_trip_catch_aftermath
    with dissolve

    gf "[friend_name]!"
    friend "I was catching you!"

    $ lc_sfx("slap_light")
    "[girlfriend_name]'s face went bright red. She smacked his shoulder with the back of her hand, more embarrassed than angry." with lc_shake("s")

    gf "Watch your hands, oh my God!"
    friend "I didn't exactly submit a landing plan!"
    gf "...Thank you for catching me."
    friend "You're welcome. Could you maybe walk forwards for the rest of the night? For me?"

    $ exit_cinematic_mode()
    scene bg ch01_island_walk_night
    with dissolve
    $ cast(ryan="casual", leia="purple_dress_no_bra", julian="evening")
    $ face("leia", "flustered")

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
            gf "I'm fine. The path just came out of nowhere."
            mc "You were walking backwards, babe."

        "[ch01_catch_joke_text]":
            $ apply_choice("ch01_catch_joke")
            $ set_story_value("ch01_catch_response", "joked")
            mc "Subtle, [friend_name]. Very subtle."
            friend "Dude. Come on, that's not— fuck off."
            gf "[player_name]!"
            mc "What? I— okay. Yeah. Not the time."
            gf "Not the time! He literally just saved my life."

        "[ch01_catch_boundary_text]":
            $ apply_choice("ch01_catch_boundary")
            $ set_story_value("ch01_catch_response", "boundary")
            mc "Careful, mate."
            friend "Yeah. I know. Sorry."
            gf "Babe, it was an accident. He was catching me."

    $ set_story_flag("ch01_accidental_catch_complete")
    $ set_story_flag("ch01_scene_11_complete")

    jump ch01_scene_11b_female_friend


label ch01_scene_11b_female_friend:

    # Continues straight from scene 11 on the same path; Ryan and Leia are
    # already on screen, so no scene reset (it made both sprites blink).
    $ lc_amb("street_night")
    $ lc_bgm("warm_night")
    $ face("leia", "skeptical")
    gf "So who was that? On the phone."
    mc "A friend from back home. She saw the posts and realized we're both here."
    gf "She?"

    "[friend_name] made a heroic attempt to become interested in a sign across the road."

    mc "Yes. She. Why'd you say it like that?"
    gf "I didn't say it like anything. And she wants to meet you?"
    mc "Tomorrow, maybe. If we're not busy."
    gf "And how do you know her? From where?"
    mc "From back home. We've been friends for ages. It's not a big thing."
    gf "Have you two ever, like... dated?"
    mc "No! No. We've always just been friends."

    friend "I'm going to go stand slightly over there. Away from this."
    gf "Nobody asked you, [friend_name]."
    friend "I know! That's why I'm leaving!"

    "[girlfriend_name]'s tone was playful, but only just. The questions were real."

    $ ch01_friend_reassure_text = format_choice("ch01_friend_reassure", "She's just a friend. You've got nothing to worry about.")
    $ ch01_friend_tease_text = format_choice("ch01_friend_tease", "Wait. Are you jealous?")
    $ ch01_friend_boundary_text = format_choice("ch01_friend_boundary", "She's my friend. I don't want us checking up on each other.")

    menu:
        "[ch01_friend_reassure_text]":
            $ apply_choice("ch01_friend_reassure")
            $ set_story_value("ch01_female_friend_response", "reassured")
            mc "She's just a friend. You've got nothing to worry about."
            $ lc_sfx("leia_grunt")
            gf "I wasn't worried. Who said I was worried?"
            mc "You asked five questions in ten seconds."
            gf "I was gathering information! That's different. You'd have, like, eleven questions if some guy from back home called me."
            mc "Very calmly."
            gf "Yes. Calm and thorough. Thank you for noticing."

        "[ch01_friend_tease_text]":
            $ apply_choice("ch01_friend_tease")
            $ set_story_value("ch01_female_friend_response", "teased_jealousy")
            mc "Wait. Are you jealous?"
            gf "No! No. Why would I be jealous?"
            mc "You answered that really fast."
            gf "I'm not jealous. I'm curious."
            friend "Those are famously different things."
            gf "[friend_name], I swear."
            friend "Yep. Walking away again. Bye."

        "[ch01_friend_boundary_text]":
            $ apply_choice("ch01_friend_boundary")
            $ set_story_value("ch01_female_friend_response", "asserted_boundary")
            mc "I mean... she's my friend. I don't want us turning into the couple that checks up on each other."
            gf "I wasn't checking up on you. I was just asking."
            mc "I know. I'm just saying I want us to trust each other about this stuff."
            "[girlfriend_name] looked at me for a second, then down at the path."
            gf "Yeah, no, that's... fair. I guess."
            "She said it lightly, but she let go of my hand to fix her strap and didn't take it back right away."

    $ set_story_flag("ch01_female_friend_meetup_seeded")
    $ set_story_flag("ch01_scene_11b_complete")

    jump ch01_scene_12_shop_and_drive_back


label ch01_scene_12_shop_and_drive_back:

    scene bg ch01_shop_night
    with dissolve
    $ lc_amb("shop")
    $ lc_bgm("warm_night")
    $ cast(ryan="casual", leia="purple_dress_no_bra", julian="evening")
    $ face("leia", "smile")

    $ lc_sfx("shop_bell")
    "The shop reset the mood almost immediately."
    "[girlfriend_name] filled the basket with snacks according to a system neither [friend_name] nor I understood, while [friend_name] contributed increasingly questionable bottles from the drinks aisle."

    $ face("leia", "skeptical")
    gf "No. Put that back."
    friend "What? Why? It looked fun."
    gf "Because the label has a skull on it."
    friend "That's just branding. It's like a pirate thing."
    mc "I'm pretty sure that's a warning, man."

    $ lc_sfx("chips_rustle")
    "[girlfriend_name] dropped two bags of chips into the basket."

    friend "Oh no, not those. Those are terrible, they taste like a candle."
    gf "You booked a private villa and somehow still have the taste buds of a child."
    friend "That has nothing to do with the— can we not? Ask [player_name] what he ate in college."
    mc "Don't. Don't do this."
    gf "What did he eat?"
    friend "Instant noodles. Dry. Straight out of the packet, he'd just crunch on them."
    gf "No. No way."
    mc "It was one time."
    friend "It was an entire semester. Every single night."
    gf "[player_name]!"
    mc "We were broke! We were students!"
    gf "You had a kettle! Water was free!"

    $ lc_sfx("leia_laugh")
    "She was laughing hard enough that another shopper glanced over."

    mc "Okay, fine. Ask him about the sunglasses phase."
    friend "There was no phase. I don't know what he's talking about."
    mc "He wore them indoors. For like a year."
    $ face("leia", "smile")
    gf "Oh, I need photos of that. I need to see that."
    friend "You need a better boyfriend."
    gf "No, this one comes with useful historical records."

    "She bumped her shoulder lightly against mine and kept walking."

    friend "I regret ever daring you two. I want that on the record."
    gf "Well, that's four years too late."
    mc "This afternoon you wanted a plaque for it."
    friend "I take the plaque back. I don't want the plaque anymore."

    $ lc_sfx("register_beep")
    "By the time we paid, [girlfriend_name] was carrying exactly one packet of chips and acting as if she had personally completed the supply run."

    gf "I want to lie down. Right now. Here, on the floor."
    mc "We're walking thirty meters to the car."
    gf "Then I want to lie down in the car."

    $ set_story_value("ch01_return_car_seating", "ryan_driver_julian_front_leia_rear")

    $ enter_cinematic_mode()
    scene cg ch01_drive_back_seating
    with dissolve
    $ lc_amb("car_night")

    "[girlfriend_name] climbed into the rear seat so she could stretch out. [friend_name] took the front passenger seat beside me."
    "It was the first time that day our positions had changed: [friend_name] beside me, [girlfriend_name] behind us."

    gf "Wake me up when we're home."
    mc "We're ten minutes away."
    gf "So that's ten minutes of sleep. Shh."

    "Within a few minutes, her breathing had settled into the slow rhythm of somebody who had actually committed to the plan."

    $ exit_cinematic_mode()
    # Leia is asleep in the back with no lines, so Julian takes the right slot
    # for the whole car talk (darryn). No swap here: Ryan stays left.
    # Night car interior for the drive home (darryn's explicit choice; overrides the evening-art default).
    scene bg ch01_car_night
    with dissolve
    $ cast(ryan="casual", julian="evening")

    "The car became quiet enough that [friend_name] lowered his voice."

    friend "Hey. Can I say something about earlier?"
    mc "What, the trip thing?"
    friend "Yeah. I just— I didn't mean to, you know. Grab anything. I was trying to stop her from hitting the ground."
    mc "Yeah, I know, man."
    friend "I just don't want you thinking I was taking advantage of the situation."
    friend "She tripped. I caught her. My hand ended up where it shouldn't have. That's it."

    $ ch01_julian_reassure_text = format_choice("ch01_julian_reassure", "I know. Don't worry about it.")
    $ ch01_julian_honest_text = format_choice("ch01_julian_honest", "It bothered me for a second, but I know it was an accident.")
    $ ch01_julian_joke_text = format_choice("ch01_julian_joke", "Next time, catch her with less enthusiasm.")
    $ ch01_julian_fine_text = format_choice("ch01_julian_fine", "Yeah. It's fine.")

    menu:
        "[ch01_julian_reassure_text]":
            $ apply_choice("ch01_julian_reassure")
            $ set_story_value("ch01_julian_apology_response", "trusted")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            mc "I know. Don't worry about it."
            friend "Good. Thanks, man. I've been weird about it this whole drive."
            mc "You looked more traumatized than she did."
            friend "Because she yelled 'watch your hands' at me in the middle of the path, man. I'm going to hear that in my sleep."

        "[ch01_julian_honest_text]":
            $ apply_choice("ch01_julian_honest")
            $ set_story_value("ch01_julian_apology_response", "honest_discomfort")
            mc "It bothered me for a second, but I know it was an accident."
            friend "That's fair. I'd probably feel the same."
            mc "Just... be careful."
            friend "Of course. Yeah. I will."

        "[ch01_julian_joke_text]":
            $ apply_choice("ch01_julian_joke")
            $ set_story_value("ch01_julian_apology_response", "joked")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            mc "Next time, catch her with less enthusiasm."
            friend "Next time I'm letting gravity deal with her."
            mc "Please don't drop my girlfriend on a sidewalk."
            friend "Fine. I'll still catch her, but really professionally. Like a fireman."

        "[ch01_julian_fine_text]":
            $ apply_choice("ch01_julian_fine")
            $ set_story_value("ch01_julian_apology_response", "said_fine")
            mc "Yeah. It's fine."
            friend "You sure? Because that's your 'it's fine' voice, and I've known that voice since college."
            mc "It's fine, man. Honestly."
            "It wasn't, really. I just didn't want to be the guy who made it a thing."
            friend "Okay. If you say so."

    "For a moment it was just the two of us again—the same easy friendship we'd had long before this trip."
    "Behind us, [girlfriend_name] shifted in her sleep and pulled her arms closer around herself."

    $ set_story_flag("ch01_scene_12_complete")


    jump ch01_scene_13_back_at_villa


label ch01_scene_13_back_at_villa:

    # Leia is asleep (in the car, then carried) and has no sprite, so Julian
    # stands in the right slot with Ryan on the left until they reach the sofa
    # (darryn). No swap here; it resumes when Leia's sprite returns.
    scene bg ch01_villa_entry_evening
    with fade
    $ lc_amb("night_pool")
    $ lc_bgm("warm_night")
    $ cast(ryan="casual", julian="evening")

    "When I parked, [girlfriend_name] didn't move."
    "She was still curled across the back seat, completely asleep."

    mc "[girlfriend_name]? Hey."
    "Nothing."
    mc "Babe. We're home."

    "She made a small sound, pulled herself tighter into the seat, and stayed asleep."

    friend "She's gone, man. She's not waking up."
    mc "Thanks, man. I can see that."

    $ lc_sfx("car_door")
    "I opened the rear door and tried to lift her without waking her properly."
    "It lasted about three seconds. Sleeping [girlfriend_name] had somehow become twice as difficult to carry as awake [girlfriend_name]."

    friend "Do you want me to take her? I don't mind."
    mc "Yeah, okay. I'll get the door."

    $ enter_cinematic_mode()
    scene cg ch01_julian_carry
    with dissolve

    "[friend_name] carefully slipped one arm behind her back and the other beneath her knees, lifting her into a proper princess carry."
    "[girlfriend_name] barely reacted. Her head settled against his shoulder and she kept sleeping."

    mc "Oh, come on. You just picked her up like it was nothing."
    friend "You were lifting her wrong, man. You've got to get under the knees."
    mc "Just don't drop her."
    friend "I'm not going to drop her. Just open the door."

    scene cg ch01_carry_walk
    with dissolve

    $ lc_sfx("keys")
    "I walked ahead with the keys while [friend_name] followed more slowly."
    "Without the sticky bra beneath her dress, the neckline was less secure than it had been when we left the villa."

    scene cg ch01_carry_dress_shift
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    "As [girlfriend_name] relaxed against his supporting arm, the dress shifted lower on one side."
    "From where [friend_name] was carrying her, he could see the problem. With one arm behind her back and the other under her knees, he had no free hand to fix it without risking dropping her."

    friend "Uh... [player_name]?"
    mc "What? What's wrong?"
    friend "Her dress is, uh. It's slipping. On the side. I can't fix it."

    "I turned. From my angle, [girlfriend_name]'s body and [friend_name]'s supporting arm hid whatever he could see. All I could tell was that [friend_name] looked deeply uncomfortable about having to announce it."

    $ exit_cinematic_mode()
    # Still at the door with Leia asleep: Ryan left, Julian right (no swap).
    scene bg ch01_villa_entry_evening
    with dissolve
    $ cast(ryan="casual", julian="evening")

    $ ch01_carry_brush_text = format_choice("ch01_carry_brush", "We're almost inside. Just keep going.")
    $ ch01_carry_lookaway_text = format_choice("ch01_carry_lookaway", "Just— don't look. Get her inside.")
    $ ch01_carry_fix_text = format_choice("ch01_carry_fix", "Wait. Hold on—I'll fix it.")
    $ ch01_carry_joke_text = format_choice("ch01_carry_joke", "Careful. Don't enjoy the view too much.")

    menu:
        "[ch01_carry_brush_text]":
            $ apply_choice("ch01_carry_brush")
            $ set_story_value("ch01_carry_response", "brushed_off")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            $ set_story_value("ch01_leia_wake_reason", "voices_at_door")
            mc "We're almost inside. Just keep going."
            friend "Right. Yeah. I just didn't want you to think I didn't say anything."
            "[friend_name] adjusted the angle of his supporting arm slightly, keeping [girlfriend_name] closer against him so the neckline would not shift any farther."

        "[ch01_carry_lookaway_text]":
            $ apply_choice("ch01_carry_lookaway")
            $ set_story_value("ch01_carry_response", "look_away")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) - 1)
            $ set_story_value("ch01_leia_wake_reason", "voices_at_door")
            mc "Just— don't look. Get her inside."
            friend "I'm not trying to look, I swear. That's why I told you."
            mc "I know. Sorry. I know."
            friend "Yeah, no, I get it. Door. I'm looking at the door."

        "[ch01_carry_fix_text]":
            $ apply_choice("ch01_carry_fix")
            $ set_story_value("ch01_carry_response", "ryan_fixed")
            $ set_story_value("ch01_leia_wake_reason", "ryan_fixed_dress")
            mc "Wait. Hold on—I'll fix it."
            "I stepped back and carefully pulled the neckline securely into place."
            "The movement finally woke her. [girlfriend_name]'s eyes opened halfway."
            gf "Mm...?"
            mc "Hey. Hey, we're home."
            gf "Why am I... why is everything moving?"
            friend "It's kind of a long story. You fell asleep."
            mc "You wouldn't wake up. I tried."
            gf "Because I was sleeping. That's what sleeping is."
            mc "That's kind of my point."
            friend "Can we finish this conversation inside?"
            gf "...Why are you carrying me?"
            friend "Because your boyfriend needed the keys."
            mc "And because you're apparently made of concrete when you're asleep."
            gf "Rude. I'm not concrete, I'm just relaxed."

        "[ch01_carry_joke_text]":
            $ apply_choice("ch01_carry_joke")
            $ set_story_value("ch01_carry_response", "joked_about_view")
            $ set_story_value("ch01_ryan_julian_trust", get_story_value("ch01_ryan_julian_trust", 0) + 1)
            $ set_story_value("ch01_leia_wake_reason", "voices_at_door")
            mc "Careful. Don't enjoy the view too much."
            friend "Dude. I really, really hate this conversation."
            mc "You're the one who called me back."
            friend "Because I'm trying to be a good person. Open the door."

    $ lc_sfx("door_unlock")
    "I unlocked the villa and held the door while [friend_name] carried her inside."
    $ lc_amb("room_tone")

    if get_story_value("ch01_leia_wake_reason") == "voices_at_door":
        "The voices finally did what the drive home hadn't. [girlfriend_name] stirred against [friend_name]'s shoulder as we crossed the doorway."
        gf "Mm... we're home?"
        mc "Finally. Yeah, we're home."
        gf "Why is [friend_name] carrying me?"
        friend "Because you wouldn't wake up, and [player_name] tried first, and it was not going well."
        mc "I tried first. Sleeping you weighs approximately twice as much."
        gf "That's not how bodies work."
        friend "I don't know, you weren't there. It was pretty bad."
        gf "I was literally there."
        mc "You were drooling on his shoulder, babe."

    $ enter_cinematic_mode()
    scene cg ch01_sofa_half_asleep_night
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    "[friend_name] lowered her onto the sofa. [girlfriend_name] curled straight into the cushions, eyes already drifting shut again."

    friend "I'm just going to say it, man. Your girlfriend is a logistical problem."
    mc "You offered! I didn't even ask."
    friend "I know. I'm going to think about that decision on my own time."

    $ exit_cinematic_mode()
    scene bg ch01_villa_living_evening
    with dissolve
    $ lc_amb("room_tone")
    $ cast(ryan="casual", leia="purple_dress_no_bra", julian="evening")
    $ face("leia", "flustered")

    gf "I can hear both of you, you know. I'm awake now."
    mc "Welcome back."
    gf "Barely. Stop talking about me like I'm luggage."

    "[friend_name] laughed, gathered the bags from the doorway, and headed toward the kitchen."
    $ set_story_flag("ch01_scene_13_complete")
    $ set_story_flag("ch01_scenes_07_13_complete")

    jump ch01_scene_13b_night_pool
