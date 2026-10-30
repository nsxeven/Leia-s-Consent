# Leia's Consent: Chapter One, Day Five ("The Water"), Scenes 9-16.
# Continues ch01_day5_scenes_01_08.rpy. Entry from scene 08: ch01_day5_scene_09_sunset.
# Ends at ch01_day5_scene_16_finish, which jumps to ch01_day6_start only if that label exists,
# otherwise shows a TEMPORARY end card.
#
# Exposure ladder for the chapter: covering (Day 2) -> brief, private (Day 4) -> comfortable,
# private among the four (Day 5, this file and scene 08) -> deliberate display with a visible
# off-ramp (Day 6). All intimacy is NON-EXPLICIT: fade/cut to CG placeholder cards.
# Every CG is Ryan's point of view with Ryan never in frame.

label ch01_day5_scene_09_sunset:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_pending = get_story_value("ch01_d5_end_route_pending", "love")
    $ d5_src = get_story_value("ch01_d2_mall_outfit_source", "leia")

    scene bg ch01_d5_boat_sunset
    with fade

    # AUDIO TODO: wind drops, halyard slap slows, low engine hum at idle, a single gull.

    "The cove turned the color of the inside of a shell. Captain Ilario motored us a few hundred yards out and set the anchor again, deep and slow, as if she was putting the day to bed."
    skipper "Dinner in an hour. Please be dressed or please be a long way from me."

    # Evening wardrobe: Love gets the outfit-control picker (mini available); others, Leia's own choice.
    if d5_track == "love" or d5_pending == "love":
        "Leia came up from the cabin with her bag, a towel over her shoulder and the look of a woman with a decision to make."
        gf "The mini or the dress or the loose one. I want it to be your fault."

        $ d5_ev_ryan = format_choice("ch01_d5_evening_ryan_picks", "Let me choose your outfit for dinner.")
        $ d5_ev_leia = format_choice("ch01_d5_evening_leia_decides", "Wear what makes you feel like yourself.")

        menu:
            "[d5_ev_ryan]":
                $ apply_choice("ch01_d5_evening_ryan_picks")
                python:
                    d5_ev_options = ch01_d5_evening_options()
                    d5_ev_pick = renpy.call_screen(
                        "leia_love_outfit_picker",
                        options=d5_ev_options,
                        title_text="Pick Leia's boat dinner outfit",
                    )
                    love_route_wear_request(d5_ev_pick, route_lane="love")
                    set_story_value("ch01_d5_evening_outfit_id", d5_ev_pick)
                    set_story_value("ch01_d5_evening_outfit_source", "ryan")
                mc "The [outfit_name(d5_ev_pick)]."
                if d5_ev_pick == "boutique_cutout_mini":
                    if d5_src == "ryan":
                        gf "You bought it. I'm wearing it. On a boat. This is your fault, officially."
                    else:
                        gf "I bought it. I'm wearing it. On a boat. Because you asked, and I wanted to."
                elif love_outfit_is_daring(d5_ev_pick):
                    gf "Brave. I like it."
                else:
                    gf "Elegant and a little bit unfair. Good call."
            "[d5_ev_leia]":
                $ apply_choice("ch01_d5_evening_leia_decides")
                mc "Wear what makes you feel like yourself."
                gf "That's a very dangerous thing to say to a person with options."
                $ d5_ev_wore = ch01_d5_wear("resort_dinner_dress")
                $ set_story_value("ch01_d5_evening_outfit_id", "resort_dinner_dress")
                $ set_story_value("ch01_d5_evening_outfit_source", "leia")
                gf "The dress. It's been waiting."
    else:
        $ d5_ev_wore = ch01_d5_wear("resort_dinner_dress")
        $ set_story_value("ch01_d5_evening_outfit_id", "resort_dinner_dress")
        $ set_story_value("ch01_d5_evening_outfit_source", "leia")
        if d5_track == "exhibitionism":
            "Leia disappeared below and came up in the Resort Dinner Dress with sun-bright cheeks, the hairclip secure."
            gf "The dress. The mini has had its week."
        else:
            "Leia came up in the Resort Dinner Dress without asking me what she should wear. I noticed. She noticed me noticing."

    scene bg ch01_d5_boat_sunset
    with dissolve

    if d5_track == "ntr_unresolved" and d5_pending == "ntr_unresolved":
        jump ch01_day5_sunset_gate_unresolved
    elif d5_track == "ntr_confirmed" and d5_pending == "ntr_confirmed":
        jump ch01_day5_sunset_gate_confirmed

    # Shared sunset: the Day Two sunset line returns, per track.
    $ enter_cinematic_mode()
    scene cg ch01_d5_sunset_deck
    with dissolve
    # CG TODO (artist): ch01_d5_sunset_deck. Ryan POV, Ryan never in frame.
    "She leaned on the stern rail with the last of the light across her face, and she looked back at me down the length of the deck."
    $ exit_cinematic_mode()
    scene bg ch01_d5_boat_sunset
    with dissolve

    if d5_pending == "love":
        gf "I like this. Us."
        mc "I like this too."
        gf "The Day Two sunset. You remember."
        mc "I remember everything about that sunset."
        gf "It's different out here. It feels like we're allowed to be a little bit more."
        if d5_track == "exhibitionism":
            gf "I wanted today to be just us, and it was. I'm glad."
    elif d5_pending == "exhibitionism":
        gf "I think part of why I liked it was because you knew."
        mc "That's what you said on Day Two."
        gf "I still think it. It's still true. It's more true."
        gf "I like that I'm brave with you here. I don't feel brave with anyone else."
        mc "You're brave with everyone."
        gf "I'm brave with you. With everyone else I'm just loud."
    else:
        # ntr_repaired track (love_repaired) or a setback from the afternoon disclosure
        if d5_pending == "love_repaired":
            gf "Are we okay?"
            mc "We're okay."
            gf "I asked that on the Day Two sunset. And you said you didn't know."
            mc "I didn't. I do now."
            gf "Say the sentence."
            mc "We're okay."
            "She leaned into my shoulder. The sun went down behind her head like something being gently put away."
        else:
            gf "Are we okay?"
            mc "I don't know."
            gf "That's the honest answer."
            mc "I'm trying to find a better one."
            gf "Keep trying. I'll be here."

    $ set_story_flag("ch01_d5_scene_09_complete")
    jump ch01_day5_scene_10_dinner


