# Leia's Consent — Chapter One: Something Different
# Playable continuation: Scenes 14–30 / end of Day One.
#
# Route rule introduced here:
# - Open/NTS choices can raise Curiosity/Exhibitionism while still reinforcing Love/Trust.
# - Dismissive/nonchalant choices make Leia feel less wanted, raising Boredom and lowering Love/Trust.
#   That pressure can later feed Temptation/Secrecy and the NTR route without treating openness itself as betrayal.

label ch01_scene_13b_night_pool:

    # Pacing Revision v2 — a non-accidental attention beat between the carry
    # sequence and movie night. Nothing goes wrong here; that is the point.
    scene bg ch01_pool_night
    with dissolve

    "Nobody was ready for bed yet."
    "We carried the shop bags outside instead, where the pool lights turned the water blue against the dark and the ocean had become more sound than view."

    gf "Okay. This was worth the ridiculous villa."
    friend "Finally. Gratitude."
    gf "I said the villa was worth it. I said nothing about you."
    mc "She's getting comfortable."
    friend "I noticed."

    "We opened the snacks on the low table and let the first day of the trip finally slow down."

    friend "Tell her about your first driving lesson."
    mc "No."
    gf "Tell me immediately."
    mc "Why is every story suddenly about me?"
    friend "Because I have material."
    gf "I like material."

    "One story became three. [girlfriend_name] retaliated with things I'd done at home that [friend_name] had never heard, and within minutes both of them were comparing notes at my expense."

    mc "This friendship was a mistake."
    gf "You introduced us."
    friend "Technically I introduced you."
    gf "Four years ago. You don't get lifetime credit."
    friend "I absolutely do."

    "[girlfriend_name] laughed and moved to sit along the edge of the pool, bare feet just above the water."
    "For a while she simply listened, leaning back on her hands while [friend_name] finished another story."

    $ enter_cinematic_mode()
    scene cg ch01_night_pool_attention
    with dissolve

    "[friend_name]'s eyes drifted toward her for a moment."
    "There was no towel slipping. No collision. Nothing to catch and nothing to explain."
    "He noticed her, realised I had noticed him noticing, and looked back toward the water."

    $ set_story_flag("ch01_night_pool_julian_glance")

    $ exit_cinematic_mode()
    scene bg ch01_pool_night
    with dissolve

    "[girlfriend_name] glanced at me a second later."

    if get_story_value("ch01_day1_nonchalant_count", chapter_nonchalant_count("ch01")) >= 2:
        "For a moment it looked as if she was waiting for me to meet her eyes."
        "My attention had already drifted elsewhere."
        "When I looked back, she was listening to [friend_name] again."
        $ set_story_value("ch01_night_pool_attention", "ryan_missed_check")
    elif partner_stats["exhibitionism"] >= 14 or player_stats["acceptance"] >= 14:
        "Her eyes flicked briefly from [friend_name] back to me."
        "She didn't say anything, but the tiny question in her expression was difficult to miss."
        "I held her gaze long enough for the corner of her mouth to lift."
        $ set_story_value("ch01_night_pool_attention", "shared_with_ryan")
    else:
        "She smiled at me and shifted closer when she came back from the pool edge."
        "A minute later her shoulder was resting against mine again."
        $ set_story_value("ch01_night_pool_attention", "returned_to_ryan")

    "Nothing happened."
    "That was what made the moment stay with me."

    gf "Movie?"
    friend "Only if I choose."
    gf "Then no."
    mc "Strong start."

    $ set_story_flag("ch01_scene_13b_complete")
    jump ch01_scene_14_movie_setup


label ch01_scene_14_movie_setup:

    scene bg ch01_villa_living_night
    with dissolve

    "[girlfriend_name] rubbed both hands over her face and stared down at the dinner dress as if she had only just remembered she was still wearing it."

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
    with dissolve

    "[girlfriend_name] returned in an oversized sleep tee and short lounge shorts, hair pulled back loosely. [friend_name] had changed too. I finally poured myself the drink I'd skipped all evening."

    gf "Congratulations. You may now participate."
    mc "I've been participating all day."
    friend "Driving doesn't count."
    mc "It counted when both of you needed a ride home."

    "[friend_name] found a terrible movie. [girlfriend_name] vetoed two better ones purely because he recommended them, then approved the terrible one because the trailer made her laugh."

    friend "Democracy has failed."
    gf "Press play."

    $ enter_cinematic_mode()
    scene cg ch01_movie_cuddle_blanket
    with dissolve

    "[girlfriend_name] tucked herself against my side beneath a throw blanket while [friend_name] claimed the other end of the sofa. Snacks covered most of the coffee table."
    "For ten quiet minutes, the movie actually held our attention."

    $ exit_cinematic_mode()
    # Continue the conversation over the seated composition. There is no
    # production loungewear sprite yet, so do not show a wrong outfit.
    scene cg ch01_movie_cuddle_blanket
    with dissolve

    $ set_story_flag("ch01_scene_14_complete")

    jump ch01_scene_15_under_blanket


