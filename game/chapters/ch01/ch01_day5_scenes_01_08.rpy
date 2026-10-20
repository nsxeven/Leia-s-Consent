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
# Track set at the start from ch01_d4_end_route (stored): love / exhibitionism / love_repaired /
# nts_discovery / ntr_unresolved / ntr_confirmed. Route history is retained separately.
# All intimacy is NON-EXPLICIT: cut to CG placeholder cards. Every CG is Ryan's point of view.
# Captain Ilario is an experienced professional; he never neglects his duties.

define skipper = Character("Captain Ilario")

label ch01_day5_start:

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
            "love_repaired": "love_repaired",
            "nts_discovery": "nts_discovery",
            "ntr_unresolved": "ntr_unresolved",
            "ntr_confirmed": "ntr_confirmed",
        }.get(d5_end, "love")
        set_story_value("ch01_d5_d4_end", d5_end)
        set_story_value("ch01_d5_lane", d5_lane)
        set_story_value("ch01_d5_track", d5_track)
        set_story_value("ch01_d5_end_route_pending", {"love": "love", "exhibitionism": "exhibitionism", "love_repaired": "love_repaired", "nts_discovery": "nts_discovery", "ntr_unresolved": "ntr_unresolved", "ntr_confirmed": "ntr_confirmed"}[d5_track])
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
        set_story_value("ch01_d5_ryan_seasick", False)
        set_story_value("ch01_d5_leia_captain_interest", False)
        set_story_value("ch01_d5_captain_event", "none")
        set_story_value("ch01_d5_captain_truth_player", "unknown")
        set_story_value("ch01_d5_captain_truth_ryan", "unknown")
        set_story_value("ch01_d5_captain_truth_leia", "known")
        set_story_value("ch01_d5_captain_willing", "unknown")
        set_story_value("ch01_d5_ntr_confronted", False)
        set_story_value("ch01_d5_ryan_knows_adrian", bool(get_story_value("ch01_d4_ryan_knows_club_event", False)))
        set_story_value("ch01_d5_photo_delivery_pending", None)
        set_story_value("ch01_d5_nts_rerequested", False)
        set_story_value("ch01_d5_nts_ryan_willing", False)
        set_story_value("ch01_d5_nts_leia_willing", False)
        set_story_value("ch01_d5_nts_captain_willing", False)
        set_story_value("ch01_d5_nts_experience_occurred", False)
        set_story_value("ch01_d5_monitoring_active", bool(get_story_value("ch01_d4_monitoring_active", False)))

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
    "A broad, heavyset man in a battered cap looked down from the cockpit. Gray stubble roughened his jaw; his sun-weathered face suggested he'd been unimpressed by guests for decades."
    "He checked the lines before he checked us."
    skipper "Captain Ilario. Four guests. Two nights. Please keep the number of guests at four."
    friend "We have a lot of faith in the number."
    skipper "Good. Faith is not a flotation device."

    if d5_hook == "maybe":
        maya "You said it depended on the morning, Ryan. It's the morning."
        mc "It turned out the morning was fine."
        maya "The morning's always fine. It's you that has to turn up."
    elif d5_hook == "ask_leia":
        friend "Ryan checked with Leia first. I want that noted in the minutes."
        maya "Julian is nominating himself for secretary."
    else:
        maya "Ryan said 'we're in' and I would like to thank him for his enthusiasm. It was a very average amount."

    if d5_track in ("love", "love_repaired"):
        "Leia's hand was in mine before we were off the gangway. She carried a canvas tote with a length of pale rope sticking out of the top."
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
        "Leia wore round sunglasses and the expression of someone carrying a secret in a very small bag."
        gf "Morning, partner in crime."
        mc "What's the idea?"
        gf "You said yes. You don't get the idea until the water."
        mc "That's not how yes works."
        gf "It's exactly how yes works when I've already packed."
    elif d5_track == "nts_discovery":
        "Leia's hand found mine at the top of the gangway. The squeeze was brief, but deliberate."
        gf "No pressure to make today about that conversation."
        mc "Good. I want the day too."
        gf "Then let's have it."
    elif d5_track == "ntr_repaired": # Legacy alias retained for older saves.
        "Leia's hand found mine at the top of the gangway. She held on longer than she needed to."
        gf "I want today to be a day together. We can talk when we're ready."
        mc "Okay."
    elif d5_track == "ntr_unresolved":
        "Leia was already on the pier, a little apart, with Maya's arm hooked through hers."
        gf "Morning."
        mc "Morning."
        "It was the kind of 'morning' two people say when both of them have rehearsed the next sentence and neither will say it first."
        "Maya looked between us and decided, visibly, to be loud."
    else:
        "Maya and Julian took me by either elbow before I'd reached the gangway."
        maya "Friend patrol."
        friend "We've been told it's mandatory."
        mc "By whom?"
        maya "By the part of us that loves you and is tired."
        "Leia stood a few steps ahead with her bag on both shoulders, not looking back, not exactly avoiding it either."

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
        "Leia unzipped her bag on the cockpit bench, sorting like a woman defusing something sweet."
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
                        title_text="Pick Leia's boat outfit",
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
        "Leia emptied two swimsuits onto the bench: the classic one and the bolder one from the pool."
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
        "Leia packed the way she'd packed all week: neatly, alone, and without asking."
        if d5_track == "ntr_repaired": # Legacy alias retained for older saves.
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
                "I stood there with my hands in my pockets while Leia carried her own bag down the companionway."

        $ d5_wore = ch01_d5_wear("pool_conservative")
        $ set_story_value("ch01_d5_swim_outfit_id", "pool_conservative")
        $ set_story_value("ch01_d5_pack_outfit_source", "leia")

    $ set_story_flag("ch01_d5_scene_01_complete")
    jump ch01_day5_scene_02_departure


