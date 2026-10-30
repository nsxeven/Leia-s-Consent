# Leia's Consent: Chapter One, Day Five ("The Water"), Scenes 1-8.
# Entry: ch01_day5_start (reached from ch01_day4_scene_16_finish when this label exists).
# Reads STORED state only (never recomputes a route): ch01_d4_end_route, ch01_d4_lane,
# ch01_d4_end_variant, ch01_d4_exposure_step, ch01_d4_exhib_variant, ch01_d4_photo_style,
# ch01_d4_dusk_outfit_id, ch01_d4_hook_reply, ch01_d4_ntr_react, flags ch01_d4_cutout_disclosed,
# ch01_d4_club_story_deferred, ch01_d4_love_exhib_seed, plus Day 2/3 keys
# (ch01_d2_mall_outfit_source, ch01_d2_pool_outfit, ch01_d3_cutout_secret, ch01_dream_response).
#
# Day Five premise: the water. Julian's family boat, "Reasonable Doubt", a private cove, no signal.
# Weather turns after midnight and the skipper takes everyone home at dawn, so Julian's "two nights"
# becomes one (humor, and it lets Day Six open on land).
# Track set at the start from ch01_d4_end_route (stored): love / exhibitionism / ntr_repaired /
# ntr_unresolved / ntr_confirmed. One visible step per day, always with Leia's stated motive.
# All intimacy is NON-EXPLICIT: cut to CG placeholder cards. Every CG is Ryan's point of view.
# The skipper (Captain Ilario) is a professional adult who stays at the helm and out of every beat.

define skipper = Character("Captain Ilario")

label ch01_day5_start:
    $ lc_review_begin("ch01_d5")

    $ set_story_flag("ch01_day_05_started")

    python:
        d5_end = get_story_value("ch01_d4_end_route", None)
        d5_lane = get_story_value("ch01_d4_lane", None)
        if d5_lane is None:
            d5_lane = get_story_value("ch01_d3_lane", "love")
        if d5_end is None:
            # Dev-skip / older-save fallback ONLY. Normal play always has ch01_d4_end_route.
            d2e = get_story_value("ch01_d2_end_route", "love")
            if d5_lane == "ntr":
                d5_end = "ntr_unresolved" if d2e == "mixed_unresolved" else "ntr_confirmed"
            elif d5_lane == "exhibitionism":
                d5_end = "exhibitionism"
            else:
                d5_end = "love"
        d5_track = {
            "love": "love",
            "exhibitionism": "exhibitionism",
            "love_repaired": "ntr_repaired",
            "ntr_unresolved": "ntr_unresolved",
            "ntr_confirmed": "ntr_confirmed",
        }.get(d5_end, "love")
        set_story_value("ch01_d5_d4_end", d5_end)
        set_story_value("ch01_d5_lane", d5_lane)
        set_story_value("ch01_d5_track", d5_track)
        set_story_value("ch01_d5_end_route_pending", {"love": "love", "exhibitionism": "exhibitionism", "ntr_repaired": "love_repaired", "ntr_unresolved": "ntr_unresolved", "ntr_confirmed": "ntr_confirmed"}[d5_track])
        set_story_value("ch01_d5_end_variant", "none")
        set_story_value("ch01_d5_pack_outfit_id", "casual_default")
        set_story_value("ch01_d5_swim_outfit_id", "pool_conservative")
        set_story_value("ch01_d5_evening_outfit_id", "resort_dinner_dress")
        set_story_value("ch01_d5_photo_group", "none")
        set_story_value("ch01_d5_exposure_step", "none")
        set_story_value("ch01_d5_exhib_variant", "none")
        set_story_value("ch01_d5_leia_call", None)
        set_story_value("ch01_d5_private_photo", "none")
        set_story_value("ch01_d5_ntr_outcome", d5_end if d5_track.startswith("ntr") else "none")
        set_story_value("ch01_d5_ntr_react", None)
        set_story_value("ch01_d5_react_return", "sunset")
        set_story_value("ch01_d5_disclosure_when", None)
        set_story_value("ch01_d5_snorkel_first", "leia")
        set_story_value("ch01_d5_secret_traded", "none")
        set_story_value("ch01_d5_bunk", "cabin")
        set_story_value("ch01_d5_truth_ryan", "none")
        set_story_value("ch01_d5_invite_reply", "none")

    scene black
    with fade
    centered "{size=50}CHAPTER ONE - DAY FIVE{/size}"

    jump ch01_day5_scene_01_boarding


label ch01_day5_scene_01_boarding:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_hook = get_story_value("ch01_d4_hook_reply", "in")

    scene bg ch01_d5_pier_morning
    with fade

    # AUDIO TODO: gulls, halyards pinging against masts, a diesel engine warming up.

    "The pier at seven in the morning smelled of rope, diesel and somebody else's breakfast."
    "At the end of it, a white sailboat with a blue stripe sat very still, as if she had heard about us."
    "Across her stern, in tidy letters: REASONABLE DOUBT."
    maya "Please tell me it's named after the law firm."
    friend "It's named after the law firm."
    maya "Oh, I love him."
    friend "That's my father, Maya. Don't love my father."
    "A compact woman in a faded cap and sunglasses looked down from the cockpit, taking us in one at a time like a customs officer."
    skipper "Captain Ilario. Four guests. Two nights. Please keep the number of guests at four."
    friend "We have a lot of faith in the number."
    skipper "Good. Faith is not a flotation device."

    if d5_hook == "maybe":
        maya "You said it depended on the morning, [player_name]. It's the morning."
        mc "It turned out the morning was fine."
        maya "The morning's always fine. It's you that has to turn up."
    elif d5_hook == "ask_leia":
        friend "[player_name] checked with [girlfriend_name] first. I want that noted in the minutes."
        maya "[friend_name] is nominating himself for secretary."
    else:
        maya "[player_name] said 'we're in' and I would like to thank him for his enthusiasm. It was a very average amount."

    if d5_track == "love":
        "[girlfriend_name]'s hand was in mine before we were off the gangway. She carried a canvas tote with a length of pale rope sticking out of the top."
        mc "What's the rope for?"
        gf "That's the plan."
        mc "It's a lot of rope."
        gf "It's very little rope. I measured."
        if has_story_flag("ch01_d4_love_exhib_seed"):
            gf "And no, not that kind of rope. Get your face under control."
            mc "I contain it well."
            gf "You really, really don't."
        if get_story_value("ch01_d4_exhib_variant", "none") == "opt_out_private":
            gf "I told you I'd say when I wanted the window back. This isn't that. This is better."
    elif d5_track == "exhibitionism":
        "[girlfriend_name] wore round sunglasses and the expression of someone carrying a secret in a very small bag."
        gf "Morning, partner in crime."
        mc "What's the idea?"
        gf "You said yes. You don't get the idea until the water."
        mc "That's not how yes works."
        gf "It's exactly how yes works when I've already packed."
    elif d5_track == "ntr_repaired":
        "[girlfriend_name]'s hand found mine at the top of the gangway. She held on longer than she needed to."
        gf "After lunch. I'm going to tell you the rest. All of it."
        mc "Okay."
        gf "I want to be somewhere I can't leave when I say it. A boat felt right."
        mc "That's the most sensible thing anyone's said about a boat."
    elif d5_track == "ntr_unresolved":
        "[girlfriend_name] was already on the pier, a little apart, with Maya's arm hooked through hers."
        gf "Morning."
        mc "Morning."
        "It was the kind of 'morning' two people say when both of them have rehearsed the next sentence and neither will say it first."
        "Maya looked between us and decided, visibly, to be loud."
    else:
        "Maya and [friend_name] took me by either elbow before I'd reached the gangway."
        maya "Friend patrol."
        friend "We've been told it's mandatory."
        mc "By whom?"
        maya "By the part of us that loves you and is tired."
        "[girlfriend_name] stood a few steps ahead with her bag on both shoulders, not looking back, not exactly avoiding it either."

    $ d5_card = ch01_d5_track_text()
    if d5_card:
        centered "[d5_card]"

    "Bags went down the companionway, one at a time, with a lot of commentary."
    jump ch01_day5_scene_01_packing


