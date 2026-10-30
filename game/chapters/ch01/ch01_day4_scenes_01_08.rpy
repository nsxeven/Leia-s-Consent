# Leia's Consent: Chapter One, Day Four, Scenes 1-8.
# First playable dialogue pass. CG insertion points use the placeholder ids in
# ch01_day4_visuals.rpy. Entry: ch01_day4_start. Day 3's stored ending is authoritative.
#
# Reads (never recomputes): ch01_d2_end_route, ch01_d3_end_variant, ch01_d3_lane,
# ch01_d3_ntr_repair_effort, ch01_d3_cutout_secret, ch01_d2_mall_outfit_source.
#
# Day Four premise: consequence and recalibration. Slow burn, one visible step.
#   Love: attentive, outfit control, private night.
#   Exhibition (NTS): one small step up with Ryan included; sub-variant 'Ryan likes watching'.
#   NTR pressure: secrecy and missed repair; Ryan's 'I'm fine.'; a repair gate.
# Tone: immersive, flirty, natural. Consent is implied; characters speak up if uncomfortable.
# All intimacy is NON-EXPLICIT: fade/cut to CG placeholder cards with artist TODOs.

label ch01_day4_start:
    $ lc_review_begin("ch01_d4")

    $ set_story_flag("ch01_day_04_started")

    python:
        d4_d2_end = get_story_value("ch01_d2_end_route", "love")
        d4_lane = get_story_value("ch01_d3_lane", None)
        if d4_lane is None:
            # Dev-skip / older-save fallback ONLY. Normal play always has ch01_d3_lane from Day Three.
            d4_lane = "ntr" if d4_d2_end in ("ntr_confirmed", "mixed_unresolved") else ("exhibitionism" if d4_d2_end == "exhibitionism" else "love")
        d4_variant = get_story_value("ch01_d3_end_variant", None)
        if d4_variant is None:
            d4_variant = {"love": "love_private", "exhibitionism": "exhibition_window"}.get(d4_lane, "ntr_restroom_nightmare")
        set_story_value("ch01_d4_lane", d4_lane)
        set_story_value("ch01_d4_d3_variant", d4_variant)
        set_story_value("ch01_d4_ntr_fine_count", 0)
        set_story_value("ch01_d4_photo_style", "none")
        set_story_value("ch01_d4_exhib_variant", "none")
        set_story_value("ch01_d4_exposure_step", "none")
        set_story_value("ch01_d4_hunt_winner", "ryan_leia")
        set_story_value("ch01_d4_end_variant", "none")
        set_story_value("ch01_d4_ntr_outcome", "ntr_confirmed")

    scene black
    with fade
    centered "{size=50}CHAPTER ONE - DAY FOUR{/size}"

    jump ch01_day4_scene_01_wake


label ch01_day4_scene_01_wake:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")
    $ d4_variant = get_story_value("ch01_d4_d3_variant", "love_private")
    $ d4_d2_end = get_story_value("ch01_d2_end_route", "love")

    scene bg ch01_villa_bedroom_night
    with fade

    if d4_lane == "love":
        "Morning came in around the edges of the curtains we hadn't opened."
        "[girlfriend_name] was already awake, one arm folded under her cheek, watching me with the face of someone who had decided not to move for at least an hour."
        gf "Don't get up."
        mc "I wasn't going to."
        gf "Good. I'm timing how long we can ignore everyone."
        mc "What's the record?"
        gf "Four minutes. Maya texted."
        if d4_d2_end == "love_repaired":
            gf "Day four. Still talking?"
            mc "Still talking."
            gf "Deal's holding."
            "It was a small thing, and neither of us treated it as small."
        else:
            gf "I like this. Mornings."
            mc "Yeah?"
            gf "Mornings with you in them."
        if get_story_value("ch01_dream_response") == "grounded":
            "The dream from the first night had long since gone back to being only a dream."
        else:
            "Somewhere under the quiet, the first night's dream and its sheer curtain were still there. Daylight kept it small."

    elif d4_lane == "exhibitionism":
        "The curtains were still open. Sunlight laid a bright stripe across the bed and across [girlfriend_name], who stood at the window wrapped in the top sheet and very little else."
        gf "Morning."
        mc "You're going to give the beach path a heart attack."
        gf "It's seven in the morning. The beach path is a man with a dog."
        mc "That's still a witness."
        gf "He's looking at the dog."
        "She turned back with the sheet clutched at her collarbone and a small, pleased look she wasn't trying to hide."
        gf "I think we're getting braver."
        mc "Together."
        gf "Together. Come here before I lose my nerve for the sheet."
        "The first night's dream had also had a curtain in it. That one had frightened me. This one, open to the light, only made me smile."

    else:
        "I woke to cool sheets and the dull weight of last night's dream."
        "The restroom corridor. The door slamming. The two messages and the dots that never stopped."
        "[girlfriend_name]'s side of the bed was empty, the pillow still dented."
        if d4_d2_end == "mixed_unresolved":
            "Nothing between us had been decided, in either direction. That had turned out to be its own kind of decision."
        else:
            "Something had been decided between us that neither of us had said out loud."
        if get_story_value("ch01_dream_response") == "withdrew":
            "I had spent days refusing to count the dreams. I was running out of ways to call it a coincidence."
        else:
            "It was only a dream. It had also happened more than once."
        "I picked up my phone off the nightstand. It was the only thing in the room that already had something to say."

    $ d4_card = ch01_d4_track_text()
    if d4_card:
        centered "[d4_card]"

    $ set_story_flag("ch01_d4_scene_01_complete")
    jump ch01_day4_scene_02_phone_morning