label ch01_scene_15_under_blanket:

    "At some point [girlfriend_name] settled deeper against me and pulled the blanket higher over both of us."
    "My hand, already resting at her waist, wandered lazily along her side and upper thigh beneath the blanket."

    "She caught my wrist."

    gf "Babe."
    mc "Mm?"

    "Her eyes flicked toward [friend_name] without turning her head. He was still watching the movie."

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
            gf "Thank you."
            mc "For the record, this movie owes me."
            gf "Watch it."

        "[ch01_movie_subtle_text]":
            $ apply_choice("ch01_movie_subtle")
            $ set_story_value("ch01_movie_first_response", "subtle")
            mc "Then don't make it obvious."
            gf "[player_name]."
            mc "What?"
            gf "That is not what I said."
            "She kept hold of my wrist for another second, then released it without moving away."

        "[ch01_movie_tease_presence_text]":
            $ apply_choice("ch01_movie_tease_presence")
            $ set_story_value("ch01_movie_first_response", "teased_presence")
            mc "You seemed fine until you remembered he was there."
            gf "Because I forgot for a second."
            mc "Exactly."
            gf "You're annoying."
            "She hid the lower half of her face behind the blanket but stayed tucked against me."

        "[ch01_movie_dismiss_concern_text]":
            $ apply_choice("ch01_movie_dismiss_concern")
            $ set_story_value("ch01_movie_first_response", "dismissed")
            mc "You're overthinking it. He won't care."
            gf "That's not really the point."
            mc "I know."
            gf "Do you?"
            "I looked back at the movie. [girlfriend_name] did too, but some of the warmth in the moment had gone with it."

    $ set_story_flag("ch01_scene_15_complete")
    jump ch01_scene_16_can_he_tell


label ch01_scene_16_can_he_tell:

    # Pacing Revision v2 — combine the old "can he tell?" and "Julian notices"
    # loops into one escalation instead of asking the player the same question twice.
    "The movie carried on for a few minutes before [girlfriend_name] leaned closer, keeping her voice beneath the soundtrack."

    if get_story_value("ch01_movie_first_response") == "stopped":
        gf "Do you think he noticed what you were doing before?"
    else:
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
            gf "Shut up."

        "[ch01_can_tell_push_text]":
            $ apply_choice("ch01_can_tell_push")
            $ set_story_value("ch01_can_tell_response", "asked_if_bothered")
            mc "Would it bother you if he could?"
            "[girlfriend_name] looked at me instead of answering immediately."
            if partner_stats["exhibitionism"] < 18:
                gf "Yes. Obviously."
            elif partner_stats["exhibitionism"] < 26:
                gf "...I don't know."
            else:
                gf "That's not an answer to my question."
                mc "Neither was that."

        "[ch01_can_tell_dismiss_text]":
            $ apply_choice("ch01_can_tell_dismiss")
            $ set_story_value("ch01_can_tell_response", "dismissed")
            mc "Does it really matter?"
            gf "To me, maybe."
            mc "Fair."

    "Before either of us could keep circling the question, [friend_name] paused the movie."

    friend "Okay. Do you need the bathroom or something?"
    gf "What?"
    friend "You've been moving around for five minutes."

    "[girlfriend_name] went completely still beside me."
    "Her eyes met mine for one mortified second."

    if get_story_value("ch01_can_tell_response") == "reassured":
        mc "She's just trying to get comfortable."
        gf "Exactly. Play the movie."
    elif get_story_value("ch01_can_tell_response") in ("teased", "asked_if_bothered"):
        mc "See? Subtle."
        gf "I hate you."
        friend "Am I missing something?"
        gf "No."
    else:
        mc "She's fine."
        "[girlfriend_name] looked at me, then back at the screen."
        gf "Movie."

    "[friend_name] stared between us, decided not to investigate, and stood to refill the drinks instead."

    friend "Ice? Coke?"
    gf "Both."
    mc "Coke."
    friend "Anything else, your majesties?"
    gf "Less commentary."

    $ set_story_flag("ch01_scene_16_complete")
    $ set_story_flag("ch01_scene_17_complete")
    jump ch01_scene_18_private_under_blanket