label ch01_day5_scene_01_packing:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_src = get_story_value("ch01_d2_mall_outfit_source", "leia")

    scene bg ch01_d5_boat_deck
    with dissolve

    if d5_track == "love":
        "[girlfriend_name] unzipped her bag on the cockpit bench, sorting like a woman defusing something sweet."
        gf "I packed three outfits for the boat and none of them are right. Help?"

        $ d5_pk_ryan = format_choice("ch01_d5_pack_ryan_picks", "Let me choose what you wear on the boat.")
        $ d5_pk_leia = format_choice("ch01_d5_pack_leia_decides", "Wear whatever you want. Salt will win anyway.")

        menu:
            "[d5_pk_ryan]":
                $ apply_choice("ch01_d5_pack_ryan_picks")
                python:
                    d5_pk_options = ch01_d5_pack_options()
                    d5_pk_pick = renpy.call_screen(
                        "leia_love_outfit_picker",
                        options=d5_pk_options,
                        title_text=('Pick ' + girlfriend_name + "'s boat outfit"),
                    )
                    love_route_wear_request(d5_pk_pick, route_lane="love")
                    set_story_value("ch01_d5_pack_outfit_id", d5_pk_pick)
                    set_story_value("ch01_d5_pack_outfit_source", "ryan")
                mc "The [outfit_name(d5_pk_pick)]."
                if love_outfit_is_swimwear(d5_pk_pick):
                    gf "A swimsuit on a boat. Practical and a little bit brave."
                elif love_outfit_is_daring(d5_pk_pick):
                    gf "That's a lot of outfit for a ship."
                    gf "I'm doing it because you asked, and because I want to."
                else:
                    gf "Sensible. I'll wear it like I invented it."
                gf "Swimsuit's underneath. You'll see it when I'm brave enough or when it's time to jump, whichever is first."

            "[d5_pk_leia]":
                $ apply_choice("ch01_d5_pack_leia_decides")
                mc "Wear whatever you want. Salt will win anyway."
                gf "That's the most romantic thing a person has ever said about salt."
                $ d5_pk_wore = ch01_d5_wear("d2_loose_low_cut")
                $ set_story_value("ch01_d5_pack_outfit_id", "d2_loose_low_cut")
                $ set_story_value("ch01_d5_pack_outfit_source", "leia")
                "She chose the loose top and shorts, tied her hair back, and clipped it, naturally, with the hairclip."

        if d5_src == "ryan":
            gf "I did bring the mini for tonight. You bought it. So dinner is technically your fault."
        else:
            gf "I did bring the mini for tonight. I bought it myself. So dinner is entirely my fault."
        mc "Dinner on a boat in a Black Cutout Mini."
        gf "I'm not saying it's wise. I'm saying I packed it."

    elif d5_track == "exhibitionism":
        "[girlfriend_name] emptied two swimsuits onto the bench: the classic one and the bolder one from the pool."
        gf "One of these is a decoy. Which goes on top of the bag?"
        $ d5_bolder_ok = ch01_d5_bolder_swim_ok()

        $ d5_pk_bold = format_choice("ch01_d5_pack_bolder", "The bolder one.")
        $ d5_pk_class = format_choice("ch01_d5_pack_classic", "The classic one. Let the day decide.")
        $ d5_pk_her = format_choice("ch01_d5_pack_her_call", "Neither. Surprise me.")

        menu:
            "[d5_pk_bold]":
                $ apply_choice("ch01_d5_pack_bolder")
                mc "The bolder one."
                if d5_bolder_ok:
                    gf "I thought you might say that."
                    $ d5_pk_wore = ch01_d5_wear("pool_bolder")
                    $ set_story_value("ch01_d5_swim_outfit_id", "pool_bolder")
                    $ set_story_value("ch01_d5_pack_outfit_source", "ryan")
                    gf "It goes on top. That doesn't mean it goes on me. Yet."
                else:
                    gf "I like that you asked. I'm not there yet. Today."
                    gf "Ask me again in a day. Not a threat. A schedule."
                    $ set_story_value("ch01_d5_swim_outfit_id", "pool_conservative")
                    $ set_story_value("ch01_d5_pack_outfit_source", "leia_declined_bolder")
                    $ set_story_flag("ch01_d5_wardrobe_friction")
                    $ d5_pk_wore = ch01_d5_wear("pool_conservative")
                    $ d5_gate_text = outfit_requirement_text("pool_bolder")
                    if d5_gate_text:
                        centered "[d5_gate_text]"
            "[d5_pk_class]":
                $ apply_choice("ch01_d5_pack_classic")
                mc "The classic. Let the day decide."
                gf "That's very wise. I'll tell the day."
                $ d5_pk_wore = ch01_d5_wear("pool_conservative")
                $ set_story_value("ch01_d5_swim_outfit_id", "pool_conservative")
                $ set_story_value("ch01_d5_pack_outfit_source", "ryan")
            "[d5_pk_her]":
                $ apply_choice("ch01_d5_pack_her_call")
                mc "Neither. Surprise me."
                if d5_bolder_ok:
                    gf "You're going to regret that sentence in about six hours."
                    gf "Possibly in a very good way."
                    $ d5_pk_wore = ch01_d5_wear("pool_bolder")
                    $ set_story_value("ch01_d5_swim_outfit_id", "pool_bolder")
                else:
                    gf "That's a lot of trust."
                    $ d5_pk_wore = ch01_d5_wear("pool_conservative")
                    $ set_story_value("ch01_d5_swim_outfit_id", "pool_conservative")
                $ set_story_value("ch01_d5_pack_outfit_source", "leia")

        $ set_story_value("ch01_d5_pack_outfit_id", get_story_value("ch01_d5_swim_outfit_id", "pool_conservative"))
        if has_story_flag("ch01_d4_exhib_ryan_likes_watching"):
            gf "And yes. I remember what you told me about liking to watch. I'm being very good and not rushing it."
            mc "You're being terrible."
            gf "I'm being strategic."

    else:
        "[girlfriend_name] packed the way she'd packed all week: neatly, alone, and without asking."
        if d5_track == "ntr_repaired":
            gf "I put the cream wrap in, in case it gets cold. And the mini. In case I'm braver after I say it."
        elif d5_track == "ntr_unresolved":
            gf "I packed light. In case it turns out I'm the one who needs a quick exit."
        else:
            gf "I packed for two nights. I didn't pack for three."
        "She zipped the bag. It was the exact size of a decision."

        $ d5_pk_help = format_choice("ch01_d5_ntr_pack_help", "Offer to carry her bag down the companionway.")
        $ d5_pk_joke = format_choice("ch01_d5_ntr_pack_joke", "Make a joke about how little she packed.")
        $ d5_pk_nothing = format_choice("ch01_d5_ntr_pack_nothing", "Say nothing. Let her get on with it.")

        menu:
            "[d5_pk_help]":
                $ apply_choice("ch01_d5_ntr_pack_help")
                mc "Can I carry that down for you?"
                if d5_track == "ntr_confirmed":
                    gf "It isn't heavy."
                    mc "I know. I'd like to carry something that isn't mine."
                    gf "...Okay."
                else:
                    gf "Please."
                "She let me take the strap. It was an inch, not a mile, and I took the inch."
            "[d5_pk_joke]":
                $ apply_choice("ch01_d5_ntr_pack_joke")
                mc "Two nights and one tote bag. Maya's going to invoice you."
                gf "She already has."
                "She almost laughed. Almost counted for something."
            "[d5_pk_nothing]":
                $ apply_choice("ch01_d5_ntr_pack_nothing")
                "I stood there with my hands in my pockets while [girlfriend_name] carried her own bag down the companionway."

        $ d5_wore = ch01_d5_wear("pool_conservative")
        $ set_story_value("ch01_d5_swim_outfit_id", "pool_conservative")
        $ set_story_value("ch01_d5_pack_outfit_source", "leia")

    $ set_story_flag("ch01_d5_scene_01_complete")
    jump ch01_day5_scene_02_seasick


label ch01_day5_scene_02_seasick:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_deck
    with dissolve

    # AUDIO TODO: engine up, hull slap, a long-suffering wave under the bow.

    "Twenty minutes past the breakwater, [friend_name] turned a shade of green I could only call 'regret'."
    friend "I'm fine."
    maya "You are the color of a lime."
    friend "It's the light."
    maya "It's seven forty in the morning, [friend_name]. The light is neutral."
    "He sat on the cockpit bench with his eyes fixed on the horizon like a man trying to negotiate with it."
    skipper "Ten more minutes and it passes."
    friend "You said that ten minutes ago."
    skipper "And it was true then."
    maya "I'm going to be so smug about this. I want you all to be ready."
    maya "I have a tab for the boat. It starts now."

    "I took a seat beside him. [girlfriend_name], a few feet away, unscrewed a bottle of water and slid it across without saying anything."

    $ d5_js_stay = format_choice("ch01_d5_julian_stay", "Sit with him. Keep him talking.")
    $ d5_js_joke = format_choice("ch01_d5_julian_joke", "Tell him the horizon's on his side.")
    $ d5_js_leave = format_choice("ch01_d5_julian_leave", "Leave him to Maya and go find some shade.")

    menu:
        "[d5_js_stay]":
            $ apply_choice("ch01_d5_julian_stay")
            mc "Tell me about the law firm."
            friend "It's a very boring law firm."
            mc "Good. Be boring at me."
            "He told me about conveyancing for six minutes. By the end, he was a shade of green I'd call 'apologetic'."
            friend "Thanks. That was a lot of conveyancing."
            mc "It was a lot of conveyancing."
            $ set_story_flag("ch01_d5_julian_looked_after")
        "[d5_js_joke]":
            $ apply_choice("ch01_d5_julian_joke")
            mc "Look at the horizon. It's on your side. It's the only thing that is."
            friend "Rude."
            maya "He's not wrong."
            friend "I'm being ganged up on by a lime joke."
        "[d5_js_leave]":
            $ apply_choice("ch01_d5_julian_leave")
            mc "I'll be in the shade."
            friend "Don't leave me with Maya."
            maya "He's being dramatic. I'm very gentle."
            friend "She is holding a tab."
            "I felt faintly guilty, which on a boat is hard to distinguish from the sea."

    "Somewhere between the second headland and the third, he sat up, took off his sunglasses and announced he was no longer dying."
    maya "You're at about forty percent."
    friend "I'll take forty."
    $ set_story_flag("ch01_d5_scene_02_complete")
    jump ch01_day5_scene_03_no_bars