label ch01_day5_sunset_gate_unresolved:

    $ enter_cinematic_mode()
    scene cg ch01_d5_ntr_deck_alone
    with dissolve
    # CG TODO (artist): ch01_d5_ntr_deck_alone. Ryan POV, Ryan never in frame. Leia's back to camera at the rail.
    "She was at the stern rail, back to me, the hairclip in one hand and the horizon in front of her."
    $ exit_cinematic_mode()
    scene bg ch01_d5_boat_sunset
    with dissolve

    gf "Are we okay?"
    "It was the same sentence she'd asked on the Day Two sunset. Her voice had less in it now, and more underneath."

    if has_story_flag("ch01_d5_eaves_listened"):
        "I was carrying a thing I wasn't supposed to have: half a conversation I'd heard in the shade. It sat between us like a third person."

    $ d5_u_ask = format_day5_gate_choice("ch01_d5_ntr_u_ask_gently", "Ask her gently. 'Whenever you're ready, I'm listening.'", severity="soft", gate_label="D5-2")
    $ d5_u_press = format_day5_gate_choice("ch01_d5_ntr_u_press_hard", "Press her. 'What happened at the club, Leia?'", severity="hard", gate_label="D5-2")
    $ d5_u_fine = format_day5_gate_choice("ch01_d5_ntr_u_fine_hard", "I'm fine.", severity="hard", gate_label="D5-2")

    menu:
        "[d5_u_ask]":
            $ apply_choice("ch01_d5_ntr_u_ask_gently")
            mc "Whenever you're ready, I'm listening."
            "She turned around slowly. Her eyes were wet and entirely hers."
            if has_story_flag("ch01_d5_eaves_listened"):
                mc "I should tell you something first. I heard you and Maya. On the foredeck. I wasn't asleep."
                gf "I know."
                mc "I'm sorry. I'd rather hear it from you than from a sail."
                gf "That's the right sentence. It's also late. But it's right."
            else:
                gf "That's the first time you've asked me that."
            gf "Okay. Sit."
            "We sat on the stern bench with the sunset draining behind us. I let her find her own first sentence."
            call ch01_day5_club_disclosure
            $ set_story_value("ch01_d5_disclosure_when", "sunset_gate")
            $ set_story_value("ch01_d5_react_return", "dinner")
            jump ch01_day5_ntr_react_menu

        "[d5_u_press]":
            $ apply_choice("ch01_d5_ntr_u_press_hard")
            $ set_story_value("ch01_d5_ntr_outcome", "ntr_confirmed")
            $ set_story_value("ch01_d5_end_route_pending", "ntr_confirmed")
            mc "What happened at the club, Leia?"
            "The question came out like a hook."
            gf "There it is."
            mc "I'm just asking."
            gf "You're not asking. You're checking."
            gf "I almost told you. Ten seconds ago. I had the first sentence."
            gf "I think I'll keep it a little longer."
            "She went below. The hatch closed softly. That was almost worse than a slam."
            $ set_story_flag("ch01_d5_ntr_pressed")
            $ set_story_value("ch01_d5_react_return", "dinner")
            jump ch01_day5_ntr_react_resolve

        "[d5_u_fine]":
            $ apply_choice("ch01_d5_ntr_u_fine_hard")
            $ set_story_value("ch01_d5_ntr_outcome", "ntr_confirmed")
            $ set_story_value("ch01_d5_end_route_pending", "ntr_confirmed")
            mc "I'm fine."
            gf "I know."
            gf "That's the most polite way anyone's ever left me alone."
            "She smiled. It wasn't a smile that went anywhere."
            $ set_story_value("ch01_d5_react_return", "dinner")
            jump ch01_day5_ntr_react_resolve


