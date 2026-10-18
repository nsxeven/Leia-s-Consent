# Leia's Consent: Chapter One, Day Four, Scenes 9-16.
# Continues ch01_day4_scenes_01_08.rpy. Entry from scene 08: ch01_day4_scene_09_getting_ready.
# Ends at ch01_day4_scene_16_finish, which jumps to ch01_day5_start when that label exists.
#
# Route night (scene 13) splits into three labels. Scene 14 resolves each.
# All intimacy is NON-EXPLICIT: fade/cut to CG placeholder cards with artist TODOs.
# Exposure ladder for this chapter: covering (Day 2) -> brief, private (Day 4, this file)
# -> comfortable, private (Day 5) -> deliberate display with an off-ramp (Day 6).

label ch01_day4_scene_09_getting_ready:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")
    $ d4_src = get_story_value("ch01_d2_mall_outfit_source", "leia")

    scene bg ch01_master_bedroom
    with fade

    if d4_src == "ryan":
        $ d4_own_line = "You bought it. So technically this is your fault."
    elif d4_src == "leia":
        $ d4_own_line = "I bought it myself. So technically this is nobody's fault but mine."
    else:
        $ d4_own_line = "It's been in the boutique bag since the boutique."

    python:
        phone_add_message(
            "maya", "maya",
            text="Dinner terrace, eight. Dress code: look like you're being photographed by someone who loves you. Advice is billable. I charge by the hour.",
            message_id="ch01_d4_maya_dress_code",
            mark_unread=True, notify=True, notification_title="Maya",
        )

    "The afternoon bled out into the amber light that made everything look expensive."
    "My phone buzzed with Maya's dress code. Leia read it over my shoulder."

    if d4_lane == "love":
        gf "Look photographed by someone who loves you."
        mc "That's a high bar."
        gf "You've been clearing it all day."
        "She turned to the bed, where three outfits waited: the Resort Dinner Dress, the loose low-cut top and fitted skirt, and the Black Cutout Mini in its boutique bag."
        gf "[d4_own_line]"
        gf "Help me pick?"

        $ d4_du_ryan = format_choice("ch01_d4_dusk_ryan_picks", "Let me choose your outfit.")
        $ d4_du_leia = format_choice("ch01_d4_dusk_leia_decides", "Wear whatever you feel best in.")

        menu:
            "[d4_du_ryan]":
                $ apply_choice("ch01_d4_dusk_ryan_picks")
                python:
                    d4_dusk_options = ch01_d4_dusk_outfit_options()
                    d4_dusk_pick = renpy.call_screen(
                        "leia_love_outfit_picker",
                        options=d4_dusk_options,
                        title_text="Pick Leia's Day Four dinner outfit",
                    )
                    love_route_wear_request(d4_dusk_pick, route_lane="love")
                    set_story_value("ch01_d4_dusk_outfit_id", d4_dusk_pick)
                    set_story_value("ch01_d4_dusk_outfit_source", "ryan")

                mc "Wear the [outfit_name(d4_dusk_pick)]."
                if d4_dusk_pick == "boutique_cutout_mini":
                    gf "Okay. The mini."
                    gf "Hold that thought. And my hand, a little tighter than usual."
                elif love_outfit_is_daring(d4_dusk_pick):
                    gf "Brave. I like it."
                else:
                    gf "Elegant and a little bit unfair. Good call."
                "She accepted the choice because she had invited it."

            "[d4_du_leia]":
                $ apply_choice("ch01_d4_dusk_leia_decides")
                mc "Wear whatever you feel best in."
                gf "Then I'm choosing the dress. It likes me."
                $ d4_wore = ch01_d4_wear("resort_dinner_dress")
                $ set_story_value("ch01_d4_dusk_outfit_id", "resort_dinner_dress")
                $ set_story_value("ch01_d4_dusk_outfit_source", "leia")
                "She smiled as if I'd passed a test she hadn't told me about."

    elif d4_lane == "exhibitionism":
        gf "Look photographed by someone who loves you."
        mc "That's a high bar."
        gf "You've been clearing it all day."
        "She held up the Resort Dinner Dress in one hand and the Black Cutout Mini in the other."
        gf "[d4_own_line]"
        gf "Dress or mini?"

        $ d4_du_bold = format_choice("ch01_d4_dusk_bolder", "The mini.")
        $ d4_du_comf = format_choice("ch01_d4_dusk_comfort", "The dress. It likes you.")

        menu:
            "[d4_du_bold]":
                $ apply_choice("ch01_d4_dusk_bolder")
                mc "The mini."
                $ d4_wore = ch01_d4_wear("boutique_cutout_mini")
                if d4_wore:
                    gf "It's loud, and it's a little bit too much."
                    gf "And I like that it's mine to wear."
                    $ set_story_value("ch01_d4_dusk_outfit_id", "boutique_cutout_mini")
                    $ set_story_value("ch01_d4_dusk_outfit_source", "ryan")
                    "She gave a small, slow smile. Not the one for the table. The one for me."
                else:
                    gf "Not tonight."
                    gf "I want to. I'm just not there. Give me time and a dark room."
                    mc "Take all of it."
                    $ outfit_gate_text = outfit_requirement_text("boutique_cutout_mini")
                    if outfit_gate_text:
                        centered "[outfit_gate_text]"
                    $ d4_wore = ch01_d4_wear("d2_loose_low_cut")
                    $ set_story_value("ch01_d4_dusk_outfit_id", "d2_loose_low_cut")
                    $ set_story_value("ch01_d4_dusk_outfit_source", "leia_declined_mini")
                    gf "The loose one, then. Compromise. Don't look so heartbroken."
                    mc "I contain it well."

            "[d4_du_comf]":
                $ apply_choice("ch01_d4_dusk_comfort")
                mc "The dress. It likes you."
                gf "It does. I'm told it has good taste."
                $ d4_wore = ch01_d4_wear("resort_dinner_dress")
                $ set_story_value("ch01_d4_dusk_outfit_id", "resort_dinner_dress")
                $ set_story_value("ch01_d4_dusk_outfit_source", "ryan")

    else:
        "Leia took the dress code the way she'd taken everything that day, as a problem she intended to solve on her own."
        $ d4_fine_n = get_story_value("ch01_d4_ntr_fine_count", 0)
        if d4_fine_n >= 2:
            $ d4_wore = ch01_d4_wear("boutique_cutout_mini")
        else:
            $ d4_wore = False
        if d4_wore:
            $ set_story_value("ch01_d4_dusk_outfit_id", "boutique_cutout_mini")
            "She lifted the Black Cutout Mini from its bag."
            gf "[d4_own_line]"
            "She didn't ask me. I didn't offer."
        else:
            $ d4_wore = ch01_d4_wear("resort_dinner_dress")
            $ set_story_value("ch01_d4_dusk_outfit_id", "resort_dinner_dress")
            "She took the Resort Dinner Dress and left the Black Cutout Mini in its bag, folded. The way she folded it said she hadn't decided."
        $ set_story_value("ch01_d4_dusk_outfit_source", "leia")
        mc "You look..."
        gf "Don't."
        mc "I was going to say you look like yourself."
        gf "That's a better answer than the one I expected."

    $ set_story_value("ch01_d4_dusk_daring", love_outfit_is_daring(get_story_value("ch01_d4_dusk_outfit_id", "resort_dinner_dress")))
    $ set_story_flag("ch01_d4_scene_09_complete")
    jump ch01_day4_scene_10_dinner