label ch01_day5_scene_03_no_bars:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_deck
    with dissolve

    "Around nine, my phone made the small unhappy noise phones make when they stop hearing the world."
    "Signal dropped from two bars to one, then to a little gray X."
    maya "No bars."
    friend "No bars?"
    maya "No bars, [friend_name]. No group chat, no maps, no one to blame."
    skipper "There is no signal beyond the second headland. This is considered a feature."

    python:
        phone_add_message(
            "group", "maya",
            text=('(sent from the middle of nowhere, delivered whenever the sea feels like it) I have started a tab for the boat. First entry: ' + friend_name + '.'),
            message_id="ch01_d5_group_no_bars_maya",
            mark_unread=True, notify=False,
        )

    if d5_track == "love":
        gf "Look at me instead."
        mc "That's the best offer I've had all week."
        gf "It's the only offer you've had all week. But it's still the best."
    elif d5_track == "exhibitionism":
        gf "Phone rule. Phones in the dry bag until dinner."
        mc "That's very strict."
        gf "I told you. I have an idea. It needs your full attention."
    elif d5_track == "ntr_repaired":
        gf "It's a relief, isn't it. Nowhere to go and no one to answer to."
        mc "It's a relief."
    elif d5_track == "ntr_unresolved":
        "[girlfriend_name]'s thread showed her last message, 'Sorry.', sent in the dark the night before. I looked at it again, and put the phone away, and looked at it again."
    else:
        "The thread with [girlfriend_name] still showed my last reply: nothing. I looked at the little gray X and, for once, was glad of it."

    $ d5_nb_bag = format_choice("ch01_d5_bars_bag", "Put the phone in the dry bag. All day.")
    $ d5_nb_check = format_choice("ch01_d5_bars_check", "Keep it in my pocket. Just in case.")

    menu:
        "[d5_nb_bag]":
            $ apply_choice("ch01_d5_bars_bag")
            mc "Dry bag. All day."
            "I zipped the phone into the bag and handed it to Maya, who made a show of writing a receipt."
            maya "Phone custody. One honey jar, redeemable on landing."
            $ set_story_flag("ch01_d5_phone_in_bag")
            if d5_track == "love":
                gf "Look at you. A man with no distractions and a very patient girlfriend."
            elif d5_track == "exhibitionism":
                gf "Perfect. You'll need both hands."
                mc "For what?"
                gf "Water. Hydration. Several things."
        "[d5_nb_check]":
            $ apply_choice("ch01_d5_bars_check")
            mc "I'll keep it. In case."
            "I kept it in my pocket, where it buzzed with nothing, from time to time, like a ghost limb."
            if d5_track.startswith("ntr"):
                gf "Of course."
                "She said it lightly. It landed less lightly."
            else:
                gf "Okay. But when you look at it, I'm going to say something dramatic."

    $ set_story_flag("ch01_d5_scene_03_complete")
    jump ch01_day5_scene_04_snorkel


label ch01_day5_scene_04_snorkel:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_reef_surface
    with fade

    # AUDIO TODO: muffled underwater hush, a regulator-free breath, distant boat engine ticking.

    "Captain Ilario cut the engine over a reef the color of bruised sea glass and dropped the anchor with the air of a woman who had done this four hundred times."
    skipper "Snorkel. Two at a time. The boat stays within shouting distance. I do not shout."
    friend "I'll supervise."
    maya "[friend_name] is the lifeguard. He's wearing a hat."
    friend "It's a very official hat."

    "There were two masks left for the first pair, and four people with opinions."
    gf "[player_name]. First pair. Pick."

    if d5_track.startswith("ntr"):
        $ d5_sn_leia = format_choice("ch01_d5_snorkel_leia_first", ('Go in with ' + girlfriend_name + '.'))
        $ d5_sn_maya = format_choice("ch01_d5_snorkel_maya_first", ('Let Maya and ' + friend_name + ' go first.'))
        $ d5_sn_stay = format_day5_gate_choice("ch01_d5_ntr_snorkel_stay", "I'll stay on the boat. You go.", severity="soft", gate_label="D5-1")
        menu:
            "[d5_sn_leia]":
                $ apply_choice("ch01_d5_snorkel_leia_first")
                $ set_story_value("ch01_d5_snorkel_first", "leia")
                mc "I'll go with [girlfriend_name], if she'll have me."
                if d5_track == "ntr_confirmed":
                    gf "It's a very big ocean."
                    mc "I'll keep to my corner of it."
                    gf "...Fine. Corner."
                else:
                    gf "I'll have you."
            "[d5_sn_maya]":
                $ apply_choice("ch01_d5_snorkel_maya_first")
                $ set_story_value("ch01_d5_snorkel_first", "maya")
                mc "Maya and [friend_name] first. I'll watch the boat."
                maya "I'm going to need a minute to forgive that."
                gf "It's fine."
                "She said it the way I'd said it eleven times in two days, and I heard it for the first time."
            "[d5_sn_stay]":
                $ apply_choice("ch01_d5_ntr_snorkel_stay")
                $ set_story_value("ch01_d5_snorkel_first", "none")
                mc "I'll stay on the boat. You go."
                gf "You'll stay on the boat."
                mc "I'll be here."
                "[girlfriend_name] pulled her mask over her hair and went in without another word. Maya watched me for a second and went in after her."
    else:
        $ d5_sn_leia = format_choice("ch01_d5_snorkel_leia_first", ('Go in with ' + girlfriend_name + '.'))
        $ d5_sn_maya = format_choice("ch01_d5_snorkel_maya_first", ('Go in with Maya. ' + girlfriend_name + ' will have more fun with ' + friend_name + '.'))
        $ d5_sn_jul = format_choice("ch01_d5_snorkel_julian_first", ('Send ' + girlfriend_name + " and Maya. I'll hold the camera."))
        menu:
            "[d5_sn_leia]":
                $ apply_choice("ch01_d5_snorkel_leia_first")
                $ set_story_value("ch01_d5_snorkel_first", "leia")
                mc "[girlfriend_name]. Obviously."
                gf "Obviously. Good. I wasn't going to ask twice."
            "[d5_sn_maya]":
                $ apply_choice("ch01_d5_snorkel_maya_first")
                $ set_story_value("ch01_d5_snorkel_first", "maya")
                mc "Maya. [friend_name] takes [girlfriend_name]."
                maya "I'm honored. And terrified."
                friend "Why am I here?"
                gf "Because you're the lifeguard."
                friend "That doesn't mean I go in."
            "[d5_sn_jul]":
                $ apply_choice("ch01_d5_snorkel_julian_first")
                $ set_story_value("ch01_d5_snorkel_first", "camera")
                mc "I'll hold the camera. You two go."
                maya "He wants to be the documentarian."
                gf "Documentarians don't get wet."
                mc "That's the point."

    $ d5_first = get_story_value("ch01_d5_snorkel_first", "leia")
    "The water was warm for the first six inches and perfect after that."

    if d5_first == "leia":
        $ enter_cinematic_mode()
        scene cg ch01_d5_snorkel_surface
        with dissolve
        # CG TODO (artist): ch01_d5_snorkel_surface. Ryan POV, Ryan never in frame.
        "She surfaced a few feet from me, mask pushed up, hair slicked back, seawater on her lashes, laughing."
        gf "There's a fish down there with a face like [friend_name]."
        mc "That's cruel."
        gf "It was a compliment. It looked very responsible."
        $ exit_cinematic_mode()
        scene bg ch01_d5_reef_surface
        with dissolve
        gf "I lost my clip."
        mc "What?"
        gf "It came off when I dove. It's down there."
        "I dove twice. The second time I found it, wedged in a bright fan of coral, the hairclip winking like an unfair sort of treasure."
        "I came up with it. [girlfriend_name] kissed me in the water, salt and sunscreen, and then took it back to wear again, damp, immediately."
        gf "You are a better treasure hunter than a photographer."
        mc "That's not a very high bar."
        gf "It's a very high bar. I've seen your photos."
        $ set_story_flag("ch01_d5_clip_rescued_by_ryan")
    elif d5_first == "maya":
        "Maya drifted beside me, her snorkel clamped between her teeth, giving a thumbs up every four seconds like a diver in a safety video."
        "On the surface, afterward, she pushed her mask up and looked at the boat."
        maya "I need to tell you something, and I need you to let me say it badly."
        mc "Okay."
        maya "I like him. [friend_name]. I don't know what to do with it."
        mc "Have you tried telling him?"
        maya "I've tried telling him in a lot of ways. All of them were jokes."
        $ set_story_flag("ch01_d5_maya_confided_early")
        "While we talked, the hairclip drifted off [girlfriend_name]'s head on the far side of the boat. [friend_name], hatted and green, leaned over the rail and netted it with Captain Ilario's long-handled skimmer."
        friend "I've saved the clip."
        skipper "Fish do not wear jewelry. Please remind them."
        $ set_story_flag("ch01_d5_clip_rescued_by_julian")
    elif d5_first == "camera":
        "I stood on the swim platform with the camera and watched two women bob on the surface like very happy buoys."
        "Maya waved. [girlfriend_name] dove, came up, and held up a perfect, tiny starfish for the lens."
        gf "Photo."
        mc "Photo."
        "On the way back up the ladder, her hairclip came off in the water. [friend_name], hatted and green, leaned over the rail and netted it with Captain Ilario's long-handled skimmer."
        friend "I've saved the clip."
        skipper "Fish do not wear jewelry. Please remind them."
        $ set_story_flag("ch01_d5_clip_rescued_by_julian")
    else:
        "From the swim platform I watched [girlfriend_name] and Maya cut slow circles over the reef, like they had a lot to say and a lot of sea to say it in."
        "A hairclip floated up through the glitter, a small gold thing, and [friend_name] leaned over with the skimmer."
        friend "I've saved the clip."
        skipper "Fish do not wear jewelry. Please remind them."
        $ set_story_flag("ch01_d5_clip_rescued_by_julian")

    $ set_story_flag("ch01_d5_scene_04_complete")
    jump ch01_day5_scene_05_cove_lunch