label ch01_day4_scene_02_phone_morning:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    # AUDIO TODO: three short phone-buzz SFX, staggered, then room tone.
    python:
        phone_add_message(
            "group", "julian",
            text="Breakfast is at ten. I have personally supervised the pancakes. Do not make me regret it.",
            message_id="ch01_d4_group_breakfast_julian",
            mark_unread=True, notify=True, notification_title="Trip Group",
        )
        phone_add_message(
            "group", "maya",
            text=(friend_name + ' does not cook. ' + friend_name + ' supervised a chef named Teodoro.'),
            message_id="ch01_d4_group_breakfast_maya",
            mark_unread=True, notify=False,
        )
        phone_add_message(
            "group", "maya",
            text="Day one it was 11 or he called the police. Growth.",
            message_id="ch01_d4_group_maya_police_growth",
            mark_unread=True, notify=False,
        )
        phone_add_message(
            "group", "julian",
            text="I contributed energy.",
            message_id="ch01_d4_group_julian_energy",
            mark_unread=True, notify=False,
        )
        phone_add_message(
            "group", "maya",
            text="Comfortable shoes today. We are walking. Outfit advice after that is billable. I charge by the hour.",
            message_id="ch01_d4_group_maya_shoes",
            mark_unread=True, notify=False,
        )

    "The Trip Group had been busy before either of us was awake."

    if d4_lane == "ntr":
        jump ch01_day4_scene_02_phone_ntr

    # Love / Exhibition: Leia texts from three feet away.
    python:
        if d4_lane == "love":
            leia_text = "I'm three feet away and I'm texting you. Please note how romantic this is."
        else:
            leia_text = "I'm at the window. The sheet is doing its best. You should come and supervise."
        phone_add_message(
            "leia", "leia",
            text=leia_text,
            message_id="ch01_d4_leia_morning_text",
            mark_unread=True, notify=True, notification_title=girlfriend_name,
        )

    "My phone lit up a second after hers did. She hadn't said a word."
    gf "Did you get it?"
    mc "I'm reading it."
    gf "Out loud."

    $ d4_text_warm = format_choice("ch01_d4_text_warm", "Best three feet of my whole week.")
    $ d4_text_flirt = format_choice("ch01_d4_text_flirt", "Come closer and I'll make it better.")
    $ d4_text_coffee = format_choice("ch01_d4_text_coffee", "Coffee first. Then all of it.")

    menu:
        "[d4_text_warm]":
            $ apply_choice("ch01_d4_text_warm")
            $ phone_send_player_message("leia", "Best three feet of my whole week.", message_id="ch01_d4_player_text_warm")
            gf "Okay. That one's going in the keepsake box."
            mc "You have a keepsake box?"
            gf "I have a box now."

        "[d4_text_flirt]":
            $ apply_choice("ch01_d4_text_flirt")
            $ phone_send_player_message("leia", "Come closer and I'll make it better.", message_id="ch01_d4_player_text_flirt")
            gf "Bold, for a man in yesterday's hair."
            mc "You're still reading it again."
            gf "I'm studying it."
            "She closed the distance anyway, taking her time about it."

        "[d4_text_coffee]":
            $ apply_choice("ch01_d4_text_coffee")
            $ phone_send_player_message("leia", "Coffee first. Then all of it.", message_id="ch01_d4_player_text_coffee")
            gf "Coffee first. Fair. It's a very serious all of it."
            mc "I'm a serious person."
            gf "You're a man who needs a menu to choose a sandwich."

    $ set_story_flag("ch01_d4_scene_02_complete")
    jump ch01_day4_scene_03_wardrobe_morning


label ch01_day4_scene_02_phone_ntr:

    scene bg ch01_villa_bedroom_night
    with dissolve

    python:
        phone_add_message(
            "leia", "leia",
            text="Morning.",
            message_id="ch01_d4_leia_morning_ntr_1",
            mark_unread=True, notify=True, notification_title=girlfriend_name,
        )

    "One word, from the terrace, sent at 7:48."
    "Then the three dots appeared under it. They stopped. Appeared again."
    "I watched them the way I'd watched them in the restroom corridor, as if staring would make them say something."

    python:
        phone_add_message(
            "leia", "leia",
            text="Coffee's on the terrace if you want some. No pressure.",
            message_id="ch01_d4_leia_morning_ntr_2",
            mark_unread=True, notify=False,
        )

    "She'd opened a door, and left it just far enough open that I could pretend not to see it."

    $ d4_ntr_join = format_choice("ch01_d4_ntr_text_join", "Be right down. Save me the good chair.")
    $ d4_ntr_later = format_choice("ch01_d4_ntr_text_later", "Give me twenty minutes.")
    $ d4_ntr_fine = format_day4_gate_choice("ch01_d4_ntr_text_fine_soft", "I'm fine. Go ahead without me.", severity="soft", gate_label="D4-1")

    menu:
        "[d4_ntr_join]":
            $ apply_choice("ch01_d4_ntr_text_join")
            $ phone_send_player_message("leia", "Be right down. Save me the good chair.", message_id="ch01_d4_player_ntr_join")
            $ set_story_value("ch01_d4_morning_reply", "joined")
            "The dots appeared again almost at once."
            python:
                phone_add_message(
                    "leia", "leia",
                    text="The good chair is the one that wobbles. I'm keeping it warm.",
                    message_id="ch01_d4_leia_morning_ntr_3",
                    mark_unread=True, notify=False,
                )
            "It was the first thing she'd written me in two days that sounded like her."

        "[d4_ntr_later]":
            $ apply_choice("ch01_d4_ntr_text_later")
            $ phone_send_player_message("leia", "Give me twenty minutes.", message_id="ch01_d4_player_ntr_later")
            $ set_story_value("ch01_d4_morning_reply", "later")
            python:
                phone_add_message(
                    "leia", "leia",
                    text="Okay.",
                    message_id="ch01_d4_leia_morning_ntr_3",
                    mark_unread=True, notify=False,
                )
            "Not a no. Not a yes. I told myself that counted as an answer."

        "[d4_ntr_fine]":
            $ apply_choice("ch01_d4_ntr_text_fine_soft")
            $ phone_send_player_message("leia", "I'm fine. Go ahead without me.", message_id="ch01_d4_player_ntr_fine")
            $ set_story_value("ch01_d4_morning_reply", "fine")
            $ set_story_value("ch01_d4_ntr_fine_count", get_story_value("ch01_d4_ntr_fine_count", 0) + 1)
            $ set_story_flag("ch01_d4_ntr_soft_gate")
            "The dots came up. Went away. Came up."
            python:
                phone_add_message(
                    "leia", "leia",
                    text="Okay.",
                    message_id="ch01_d4_leia_morning_ntr_3",
                    mark_unread=True, notify=False,
                )
            "Just that. I knew exactly how many times in two days I'd given her the same sentence, and exactly how many times she'd taken it."

            if current_choice_mode() == "developer":
                centered "NTR SOFT GATE D4-1 - ch01_d4_ntr_soft_gate = True"
            elif current_choice_mode() == "full":
                centered "Major relationship consequence."
            elif current_choice_mode() == "insight":
                centered "[girlfriend_name] stops leaving doors open."

    $ set_story_flag("ch01_d4_scene_02_complete")
    jump ch01_day4_scene_03_wardrobe_morning