label ch01_day4_scene_10_dinner:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")
    $ d4_style = get_story_value("ch01_d4_photo_style", "none")

    scene bg ch01_d4_dinner_terrace
    with fade

    # AUDIO TODO: restaurant murmur, string-light hum, distant surf.
    "The terrace restaurant sat on a roof above the harbor, string lights looped between the rail posts, the sea gone dark and soft below."
    "Maya and Julian were already at the table. Julian stood when Leia arrived, like he'd been taught to, and then looked embarrassed that he had."
    maya "Look at you."
    gf "Look at us."
    maya "I'm very good at telling people they look good."
    friend "She's contractually obligated."

    if get_story_value("ch01_d4_hunt_winner") == "maya_julian":
        "I picked up the bill when it came, which was the deal."
        friend "I'd like to thank the academy."
        maya "He's going to say that every year."
    else:
        "Julian winced at the prices and pushed the menu back toward the middle."
        friend "I'm going to appeal."
        maya "Appeal denied. Order the lobster."
        friend "The lobster has claws."
        maya "It's a lobster."

    "Julian ordered for Maya without looking at the menu, a dessert she hadn't mentioned out loud. She noticed and pretended she hadn't."

    if d4_lane == "love":
        gf "I like this."
        mc "Dinner?"
        gf "Still. Us. I said it at sunset and I meant it. I still mean it."
    elif d4_lane == "exhibitionism":
        "Leia caught my eye over the candle."
        gf "What I said at sunset. It's still true."
        mc "Which part?"
        gf "I think part of why I liked it was because you knew."
        "Maya looked between the two of us and decided, wisely, to find the bread very interesting."
    else:
        "Leia's phone sat face down beside her plate."
        "Twice she picked it up, typed, and put it down again. I watched her thumbs."
        "I told myself she was texting her sister. I told myself a lot of things."

    maya "Toast. One true thing. No explanations."
    friend "I hate this game."
    maya "You've hated every game and you've enjoyed all of them."

    $ d4_t_leia = format_choice("ch01_d4_toast_leia", "To Leia, who made me laugh before the first coffee.")
    $ d4_t_group = format_choice("ch01_d4_toast_group", "To the four of us, and the bee that started it.")
    $ d4_t_dare = format_choice("ch01_d4_toast_dare", "To bad ideas that turned out fine.")

    menu:
        "[d4_t_leia]":
            $ apply_choice("ch01_d4_toast_leia")
            mc "To Leia, who made me laugh before the first coffee."
            gf "That's not a toast. That's a weapon."
            maya "It's a very good toast."
            "Leia's hand found mine under the table without her looking."
            if d4_lane == "ntr":
                "I felt her squeeze once and then hesitate, as if she'd forgotten whether she was allowed."

        "[d4_t_group]":
            $ apply_choice("ch01_d4_toast_group")
            mc "To the four of us, and the bee that started it."
            friend "I'd like it known I'm not toasting the bee."
            maya "He's toasting the bee. He's just scared."
            gf "To the bee."
            friend "I take it back. All of it."

        "[d4_t_dare]":
            $ apply_choice("ch01_d4_toast_dare")
            mc "To bad ideas that turned out fine."
            maya "I love that for us."
            gf "Name one."
            mc "The swim rings."
            friend "I was wedged."
            gf "And you survived."
            "Maya raised her glass at Leia, a small, private salute that I decided not to ask about."

    "The food arrived in waves, as it does, and the conversation fell into the easy shape of four people who'd quietly decided to keep each other."

    if d4_style == "candid" or d4_style == "posed" or d4_style == "swap":
        gf "Ryan, send me the photo from the market."
        mc "Which one?"
        if d4_style == "candid":
            gf "The one where I'm laughing. I keep looking at it. I look like someone who's having a good time."
            mc "You were."
        elif d4_style == "posed":
            gf "The sunglasses one. The eyebrow is doing a lot of work."
            mc "It's the star."
        else:
            gf "Both. The honey one is for the box."
            mc "You and your box."
        python:
            phone_add_message(
                "leia", "leia",
                text="Your toast was good. Do not tell Maya I said so.",
                message_id="ch01_d4_leia_dinner_toast",
                mark_unread=True, notify=False,
            )
    else:
        "Maya asked to see the market photos on the group chat. Leia pulled up the one Maya had taken and said it was fine, and then showed no one else."

    $ set_story_flag("ch01_d4_scene_10_complete")
    jump ch01_day4_scene_11_dusk_walk


