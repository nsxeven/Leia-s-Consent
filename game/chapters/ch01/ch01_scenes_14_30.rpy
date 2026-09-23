# Leia's Consent — Chapter One: Something Different
# Playable continuation: Scenes 14–30 / end of Day One.
#
# Route rule introduced here:
# - Open/NTS choices can raise Curiosity/Exhibitionism while still reinforcing Love/Trust.
# - Dismissive/nonchalant choices make Leia feel less wanted, raising Boredom and lowering Love/Trust.
#   That pressure can later feed Temptation/Secrecy and the NTR route without treating openness itself as betrayal.

label ch01_scene_14_movie_setup:

    scene bg ch01_villa_living_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p03", "neutral")
    with dissolve

    "Leia rubbed both hands over her face and stared down at the dinner dress as if she had only just remembered she was still wearing it."

    gf "I'm changing before I fall asleep in this again."
    mc "Strong plan."
    friend "I support any plan that doesn't involve me carrying anybody else tonight."
    gf "Nobody asked you to."
    friend "History will remember the sacrifice."

    "We scattered to our rooms for a few minutes. By the time I came back downstairs, the villa had shifted from 'night out' to 'we live here now.'"

    $ grant_story_outfit("resort_loungewear", equip=True)
    $ set_story_value("ch01_dinner_dress_state", "changed_out_at_villa")
    $ set_story_value("ch01_movie_blanket_state", "on")
    $ set_story_value("ch01_movie_night_started", True)

    scene bg ch01_villa_living_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p01", "smile")
    with dissolve

    "Leia returned in an oversized sleep tee and short lounge shorts, hair pulled back loosely. Julian had changed too. I finally poured myself the drink I'd skipped all evening."

    gf "Congratulations. You may now participate."
    mc "I've been participating all day."
    friend "Driving doesn't count."
    mc "It counted when both of you needed a ride home."

    "Julian found a terrible movie. Leia vetoed two better ones purely because he recommended them, then approved the terrible one because the trailer made her laugh."

    friend "Democracy has failed."
    gf "Press play."

    $ enter_cinematic_mode()
    hide leia
    scene cg ch01_movie_cuddle_blanket
    with dissolve

    "Leia tucked herself against my side beneath a throw blanket while Julian claimed the other end of the sofa. Snacks covered most of the coffee table."
    "For ten quiet minutes, the movie actually held our attention."

    $ exit_cinematic_mode()
    scene bg ch01_villa_living_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p01", "smile")
    with dissolve

    $ set_story_flag("ch01_scene_14_complete")

    jump ch01_scene_15_under_blanket


label ch01_scene_15_under_blanket:

    "At some point Leia settled deeper against me and pulled the blanket higher over both of us."
    "My hand, already resting at her waist, wandered lazily along her side and upper thigh beneath the blanket."

    "She caught my wrist."

    gf "Babe."
    mc "Mm?"

    "Her eyes flicked toward Julian without turning her head. He was still watching the movie."

    gf "He's literally right there."

    $ ch01_movie_stop_text = format_choice("ch01_movie_stop", "Okay, okay. I'll behave.")
    $ ch01_movie_subtle_text = format_choice("ch01_movie_subtle", "Then don't make it obvious.")
    $ ch01_movie_tease_presence_text = format_choice("ch01_movie_tease_presence", "You seemed fine until you remembered he was there.")
    $ ch01_movie_dismiss_concern_text = format_choice("ch01_movie_dismiss_concern", "You're overthinking it. He won't care.")

    menu:
        "[ch01_movie_stop_text]":
            $ apply_choice("ch01_movie_stop")
            $ set_story_value("ch01_movie_first_response", "stopped")
            mc "Okay, okay. I'll behave."
            "I loosened my arm around her and left my hand where it could not be mistaken for anything except a cuddle."
            $ set_leia_expression("smile")
            gf "Thank you."
            mc "For the record, this movie owes me."
            gf "Watch it."

        "[ch01_movie_subtle_text]":
            $ apply_choice("ch01_movie_subtle")
            $ set_story_value("ch01_movie_first_response", "subtle")
            mc "Then don't make it obvious."
            $ set_leia_expression("embarrassed")
            gf "[player_name]."
            mc "What?"
            gf "That is not what I said."
            "She kept hold of my wrist for another second, then released it without moving away."

        "[ch01_movie_tease_presence_text]":
            $ apply_choice("ch01_movie_tease_presence")
            $ set_story_value("ch01_movie_first_response", "teased_presence")
            mc "You seemed fine until you remembered he was there."
            $ set_leia_expression("embarrassed")
            gf "Because I forgot for a second."
            mc "Exactly."
            gf "You're annoying."
            "She hid the lower half of her face behind the blanket but stayed tucked against me."

        "[ch01_movie_dismiss_concern_text]":
            $ apply_choice("ch01_movie_dismiss_concern")
            $ set_story_value("ch01_movie_first_response", "dismissed")
            mc "You're overthinking it. He won't care."
            $ set_leia_expression("annoyed")
            gf "That's not really the point."
            mc "I know."
            gf "Do you?"
            "I looked back at the movie. Leia did too, but some of the warmth in the moment had gone with it."

    $ set_story_flag("ch01_scene_15_complete")
    jump ch01_scene_16_can_he_tell