label ch01_day5_sunset_gate_confirmed:

    $ enter_cinematic_mode()
    scene cg ch01_d5_ntr_deck_alone
    with dissolve
    # CG TODO (artist): ch01_d5_ntr_deck_alone. Ryan POV, Ryan never in frame. Leia's back to camera at the rail.
    "She was at the stern rail alone, back to me, the hairclip clasped in one hand and the horizon in front of her."
    $ exit_cinematic_mode()
    scene bg ch01_d5_boat_sunset
    with dissolve

    "Maya's sentence went round in my head: don't go and say 'fine'."
    "From the cockpit, a very small, very deliberate cough. Julian, three yards away, studying a cleat with great intensity."

    $ d5_c_go = format_day5_gate_choice("ch01_d5_ntr_c_go_to_her", "Go to her. 'I'm not fine. I'm sorry I kept saying it.'", severity="soft", gate_label="D5-2")
    $ d5_c_acc = format_day5_gate_choice("ch01_d5_ntr_c_accuse_hard", "Go to her. 'Did you tell Maya something you wouldn't tell me?'", severity="hard", gate_label="D5-2")
    $ d5_c_fine = format_day5_gate_choice("ch01_d5_ntr_c_fine_hard", "Stay where I am. 'I'm fine.'", severity="hard", gate_label="D5-2")

    menu:
        "[d5_c_go]":
            $ apply_choice("ch01_d5_ntr_c_go_to_her")
            $ set_story_value("ch01_d5_ntr_outcome", "ntr_unresolved")
            $ set_story_value("ch01_d5_end_route_pending", "ntr_unresolved")
            $ set_story_flag("ch01_d5_ntr_reopened")
            mc "I'm not fine. I'm sorry I kept saying it."
            "She turned slowly. It was the first time all day she'd looked at me for longer than a second."
            gf "I've been waiting for you to say that for about two days."
            mc "I know."
            gf "I'm not ready to tell you everything. Not tonight."
            gf "But I want you to ask me again at the pier. Tomorrow. And I want you to ask me the way you just did."
            mc "Okay."
            gf "That's a door. It's small. It's open."
        "[d5_c_acc]":
            $ apply_choice("ch01_d5_ntr_c_accuse_hard")
            $ set_story_value("ch01_d5_ntr_outcome", "ntr_confirmed")
            mc "Did you tell Maya something you wouldn't tell me?"
            "She didn't turn."
            gf "Yes."
            mc "What?"
            gf "That's not the question I wanted. And it's not the one you needed."
            gf "Go and sit with your granola bar, Ryan."
            "She said it without cruelty. That was the cruelty."
            $ set_story_flag("ch01_d5_ntr_pressed")
        "[d5_c_fine]":
            $ apply_choice("ch01_d5_ntr_c_fine_hard")
            $ set_story_value("ch01_d5_ntr_outcome", "ntr_confirmed")
            mc "I'm fine."
            "I didn't move. She didn't turn."
            gf "Okay."
            "Maya, in the cockpit, exhaled through her nose like a kettle."

    $ set_story_value("ch01_d5_react_return", "dinner")
    jump ch01_day5_ntr_react_resolve


label ch01_day5_scene_10_dinner:

    # Wiring: the NTR sunset gates return here without passing the end of scene 9, so close scene 9 here too.
    $ set_story_flag("ch01_d5_scene_09_complete")

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_pending = get_story_value("ch01_d5_end_route_pending", "love")

    scene bg ch01_d5_galley
    with fade

    # AUDIO TODO: cutlery, a kettle, the low glow-hum of a lantern, the creak of a hull at anchor.

    "Teodoro had packed a dinner that deserved more than a folding table: grilled fish, charred peppers, tomatoes still warm from somebody's sun."
    "Captain Ilario ate standing at the helm, eight feet away, with the serene indifference of a lighthouse."
    maya "Right. I brought a thing."
    "She produced a small tin with a faded lemon on the lid and shook it like a maraca."
    maya "Questions of Doom. They're from my aunt. They're not a strip game and they're not a trap. They're a conversation with a very rude friend."
    friend "I vote no."
    maya "You're outvoted by the boat."
    "She drew the first card with a showman's flourish."
    maya "Julian. 'Name something you are afraid of that is not bees.'"
    friend "Boats. Knives. This boat. Seafood. Large animals that look like seafood."
    maya "Wow. Okay. Beautiful."
    maya "My card. 'What do you want that you haven't asked for?' ...Pass."
    gf "You can't pass your own card."
    maya "I'm the dealer. I can do whatever I want."
    "She looked at Julian for roughly one second longer than a joke needed. He looked at his fish."

    "Maya slid the tin to me. I drew one."
    maya "Ryan. 'What's something you've been pretending to be fine about?'"
    if d5_track.startswith("ntr"):
        "Nobody laughed. Julian put down his fork."
    else:
        "A small, kind groan went round the table."

    $ d5_tr_honest = format_choice("ch01_d5_truth_honest", "Answer it honestly.")
    $ d5_tr_funny = format_choice("ch01_d5_truth_funny", "Answer it with a joke. Make it count.")
    $ d5_tr_dodge = format_choice("ch01_d5_truth_dodge", "Pass the tin to Julian. 'I'm the audience.'")

    menu:
        "[d5_tr_honest]":
            $ apply_choice("ch01_d5_truth_honest")
            $ set_story_value("ch01_d5_truth_ryan", "honest")
            if d5_track == "love":
                mc "That I'm this happy. I keep waiting to say the wrong thing and wreck it."
                gf "You've been saying the right things for ages."
                mc "That's the other thing I'm pretending. That I don't notice."
                maya "Oh, good. He's a human."
            elif d5_track == "exhibitionism":
                mc "That I like seeing you brave more than I thought I would. I thought I'd be nervous. I'm not. I'm proud."
                gf "That's not pretending. That's just saying it."
                mc "It's the saying it that's the hard part."
            else:
                mc "That I've been fine. For days. I've said it so many times I've forgotten what the question was."
                gf "..."
                mc "I've been scared. I didn't know how to say it without sounding like I was accusing you of something."
                "Leia put down her fork and looked at me properly. Julian looked at the fish. Maya looked, for the first time all dinner, like she wasn't on duty."
        "[d5_tr_funny]":
            $ apply_choice("ch01_d5_truth_funny")
            $ set_story_value("ch01_d5_truth_ryan", "funny")
            mc "That I can read a map. I can't. I just like being the person who holds the map."
            friend "I knew it. I knew the map thing."
            maya "That's a very good truth. It's also a deflection. I've charged you for both."
            gf "He's very good at one-liners. It's the other lines he's still working on."
        "[d5_tr_dodge]":
            $ apply_choice("ch01_d5_truth_dodge")
            $ set_story_value("ch01_d5_truth_ryan", "dodge")
            mc "I'm the audience. Julian?"
            friend "Don't."
            maya "I'm going to write that on your tab."
            "I handed the tin across and felt Leia not look at me, which on a very small boat is a loud thing to do."

    "The tin went round. A card asked who would survive longest on a desert island, and Julian said Teodoro, and Maya said the skipper, and Leia said the three of us would eat Julian first. Everyone agreed, and Julian asked for a vote."
    "A last card landed on me. 'Ask someone at the table something you really want to know.'"

    $ d5_as_sweet = format_choice("ch01_d5_ask_sweet", "Ask Leia: 'What was your favorite part of today?'")
    $ d5_as_brave = format_choice("ch01_d5_ask_brave", "Ask Leia: 'What's the bravest thing you did this week?'")
    $ d5_as_silly = format_choice("ch01_d5_ask_silly", "Ask Leia: 'Which of us would you push overboard first?'")

    menu:
        "[d5_as_sweet]":
            $ apply_choice("ch01_d5_ask_sweet")
            mc "What was your favorite part of today?"
            if d5_track == "love":
                gf "The rock. And the knot. And you not saying anything clever."
            elif d5_track == "exhibitionism":
                gf "The sun. The sun and the fact that I wasn't scared of it."
            elif d5_pending == "love_repaired":
                gf "The ten seconds after I told you. When you didn't leave."
            else:
                gf "Honestly? This. A table. Everyone present. Nobody being fine."
        "[d5_as_brave]":
            $ apply_choice("ch01_d5_ask_brave")
            mc "What's the bravest thing you did this week?"
            if d5_track == "ntr_repaired":
                gf "Telling you. Obviously."
            elif d5_track in ("ntr_unresolved", "ntr_confirmed") and d5_pending != "love_repaired":
                gf "Showing up at the pier. And not running."
            elif d5_track == "exhibitionism":
                gf "I'd say today. But I think the bravest thing is that I told you all of it first."
            else:
                gf "Telling you about the hallway. The ten minutes."
            maya "I'd like it on the record that I've heard none of this."
        "[d5_as_silly]":
            $ apply_choice("ch01_d5_ask_silly")
            mc "Which of us would you push overboard first?"
            gf "Julian."
            friend "I have a hat!"
            gf "That's why. The hat is a flotation hazard."
            maya "I'd push him second. I'd get a very good run-up."
            friend "Everyone at this table is legally liable."

    $ set_story_flag("ch01_d5_scene_10_complete")
    jump ch01_day5_scene_11_bunks