label ch01_day4_scene_11_dusk_walk:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    scene bg ch01_d4_dusk_path
    with fade

    "We walked back in the blue hour with the lanterns coming on one by one."
    maya "We're going to take the cliff path."
    gf "The cliff path is the long way."
    maya "That's the point. Julian and I are going to look at lights."
    friend "I was told there would be lights."
    maya "There are lights, and we are going to look at them. For one hour. Possibly two. Don't wait up."
    "Julian looked at me, then at the ground. He didn't look at Leia at all."
    friend "We'll be careful."
    mc "It's a cliff path. Be careful."
    friend "That's what I said."

    "They turned off into the dark with Maya's laugh trailing behind them."

    if d4_lane == "love":
        "Leia leaned her head against my arm as we walked, whatever she was wearing suddenly the least important thing about her."
        gf "That was a good day."
        mc "It was."
        gf "No, I mean it was a good day. I'm trying to remember how we got here."
        mc "Pancakes."
        gf "Pancakes and a bee."
        "We laughed. The sound of it stayed on the path behind us a little longer than we did."
    elif d4_lane == "exhibitionism":
        "Leia slowed as we reached the villa gate."
        gf "I've been thinking about something all afternoon."
        mc "Yeah?"
        gf "I'm not going to say it. You'll know when we get upstairs. Your face will tell me."
        mc "My face?"
        gf "It's very easy to read."
        "She pushed the gate open, then looked back with the clip in her hair catching the lantern light."
    else:
        "Neither of us said anything for the first half of the walk."
        "Somewhere near the gate Leia stopped, took out her phone, checked it, and put it away."
        gf "Sorry."
        mc "Everything okay?"
        gf "Yeah. No. Can we talk when we get in?"
        mc "Sure."
        "She nodded once, the way you nod when you've decided something and haven't yet decided how."

    $ set_story_flag("ch01_d4_scene_11_complete")
    jump ch01_day4_scene_12_route_split


label ch01_day4_scene_12_route_split:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    # Legibility: in Insight / Full / Developer the player is told which kind of night this is.
    if current_choice_mode() != "normal":
        if d4_lane == "love":
            centered "Tonight: private. Your choices lean Love."
        elif d4_lane == "exhibitionism":
            centered "Tonight: one small step up, shared. 'Keep it just us' is always available."
        else:
            centered "Tonight: a repair gate. Honesty returns you to Love. Distance deepens NTR."

    $ set_story_flag("ch01_d4_scene_12_complete")

    if d4_lane == "exhibitionism":
        jump ch01_day4_scene_13_exhib_night
    elif d4_lane == "ntr":
        jump ch01_day4_scene_13_ntr_night
    else:
        jump ch01_day4_scene_13_love_night


label ch01_day4_scene_13_love_night:

    scene bg ch01_villa_kitchen_night
    with fade

    $ d4_style = get_story_value("ch01_d4_photo_style", "none")

    "The villa was quiet, the way it gets when everyone has somewhere better to be."
    "Leia put her phone on the counter, found a slow song, and turned the volume down until it was barely there."
    gf "Dance with me. Badly."
    mc "I'm excellent at bad."
    gf "I know. It's one of your best qualities."

    $ d4_l_dance = format_choice("ch01_d4_love_slow_dance", "Pull her in and dance. Badly. Slowly.")
    $ d4_l_stay = format_choice("ch01_d4_love_terrace_stay", "Take her out to the terrace and talk first.")
    $ d4_l_open = format_choice("ch01_d4_love_open_door", "Tell her how brave she was today, and that I'd want to know if she ever wanted braver.")

    menu:
        "[d4_l_dance]":
            $ apply_choice("ch01_d4_love_slow_dance")
            $ set_story_value("ch01_d4_end_variant", "love_slow_dance")

            $ enter_cinematic_mode()
            scene cg ch01_d4_love_night_01
            with dissolve
            # CG TODO (artist): ch01_d4_love_night_01. Ryan POV, Ryan never in frame. See visuals file.
            "We danced in the half-dark kitchen, badly, her forehead against my jaw."
            "She kept time to a song that ended and started again and neither of us reached for the phone."

            if d4_style == "candid":
                gf "I looked at that photo for ten minutes."
                mc "Which one?"
                gf "The laughing one. I don't look like someone who's been told what to feel."
                gf "I look like someone you were paying attention to."

        "[d4_l_stay]":
            $ apply_choice("ch01_d4_love_terrace_stay")
            $ set_story_value("ch01_d4_end_variant", "love_terrace_talk")

            scene bg ch01_d4_terrace_night
            with dissolve
            "We took the quiet out onto the terrace, where the night was warm and the path below was empty."
            gf "Can I tell you what I want this week?"
            mc "Please."
            gf "More of this. And some things I haven't named yet. Small ones."
            gf "Not tonight. Just so you know I know."
            mc "I'm glad you told me."
            gf "I'm glad you're the person I tell."

            $ enter_cinematic_mode()
            scene cg ch01_d4_love_night_01
            with dissolve
            # CG TODO (artist): ch01_d4_love_night_01. Ryan POV, Ryan never in frame.
            "She leaned into me and the song from her phone drifted out from inside. It didn't need to be anything more than that."

        "[d4_l_open]":
            $ apply_choice("ch01_d4_love_open_door")
            $ set_story_value("ch01_d4_end_variant", "love_open_door")
            $ set_story_flag("ch01_d4_love_exhib_seed")

            mc "You were brave today. In the little ways."
            gf "The sunglasses?"
            mc "The sunglasses. The honey. The eyebrow."
            gf "I felt very brave about the eyebrow."
            mc "If you ever want to be braver, I'd want to know."
            gf "Before? Or after?"
            mc "Before. So I can be there."
            "She was quiet for a moment, then smiled, small and private."
            gf "Okay. Together. I'm not promising anything."
            mc "I'm not asking for anything."
            gf "That's what makes it possible."

            $ enter_cinematic_mode()
            scene cg ch01_d4_love_night_01
            with dissolve
            # CG TODO (artist): ch01_d4_love_night_01. Ryan POV, Ryan never in frame.
            "She pulled me close, and for a while there was nothing to think about at all."

    # Fade to the implied beat. NOTHING explicit is shown.
    scene cg ch01_d4_love_night_02
    with dissolve
    # CG TODO (artist): ch01_d4_love_night_02. Ryan POV, Ryan never in frame. Fade card. Curtains drawn, lamplight, Leia's hand at the lamp only.
    "She switched off the lamp. We took the rest of the night slowly, and quietly, with the curtains drawn."
    $ exit_cinematic_mode()

    if d4_style != "skipped" and get_story_value("ch01_d4_dusk_outfit_id") == "boutique_cutout_mini" and get_story_value("ch01_d4_dusk_outfit_source") == "ryan":
        $ set_story_flag("ch01_d4_love_mini_thanks")

    $ set_story_value("ch01_d4_end_route_pending", "love")
    $ set_story_flag("ch01_d4_scene_13_complete")
    jump ch01_day4_scene_14_night_after