label ch01_scene_16_can_he_tell:

    "The movie carried on. So did the silence between the three of us."

    if get_story_value("ch01_movie_first_response") == "stopped":
        "A few minutes later Leia leaned closer again, keeping her voice low."
        gf "Do you think he noticed what you were doing before?"
    else:
        "A few minutes later Leia leaned closer, voice barely above the movie."
        gf "Do you think he can tell?"

    mc "Can tell what?"
    gf "Don't make me say it."

    $ ch01_can_tell_behave_text = format_choice("ch01_can_tell_behave", "Probably not. And I'll behave.")
    $ ch01_can_tell_tease_text = format_choice("ch01_can_tell_tease", "Only if you keep making that face.")
    $ ch01_can_tell_push_text = format_choice("ch01_can_tell_push", "Would it bother you if he could?")
    $ ch01_can_tell_dismiss_text = format_choice("ch01_can_tell_dismiss", "Does it really matter?")

    menu:
        "[ch01_can_tell_behave_text]":
            $ apply_choice("ch01_can_tell_behave")
            $ set_story_value("ch01_can_tell_response", "reassured")
            mc "Probably not. And I'll behave."
            gf "Good."
            "She relaxed against me again."

        "[ch01_can_tell_tease_text]":
            $ apply_choice("ch01_can_tell_tease")
            $ set_story_value("ch01_can_tell_response", "teased")
            mc "Only if you keep making that face."
            gf "What face?"
            mc "That one."
            $ set_leia_expression("embarrassed")
            gf "Shut up."

        "[ch01_can_tell_push_text]":
            $ apply_choice("ch01_can_tell_push")
            $ set_story_value("ch01_can_tell_response", "asked_if_bothered")
            mc "Would it bother you if he could?"
            "Leia looked at me instead of answering immediately."

            if partner_stats["exhibitionism"] < 18:
                gf "Yes. Obviously."
                mc "Okay."
            elif partner_stats["exhibitionism"] < 26:
                gf "...I don't know."
                mc "That's allowed."
            else:
                gf "That's not an answer to my question."
                mc "Neither was that."
                "Her mouth twitched despite herself."

        "[ch01_can_tell_dismiss_text]":
            $ apply_choice("ch01_can_tell_dismiss")
            $ set_story_value("ch01_can_tell_response", "dismissed")
            mc "Does it really matter?"
            "Leia studied my face for a moment."
            gf "To me, maybe."
            mc "Fair."
            gf "Right."

    $ set_story_flag("ch01_scene_16_complete")
    jump ch01_scene_17_julian_notices


label ch01_scene_17_julian_notices:

    "Another ten minutes passed before Julian finally paused the movie."

    friend "Okay. Serious question."
    gf "What?"
    friend "Do you need the bathroom or something?"
    gf "No?"
    friend "You've been moving around for like five minutes."

    "Leia went completely still beside me."

    $ ch01_fidget_cover_text = format_choice("ch01_fidget_cover", "She's just trying to get comfortable.")
    $ ch01_fidget_tease_text = format_choice("ch01_fidget_tease", "Yeah, Leia. Why are you moving around so much?")
    $ ch01_fidget_push_text = format_choice("ch01_fidget_push", "She's fine. Keep watching.")
    $ ch01_fidget_dismiss_text = format_choice("ch01_fidget_dismiss", "She's fine. Whatever.")

    menu:
        "[ch01_fidget_cover_text]":
            $ apply_choice("ch01_fidget_cover")
            $ set_story_value("ch01_fidget_response", "covered")
            mc "She's just trying to get comfortable."
            gf "Exactly."
            friend "You have an entire sofa."
            gf "And yet comfort remains elusive. Play the movie."

        "[ch01_fidget_tease_text]":
            $ apply_choice("ch01_fidget_tease")
            $ set_story_value("ch01_fidget_response", "teased")
            mc "Yeah, Leia. Why are you moving around so much?"
            $ set_leia_expression("annoyed")
            gf "I hate you."
            mc "No you don't."
            "Something connected sharply with my shin beneath the blanket."
            friend "Am I missing something?"
            gf "No. Play the movie."

        "[ch01_fidget_push_text]":
            $ apply_choice("ch01_fidget_push")
            $ set_story_value("ch01_fidget_response", "risk_pushed")
            mc "She's fine. Keep watching."
            "Leia gave me a look that could only have been interpreted correctly by one person in the room."
            friend "Okay...?"
            gf "Movie."

        "[ch01_fidget_dismiss_text]":
            $ apply_choice("ch01_fidget_dismiss")
            $ set_story_value("ch01_fidget_response", "dismissed")
            mc "She's fine. Whatever."
            "Leia's eyes moved from Julian to me."
            gf "I'm right here."
            mc "I know."
            friend "...I'm just going to unpause this."

    "Julian reached for his glass, found only melting ice, and stood."

    friend "I'm getting ice and soft drinks before you two finish everything without me."
    mc "Grab another Coke."
    gf "And ice. A lot of ice."
    friend "Yes, your majesty."

    with dissolve

    $ set_story_flag("ch01_scene_17_complete")
    jump ch01_scene_18_private_under_blanket