label ch01_scene_18_private_under_blanket:

    "The second [friend_name] disappeared toward the kitchen, [girlfriend_name] turned to me."
    # The seated group CG includes Julian, so retire it while he is absent.
    scene bg ch01_villa_living_night
    with dissolve

    $ ch01_movie_respected_request = (
        get_story_value("ch01_movie_first_response") == "stopped"
        and get_story_value("ch01_can_tell_response") == "reassured"
    )

    if ch01_movie_respected_request:
        gf "Thanks for actually listening earlier."
        mc "I wasn't trying to make you uncomfortable."
        gf "I know. I was a little embarrassed, that's all."
        mc "We can talk about it when you're ready."
        "She smiled, although her eyes flicked toward the kitchen."
    else:
        gf "You were doing that on purpose."
        mc "Doing what?"
        gf "Don't."
        mc "I genuinely have no idea what you're talking about."
        gf "Trying to make me react while he was sitting right there."

    $ ch01_private_apologize_text = format_choice("ch01_private_apologize", "I'm glad we could talk." if ch01_movie_respected_request else "Okay. I got carried away. Sorry.")
    $ ch01_private_playful_text = format_choice("ch01_private_playful", "I did manage to behave, didn't I?" if ch01_movie_respected_request else "You weren't exactly telling me to stop.")
    $ ch01_private_curiosity_text = format_choice("ch01_private_curiosity", "Was any part of that interesting to you?" if ch01_movie_respected_request else "Did you actually want me to stop?")
    $ ch01_private_dismiss_text = format_choice("ch01_private_dismiss", "We don't need to make a big deal of it." if ch01_movie_respected_request else "You're making a big deal out of nothing.")

    menu:
        "[ch01_private_apologize_text]":
            $ apply_choice("ch01_private_apologize")
            $ set_story_value("ch01_private_movie_response", "apologized")
            if ch01_movie_respected_request:
                mc "I'm glad we could talk."
                gf "Me too."
                mc "Always."
            else:
                mc "Okay. I got carried away. Sorry."
                "[girlfriend_name]'s expression softened."
                gf "I know you were joking around. Just... ask me next time."
                mc "Deal."

        "[ch01_private_playful_text]":
            $ apply_choice("ch01_private_playful")
            $ set_story_value("ch01_private_movie_response", "playful")
            if ch01_movie_respected_request:
                mc "I did manage to behave, didn't I?"
                gf "For once."
                mc "High praise."
                "She was fighting a smile."
            else:
                mc "You weren't exactly telling me to stop."
                gf "Because I was trying not to make it obvious!"
                mc "So that wasn't a no."
                gf "That is an incredibly annoying way to phrase it."
                "She was fighting a smile."

        "[ch01_private_curiosity_text]":
            $ apply_choice("ch01_private_curiosity")
            $ set_story_value("ch01_private_movie_response", "curious_open")
            if ch01_movie_respected_request:
                mc "Was any part of that interesting to you?"
            else:
                mc "Did you actually want me to stop?"
            "[girlfriend_name] hesitated."
            gf "...I don't know."
            mc "That's okay."
            gf "It was embarrassing."
            "She glanced toward the kitchen."
            gf "But it was also kind of..."
            mc "Kind of what?"

        "[ch01_private_dismiss_text]":
            $ apply_choice("ch01_private_dismiss")
            $ set_story_value("ch01_private_movie_response", "dismissed")
            if ch01_movie_respected_request:
                mc "We don't need to make a big deal of it."
            else:
                mc "You're making a big deal out of nothing."
            "[girlfriend_name]'s expression flattened."
            gf "Right. Fine."
            mc "I didn't mean—"
            gf "It's fine."

    with dissolve

    "[friend_name] returned balancing a bowl of ice, two soft drinks and three glasses."
    scene cg ch01_movie_cuddle_blanket
    with dissolve

    friend "Why do I feel like I interrupted something?"
    gf "You didn't."
    friend "That was suspiciously fast."
    mc "Put the ice down, detective."
    friend "Gladly. This is freezing my hand."

    if get_story_value("ch01_private_movie_response") == "curious_open":
        "[girlfriend_name] refused to look at me while [friend_name] rebuilt everyone's drinks. The unfinished sentence stayed exactly where she'd left it."

    $ set_story_flag("ch01_scene_18_complete")
    jump ch01_scene_19_too_hot


label ch01_scene_19_too_hot:

    "The movie resumed. [friend_name] had barely settled back down before [girlfriend_name] started tugging at the blanket."

    gf "Okay, I'm actually dying under this thing."
    friend "I'll lower the aircon."
    mc "Don't. It'll become a freezer in ten minutes."
    friend "It is objectively warm."
    mc "You're holding a glass full of ice."
    gf "Fine. Then this is going."

    "[girlfriend_name] pushed the blanket completely off both of us and dropped it over the arm of the sofa."
    $ set_story_value("ch01_movie_blanket_state", "off")

    $ enter_cinematic_mode()
    scene cg ch01_movie_no_blanket
    with dissolve

    "Without it, there was nothing unusual about the way we were sitting—just [girlfriend_name] curled beside me in her loungewear."
    "But whatever had felt private under the blanket no longer had anywhere to hide."

    $ exit_cinematic_mode()
    # After the blanket comes off, hold the matching sofa composition.
    scene cg ch01_movie_no_blanket
    with dissolve

    $ set_story_flag("ch01_scene_19_complete")
    jump ch01_scene_20_no_hiding_place