label ch01_day4_scene_03_wardrobe_morning:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    if d4_lane == "love":
        scene bg ch01_master_bedroom
        with dissolve

        "[girlfriend_name] sat cross-legged in front of her open suitcase, holding up a shirt, putting it down, holding up another."
        gf "Walking day. Market day. No dress code but Maya has a face when she's disappointed."
        gf "Help me pick?"

        $ d4_wd_ryan = format_choice("ch01_d4_wardrobe_ryan_picks", "Let me choose your outfit.")
        $ d4_wd_leia = format_choice("ch01_d4_wardrobe_leia_decides", "Wear whatever you feel best in.")

        menu:
            "[d4_wd_ryan]":
                $ apply_choice("ch01_d4_wardrobe_ryan_picks")
                python:
                    # Love outfit control: Leia asked, so the picker is allowed here. Never offered
                    # outside an explicit Leia request. Swimwear and nightlife items are filtered out.
                    d4_day_options = ch01_d4_day_outfit_options()
                    d4_day_pick = renpy.call_screen(
                        "leia_love_outfit_picker",
                        options=d4_day_options,
                        title_text=('Pick ' + girlfriend_name + "'s Day Four market outfit"),
                    )
                    love_route_wear_request(d4_day_pick, route_lane="love")
                    set_story_value("ch01_d4_day_outfit_id", d4_day_pick)
                    set_story_value("ch01_d4_day_outfit_source", "ryan")

                mc "Wear the [outfit_name(d4_day_pick)]."
                if love_outfit_is_daring(d4_day_pick):
                    gf "For a market. Okay. Bold."
                    gf "I'm wearing it because you asked. If a stall owner winks, I'm blaming you."
                    mc "Reasonable."
                else:
                    gf "Sensible. Warm. Walkable."
                    gf "Look at you, building a woman a dependable outfit."
                    mc "I contain multitudes."
                gf "Don't push it."

            "[d4_wd_leia]":
                $ apply_choice("ch01_d4_wardrobe_leia_decides")
                mc "Wear whatever you feel best in."
                gf "You say that now."
                mc "I'll say it later too."
                gf "Then I'm choosing comfort and sandals."
                python:
                    attempt_wear_outfit("casual_default")
                    set_story_value("ch01_d4_day_outfit_id", "casual_default")
                    set_story_value("ch01_d4_day_outfit_source", "leia")
                "She dressed fast, like someone who'd just been given back a small piece of the morning."

    elif d4_lane == "exhibitionism":
        scene bg ch01_master_bedroom
        with dissolve

        "[girlfriend_name] stood in front of the open suitcase with two options on the bed: her everyday market-walking outfit, and the loose low-cut top and fitted skirt from the second night's dinner."
        gf "Walking day. Market. Maya in my ear. Tell me which one."
        gf "And before you answer, I want you to know I'm going to ask why."

        $ d4_wd_bold = format_choice("ch01_d4_wardrobe_bolder", "The low-cut one.")
        $ d4_wd_comf = format_choice("ch01_d4_wardrobe_comfort", "The comfortable one. Walking is a long game.")

        menu:
            "[d4_wd_bold]":
                $ apply_choice("ch01_d4_wardrobe_bolder")
                mc "The low-cut one."
                gf "Why?"
                mc "Because you looked incredible in it and I'm greedy."
                gf "That's an honest answer."
                "She took it off the bed and held it against herself."
                gf "A loose top is a very small amount of brave. It's market brave. I can do market brave."
                $ d4_wore = ch01_d4_wear("d2_loose_low_cut")
                $ set_story_value("ch01_d4_day_outfit_id", "d2_loose_low_cut")
                $ set_story_value("ch01_d4_day_outfit_source", "ryan")

            "[d4_wd_comf]":
                $ apply_choice("ch01_d4_wardrobe_comfort")
                mc "The comfortable one. Walking is a long game."
                gf "That's the sensible answer."
                mc "I'm full of those."
                gf "You are not. That's why I'm slightly disappointed."
                mc "Do you want me to say the other one?"
                gf "I want you to mean it when you say it. Tonight, maybe."
                python:
                    attempt_wear_outfit("casual_default")
                    set_story_value("ch01_d4_day_outfit_id", "casual_default")
                    set_story_value("ch01_d4_day_outfit_source", "ryan")

    else:
        scene bg ch01_d4_breakfast_terrace
        with dissolve

        $ d4_fine_n = get_story_value("ch01_d4_ntr_fine_count", 0)

        if get_story_value("ch01_d4_morning_reply") == "joined":
            "I found her on the terrace in the good chair, which did wobble, with two cups and a look I couldn't fully read."
        else:
            "By the time I got downstairs the coffee was lukewarm and [girlfriend_name] was already dressed, the second cup untouched across from her."

        if d4_fine_n > 0:
            python:
                d4_wore = ch01_d4_wear("d2_loose_low_cut")
                set_story_value("ch01_d4_day_outfit_id", "d2_loose_low_cut")
            "She was wearing the loose low-cut top and fitted skirt, the bolder of the two evening options she'd packed."
        else:
            python:
                attempt_wear_outfit("casual_default")
                set_story_value("ch01_d4_day_outfit_id", "casual_default")
            "She was in her everyday walking clothes, hair pinned up with the clip, comfortable and a little guarded."

        $ set_story_value("ch01_d4_day_outfit_source", "leia")
        "She hadn't asked what I thought she should wear. That was new."

        $ d4_ntr_comp = format_choice("ch01_d4_ntr_compliment", "You look great. Really.")
        $ d4_ntr_guard = format_choice("ch01_d4_ntr_guarded", "Going out like that?")
        $ d4_ntr_flat = format_choice("ch01_d4_ntr_flat", "Nice.")

        menu:
            "[d4_ntr_comp]":
                $ apply_choice("ch01_d4_ntr_compliment")
                mc "You look great. Really."
                gf "Thank you."
                "She looked at me a second longer than the compliment needed, as if checking it for a catch."
                gf "That's the nicest thing you've said to me in a while."
                mc "That might be a problem."
                gf "It might be a start."

            "[d4_ntr_guard]":
                $ apply_choice("ch01_d4_ntr_guarded")
                mc "Going out like that?"
                gf "Like what?"
                mc "Nothing. Forget it."
                gf "No. Like what?"
                "I didn't have a version of the answer that I could say out loud without sounding like someone I didn't want to be."
                gf "That's what I thought."
                $ set_story_value("ch01_d4_wardrobe_friction", True)

            "[d4_ntr_flat]":
                $ apply_choice("ch01_d4_ntr_flat")
                mc "Nice."
                gf "Nice."
                "She repeated it back at me like she was holding it up to the light."
                gf "Thanks."
                "I could hear exactly how little I'd put into it, a second too late to take it back."

    $ set_story_flag("ch01_d4_scene_03_complete")
    jump ch01_day4_scene_04_breakfast