label ch01_scene_18_private_under_blanket:

    "The second Julian disappeared toward the kitchen, Leia turned to me."

    gf "You were doing that on purpose."
    mc "Doing what?"
    gf "Don't."
    mc "I genuinely have no idea what you're talking about."
    gf "Trying to make me react while he was sitting right there."

    $ ch01_private_apologize_text = format_choice("ch01_private_apologize", "Okay. I got carried away. Sorry.")
    $ ch01_private_playful_text = format_choice("ch01_private_playful", "You weren't exactly telling me to stop.")
    $ ch01_private_curiosity_text = format_choice("ch01_private_curiosity", "Did you actually want me to stop?")
    $ ch01_private_dismiss_text = format_choice("ch01_private_dismiss", "You're making a big deal out of nothing.")

    menu:
        "[ch01_private_apologize_text]":
            $ apply_choice("ch01_private_apologize")
            $ set_story_value("ch01_private_movie_response", "apologized")
            mc "Okay. I got carried away. Sorry."
            "Leia's expression softened."
            gf "I know you were joking around. Just... ask me next time."
            mc "Deal."

        "[ch01_private_playful_text]":
            $ apply_choice("ch01_private_playful")
            $ set_story_value("ch01_private_movie_response", "playful")
            mc "You weren't exactly telling me to stop."
            gf "Because I was trying not to make it obvious!"
            mc "So that wasn't a no."
            gf "That is an incredibly annoying way to phrase it."
            "She was fighting a smile."

        "[ch01_private_curiosity_text]":
            $ apply_choice("ch01_private_curiosity")
            $ set_story_value("ch01_private_movie_response", "curious_open")
            mc "Did you actually want me to stop?"
            "Leia hesitated."
            gf "...I don't know."
            mc "That's okay."
            gf "It was embarrassing."
            "She glanced toward the kitchen."
            gf "But it was also kind of..."
            mc "Kind of what?"

        "[ch01_private_dismiss_text]":
            $ apply_choice("ch01_private_dismiss")
            $ set_story_value("ch01_private_movie_response", "dismissed")
            mc "You're making a big deal out of nothing."
            "Leia's expression flattened."
            gf "Right. Fine."
            mc "I didn't mean—"
            gf "It's fine."

    with dissolve

    "Julian returned balancing a bowl of ice, two soft drinks and three glasses."

    friend "Why do I feel like I interrupted something?"
    gf "You didn't."
    friend "That was suspiciously fast."
    mc "Put the ice down, detective."
    friend "Gladly. This is freezing my hand."

    if get_story_value("ch01_private_movie_response") == "curious_open":
        "Leia refused to look at me while Julian rebuilt everyone's drinks. The unfinished sentence stayed exactly where she'd left it."

    $ set_story_flag("ch01_scene_18_complete")
    jump ch01_scene_19_too_hot


label ch01_scene_19_too_hot:

    "The movie resumed. Julian had barely settled back down before Leia started tugging at the blanket."

    gf "Okay, I'm actually dying under this thing."
    friend "I'll lower the aircon."
    mc "Don't. It'll become a freezer in ten minutes."
    friend "It is objectively warm."
    mc "You're holding a glass full of ice."
    gf "Fine. Then this is going."

    "Leia pushed the blanket completely off both of us and dropped it over the arm of the sofa."
    $ set_story_value("ch01_movie_blanket_state", "off")

    $ enter_cinematic_mode()
    hide leia
    scene cg ch01_movie_no_blanket
    with dissolve

    "Without it, there was nothing unusual about the way we were sitting—just Leia curled beside me in her loungewear."
    "But whatever had felt private under the blanket no longer had anywhere to hide."

    $ exit_cinematic_mode()
    scene bg ch01_villa_living_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p01", "neutral")
    with dissolve

    $ set_story_flag("ch01_scene_19_complete")
    jump ch01_scene_20_no_hiding_place