label ch01_scene_20_no_hiding_place:

    "My hand settled naturally on [girlfriend_name]'s thigh. Nothing about the gesture would have looked strange from across the sofa."
    "[girlfriend_name] looked down at it anyway. Then at [friend_name]. Then back at me."

    $ ch01_noblanket_behave_text = format_choice("ch01_noblanket_behave", "Leave your hand there and behave.")
    $ ch01_noblanket_test_text = format_choice("ch01_noblanket_test", "Move it slightly higher and see how she reacts.")
    $ ch01_noblanket_tease_text = format_choice("ch01_noblanket_tease", "Problem?")
    $ ch01_noblanket_phone_text = format_choice("ch01_noblanket_phone", "Pull your hand away and check your phone.")

    menu:
        "[ch01_noblanket_behave_text]":
            $ apply_choice("ch01_noblanket_behave")
            $ set_story_value("ch01_noblanket_response", "behaved")
            "I left my hand exactly where it was and turned my attention back to the movie."
            "A few seconds later [girlfriend_name] leaned against me again."

        "[ch01_noblanket_test_text]":
            $ apply_choice("ch01_noblanket_test")
            $ set_story_value("ch01_noblanket_response", "tested")
            "I shifted my hand only slightly—still somewhere completely defensible as ordinary couple contact."
            "[girlfriend_name]'s eyes narrowed. I stopped there."
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
            "[girlfriend_name] watched me for half a second before turning back toward the television."
            gf "Never mind."
            mc "Hm?"
            gf "Nothing."

    $ set_story_flag("ch01_scene_20_complete")
    jump ch01_scene_21_watching_julian


label ch01_scene_21_watching_julian:

    "Eventually [girlfriend_name] turned sideways and stretched her legs across my lap."
    "When [friend_name] reached forward for the snacks, she adjusted instinctively—and checked where his eyes were before settling again."
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
            "[girlfriend_name] looked at me, startled, then understood exactly what I meant."
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
            "[girlfriend_name] looked at me once as if waiting for a reaction that never came. Then she looked away."

    $ set_story_flag("ch01_scene_21_complete")
    jump ch01_scene_22_first_micro_test


label ch01_scene_22_first_micro_test:

    "[girlfriend_name] got up for her drink. When she dropped back onto the sofa, the loose neckline of her sleep tee had shifted slightly from the way she'd been lying against me."
    "She noticed almost immediately."
    "Her hand started toward the fabric, stopped, and her eyes flicked toward [friend_name]."
    "He was watching the movie."
    "Then she looked at me."

    $ enter_cinematic_mode()
    scene cg ch01_lounge_micro_test
    with dissolve

    "She knew. I knew she knew. For the first time that day, nothing accidental had forced the decision for her."

    $ exit_cinematic_mode()
    # Remain on the moment-of-choice still until Leia responds below.
    $ ch01_micro_warn_text = format_choice("ch01_micro_warn", "Your top.")
    $ ch01_micro_silent_text = format_choice("ch01_micro_silent", "Say nothing. Let her decide.")
    $ ch01_micro_open_text = format_choice("ch01_micro_open", "You know.")
    $ ch01_micro_dismiss_text = format_choice("ch01_micro_dismiss", "Doesn't matter.")

    menu:
        "[ch01_micro_warn_text]":
            $ apply_choice("ch01_micro_warn")
            $ set_story_value("ch01_micro_test_response", "warned")
            mc "Your top."
            "[girlfriend_name] fixed it immediately."
            gf "Thanks."
            mc "Mm."

        "[ch01_micro_silent_text]":
            $ apply_choice("ch01_micro_silent")
            $ set_story_value("ch01_micro_test_response", "silent_choice")
            "I said nothing."
            "[girlfriend_name] held my gaze for a second, then eventually adjusted the neckline herself."
            "The pause before she did it was the part I remembered."

        "[ch01_micro_open_text]":
            $ apply_choice("ch01_micro_open")
            $ set_story_value("ch01_micro_test_response", "knowingly_left")
            mc "You know."
            "[girlfriend_name]'s eyes stayed on mine."
            gf "I know."
            "She left the fabric exactly where it was for a little while longer."
            "[friend_name] never visibly noticed. That somehow made the choice feel more deliberate, not less."

        "[ch01_micro_dismiss_text]":
            $ apply_choice("ch01_micro_dismiss")
            $ set_story_value("ch01_micro_test_response", "dismissed")
            mc "Doesn't matter."
            "[girlfriend_name] blinked."
            gf "Okay."
            "She fixed the top herself and turned back to the screen."

    # All outcomes settle back into an ordinary, covered sofa posture.
    scene cg ch01_movie_no_blanket
    with dissolve

    $ set_story_flag("ch01_scene_22_complete")
    jump ch01_scene_23_relationship_philosophy