label ch01_day4_scene_13_exhib_night:

    scene bg ch01_d4_terrace_night
    with fade

    $ d4_style = get_story_value("ch01_d4_photo_style", "none")

    "Leia went into the bedroom alone and came out a minute later in the cream wrap she'd packed for slow mornings, tied loosely at the waist."
    gf "Terrace."
    "She took my hand and led me through the glass doors, past the potted lemon tree, to the rail."
    "Below, the beach path ran pale in the dark. A couple were a long way off, small as chess pieces, not looking up."
    gf "Last night I was the one under the window."
    gf "Tonight I wanted to be the one who chose the window."
    mc "I like that."
    gf "I know. That's partly why."

    $ d4_x_together = format_choice("ch01_d4_exhib_together", "Stay beside her. She sets the pace.")
    $ d4_x_watching = format_choice("ch01_d4_exhib_like_watching", "Tell her I like watching her get noticed.")
    $ d4_x_private = format_choice("ch01_d4_exhib_private", "Keep this one just for us. Close the doors.")

    menu:
        "[d4_x_together]":
            $ apply_choice("ch01_d4_exhib_together")
            $ set_story_value("ch01_d4_exhib_variant", "shared_step")
            mc "Your pace. I'm right here."
            gf "That's all I wanted."
            jump ch01_day4_exhib_step

        "[d4_x_watching]":
            $ apply_choice("ch01_d4_exhib_like_watching")
            $ set_story_value("ch01_d4_exhib_variant", "ryan_likes_watching")
            $ set_story_flag("ch01_d4_exhib_ryan_likes_watching")
            mc "I like watching you get noticed."
            "It came out lower than I meant it to."
            gf "Say that again."
            mc "I like watching you get attention. Not instead of me. With me watching."
            gf "You really do, don't you."
            mc "It turns out I do."
            "She took that in slowly, her hand tightening on the rail, and I understood I'd handed her something: not a favour, a decision."
            gf "So how far do I take it?"

            $ d4_x_hercall = format_choice("ch01_d4_exhib_her_call", "Your call. However far you want to take it.")
            $ d4_x_tease = format_choice("ch01_d4_exhib_tease_then_me", "Tease them, then come back to me.")

            menu:
                "[d4_x_hercall]":
                    $ apply_choice("ch01_d4_exhib_her_call")
                    mc "Your call. However far you want to take it."
                    gf "I'm taking my time."
                    $ set_story_value("ch01_d4_exhib_framing", "her_call")
                "[d4_x_tease]":
                    $ apply_choice("ch01_d4_exhib_tease_then_me")
                    mc "Tease them. Then come back to me."
                    gf "That's a very specific instruction."
                    mc "It's a very specific night."
                    $ set_story_value("ch01_d4_exhib_framing", "tease_then_me")

            jump ch01_day4_exhib_step

        "[d4_x_private]":
            $ apply_choice("ch01_d4_exhib_private")
            $ set_story_value("ch01_d4_exhib_variant", "opt_out_private")
            $ set_story_value("ch01_d4_end_variant", "exhib_private_optout")
            mc "Keep this one just for us."
            "Her shoulders loosened as if she'd been carrying a heavy bag she'd forgotten to put down."
            gf "Thank you for not making me explain."
            mc "I don't need an explanation."
            gf "I know. That's why I want to give you one anyway."
            gf "I didn't stop wanting it. I just wanted tonight to be only us."
            mc "Then it's only us."
            gf "I'll tell you when I want the window back."
            "She stepped inside, and I pulled the glass doors closed behind us."

            $ enter_cinematic_mode()
            scene cg ch01_d4_love_night_02
            with dissolve
            # CG TODO (artist): ch01_d4_love_night_02. Ryan POV, Ryan never in frame. Reuses the Love fade card.
            "The curtains came across with a whisper, and the night belonged to the two of us."
            $ exit_cinematic_mode()

            $ set_story_value("ch01_d4_end_route_pending", "love")
            $ set_story_flag("ch01_d4_scene_13_complete")
            jump ch01_day4_scene_14_night_after