label ch01_scene_20_no_hiding_place:

    "My hand settled naturally on Leia's thigh. Nothing about the gesture would have looked strange from across the sofa."
    "Leia looked down at it anyway. Then at Julian. Then back at me."

    $ ch01_noblanket_behave_text = format_choice("ch01_noblanket_behave", "Leave your hand there and behave.")
    $ ch01_noblanket_test_text = format_choice("ch01_noblanket_test", "Move it slightly higher and see how she reacts.")
    $ ch01_noblanket_tease_text = format_choice("ch01_noblanket_tease", "Problem?")
    $ ch01_noblanket_phone_text = format_choice("ch01_noblanket_phone", "Pull your hand away and check your phone.")

    menu:
        "[ch01_noblanket_behave_text]":
            $ apply_choice("ch01_noblanket_behave")
            $ set_story_value("ch01_noblanket_response", "behaved")
            "I left my hand exactly where it was and turned my attention back to the movie."
            "A few seconds later Leia leaned against me again."

        "[ch01_noblanket_test_text]":
            $ apply_choice("ch01_noblanket_test")
            $ set_story_value("ch01_noblanket_response", "tested")
            "I shifted my hand only slightly—still somewhere completely defensible as ordinary couple contact."
            "Leia's eyes narrowed. I stopped there."
            gf "Behave."
            mc "I am."
            gf "Barely."

        "[ch01_noblanket_tease_text]":
            $ apply_choice("ch01_noblanket_tease")
            $ set_story_value("ch01_noblanket_response", "teased")
            mc "Problem?"
            gf "You know exactly what the problem is."
            mc "There's no blanket anymore."
            gf "Exactly."
            "She still did not move my hand."

        "[ch01_noblanket_phone_text]":
            $ apply_choice("ch01_noblanket_phone")
            $ set_story_value("ch01_noblanket_response", "withdrew_distracted")
            "I pulled my hand away and checked my phone instead."
            "Leia watched me for half a second before turning back toward the television."
            gf "Never mind."
            mc "Hm?"
            gf "Nothing."

    $ set_story_flag("ch01_scene_20_complete")
    jump ch01_scene_21_watching_julian


label ch01_scene_21_watching_julian:

    "Eventually Leia turned sideways and stretched her legs across my lap."
    "When Julian reached forward for the snacks, she adjusted instinctively—and checked where his eyes were before settling again."
    "It was quick. I still caught it."

    $ ch01_watch_claim_text = format_choice("ch01_watch_claim", "Eyes on me.")
    $ ch01_watch_tease_text = format_choice("ch01_watch_tease", "You're watching him.")
    $ ch01_watch_check_text = format_choice("ch01_watch_check", "You okay?")
    $ ch01_watch_ignore_text = format_choice("ch01_watch_ignore", "Say nothing and keep scrolling on your phone.")

    menu:
        "[ch01_watch_claim_text]":
            $ apply_choice("ch01_watch_claim")
            $ set_story_value("ch01_watching_response", "claimed_attention")
            mc "Eyes on me."
            "Leia looked at me, startled, then understood exactly what I meant."
            $ set_leia_expression("embarrassed")
            gf "Possessive."
            mc "Complaining?"
            "Her foot nudged my side."
            gf "Maybe not."

        "[ch01_watch_tease_text]":
            $ apply_choice("ch01_watch_tease")
            $ set_story_value("ch01_watching_response", "called_out")
            mc "You're watching him."
            gf "I'm not."
            mc "You literally just checked if he was looking."
            gf "Because of you."
            "That answer did not actually settle anything."

        "[ch01_watch_check_text]":
            $ apply_choice("ch01_watch_check")
            $ set_story_value("ch01_watching_response", "checked_in")
            mc "You okay?"
            gf "Yeah."
            "She looked at me for another second."
            gf "Just very aware of everything now."
            mc "We can stop making it weird."
            gf "I didn't say it was weird."

        "[ch01_watch_ignore_text]":
            $ apply_choice("ch01_watch_ignore")
            $ set_story_value("ch01_watching_response", "ignored")
            "I noticed, but said nothing and kept scrolling."
            "Leia looked at me once as if waiting for a reaction that never came. Then she looked away."

    $ set_story_flag("ch01_scene_21_complete")
    jump ch01_scene_22_first_micro_test


label ch01_scene_22_first_micro_test:

    "Leia got up for her drink. When she dropped back onto the sofa, the loose neckline of her sleep tee had shifted slightly from the way she'd been lying against me."
    "She noticed almost immediately."
    "Her hand started toward the fabric, stopped, and her eyes flicked toward Julian."
    "He was watching the movie."
    "Then she looked at me."

    $ enter_cinematic_mode()
    hide leia
    scene cg ch01_lounge_micro_test
    with dissolve

    "She knew. I knew she knew. For the first time that day, nothing accidental had forced the decision for her."

    $ exit_cinematic_mode()
    scene bg ch01_villa_living_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p03", "embarrassed")
    with dissolve

    $ ch01_micro_warn_text = format_choice("ch01_micro_warn", "Your top.")
    $ ch01_micro_silent_text = format_choice("ch01_micro_silent", "Say nothing. Let her decide.")
    $ ch01_micro_open_text = format_choice("ch01_micro_open", "You know.")
    $ ch01_micro_dismiss_text = format_choice("ch01_micro_dismiss", "Doesn't matter.")

    menu:
        "[ch01_micro_warn_text]":
            $ apply_choice("ch01_micro_warn")
            $ set_story_value("ch01_micro_test_response", "warned")
            mc "Your top."
            "Leia fixed it immediately."
            gf "Thanks."
            mc "Mm."

        "[ch01_micro_silent_text]":
            $ apply_choice("ch01_micro_silent")
            $ set_story_value("ch01_micro_test_response", "silent_choice")
            "I said nothing."
            "Leia held my gaze for a second, then eventually adjusted the neckline herself."
            "The pause before she did it was the part I remembered."

        "[ch01_micro_open_text]":
            $ apply_choice("ch01_micro_open")
            $ set_story_value("ch01_micro_test_response", "knowingly_left")
            mc "You know."
            "Leia's eyes stayed on mine."
            gf "I know."
            "She left the fabric exactly where it was for a little while longer."
            "Julian never visibly noticed. That somehow made the choice feel more deliberate, not less."

        "[ch01_micro_dismiss_text]":
            $ apply_choice("ch01_micro_dismiss")
            $ set_story_value("ch01_micro_test_response", "dismissed")
            mc "Doesn't matter."
            "Leia blinked."
            gf "Okay."
            "She fixed the top herself and turned back to the screen."

    $ set_story_flag("ch01_scene_22_complete")
    jump ch01_scene_23_relationship_philosophy