label ch01_day5_scene_11_bunks:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_pending = get_story_value("ch01_d5_end_route_pending", "love")

    scene bg ch01_d5_boat_cabin
    with fade

    skipper "Sleeping arrangements. Forward cabin: a double bunk. Saloon: two benches. Deck: weather permitting, and I will tell you whether it permits. Please do not move the anchor."
    maya "Julian gets a bench. I get the other bench. There is exactly one cabin door between us."
    friend "A door has never been a stronger statement."
    maya "Shut up."
    "Maya and Julian went below to the saloon, a conversation of looks and mismatched blankets already underway. Their door, I noticed, was not closed all the way."
    "Leia and I stood in the companionway with a pillow each and one rope."
    gf "So. Forward cabin, or the deck, or something else."

    $ d5_bk_cabin = format_choice("ch01_d5_bunk_cabin", "Share the forward cabin.")
    $ d5_bk_deck = format_choice("ch01_d5_bunk_deck", "Take blankets up on deck. Stars.")
    if d5_track.startswith("ntr"):
        $ d5_bk_apart = format_day5_gate_choice("ch01_d5_ntr_bunk_apart", "Give her the cabin. I'll take a bench.", severity="soft", gate_label="D5-3")
    else:
        $ d5_bk_apart = format_choice("ch01_d5_bunk_apart", "Give her the cabin. I'll take a bench. Whatever she'd like.")

    menu:
        "[d5_bk_cabin]":
            $ apply_choice("ch01_d5_bunk_cabin")
            $ set_story_value("ch01_d5_bunk", "cabin")
            mc "The cabin. If you'd like."
            if d5_pending == "ntr_confirmed":
                gf "Okay. Just sleeping."
                mc "Just sleeping."
                gf "...Okay."
            elif d5_pending == "ntr_unresolved":
                gf "I'd like that. I'd like it to be quiet, though."
                mc "Quiet's good."
            else:
                gf "I'd like that. Very much."
        "[d5_bk_deck]":
            $ apply_choice("ch01_d5_bunk_deck")
            $ set_story_value("ch01_d5_bunk", "deck")
            mc "Blankets, stars, deck."
            if d5_pending == "ntr_confirmed":
                gf "That's a lot of sky for two people who aren't talking."
                mc "It's a very big sky."
                gf "...Fine. But I'm bringing the rope."
            else:
                gf "That's the best thing anyone's suggested all day. Skipper? Is it permitted?"
                skipper "It is permitted. Until it is not."
        "[d5_bk_apart]":
            if d5_track.startswith("ntr"):
                $ apply_choice("ch01_d5_ntr_bunk_apart")
            else:
                $ apply_choice("ch01_d5_bunk_apart")
            $ set_story_value("ch01_d5_bunk", "apart")
            mc "You take the cabin. I'll take the bench."
            if d5_pending == "ntr_confirmed":
                gf "That's probably best."
                "It was a perfectly reasonable thing to say. She said it like a door being shut gently."
            elif d5_pending == "ntr_unresolved":
                gf "If that's what you'd like."
                mc "I'd like whatever you'd like."
                gf "I'd like you to want to be in the room. That's a different thing."
            elif d5_pending == "love_repaired":
                gf "You don't have to do that."
                mc "I know. I wanted you to have the choice."
                gf "Then I choose the cabin. With you in it. Come on."
                $ set_story_value("ch01_d5_bunk", "cabin")
            else:
                gf "Whatever you'd like. Whatever I'd like. Whatever's easiest."
                gf "Come find me if you change your mind."

    $ set_story_flag("ch01_d5_scene_11_complete")
    jump ch01_day5_scene_12_route_night