label ch01_day4_exhib_step:

    # Leia decides how far to go. Both outcomes are a positive step. The threshold is
    # her own Exhibitionism stat, and it is shown in Full / Developer modes.
    python:
        d4_ex_now = partner_stats["exhibitionism"]
        d4_ex_framing = get_story_value("ch01_d4_exhib_framing", "own_pace")
        if d4_ex_now >= D4_EXHIBITION_BRIEF_REVEAL_MIN:
            d4_ex_call = "brief_reveal"
        else:
            d4_ex_call = "cover_tease"
        set_story_value("ch01_d4_leia_call", d4_ex_call)
        d4_ex_variant = get_story_value("ch01_d4_exhib_variant", "shared_step")

    if current_choice_mode() == "developer":
        centered "LEIA'S CALL: Exhibitionism [d4_ex_now] / [D4_EXHIBITION_BRIEF_REVEAL_MIN] -> [d4_ex_call]"
    elif current_choice_mode() == "full":
        centered "Leia decides how far she goes. Brief reveal needs Exhibitionism [D4_EXHIBITION_BRIEF_REVEAL_MIN]. Current: [d4_ex_now]."
    elif current_choice_mode() == "insight":
        centered "Leia decides how far she goes, based on her own confidence."

    if d4_ex_variant == "ryan_likes_watching":
        $ enter_cinematic_mode()
        scene cg ch01_d4_exhib_watching
        with dissolve
        # CG TODO (artist): ch01_d4_exhib_watching. Ryan POV, Ryan never in frame. Sub-variant 'Ryan likes watching'. Covered.
        "I stood behind her at the rail with my chin near her shoulder. We looked at the same lights."
        "I watched her decide."
        $ exit_cinematic_mode()
        scene bg ch01_d4_terrace_night
        with dissolve

    if d4_ex_call == "cover_tease":
        $ enter_cinematic_mode()
        scene cg ch01_d4_exhib_terrace_01
        with dissolve
        # CG TODO (artist): ch01_d4_exhib_terrace_01. Ryan POV, Ryan never in frame. COVERED tease frame.
        "Leia let the wrap slip off one shoulder, slowly. She held it closed at the front with both hands and looked back at me over the bare shoulder."
        "Down on the path, the couple turned a corner and were gone."
        gf "That's as far as I'm going tonight."
        gf "I wanted to see if I could do that much and still be me."
        "She laughed, delighted at her own nerve, and pulled the wrap back up."
        $ exit_cinematic_mode()
        $ set_story_value("ch01_d4_exposure_step", "covered_tease")
        $ set_story_flag("ch01_d4_exhib_tease_done")
    else:
        $ enter_cinematic_mode()
        scene cg ch01_d4_exhib_terrace_02
        with dissolve
        # CG TODO (artist): ch01_d4_exhib_terrace_02. Ryan POV, Ryan never in frame. BRIEF, implied, non-explicit. See visuals file.
        "Leia stood very straight at the rail. Then she opened the wrap, eyes on me and not on the path, for one slow heartbeat."
        gf "One."
        "She closed it again, her whole face lit."
        gf "Two. I counted."
        "Her hands were shaking a little. Her smile wasn't."
        $ exit_cinematic_mode()
        $ set_story_value("ch01_d4_exposure_step", "brief_reveal")
        $ set_story_flag("ch01_d4_exhib_brief_done")

    scene bg ch01_d4_terrace_night
    with dissolve

    if d4_ex_variant == "ryan_likes_watching":
        gf "You liked that I looked at you the whole time."
        mc "I liked that you were the one deciding."
        gf "Good answer."
        gf "If that stops being fun for me, I'll say so. Loudly."
        mc "I'd expect nothing less."
        if d4_ex_framing == "tease_then_me":
            gf "And I came back to you."
            mc "You did."
            gf "That was the best part."
    else:
        gf "I'm going to need a minute, a glass of water and a new personality."
        mc "I'll get the water."
        gf "Get the personality too."

    "She leaned against me, warm in the thin wrap, and the beach path stayed empty."

    $ enter_cinematic_mode()
    scene cg ch01_d4_love_night_02
    with dissolve
    # CG TODO (artist): ch01_d4_love_night_02. Ryan POV, Ryan never in frame. Fade card. Hand at the lamp only. Doors closed, curtains drawn.
    "We went inside. She drew the curtains, and we took the rest of the night slowly, and out of anyone's sight."
    $ exit_cinematic_mode()

    $ set_story_value("ch01_d4_end_variant", "exhib_" + d4_ex_variant)
    $ set_story_value("ch01_d4_end_route_pending", "exhibitionism")
    $ set_story_flag("ch01_d4_scene_13_complete")
    jump ch01_day4_scene_14_night_after