label ch01_day5_scene_02_departure:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_deck
    with dissolve

    # AUDIO TODO: engine starting, halyards, gulls fading behind the breakwater.

    "The yacht eased away from the pier. The water beyond the harbor was bright and calm, and my stomach felt perfectly ordinary."
    friend "You used to steer from that bench when you were twelve."
    maya "You were twelve?"
    friend "I was trusted with a line. Not the boat."
    skipper "And he still knows which one not to touch. That's a start."
    "Julian moved around the deck without hesitation, pointing out the headland and the reef beyond it."
    "The forward cabin opened onto a shaded side deck. From the bunk, with the door open, I could see that narrow stretch; the helm sat farther aft around the saloon."
    "I leaned against the rail and let the morning warm my face. No one was sick. No one was in a hurry."

    $ d5_js_stay = format_choice("ch01_d5_julian_stay", "Sit with him. Keep him talking.")
    $ d5_js_joke = format_choice("ch01_d5_julian_joke", "Tell him the horizon's on his side.")
    $ d5_js_leave = format_choice("ch01_d5_julian_leave", "Leave him to Maya and go find some shade.")

    menu:
        "[d5_js_stay]":
            $ apply_choice("ch01_d5_julian_stay")
            mc "Show me where you used to sit."
            friend "Right here. I thought I was in charge of the sea."
            mc "And now?"
            friend "Now I know better."
            "He grinned and took the line I offered him, hands sure and practiced."
        "[d5_js_joke]":
            $ apply_choice("ch01_d5_julian_joke")
            mc "You're very smug for someone who doesn't own the boat."
            friend "I own the confidence. The boat's my father's."
            maya "And the tab is mine."
        "[d5_js_leave]":
            $ apply_choice("ch01_d5_julian_leave")
            mc "I'll take the camera. You two have the view."
            friend "A generous arrangement."
            maya "I want it noted he surrendered the camera voluntarily."
            "Leia leaned into my shoulder as Maya framed the headland."

    "Julian named the coves as they passed them. He was comfortable enough to tease Maya about her navigation app, then correct it from memory."
    "I felt good. The sun, the wind, the easy noise of the group: all of it was exactly what I'd hoped the trip would be."
    $ set_story_flag("ch01_d5_scene_02_complete")
    jump ch01_day5_scene_03_no_bars