label ch01_day5_scene_12_route_night:

    # Dispatcher by the stored pending route (Leia's own and Ryan's choices today, never recomputed from stats).
    $ d5_pending = get_story_value("ch01_d5_end_route_pending", "love")

    if d5_pending == "love":
        jump ch01_day5_scene_12_love_night
    elif d5_pending == "exhibitionism":
        jump ch01_day5_scene_12_exhib_night
    else:
        jump ch01_day5_scene_12_ntr_night


label ch01_day5_scene_12_love_night:

    $ d5_bunk = get_story_value("ch01_d5_bunk", "cabin")

    scene bg ch01_d5_boat_cabin
    with fade

    if d5_bunk == "deck":
        scene bg ch01_d5_boat_deck_night
        with dissolve
        "She spread the blankets on the deck cushions, and we lay on our backs under more stars than I'd known a sky could hold."
    else:
        "The forward cabin was a wedge of warm wood and lantern light, the hull ticking softly around us."

    "Leia pulled the pale rope out of the tote. It had two short lengths now, cut and singed at the ends."
    gf "This is the plan. I told you. Two bracelets. A knot each. It's tradition."
    mc "Whose?"
    gf "Ours. As of this morning."
    gf "The knot stays tied until we both decide to cut it. That's the rule. It's the whole rule."

    $ d5_lb_hers = format_choice("ch01_d5_love_bracelet_hers", "Tie hers first. 'You go first. I'll be careful.'")
    $ d5_lb_his = format_choice("ch01_d5_love_bracelet_his", "Hold out my wrist. 'You first. I trust you.'")

    menu:
        "[d5_lb_hers]":
            $ apply_choice("ch01_d5_love_bracelet_hers")
            mc "You first. I'll be careful."
            "I tied hers slowly, a small flat knot, three turns around her wrist. Her pulse beat under my thumb."
            gf "Not too tight."
            mc "Never."
            gf "You didn't even hesitate."
            mc "I've been practicing. On a rock."
        "[d5_lb_his]":
            $ apply_choice("ch01_d5_love_bracelet_his")
            mc "Mine first. I trust you."
            "She tied mine with her tongue between her teeth, concentrating the way she did when she was proud of a small thing."
            gf "That's the best knot I've ever made."
            mc "It's the only knot you've ever made."
            gf "Which makes it the best."

    "The second bracelet went on a minute later. She held her wrist next to mine and looked at the two small knots lined up together."
    gf "I want it written down somewhere that I did this."
    mc "I'll tell Maya."
    gf "God, no. Don't tell Maya. She'd invoice it."
    $ set_story_flag("ch01_d5_rope_bracelets")

    $ enter_cinematic_mode()
    scene cg ch01_d5_love_night_01
    with dissolve
    # CG TODO (artist): ch01_d5_love_night_01. Ryan POV, Ryan never in frame. Leia's hand turning the lantern down, rope bracelet on her wrist. One figure only. Implied.
    "She reached over and turned the lantern down until it was only a coin of gold on the wood, and the night came in slowly around it."
    "The rest of it belonged to the two of us, and to the small, patient sea."
    $ exit_cinematic_mode()

    $ set_story_value("ch01_d5_end_variant", "love_bracelets")
    $ set_story_flag("ch01_d5_scene_12_complete")
    jump ch01_day5_scene_13_night_after