label ch01_day4_scene_13_ntr_night:

    scene bg ch01_d4_terrace_night
    with fade

    $ d4_disclosed = has_story_flag("ch01_d4_cutout_disclosed")
    $ d4_pressed = has_story_flag("ch01_d4_ntr_pressed_early")
    $ d4_fine_n = get_story_value("ch01_d4_ntr_fine_count", 0)

    "Leia was already out on the terrace when I came up, sitting on the low wall with the hairclip open in her hands."
    "She turned it over once. She didn't put it on."

    $ enter_cinematic_mode()
    scene cg ch01_d4_ntr_terrace_talk
    with dissolve
    # CG TODO (artist): ch01_d4_ntr_terrace_talk. Ryan POV, Ryan never in frame. Quiet. No third person in frame.
    $ exit_cinematic_mode()

    scene bg ch01_d4_terrace_night
    with dissolve

    if d4_disclosed:
        gf "I told you what I could this afternoon."
        gf "I said I'd tell you the rest tomorrow. I will."
        gf "But I can't say it if you look at me like that. How are you looking at me?"
        jump ch01_day4_ntr_gate_disclosed

    if d4_pressed:
        gf "You asked me this afternoon like you wanted to catch me."
        gf "I'd like to try again, if you'll let me."
    else:
        gf "Can I tell you something, and have you let me finish?"

    "I knew it was the third time she'd opened a door that day."

    $ d4_g_reconnect = format_day4_gate_choice("ch01_d4_ntr_gate_reconnect", "I'm listening. All of it, whenever you're ready.", severity="soft", gate_label="D4-3")
    $ d4_g_accuse = format_day4_gate_choice("ch01_d4_ntr_gate_accuse_hard", "What did you do yesterday?", severity="hard", gate_label="D4-3")
    $ d4_g_withdraw = format_day4_gate_choice("ch01_d4_ntr_gate_withdraw_hard", "I'm fine.", severity="hard", gate_label="D4-3")

    menu:
        "[d4_g_reconnect]":
            $ apply_choice("ch01_d4_ntr_gate_reconnect")
            mc "I'm listening. All of it, whenever you're ready."
            "Leia looked at me as if I'd handed her something she'd stopped expecting."
            call ch01_day4_ntr_disclosure
            $ set_story_value("ch01_d4_disclosure_when", "night_gate")
            jump ch01_day4_ntr_react_menu

        "[d4_g_accuse]":
            $ apply_choice("ch01_d4_ntr_gate_accuse_hard")
            $ set_story_value("ch01_d4_ntr_confirmed", True)
            $ set_story_value("ch01_d4_ntr_outcome", "ntr_unresolved")
            mc "What did you do yesterday?"
            "Leia stared at me, suddenly cold."
            gf "That's what you want to ask me."
            mc "I'm asking."
            gf "Something happened at the stand. Something I would have told you if you'd asked what it was."
            gf "You asked what I did. That's not the same question."
            mc "Then what's the question?"
            gf "That's what I was waiting for you to find."
            "She closed the clip. It clicked louder than it should have."
            gf "I'm going to bed."
            "She went inside. I stayed on the terrace long enough for the lights to feel too bright."
            $ set_story_flag("ch01_d4_cutout_partial")

        "[d4_g_withdraw]":
            $ apply_choice("ch01_d4_ntr_gate_withdraw_hard")
            $ set_story_value("ch01_d4_ntr_confirmed", True)
            $ set_story_value("ch01_d4_ntr_outcome", "ntr_confirmed")
            $ set_story_value("ch01_d4_ntr_fine_count", d4_fine_n + 1)
            mc "I'm fine."
            "Leia watched me for a long few seconds."
            "It was the same answer I'd given her all day."
            gf "...Okay."
            "She didn't push. She put the hairclip in her pocket instead of her hair."
            gf "I'm going to bed."
            "She went inside. I let her."

    jump ch01_day4_ntr_gate_resolved


label ch01_day4_ntr_gate_disclosed:

    $ d4_react_thanks = format_choice("ch01_d4_ntr_react_thanks", "Like someone who's glad you told me. The secret hurt more than the story.")
    $ d4_react_boundary = format_choice("ch01_d4_ntr_react_boundary", "Like someone who needs to hear it before it happens next time.")
    $ d4_react_curious = format_choice("ch01_d4_ntr_react_curious", "Like someone still working out how he feels. Tell me what it felt like.")
    $ d4_react_fine = format_day4_gate_choice("ch01_d4_ntr_gate_withdraw_hard", "I'm fine.", severity="hard", gate_label="D4-3")

    menu:
        "[d4_react_thanks]":
            $ apply_choice("ch01_d4_ntr_react_thanks")
            $ set_story_value("ch01_d4_ntr_react", "thanks")
            jump ch01_day4_ntr_react_resolve
        "[d4_react_boundary]":
            $ apply_choice("ch01_d4_ntr_react_boundary")
            $ set_story_value("ch01_d4_ntr_react", "boundary")
            jump ch01_day4_ntr_react_resolve
        "[d4_react_curious]":
            $ apply_choice("ch01_d4_ntr_react_curious")
            $ set_story_value("ch01_d4_ntr_react", "curious")
            jump ch01_day4_ntr_react_resolve
        "[d4_react_fine]":
            $ apply_choice("ch01_d4_ntr_gate_withdraw_hard")
            $ set_story_value("ch01_d4_ntr_confirmed", True)
            $ set_story_value("ch01_d4_ntr_outcome", "ntr_confirmed")
            $ set_story_value("ch01_d4_ntr_fine_count", get_story_value("ch01_d4_ntr_fine_count", 0) + 1)
            mc "I'm fine."
            "Leia flinched as if the words had weight."
            gf "She told you something real, and you said fine."
            "She wasn't angry. That was the worst part."
            gf "Goodnight, Ryan."
            "She went inside and I stayed with a gate I had closed myself."
            jump ch01_day4_ntr_gate_resolved


label ch01_day4_ntr_react_menu:

    $ d4_react_thanks = format_choice("ch01_d4_ntr_react_thanks", "Thank you for telling me. The secret hurt more than the story.")
    $ d4_react_boundary = format_choice("ch01_d4_ntr_react_boundary", "I need you to tell me next time, before it happens.")
    $ d4_react_curious = format_choice("ch01_d4_ntr_react_curious", "I'm still working out how I feel. Tell me what it felt like.")

    "She waited. The terrace lights hummed. I understood she was waiting for me to say something she could live with."

    menu:
        "[d4_react_thanks]":
            $ apply_choice("ch01_d4_ntr_react_thanks")
            $ set_story_value("ch01_d4_ntr_react", "thanks")
            mc "Thank you for telling me. The secret hurt more than the story."
            gf "That's fair. It hurt me too."
            jump ch01_day4_ntr_react_resolve
        "[d4_react_boundary]":
            $ apply_choice("ch01_d4_ntr_react_boundary")
            $ set_story_value("ch01_d4_ntr_react", "boundary")
            mc "I need you to tell me next time, before it happens. Not after."
            gf "Okay. Before. I can do before."
            jump ch01_day4_ntr_react_resolve
        "[d4_react_curious]":
            $ apply_choice("ch01_d4_ntr_react_curious")
            $ set_story_value("ch01_d4_ntr_react", "curious")
            mc "I'm still working out how I feel. Tell me what it felt like."
            gf "Scary. And good. And I hated that it was good."
            gf "Ask me again when we both know what to do with that."
            jump ch01_day4_ntr_react_resolve