label ch01_scene_23_relationship_philosophy:

    # Pacing Revision v2 — relationship philosophy and "does looking count?"
    # now live in the same conversation.
    "By then none of us were pretending the movie was good."
    "On screen, one character discovered their partner flirting at a party and reacted like the world had ended."

    friend "Imagine breaking up over that."
    gf "Depends what you call flirting."
    friend "Talking to somebody?"
    gf "That's not flirting."
    mc "You interrogated me over one phone call earlier."
    gf "I did not interrogate you."
    friend "I witnessed an interrogation."
    gf "Nobody asked you."

    "[girlfriend_name] looked back at me."

    gf "Okay then. Where's the line?"
    gf "Like... someone looking at someone attractive doesn't count, right?"

    $ ch01_philosophy_couple_text = format_choice("ch01_philosophy_couple", "Some things should stay between the couple.")
    $ ch01_philosophy_trust_text = format_choice("ch01_philosophy_trust", "Trust matters more than arbitrary rules.")
    $ ch01_philosophy_jealousy_fun_text = format_choice("ch01_philosophy_jealousy_fun", "I think a little jealousy can actually be fun.")
    $ ch01_philosophy_dont_care_text = format_choice("ch01_philosophy_dont_care", "People can do what they want. I don't really care.")

    menu:
        "[ch01_philosophy_couple_text]":
            $ apply_choice("ch01_philosophy_couple")
            $ set_story_value("ch01_relationship_philosophy", "couple_boundary")
            $ set_story_value("ch01_looking_philosophy", "encouragement_boundary")
            mc "Some things should stay between the couple."
            gf "Looking?"
            mc "Looking is looking. Encouraging it is different."
            gf "Okay. That makes sense."

        "[ch01_philosophy_trust_text]":
            $ apply_choice("ch01_philosophy_trust")
            $ set_story_value("ch01_relationship_philosophy", "trust_based")
            $ set_story_value("ch01_looking_philosophy", "harmless")
            mc "Trust matters more than arbitrary rules."
            gf "So someone looking doesn't matter as long as nobody's hiding anything?"
            mc "Pretty much."
            gf "I like that answer."
            friend "Disturbingly mature."

        "[ch01_philosophy_jealousy_fun_text]":
            $ apply_choice("ch01_philosophy_jealousy_fun")
            $ set_story_value("ch01_relationship_philosophy", "playful_jealousy")
            $ set_story_value("ch01_looking_philosophy", "enjoy_attention")
            mc "I think a little jealousy can actually be fun."
            gf "Fun?"
            mc "Someone noticing you doesn't mean I'm losing you."
            gf "And if I noticed them noticing?"
            mc "Still depends what you do with it."
            "[girlfriend_name] laughed softly, but she was clearly thinking about the answer."

        "[ch01_philosophy_dont_care_text]":
            $ apply_choice("ch01_philosophy_dont_care")
            $ set_story_value("ch01_relationship_philosophy", "nonchalant")
            $ set_story_value("ch01_looking_philosophy", "indifferent")
            mc "People can do what they want. I don't really care."
            gf "You wouldn't care at all?"
            mc "Not enough to make rules about somebody looking."
            "[girlfriend_name]'s attention stayed on me for a moment longer than necessary."
            gf "Right."

    "Across from us, [friend_name] had become extremely interested in the ice inside his glass."

    $ set_story_flag("ch01_scene_23_complete")
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
            "[girlfriend_name] immediately looked at [friend_name]."
            friend "Thank you, [player_name]. Very helpful."
            gf "Why would you get killed?"
            mc "Exactly."
            friend "I hate both of you."

        "[ch01_julian_dont_care_text]":
            $ apply_choice("ch01_julian_dont_care")
            $ set_story_value("ch01_julian_attraction_prompt", "ryan_indifferent")
            mc "Just answer her. It's not like I care."
            "[girlfriend_name] looked at me before she looked back at [friend_name]."
            friend "That somehow makes this worse."
            gf "Answer."

    $ set_story_flag("ch01_scene_25_complete")
    jump ch01_scene_26_the_compliment