label ch01_day5_scene_12_exhib_night:

    $ d5_bunk = get_story_value("ch01_d5_bunk", "cabin")
    $ d5_step = get_story_value("ch01_d5_exposure_step", "none")

    scene bg ch01_d5_boat_deck_night
    with fade

    if d5_bunk == "cabin":
        "We took the blankets up anyway, because the cabin's hatch looked up at the sky and Leia had already dragged her pillow under it."
    "The deck was a quilt of warm cushions and Captain Ilario's neatly coiled lines. The anchor light made a little gold moon on the water."
    gf "Today I did a thing."
    mc "You did a very good thing."
    gf "I want to talk about the rule."
    mc "What rule?"
    gf "My rule. The dial. I keep it. But I want us to have a little something extra. A signal."

    $ d5_xr_wrist = format_choice("ch01_d5_exhib_rule_wrist", "Agree a signal. 'Two taps on the wrist means stop, no questions.'")
    $ d5_xr_dare = format_choice("ch01_d5_exhib_rule_dare", "Offer her a dare for tomorrow. 'Your pick. Your pace.'")
    $ d5_xr_skip = format_choice("ch01_d5_exhib_rule_skip", "Tell her no rules tonight. Just the stars.")

    menu:
        "[d5_xr_wrist]":
            $ apply_choice("ch01_d5_exhib_rule_wrist")
            $ set_story_flag("ch01_d5_pass_signal")
            mc "Two taps on the wrist. Stop, no questions, no sulking."
            gf "Two taps on the wrist. A pass. And I can use it any time. On anything."
            mc "And so can I."
            gf "So can you. Deal."
            "She tapped her own wrist twice, then mine, then laughed at how serious we both sounded."
            gf "That's the best rule I've ever had. It's also the most romantic."
        "[d5_xr_dare]":
            $ apply_choice("ch01_d5_exhib_rule_dare")
            $ set_story_flag("ch01_d5_dare_offered")
            mc "A dare for tomorrow. Your pick. Your pace."
            gf "You're giving me the dare."
            mc "I'm giving you the dial. The dare's just a costume."
            gf "I'll think about it. Very carefully. With a notebook."
        "[d5_xr_skip]":
            $ apply_choice("ch01_d5_exhib_rule_skip")
            mc "No rules tonight. Just the stars."
            gf "You're my favorite person at this very low-key moment."
            gf "The dial stays with me anyway. I just won't make a speech about it."

    $ enter_cinematic_mode()
    scene cg ch01_d5_exhib_night_01
    with dissolve
    # CG TODO (artist): ch01_d5_exhib_night_01. Ryan POV, Ryan never in frame. Leia on the deck cushions under a blanket drawn to her chin, stars overhead, eyes on the lens, delighted and a little daring. Covered. One figure only.
    "She pulled the blanket up to her chin and tilted her head back to look at the stars, then at me, a slow, pleased, completely unrepentant smile."
    gf "I took my top off in front of Julian, and it was fine. I'm a different person."
    mc "You're the same person. A braver one."
    gf "Is there a difference?"
    mc "It's a very good difference."
    $ exit_cinematic_mode()

    if d5_step == "comfortable":
        "I'm still not sure if I slept, or if I only lay awake watching her breathe against the blanket and thinking about a girl on a rock with the sun on her face."
    else:
        "I'm still not sure if I slept, or if I only lay there thinking about a girl on a rock with her ties undone and her whole face open."

    $ set_story_value("ch01_d5_end_variant", "exhib_" + get_story_value("ch01_d5_exhib_variant", "shared_step"))
    $ set_story_flag("ch01_d5_scene_12_complete")
    jump ch01_day5_scene_13_night_after


label ch01_day5_scene_12_ntr_night:

    $ d5_pending = get_story_value("ch01_d5_end_route_pending", "ntr_unresolved")
    $ d5_bunk = get_story_value("ch01_d5_bunk", "cabin")
    $ d5_react = get_story_value("ch01_d5_ntr_react", None)

    scene bg ch01_d5_boat_cabin
    with fade

    if d5_pending == "love_repaired":
        if d5_bunk == "deck":
            scene bg ch01_d5_boat_deck_night
            with dissolve
        $ enter_cinematic_mode()
        scene cg ch01_d5_ntr_night_01
        with dissolve
        # CG TODO (artist): ch01_d5_ntr_night_01. Ryan POV, Ryan never in frame. Leia's hand setting the hairclip on a shelf beside a lantern, a rope bracelet or a bare wrist. One figure only, no third person.
        "She took the hairclip out of her hair and set it on the shelf beside the lantern, carefully, like a promise made visible."
        $ exit_cinematic_mode()
        if d5_react == "curious":
            gf "You asked me what it felt like."
            mc "I did."
            gf "I want to ask you something. What did it feel like to hear it?"
            mc "Honest answer? Warm. And like I'd been handed the other half of a puzzle."
            gf "That's a strange answer. I'm saving it."
        elif d5_react == "boundary":
            gf "A seatbelt."
            mc "A seatbelt."
            gf "I like us with seatbelts."
        else:
            gf "Thank you for not leaving."
            mc "I wasn't going anywhere."
            gf "I know. That's the thing. I know."
        "She curled against me, and there was nothing dramatic about it. We slept."
        $ set_story_value("ch01_d5_end_variant", "ntr_repaired_" + (d5_react or "thanks"))
    elif d5_pending == "ntr_unresolved":
        if d5_bunk == "apart":
            "I lay on the saloon bench, listening to the soft sounds of the boat. Beyond the half-closed door, Maya and Julian were whispering."
            "Forward, the cabin was dark. I could picture Leia awake in it, doing the same arithmetic."
        else:
            "She lay with her back to me, and I lay with mine toward hers, and the inch between us was a very specific, very honest inch."
        "In the middle of the night, I felt the mattress shift and a hand rest, briefly, on my shoulder."
        gf "Not tonight. But I haven't left."
        mc "I know."
        "That was all. It was something."
        $ set_story_value("ch01_d5_end_variant", "ntr_unresolved")
    else:
        if d5_bunk == "apart":
            "I lay on the saloon bench in the dark, a blanket up to my chin and a promise to myself that I'd stop saying a word I'd spent three days misusing."
            "Beyond the half-closed door, Maya said something low, and Julian answered. Their voices went on for a long time, then stopped."
        else:
            "Leia lay with her back to me and her breathing too even to be sleep."
            gf "I'm not mad."
            mc "I know."
            gf "I'm tired. It's different. Goodnight."
        $ set_story_value("ch01_d5_end_variant", "ntr_confirmed")

    $ set_story_flag("ch01_d5_scene_12_complete")
    jump ch01_day5_scene_13_night_after