label ch01_day4_ntr_react_resolve:

    $ d4_react = get_story_value("ch01_d4_ntr_react", "thanks")

    "Leia closed her eyes for a moment, and when she opened them she looked ten pounds lighter."
    gf "Thank you."
    "She stood, put the hairclip back in her hair, and took my hand."
    gf "I don't have it all figured out."
    mc "Neither do I."
    gf "But I'd like to stop figuring it out by myself."

    $ set_story_value("ch01_d4_ntr_outcome", "love_repaired")
    $ set_story_value("ch01_d4_ntr_repaired", True)
    if d4_react == "boundary":
        $ set_story_flag("ch01_d4_ntr_boundary_set")
    elif d4_react == "curious":
        $ set_story_flag("ch01_d4_ntr_repaired_curious")
    jump ch01_day4_ntr_gate_resolved


label ch01_day4_ntr_gate_resolved:

    $ d4_outcome_text = get_story_value("ch01_d4_ntr_outcome", "ntr_confirmed")
    if get_story_value("ch01_d4_ntr_confirmed", False):
        if current_choice_mode() == "developer":
            centered "NTR HARD GATE D4-3 - ch01_d4_ntr_confirmed = True, outcome = [d4_outcome_text]"
        elif current_choice_mode() == "full":
            centered "NTR route deepened."
        elif current_choice_mode() == "insight":
            centered "A major route boundary has been crossed."
        else:
            centered "Something changed tonight."

    $ set_story_value("ch01_d4_end_route_pending", get_story_value("ch01_d4_ntr_outcome", "ntr_confirmed"))
    $ set_story_flag("ch01_d4_scene_13_complete")
    jump ch01_day4_scene_14_night_after


label ch01_day4_scene_14_night_after:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")
    $ d4_pending = get_story_value("ch01_d4_end_route_pending", "love")

    scene bg ch01_villa_bedroom_night
    with fade

    if d4_lane == "love":
        "Afterward Leia lay with her head on my shoulder and her phone on the pillow, the screen dark."
        gf "Maya's going to text in the morning."
        mc "About what?"
        gf "About everything. She has a talent."
        mc "And you'll answer?"
        gf "I'll answer with the eyebrow."
        if has_story_flag("ch01_d4_love_mini_thanks"):
            gf "And thank you for the mini. I felt like I could be someone for an hour."
            mc "You were always someone."
            gf "A different someone. A fun one."
        if has_story_flag("ch01_d4_love_exhib_seed"):
            gf "And I meant what I said. If I ever want braver, I'll tell you first."
            mc "I'll hold you to that."
            gf "I'm counting on it."
        gf "Goodnight."
        mc "Goodnight."

    elif d4_lane == "exhibitionism":
        $ d4_xv = get_story_value("ch01_d4_exhib_variant", "shared_step")
        if d4_xv == "opt_out_private":
            "Leia lay with her head on my chest."
            gf "I didn't stop wanting it, you know."
            mc "I know."
            gf "Just tonight was too good to share."
            mc "That's the nicest thing anyone's said about me."
            gf "It's about us. Don't make it about you."
            "She was smiling in the dark."
        else:
            "Leia lay on her side, one hand under her cheek, studying me."
            gf "I think I surprised myself."
            mc "Me too."
            if d4_xv == "ryan_likes_watching":
                gf "You said you like watching me get attention."
                mc "I do."
                gf "Does that make you possessive, or the opposite?"
                mc "Both. Somehow."
                gf "That sounds about right."
                gf "I'm not doing anything you're not in on, you know."
                mc "I know."
            else:
                gf "I wanted to do that one with you beside me. I'd do it again."
                mc "Tomorrow?"
                gf "Don't push your luck."
                "She said it with her eyes closed and a very small smile."
        "She fell asleep first, with her hand still tangled in mine."

    else:
        if d4_pending == "love_repaired":
            "Leia turned toward me instead of away, which was a small thing and was not small."
            gf "Tomorrow I'll tell you the rest. About the club."
            mc "I'll be here."
            gf "I know. That's the new part."
            "I fell asleep with her breath against my collarbone and the first honest quiet I'd had in two days."
        elif d4_pending == "ntr_unresolved":
            "We lay with our backs almost touching."
            "Leia's phone lit the ceiling for a second. She turned it face down without reading it."
            "I watched the little glow die and wondered who it was, and then hated myself a little for wondering."
        else:
            "Leia slept on the far edge of the bed. I looked at the ceiling for a long time."
            "Her phone lit once, three dots appearing and vanishing in a small gray window on the screen. She didn't wake."
            "I didn't reach over to look. That was the one thing I did right that day, and it didn't feel like much."

    $ set_story_flag("ch01_d4_scene_14_complete")
    jump ch01_day4_scene_15_phone_hook