label ch01_day5_scene_05_cove_lunch:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_style = get_story_value("ch01_d4_photo_style", "none")

    scene bg ch01_d5_cove_beach
    with fade

    # AUDIO TODO: quiet lapping, a cicada, the canvas of the boat's awning flapping once.

    "The cove was a perfect crescent of white sand, closed in by pale rocks and a lone fig tree that looked like it had no intention of being anywhere else."
    "Captain Ilario anchored in six feet of water, said one word, 'Lunch', and went back to the helm."
    "Lunch was a basket the chef Teodoro had packed: cold chicken, flatbread, olives, and a jar of honey with a note taped to the lid."
    maya "'For the bee enthusiast.' [friend_name]."
    friend "I want it known that I did not request that."
    maya "Teodoro's a poet."

    python:
        phone_add_message(
            "group", "maya",
            text="(sent hours ago, delivered now) Inés says be in the harbor by dawn if we want the good spots. I have no idea what that means and neither does she.",
            message_id="ch01_d5_queue_maya_ines",
            mark_unread=True, notify=True, notification_title="Maya",
        )
    "At the edge of the cove, for exactly four seconds, my phone found one bar of signal. It buzzed in my pocket like a captured insect."

    if get_story_value("ch01_d5_track") == "love":
        python:
            phone_add_message(
                "leia", "leia",
                text="I miss you. You're ten feet away. This is how bad it is.",
                message_id="ch01_d5_queue_leia_love",
                mark_unread=True, notify=True, notification_title=girlfriend_name,
            )
        "A second buzz: [girlfriend_name], sent from the other end of the beach, five minutes earlier. She was looking out at the water, very carefully, while I read it."
    elif get_story_value("ch01_d5_track") == "exhibitionism":
        python:
            phone_add_message(
                "leia", "leia",
                text="Phone away. Idea soon. You're welcome.",
                message_id="ch01_d5_queue_leia_exhib",
                mark_unread=True, notify=True, notification_title=girlfriend_name,
            )
        "A second buzz: [girlfriend_name], drafted somewhere in the middle of the sea. I turned the phone face down."
    elif get_story_value("ch01_d5_track") == "ntr_repaired":
        python:
            phone_add_message(
                "leia", "leia",
                text="(drafted at 6am, never sent until now) I'm going to tell you today. I'm scared. I'm still going to.",
                message_id="ch01_d5_queue_leia_ntr_repaired",
                mark_unread=True, notify=True, notification_title=girlfriend_name,
            )
        "A second buzz: a draft [girlfriend_name] had never sent. It had been sitting in her phone since six that morning."
    elif get_story_value("ch01_d5_track") == "ntr_unresolved":
        python:
            phone_add_message(
                "leia", "leia",
                text="I didn't mean 'sorry' to end it there. I didn't know how to say the rest.",
                message_id="ch01_d5_queue_leia_ntr_unresolved",
                mark_unread=True, notify=True, notification_title=girlfriend_name,
            )
        "A second buzz, on [girlfriend_name]'s thread, under the single word she'd sent the night before."
    else:
        python:
            phone_add_message(
                "julian", "julian",
                text="Stern after lunch. Just you and me. Not a referee. Just a friend with a hat.",
                message_id="ch01_d5_queue_julian_ntr_confirmed",
                mark_unread=True, notify=True, notification_title=friend_name,
            )
        "A second buzz, from [friend_name], from eleven feet away. He was studying the fig tree very hard."

    "Then the bar went away, and the bee arrived."

    # Honey / bee gag: callback to Day 2 bee and Julian's fear.
    "It was a regular, unremarkable honeybee. It landed on the lid of the honey jar as if it had been summoned."
    friend "Nobody. Move."
    maya "It's a bee."
    friend "It is a bee, Maya. It is a bee on a jar of honey on a beach in a cove on a boat."
    maya "You're holding the chicken."
    friend "I'm holding the chicken extremely still."

    $ d5_be_calm = format_choice("ch01_d5_bee_calm", ('Calmly lift the jar and carry the bee away from ' + friend_name + '.'))
    $ d5_be_film = format_choice("ch01_d5_bee_film", "Hold up the camera. 'This is going in the album.'")

    menu:
        "[d5_be_calm]":
            $ apply_choice("ch01_d5_bee_calm")
            mc "Everybody stay exactly where you are."
            "I picked up the jar very gently and walked it down to the waterline. The bee came with it, unimpressed, and eventually remembered it had a life."
            friend "Photographer of the year. And bee wrangler."
            maya "I'm adding it to your tab."
            $ set_story_flag("ch01_d5_bee_rescued")
        "[d5_be_film]":
            $ apply_choice("ch01_d5_bee_film")
            mc "Hold that face."
            $ enter_cinematic_mode()
            scene cg ch01_d5_cove_lunch_bee
            with dissolve
            # CG TODO (artist): ch01_d5_cove_lunch_bee. Ryan POV, Ryan never in frame. Comic.
            "[friend_name] froze with a drumstick in one fist and a bee on the lid of the honey jar in front of him. Maya, off to the side, was losing her whole self to laughter."
            $ exit_cinematic_mode()
            scene bg ch01_d5_cove_beach
            with dissolve
            friend "I want it on record that I am not okay."
            maya "It's on the record. It's in the photo. It's evidence."
            gf "[player_name]. Put the camera down and help him."
            "I did, eventually, and the bee left on its own, which was either mercy or contempt."

    "Maya took the camera out of my hands before I'd set it down."
    maya "Group photo. [friend_name], stand next to [girlfriend_name]. [girlfriend_name], stand next to the light. [player_name], you take it, you're the camera."
    friend "I'm still recovering from the bee."
    maya "Everyone's recovering from something. Look pleased."

    $ enter_cinematic_mode()
    scene cg ch01_d5_photo_three
    with dissolve
    # CG TODO (artist): ch01_d5_photo_three. Ryan POV, Ryan never in frame (he is holding the camera).
    "Click."
    $ exit_cinematic_mode()
    scene bg ch01_d5_cove_beach
    with dissolve

    gf "I'm being very beautiful in that one."
    friend "I look like I'm hostage to a bee."
    maya "Because you are."

    if d5_style == "candid":
        gf "You've still got the knack for catching me off guard. Do it again later."
    elif d5_style == "posed":
        gf "Next time, I'll bring the sunglasses and the eyebrow."
    elif d5_style == "swap":
        gf "And next time, I'm taking the first one."
    elif d5_style == "skipped":
        gf "That's one photo of me this week that you took on purpose."
        mc "I deserve that."
        gf "A little. But it's a good one."

    $ d5_ps_share = format_choice("ch01_d5_photo_share_group", "Post it to the Trip Group when I get signal.")
    $ d5_ps_keep = format_choice("ch01_d5_photo_keep_album", "Keep it in my own album for now.")

    menu:
        "[d5_ps_share]":
            $ apply_choice("ch01_d5_photo_share_group")
            $ set_story_value("ch01_d5_photo_group", "shared")
            mc "I'll post it as soon as we have signal."
            maya "He's a team player."
            python:
                phone_add_message(
                    "group", "maya",
                    text="Photo from the cove. I look like a woman who has never lost a negotiation.",
                    message_id="ch01_d5_group_photo_three",
                    attachment_id="ch01_d5_photo_three",
                    attachment_label=('The three of them at the cove, ' + friend_name + ' pale, Maya triumphant, ' + girlfriend_name + ' glowing'),
                    mark_unread=True, notify=False,
                )
        "[d5_ps_keep]":
            $ apply_choice("ch01_d5_photo_keep_album")
            $ set_story_value("ch01_d5_photo_group", "kept")
            mc "I'm keeping this one for myself."
            gf "He's a collector."
            maya "He's a thief."
            python:
                phone_add_message(
                    "leia", "leia",
                    text=('Send me the one with all three of us. I want to remember ' + friend_name + "'s face."),
                    message_id="ch01_d5_leia_photo_three",
                    attachment_id="ch01_d5_photo_three",
                    attachment_label=('The three of them at the cove, ' + friend_name + ' pale, Maya triumphant, ' + girlfriend_name + ' glowing'),
                    mark_unread=True, notify=False,
                )

    $ set_story_flag("ch01_d5_scene_05_complete")
    jump ch01_day5_scene_06_deck_talk