label ch01_day4_scene_04_breakfast:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    scene bg ch01_d4_breakfast_terrace
    with dissolve

    "The terrace table had been set for four with the kind of care that suggested [friend_name] had been standing over it."
    "[friend_name] arrived first, with his sunglasses restored to office, and a plate of pancakes held out like a diplomatic gift."
    friend "Teodoro made them. I supervised."
    gf "He didn't make them."
    friend "I made the decision to have them."
    "Maya came out last, in [friend_name]'s second-best sunglasses, which nobody mentioned."
    maya "Don't start."
    mc "I haven't said a word."
    maya "Your face is doing the thing."
    friend "That's what I said."

    "[girlfriend_name] pinned her hair back with the clip from the club, the one that had made so many appearances in the story of that night."
    maya "That clip has seen more action than I have."
    friend "Maya."
    maya "What? It's a hairclip. It has a past."

    if d4_lane == "love":
        gf "It was a very good night."
        "She said it to the table, and her eyes came to me while she did."
    elif d4_lane == "exhibitionism":
        gf "It was a very good night."
        "She said it to the table, and her eyes came to me while she did. Maya raised an eyebrow. I raised the same one back."
    else:
        "[girlfriend_name] touched the clip once, a small habit I'd started to notice."
        "Maya had put me in the chair beside [girlfriend_name]'s. She'd done it so casually that I'd only seen the choreography afterward."

    $ d4_dessert = get_story_value("ch01_d3_maya_dessert", None)
    if d4_dessert:
        maya "I'm still thinking about the dessert last night."
        friend "You're welcome."
        if d4_dessert == "chocolate":
            maya "It was chocolate. It was chocolate and it was correct."
        elif d4_dessert == "recommended":
            maya "The bartender's recommendation. A man who trusts professionals."
        else:
            maya "A surprise dessert. Nobody warned me it was thoughtful."
        "[friend_name] turned a faint pink behind the sunglasses."

    maya "Before anyone asks. Yes, I slept. In a bed. [friend_name]'s blanket policy is aggressive."
    friend "I run a tight ship."
    maya "He folded the corner of the sheet. Like a hotel."
    friend "Standards."
    "Neither of them said anything else, and neither of them was lying, and both of them were watching how the table took it."

    $ d4_bk_leave = format_choice("ch01_d4_breakfast_leave_it", "Reach for the pancakes. Not my business.")
    $ d4_bk_tease = format_choice("ch01_d4_breakfast_tease", ('Hotel corners. ' + friend_name + ", that's practically a proposal."))
    $ d4_bk_ask = format_choice("ch01_d4_breakfast_ask_maya", "Maya. You good? Honestly.")

    menu:
        "[d4_bk_leave]":
            $ apply_choice("ch01_d4_breakfast_leave_it")
            "I reached for the pancakes and let the subject go."
            maya "Thank you."
            mc "For what?"
            maya "Nothing. The best thing you've done all week."
            friend "That's a low bar."
            maya "It is, and he cleared it."

        "[d4_bk_tease]":
            $ apply_choice("ch01_d4_breakfast_tease")
            mc "Hotel corners. [friend_name], that's practically a proposal."
            friend "It's linen etiquette."
            maya "It's a very specific kind of etiquette."
            gf "I'm writing this down."
            friend "Please don't."
            "Everyone laughed. [friend_name]'s laugh came a half second late and a little relieved."

        "[d4_bk_ask]":
            $ apply_choice("ch01_d4_breakfast_ask_maya")
            "I said it quietly enough that it was only for her."
            maya "I'm good. I'm better than good, and I'm not narrating it before I've decided what it is."
            maya "Ask me when I know."
            mc "That's fair."
            maya "I'm very fair. It's my brand."
            "Across the table, [friend_name], who had heard none of it, passed her the syrup without looking up. She took it without looking either."
            $ set_story_flag("ch01_d4_maya_real_talk")

    maya "Right. Now that we're all fed and emotionally stable, announcements."
    maya "Today is market day, and it is also a competition."
    friend "Those words never end well."
    maya "That's what you said about the swim rings."
    friend "And I was right."
    maya "You were wedged in a ring."
    maya "Teams: the couples versus the friends. You each photograph your own person. The other team scores it. Loser pays for dinner tonight."
    gf "What are the prompts?"
    maya "You get them at the market. That's the fun."

    if d4_lane == "ntr":
        "[girlfriend_name] glanced at me, then at her plate."
        gf "Fine. I'm in."
        "She didn't look relieved. She looked like she'd decided to be brave about something small so she wouldn't have to be about something large."
    else:
        gf "We're going to destroy you."
        maya "You're going to try."
        friend "I want the record to show I never agreed to be the friends."

    $ set_story_flag("ch01_d4_scene_04_complete")
    jump ch01_day4_scene_05_market_walk