label ch01_scene_26_the_compliment:

    if get_story_value("ch01_julian_attraction_prompt") == "changed_subject":
        "[friend_name] took the escape route I'd given him and the conversation drifted for another minute."
        "[girlfriend_name] eventually let him off the hook, though not without calling him a coward one more time."
        $ set_story_value("ch01_julian_compliment_given", False)

    else:
        "[friend_name] looked between us, apparently deciding that there was no answer left that would make the conversation less awkward."

        friend "Obviously you're attractive."
        "[girlfriend_name] went quiet for half a second."
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
                "[girlfriend_name] looked at me and smiled before turning back to [friend_name]."
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
                "[girlfriend_name] shook her head, but she was smiling."
                gf "Thank you, [friend_name]."
                friend "You're welcome. Please never make me do that again."

            "[ch01_compliment_shrug_text]":
                $ apply_choice("ch01_compliment_shrug")
                $ set_story_value("ch01_compliment_response", "shrugged")
                "I shrugged and checked my phone."
                "[girlfriend_name]'s attention lingered on me for a beat, then returned to [friend_name]."
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

    "[friend_name] gathered his empty glass and headed toward the hallway."

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
    with dissolve

    "The villa became noticeably quieter once [friend_name]'s door closed upstairs."
    "[girlfriend_name] stayed beside me, turning her empty glass slowly between both hands."

    $ ch01_movie_pressed = (
        get_story_value("ch01_movie_first_response") != "stopped"
        or get_story_value("ch01_can_tell_response") != "reassured"
        or get_story_value("ch01_noblanket_response") in ("tested", "teased")
    )
    $ ch01_pressed_julian = get_story_value("ch01_julian_attraction_prompt") in ("put_on_spot", "ryan_indifferent")

    if not ch01_movie_pressed and not ch01_pressed_julian:
        gf "You were good about everything tonight."
        mc "Is that a compliment?"
        gf "You listened when I was embarrassed. I noticed."
        mc "I wanted you to be comfortable."
    else:
        gf "You were weird tonight."
        mc "Me?"
        gf "Yes, you."
        mc "Specific."
        if ch01_pressed_julian and ch01_movie_pressed:
            gf "The blanket. The questions. Putting [friend_name] on the spot. All of it."
        elif ch01_pressed_julian:
            gf "Putting [friend_name] on the spot with all those questions."
        else:
            gf "The blanket. The questions. All of it."

    $ ch01_alone_apologize_text = format_choice("ch01_alone_apologize", "I'm glad I didn't make you uncomfortable." if not ch01_movie_pressed and not ch01_pressed_julian else "I think I pushed the joke too far.")
    $ ch01_alone_curiosity_text = format_choice("ch01_alone_curiosity", "I was curious how you'd react.")
    $ ch01_alone_open_text = format_choice("ch01_alone_open", "I liked watching you get nervous.")
    $ ch01_alone_dismiss_text = format_choice("ch01_alone_dismiss", "It was just messing around. Don't overthink it.")

    menu:
        "[ch01_alone_apologize_text]":
            $ apply_choice("ch01_alone_apologize")
            $ set_story_value("ch01_alone_movie_response", "apologized")
            if not ch01_movie_pressed and not ch01_pressed_julian:
                mc "I'm glad I didn't make you uncomfortable."
                gf "You didn't. Thank you for checking on me."
            else:
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
            "[girlfriend_name] opened her mouth to deny it, stopped, then looked down at her glass."
            gf "...A little."
            mc "Yeah?"
            gf "Don't make me regret admitting that."

        "[ch01_alone_dismiss_text]":
            $ apply_choice("ch01_alone_dismiss")
            $ set_story_value("ch01_alone_movie_response", "dismissed")
            mc "It was just messing around. Don't overthink it."
            "[girlfriend_name]'s thumb stopped moving against the glass."
            gf "Right."
            mc "What?"
            gf "Nothing. I'm tired."

    $ set_story_flag("ch01_scene_28_complete")
    jump ch01_scene_29_private_reflection