label ch01_day5_scene_13_night_after:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_deck_night
    with fade

    # AUDIO TODO: a sudden wind in the rigging, the boat shifting on her anchor chain.

    "At twenty to three, a flashlight beam swung across the cabin ceiling and a deadpan voice came down the hatch."
    skipper "Everyone. Dress. Weather is turning. We go home at first light."
    friend "We go home?"
    skipper "We go home."
    friend "We were supposed to have two nights."
    skipper "You have had one. It was good."
    friend "I had a speech."
    maya "He did. It was about the sea."
    friend "It was a very good speech."
    "On deck, the wind had a cold edge and the sky to the west was a wall of slow, towering cloud. The stars had been rubbed out in one corner like a smudge."
    "Maya, wrapped in a blanket on the cockpit bench, was holding two mugs of something hot. She handed one to Julian without looking at him."
    maya "It's tea. Don't make it weird."
    friend "I wasn't going to."
    maya "You were. I could hear it."
    "They sat an unreasonable distance apart, and then, without anyone moving, a slightly shorter distance."
    "Captain Ilario weighed the anchor in six minutes flat, her face a map of calm."
    skipper "Ten more minutes to the headland. After that, we run."

    if d5_track.startswith("ntr"):
        "Leia stood at the rail in a blanket, the hairclip back in her hair, the horizon invisible. I stood three feet away. The distance between us was a thing the wind kept moving."
    else:
        "Leia stood at the rail in a blanket, her shoulder against mine, the horizon invisible, her head tipped back at the first stars of a sky about to close."

    $ set_story_flag("ch01_d5_scene_13_complete")
    jump ch01_day5_scene_14_dawn_run


label ch01_day5_scene_14_dawn_run:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_pending = get_story_value("ch01_d5_end_route_pending", "love")

    scene bg ch01_d5_boat_deck
    with fade

    "We ran home under a slate-gray sky with the wind on our beam, the boat leaning like a very expensive swimmer."
    "Julian was not sick. This was noted by everyone, and by Julian most of all."
    friend "I'd like it recorded that I'm not green."
    maya "You're a pleasant beige."
    friend "I'll take beige."

    "Just after dawn, around the last headland, my phone woke up. One bar. Two. Then it stuttered and began unloading a night's worth of nothing."

    python:
        phone_add_message(
            "group", "maya",
            text="Inés again: 'The invitation is at the pier. Look at the post by the blue boat. Masks required, secrets optional.'",
            message_id="ch01_d5_late_maya_ines",
            mark_unread=True, notify=True, notification_title="Trip Group",
        )
        phone_add_message(
            "group", "julian",
            text="She says 'secrets optional' like it's a dress code.",
            message_id="ch01_d5_late_julian",
            mark_unread=True, notify=False,
        )
    maya "I've been informed there is a festival tonight."
    friend "Tonight? I thought we had a boat."
    skipper "You have a pier. In twelve minutes."

    if d5_track == "love":
        python:
            phone_add_message(
                "leia", "leia",
                text="I wore my rope bracelet to sleep. Very unsexy. Extremely sincere.",
                message_id="ch01_d5_late_leia_love",
                mark_unread=True, notify=False,
            )
        "Leia's thread, sent from three feet away, with her thumb already hovering at the corner of the screen."
    elif d5_track == "exhibitionism":
        python:
            phone_add_message(
                "leia", "leia",
                text="I think I might have an idea for tonight. Say yes later. Not now.",
                message_id="ch01_d5_late_leia_exhib",
                mark_unread=True, notify=False,
            )
        "Leia's thread, sent from three feet away, with a very pleased little smile she was working hard to put away."
    elif d5_pending == "love_repaired":
        python:
            phone_add_message(
                "leia", "leia",
                text="Thank you for the cove. For the order I told it in. For listening to the end.",
                message_id="ch01_d5_late_leia_ntr_repaired",
                mark_unread=True, notify=False,
            )
        "Leia's thread, a single message, sent from the rail with her face turned toward the sea."
    elif d5_pending == "ntr_unresolved":
        python:
            phone_add_message(
                "leia", "leia",
                text="Tonight, at the pier. You asked me gently once. Ask me again, if you still want to.",
                message_id="ch01_d5_late_leia_ntr_unresolved",
                mark_unread=True, notify=False,
            )
        "A message on Leia's thread, under 'Sorry.', under the draft that had finally landed."
    else:
        python:
            phone_add_message(
                "julian", "julian",
                text="For the record. You looked like you wanted to say something at the rail. I think you should say it.",
                message_id="ch01_d5_late_julian_ntr_confirmed",
                mark_unread=True, notify=False,
            )
        "A message from Julian, who was fourteen feet away, pretending to coil a rope."

    "The pier came up out of the mist like a half-remembered idea."
    $ set_story_flag("ch01_d5_scene_14_complete")
    jump ch01_day5_scene_15_pier_invitation