label ch01_day4_scene_05_market_walk:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    scene bg ch01_d4_market
    with fade

    # AUDIO TODO: market ambience, bargaining chatter, a distant radio.
    "The market was a lane of striped awnings and noise, honey and spices and sunglasses stacked on every available surface."
    "Maya took [friend_name]'s arm and steered him ahead without being asked, which left [girlfriend_name] and me a few comfortable steps behind."

    if d4_lane == "ntr":
        "[girlfriend_name] walked beside me with her hands in her pockets, careful about the space between us."
        "Maya looked back once over her shoulder, saw the gap, and turned around again with a very small shrug that said she was working on it."
    else:
        "[girlfriend_name]'s fingers found mine somewhere around the second stall."
        gf "Hand-holding in public. Very bold of us."
        mc "I think we've done worse in public."
        gf "I am choosing to forget the pool."
        mc "I'm choosing to remember the top."
        gf "[player_name]!"

    "A honey stall sat at the end of the lane, jars of amber glass stacked in pyramids."
    stranger "Wild honey. Very fresh. From the hills."
    friend "Define wild."
    stranger "From bees that live in the hills."
    friend "Right. That is exactly the part I was asking about."
    "He took one slow step backward, then another, until he was standing behind the sunglasses stall."
    maya "[friend_name]."
    friend "I'm browsing."
    maya "You're hiding."
    friend "I'm browsing at a safe distance."

    "A single bee, either very brave or very lost, wandered across the rim of the honey jars. [friend_name] vanished behind the sunglasses rack so completely that the rack swayed."
    gf "He moved six inches without his feet again."
    mc "Maya's going to put that on a plaque."
    maya "It's already on a plaque. In my heart."

    "The stall owner offered [girlfriend_name] a wooden stick dipped in honey."
    gf "For me?"
    stranger "For the lady who is not afraid of bees."
    gf "That is the nicest thing anyone's said to me since the swim rings."

    if d4_lane == "ntr":
        "She took a taste, then held the stick out toward me without quite looking."
        "I took it. For one second it felt normal."
    elif d4_lane == "exhibitionism":
        "She tasted the honey, then slowly licked a drip off her thumb, with a look that had nothing whatsoever to do with honey."
        mc "You're doing that on purpose."
        gf "I'm doing it at a stall, with a man selling jars. I'm being very responsible."
        "Maya, three stalls away, whistled once without turning around."
    else:
        "She tasted the honey, then offered me the stick, her eyes on my face while I did."
        gf "Good?"
        mc "Dangerous."
        gf "That's the correct answer."

    $ set_story_flag("ch01_d4_market_honey_bee_callback")
    $ set_story_flag("ch01_d4_scene_05_complete")
    jump ch01_day4_scene_06_photo_hunt