label ch01_day5_scene_03_no_bars:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_deck
    with dissolve

    "Leia took her towel to the bow, where the folded sail shaded the cushions but left the open water in view."
    if d5_track in ("exhibitionism", "nts_discovery"):
        gf "Stay there a second. I want to know if I still like being noticed when you're the one watching."
        mc "And if you don't?"
        gf "Then I'll say so, and we'll go swimming."
        $ d5_attention_choice = format_choice("ch01_d5_attention_join", "Stay with her and share the moment.")
        $ d5_attention_private = format_choice("ch01_d5_attention_private", "Tell her you would rather keep this between you two.")
        menu:
            "[d5_attention_choice]":
                $ apply_choice("ch01_d5_attention_join")
                $ set_story_value("ch01_d5_attention_shared", True)
                $ set_story_value("ch01_d5_leia_captain_interest", True)
                gf "Okay. With you here. That's what I wanted."
                "She lay face down in the sun, then quietly loosened the back of her swimsuit beneath the towel. She glanced from me to the helm, checking that I understood the choice was deliberate."
                "I stayed beside her. The moment belonged to both of us because we'd chosen it together."
                skipper "If you need shade moved, say so."
                gf "I'm all right, Captain. Thank you."
                "Ilario acknowledged her with a nod and went back to checking the line."
            "[d5_attention_private]":
                $ apply_choice("ch01_d5_attention_private")
                $ set_story_value("ch01_d5_attention_shared", False)
                $ set_story_value("ch01_d5_leia_captain_interest", False)
                gf "Then just you. Or nobody. I can decide that too."
                "She smiled, drew the towel closer and leaned her shoulder against mine."
    elif d5_track == "love":
        gf "Come sit with me. I want the quiet before Maya finds another game."
        "We watched the coastline slide by, her head resting against my shoulder."
    elif d5_track == "love_repaired":
        gf "Could you sit with me? I don't need an answer to anything. Just company."
        mc "Yeah."
        "We sat side by side and watched the coast pass without asking the morning to fix us."
    elif d5_track == "ntr_confirmed":
        $ set_story_value("ch01_d5_leia_captain_interest", True)
        "Leia carried her towel toward the bow while I stayed near the cockpit. Julian asked me to help him check the dry bags."
        "By the time I looked up, Leia had settled near the rail. I could not tell what she had intended by choosing that spot."
    else:
        "Leia sat alone near the bow for a while. I watched the shoreline instead of asking what she wanted from me."

    "Around nine, my phone made the small unhappy noise phones make when they stop hearing the world."
    "Signal dropped from two bars to one, then to a little gray X."
    maya "No bars."
    friend "No bars?"
    maya "No bars, Julian. No group chat, no maps, no one to blame."
    skipper "There is no signal beyond the second headland. This is considered a feature."

    if d5_track == "love":
        gf "Look at me instead."
        mc "That's the best offer I've had all week."
        gf "It's the only offer you've had all week. But it's still the best."
    elif d5_track == "exhibitionism":
        gf "Phone rule. Phones in the dry bag until dinner."
        mc "That's very strict."
        gf "I told you. I have an idea. It needs your full attention."
    elif d5_track == "love_repaired":
        gf "No signal. We can have a few quiet hours."
        mc "Quiet sounds good."
    elif d5_track == "nts_discovery":
        gf "No signal. No pressure to make a decision today."
        mc "I don't want a decision just because we're on a boat."
        gf "Good. I want it to be ours when we do decide."
    elif d5_track == "ntr_unresolved":
        "Leia's thread showed her last message, 'Sorry.', sent in the dark the night before. I looked at it again, and put the phone away, and looked at it again."
    else:
        "The thread with Leia still showed my last reply: nothing. I looked at the little gray X and, for once, was glad of it."

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

    "Captain Ilario cut the engine over a reef the color of bruised sea glass and dropped the anchor with the calm precision of long practice."
    skipper "Snorkel. Two at a time. The boat stays within shouting distance. I do not shout."
    friend "I'll supervise."
    maya "Julian is the lifeguard. He's wearing a hat."
    friend "It's a very official hat."

    "There were two masks left for the first pair, and four people with opinions."
    gf "Ryan. First pair. Pick."

    if d5_track.startswith("ntr"):
        $ d5_sn_leia = format_choice("ch01_d5_snorkel_leia_first", "Go in with Leia.")
        $ d5_sn_maya = format_choice("ch01_d5_snorkel_maya_first", "Let Maya and Julian go first.")
        $ d5_sn_stay = format_day5_gate_choice("ch01_d5_ntr_snorkel_stay", "I'll stay on the boat. You go.", severity="soft", gate_label="D5-1")
        menu:
            "[d5_sn_leia]":
                $ apply_choice("ch01_d5_snorkel_leia_first")
                $ set_story_value("ch01_d5_snorkel_first", "leia")
                mc "I'll go with Leia, if she'll have me."
                if d5_track == "ntr_confirmed":
                    gf "It's a very big ocean."
                    mc "I'll keep to my corner of it."
                    gf "...Fine. Corner."
                else:
                    gf "I'll have you."
            "[d5_sn_maya]":
                $ apply_choice("ch01_d5_snorkel_maya_first")
                $ set_story_value("ch01_d5_snorkel_first", "maya")
                mc "Maya and Julian first. I'll watch the boat."
                maya "I'm going to need a minute to forgive that."
                gf "It's fine."
                "She said it the way I'd said it eleven times in two days, and I heard it for the first time."
            "[d5_sn_stay]":
                $ apply_choice("ch01_d5_ntr_snorkel_stay")
                $ set_story_value("ch01_d5_snorkel_first", "none")
                mc "I'll stay on the boat. You go."
                gf "You'll stay on the boat."
                mc "I'll be here."
                "Leia pulled her mask over her hair and went in without another word. Maya watched me for a second and went in after her."
    else:
        $ d5_sn_leia = format_choice("ch01_d5_snorkel_leia_first", "Go in with Leia.")
        $ d5_sn_maya = format_choice("ch01_d5_snorkel_maya_first", "Go in with Maya. Leia will have more fun with Julian.")
        $ d5_sn_jul = format_choice("ch01_d5_snorkel_julian_first", "Send Leia and Maya. I'll hold the camera.")
        menu:
            "[d5_sn_leia]":
                $ apply_choice("ch01_d5_snorkel_leia_first")
                $ set_story_value("ch01_d5_snorkel_first", "leia")
                mc "Leia. Obviously."
                gf "Obviously. Good. I wasn't going to ask twice."
            "[d5_sn_maya]":
                $ apply_choice("ch01_d5_snorkel_maya_first")
                $ set_story_value("ch01_d5_snorkel_first", "maya")
                mc "Maya. Julian takes Leia."
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
        gf "There's a fish down there with a face like Julian."
        mc "That's cruel."
        gf "It was a compliment. It looked very responsible."
        $ exit_cinematic_mode()
        scene bg ch01_d5_reef_surface
        with dissolve
        gf "I lost my clip."
        mc "What?"
        gf "It came off when I dove. It's down there."
        "I dove twice. The second time I found it, wedged in a bright fan of coral, the hairclip winking like an unfair sort of treasure."
        "I came up with it. Leia kissed me in the water, salt and sunscreen, and then took it back to wear again, damp, immediately."
        gf "You are a better treasure hunter than a photographer."
        mc "That's not a very high bar."
        gf "It's a very high bar. I've seen your photos."
        if d5_track == "love":
            $ enter_cinematic_mode()
            scene cg ch01_d5_love_cove_swim
            with dissolve
            "We stayed close in the water, laughing when the current nudged us apart and reaching for each other again."
            $ exit_cinematic_mode()
            scene bg ch01_d5_reef_surface
            with dissolve
            gf "One photo before we go back? Just me, when I'm happy."
            $ enter_cinematic_mode()
            scene cg ch01_d5_love_cove_secret
            with dissolve
            "She settled on a warm rock beside the swim ladder, chin resting on her arm. I took the picture when she looked up and smiled."
            $ exit_cinematic_mode()
            scene bg ch01_d5_reef_surface
            with dissolve
            $ set_story_value("ch01_d5_love_photo_saved", True)
        $ set_story_flag("ch01_d5_clip_rescued_by_ryan")
    elif d5_first == "maya":
        "Maya drifted beside me, her snorkel clamped between her teeth, giving a thumbs up every four seconds like a diver in a safety video."
        "On the surface, afterward, she pushed her mask up and looked at the boat."
        maya "I need to tell you something, and I need you to let me say it badly."
        mc "Okay."
        maya "I like him. Julian. I don't know what to do with it."
        mc "Have you tried telling him?"
        maya "I've tried telling him in a lot of ways. All of them were jokes."
        $ set_story_flag("ch01_d5_maya_confided_early")
        "While we talked, the hairclip drifted off Leia's head on the far side of the boat. Julian leaned over the rail and netted it with Captain Ilario's long-handled skimmer."
        friend "I've saved the clip."
        skipper "Fish do not wear jewelry. Please remind them."
        $ set_story_flag("ch01_d5_clip_rescued_by_julian")
    elif d5_first == "camera":
        "I stood on the swim platform with the camera and watched two women bob on the surface like very happy buoys."
        "Maya waved. Leia dove, came up, and held up a perfect, tiny starfish for the lens."
        gf "Photo."
        mc "Photo."
        "On the way back up the ladder, her hairclip came off in the water. Julian leaned over the rail and netted it with Captain Ilario's long-handled skimmer."
        friend "I've saved the clip."
        skipper "Fish do not wear jewelry. Please remind them."
        $ set_story_flag("ch01_d5_clip_rescued_by_julian")
    else:
        "From the swim platform I watched Leia and Maya cut slow circles over the reef, like they had a lot to say and a lot of sea to say it in."
        "A hairclip floated up through the glitter, a small gold thing, and Julian leaned over with the skimmer."
        friend "I've saved the clip."
        skipper "Fish do not wear jewelry. Please remind them."
        $ set_story_flag("ch01_d5_clip_rescued_by_julian")

    $ set_story_flag("ch01_d5_scene_04_complete")
    jump ch01_day5_scene_05_cove_lunch