label ch01_scene_23_relationship_philosophy:

    "The movie finally reached the point where none of us were pretending it was good."
    "On screen, one character discovered their partner flirting with somebody at a party and reacted like the world had ended."

    friend "Imagine breaking up over that."
    gf "Depends what you call flirting."
    friend "Talking to somebody?"
    gf "That's not flirting."
    mc "You interrogated me over one phone call earlier."
    gf "I did not interrogate you."
    mc "You asked if we'd ever dated."
    gf "Perfectly normal question."
    friend "I witnessed an interrogation."
    gf "Nobody asked you."

    "Julian grinned and raised both hands in surrender."
    gf "Okay then. Where's the line?"

    $ ch01_philosophy_couple_text = format_choice("ch01_philosophy_couple", "Some things should stay between the couple.")
    $ ch01_philosophy_trust_text = format_choice("ch01_philosophy_trust", "Trust matters more than arbitrary rules.")
    $ ch01_philosophy_jealousy_fun_text = format_choice("ch01_philosophy_jealousy_fun", "I think a little jealousy can actually be fun.")
    $ ch01_philosophy_dont_care_text = format_choice("ch01_philosophy_dont_care", "People can do what they want. I don't really care.")

    menu:
        "[ch01_philosophy_couple_text]":
            $ apply_choice("ch01_philosophy_couple")
            $ set_story_value("ch01_relationship_philosophy", "couple_boundary")
            mc "Some things should stay between the couple."
            gf "Like?"
            mc "Depends on the couple. But yeah, there should still be things that are ours."
            "Leia nodded slowly."
            gf "I get that."

        "[ch01_philosophy_trust_text]":
            $ apply_choice("ch01_philosophy_trust")
            $ set_story_value("ch01_relationship_philosophy", "trust_based")
            mc "Trust matters more than arbitrary rules."
            gf "So as long as nobody's hiding anything?"
            mc "That's a pretty big part of it."
            friend "Disturbingly mature answer."

        "[ch01_philosophy_jealousy_fun_text]":
            $ apply_choice("ch01_philosophy_jealousy_fun")
            $ set_story_value("ch01_relationship_philosophy", "playful_jealousy")
            mc "I think a little jealousy can actually be fun."
            gf "Fun?"
            mc "A little."
            gf "You're weird."
            friend "I've been saying this for years."
            "Leia laughed, but she was still thinking about it."

        "[ch01_philosophy_dont_care_text]":
            $ apply_choice("ch01_philosophy_dont_care")
            $ set_story_value("ch01_relationship_philosophy", "nonchalant")
            mc "People can do what they want. I don't really care."
            gf "You wouldn't care at all?"
            mc "Not enough to make rules about it."
            "Leia stared at the television instead of me."
            gf "Right."

    $ set_story_flag("ch01_scene_23_complete")
    jump ch01_scene_24_looking_counts