label ch01_day4_scene_06_photo_hunt:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    scene bg ch01_d4_market
    with dissolve

    maya "Prompts."
    "She held up a creased card and read it with the voice of a game-show host."
    maya "Prompt one. Your person, looking like themselves."
    friend "That's not a prompt. That's a trap."
    maya "Prompt two, for later. Something sweet. Prompt three, something that looks like [friend_name]'s personality."
    friend "I hate this."
    maya "Sunglasses stall. Go."

    "Maya dragged [friend_name] toward the sunglasses stall with the cheerful efficiency of someone who has done this to many men."
    "That left the other half of our team with a phone, a prompt, and a stall owner offering [girlfriend_name] a pair of round tortoiseshell sunglasses."
    gf "[player_name]. You're photographing me."
    mc "So I am."
    gf "How do you want me?"
    "She heard it a second after she said it. She went pink, and did not take it back."

    $ d4_ph_candid = format_choice("ch01_d4_photo_candid", "Catch her mid-laugh without telling her.")
    $ d4_ph_pose = format_choice("ch01_d4_photo_pose", "Ask her to give the camera that look.")
    $ d4_ph_swap = format_choice("ch01_d4_photo_swap", "Hand her the phone. 'You take one of me first.'")
    $ d4_ph_skip = format_choice("ch01_d4_photo_skip", "Check a message first. 'Give me a second.'")

    menu:
        "[d4_ph_candid]":
            $ apply_choice("ch01_d4_photo_candid")
            $ set_story_value("ch01_d4_photo_style", "candid")
            "I raised the phone and said nothing, and waited until the stall owner told her a joke she wasn't ready for."
            gf "Wait, he said what?"
            "She laughed with her whole face, one hand pushing the tortoiseshell frames up her nose."

            $ enter_cinematic_mode()
            scene cg ch01_d4_photo_candid
            with dissolve
            # CG TODO (artist): ch01_d4_photo_candid. Ryan POV, Ryan never in frame. See visuals file for the brief.
            "Click."
            $ exit_cinematic_mode()
            scene bg ch01_d4_market
            with dissolve

            gf "Did you just take that?"
            mc "Yes."
            gf "I wasn't ready."
            mc "That's why it's good."
            python:
                phone_add_message(
                    "leia", "player",
                    text="Maya's prompt one. Your person, looking like themselves.",
                    message_id="ch01_d4_leia_photo_candid",
                    attachment_id="ch01_d4_photo_candid",
                    attachment_label=(girlfriend_name + ', market, candid'),
                    mark_unread=False,
                )
                phone_add_message(
                    "leia", "leia",
                    text="Okay that's actually good. Send it to me. Do not send it to Maya.",
                    message_id="ch01_d4_leia_photo_candid_reply",
                    mark_unread=True, notify=True, notification_title=girlfriend_name,
                )
            "She looked at the photo for a long moment. Then she looked at me, not at the picture."
            $ set_story_flag("ch01_d4_photo_candid_taken")

        "[d4_ph_pose]":
            $ apply_choice("ch01_d4_photo_pose")
            $ set_story_value("ch01_d4_photo_style", "posed")
            mc "Give the camera that look."
            gf "Which look?"
            mc "The one you gave the window this morning."
            gf "You absolute menace."
            "She pushed the sunglasses down her nose with one finger, tilted her head, and raised a single eyebrow."

            $ enter_cinematic_mode()
            scene cg ch01_d4_photo_pose
            with dissolve
            # CG TODO (artist): ch01_d4_photo_pose. Ryan POV, Ryan never in frame.
            "Click."
            $ exit_cinematic_mode()
            scene bg ch01_d4_market
            with dissolve

            gf "I'm only doing this because it's a game and the game has rules."
            mc "Of course."
            gf "And because you're the one holding the camera."
            "She said that second part to the pavement, not to me."
            python:
                phone_add_message(
                    "leia", "player",
                    text="Maya's prompt one. Your person, looking like themselves.",
                    message_id="ch01_d4_leia_photo_pose",
                    attachment_id="ch01_d4_photo_pose",
                    attachment_label=(girlfriend_name + ', sunglasses stall, posed'),
                    mark_unread=False,
                )
                phone_add_message(
                    "leia", "leia",
                    text="That is a very good picture of a woman who is pretending not to like it.",
                    message_id="ch01_d4_leia_photo_pose_reply",
                    mark_unread=True, notify=True, notification_title=girlfriend_name,
                )
            $ set_story_flag("ch01_d4_photo_pose_taken")

        "[d4_ph_swap]":
            $ apply_choice("ch01_d4_photo_swap")
            $ set_story_value("ch01_d4_photo_style", "swap")
            mc "You take one of me first."
            gf "Excuse me?"
            mc "Rule one. You're my person too."
            gf "Oh my God. He's rules-lawyering."
            "She took the phone before I changed my mind, and I found myself holding a jar of honey for no reason I could name."

            $ enter_cinematic_mode()
            scene cg ch01_d4_photo_swap
            with dissolve
            # CG TODO (artist): ch01_d4_photo_swap. Ryan POV, Ryan never in frame.
            "Click."
            $ exit_cinematic_mode()
            scene bg ch01_d4_market
            with dissolve

            gf "You look terrified."
            mc "I'm holding a jar of bee juice."
            gf "That's what I'm saying."
            "She handed the phone back. I took my turn, and she turned to the stall with her back half to me and her laugh already coming."
            python:
                phone_add_message(
                    "leia", "leia",
                    text="Saving the one I took of you. You look terrified. For the box.",
                    message_id="ch01_d4_leia_photo_swap_reply",
                    mark_unread=True, notify=True, notification_title=girlfriend_name,
                )
            $ set_story_flag("ch01_d4_photo_swap_taken")

        "[d4_ph_skip]":
            $ apply_choice("ch01_d4_photo_skip")
            $ set_story_value("ch01_d4_photo_style", "skipped")
            mc "Give me a second."
            "I checked my phone. There was nothing on it. I scrolled anyway."
            gf "[player_name]."
            mc "One sec."
            "When I looked up, Maya had drifted back from the sunglasses stall with [friend_name] in tow."
            maya "[girlfriend_name], hold still. I'll do this one."
            "She raised her own phone and took the picture before [girlfriend_name] had finished turning. [girlfriend_name] smiled the way you smile for a camera you didn't choose."
            maya "Got it."
            gf "Thanks."
            "She wasn't angry. That was the part that stayed with me."
            $ set_story_flag("ch01_d4_photo_skipped")

    $ set_story_flag("ch01_d4_scene_06_complete")
    jump ch01_day4_scene_07_photo_results