label ch01_day5_scene_15_pier_invitation:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_pending = get_story_value("ch01_d5_end_route_pending", "love")

    scene bg ch01_d5_dawn_pier
    with fade

    "Captain Ilario put the bow against the pier so gently it felt like a courtesy. She tipped her cap at the four of us, said 'Good guests' and went to coil a rope."
    "Maya, first onto the pier, stopped at a weathered post beside a blue fishing boat and stared."
    "Pinned to the wood with a brass tack, a stiff card the color of cream."

    $ enter_cinematic_mode()
    scene cg ch01_d5_invitation
    with dissolve
    # CG TODO (artist): ch01_d5_invitation. Close-up of the printed invitation on the post (a prop, not a person). Ryan POV, Ryan never in frame. Second line in a different, looser hand; text varies by track (see the checklist).
    "THE NIGHT OF THE LANTERNS. Tonight. The old square. Bring a friend. Bring a mask. We will provide the rest."
    $ exit_cinematic_mode()
    scene bg ch01_d5_dawn_pier
    with dissolve

    "Below the printed text, in a different, looser hand, in ink that hadn't quite dried:"

    if d5_pending == "love" or d5_track == "love":
        "'Come as you are, together.'"
    elif d5_pending == "exhibitionism" or d5_track == "exhibitionism":
        "'Masks keep secrets. You choose which ones.'"
    else:
        "'Some conversations are easier behind a mask.'"

    maya "Inés wrote that. Or somebody braver than Inés."
    friend "It's a very low-stakes sentence."
    maya "It's the most high-stakes sentence I've ever read."

    if d5_track.startswith("ntr") and d5_pending != "love":
        $ d5_iv_read = format_choice("ch01_d5_invite_read_aloud", "Read the handwritten line aloud, to Leia.")
        $ d5_iv_quiet = format_choice("ch01_d5_invite_keep_quiet", "Keep it to myself. Let her find it.")
        menu:
            "[d5_iv_read]":
                $ apply_choice("ch01_d5_invite_read_aloud")
                $ set_story_value("ch01_d5_invite_reply", "read_aloud")
                mc "'Some conversations are easier behind a mask.'"
                "Leia looked at the card and then at me. Her mouth did something complicated."
                gf "That's a very good sentence."
                mc "It's not mine. It was on the post."
                gf "It's yours now. You said it first."
            "[d5_iv_quiet]":
                $ apply_choice("ch01_d5_invite_keep_quiet")
                $ set_story_value("ch01_d5_invite_reply", "kept_quiet")
                "I put the card back, flat against the post, and said nothing about the handwritten line."
                "Leia found it a minute later, on her own. She read it twice and didn't look at me."
    else:
        $ d5_iv_in = format_choice("ch01_d5_invite_in", "'We're going. All of us.'")
        $ d5_iv_ask = format_choice("ch01_d5_invite_ask_leia", "Look at Leia. 'What do you want to do?'")
        $ d5_iv_maybe = format_choice("ch01_d5_invite_maybe", "'Let's see how we feel after a shower.'")
        menu:
            "[d5_iv_in]":
                $ apply_choice("ch01_d5_invite_in")
                $ set_story_value("ch01_d5_invite_reply", "in")
                mc "We're going. All of us."
                maya "That's the most enthusiasm you've shown on this entire trip."
                gf "It's a very good sentence."
            "[d5_iv_ask]":
                $ apply_choice("ch01_d5_invite_ask_leia")
                $ set_story_value("ch01_d5_invite_reply", "ask_leia")
                mc "What do you want to do?"
                gf "I want to go. I want to wear something I haven't worn yet. And I want you to hold my hand through the loud parts."
                mc "Done."
            "[d5_iv_maybe]":
                $ apply_choice("ch01_d5_invite_maybe")
                $ set_story_value("ch01_d5_invite_reply", "maybe")
                mc "Let's see how we feel after a shower."
                maya "You're going to feel exactly the same, but cleaner."
                friend "I vote yes. For the record."

    "Behind us, the engine of the Reasonable Doubt coughed, caught and settled into a quiet that sounded almost like an answer."
    "On the horizon, a ribbon of gray was turning slowly to gold."
    "Tonight was the last night of the week, and I had no idea what any of us were going to say."

    $ set_story_flag("ch01_d5_scene_15_complete")
    jump ch01_day5_scene_16_finish


label ch01_day5_scene_16_finish:

    # Resolve the Day Five end state from STORED values only (never from stats).
    python:
        d5_track = get_story_value("ch01_d5_track", "love")
        d5_pending = get_story_value("ch01_d5_end_route_pending", "love")
        d5_allowed = ("love", "exhibitionism", "love_repaired", "ntr_unresolved", "ntr_confirmed")
        d5_end = d5_pending if d5_pending in d5_allowed else "love"
        set_story_value("ch01_d5_end_route", d5_end)
        if d5_end == "love_repaired":
            set_story_value("ch01_d5_end_variant", "ntr_repaired_" + (get_story_value("ch01_d5_ntr_react", "thanks") or "thanks"))
        elif d5_end == "ntr_unresolved":
            set_story_value("ch01_d5_end_variant", "ntr_unresolved_reopened" if has_story_flag("ch01_d5_ntr_reopened") else "ntr_unresolved")
        elif d5_end == "ntr_confirmed":
            set_story_value("ch01_d5_end_variant", "ntr_confirmed")
        elif d5_end == "love" and get_story_value("ch01_d5_exhib_variant", "none") == "opt_out_private":
            set_story_value("ch01_d5_end_variant", "exhib_private_optout")
        if d5_track == "love" and ch01_d5_nonchalant_count() >= 2:
            set_story_flag("ch01_d5_love_strained")

    $ set_story_flag("ch01_d5_scene_16_complete")
    $ set_story_flag("ch01_day_05_complete")

    scene black
    with fade

    call lc_day_review("ch01_d5") from lc_review_return_ch01_d5

    # Day Six hand-off. Day Six does not exist yet, so the label is checked at runtime.
    # Once ch01_day6_start exists, replace this block with the literal:
    #     jump ch01_day6_start
    if renpy.has_label("ch01_day6_start"):
        jump expression "ch01_day6_start"

    # TEMPORARY END CARD, only reached while Day Six is missing.
    centered "{size=25}Current development build ends here{/size}"
    return