label ch01_day5_scene_05_cove_lunch:

    $ d5_track = get_story_value("ch01_d5_track", "love")
    $ d5_style = get_story_value("ch01_d4_photo_style", "none")

    scene bg ch01_d5_boat_deck
    with fade

    # AUDIO TODO: quiet lapping, a cicada, the canvas of the boat's awning flapping once.

    "The yacht turned toward a sheltered cove and settled at anchor. Captain Ilario checked the lines and the weather before joining us at the cockpit table."
    "Lunch was a basket Teodoro had packed: cold chicken, flatbread, olives, and a jar of honey with a note taped to the lid."
    maya "'For the bee enthusiast.' Julian."
    friend "I want it known that I did not request that."
    maya "Teodoro's a poet."

    "We ate at the cockpit table, close enough to hear the water under the hull and far enough from the shore that the cove felt private. My phone had no service; I left it in the dry bag."

    # Honey / bee gag: callback to Day 2 bee and Julian's fear.
    "It was a regular, unremarkable honeybee. It landed on the lid of the honey jar as if it had been summoned."
    friend "Nobody. Move."
    maya "It's a bee."
    friend "It is a bee, Maya. It is a bee on a jar of honey on a beach in a cove on a boat."
    maya "You're holding the chicken."
    friend "I'm holding the chicken extremely still."

    $ d5_be_calm = format_choice("ch01_d5_bee_calm", "Calmly lift the jar and carry the bee away from Julian.")
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
            "Julian froze with a drumstick in one fist and a bee on the lid of the honey jar in front of him. Maya, off to the side, was losing her whole self to laughter."
            $ exit_cinematic_mode()
            scene bg ch01_d5_cove_beach
            with dissolve
            friend "I want it on record that I am not okay."
            maya "It's on the record. It's in the photo. It's evidence."
            gf "Ryan. Put the camera down and help him."
            "I did, eventually, and the bee left on its own, which was either mercy or contempt."

    "Maya took the camera out of my hands before I'd set it down."
    maya "Group photo. Julian, next to me. Leia, stand by the light. Ryan, you take it."
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
            $ set_story_value("ch01_d5_photo_delivery_pending", "group")
        "[d5_ps_keep]":
            $ apply_choice("ch01_d5_photo_keep_album")
            $ set_story_value("ch01_d5_photo_group", "kept")
            mc "I'm keeping this one for myself."
            gf "He's a collector."
            maya "He's a thief."
            $ set_story_value("ch01_d5_photo_delivery_pending", "private_album")

    $ set_story_flag("ch01_d5_scene_05_complete")
    jump ch01_day5_scene_06_deck_talk