label ch01_scene_29_private_reflection:

    if get_story_value("ch01_julian_compliment_given", False):
        mc "What about when [friend_name] called you attractive?"
        gf "What about it?"
        mc "Did you like hearing it?"

        if partner_stats["curiosity"] < 25:
            gf "It was a compliment. Obviously it was nice."
        elif relationship_stats["boredom"] >= 16 and get_story_value("ch01_compliment_response") == "shrugged":
            "[girlfriend_name] hesitated longer than I expected."
            gf "Maybe."
            gf "He actually looked nervous saying it."
            mc "And?"
            gf "Nothing. It was just... nice."
        else:
            "[girlfriend_name] thought about it."
            gf "I think I liked that he was nervous saying it."
            mc "Why?"
            gf "I don't know. It made it feel... real, I guess."

    else:
        mc "Did you actually enjoy any of that tonight?"
        gf "Any of what?"
        mc "Being aware he was there."
        "[girlfriend_name] considered the question."
        if get_story_value("ch01_micro_test_response") == "knowingly_left":
            gf "I liked that it felt a little dangerous without anything actually happening."
        elif get_story_value("ch01_micro_test_response") in ("warned", "dismissed"):
            gf "Mostly I was embarrassed. You being there helped."
        else:
            gf "Maybe a little. I liked knowing I could decide what to do."

    $ ch01_private_claim_text = format_choice("ch01_private_claim", "That's okay. I still like knowing you're mine.")
    $ ch01_private_open_text = format_choice("ch01_private_open", "I liked seeing you enjoy the attention.")
    $ ch01_private_jealous_text = format_choice("ch01_private_jealous", "I'd be lying if I said I wasn't a little jealous.")
    $ ch01_private_indifferent_text = format_choice("ch01_private_indifferent", "Doesn't really matter to me either way.")

    menu:
        "[ch01_private_claim_text]":
            $ apply_choice("ch01_private_claim")
            $ set_story_value("ch01_private_attention_response", "claimed")
            mc "That's okay. I still like knowing you're mine."
            "[girlfriend_name] looked up at me."
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
            "[girlfriend_name]'s expression softened."
            gf "A little?"
            mc "A little."
            gf "Good."
            mc "Good?"
            gf "I don't want you feeling like you have to pretend."

        "[ch01_private_indifferent_text]":
            $ apply_choice("ch01_private_indifferent")
            $ set_story_value("ch01_private_attention_response", "indifferent")
            mc "Doesn't really matter to me either way."
            "[girlfriend_name] went still for a moment."
            gf "Oh."
            mc "What?"
            gf "Nothing."
            "She stood and picked up her glass."
            gf "Come on. I'm tired."

    $ set_story_flag("ch01_scene_29_complete")
    jump ch01_scene_30_end_day_one


# Compatibility labels retained for development saves created before Pacing Revision v2.
label ch01_scene_17_julian_notices:
    jump ch01_scene_18_private_under_blanket

label ch01_scene_24_looking_counts:
    jump ch01_scene_25_julian_put_on_spot