label ch01_scene_24_looking_counts:

    gf "Okay, but looking doesn't count, right?"
    mc "Looking at what?"
    gf "Someone attractive."
    friend "I feel like I've accidentally joined couples therapy."
    gf "You're the one who started this."

    gf "You seriously wouldn't care if some girl was checking you out?"

    $ ch01_looking_enjoy_text = format_choice("ch01_looking_enjoy", "I'd probably enjoy it.")
    $ ch01_looking_harmless_text = format_choice("ch01_looking_harmless", "It doesn't matter as long as nothing happens.")
    $ ch01_looking_boundary_text = format_choice("ch01_looking_boundary", "I'd care if you were encouraging it.")
    $ ch01_looking_dont_care_text = format_choice("ch01_looking_dont_care", "I genuinely wouldn't care.")

    menu:
        "[ch01_looking_enjoy_text]":
            $ apply_choice("ch01_looking_enjoy")
            $ set_story_value("ch01_looking_philosophy", "enjoy_attention")
            mc "I'd probably enjoy it."
            gf "Of course you would."
            mc "You asked."
            gf "So if someone was checking me out?"
            mc "Might enjoy that too."
            $ set_leia_expression("embarrassed")
            gf "...Of course you would."

        "[ch01_looking_harmless_text]":
            $ apply_choice("ch01_looking_harmless")
            $ set_story_value("ch01_looking_philosophy", "harmless")
            mc "It doesn't matter as long as nothing happens."
            gf "So looking is just looking."
            mc "Pretty much."
            gf "Even if it's me?"
            mc "Even if it's you."

        "[ch01_looking_boundary_text]":
            $ apply_choice("ch01_looking_boundary")
            $ set_story_value("ch01_looking_philosophy", "encouragement_boundary")
            mc "I'd care if you were encouraging it."
            gf "That's different from someone just looking though."
            mc "Exactly."
            "Leia nodded."

        "[ch01_looking_dont_care_text]":
            $ apply_choice("ch01_looking_dont_care")
            $ set_story_value("ch01_looking_philosophy", "indifferent")
            mc "I genuinely wouldn't care."
            gf "At all?"
            mc "Why would I?"
            "Leia's smile faded by a fraction."
            gf "No reason."

    "Julian suddenly became extremely interested in the ice inside his glass."

    $ set_story_flag("ch01_scene_24_complete")
    jump ch01_scene_25_julian_put_on_spot


label ch01_scene_25_julian_put_on_spot:

    gf "What about you?"
    friend "What about me?"
    gf "You're single. Surely you look."
    friend "At people? Occasionally. I possess eyes."
    gf "Would you actually tell someone if you thought they were attractive?"
    friend "Depends who."
    gf "That's such a non-answer."
    friend "It's an excellent answer."

    $ ch01_julian_change_subject_text = format_choice("ch01_julian_change_subject", "Alright. Enough relationship court.")
    $ ch01_julian_let_play_text = format_choice("ch01_julian_let_play", "Say nothing and let them keep talking.")
    $ ch01_julian_put_spot_text = format_choice("ch01_julian_put_spot", "He's avoiding it because he doesn't want to get himself killed.")
    $ ch01_julian_dont_care_text = format_choice("ch01_julian_dont_care", "Just answer her. It's not like I care.")

    menu:
        "[ch01_julian_change_subject_text]":
            $ apply_choice("ch01_julian_change_subject")
            $ set_story_value("ch01_julian_attraction_prompt", "changed_subject")
            mc "Alright. Enough relationship court."
            friend "Thank you."
            gf "Cowards. Both of you."
            mc "Correct."

        "[ch01_julian_let_play_text]":
            $ apply_choice("ch01_julian_let_play")
            $ set_story_value("ch01_julian_attraction_prompt", "let_play")
            "I stayed out of it."
            gf "See? You're still avoiding it."
            friend "Because I'm capable of identifying traps."

        "[ch01_julian_put_spot_text]":
            $ apply_choice("ch01_julian_put_spot")
            $ set_story_value("ch01_julian_attraction_prompt", "put_on_spot")
            mc "He's avoiding it because he doesn't want to get himself killed."
            "Leia immediately looked at Julian."
            friend "Thank you, [player_name]. Very helpful."
            gf "Why would you get killed?"
            mc "Exactly."
            friend "I hate both of you."

        "[ch01_julian_dont_care_text]":
            $ apply_choice("ch01_julian_dont_care")
            $ set_story_value("ch01_julian_attraction_prompt", "ryan_indifferent")
            mc "Just answer her. It's not like I care."
            "Leia looked at me before she looked back at Julian."
            friend "That somehow makes this worse."
            gf "Answer."

    $ set_story_flag("ch01_scene_25_complete")
    jump ch01_scene_26_the_compliment


label ch01_scene_26_the_compliment:

    if get_story_value("ch01_julian_attraction_prompt") == "changed_subject":
        "Julian took the escape route I'd given him and the conversation drifted for another minute."
        "Leia eventually let him off the hook, though not without calling him a coward one more time."
        $ set_story_value("ch01_julian_compliment_given", False)

    else:
        "Julian looked between us, apparently deciding that there was no answer left that would make the conversation less awkward."

        friend "Obviously you're attractive."
        "Leia went quiet for half a second."
        friend "You're an attractive woman. I'm pretty sure [player_name] knows that."
        gf "That was very diplomatic."
        friend "I've had a difficult day."

        $ set_story_value("ch01_julian_compliment_given", True)

        $ ch01_compliment_affirm_text = format_choice("ch01_compliment_affirm", "Of course she is.")
        $ ch01_compliment_tease_text = format_choice("ch01_compliment_tease", "Careful, mate.")
        $ ch01_compliment_enjoy_text = format_choice("ch01_compliment_enjoy", "See? Told you.")
        $ ch01_compliment_shrug_text = format_choice("ch01_compliment_shrug", "Shrug and check your phone.")

        menu:
            "[ch01_compliment_affirm_text]":
                $ apply_choice("ch01_compliment_affirm")
                $ set_story_value("ch01_compliment_response", "affirmed")
                mc "Of course she is."
                "Leia looked at me and smiled before turning back to Julian."
                gf "Thank you."
                friend "You're welcome."

            "[ch01_compliment_tease_text]":
                $ apply_choice("ch01_compliment_tease")
                $ set_story_value("ch01_compliment_response", "teased")
                mc "Careful, mate."
                friend "You put me here."
                mc "I know."
                gf "You two are ridiculous."

            "[ch01_compliment_enjoy_text]":
                $ apply_choice("ch01_compliment_enjoy")
                $ set_story_value("ch01_compliment_response", "enjoyed")
                mc "See? Told you."
                gf "You are enjoying this way too much."
                mc "Maybe."
                "Leia shook her head, but she was smiling."
                gf "Thank you, Julian."
                friend "You're welcome. Please never make me do that again."

            "[ch01_compliment_shrug_text]":
                $ apply_choice("ch01_compliment_shrug")
                $ set_story_value("ch01_compliment_response", "shrugged")
                "I shrugged and checked my phone."
                "Leia's attention lingered on me for a beat, then returned to Julian."
                gf "...Thank you."
                friend "Yeah. Of course."
                "The compliment landed more cleanly than my reaction to it did."

    $ set_story_flag("ch01_scene_26_complete")
    jump ch01_scene_27_late_photo_drop