label ch01_day4_scene_15_phone_hook:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")
    $ d4_pending = get_story_value("ch01_d4_end_route_pending", "love")

    # AUDIO TODO: single soft phone buzz, then silence.
    python:
        phone_add_message(
            "group", "julian",
            text="Announcement. Pack for the water. Two nights. My family's boat is hungry for guests. Everyone. Yes, you two.",
            message_id="ch01_d4_group_day5_announce",
            mark_unread=True, notify=True, notification_title="Trip Group",
        )
        phone_add_message(
            "group", "maya",
            text="He says 'hungry for guests' like it's a haunted house.",
            message_id="ch01_d4_group_day5_maya",
            mark_unread=True, notify=False,
        )
        phone_add_message(
            "group", "julian",
            text="It's a boat.",
            message_id="ch01_d4_group_day5_julian_boat",
            mark_unread=True, notify=False,
        )
        phone_add_message(
            "group", "maya",
            text="It's a haunted boat.",
            message_id="ch01_d4_group_day5_maya_haunted",
            mark_unread=True, notify=False,
        )

    "My phone lit the dark room with the Trip Group."

    if d4_lane == "love":
        python:
            phone_add_message(
                "leia", "leia",
                text="I have a plan for the boat. You'll like it. It involves very little rope.",
                message_id="ch01_d4_leia_day5_love",
                mark_unread=True, notify=False,
            )
        "A second later, a single message from Leia, sent from the other side of the bed."
    elif d4_lane == "exhibitionism":
        python:
            phone_add_message(
                "maya", "maya",
                text="Dress code for the boat: brave. Billing: pending.",
                message_id="ch01_d4_maya_day5_exhib",
                mark_unread=True, notify=False,
            )
            phone_add_message(
                "leia", "leia",
                text="Ryan. I have an idea. Tell you tomorrow. Say yes now.",
                message_id="ch01_d4_leia_day5_exhib",
                mark_unread=True, notify=False,
            )
        "Then two more. Maya, and Leia, sent from the other side of the bed."
    else:
        if d4_pending == "love_repaired":
            python:
                phone_add_message(
                    "leia", "leia",
                    text="Thank you for tonight. Tomorrow I'll tell you the rest. All of it.",
                    message_id="ch01_d4_leia_day5_ntr_repaired",
                    mark_unread=True, notify=False,
                )
            "One more, from Leia, sent in the dark from three feet away."
        elif d4_pending == "ntr_unresolved":
            "Under the group chat, Leia's thread showed the three dots. They appeared. They disappeared."
            python:
                phone_add_message(
                    "leia", "leia",
                    text="Sorry.",
                    message_id="ch01_d4_leia_day5_ntr_unresolved",
                    mark_unread=True, notify=False,
                )
            "One word. I didn't know what it was apologizing for, and I didn't know how to ask."
        else:
            python:
                phone_add_message(
                    "maya", "maya",
                    text="I'm not taking sides. I'm taking both of you to breakfast. Be there.",
                    message_id="ch01_d4_maya_day5_ntr_confirmed",
                    mark_unread=True, notify=False,
                )
                phone_add_message(
                    "julian", "julian",
                    text="Hey. Whatever it is, I'm here. Not as a referee. As your friend.",
                    message_id="ch01_d4_julian_day5_ntr_confirmed",
                    mark_unread=True, notify=False,
                )
            "Two more. Maya. And Julian, in a private thread."

    $ d4_h_in = format_choice("ch01_d4_hook_in", "We're in.")
    $ d4_h_ask = format_choice("ch01_d4_hook_ask_leia", "Let me check with Leia first.")
    $ d4_h_maybe = format_choice("ch01_d4_hook_maybe", "Depends on tomorrow morning.")

    menu:
        "[d4_h_in]":
            $ apply_choice("ch01_d4_hook_in")
            $ phone_send_player_message("group", "We're in.", message_id="ch01_d4_player_hook_in")
            $ set_story_value("ch01_d4_hook_reply", "in")
            python:
                phone_add_message(
                    "group", "maya", text="Say it with more enthusiasm.",
                    message_id="ch01_d4_group_hook_reply_in",
                    mark_unread=True, notify=False,
                )

        "[d4_h_ask]":
            $ apply_choice("ch01_d4_hook_ask_leia")
            $ phone_send_player_message("group", "Let me check with Leia first.", message_id="ch01_d4_player_hook_ask")
            $ set_story_value("ch01_d4_hook_reply", "ask_leia")
            python:
                phone_add_message(
                    "group", "julian", text="That's the right answer. Annoying, but right.",
                    message_id="ch01_d4_group_hook_reply_ask",
                    mark_unread=True, notify=False,
                )

        "[d4_h_maybe]":
            $ apply_choice("ch01_d4_hook_maybe")
            $ phone_send_player_message("group", "Depends on tomorrow morning.", message_id="ch01_d4_player_hook_maybe")
            $ set_story_value("ch01_d4_hook_reply", "maybe")
            python:
                phone_add_message(
                    "group", "maya", text="Tomorrow morning is a very long time. See you on the dock.",
                    message_id="ch01_d4_group_hook_reply_maybe",
                    mark_unread=True, notify=False,
                )

    "I put the phone face up on the nightstand this time."
    "Somewhere beyond the curtains, the sea went on being the sea. Tomorrow we were leaving the villa behind for the first time, all four of us, with no map and no plan."

    $ set_story_flag("ch01_d4_scene_15_complete")
    jump ch01_day4_scene_16_finish


label ch01_day4_scene_16_finish:

    # Resolve the Day Four end state from STORED values only (never from stats).
    python:
        d4_lane = get_story_value("ch01_d4_lane", "love")
        d4_pending = get_story_value("ch01_d4_end_route_pending", "love")
        d4_allowed = ("love", "exhibitionism", "love_repaired", "ntr_unresolved", "ntr_confirmed")
        d4_end = d4_pending if d4_pending in d4_allowed else "love"
        set_story_value("ch01_d4_end_route", d4_end)
        if d4_lane == "love" and ch01_d4_nonchalant_count() >= 2:
            set_story_flag("ch01_d4_love_strained")
        if d4_end == "love_repaired":
            set_story_value("ch01_d4_end_variant", "ntr_repaired_" + get_story_value("ch01_d4_ntr_react", "thanks"))
        elif d4_end in ("ntr_unresolved", "ntr_confirmed"):
            set_story_value("ch01_d4_end_variant", d4_end)

    $ set_story_flag("ch01_d4_scene_16_complete")
    $ set_story_flag("ch01_day_04_complete")

    scene black
    with fade

    # Day Five hand-off. Day Five does not exist yet, so the label is checked at runtime.
    # Once ch01_day5_start exists, replace this block with the literal:
    #     jump ch01_day5_start
    if renpy.has_label("ch01_day5_start"):
        jump expression "ch01_day5_start"

    # TEMPORARY END CARD, only reached while Day Five is missing.
    centered "{size=46}CHAPTER ONE - DAY FOUR COMPLETE{/size}\n\n{size=25}Current development build ends here{/size}"
    return