label ch01_day4_scene_07_photo_results:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")
    $ d4_style = get_story_value("ch01_d4_photo_style", "none")

    scene bg ch01_d4_market
    with dissolve

    "We found a low wall under an awning and Maya set up her judges' table, which was the wall."
    maya "The friends go first. [friend_name]'s entry."

    $ enter_cinematic_mode()
    scene cg ch01_d4_photo_maya_julian
    with dissolve
    # CG TODO (artist): ch01_d4_photo_maya_julian. Ryan POV, Ryan never in frame. Comic.
    "It was a good photograph of Maya, perfectly framed. A large blurred thumb covered one corner of the lens."
    $ exit_cinematic_mode()
    scene bg ch01_d4_market
    with dissolve

    maya "That's my best angle."
    friend "I know."
    gf "That's your thumb."
    friend "It's called depth."
    maya "It's called a thumb."
    friend "I was told 'photographer of the year' at some point and I'm still processing it."
    maya "Four out of five. It's a great angle with a thumb in it."
    gf "Three. Thumb's a crime."
    friend "You're both a tough room."

    maya "[player_name] and [girlfriend_name]."

    if d4_style == "candid":
        maya "Oh."
        gf "What?"
        maya "Nothing. That's a person who's loved."
        friend "Five."
        maya "It's unfair. He actually knows her face."
        "[girlfriend_name] looked at her shoes and smiled so hard it made her dimple show."
        $ set_story_value("ch01_d4_hunt_winner", "ryan_leia")
    elif d4_style == "posed":
        maya "It's giving brand deal."
        gf "It's giving a woman who needed sunglasses."
        friend "Four. The eyebrow is doing a lot of work."
        maya "Four. The eyebrow is the star."
        $ set_story_value("ch01_d4_hunt_winner", "ryan_leia")
    elif d4_style == "swap":
        maya "Two photos?"
        gf "Rule one. We're each other's person."
        maya "Rules lawyer."
        friend "Five. And [player_name] looks like he's being held hostage by honey."
        maya "Five. It's chaos and it's affectionate."
        $ set_story_value("ch01_d4_hunt_winner", "ryan_leia")
    else:
        maya "Mine, for [player_name] and [girlfriend_name]. Since [player_name] was busy."
        "She held up the picture she'd taken. It was a perfectly competent photo of a woman smiling at the wrong camera."
        friend "Two."
        maya "Two. Technically correct, spiritually missing."
        "Nobody had said it unkindly, which somehow made it worse."
        $ set_story_value("ch01_d4_hunt_winner", "maya_julian")

    if get_story_value("ch01_d4_hunt_winner") == "maya_julian":
        maya "The friends win. [player_name], dinner's on you."
        mc "Fair."
        friend "I'd like to thank the academy."
    else:
        maya "The couples win. [friend_name], dinner's on you."
        friend "I'd like to appeal."
        maya "Appeal denied."

    if d4_lane == "ntr":
        "[girlfriend_name] laughed at the right places. She laughed at them a beat late, as if she had to check where the jokes were."

    $ set_story_flag("ch01_d4_scene_07_complete")
    jump ch01_day4_scene_08_afternoon_quiet


label ch01_day4_scene_08_afternoon_quiet:

    $ d4_lane = get_story_value("ch01_d4_lane", "love")

    scene bg ch01_d4_harbor_wall
    with fade

    "The market emptied out toward the harbor as the heat got serious. We ended up on a low stone wall above the boats, sunglasses on, ice melting in plastic cups."
    friend "[player_name]. Walk with me. I need water."
    mc "You have water."
    friend "I need different water."
    "Maya took the hint. She slid onto the wall next to [girlfriend_name] and started a conversation about nothing."

    "[friend_name] and I walked to a kiosk fifty meters away and stood in its shade."
    friend "I'm going to say one thing about last night, and then I never will again."
    mc "You don't owe me that."
    friend "I do."
    friend "You're my friend. That doesn't move, whatever happened or didn't happen behind that door. It doesn't move."
    friend "And [girlfriend_name] is your girlfriend. I'm careful where I look. I'll stay careful."

    if d4_lane == "love":
        friend "Also, you two are disgusting. Good disgusting."
    elif d4_lane == "exhibitionism":
        friend "And if you two are doing a thing, I'm not the thing. I'm furniture with opinions."
        mc "Furniture with opinions."
        friend "Soft furnishings. The opinions are private."
    else:
        friend "And whatever's going on with the two of you, don't make me the reason."
        friend "Don't make me the audience either. Talk to her."

    $ d4_j_thanks = format_choice("ch01_d4_julian_thanks", "Thanks for being straight with me.")
    $ d4_j_joke = format_choice("ch01_d4_julian_joke", "So. Pancakes.")
    $ d4_j_deflect = format_choice("ch01_d4_julian_deflect", "Not the time. Later.")

    menu:
        "[d4_j_thanks]":
            $ apply_choice("ch01_d4_julian_thanks")
            mc "Thanks for being straight with me."
            friend "Don't get weird."
            mc "I'm not."
            friend "You've got the look."
            mc "I'm allowed to be grateful."
            friend "In moderation."

        "[d4_j_joke]":
            $ apply_choice("ch01_d4_julian_joke")
            mc "So. Pancakes."
            friend "It was one pancake."
            mc "Hotel corners."
            friend "I will leave you in this kiosk."
            "He was grinning when he said it, and I could tell the thing he'd said before had cost him something to say."

        "[d4_j_deflect]":
            $ apply_choice("ch01_d4_julian_deflect")
            mc "Not the time. Later."
            friend "Right."
            "He nodded like it was an answer, and for a second he looked at me the way you look at a friend who's drifting out from the shore."
            friend "Later, then."

    "Meanwhile on the wall:"

    maya "You're quiet."
    gf "I'm thinking."
    maya "That's the dangerous thing."
    gf "You're glowing, by the way."
    maya "I'm sunburned."
    gf "It's a glowing sunburn."
    maya "He checked the thermostat three times. He asked whether I was warm enough. I'm not saying it's a thing. I'm saying I noticed."
    gf "You're going to be insufferable about this."
    maya "I'm going to be extremely cool about it."

    if d4_lane == "love":
        maya "And you?"
        gf "I'm good. I'm better than good."
        maya "I can see that. [player_name]'s looking at you like a man who's winning."
        gf "He's looking at the honey."
        maya "He is not looking at the honey."
    elif d4_lane == "exhibitionism":
        maya "And you?"
        gf "I'm fine."
        maya "That window was very open last night. I'm a light sleeper."
        gf "Maya."
        maya "I'm not asking. I'm saying the villa has walls like paper and I'm a light sleeper."
        gf "You have no evidence."
        maya "Circumstantial."
        "[girlfriend_name] hid her face behind her cup. She was grinning behind it."
    else:
        maya "And you? Don't say fine."
        gf "I'm trying to find the words."
        maya "Tell him."
        gf "I don't know where to start."
        maya "Use the dumb words. The dumb ones work."
        gf "That's your advice?"
        maya "It's my entire philosophy."

    "When [friend_name] and I came back with the water, Maya stood up with the expertise of someone who had been waiting."

    if d4_lane == "ntr":
        maya "[friend_name]. Ice. Now."
        friend "We just got water."
        maya "Ice."
        "She took his sleeve and led him away. He looked back once at me with an expression that managed to say I'm sorry and good luck at the same time."
        jump ch01_day4_scene_08_ntr_wall

    gf "We're going to get a better cup of something."
    maya "Meaning me and [friend_name] are being gently removed."
    gf "Meaning you two take your time."
    maya "I love it when she speaks in code."
    "They wandered off. [girlfriend_name] leaned against my shoulder and closed her eyes against the sun."

    if d4_lane == "love":
        gf "Today's a good day."
        mc "It's barely afternoon."
        gf "That's why I said it. I get to be right for a long time."
    else:
        gf "I'm thinking about tonight."
        mc "Yeah?"
        gf "Maya says the dinner has a dress code. She says the code is 'look photographed.'"
        gf "I said I'd think about it. I didn't say which way."
        mc "That's the most dangerous sentence you've said all day."
        gf "I know."

    $ set_story_flag("ch01_d4_scene_08_complete")
    jump ch01_day4_scene_09_getting_ready