label ch01_scene_27_late_photo_drop:

    "The movie had been over for several minutes before any of us bothered to stand."

    friend "I'm done. If I stay here another ten minutes I'm sleeping on this sofa."
    gf "Weak."
    friend "You fell asleep in a car."
    gf "That was tactical."

    "Julian gathered his empty glass and headed toward the hallway."

    friend "Goodnight, children."
    mc "Goodnight, grandpa."
    gf "Night."

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

    "It was one of the pool photos he had not sent earlier—less posed than the others, and somehow better because of it."

    python:
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

    gf "Okay, this one's actually good."
    mc "Actually?"
    gf "Don't start."
    mc "That was his line."
    gf "You're both annoying."

    "The attachment stayed in the Trip Group and was indexed into the Phone's Photos state for later viewing."

    $ set_story_flag("ch01_scene_27_complete")
    jump ch01_scene_28_ryan_leia_alone


label ch01_scene_28_ryan_leia_alone:

    scene bg ch01_villa_living_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p01", "neutral")
    with dissolve

    "The villa became noticeably quieter once Julian's door closed upstairs."
    "Leia stayed beside me, turning her empty glass slowly between both hands."

    gf "You were weird tonight."
    mc "Me?"
    gf "Yes, you."
    mc "Specific."
    gf "The blanket. The questions. Putting Julian on the spot. All of it."

    $ ch01_alone_apologize_text = format_choice("ch01_alone_apologize", "I think I pushed the joke too far.")
    $ ch01_alone_curiosity_text = format_choice("ch01_alone_curiosity", "I was curious how you'd react.")
    $ ch01_alone_open_text = format_choice("ch01_alone_open", "I liked watching you get nervous.")
    $ ch01_alone_dismiss_text = format_choice("ch01_alone_dismiss", "It was just messing around. Don't overthink it.")

    menu:
        "[ch01_alone_apologize_text]":
            $ apply_choice("ch01_alone_apologize")
            $ set_story_value("ch01_alone_movie_response", "apologized")
            mc "I think I pushed the joke too far."
            gf "A little."
            mc "Sorry."
            gf "I know you weren't trying to make me uncomfortable."
            "She leaned against my shoulder."

        "[ch01_alone_curiosity_text]":
            $ apply_choice("ch01_alone_curiosity")
            $ set_story_value("ch01_alone_movie_response", "curious")
            mc "I was curious how you'd react."
            gf "And?"
            mc "I'm still figuring that out."
            gf "Helpful."
            mc "What about you?"
            gf "Also still figuring it out."

        "[ch01_alone_open_text]":
            $ apply_choice("ch01_alone_open")
            $ set_story_value("ch01_alone_movie_response", "open")
            mc "I liked watching you get nervous."
            gf "That's so mean."
            mc "You liked it."
            "Leia opened her mouth to deny it, stopped, then looked down at her glass."
            gf "...A little."
            mc "Yeah?"
            gf "Don't make me regret admitting that."

        "[ch01_alone_dismiss_text]":
            $ apply_choice("ch01_alone_dismiss")
            $ set_story_value("ch01_alone_movie_response", "dismissed")
            mc "It was just messing around. Don't overthink it."
            "Leia's thumb stopped moving against the glass."
            gf "Right."
            mc "What?"
            gf "Nothing. I'm tired."

    $ set_story_flag("ch01_scene_28_complete")
    jump ch01_scene_29_private_reflection