label ch01_scene_30_end_day_one:

    scene bg ch01_villa_bedroom_night
    with fade

    "We switched off the downstairs lights and finally headed upstairs."
    "[girlfriend_name] plugged her phone in beside the bed and climbed under the covers."

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
        set_story_flag("ch01_breakfast_reply_pending")
        clear_story_flag("ch01_breakfast_phone_session_active")

    "[girlfriend_name] checked the same message on her phone and laughed quietly."

    gf "He's dramatic."
    mc "He's correct."
    gf "Eleven-thirty."
    mc "Eleven-fifteen."
    gf "Eleven-thirty."
    mc "Fine."

    $ set_story_value("ch01_day1_nonchalant_count", chapter_nonchalant_count("ch01"))

    $ lc_day1_route_focus = lc_route_explorer_for_lane()
    if lc_day1_route_focus == "ntr_risk" or (
        lc_day1_route_focus is None
        and chapter_nonchalant_count("ch01") >= 3
        and (relationship_stats["boredom"] >= 15 or relationship_stats["love"] <= 48)
    ):
        $ set_story_value("ch01_day1_route_pressure", "ntr_seeded")
        "[girlfriend_name] put her phone down, but the small distance between us felt more noticeable than it had that morning."
        "[friend_name] had not done anything wrong. If anything changed from here, it would begin with the spaces I kept leaving open."
    elif lc_day1_route_focus == "exhibitionism" or (
        lc_day1_route_focus is None
        and nts_score() >= ntr_score() + 5
        and partner_stats["curiosity"] >= 24
    ):
        $ set_story_value("ch01_day1_route_pressure", "nts_seeded")
        "Somewhere during the day, a private joke between [girlfriend_name] and me had started acquiring a third point of reference."
        "Nothing had happened. The fact that nothing had happened was part of what made the possibility feel new."
    else:
        $ set_story_value("ch01_day1_route_pressure", "mixed")
        "Yesterday, [friend_name] had simply been my friend."
        "By the end of the day, he'd started becoming [girlfriend_name]'s friend too, and none of us had decided yet what that would mean."

    # Ryan falls asleep with the day's towel incident still somewhere in the back of his mind.
    # This is a dream, not a route lock: it combines the real accident with the
    # earlier discovery that the bedroom's only curtains are sheer.
    $ ch01_day1_love_ending = (
        get_story_value("ch01_day1_route_pressure") == "mixed"
        and relationship_stats["love"] >= 54
        and relationship_stats["trust"] >= 54
        and chapter_nonchalant_count("ch01") < 2
    )
    if ch01_day1_love_ending:
        "[girlfriend_name] settled against my shoulder before we fell asleep."
        gf "Today was good."
        mc "Even the part where the floor attacked you?"
        gf "Especially after you stopped making fun of me."
        "I kissed her forehead, and she reached for my hand beneath the covers."

    "At some point, I fell asleep."
    scene black
    with fade

    $ enter_cinematic_mode()
    scene cg ch01_dream_towel_replay
    with dissolve

    "I was back by the pool."
    "[girlfriend_name] stood upstairs again, wet hair over one shoulder and the same small towel wrapped around her."

    gf "Dinner is at seven!"
    friend "Six twenty-three."
    gf "Why are both of you still sitting there?"

    scene cg ch01_dream_towel_shift
    with dissolve

    "She stepped farther out. The towel shifted exactly the way I remembered."

    mc "[girlfriend_name]—"

    "Nothing came out."

    "I tried again. My mouth moved, but there was no sound."
    "She kept talking, completely unaware."

    "The towel rode a little higher as she turned back toward the bedroom."

    scene cg ch01_dream_towel_curtain
    with dissolve

    "Then she reached for the curtain and pulled it across the glass."

    "For a second, relief washed through me."

    "Then I remembered."

    "{i}These barely cover anything.{/i}"

    "The sheer fabric softened her outline. It did not hide it."

    scene cg ch01_dream_stranger_behind
    with dissolve

    "Behind the sheer curtain, [girlfriend_name] turned away from the window."
    "Someone was standing behind her."
    "The man from dinner."

    "There was no door opening. No footsteps. One moment she was alone; the next he was simply there."

    "{i}[girlfriend_name].{/i}"

    "Still no voice."

    scene cg ch01_dream_stranger_look
    with dissolve

    "Her eyes dropped immediately, following the same path they had at dinner."
    "This time, she didn't correct herself."

    "I tried to call her name again."
    "Nothing."

    scene cg ch01_dream_stranger_reach
    with dissolve

    "She stepped closer."
    "Slowly, almost experimentally, she reached toward him."
    "Her hand disappeared between their silhouettes—"

    scene black
    with dissolve

    $ exit_cinematic_mode()

    "My eyes opened."

    scene bg ch01_villa_bedroom_night
    with dissolve

    "[girlfriend_name] was asleep beside me, breathing softly, exactly where she'd been."

    "I stared at the ceiling for a moment."

    "{i}What the hell was that?{/i}"

    $ dream_ground_text = format_choice("ch01_dream_ground", "It was a dream. {} hadn't done anything.".format(girlfriend_name))
    $ dream_curiosity_text = format_choice("ch01_dream_curiosity", "Why did that bother me... and why couldn't I stop thinking about it?")
    $ dream_withdraw_text = format_choice("ch01_dream_withdraw", "Don't think about it. Don't make it a thing.")

    menu:
        "[dream_ground_text]":
            $ apply_choice("ch01_dream_ground")
            $ set_story_value("ch01_dream_response", "grounded")
            "I turned my head toward her."
            "She was asleep exactly where she'd been before my brain decided to invent the rest."
            "{i}It was a dream. [girlfriend_name] hadn't done anything.{/i}"
            "I let the image go instead of making it hers to answer for."

        "[dream_curiosity_text]":
            $ apply_choice("ch01_dream_curiosity")
            $ set_story_value("ch01_dream_response", "curious")
            "I shut my eyes again, but the last image stayed there."
            "{i}Why did that bother me... and why couldn't I stop thinking about it?{/i}"
            "Jealousy explained some of it. Not all of it."
            "I wasn't ready to put a name to the rest."

        "[dream_withdraw_text]":
            $ apply_choice("ch01_dream_withdraw")
            $ set_story_value("ch01_dream_response", "withdrew")
            "I looked away from her and pulled the sheet higher."
            "{i}Don't think about it. Don't make it a thing.{/i}"
            "There was nothing to confront her about, so I kept the feeling to myself."
            "It was easier than trying to understand why it had stayed with me."

    $ set_story_flag("ch01_day1_towel_dream_seen")
    $ set_story_flag("ch01_scene_30_complete")
    $ set_story_flag("ch01_day_01_complete")
    $ set_story_flag("ch01_scenes_14_30_complete")

    scene black
    with fade

    centered "{size=46}CHAPTER ONE — DAY ONE COMPLETE{/size}"

    if LC_DAY1_DEMO_BUILD:
        jump ch01_day1_demo_complete

    jump ch01_day2_start