label ch01_day5_scene_06_deck_talk:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_foredeck
    with fade

    "After lunch, we left the shelter of the first cove and headed toward the second. The swell was gentle, but the yacht began to move under me in a way I couldn't ignore."
    "I lost the thread of Maya's story, then the horizon, then my appetite."
    $ d5_seasick_tell = format_choice("ch01_d5_seasick_tell_leia", "Tell Leia plainly that you feel sick.")
    $ d5_seasick_minimize = format_choice("ch01_d5_seasick_minimize", "Brush it off, then admit you need to lie down.")
    menu:
        "[d5_seasick_tell]":
            $ apply_choice("ch01_d5_seasick_tell_leia")
            mc "I think I need to lie down. I'm getting seasick."
            gf "Okay. Forward cabin or saloon? I'll get water."
            $ set_story_value("ch01_d5_seasick_communication", "direct")
        "[d5_seasick_minimize]":
            $ apply_choice("ch01_d5_seasick_minimize")
            mc "I'm fine. Just need a minute."
            gf "Ryan, you stopped answering me. You don't have to pretend."
            mc "I know. Cabin, please."
            $ set_story_value("ch01_d5_seasick_communication", "minimized")

    $ set_story_value("ch01_d5_ryan_seasick", True)
    $ set_story_flag("ch01_d5_ryan_seasick")
    "Leia brought water and stayed beside me while I settled into the forward cabin."
    gf "Do you want me to stay?"
    $ d5_rest_company = format_choice("ch01_d5_rest_company", "Ask her to sit with you for a little while.")
    $ d5_rest_quiet = format_choice("ch01_d5_rest_quiet", "Ask for quiet and let her go back on deck.")
    menu:
        "[d5_rest_company]":
            $ apply_choice("ch01_d5_rest_company")
            mc "A little while. If you don't mind."
            gf "I don't."
            "She sat near the doorway and kept the conversation light until my eyes closed."
            $ set_story_value("ch01_d5_care_choice", "company")
        "[d5_rest_quiet]":
            $ apply_choice("ch01_d5_rest_quiet")
            mc "Quiet would help."
            gf "All right. I'll be right outside. Call if you need me."
            "She left the water within reach and waited for me to settle before closing the cabin door partway."
            $ set_story_value("ch01_d5_care_choice", "quiet")

    "Julian checked the course with Ilario, entirely at ease as the yacht continued toward the cove."
    $ set_story_flag("ch01_d5_scene_06_complete")
    jump ch01_day5_scene_07_stern


label ch01_day5_scene_07_stern:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    scene bg ch01_d5_boat_deck
    with fade

    "The anchor caught in the second cove. Ilario checked the line, the depth and the weather before easing the engine down."
    "Maya and Julian took the tender toward the rocks with an agreed return time. Julian checked the painter himself, then helped Maya aboard."
    "Leia stayed with me. She brought a fresh glass of water, then stopped at the cabin doorway instead of assuming I wanted company."
    gf "How are you feeling now?"
    mc "Still rough. A little better when I don't look at the water."
    gf "Then don't. I'll be here."
    "She sat outside the cabin with her back against the frame. I could hear Ilario moving through his checks on deck and talking through the return route."
    if d5_track == "nts_discovery":
        gf "We can leave our conversation for another day."
        mc "Let's wait until I feel like myself."
        $ set_story_value("ch01_d5_nts_defer_until_recovered", True)
        gf "Okay. I mean it."
    "Time passed. The water and the still cabin eased the worst of it. I was still queasy, but steady enough to sit up and follow a conversation."
    $ set_story_value("ch01_d5_ryan_recovered", True)
    $ set_story_value("ch01_d5_second_cove_status", "anchored_safe")
    $ set_story_flag("ch01_d5_scene_07_complete")
    jump ch01_day5_scene_08_cove_afternoon