label ch01_day5_scene_06_deck_talk:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_foredeck
    with fade

    "After lunch, the heat turned heavy and slow. I found the one shaded spot on the foredeck, under a folded sail the color of old paper, and lay down with a hat over my face."
    "I'd meant to nap. I'd meant a lot of things."
    "Two sets of bare feet came up the side deck, and settled a few feet away, on the other side of the sail."
    "They thought I was asleep. I might have been, if I'd been a better liar."

    # Eavesdropping choice: complicity with a visible cost.
    $ d5_ev_announce = format_choice("ch01_d5_eaves_announce", "Sit up and say 'Hello. I'm here.'")
    $ d5_ev_listen = format_choice("ch01_d5_eaves_listen", "Lie still. Listen.")

    menu:
        "[d5_ev_announce]":
            $ apply_choice("ch01_d5_eaves_announce")
            "I tipped the hat back and sat up."
            mc "Hello. I'm here. I'm not asleep."
            maya "Of course you're not."
            gf "We were about to talk about you."
            mc "That's what I was afraid of."
            gf "In a good way. Mostly. Go to the stern. [friend_name] wants you anyway."
            maya "Leave us. Girls' meeting. There's a tab."
            "I left them to it, and the folded sail swallowed their voices before I'd reached the cockpit."
            $ set_story_flag("ch01_d5_eaves_announced")
        "[d5_ev_listen]":
            $ apply_choice("ch01_d5_eaves_listen")
            $ set_story_flag("ch01_d5_eaves_listened")
            "I stayed exactly where I was. I even breathed slower, which probably gave me away on its own."

            if d5_track == "love":
                maya "So. [player_name]. You're being very brave."
                gf "I'm being brave. I'm terrified. I'm also happy, which feels like it shouldn't be allowed at the same time."
                maya "It's allowed. That's most of it."
                gf "I keep stepping a little further. Every day, a little further. And the thing I keep noticing is that I'm not stepping away from him. I'm stepping toward."
                maya "That's the difference."
                gf "That's the entire difference."
            elif d5_track == "exhibitionism":
                maya "Okay. Explain it to me like I'm an idiot with a lot of questions."
                gf "I like being looked at. I didn't know. I thought I'd hate it. And then [player_name] looked, and I didn't."
                maya "And now?"
                gf "Now I want to see how far I can go and still be me. That's the whole experiment. And I keep the dial. Always. Whatever he says, whatever anyone says, I keep the dial."
                maya "That's the best thing I've heard you say all week."
                gf "It's also very frightening."
                maya "It's the only way it's fun."
            elif d5_track == "ntr_repaired":
                gf "I'm going to tell him today."
                maya "I know."
                gf "I'm going to tell him the part I haven't. And I think I might throw up. Is that normal?"
                maya "[friend_name] threw up this morning. We're on a boat. It's practically a theme."
                gf "I'm serious."
                maya "I know you're serious. So tell him slowly. Tell him the order it happened in. Don't tell him the ending first."
            elif d5_track == "ntr_unresolved":
                gf "He's trying. I can see him trying. It's the saddest thing."
                maya "Why is it sad?"
                gf "Because I know that if I tell him the rest, he might stop trying. Or he might try harder. And I don't know which one I'd rather."
                maya "You should tell him anyway."
                gf "I know. I don't have the first sentence."
                maya "Then start with the second."
            else:
                gf "He said 'I'm fine' again."
                maya "I heard."
                gf "He's said it so many times I'm not sure if it's an answer or an apology."
                maya "Probably both."
                gf "I told you what happened. At the club. The upstairs. I told you the order."
                maya "And?"
                gf "And I still can't say it to him."
                "I lay absolutely still, with a hat on my face and a different kind of weight on my chest."
                $ set_story_flag("ch01_d5_overheard_club")

            if d5_track in ("ntr_unresolved", "ntr_confirmed"):
                "I heard enough to know something had happened that [girlfriend_name] hadn't said to me. I didn't hear what. That was the cruel part: she was telling Maya the shape of it, and I was getting only the weather."
            "A moment later, the hat was lifted off my face by a finger."
            gf "[player_name]. I know you're awake."
            mc "I'm not."
            gf "Your foot's tapping."
            if d5_track.startswith("ntr"):
                gf "That was mine to tell. I'd have told you."
                "She didn't shout. She sounded exactly like someone who's tired of explaining what privacy is."
                $ set_story_flag("ch01_d5_privacy_breach")
            else:
                gf "I could tell from the breathing. You're the worst fake sleeper I've ever met."
                maya "He's like a shy dolphin."
                gf "Come on. Out. We were about to tell you anyway."

    $ set_story_flag("ch01_d5_scene_06_complete")
    jump ch01_day5_scene_07_stern


label ch01_day5_scene_07_stern:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_stern
    with fade

    "[friend_name] was sitting on the transom with his sunglasses restored to office, watching the wake as if it owed him money."
    "I sat down next to him. He didn't look up."

    if d5_track == "love":
        friend "I've never seen anyone look as happy as you two."
        mc "It's the boat."
        friend "It's not the boat. I've known you eight years. You've never once looked this relaxed on a boat."
        friend "I just wanted to say. I'm glad. And I'm a little bit jealous."
        mc "You've got Maya."
        friend "I've got a tab."
    elif d5_track == "exhibitionism":
        friend "I want you to know something."
        mc "That sounds ominous."
        friend "If the afternoon goes the way I think it's going, I'm going to be looking at the horizon. The whole time. Like it owes me money."
        mc "You don't have to."
        friend "I do. You're my friend. I'm not going to be the guy who looked."
        mc "That's very noble."
        friend "It's also very boring. But it's mine."
    elif d5_track == "ntr_repaired":
        friend "I know she's telling you something today."
        mc "How do you know?"
        friend "Maya told me not to say. So I'm saying it."
        mc "Great."
        friend "I'm not going to ask what. I'm just going to be on the boat. Within shouting distance. I don't shout."
        mc "That's a captain line."
        friend "I'm learning."
    elif d5_track == "ntr_unresolved":
        friend "She told Maya something."
        mc "I know."
        friend "Maya told me she did. She didn't tell me what. I don't want to know what. If I knew, I'd have to decide whether to tell you. And I don't want to be the guy who decides."
        mc "Thank you."
        friend "I'm not doing it for you. I'm doing it for me. I like having nothing to confess."
    else:
        friend "I need to say a thing, and I need you not to hate me."
        mc "No promises."
        friend "I'm not going to take sides. I'm not going to be your excuse, and I'm not going to be your audience. If you want me to tell you how bad she is, I won't. If you want me to tell you it's your fault, I won't do that either."
        mc "What will you do?"
        friend "Sit here. Be bad at silence. Ask you if you want a granola bar."

    "He looked, for the first time, straight at me."
    friend "Loyalty costs more than I thought it would. It cost me a very nice afternoon of not caring."
    friend "I'm paying it. You'd pay it for me."

    $ d5_st_thanks = format_choice("ch01_d5_stern_thanks", "Say thank you. Mean it.")
    $ d5_st_joke = format_choice("ch01_d5_stern_joke", "Tell him he's growing a spine and it looks good on him.")
    if d5_track in ("ntr_unresolved", "ntr_confirmed"):
        $ d5_st_push = format_choice("ch01_d5_stern_push", "Ask him to just tell me what Maya said.")
    else:
        $ d5_st_push = format_choice("ch01_d5_stern_push", "Ask him if he and Maya have talked.")

    menu:
        "[d5_st_thanks]":
            $ apply_choice("ch01_d5_stern_thanks")
            mc "Thank you."
            friend "You're welcome."
            mc "I mean it."
            friend "I know. It's embarrassing. Don't do it again."
            $ set_story_flag("ch01_d5_julian_thanked")
        "[d5_st_joke]":
            $ apply_choice("ch01_d5_stern_joke")
            mc "You're growing a spine."
            friend "It's still very small."
            mc "It looks good on you."
            friend "I've been in the sun too long."
        "[d5_st_push]":
            $ apply_choice("ch01_d5_stern_push")
            if d5_track in ("ntr_unresolved", "ntr_confirmed"):
                mc "Just tell me what Maya said."
                friend "No."
                mc "[friend_name]."
                friend "No. It's [girlfriend_name]'s. It's hers to say. If I told you, I'd be a very small kind of friend."
                "He said it quietly, and I knew he'd decided long before I asked."
            else:
                mc "Have you and Maya talked?"
                friend "We have talked a lot. About everything but that."
                mc "Have you tried?"
                friend "I've tried in a lot of ways. All of them were bits."
                "That sounded familiar, and I didn't say why."

    $ set_story_flag("ch01_d5_scene_07_complete")
    jump ch01_day5_scene_08_cove_afternoon


label ch01_day5_scene_08_cove_afternoon:

    # Dispatcher. Track was stored at the start of the day and never recomputed.
    $ d5_track = get_story_value("ch01_d5_track", "love")

    if d5_track == "love":
        jump ch01_day5_scene_08_love_cove
    elif d5_track == "exhibitionism":
        jump ch01_day5_scene_08_exhib_cove
    elif d5_track == "ntr_repaired":
        jump ch01_day5_scene_08_ntr_repaired
    else:
        jump ch01_day5_scene_08_ntr_apart