label ch01_day4_scene_08_ntr_wall:

    $ d4_fine_n = get_story_value("ch01_d4_ntr_fine_count", 0)

    "[girlfriend_name] moved over on the wall to make room. Not much. Enough."
    gf "[player_name]."
    mc "Yeah."
    gf "I asked you once, at sunset, whether we were okay. Do you remember?"
    mc "I remember."
    "She reached up and touched the hairclip, turning it once between two fingers."
    gf "Is there anything you want to ask me?"

    $ d4_ask_gently = format_choice("ch01_d4_ntr_ask_gently", "Yes. Yesterday, at the stand. I'd rather hear it from you than guess.")
    $ d4_fine2 = format_day4_gate_choice("ch01_d4_ntr_fine_soft2", "I'm fine. There's nothing to ask.", severity="soft", gate_label="D4-2")
    $ d4_press = format_choice("ch01_d4_ntr_press_early", "Tell me what happened at the stand. All of it.")

    menu:
        "[d4_ask_gently]":
            $ apply_choice("ch01_d4_ntr_ask_gently")
            mc "Yes. Yesterday, at the stand. I'd rather hear it from you than guess."
            "[girlfriend_name] let out a breath that sounded as if she'd been holding it since the path."
            call ch01_day4_ntr_disclosure
            $ set_story_value("ch01_d4_disclosure_when", "harbor_wall")

        "[d4_fine2]":
            $ apply_choice("ch01_d4_ntr_fine_soft2")
            $ set_story_value("ch01_d4_ntr_fine_count", d4_fine_n + 1)
            $ set_story_flag("ch01_d4_ntr_soft_gate")
            mc "I'm fine. There's nothing to ask."
            gf "Okay."
            "The hairclip clicked shut in her hand."
            "She looked out at the boats for a while, the way you look at something because you've run out of other places to look."
            if current_choice_mode() == "developer":
                centered "NTR SOFT GATE D4-2 - ch01_d4_ntr_soft_gate = True (count = 2 if D4-1 also taken)"
            elif current_choice_mode() == "full":
                centered "Major relationship consequence."
            elif current_choice_mode() == "insight":
                centered "[girlfriend_name] stops opening doors."

        "[d4_press]":
            $ apply_choice("ch01_d4_ntr_press_early")
            mc "Tell me what happened at the stand. All of it."
            gf "You make it sound like an interrogation."
            mc "I'm asking."
            gf "You're asking like you want to catch me."
            "She stood. The clip stayed in her hand."
            gf "I'll tell you when you're asking because you want to know me, not because you want to catch me."
            $ set_story_flag("ch01_d4_ntr_pressed_early")

    "Down in the harbor, a boat horn blew twice and someone laughed at it."

    $ set_story_flag("ch01_d4_scene_08_complete")
    jump ch01_day4_scene_09_getting_ready


label ch01_day4_ntr_disclosure:

    # Shared Leia disclosure beat (NTR lane). Called from the harbor-wall opening and the
    # night gate. NON-EXPLICIT: told in her own words. The cutout encounter is the only
    # thing disclosed. The club is explicitly deferred to Day Five, honouring Day Three's
    # 'dream is not evidence' rule.

    if has_story_flag("ch01_d3_cutout_secret"):
        gf "At the stand yesterday. Someone stopped to help."
        gf "He tried, honestly. He pulled and the frame wouldn't move, and then his hands were at my waist and it stopped being helping."
        gf "I said yes. I told him to go the second I heard Maya laugh."
        gf "I didn't tell you because you were already looking at me like I'd done something. And I had. And I couldn't make the words come out right."
    else:
        gf "I haven't been honest about yesterday."
        gf "About how much of it I liked being looked at, and about what I did when you walked away."
        gf "I didn't tell you because you were already looking at me like I'd done something, and I couldn't make the words come out right."

    gf "And the club. There's more about the club."
    gf "I want to tell it properly. Slowly. Not in one terrible gulp that you hear as a confession."
    gf "Can I tell it tomorrow?"
    "She asked it plainly. It wasn't a stall. It was a request."

    $ set_story_flag("ch01_d4_cutout_disclosed")
    $ set_story_flag("ch01_d4_club_story_deferred")
    return