label ch01_scene_29_private_reflection:

    if get_story_value("ch01_julian_compliment_given", False):
        mc "What about when Julian called you attractive?"
        gf "What about it?"
        mc "Did you like hearing it?"

        if partner_stats["curiosity"] < 25:
            gf "It was a compliment. Obviously it was nice."
        elif relationship_stats["boredom"] >= 16 and get_story_value("ch01_compliment_response") == "shrugged":
            "Leia hesitated longer than I expected."
            gf "Maybe."
            gf "He actually looked nervous saying it."
            mc "And?"
            gf "Nothing. It was just... nice."
        else:
            "Leia thought about it."
            gf "I think I liked that he was nervous saying it."
            mc "Why?"
            gf "I don't know. It made it feel... real, I guess."

    else:
        mc "Did you actually enjoy any of that tonight?"
        gf "Any of what?"
        mc "Being aware he was there."
        "Leia considered the question."
        gf "I liked that it felt a little dangerous without anything actually happening."

    $ ch01_private_claim_text = format_choice("ch01_private_claim", "That's okay. I still like knowing you're mine.")
    $ ch01_private_open_text = format_choice("ch01_private_open", "I liked seeing you enjoy the attention.")
    $ ch01_private_jealous_text = format_choice("ch01_private_jealous", "I'd be lying if I said I wasn't a little jealous.")
    $ ch01_private_indifferent_text = format_choice("ch01_private_indifferent", "Doesn't really matter to me either way.")

    menu:
        "[ch01_private_claim_text]":
            $ apply_choice("ch01_private_claim")
            $ set_story_value("ch01_private_attention_response", "claimed")
            mc "That's okay. I still like knowing you're mine."
            "Leia looked up at me."
            $ set_leia_expression("smile")
            gf "Possessive again."
            mc "You complained less this time."
            gf "Maybe I changed my mind."

        "[ch01_private_open_text]":
            $ apply_choice("ch01_private_open")
            $ set_story_value("ch01_private_attention_response", "open")
            mc "I liked seeing you enjoy the attention."
            gf "That's still weird."
            mc "Probably."
            gf "...Not necessarily bad weird."

        "[ch01_private_jealous_text]":
            $ apply_choice("ch01_private_jealous")
            $ set_story_value("ch01_private_attention_response", "jealous")
            mc "I'd be lying if I said I wasn't a little jealous."
            "Leia's expression softened."
            gf "A little?"
            mc "A little."
            gf "Good."
            mc "Good?"
            gf "It means you care."

        "[ch01_private_indifferent_text]":
            $ apply_choice("ch01_private_indifferent")
            $ set_story_value("ch01_private_attention_response", "indifferent")
            mc "Doesn't really matter to me either way."
            "Leia went still for a moment."
            gf "Oh."
            mc "What?"
            gf "Nothing."
            "She stood and picked up her glass."
            gf "Come on. I'm tired."

    $ set_story_flag("ch01_scene_29_complete")
    jump ch01_scene_30_end_day_one


label ch01_scene_30_end_day_one:

    scene bg ch01_villa_bedroom_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p01", "neutral")
    with fade

    "We switched off the downstairs lights and finally headed upstairs."
    "Leia plugged her phone in beside the bed and climbed under the covers."

    "Before either of us could settle, my phone lit up one last time."

    python:
        phone_add_message(
            "group",
            "julian",
            text="Breakfast after 11 or I'm calling the police.",
            message_id="ch01_trip_group_breakfast_warning",
            mark_unread=True,
            notify=True,
            notification_title="Trip Group",
        )
        phone_add_message(
            "group",
            "leia",
            text="No promises.",
            message_id="ch01_trip_group_breakfast_leia_reply",
            mark_unread=True,
            notify=False,
        )

    "Leia's phone buzzed a second later. She read the message and laughed quietly."

    gf "He's dramatic."
    mc "He's correct."
    gf "Eleven-thirty."
    mc "Eleven-fifteen."
    gf "Eleven-thirty."
    mc "Fine."

    $ set_story_value("ch01_day1_nonchalant_count", chapter_nonchalant_count("ch01"))

    if chapter_nonchalant_count("ch01") >= 3 and (relationship_stats["boredom"] >= 15 or relationship_stats["love"] <= 48):
        $ set_story_value("ch01_day1_route_pressure", "ntr_seeded")
        "Leia put her phone down, but the small distance between us felt more noticeable than it had that morning."
        "Julian had not done anything wrong. If anything changed from here, it would begin with the spaces I kept leaving open."
    elif nts_score() >= ntr_score() + 5 and partner_stats["curiosity"] >= 24:
        $ set_story_value("ch01_day1_route_pressure", "nts_seeded")
        "Somewhere during the day, a private joke between Leia and me had started acquiring a third point of reference."
        "Nothing had happened. The fact that nothing had happened was part of what made the possibility feel new."
    else:
        $ set_story_value("ch01_day1_route_pressure", "mixed")
        "Yesterday, Julian had simply been my friend."
        "By the end of the day, he'd started becoming Leia's friend too—and none of us had decided yet what that would mean."

    $ set_story_flag("ch01_scene_30_complete")
    $ set_story_flag("ch01_day_01_complete")
    $ set_story_flag("ch01_scenes_14_30_complete")

    scene black
    with fade

    centered "{size=46}CHAPTER ONE — DAY ONE COMPLETE{/size}\n\n{size=25}Current development build ends here{/size}"

    return