# ---------------------------------------------------------------------------
# Scene 8 (route beats). Love / Exhibition / NTR repaired / NTR apart.
# ---------------------------------------------------------------------------

label ch01_day5_scene_08_love_cove:

    scene bg ch01_d5_cove_rock
    with fade

    "[girlfriend_name] led me around the fig tree and over a spine of warm rock to a second cove no bigger than a living room, a thumbprint of sand and glass-clear water."
    gf "Maya says it's called 'Nobody's'. She says she's never seen anyone in it."
    mc "That's a weirdly useful name."
    gf "It's a very good name. I'm going to say it to myself in the dark."
    "She dropped her tote on the rock and pulled the pale rope out of the top, coiling it over one wrist like a very small lasso."
    gf "I told you I had a plan."
    mc "I thought the plan was the rope."
    gf "The rope is the prop. The plan is that we swim, and then you tell me something you've never told anyone. And I tell you one. And then, if we survive it, I teach you a knot."
    mc "That's a lot of plan."
    gf "It's a very small plan. It's the biggest thing I've ever organized."

    $ d5_lv_close = format_choice("ch01_d5_love_swim_close", "Swim out together. Slowly.")
    $ d5_lv_race = format_choice("ch01_d5_love_swim_race", "Race her to the rock.")

    menu:
        "[d5_lv_close]":
            $ apply_choice("ch01_d5_love_swim_close")
            mc "Together. Slowly."
            gf "That's the nicest word anyone's said to me today."
            $ enter_cinematic_mode()
            scene cg ch01_d5_love_cove_swim
            with dissolve
            # CG TODO (artist): ch01_d5_love_cove_swim. Ryan POV, Ryan never in frame.
            "We treaded water in the clear green and she came close, and then closer, until her forehead was tipped toward mine and her hands rested on my shoulders."
            gf "Hi."
            mc "Hi."
            gf "I like this version of us. It's quieter."
            $ exit_cinematic_mode()
            scene bg ch01_d5_cove_rock
            with dissolve
        "[d5_lv_race]":
            $ apply_choice("ch01_d5_love_swim_race")
            mc "Race you to the rock."
            gf "You're going to lose."
            mc "I'm going to lose very hard."
            "She won by a body length and a lot of splashing. At the rock she pulled herself up, rolled over and held out her hand."
            gf "Winner's right. You owe me a secret."
            mc "That's not how races work."
            gf "That's exactly how my races work."

    "We pulled ourselves out onto the rock, wet and warm, and she sat with her knees drawn up, the hairclip drying in her hair."
    gf "I'll go first."
    gf "The night of the first dream. The one you told me about. After you fell asleep, I stood in the hallway and watched you for ten minutes before I came to bed."
    mc "Why?"
    gf "I wasn't scared. I was memorizing. I wanted to know what you looked like when you weren't performing being okay."
    gf "That's mine. That's the one I've never told anyone."
    "She looked at the horizon, not at me, and let out one long breath."
    gf "Your turn."

    $ d5_lv_dream = format_choice("ch01_d5_love_secret_dream", "Tell her about the curtain dream. The part I didn't say.")
    $ d5_lv_mirror = format_choice("ch01_d5_love_secret_mirror", "Tell her I practiced asking her out in the bathroom mirror.")
    $ d5_lv_owe = format_choice("ch01_d5_love_secret_owe", "Say 'I owe you one' and keep it for later.")

    menu:
        "[d5_lv_dream]":
            $ apply_choice("ch01_d5_love_secret_dream")
            $ set_story_value("ch01_d5_secret_traded", "dream")
            mc "The curtain dream. I told you there was a curtain. I didn't tell you that you were on the other side of it, looking back at me, and you weren't upset."
            mc "You were curious. And I woke up scared that I liked it."
            "I braced for something. She didn't give me anything to brace against."
            gf "Dreams aren't evidence. They're weather. You can tell me the weather any day you want."
            gf "And for what it's worth, I'm still on this side of the curtain. Where you can see me."
            "She moved her hand to cover mine, wet, warm, certain."
        "[d5_lv_mirror]":
            $ apply_choice("ch01_d5_love_secret_mirror")
            $ set_story_value("ch01_d5_secret_traded", "mirror")
            mc "The bathroom mirror at my old place. I practiced asking you out for three weeks. I had three versions. The funny one, the serious one, and the one where I just stood there."
            gf "Which one did you use?"
            mc "The one where I just stood there."
            gf "That's the one that worked."
            "She laughed, and then stopped, and then looked at me with a brand-new kind of tenderness."
        "[d5_lv_owe]":
            $ apply_choice("ch01_d5_love_secret_owe")
            $ set_story_value("ch01_d5_secret_traded", "owed")
            mc "I owe you one. I'm not ready to pay it out here."
            gf "Interest accrues."
            mc "At what rate?"
            gf "Rope-based. I'll be strict."
            "She said it lightly. She also didn't look away, and that told me she'd decided I was worth waiting for."

    "She took the pale rope from her wrist and held it up between us."
    gf "Now the rope. You get a knot when you've paid. I get a knot when I have. It's tradition."
    mc "Whose tradition?"
    gf "Mine. As of about eight this morning."
    "We spent the next twenty minutes tying and untying a small, ridiculous knot on the rock, and I discovered I was better at it than I'd feared. She put the finished loop on the stone between us like a prize."
    gf "Keep that. We'll use it tonight."

    $ enter_cinematic_mode()
    scene cg ch01_d5_love_cove_secret
    with dissolve
    # CG TODO (artist): ch01_d5_love_cove_secret. Ryan POV, Ryan never in frame.
    "Before we swam back, she asked me to take one photo. Not posed. The one where she was just listening."
    "She sat on the rock with her knees up and her chin on her arm, sun on her wet hair, looking up with the soft, whole expression of someone who has told the truth and is waiting to be held in it."
    $ exit_cinematic_mode()

    python:
        phone_add_message(
            "leia", "leia",
            text="For the box. The one where I'm listening to you. Don't show Maya.",
            message_id="ch01_d5_leia_photo_love_cove",
            attachment_id="ch01_d5_photo_love_cove",
            attachment_label=(girlfriend_name + " at Nobody's Cove, listening"),
            mark_unread=True, notify=False,
        )
    $ set_story_flag("ch01_d5_love_cove_done")
    $ set_story_value("ch01_d5_exposure_step", "none")
    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset


label ch01_day5_scene_08_exhib_cove:

    scene bg ch01_d5_cove_rock
    with fade

    $ d5_sw = get_story_value("ch01_d5_swim_outfit_id", "pool_conservative")
    $ d5_watch_d4 = has_story_flag("ch01_d4_exhib_ryan_likes_watching")

    "[girlfriend_name] took us all around the fig tree to the second cove, the one behind the rocks. The boat sat just out of sight. Captain Ilario was a pair of sunglasses in a distant cockpit, reading a paperback."
    maya "This is a very good cove. It's got privacy. It's got ambiance. It's got [friend_name]."
    friend "I'm standing very still in the sun. I've decided it's a personality."
    "[girlfriend_name] dropped her bag on a flat rock, turned to the three of us, and put her hands on her hips like a woman about to announce a merger."
    gf "Okay. I have a thing. It's not a big thing. It's a medium thing."
    gf "I want to try something today, and I want to do it with the three people on earth who'd make it funny instead of weird."
    maya "I'm flattered. And on notice."
    gf "I'm going to take my top off. Maybe. If I decide. On my own. Not because anyone told me to."
    friend "I'll be looking at the horizon."
    maya "[friend_name] has named the horizon Gerald."
    friend "It's a very reliable horizon."
    gf "And Maya, you do whatever you want. Whatever makes you comfortable."
    maya "My arrangement with my sunburn is very complicated and I'm not renegotiating it today. I'm keeping mine on. But I'll be your biggest fan from behind a book."
    gf "That's all I need."
    "[girlfriend_name] turned to me, and her voice dropped for me alone."
    gf "I'm doing this because I want to know what I can do and still be me. That's all. That's the whole experiment."
    gf "And I'm telling you because you're the one I'm doing it with."

    if d5_watch_d4:
        gf "And I haven't forgotten what you said about liking to watch. I'm the one who decides how much you get."
        mc "That seems fair."
        gf "It's extremely fair. It's practically law."

    $ d5_ex_stay = format_choice("ch01_d5_exhib_stay", "Stay beside her. She sets the pace.")
    $ d5_ex_watch = format_choice("ch01_d5_exhib_watching", "Tell her I like watching her do this. With me watching.")
    $ d5_ex_priv = format_choice("ch01_d5_exhib_private", "Take her hand. 'Just us. Come with me.'")

    menu:
        "[d5_ex_stay]":
            $ apply_choice("ch01_d5_exhib_stay")
            $ set_story_value("ch01_d5_exhib_variant", "shared_step")
            mc "Your pace. I'm right here."
            gf "Thank you for not saying anything clever."
            jump ch01_day5_exhib_step

        "[d5_ex_watch]":
            $ apply_choice("ch01_d5_exhib_watching")
            $ set_story_value("ch01_d5_exhib_variant", "ryan_likes_watching")
            $ set_story_flag("ch01_d5_exhib_ryan_likes_watching")
            mc "I like watching you do this. Especially when you're the one deciding."
            gf "You really do."
            mc "Not instead of you. With you. Watching."
            gf "I'm going to hold you to that exact sentence."
            "She sat down on the rock with her back to the water and took a very long breath."
            gf "How far should I go?"

            $ d5_ex_hercall = format_choice("ch01_d5_exhib_her_call", "Your call. However far you want to go.")
            $ d5_ex_tease = format_choice("ch01_d5_exhib_tease_then_me", "Tease them, then come back to me.")

            menu:
                "[d5_ex_hercall]":
                    $ apply_choice("ch01_d5_exhib_her_call")
                    mc "Your call. However far you want to go."
                    gf "I'm taking my time."
                    $ set_story_value("ch01_d5_exhib_framing", "her_call")
                "[d5_ex_tease]":
                    $ apply_choice("ch01_d5_exhib_tease_then_me")
                    mc "Tease them. Then come back to me."
                    gf "That's an extremely specific instruction."
                    mc "I'm a specific man."
                    $ set_story_value("ch01_d5_exhib_framing", "tease_then_me")
            jump ch01_day5_exhib_step

        "[d5_ex_priv]":
            $ apply_choice("ch01_d5_exhib_private")
            $ set_story_value("ch01_d5_exhib_variant", "opt_out_private")
            $ set_story_value("ch01_d5_end_route_pending", "love")
            mc "Just us. Come on."
            "Her whole body unclenched. She looked back at Maya and [friend_name]."
            gf "I'm borrowing him. Back in an hour."
            maya "Billable."
            friend "Gerald and I will hold the fort."
            "She led me over a spine of warm rock to a second, smaller cove, no bigger than a living room, with nobody in it but the water."
            gf "I didn't stop wanting it. I wanted it to be only us today."
            mc "Then it's only us."
            gf "I'll tell you when I want the window back."

            $ enter_cinematic_mode()
            scene cg ch01_d5_love_cove_swim
            with dissolve
            # CG TODO (artist): ch01_d5_love_cove_swim. Ryan POV, Ryan never in frame. Reused for the private opt-out.
            "We swam out, slowly, and treaded water, and she put her forehead against mine and kept it there, and neither of us said anything for a long time."
            $ exit_cinematic_mode()
            scene bg ch01_d5_cove_rock
            with dissolve
            "Later, on the warm rock, she asked for one photo. Not posed. The one where she was just happy."
            python:
                phone_add_message(
                    "leia", "leia",
                    text="For the box. The one where I'm happy and nobody's watching.",
                    message_id="ch01_d5_leia_photo_love_cove_optout",
                    attachment_id="ch01_d5_photo_love_cove",
                    attachment_label=(girlfriend_name + " at Nobody's Cove, happy"),
                    mark_unread=True, notify=False,
                )
            $ set_story_flag("ch01_d5_scene_08_complete")
            jump ch01_day5_scene_09_sunset