label ch01_day5_scene_08_cove_afternoon:

    $ d5_track = get_story_value("ch01_d5_track", "love")

    if d5_track == "love":
        jump ch01_day5_scene_08_love_cove
    elif d5_track == "exhibitionism":
        jump ch01_day5_scene_08_exhib_cove
    elif d5_track == "nts_discovery":
        jump ch01_day5_scene_08_nts_discovery
    elif d5_track == "love_repaired":
        jump ch01_day5_scene_08_love_repaired
    else:
        jump ch01_day5_scene_08_ntr_apart


label ch01_day5_scene_08_love_cove:

    scene bg ch01_d5_boat_cabin
    with fade

    "The cabin stopped moving as much once the anchor settled. The water stayed within reach. Leia sat in the open doorway, giving me room to breathe."
    gf "I thought we'd have the whole afternoon together."
    mc "I did too. I'm sorry I'm missing the cove."
    gf "You don't have to apologize for being sick."
    mc "I know. I still wanted the day with you."
    gf "You have it. Just a slower version."
    "She told me about the coastline from the deck, making the view sound better than it probably was. I told her about a trip we'd taken years ago, before we knew how to plan anything."
    "The conversation wandered. It didn't need to fix anything. It was enough that she wanted to stay and I wanted her there."
    gf "When you're feeling better, I'll show you the knot I learned."
    mc "And the rope?"
    gf "That's for later. No deadlines."

    $ d5_love_companionship = format_choice("ch01_d5_love_company", "Ask her to stay a little longer.")
    $ d5_love_rest = format_choice("ch01_d5_love_rest", "Tell her you need to close your eyes.")
    menu:
        "[d5_love_companionship]":
            $ apply_choice("ch01_d5_love_company")
            mc "Stay until I fall asleep?"
            gf "Of course."
            "She took my hand and sat quietly until I drifted off."
            $ set_story_value("ch01_d5_love_afternoon", "company")
        "[d5_love_rest]":
            $ apply_choice("ch01_d5_love_rest")
            mc "I need to close my eyes for a while."
            gf "Sleep. I'll be right outside."
            "She set the glass within reach and let the cabin go quiet."
            $ set_story_value("ch01_d5_love_afternoon", "rest")

    $ set_story_value("ch01_d5_ryan_recovered", True)
    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset


label ch01_day5_scene_08_love_repaired:

    scene bg ch01_d5_boat_cabin
    with fade

    "The cabin had grown quiet. Leia stayed in the doorway while I drank the water she'd brought."
    if get_story_value("ch01_d4_betrayal_disclosed", False):
        gf "I know a good afternoon doesn't undo what I told you. I don't expect it to."
        mc "I want today to be a day together. I also want to be honest when something still hurts."
        gf "Then be honest. I can hear it."
        "We talked about one specific moment from the night before: what each of us had heard, and what still felt difficult to say. Leia listened without reaching for an easy promise."
        $ set_story_value("ch01_d5_repair_provenance", "disclosed_betrayal")
    else:
        gf "We don't have to solve the week today."
        mc "I know. I just don't want to drift past each other again."
        gf "Then let's stay here for a bit."
        "We talked about the small misunderstandings we'd left alone and what we wanted to do differently when we got home."
        $ set_story_value("ch01_d5_repair_provenance", "unresolved_uncertainty")
    $ enter_cinematic_mode()
    scene cg ch01_d5_ntr_cove_talk
    with dissolve
    "She sat near the open doorway with her hands folded around the hairclip. I sat on the bunk, listening without asking her to turn the afternoon into a promise."
    $ exit_cinematic_mode()
    scene bg ch01_d5_boat_cabin
    with dissolve
    "She asked whether I wanted company or quiet and accepted my answer. There was no second confession and no new route pitch."
    $ set_story_value("ch01_d5_ryan_recovered", True)
    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset


label ch01_day5_scene_08_exhib_cove:

    $ d5_watch_d4 = has_story_flag("ch01_d4_exhib_ryan_likes_watching")
    scene bg ch01_d5_boat_foredeck
    with fade

    "After resting, I felt steady enough to sit in the shade by the companionway. Leia came up from below and stopped beside me."
    gf "This morning was for being noticed. I want to know what it feels like to choose that with you here."
    mc "Only as far as you want."
    gf "I know."
    "Maya and Julian were still ashore. Ilario stayed at the helm, attentive to the anchored boat and the weather."
    $ d5_ex_stay = format_choice("ch01_d5_exhib_stay", "Stay beside her. Let her set the pace.")
    $ d5_ex_watch = format_choice("ch01_d5_exhib_watching", "Tell her you like watching when she chooses it.")
    $ d5_ex_priv = format_choice("ch01_d5_exhib_private", "Ask to keep the afternoon private between you two.")
    menu:
        "[d5_ex_stay]":
            $ apply_choice("ch01_d5_exhib_stay")
            $ set_story_value("ch01_d5_exhib_variant", "shared_step")
            mc "Your pace. I'm right here."
            gf "Thank you. I want you here."
        "[d5_ex_watch]":
            $ apply_choice("ch01_d5_exhib_watching")
            $ set_story_value("ch01_d5_exhib_variant", "ryan_likes_watching")
            $ set_story_flag("ch01_d5_exhib_ryan_likes_watching")
            mc "I like watching when I know you're choosing it."
            gf "That's exactly why I asked you."
        "[d5_ex_priv]":
            $ apply_choice("ch01_d5_exhib_private")
            $ set_story_value("ch01_d5_exhib_variant", "private")
            mc "Could we keep the rest of this between us?"
            gf "Yes. I wanted to ask you the same thing."

    if get_story_value("ch01_d5_exhib_variant") != "private":
        python:
            d5_ex_now = partner_stats["exhibitionism"]
            d5_ex_prev = get_story_value("ch01_d4_exposure_step", "none")
            d5_ex_call = ch01_d5_leia_call_for(d5_ex_now, d5_ex_prev)
            d5_ex_variant = get_story_value("ch01_d5_exhib_variant", "shared_step")
        if d5_ex_variant == "ryan_likes_watching":
            $ enter_cinematic_mode()
            scene cg ch01_d5_exhib_cove_watching
            with dissolve
            "From my place beside the cabin doorway, I watched Leia decide what she was comfortable showing. The cove and the water were visible behind her; Ilario remained at the helm."
            $ exit_cinematic_mode()
        if d5_ex_call == "ties_loosened":
            $ enter_cinematic_mode()
            scene cg ch01_d5_exhib_cove_01
            with dissolve
            "Leia lay face down on the cushioned foredeck and loosened the ties of her swimsuit beneath the towel. She turned her head to check my expression, then settled when I met her eyes."
            gf "That's enough for today."
            $ exit_cinematic_mode()
            $ set_story_value("ch01_d5_exposure_step", "ties_loosened")
            $ set_story_flag("ch01_d5_exhib_tease_done")
        else:
            $ enter_cinematic_mode()
            scene cg ch01_d5_exhib_cove_02
            with dissolve
            "After checking with me once more, Leia sat in the sun with her swimsuit top folded beside her, her arms comfortably crossed and her face tipped toward the light. The framing stayed on her face and shoulders."
            gf "It's warm. That's all. I thought I'd feel different."
            $ exit_cinematic_mode()
            $ set_story_value("ch01_d5_exposure_step", "comfortable")
            $ set_story_flag("ch01_d5_exhib_comfortable_done")
    else:
        "She stayed dressed and tucked herself against my shoulder. The attention we shared was ours alone."

    scene bg ch01_d5_boat_foredeck
    with dissolve
    gf "What did it feel like for you?"
    menu:
        "I liked sharing the moment.":
            $ set_story_value("ch01_d5_exhib_afternoon_reaction", "shared")
            mc "Like we were both choosing it. That was the part I liked."
            gf "Me too."
        "I liked having it just between us.":
            $ set_story_value("ch01_d5_exhib_afternoon_reaction", "private")
            mc "I liked that it was still just us, even with the rest of the boat around."
            gf "That's what I wanted to hear."
    $ set_story_value("ch01_d5_end_route_pending", "exhibitionism")
    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset


label ch01_day5_scene_08_nts_discovery:

    scene bg ch01_d5_boat_cabin
    with fade

    "Leia waited until my breathing had settled and I could sit up without the cabin tilting. She brought water, then asked before taking the chair beside the bunk."
    gf "We said we might talk about it again. We don't have to."
    mc "I want to talk. I'm not sure I want to do anything."
    gf "That's enough for me."
    if not ch01_nts_agreed():
        "The agreement we'd discussed before wasn't present in the saved story state. We left the subject there and spent the afternoon together."
        $ set_story_value("ch01_d5_nts_postponed", True)
        $ set_story_value("ch01_d5_end_route_pending", "love_repaired")
        $ set_story_flag("ch01_d5_scene_08_complete")
        jump ch01_day5_scene_09_sunset

    gf "I did feel something at the club. I also know you were hurt by how I handled it. I don't want curiosity to erase that."
    mc "It doesn't. I don't want what happened before to become permission for anything now."
    gf "Good. Then we decide now, together, and we can stop at any point."
    "Ilario came by after finishing his checks. Leia asked if he had a few minutes to talk. He stayed on the shaded side deck just beyond the open cabin door, free to return to work. From the bunk, I could see them clearly."
    skipper "I can talk. I'm not promising anything."
    gf "That's fair."

    $ d5_nts_talk_only = format_choice("ch01_d5_nts_talk_only", "Keep this as a conversation. No contact today.")
    $ d5_nts_first_step = format_choice("ch01_d5_nts_first_step", "If everyone still wants it, allow one brief first step.")
    menu:
        "[d5_nts_talk_only]":
            $ apply_choice("ch01_d5_nts_talk_only")
            $ set_story_value("ch01_d5_nts_rerequested", True)
            $ set_story_value("ch01_d5_end_route_pending", "nts_discovery")
            mc "Let's leave it at talking today."
            gf "I like that you said what you wanted."
            skipper "Then that's what we do."
            "We talked about what each of us was curious about, what would make us uncomfortable, and how either of them could stop the conversation. We made no plan to act before discussing it again."
            $ set_story_value("ch01_d5_nts_boundaries_discussed", True)
            $ set_story_value("ch01_d5_ryan_willing", True)
            $ set_story_value("ch01_d5_leia_willing", True)
            $ set_story_value("ch01_d5_captain_willing", "not_asked")
            $ set_story_value("ch01_d5_nts_ryan_willing", True)
            $ set_story_value("ch01_d5_nts_leia_willing", True)
            $ set_story_value("ch01_d5_nts_captain_willing", False)
            $ set_story_value("ch01_d5_nts_experience_occurred", False)
            $ set_story_value("ch01_d5_nts_postponed", True)
        "[d5_nts_first_step]":
            $ apply_choice("ch01_d5_nts_first_step")
            $ set_story_value("ch01_d5_nts_rerequested", True)
            mc "Only if we're all still choosing it. One step, and anyone can stop."
            gf "I am choosing it. But I want us to check again after."
            skipper "I'm willing, if the boat is settled and my duties stay clear. We stop if I need the deck."
            $ set_story_value("ch01_d5_ryan_willing", True)
            $ set_story_value("ch01_d5_leia_willing", True)
            $ set_story_value("ch01_d5_captain_willing", True)
            $ set_story_value("ch01_d5_nts_ryan_willing", True)
            $ set_story_value("ch01_d5_nts_leia_willing", True)
            $ set_story_value("ch01_d5_nts_captain_willing", True)
            $ set_story_value("ch01_d5_nts_boundaries_discussed", True)
            $ set_story_value("ch01_d5_nts_experience_occurred", True)
            $ set_story_value("ch01_d5_nts_postponed", False)
            $ set_story_value("ch01_d5_end_route_pending", "nts_discovery")
            "Ilario waited until I gave a clear nod. Leia checked my face once more. The moment remained brief and non-graphic. I watched from the open cabin doorway, knowing what we'd agreed to and knowing I could end it. When it was over, nobody pretended the feeling was simple."
            $ set_story_value("ch01_d5_nts_ryan_reaction", "mixed")
            $ set_story_value("ch01_d5_nts_leia_reaction", "uncertain")
            mc "I need a minute to understand what I felt."
            gf "Take it. I'll stay."

    "Leia sat beside me again after Ilario returned to his checks. We talked about what we had each felt, without turning it into a promise about next time."
    $ set_story_value("ch01_d5_ryan_recovered", True)
    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset


label ch01_day5_scene_08_ntr_repaired:
    # Legacy save compatibility: older builds used this label for the repaired route.
    jump ch01_day5_scene_08_love_repaired


label ch01_day5_scene_08_ntr_apart:

    $ d5_track = get_story_value("ch01_d5_track", "ntr_unresolved")

    scene bg ch01_d5_boat_cabin
    with fade

    "Leia came back to the cabin with the water. I was awake enough to hear the deck boards creak as she stepped away and returned."
    if d5_track == "ntr_confirmed":
        # Objective story truth is stored separately. Strict Ryan POV leaves both Ryan and
        # the player without confirmation here; no off-screen event is presented as evidence.
        $ set_story_value("ch01_d5_captain_event", "secret_kiss")
        $ set_story_value("ch01_d5_captain_truth_player", "unknown")
        $ set_story_value("ch01_d5_captain_truth_ryan", "unknown")
        $ set_story_value("ch01_d5_captain_truth_leia", "known")
        $ set_story_value("ch01_d5_captain_willing", "yes")
        $ set_story_value("ch01_d5_monitoring_active", True)
        $ set_story_flag("ch01_d5_captain_secret_meeting")
        "A low exchange carried through the open companionway, too indistinct to make out. When Leia returned, she set down the water and asked if I needed anything else."
        gf "I'll be on deck if you need me."
        mc "Okay."
        "She waited a second longer than the question required. I couldn't tell why."
    else:
        "She sat outside the doorway while I rested. When I apologized for missing the cove, she told me not to turn a bad stomach into a bad day between us."
        gf "We can talk when you're ready. I'm not going to make you do it from a bunk."
        mc "Thanks."
        "For a while, neither of us tried to fill the quiet."

    $ set_story_value("ch01_d5_ryan_recovered", True)
    $ set_story_flag("ch01_d5_scene_08_complete")
    jump ch01_day5_scene_09_sunset