label ch01_day5_exhib_step:

    # Leia decides how far to go. Both outcomes are a positive step. Her own Exhibitionism
    # (and the Day Four step she already took) sets how far. Shown in Full / Developer.
    python:
        d5_ex_now = partner_stats["exhibitionism"]
        d5_ex_prev = get_story_value("ch01_d4_exposure_step", "none")
        d5_ex_call = ch01_d5_leia_call_for(d5_ex_now, d5_ex_prev)
        set_story_value("ch01_d5_leia_call", d5_ex_call)
        d5_ex_variant = get_story_value("ch01_d5_exhib_variant", "shared_step")
        d5_ex_framing = get_story_value("ch01_d5_exhib_framing", "own_pace")

    if current_choice_mode() == "developer":
        centered "[girlfriend_name!u]'S CALL: Exhibitionism [d5_ex_now] / [D5_COMFORTABLE_MIN] (Day 4 step: [d5_ex_prev]) -> [d5_ex_call]"
    elif current_choice_mode() == "full":
        centered "[girlfriend_name] decides how far she goes. Comfortable needs Exhibitionism [D5_COMFORTABLE_MIN] (or [D5_COMFORTABLE_MIN_AFTER_BRIEF] after Day Four's brief step). Current: [d5_ex_now]."
    elif current_choice_mode() == "insight":
        centered "[girlfriend_name] decides how far she goes, based on her own confidence."

    if d5_ex_variant == "ryan_likes_watching":
        $ enter_cinematic_mode()
        scene cg ch01_d5_exhib_cove_watching
        with dissolve
        # CG TODO (artist): ch01_d5_exhib_cove_watching. Ryan POV, Ryan never in frame. Sub-variant 'Ryan likes watching'. Covered.
        "I stood just behind her on the rock. Over her shoulder, far down the cove, Maya had propped a paperback in front of her face like a medieval screen, and [friend_name] was staring at Gerald."
        "I watched [girlfriend_name] decide."
        $ exit_cinematic_mode()
        scene bg ch01_d5_cove_rock
        with dissolve

    if d5_ex_call == "ties_loosened":
        $ enter_cinematic_mode()
        scene cg ch01_d5_exhib_cove_01
        with dissolve
        # CG TODO (artist): ch01_d5_exhib_cove_01. Ryan POV, Ryan never in frame. COVERED / implied.
        "[girlfriend_name] lay down on her front on the warm rock. She reached behind her neck, and then behind her back, and undid the ties, one slow loop at a time."
        "She turned her head and looked straight at me, her swimsuit loose against her back and her arms folded under her chin."
        gf "That's the bit I'm comfortable with today."
        gf "I wanted to see if I could be this undone and still be me."
        "She laughed, delighted at her own nerve, and rested her cheek on her arm."
        $ exit_cinematic_mode()
        $ set_story_value("ch01_d5_exposure_step", "ties_loosened")
        $ set_story_flag("ch01_d5_exhib_tease_done")
    else:
        $ enter_cinematic_mode()
        scene cg ch01_d5_exhib_cove_02
        with dissolve
        # CG TODO (artist): ch01_d5_exhib_cove_02. Ryan POV, Ryan never in frame. COMFORTABLE and IMPLIED: cropped at the collarbone, not anatomy as subject.
        "[girlfriend_name] stood, took a long breath, and slipped her top over her head, folding it neatly on the rock like it was a very small flag."
        "She sat back down in the sun with her arms loosely crossed and her face tipped up, eyes on me and not on anyone else, laughing at herself in quiet disbelief."
        gf "Oh. Oh, that's the sun."
        gf "I thought it would be terrifying. It's just warm. It's just me, being warm."
        "Down the cove, a paperback rose a little higher. Gerald the horizon received [friend_name]'s full and unwavering attention."
        $ exit_cinematic_mode()
        $ set_story_value("ch01_d5_exposure_step", "comfortable")
        $ set_story_flag("ch01_d5_exhib_comfortable_done")

    scene bg ch01_d5_cove_rock
    with dissolve

    if d5_ex_variant == "ryan_likes_watching":
        gf "You liked that I looked at you the whole time."
        mc "I liked that you were the one deciding."
        gf "Good answer."
        gf "If it stops being fun for me, I'll say so. Loudly. In front of [friend_name]."
        friend "I'd be able to hear that from Gerald."
        if d5_ex_framing == "tease_then_me":
            gf "And I came back to you."
            mc "You did."
            gf "That was the best part."
    else:
        gf "Okay. I'm going to need a minute, a glass of water and a second personality."
        maya "I'll bill you for the personality."
        gf "You're welcome to try."

    "Maya, from her book, called out that she was proud of her. [friend_name] said, to Gerald, that he was too."

    # Private photo: Leia owns the frame. The phone system carries the result.
    gf "One photo. Only you get it. Your call on the frame."
    $ d5_pp_face = format_choice("ch01_d5_photo_private_face", "Her face. Just her face, laughing.")
    $ d5_pp_moment = format_choice("ch01_d5_photo_private_moment", "The moment, cropped at the shoulders. She decides what stays.")
    $ d5_pp_none = format_choice("ch01_d5_photo_private_none", "No photo. I'll remember.")

    menu:
        "[d5_pp_face]":
            $ apply_choice("ch01_d5_photo_private_face")
            $ set_story_value("ch01_d5_private_photo", "face")
            mc "Your face. Just that."
            gf "That's the one that gets me."
            python:
                phone_add_message(
                    "leia", "leia",
                    text="Just for you. Don't ever let Maya see my face this honest.",
                    message_id="ch01_d5_leia_photo_private_face",
                    attachment_id="ch01_d5_photo_private",
                    attachment_label=(girlfriend_name + ' at the cove, laughing, face only'),
                    mark_unread=True, notify=False,
                )
        "[d5_pp_moment]":
            $ apply_choice("ch01_d5_photo_private_moment")
            $ set_story_value("ch01_d5_private_photo", "moment")
            mc "The moment. You decide how much of it stays in."
            gf "Good answer. I'll crop it myself."
            python:
                phone_add_message(
                    "leia", "leia",
                    text="Cropped by me. Yours alone. If it ever gets out I'll know exactly who to haunt.",
                    message_id="ch01_d5_leia_photo_private_moment",
                    attachment_id="ch01_d5_photo_private",
                    attachment_label=(girlfriend_name + ' at the cove, cropped at the shoulders, her call'),
                    mark_unread=True, notify=False,
                )
        "[d5_pp_none]":
            $ apply_choice("ch01_d5_photo_private_none")
            $ set_story_value("ch01_d5_private_photo", "none")
            mc "No photo. I'll remember."
            gf "That might be the most romantic thing you've ever said in swimwear."

    $ set_story_value("ch01_d5_end_route_pending", "exhibitionism")
    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset


label ch01_day5_scene_08_ntr_repaired:

    scene bg ch01_d5_cove_rock
    with fade

    "After the stern, [girlfriend_name] found me at the edge of the cove with the rope still coiled in her bag, unused."
    gf "Come with me."
    "She led me past the fig tree and over a spine of warm rock to the second cove, a thumbprint of sand and glass-clear water with nobody in it but the light."
    gf "This is where I'm going to say it."
    mc "Okay."
    gf "I want you to sit. And I want you to keep your hands where I can see them. Not because you'll do anything. Because I'll look at them when I can't look at you."

    $ enter_cinematic_mode()
    scene cg ch01_d5_ntr_cove_talk
    with dissolve
    # CG TODO (artist): ch01_d5_ntr_cove_talk. Ryan POV, Ryan never in frame. Quiet. No third person.
    "She sat on the rock with her knees drawn up and the hairclip open in both hands, turning it over like a very small clock."
    $ exit_cinematic_mode()
    scene bg ch01_d5_cove_rock
    with dissolve

    call ch01_day5_club_disclosure
    $ set_story_value("ch01_d5_disclosure_when", "cove_afternoon")
    jump ch01_day5_ntr_react_menu


label ch01_day5_scene_08_ntr_apart:

    $ d5_track = get_story_value("ch01_d5_track", "ntr_unresolved")

    scene bg ch01_d5_cove_beach
    with fade

    "[girlfriend_name] spent the afternoon with Maya, the two of them out on the swim platform with their feet in the water, heads together, a little pool of low voices in the big blue."
    "I stayed on the sand with the camera and nothing to point it at."

    if d5_track == "ntr_unresolved":
        "Twice, [girlfriend_name] looked back across the water. Twice, I raised a hand. Neither time did either of us know what to do with the distance."
        "[friend_name] sat down next to me with two granola bars and offered one without a word."
        friend "It's not a speech. It's a granola bar."
        mc "Thanks."
        friend "She's going to need you to ask. Not demand. Ask."
        mc "Did Maya say that?"
        friend "Maya says a lot of things. That one I invented."
    else:
        "[friend_name] lasted forty minutes in the sun before he came to sit by me with his hat in his hands."
        friend "I'm not a good friend for this. But I'm a loud friend. Do you want me to be loud?"
        mc "No."
        friend "Good. Because I'd be bad at it."
        "He ate a granola bar in a very supportive silence."
        "Later, Maya waded ashore alone, dripping, and sat down on my other side, closer than she usually would."
        maya "I'm going to say one thing and then I'm going to go back in the water."
        maya "She won't knock twice, [player_name]. She's knocked more than twice already. You've said 'I'm fine' to her like a locked door."
        mc "I know."
        maya "Do you? Because I've never seen two people stand so politely on either side of a window."
        maya "Sunset. The stern. She'll be there. Go and ask her properly, or go and don't, but don't go and say 'fine'."
        "She stood, shook out her hair, and left a small, salty puddle where she'd been."

    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset


# ---------------------------------------------------------------------------
# Shared NTR beats: club disclosure (Leia tells it in order) and Ryan's reaction.
# Non-explicit, told in her own words. The dream is not evidence: Ryan's nightmares
# had the details wrong, and Leia's real account is smaller and human sized.
# ---------------------------------------------------------------------------

label ch01_day5_club_disclosure:

    gf "I'm going to tell you in the order it happened. I need you to let me get to the end."
    gf "You went to the bar for [friend_name]'s surprise. I stayed on the sofa with them. They were nice. Not safe nice. Just regular nice."
    gf "One of them asked if I wanted to see the terrace upstairs. I said yes. I told myself it was for the view."
    gf "Upstairs there was a low table, a view and two of them. They didn't touch me. They asked me questions."
    gf "Do you know how long it's been since someone asked me what I wanted, and actually wanted the answer?"
    gf "I said I'd never been looked at like that. He said, 'Like what?' I said, 'Like I'm the only person in the room.'"
    gf "I knew that was the sentence. I knew while I was saying it."
    gf "He kissed me. I let him. It lasted about four seconds, and I kept my hands in my lap the whole time like I was in a waiting room."
    gf "And then I stopped it. I said I had someone downstairs. I said your name. I didn't say it for him. I said it for me."
    gf "I went into the restroom and shook for ten minutes. I typed to you, I deleted, I typed, I deleted. That's the dots."
    gf "'immn the toliet.' I was crying into the sink, [player_name]. I got it wrong because my hands wouldn't work."
    gf "I lied about the queue because I wanted to tell you in a world where you'd look at me the way you're looking at me now. Not the way you did in the corridor."
    gf "I liked being wanted. I didn't like him. I didn't know those were two different things until about four seconds in."
    gf "That's all of it. There isn't another door."

    "She stopped. The water went on lapping at the rock. I realized I'd been holding my breath for most of it."
    "Whatever the dreams had put in my head, they'd been wrong in every detail that mattered. The real version was smaller than the nightmare, and somehow harder, because it was the size of a person."
    gf "You said you had a dream. I don't know what you dreamed. I'd rather you ask me than dream it."
    gf "So. How are you looking at me?"

    $ set_story_flag("ch01_d5_club_disclosed")
    return


label ch01_day5_ntr_react_menu:

    $ d5_rt_thanks = format_choice("ch01_d5_ntr_react_thanks", "Thank you for telling me. The secret hurt more than the story.")
    $ d5_rt_bound = format_choice("ch01_d5_ntr_react_boundary", "I want to know before it happens next time. Not as a rule. Because I'd rather you not be alone.")
    $ d5_rt_curious = format_choice("ch01_d5_ntr_react_curious", "Tell me what it felt like, being looked at like that.")
    $ d5_rt_fine = format_day5_gate_choice("ch01_d5_ntr_gate_fine_hard", "I'm fine.", severity="hard", gate_label="D5-2")

    menu:
        "[d5_rt_thanks]":
            $ apply_choice("ch01_d5_ntr_react_thanks")
            $ set_story_value("ch01_d5_ntr_react", "thanks")
            mc "Thank you for telling me. The secret hurt more than the story."
            gf "That's the kindest thing you could have said. I don't think I'll ever be able to repay it."
            "She leaned against my shoulder, small and light, and the hairclip went back into her hair on the second try."
            jump ch01_day5_ntr_react_resolve
        "[d5_rt_bound]":
            $ apply_choice("ch01_d5_ntr_react_boundary")
            $ set_story_value("ch01_d5_ntr_react", "boundary")
            $ set_story_flag("ch01_d5_ntr_boundary_set")
            mc "Next time, I want to know before. Not as a rule. Because I'd rather you weren't alone."
            gf "That isn't a rule. That's a seatbelt."
            gf "Deal. And I want the same from you."
            mc "Deal."
            jump ch01_day5_ntr_react_resolve
        "[d5_rt_curious]":
            $ apply_choice("ch01_d5_ntr_react_curious")
            $ set_story_value("ch01_d5_ntr_react", "curious")
            $ set_story_flag("ch01_d5_ntr_curious")
            mc "Tell me what it felt like. Being looked at like that."
            gf "You're asking."
            mc "I'm asking."
            gf "Bright. And scary. Like standing very close to something I didn't understand. And then, after, like I'd been handed a mirror I didn't want to put down."
            gf "Why are you smiling?"
            mc "I'm not. I mean. I think my face is warm."
            gf "Not because someone kissed me."
            mc "Because you told me."
            gf "That's a very strange answer. And somehow the best one."
            jump ch01_day5_ntr_react_resolve
        "[d5_rt_fine]":
            $ apply_choice("ch01_d5_ntr_gate_fine_hard")
            $ set_story_value("ch01_d5_ntr_react", "fine")
            $ set_story_value("ch01_d5_ntr_outcome", "ntr_unresolved")
            $ set_story_value("ch01_d5_end_route_pending", "ntr_unresolved")
            mc "I'm fine."
            "It left my mouth like a coin I'd been told to spend."
            gf "No. You're not."
            gf "And I'm not either. But I thought you'd say something other than that."
            "She stood, put the hairclip back in, and looked out at the cove for a long time."
            gf "I'm still here. I'm just going to need you to be too."
            jump ch01_day5_ntr_react_resolve


label ch01_day5_ntr_react_resolve:

    # Only a real reaction (thanks / boundary / curious) after a disclosure repairs the route.
    # Gate picks that reach this label without a reaction leave the pending route as set.
    $ d5_react = get_story_value("ch01_d5_ntr_react", None)
    if d5_react in ("thanks", "boundary", "curious"):
        $ set_story_value("ch01_d5_ntr_outcome", "love_repaired")
        $ set_story_value("ch01_d5_end_route_pending", "love_repaired")
        $ set_story_flag("ch01_d5_ntr_repaired_by_disclosure")
    $ set_story_flag("ch01_d5_scene_08_complete")
    if get_story_value("ch01_d5_react_return", "sunset") == "dinner":
        jump ch01_day5_scene_10_dinner
    jump ch01_day5_scene_09_sunset

