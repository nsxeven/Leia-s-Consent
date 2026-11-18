# Leia's Consent — Chapter One: Something Different
# Day Two, Scenes 1–15.
#
# Day Two progression:
# - Love: Ryan stays attentive/protective without suppressing Leia's agency.
# - Exhibitionism: Ryan and Leia explore attention together.
# - NTR-risk: emotional disengagement, not consensual openness, creates pressure.



label ch01_day2_start:
    if LC_DAY1_DEMO_BUILD:
        jump ch01_day1_demo_complete
    $ lc_review_begin("ch01_d2")


    $ set_story_flag("ch01_day_02_started")
    $ set_story_value("ch01_d2_ntr_soft_gate", False)
    $ set_story_value("ch01_d2_ntr_confirmed", False)
    $ set_story_value("ch01_d2_dinner_wink", False)

    scene black
    with fade
    centered "[lc_chapter_card_day2]"

    jump ch01_day2_scene_01_morning_after


label ch01_day2_scene_01_morning_after:

    scene bg ch01_master_bedroom_curtains  # Day 2 morning: day art (darryn); text mentions the curtains
    with fade

    "Morning arrived slowly through the useless decorative curtains."

    # 11:00 = the time Julian set last night ("Breakfast after 11 or I'm calling the police").
    # Keep this diegetic time local to the wake beat; it is rollback-safe and
    # each delivered message keeps its own time when the thread is revisited.
    $ lc_phone_set_story_time("11:00")
    $ lc_sfx("phone_notify")
    "My phone buzzed against the nightstand until I gave up and looked at it. 11:00, on the dot."
    python:
        phone_add_message(
            "group",
            "julian",
            text="Bro wake up",
            message_id="ch01_d2_julian_wake_up",
            mark_unread=True,
            notify=True,
            notification_title="Trip Group",
        )
    think "He'd said eleven last night. I was there when he said it, and I'd still somehow decided it was a joke."

    "I eased out of bed as quietly as I could and looked back."

    scene cg ch01_d2_leia_sleeping
    with dissolve
    $ lc_notice_begin("d2_notice_bed_hand")  # Things Ryan noticed (docs/NOTICES.md)

    "[girlfriend_name] had claimed about three-quarters of the bed at some point in the night."
    "One arm was flung over her head, the other was hanging off the edge, and her mouth was wide open like she was halfway through arguing with someone in her dream."
    "The duvet had lost the fight completely and was bunched somewhere around her knees."
    think "Four years, and I still got whatever quarter of the bed she didn't need. I'd never once asked for it back."
    mc "Hey. [friend_name]'s awake. Which means we're officially late."
    gf "Mmhh... five more... hours."
    mc "He's texting the group now. He's escalating."
    $ lc_notice_end()

    scene cg ch01_d2_leia_waking
    with dissolve

    "She dragged a fist across her face and blinked up at me, eyes not quite on duty yet."
    gf "Mm... why are you all the way over there? Come back, you were warm."
    gf "It's supposed to be eleven-thirty. I negotiated eleven-thirty. He was there. You were there."
    mc "I'll tell him you said that."

    scene bg ch01_master_bedroom_curtains
    with dissolve
    $ cast(ryan="home", leia="camisole_panty")

    "I sat back down on the edge of the bed. She pulled half the duvet back over herself and looked at me like she'd just remembered something and hadn't decided yet whether to bring it up."

    if get_story_value("ch01_dream_response") == "grounded":
        "The dream still existed somewhere at the back of my mind, but daylight had put it back where it belonged."
    elif get_story_value("ch01_dream_response") == "curious":
        "The dream had lost its sharp edges by morning, though the uncomfortable question it left behind was still sitting there."
    elif get_story_value("ch01_dream_response") == "withdrew":
        "I had managed not to think about the dream again. Mostly. Keeping it there felt easier than examining it."

    # Day One echo: the upstairs talk before movie night (ch01_upstairs_response).
    # honest/liked = the loving path, so Ryan thanks her (out loud and in his head).
    if get_story_value("ch01_upstairs_response") == "honest":
        "She caught me watching her and smiled into the pillow."
        gf "You carried me up those stairs last night. Like a sack of laundry, and there was a step in my hip the whole way up, but you actually carried me."
        mc "You said badly was fine. I did exactly what I was told."
        gf "You did. Worst carry of my entire life. I loved it, I want that on record."
        mc "Hey. Thanks for last night. Upstairs. I said a pretty weird thing, and you just... hugged me."
        gf "It wasn't weird. You told me a thing. I like it when you tell me things."
        think "Four years, and she still made the hard stuff easier to say than it had any right to be."
    elif get_story_value("ch01_upstairs_response") == "liked":
        gf "I've been lying here thinking about our talk last night. The proper one."
        mc "Good thinking or bad thinking?"
        gf "Good. Mostly good. I keep replaying the bit where you actually said stuff, in real sentences, without me having to drag every word out of you."
        mc "You did drag a few out. But thank you. For making me do it, and for upstairs before that. I told you I didn't hate people noticing you, and you didn't look at me like I was a freak."
        gf "Oh, I freaked out. Internally. Very quietly. And then I decided I didn't hate it either, so."
        think "I'd half expected her to go looking for the catch. She'd checked my face, decided I meant it, and then held me to the talk instead of letting it slide. I didn't know what I'd done to get that lucky."
    elif get_story_value("ch01_upstairs_response") == "swallowed":
        "She was on her side of the bed, close enough to touch and not quite touching."
        gf "Are you still tired? Last night you said you were just tired."
        mc "No. I slept it off. I'm good."
        gf "Okay. Good."
        think "Last night she'd decided to believe me because I'd asked her to. This morning she was still being careful with me, and that was my doing."
    elif get_story_value("ch01_upstairs_response") == "snapped":
        "Over her shoulder, the dinner dress lay folded on the chair. Neatly. She never folds anything."
        if get_story_value("ch01_dream_response") == "withdrew":
            gf "Morning."
            "She said it carefully, the way you'd step around something on the floor in the dark. I let her."
        else:
            mc "Hey. What I said upstairs last night. The 'stay awake next time' thing. That was a crap thing to say."
            gf "It was kind of a crap thing to say."
            mc "Yeah. You were tired. You're allowed to be tired. I was just being— I don't know. Sorry."
            gf "Okay. Thank you. That's a lot better than the half a sentence you gave me in the dark."
            mc "Yeah. That one didn't really count."
            "She shifted half an inch closer, which for [girlfriend_name], after a fight, was practically a hug."

    # Day One continuity: Julian already sent every earned solo pool Capture to
    # Trip Group last night. Review that same inventory here instead of creating
    # a second photo-count/route state for the morning.
    $ d2_morning_pool_photos = ch01_pool_capture_assets()
    $ d2_morning_withdrew = get_story_value("ch01_dream_response") == "withdrew"

    if d2_morning_pool_photos:
        "[girlfriend_name] reached for her phone and opened the photos [friend_name] had sent the night before."
        gf "I still think he was way too pleased with himself, sending these at midnight like a proud dad, but..."
        gf "This one's actually not bad. Like, I'd let my mom see this one."

        $ renpy.scene()
        $ renpy.show("cg " + d2_morning_pool_photos[0])
        with dissolve

        gf "What do you think? Be honest. Actually, no, be nice first, then honest."

        if d2_morning_withdrew:
            "I looked at the photo. For a second, yesterday and the dream tried to occupy the same space in my head."
            mc "Yeah. It's nice."
            gf "...That's it?"
            mc "What? It is nice."
            gf "No, it's— yeah. Nothing. It is nice."
            "Her eyes returned to the phone before mine did."
        elif get_story_value("ch01_dream_response") == "curious":
            "She looked more comfortable in the photo than she had while [friend_name] was taking it."
            mc "You look really good. Comfortable, even."
            gf "Comfortable? I was dying. I was holding my stomach in the entire time."
            mc "Well, it doesn't look like it. You look confident."
            gf "I was trying so hard to look confident. That's the face of a woman trying very hard."
            mc "It worked, then."
        else:
            mc "I like it. You look happy in it."
            "She pulled the phone up until it hid most of her face."
            gf "You can't just say that so fast. You didn't even zoom in."
            mc "I don't need to zoom in. You're asking me if I like a photo of my girlfriend, babe. It's not a hard question."
            gf "That's actually a good answer. Annoyingly."

        if len(d2_morning_pool_photos) >= 2:
            "[girlfriend_name] swiped to the next photo."
            $ renpy.scene()
            $ renpy.show("cg " + d2_morning_pool_photos[1])
            with dissolve

            if d2_morning_withdrew:
                "She studied it this time, no longer asking me to judge it."
            elif get_story_value("ch01_dream_response") == "curious":
                gf "Wait, I actually like this one more. My arm's doing a weird thing, but my face is better."
                mc "You look more relaxed in this one."
                gf "Maybe I was getting used to it? By then I'd kind of stopped thinking about the camera."
                "The admission seemed to surprise her slightly less than it surprised me."
            else:
                gf "Wait, no, this one might be better. Is this one better?"
                mc "You're going to make me rank them, aren't you?"
                gf "Obviously. Top three, with reasons."

        if len(d2_morning_pool_photos) >= 3:
            "Her thumb moved again."
            $ renpy.scene()
            $ renpy.show("cg " + d2_morning_pool_photos[2])
            with dissolve

            if d2_morning_withdrew:
                "Another good photo. Another moment where she seemed more interested in sharing it with me than I was capable of being."
                "[girlfriend_name] stayed on it for a second, then locked the phone without asking."
            elif get_story_value("ch01_dream_response") == "curious":
                gf "I definitely wasn't this comfortable at the start. Not even close."
                mc "No. You really weren't."
                gf "Is that a bad thing?"
                "She asked it plainly, like she genuinely wanted to know."
                mc "I don't know yet. I mean, I don't think so. I just don't know what it is yet."
                gf "That's honest, at least. I'll take honest."
            else:
                gf "That one. That's my favorite, final answer."
                mc "I thought the last one was your favorite."
                gf "I'm allowed to change my mind, it's my face."
                mc "In the last four seconds?"
                gf "That's called growth, babe."
    else:
        # No solo captures: the Day 1 photoshoot was stopped or rushed, and
        # Julian deleted them. The group selfie still exists.
        "[girlfriend_name] reached for her phone and scrolled back to yesterday's group selfie."
        $ d2_morning_group_selfie = ("ch01_photo_group_blue" if get_story_value("ch01_pool_outfit", "pool_conservative") == "pool_bolder" else "ch01_photo_group_white")
        $ renpy.scene()
        $ renpy.show("cg " + d2_morning_group_selfie)
        with dissolve

        gf "At least we still have this one. I'm the one holding the phone, so I've got, like, an extra chin, but it survived."
        if d2_morning_withdrew:
            mc "Yeah. It's a good one."
            gf "You barely looked."
            mc "I looked. It's a good one."
            "She locked the phone after a second and didn't ask again."
        else:
            mc "You look happy in it."
            gf "I was trying not to drop my phone in the pool. That's concentration, not happiness."
            mc "Still looks happy."
            gf "I'll take it. It's the only decent one that survived yesterday."

    scene bg ch01_master_bedroom_curtains  # Day 2 morning: day art (darryn)
    with dissolve
    $ lc_phone_clear_story_time()
    $ cast(ryan="home", leia="camisole_panty")

    # Subtle Day Two tint (lc_leia_tint): shy by default; the stat furthest over its bar colours the line.
    $ d2_tint = lc_leia_tint(ch01_d2_route_lane())
    if d2_tint == "love":
        gf "You were a menace last night, by the way. During the movie. My menace, but still a menace."
    elif d2_tint == "temptation":
        gf "You were kind of a menace last night, by the way. During the movie."
        "She said it to her phone, thumb still scrolling, like it had only just crossed her mind."
    else:
        gf "You were kind of a menace last night, you know. During the movie. I didn't forget."
    mc "Good morning to you too."
    gf "I'm serious. I spent half that movie trying to act normal."
    mc "You were the one who kept checking if he was looking. Sorry. You were, a bit."

    if lc_stat("exhibitionism") < LC_T["d2_morning_unsure"]:
        gf "I was checking that he wasn't! That's a completely different direction of checking."
    elif lc_stat("exhibitionism") < LC_T["d2_morning_bold"]:
        gf "That is not the same thing, and you know it isn't."
        mc "Sure. Totally different."
        gf "It isn't! Stop saying it like that."
    else:
        gf "You have no evidence of that."
        mc "I was sitting right next to you. I have eyes."
        gf "Eyes are circumstantial."

    # Day One echo: the scene 28 talk about movie night (ch01_alone_movie_response).
    if get_story_value("ch01_alone_movie_response") == "apologized":
        gf "You did check on me after, though. When he went to bed. That was really sweet. I'm still saying menace."
    elif get_story_value("ch01_alone_movie_response") == "curious":
        gf "So did you figure it out? Last night you said you were still figuring out how I reacted."
        mc "I've had seven hours. Most of them asleep."
        gf "Well, me neither. For the record."
    elif get_story_value("ch01_alone_movie_response") == "open":
        gf "And don't think I forgot the other thing. The 'I liked watching you get nervous' thing."
        mc "You said 'a little.'"
        gf "I said a little! I was tired! A little is still a little, it doesn't grow overnight."
    elif get_story_value("ch01_alone_movie_response") == "dismissed":
        gf "I know, I know. It was just messing around."
        "She said it exactly the way I'd said it last night, flat and quick, and looked back at her phone."
        think "It sounded worse in her mouth than it had in mine."

    $ d2_morning_reassure_text = format_choice("ch01_d2_morning_reassure", "Relax. I was only teasing you.")
    $ d2_morning_tease_text = format_choice("ch01_d2_morning_tease", "I liked seeing you curious.")
    $ d2_morning_dismiss_text = format_choice("ch01_d2_morning_dismiss", "It wasn't a big deal.")

    menu:
        "[d2_morning_reassure_text]":
            $ apply_choice("ch01_d2_morning_reassure")
            mc "Relax. I was only teasing you."
            gf "I know. I just like hearing you say it."
            "She moved closer and rested her forehead briefly against my shoulder."

        "[d2_morning_tease_text]":
            $ apply_choice("ch01_d2_morning_tease")
            mc "I liked seeing you curious."
            gf "Curious? Curious about what?"
            mc "I don't know. That's kind of the point. You looked like you were figuring something out."
            gf "You're impossible. You know that? Completely impossible."
            "She was smiling when she said it."

        "[d2_morning_dismiss_text]":
            $ apply_choice("ch01_d2_morning_dismiss")
            mc "It wasn't a big deal."
            gf "Right."
            "The subject died more quickly than it needed to."

    "For a moment neither of us said anything."

    if get_story_value("ch01_dream_response") == "withdrew":
        "[girlfriend_name] shifted closer anyway, her shoulder settling against mine."
        "I felt the invitation in it. I just didn't quite know what to do with it."
        gf "Hey. You okay? You've got your thinking face on again."
        mc "Yeah. Just didn't sleep that well."
        "She watched me for another second, then let me have the answer."
    elif get_story_value("ch01_dream_response") == "curious":
        "[girlfriend_name] shifted closer, warm and familiar against my side."
        think "She was right here, warm and normal. That should have made the dream easier to dismiss. Somehow it only made my reaction to it stranger."
    else:
        "[girlfriend_name] shifted closer and stole the last corner of duvet I still technically owned."
        mc "Seriously? That was my last corner."
        gf "You weren't using it properly."
        mc "It was on me. That's how you use a duvet."
        gf "That's not using it, babe. That's just storing it on you."

    "A few minutes later, [girlfriend_name] finally pushed herself out of bed and stretched."
    gf "I'm showering before [friend_name] sends a second text. The second one's always worse than 'Bro wake up.'"
    mc "He's probably been up for an hour already. Standing in front of the fridge."
    gf "He's always awake when there's food. It's like a sixth sense with him."

    "She disappeared toward the bathroom, leaving me with a quiet room and far too much time inside my own head."
    $ cast_remove("leia")

    if get_story_value("ch01_dream_response") == "withdrew":
        "I picked up my phone mostly so I would have something else to look at."
    elif get_story_value("ch01_dream_response") == "curious":
        "I caught myself thinking about the photos again, and about how quickly [girlfriend_name] had gone from awkward to comfortable in front of the camera."
        think "It wasn't jealousy. That was what made it harder to file away."
    else:
        "By the time I checked my phone, the dream had already started to feel like something that belonged to the night before."

    $ cast()
    $ set_story_flag("ch01_d2_scene_01_complete")
    jump ch01_day2_scene_02_breakfast


label ch01_day2_scene_02_breakfast:

    $ enter_cinematic_mode()
    scene cg ch01_d2_breakfast_01
    with fade
    $ lc_notice_begin("d2_notice_breakfast_smile")  # Things Ryan noticed (docs/NOTICES.md)
    "Breakfast started with the kind of easy rhythm we'd found by the end of yesterday."

    friend "Oh, look who's alive. I was about to send a search party. I had a whole message drafted and everything."
    gf "Mostly alive. Your couch did something to my back, I think."
    friend "That's because you spent half the movie rearranging yourself every thirty seconds. I counted. Well, I stopped counting, but I started."

    "[girlfriend_name]'s eyes moved directly to mine."

    mc "Maybe your movie was making her uncomfortable. Did you think about that?"
    friend "My movie was art. It won awards. Small ones. Online ones, but still."
    gf "Your movie had a shark driving a speedboat, [friend_name]. Like, at the wheel."
    friend "And did anyone look away? No. Because it was art."

    "[friend_name] grinned over his mug while [girlfriend_name] lifted hers at him. The movie argument wasn't going to survive breakfast."

    friend "So what does everyone want to do today? I'm open to anything, honestly. Within reason."
    gf "Something that doesn't involve me wearing dinner again, ideally."
    friend "That was one accident. And it wasn't even your drink, technically."
    gf "One very wet accident. That dress is never recovering."
    mc "You did, though. Recover, I mean."
    gf "Eventually."

    "[friend_name] pointed at the spread between us."
    friend "Okay, hear me out. We eat first, and then we decide later. That's a plan."
    gf "That's not a plan, that's just breakfast."
    friend "It's worked for me for twenty-seven years. I'm not changing the system now."

    if get_story_value("ch01_dream_response") == "withdrew":
        "My attention drifted somewhere between the table and the remains of the dream."
        gf "[player_name]?"
        mc "Hm?"
        gf "Coffee?"
        "She was holding the pot slightly toward me."
        gf "That's the second time I've asked, by the way."
        mc "Oh. Yeah. Thanks."
        "She poured it without commenting, but I caught the brief look she gave me before turning back to [friend_name]."
    elif get_story_value("ch01_dream_response") == "curious":
        gf "Coffee?"
        mc "Please. A lot of it."
        "She poured mine before her own without thinking about it."
        "It was small and automatic, the kind of gesture four years turns into, and neither of us noticed it anymore."
    else:
        gf "Coffee?"
        mc "Only if you're admitting you stole the duvet."
        gf "I admit nothing. The duvet came to me."
        "She poured it anyway."

    $ lc_notice_end()
    $ set_story_flag("ch01_d2_scene_02_complete")
    jump ch01_day2_scene_03_maya_message


label ch01_day2_scene_03_maya_message:

    "My phone buzzed beside the coffee."

    python:
        phone_add_message(
            "maya",
            "maya",
            text="You people alive? I'm near the resort around lunch. Still meeting?",
            message_id="ch01_d2_maya_lunch_checkin",
            mark_unread=True,
            notify=True,
            notification_title="Maya",
        )

    $ enter_cinematic_mode()
    scene cg ch01_d2_breakfast_02
    with dissolve
    $ lc_pov_begin("d2_breakfast_julian")
    # Restore the phone HUD for the optional reply, but keep Breakfast_02
    # behind the conversation instead of cutting to the placeholder card.
    $ exit_cinematic_mode()
    $ lc_phone_hud_on_cg = True

    "Maya's name appeared in the notification."
    "[girlfriend_name] saw it before I put the phone down."

    gf "Oh. Maya."
    mc "What? What's that face?"
    gf "Nothing! No face. That's just my face. It's a nice name."
    friend "That was the loudest 'nothing' I've ever heard, and I've known you two for four years."

    python:
        phone_offer_reply("maya", "ch01_d2_maya_lunch_reply", [
            {"id": "alive", "text": "Alive. Barely. Lunch works, I'll send you where we are.",
             "followups": [("maya", "Look at you, being organized 👍")]},
            {"id": "leia", "text": "[girlfriend_name] says hi.",
             "followups": [("maya", "Hi [girlfriend_name]! 👋")]},
            {"id": "buying", "text": "Depends. Are you buying?",
             "followups": [("maya", "In your dreams. See you at lunch.")]},
        ], "alive")

    # Leia's "Is she pretty?" beat (restored from the original scene 3). The
    # loudest-'nothing' joke already landed above, so the lead-in goes straight
    # to her question instead of repeating it.
    "[girlfriend_name] waited until I'd set the phone face-down again."

    gf "So that's the Maya I've heard about."
    mc "You've heard about her."
    gf "Mm."
    "She turned her cup a slow quarter-turn, trying and failing to make the next question sound casual."
    gf "Is she pretty?"

    $ d2_maya_reassure_text = format_choice("ch01_d2_maya_reassure", "You're the one I'm here with.")
    $ d2_maya_tease_jealousy_text = format_choice("ch01_d2_maya_tease_jealousy", "Are you jealous?")
    $ d2_maya_honest_text = format_choice("ch01_d2_maya_open_honest", "Yeah. She's attractive. She's also just my friend.")

    menu:
        "[d2_maya_reassure_text]":
            $ apply_choice("ch01_d2_maya_reassure")
            mc "You're the one I'm here with."
            gf "That wasn't technically the question."
            mc "It was the question underneath the question."
            "The corner of her mouth gave her away."
            gf "Acceptable answer."

        "[d2_maya_tease_jealousy_text]":
            $ apply_choice("ch01_d2_maya_tease_jealousy")
            mc "Are you jealous?"
            gf "No."
            mc "That was fast."
            gf "Because the answer is no."
            friend "Very convincing."
            "[girlfriend_name] went pink and lifted her cup in front of her face."
            gf "You weren't even in this conversation, [friend_name]. Drink your coffee."

        "[d2_maya_honest_text]":
            $ apply_choice("ch01_d2_maya_open_honest")
            mc "Yeah. She's attractive. She's also just my friend."
            "[girlfriend_name] considered that for a second."
            gf "Okay."
            mc "Okay?"
            gf "I asked. You answered."
            "She'd accepted it a little too easily, like she had already decided how she was going to take the answer."

    if get_story_value("ch01_dream_response") == "withdrew":
        "Her answer should have reassured me. Instead, I found myself wondering whether I had been offering her the same honesty since I woke up."

    $ set_story_flag("ch01_d2_maya_meetup_confirmed")
    $ lc_pov_end()
    jump ch01_day2_scene_04_jealousy_callback


label ch01_day2_scene_04_jealousy_callback:

    "The subject should have ended there, but [girlfriend_name]'s curiosity survived breakfast."

    if get_story_value("ch01_female_friend_response") == "teased_jealousy":
        gf "And for the record, I'm still not jealous. I'm just asking things. Normally."
        mc "I didn't say anything."
        gf "Your face said something. Your face is very chatty this morning."
    elif get_story_value("ch01_female_friend_response") == "asserted_boundary":
        gf "I'm glad she's meeting all of us, by the way. Properly. Not just as a name on your phone."
        mc "Me too. She's going to like you."
        gf "Good. I mean, obviously she is. But good."
    else:
        gf "I am curious to finally meet her, though. You talk about her, like, a normal amount, which is somehow more suspicious."
        mc "That's allowed. I'm curious what she makes of you, too."
        gf "Wait, so she's going to be reviewing me? Great. That's great. No pressure at all."

    "Whatever tiny tension had been there stayed small enough to joke about."

    # These are reactions to the conversation, not a reward for using the
    # optional phone reply. No line assumes Ryan sent a message.
    $ lc_phone_hud_on_cg = False
    $ enter_cinematic_mode()
    scene cg ch01_d2_breakfast_03
    with dissolve
    "[girlfriend_name]'s expression eased as the conversation moved on."
    scene cg ch01_d2_breakfast_04
    with dissolve
    "She glanced back at me. [friend_name], caught watching our faces, looked away."

    $ set_story_flag("ch01_d2_scene_04_complete")
    jump ch01_day2_scene_05_meet_maya


label ch01_day2_scene_05_meet_maya:

    $ enter_cinematic_mode()
    scene cg ch01_d2_maya_reveal
    with fade
    "By the time we reached the café, Maya was already waiting at the open doorway. A small day bag hung from one shoulder, looking more prepared for an island afternoon than the rest of us were."

    maya "[player_name]! Wait, you're tan? Since when do you tan?"
    mc "Since yesterday, apparently. Hey, Maya."

    $ exit_cinematic_mode()
    scene bg ch01_d2_cafe
    with dissolve
    # Café outfits only; keep Maya off-screen until after her doorway reveal.
    # Julian's café/mall CGs show the black button-up (evening / BASE_BlackShirt).
    # Leia's café/mall CGs show the white off-shoulder top and denim shorts
    # (casual / PRO/Base_Casual.png).
    $ cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")
    "She hugged me the way people do when they've known you too long to bother being polite about it."
    "[girlfriend_name] watched the greeting carefully."

    # Day One echo: the scene 29 talk (ch01_private_attention_response).
    if get_story_value("ch01_private_attention_response") == "jealous":
        "When Maya let go of me, [girlfriend_name] leaned in close enough that only I could hear."
        gf "Okay. I get it now. The 'a little jealous' thing from last night. I'm a little jealous."
        mc "Only a little?"
        gf "Don't use my own lines on me. I'll be fine in five minutes."
    elif get_story_value("ch01_private_attention_response") == "claimed":
        "When Maya let go of me, [girlfriend_name] slid her hand into mine and kept it there."
        gf "Just so we're clear, the 'mine' thing goes both ways."
        mc "Yeah. Obviously."
        gf "Good. I'm not complaining. I'm just saying."
    elif get_story_value("ch01_private_attention_response") == "open":
        "[girlfriend_name] caught me watching her instead of Maya."
        gf "Don't do the face. The 'I like seeing you get attention' face. She hasn't even said hi to me yet."
        mc "She's about to."
        gf "Still weird, babe. Not bad weird. But weird."
    elif get_story_value("ch01_private_attention_response") == "indifferent":
        "Usually, after something like that, she'd look at me to see what I thought. This time she didn't."

    maya "And you're [girlfriend_name]. Finally. Hi! Sorry, I feel like I already know you."
    gf "Hi. Sorry, hi. Finally? How long have you been waiting for this?"
    maya "Years. I've been hearing about you for years. He talks about you like you invented coffee."

    "[girlfriend_name] slowly turned toward me."

    gf "Years? You talk about me? To people?"
    mc "I mean, apparently. I didn't think it was that much."
    maya "Constantly. Every time we got lunch. It's honestly exhausting."
    friend "Thank you. Finally someone else gets it. I've been suffering through this alone for four years."

    "Maya introduced herself to [friend_name] and, within thirty seconds, had already made fun of his sunglasses."

    maya "Those sunglasses cost more than my flight. Don't lie to me. They do, don't they?"
    friend "They're... they're just sunglasses. They were on sale. Kind of."
    maya "He went red. That's a yes."

    "We ordered drinks and found a table near the open side of the café."
    $ enter_cinematic_mode()
    scene cg ch01_d2_maya_cafe_01
    with dissolve
    maya "So. Four years. Tell me everything. No, wait, tell me the bad stuff first, he already told me the good stuff."
    "[girlfriend_name] glanced at me before she answered."
    gf "Um. Bad stuff. There's... probably some? I don't really know where I'd start."
    maya "Start here. I need to know one thing."
    gf "That sounds threatening. Okay. Go."
    maya "Has he always taken twenty minutes to decide what to eat?"
    gf "Oh my God. Yes. Every single time."
    mc "This is character assassination. I'd like that on the record."
    gf "He reads the entire menu, picks something, changes his mind, asks the waiter what's good, and then orders the first thing anyway."
    maya "He used to do that at lunch! With a sandwich menu. Six sandwiches."
    gf "He still does it at dinner. He did it last night."

    "They looked at each other like two people who'd been studying the same flaw from opposite ends for years."
    mc "I regret this meeting already. Can we go back to before you two met?"

    $ exit_cinematic_mode()
    scene bg ch01_d2_cafe
    with dissolve
    $ cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")
    $ face("maya", "smile")
    maya "Good. That means it's going well. That's how you know."

    $ set_story_flag("ch01_d2_scene_05_complete")
    jump ch01_day2_scene_06_jealousy_test


label ch01_day2_scene_06_jealousy_test:

    "Maya and I fell briefly into the shorthand of old stories and mutual friends."
    "[girlfriend_name] listened rather than interrupting. The quiet was subtle enough that Maya did not notice. I did."

    $ d2_maya_include_text = format_choice("ch01_d2_maya_include", ('Pull ' + girlfriend_name + ' into the conversation.'))
    $ d2_maya_catchup_text = format_choice("ch01_d2_maya_catchup", "Keep catching up normally.")
    $ d2_maya_dismiss_text = format_choice("ch01_d2_maya_dismiss_leia", "Lose track of time in the old stories.")

    menu:
        "[d2_maya_include_text]":
            $ apply_choice("ch01_d2_maya_include")
            mc "Wait, tell her the airport story. She's never heard the airport story."
            maya "No, you tell her, because you're the one who caused it. I was an innocent bystander."
            gf "Now I need to hear this. What did you do at an airport?"
            "[girlfriend_name] shifted closer to the conversation instead of sitting outside it."

        "[d2_maya_catchup_text]":
            $ apply_choice("ch01_d2_maya_catchup")
            "I kept catching up with Maya. [girlfriend_name] stayed quiet for another minute before Maya turned to her directly."

        "[d2_maya_dismiss_text]":
            $ apply_choice("ch01_d2_maya_dismiss_leia")
            "One old story turned into three. I didn't notice [girlfriend_name] had gone quiet until she looked at me, and by then Maya was already halfway into the next one."
            "By the time Maya turned the conversation toward her, [girlfriend_name] was smiling again, but the delay had registered."

    "Maya eventually rescued me from my own old stories by turning to [girlfriend_name]."

    maya "Okay, enough [player_name] history. Tell me something about you that he wouldn't think to tell me."
    gf "Oh no. That's a dangerous amount of freedom. Okay. Um."
    mc "Hey. I tell people things about you."
    maya "You tell people the boring things. Overruled. Go, [girlfriend_name]."

    if get_story_value("ch01_dream_response") == "withdrew":
        "[girlfriend_name] glanced at me before answering. It was brief, but after the morning we'd had, I noticed it."
    else:
        "[girlfriend_name] thought about it like she was picking one card out of a whole hand."

    gf "I hate folding laundry."
    maya "That's it? That's your secret?"
    gf "I mean I really hate it. I will live out of a clean laundry basket for a week."
    mc "Two weeks. I've seen two weeks."
    gf "Nobody asked for your testimony, babe."
    maya "No, that's perfect. That's so human. Okay, keep going, what else?"

    "The conversation stopped being mine and Maya's reunion after that."

    $ set_story_flag("ch01_d2_scene_06_complete")
    jump ch01_day2_scene_07_leia_maya_click


label ch01_day2_scene_07_leia_maya_click:

    "The awkwardness lasted considerably less time than I'd expected."
    "Maya asked [girlfriend_name] one question about the resort. [girlfriend_name] answered with a story. One story became three."

    maya "Wait, wait. You actually like traveling with him? On purpose?"
    gf "Most of the time? I'd say eighty percent."
    mc "Eighty?"
    gf "Airports bring out the worst in you, babe. You know they do."
    maya "Thank you! Thank you."
    gf "He gets convinced every line is the wrong line, and then he moves us, and then that line's the wrong line too."
    maya "THANK you. Somebody finally said it."
    mc "I have instincts. Sometimes the other line is faster."
    maya "No, you have anxiety with luggage. That's different from instincts."

    "[girlfriend_name] laughed hard enough to cover her mouth."
    $ enter_cinematic_mode()
    scene cg ch01_d2_maya_cafe_02
    with dissolve
    "Whatever caution she'd brought into meeting Maya was disappearing quickly."

    maya "What about you? Holiday person or itinerary person?"
    gf "I like having a plan. Like, a loose plan. A loose plan with times on it."
    mc "She has a spreadsheet. With tabs."
    gf "One tab! And a spreadsheet is just a plan that respects you."
    maya "We're going to get along. I don't have a spreadsheet, but I respect a spreadsheet."

    "The conversation wandered from travel to food, then clothes, then the photos on [girlfriend_name]'s phone."

    maya "Wait, you took this one? This is good."
    gf "Yes! Why does everyone sound so surprised?"
    maya "Because [player_name] told me he was the photographer in this relationship."
    gf "[player_name] says a lot of things."
    mc "I'm sitting right here, you know."
    maya "We know. It's more fun this way."

    maya "You photograph well, by the way."
    gf "Only when I forget someone's taking one. The second I know, I go all weird."
    maya "That's everybody. The second people see a camera they start manually operating their face."
    gf "That's exactly what I do! I manually operate my face!"
    maya "So next time, don't pose. Just talk to whoever's holding the phone."

    $ exit_cinematic_mode()
    scene bg ch01_d2_cafe
    with dissolve
    $ cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")
    # Day 1 photo continuity: Julian deleted the solo pool Captures on the early-stop
    # photoshoot (ch01_photo_outcome "stopped"), so ch01_pool_capture_count is 0 and the
    # morning showed only the group selfie. Same value and default as ch01_pool_capture_assets().
    if int(get_story_value("ch01_pool_capture_count", 1)) > 0:
        "[girlfriend_name] scrolled back to one of yesterday's pool photos."
        gf "I did get better eventually, though. Look, by the end I wasn't even posing."
        maya "See? This one's really good. Who took this one?"
        gf "[friend_name] did."
        maya "Ugh. Annoying. I was really hoping I could insult his photography too."
        maya "Seriously, though. [player_name], you've had four years. Where's your version of this?"
        gf "He has about four hundred photos of me squinting at a menu."
        friend "In my defense, she'd stopped posing by then. She was mostly looking past me at [player_name]. I just pressed the button."
        gf "Well, it's going on my lock screen. Don't look at me like that, it's the best one of me on the whole trip."
        "She did it right there at the table, then turned the phone around to show me."
        # Ryan's thoughts (B3): the Day One photo thought, if he kept it. Otherwise today's line.
        if lc_thought_kept("ch01_d1") == "d1_photo_shoot":
            think "Last night I'd told myself I should learn how to hold a phone properly. Today [friend_name]'s photo was on her lock screen. At least I was the one she'd been looking at."
        else:
            think "Yesterday I'd been the photographer in this relationship. Apparently that had a shelf life. At least I was the one she'd been looking at."
    else:
        "[girlfriend_name] scrolled back to yesterday's group selfie instead. It was the only pool photo she still had."
        gf "This is all that's left from the pool. I'm the one holding the phone, so it's mostly my arm and everybody's foreheads."
        maya "Foreheads are underrated. You all look like you actually like each other, that's the hard part."
        maya "Seriously, though. [player_name], you've had four years. Where's your version of this?"
        gf "He has about four hundred photos of me squinting at a menu."
        think "Four years as the photographer in this relationship, and my best work was apparently a menu and a squint."

    "[friend_name] looked at me over his drink."

    friend "You know you've completely lost control of this, right? This is their table now. We're just sitting at it."
    mc "Yeah. I think introducing them was a mistake."
    gf "Too late. I like her, she's staying."
    maya "Same. I'm keeping her."

    "It was said jokingly, but [girlfriend_name]'s posture had changed. She had stopped being the girlfriend meeting my friend and was just talking to Maya, on her own terms."

    # Who saw what (B1): only when this save opened Julian's breakfast view (lc_pov_seen_in_save,
    # save-local). Not opened, or an old save: nothing extra plays. Flavor only, no stats.
    if lc_pov_seen_in_save("d2_breakfast_julian"):
        $ d2_witness_lane = ch01_d2_route_lane()
        "[girlfriend_name] knelt up on her chair and leaned all the way across the table to show Maya another photo."
        "[friend_name]'s eyes went with her. They came back about half a second later than they should have, and went straight into his glass."
        friend "These are really good drinks, by the way. Has everyone tried theirs? I'm just, um. I'm really enjoying mine."
        think "That was twice today. At breakfast I'd caught him watching us too, and he'd looked away with exactly the same face."
        "[girlfriend_name] sat back down and caught us both at it: him studying his ice, me studying him."
        if d2_witness_lane == "exhibitionism":
            "She went a little pink and tugged the hem of her shorts down. Then she checked my face, and whatever she found there made her smile into her straw."
        elif d2_witness_lane == "ntr_risk":
            "For a second she looked at me like she was waiting for me to say something. I didn't, so she went back to Maya."
        else:
            gf "What? Why are you two being weird?"
            "She looked from him to me, worked it out about a second later, and burst out laughing."
            gf "Oh my God. Babe. You've got the guard dog face on."
            mc "I don't have a guard dog face."
            "She scooted her chair over until it bumped mine and leaned her whole weight against my shoulder."
            gf "You do, and it's really cute. I'm right here, okay? Right here, leaning on you, being all yours. Nobody else gets a vote."
            "She stayed there for the rest of her drink, and I stopped keeping track of where anybody else was looking."

    $ set_story_value("ch01_d2_leia_maya_comfort", 2)
    $ set_story_flag("ch01_d2_scene_07_complete")
    jump ch01_day2_scene_08_maya_julian


label ch01_day2_scene_08_maya_julian:

    "Maya's attention eventually shifted to [friend_name]."

    maya "So you're the rich one. [player_name] told me."
    friend "He— wow. Okay. It's not really— it's my family, it's not me. I don't do anything. The villa's just a booking, anyone could've— can we look at the menu? I think I'm getting the fish. Is anyone else getting the fish?"
    maya "No, relax, the sunglasses are your personality. The money's just supporting cast."

    "[friend_name] didn't laugh it off. He went red, took his sunglasses off, put them straight back on, and read the menu like there was going to be a test on it."
    think "I'd told her that once, years ago, and forgotten about it. I should have known Maya would keep it."
    "[girlfriend_name] leaned toward me."

    gf "They get along. Like, really get along."
    mc "She only insults people she likes. I'm going to owe him a drink for that one, though."
    gf "That explains you."

    "A bee wandered close to the table."
    "[friend_name] stopped mid-sentence and leaned sharply away from it."

    maya "...Are you scared of bees?"
    friend "No. No. Is it gone? It's gone, right?"
    maya "You moved six inches without using your feet."
    friend "I respect bees. I just respect them from a reasonable distance. Is that a crime?"
    gf "Oh my God, you're actually scared of bees."

    "The bee wandered off a second later, but Maya and [girlfriend_name] had clearly filed the whole thing away for later."

    $ set_story_flag("ch01_d2_julian_bee_fear_seeded")
    $ set_story_flag("ch01_d2_scene_08_complete")
    jump ch01_day2_scene_09_photo_walk


label ch01_day2_scene_09_photo_walk:

    scene bg ch01_d2_island_day
    with dissolve
    # No walk/pool/boutique outfits for Maya yet: avoid carrying the café cast.
    $ cast()

    "After lunch, Maya turned a walk through the island shops into a photography project."

    "There was no urgency to it. We drifted between shaded storefronts, stopped whenever somebody saw something interesting, and argued about whether [friend_name] needed another pair of sunglasses."

    friend "They're different, though. These ones are for driving."
    maya "They're black. They're the same black."
    friend "The frames are completely different. Look at the hinge. Nobody ever looks at the hinge."
    gf "The hinge is also black, [friend_name]."
    friend "Wow. Four years, [girlfriend_name]. I expected more from you."
    gf "Four years of watching you buy the same sunglasses. I'm allowed an opinion."
    friend "This is betrayal. I'm buying them anyway."

    "Maya had started walking beside [girlfriend_name] without anybody arranging it."
    "Every few minutes one of them would stop to point something out, and the rest of us would realize we'd walked several steps ahead."

    if get_story_value("ch01_dream_response") == "withdrew":
        "Watching [girlfriend_name] settle so easily into somebody else's company should have been reassuring."
        think "And it had taken somebody else about five minutes to give her the attention I'd been holding back all morning."
    elif get_story_value("ch01_dream_response") == "curious":
        "[girlfriend_name] seemed lighter around Maya already. Less concerned with how she was being perceived, more willing to just react."
    else:
        "Seeing [girlfriend_name] relax around Maya removed the last trace of tension from breakfast."

    # Selfies (darryn 2026-11-19): Leia + Maya first (MayaLeiaSelfie_01, Maya holds the phone),
    # then Julian brings up the Trip Group picture, Maya finds out she isn't in the group, and
    # all four take the new group picture (GroupSelfie_01, Ryan holds the phone).
    maya "Okay. Before anything else. You, me, selfie."
    "She didn't wait for an answer. She hooked an arm around [girlfriend_name], held her phone out at arm's length and pulled her in until their heads touched."
    gf "Wait, I'm not ready, my hair's doing a thing—"
    maya "Your hair is perfect. Smile like I just said something rude."
    "[girlfriend_name] laughed, and Maya took it right then."
    $ lc_sfx("camera_shutter")

    $ enter_cinematic_mode()
    scene cg ch01_d2_photo_leia_maya
    with dissolve

    maya "See? That's the one. You stopped thinking about the camera."
    gf "Easy for you to say, you look like that in every photo."
    maya "Correct. I'm extremely photogenic. It's a curse."
    gf "You made me laugh on purpose, though. That's cheating."
    maya "That's not cheating, that's technique. You owe me photography credit now."
    gf "Absolutely not. I'm not crediting you."

    $ exit_cinematic_mode()
    scene bg ch01_d2_island_day
    with dissolve

    friend "Okay, that one's actually good. That reminds me, we should update the Trip Group picture. It's still the three of us at the pool yesterday."
    maya "...Sorry. The what?"
    friend "The Trip Group. The group chat. For the trip."
    maya "You have a trip group? And I'm not in it?"
    mc "You've been here for one lunch."
    maya "One lunch, and I'm already a better member than all three of you. Wow. Okay. I see how it is."
    gf "Oh my God, she's right, though. Add her! [friend_name], add her right now."
    friend "I'm adding her! I'm adding her. Give me a second, I have to find the button."
    maya "And we're taking a new picture for it. All four of us, right now, or it doesn't count."
    mc "I've got the longest arms. Everyone get in."
    "I held my phone up. Maya pulled [girlfriend_name] in under my arm, and [friend_name] squeezed in behind them with his sunglasses still on."
    $ lc_sfx("camera_shutter")

    $ enter_cinematic_mode()
    scene cg ch01_d2_photo_group
    with dissolve

    maya "Okay, that's so cute. Look at us."
    gf "[friend_name], you kept your sunglasses on."
    friend "Strategic. Nobody can prove I blinked."
    maya "Coward. It's perfect, though. That's the group picture. Send it."

    $ exit_cinematic_mode()
    scene bg ch01_d2_island_day
    with dissolve

    "I sent it to the group, and [friend_name] finally found the button."
    $ phone_group_maya_member = True
    $ phone_add_message("group", "system", text=friend_name + " added Maya to the group.", message_id="ch01_trip_group_maya_added", mark_unread=False)
    $ phone_group_avatar_stage = "four"
    $ phone_add_message("group", "system", text=friend_name + " changed the group picture.", message_id="ch01_trip_group_four_photo", mark_unread=False)
    $ phone_add_message("group", "maya", text="First post as an official member. You're welcome.", message_id="ch01_trip_group_maya_first_post", attachment_id="ch01_d2_leia_maya_selfie", attachment_label=girlfriend_name + " and Maya", mark_unread=False)
    "Maya's first message in the group was the selfie of her and [girlfriend_name], obviously."
    gf "Obviously."

    maya "And the group one's going on [LC_FEED_APP_NAME]. A photo this good doesn't get to live in a group chat."
    "She was already typing a caption with one thumb."
    maya "Wait. [player_name], you're not even on [LC_FEED_APP_NAME], are you? I just tried to tag you and you don't exist."
    mc "I've never really needed it."
    maya "Nobody needs it, that's not the point. Give me your phone, I'm doing this for you whether you like it or not."
    gf "She did mine at lunch while she was going through my photos. I didn't even get a say, babe, so just hand it over."
    "I handed it over before I'd really decided to. She had the app installed, an account made and herself followed in about the time it took [friend_name] to pay for his sunglasses."
    maya "There. Now you follow me, so you'll see my posts. Liking them is mandatory."
    # Feed app intro (systems/feed.rpy, docs/FEED.md): the app joins Ryan's home grid with
    # Maya's post. Old saves already past this point keep a phone without the app.
    # 14:10 = after lunch (breakfast after 11, then the café); the post is stamped with it.
    $ lc_phone_set_story_time("14:10")
    $ lc_feed_install()
    $ lc_feed_release("d2_maya_group_photo")
    "My phone buzzed in my hand the second she gave it back. Maya had already posted."

    # The pair photos ("complete the set") were cut (darryn 2026-11-19): the walk is the Leia + Maya
    # selfie and the Trip Group selfie only.
    $ set_story_flag("ch01_d2_photo_group")

    $ lc_phone_clear_story_time()
    jump ch01_day2_scene_10_leia_maya_photo


label ch01_day2_scene_10_leia_maya_photo:

    # The Leia + Maya selfie itself now plays in scene 09, before the group picture.
    "[girlfriend_name] had the selfie of her and Maya open on her phone again before we'd even reached the next shop."
    gf "I'm actually keeping this one. Don't tell her."
    mc "She's standing right there."
    maya "I heard that! Credit. I want credit."
    "[girlfriend_name] saved it anyway, still smiling."

    $ set_story_flag("ch01_d2_photo_leia_maya")
    $ set_story_flag("ch01_d2_scene_10_complete")
    jump ch01_day2_scene_11_missing_pair


label ch01_day2_scene_11_missing_pair:

    # Cut (darryn 2026-11-19): the "we're missing one" pair photo and its choice. The label stays
    # so a save made inside it still loads; it goes straight on to the mall.
    $ set_story_flag("ch01_d2_scene_11_complete")
    jump ch01_day2_scene_11b_boutique


label ch01_day2_scene_11b_boutique:

    friend "Before we head back, can we stop for a second? I need a shirt. The one I brought got sunscreen all down the front."
    maya "You're wearing a shirt. You own, like, twelve versions of that exact shirt, I can tell."
    friend "They're not all the same. Okay, some of them are. But this one has sunscreen down the whole front, like a map of everywhere I missed, and I can't wear a map to dinner."

    $ enter_cinematic_mode()
    scene cg ch01_d2_mall_arrival
    with dissolve
    "The mall stop was supposed to take five minutes."
    $ exit_cinematic_mode()
    scene bg ch01_d2_mall
    with dissolve
    "[friend_name] disappeared toward menswear. Maya made it approximately three storefronts before stopping at a boutique window."

    $ enter_cinematic_mode()
    scene cg ch01_d2_mall_boutique_window
    with dissolve
    "A red dress and a black one stood in the display. Maya pointed at the red one; [girlfriend_name]'s eyes kept drifting toward the black."
    maya "Oh. Oh, no."
    gf "Why did you say that like that?"
    maya "Look at these. Just look, that's all."
    gf "No. I know that voice."
    maya "I'm only looking at the dresses. You're allowed to look."
    gf "I've known you for, like, a couple of hours, and I already know that voice."

    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve
    "[girlfriend_name] still followed her inside."

    $ enter_cinematic_mode()
    scene cg ch01_d2_shop_dresses
    with dissolve
    "Maya came back from the nearest rack with a dress on each hand: a long red slip with a lace neckline, and a black one just as long, cut clean and simple."
    maya "Okay. Be honest. Red or black?"
    gf "For you?"
    maya "For me. I'm not buying either. I just need to know."
    "She held them up against herself one at a time, then both at once, as if the answer might be hiding somewhere between them."
    gf "The red one's gorgeous. Look at the lace."
    maya "Right? But the black one. Look how simple it is. It's so elegant."
    "[girlfriend_name] rested a knuckle against her chin and actually studied them, which only made Maya happier."
    gf "Red. The black one's what you'd pick to play it safe."
    maya "Two hours, and you already know me. That's rude. Red it is."

    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve
    # The mall CGs show the café outfits (Leia casual, Maya green tube top).
    # Julian is off in menswear.
    $ cast(ryan="casual", leia="casual", maya="green_tube_top")
    "Maya kept the red dress over her arm. [girlfriend_name] drifted on to another rack, slower."
    "She'd been eyeing the black dress through the window. Then she came around the last rack and stopped dead."

    # Leia stops at the spotlit mannequin (DressReveal_01, darryn 2026-11-19).
    $ enter_cinematic_mode()
    scene cg ch01_d2_boutique_dress_reveal
    with dissolve

    "In the middle of the floor, on its own little stage under a spotlight, a mannequin was wearing the most daunting dress in the shop."
    "Black latex, so glossy it caught every light in the room. Two thin straps, a skirt that barely started before it stopped, and cutouts everywhere: one plunging down the chest, more running down both sides."
    "It made the dress in the window look like something you'd wear to a job interview. It should have sent her straight back to the safe rack."
    "Somehow it didn't. Something about it pulled her in, and she just stood there looking at it, long enough for Maya to notice."

    maya "That one. You want that one."
    gf "What? No. I'm just looking."
    maya "You've been staring at it for a full minute."
    gf "I have not! I was looking at the... the shine. How do they even get it that shiny?"
    maya "The shine. Okay. You absolutely have."
    gf "It's just... I don't get how it even stays on. That's all. I'm curious. Like, from a design point of view."
    maya "Oh, babe. That's not curious. That's wanting."

    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve
    $ cast(ryan="casual", leia="casual", maya="green_tube_top")

    "Maya found the same dress on the rail beside the stage before [girlfriend_name] could stop her, and held it up against her."
    maya "Yeah. No. You're trying this one."
    gf "Maya, no. Look at it. Look at how little of it there is."
    maya "That's what the changing room is for. Go find out how it stays on. From a design point of view."

    "[girlfriend_name] stared at the black dress, then at Maya."
    gf "I'm not wearing that outside. Ever."
    maya "I didn't say outside! I said try it. Nobody's buying anything."
    gf "Why? What's the point if I'm not wearing it?"
    maya "Because you've been staring at that rack like it owes you money, and I want to see your face when you see yourself in it. And I want to see you in it. Here. Changing room's right there. Go."

    "[girlfriend_name] hesitated, then took the hanger from her."
    $ set_story_flag("ch01_d2_maya_pushed_boutique_tryon")
    $ set_story_value("ch01_d2_boutique_trial_outfit", "boutique_cutout_mini")

    maya "I'm trying the red one too. Solidarity. Now go, before you talk yourself out of it."

    "Maya took the curtain on the left. [girlfriend_name] took the one beside it, like she was walking into an exam."

    # Leia and Maya are in the changing rooms in the try-on dresses (no sprites for
    # those outfits yet), so only Ryan stays on stage for the rest of the boutique.
    $ cast_remove("leia", "maya")
    "I found the one chair in the boutique, next to the window display, and settled in to wait."

    $ enter_cinematic_mode()
    scene cg ch01_d2_boutique_changing_room
    with dissolve

    "Behind the curtain, [girlfriend_name] held the dress up at arm's length, put her other hand to her chin and looked at it for a long time."
    "Off the mannequin it looked even smaller. A handful of shiny black latex, two thin straps and a lot of cutouts, and somehow it was supposed to hold her in."
    gf "Okay. It's a dress. People wear dresses. People wear dresses all the time."
    "Then she looked down at herself. White off-shoulder T-shirt, denim shorts, and plain white underwear under all of it. A bra and panties. Nothing exciting."
    "She looked back at the dress."
    gf "Holes... everywhere." # under her breath
    "Every single one of them sat right where a bra strap or a waistband would be."
    "So her underwear would show. White straps poking out of every hole, like wearing socks with sandals, only worse, because the whole point of the dress was the holes."
    "Which meant the bra would have to come off. And honestly, the panties too, the way those side cutouts went. Which meant there'd be nothing under the dress. At all. In a mall. Behind a curtain that didn't quite reach the wall."
    gf "No. Absolutely not. That's insane."
    "She kept holding the dress up anyway."
    gf "...Maya?"
    maya "Yes! Are you in it?"
    gf "No. I'm wearing white underwear, and this thing has, like, holes everywhere. It's going to show. Like, all of it is going to show."
    maya "So take it off."
    gf "The bra?"
    maya "Everything. Take it all off. Nobody wears anything under a dress like that, babe. That's the whole point of a dress like that."
    gf "Is that true? That can't be true. Wait, is that actually true?"
    maya "Why do you think mine looks this good? Confidence and nothing else. Mostly nothing else."
    gf "Maya!"
    maya "What? Now you know! Everything off, dress on. I want to see."
    # Eavesdropper (darryn 2026-11-19): someone outside might have heard, or might not.
    "Outside the curtain, something shifted. A shuffle of feet, the soft scrape of a hanger on a rail, voices too muffled to make out."
    "Then, low, barely more than a breath, a man's voice from somewhere close: \"...I wanna see that too.\""
    "[girlfriend_name] froze with the dress halfway to her chest."
    gf "Maya. Did you hear that?"
    maya "Hear what?"
    "She listened. Hangers. The shop music. Someone laughing over by the till. Nothing else."
    gf "Somebody said... No. Nobody said anything. Great, now I'm hearing things."
    maya "You're stalling, is what you're doing."
    "[girlfriend_name] looked at the curtain, then at the gap at its edge, then back at the dress."
    gf "If anyone opens this curtain, I'm just going to live in here now. This is my home."
    maya "Noted. Hurry up."

    scene cg ch01_d2_changing_room_02
    with dissolve

    "The bra and panties went into her bag with the T-shirt and shorts. The dress went on easier than she expected, which somehow made it worse. Then she looked up at the mirror."
    gf "Oh. Oh, okay."
    "The latex hugged everything, cool and tight and squeaking faintly when she moved. The cutouts sat exactly where she'd been afraid they would, and the hem stopped a lot higher up her thighs than anything she owned."
    gf "Maya, how short is this supposed to be?"
    maya "Short! It's a mini, that's the whole idea of a mini!"

    scene cg ch01_d2_changing_room_03
    with dissolve

    "She turned to check the back, and the hem rode straight up with her."
    "She tugged it down. The top shifted. She caught that with her other arm, pressed the top of the dress up against her chest and stood very, very still."
    gf "Yeah, no. It's a size too small."
    maya "Is it, though? Or is it just a lot of dress?"
    gf "It's not a lot of anything, Maya, that's the problem. If I pull it down, the top goes, and if I fix the top, the bottom goes, and I only have two hands."
    maya "So you hold both. Easy."
    gf "I'm not going out there holding both."
    "She looked at herself for a while anyway. Then, still holding the front in place with one arm, she dug her phone out of her bag on the bench."

    scene cg ch01_d2_changing_room_capture
    with dissolve
    $ lc_photo()

    "She angled the phone at the mirror and took the picture before she could change her mind."

    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve
    $ cast(ryan="casual")

    $ lc_sfx("phone_notify")
    "My phone buzzed against my leg. [girlfriend_name]."
    python:
        phone_add_message(
            "leia",
            "leia",
            text="",
            message_id="ch01_d2_boutique_selfie",
            attachment_id="ch01_d2_changing_room_selfie",
            attachment_label=girlfriend_name + " in the changing room",
            mark_unread=True,
            notify=True,
        )
        phone_add_message(
            "leia",
            "leia",
            text="Be honest. Is this too much?? Maya picked it. Obviously.",
            message_id="ch01_d2_boutique_selfie_ask",
            mark_unread=True,
        )

    # Ryan answers the selfie inside the phone (darryn 2026-11-19: phone replies are never
    # dialogue menus, and the scene never repeats what the phone shows). The card carries the
    # scored reveal choices (same choice ids, message ids and story value as before); the
    # story waits for the pick, then lc_phone_await_reply applies the option's choice_id.
    $ phone_offer_reply("leia", "ch01_d2_boutique_selfie_reply", [
        {"id": "affection", "text": "You look incredible.", "choice_id": "ch01_d2_mall_reveal_affection",
         "message_id": "ch01_d2_boutique_selfie_reply",
         "followups": [("leia", "You have to say that. You're biased.", "ch01_d2_boutique_selfie_followup"), ("leia", "Don't come over here. I'm not coming out in this. Changing room only.", "ch01_d2_boutique_selfie_stay")]},
        {"id": "open", "text": "Didn't know you had that in you.", "choice_id": "ch01_d2_mall_reveal_open",
         "message_id": "ch01_d2_boutique_selfie_reply",
         "followups": [("leia", "I DON'T. This is all Maya. I'm just standing in it.", "ch01_d2_boutique_selfie_followup"), ("leia", "Don't come over here. I'm not coming out in this. Changing room only.", "ch01_d2_boutique_selfie_stay")]},
        {"id": "tease", "text": "Maya really did this to you?", "choice_id": "ch01_d2_mall_reveal_tease",
         "message_id": "ch01_d2_boutique_selfie_reply",
         "followups": [("leia", "Against my better judgment. VERY much against it.", "ch01_d2_boutique_selfie_followup"), ("leia", "Don't come over here. I'm not coming out in this. Changing room only.", "ch01_d2_boutique_selfie_stay")]},
        {"id": "flat", "text": "It's... nice.", "choice_id": "ch01_d2_mall_reveal_flat",
         "message_id": "ch01_d2_boutique_selfie_reply",
         "followups": [("leia", "Nice.", "ch01_d2_boutique_selfie_followup"), ("leia", "Don't come over here. I'm not coming out in this. Changing room only.", "ch01_d2_boutique_selfie_stay")]},
    ], "affection")
    call lc_phone_await_reply("leia") from ch01_d2_boutique_selfie_await
    $ d2_selfie_reply = get_story_value("ch01_d2_boutique_selfie_reply")
    if d2_selfie_reply == "flat":
        "I started typing that I meant really nice, deleted it, and didn't send anything after all."

    "I put my phone away and stayed in my chair. Whatever happened next, it was going to be her call."

    $ enter_cinematic_mode()
    scene cg ch01_d2_changing_room_04
    with dissolve

    # ChangingRoom_04: Leia has pulled the curtain partway open with one hand, the other arm
    # clamped across her chest; Maya (back to camera) is right outside.
    "On the other side of the shop, [girlfriend_name]'s curtain slid open partway. She stood in the gap with one hand still gripping the fabric and the other arm clamped across her chest."
    gf "Maya? Okay. Thoughts. Quick ones, before I change my mind."
    "Maya was already standing right outside, in her red dress. She looked at [girlfriend_name] for a long second."
    maya "Oh, I hate you. Babe, you look so hot right now it's actually kind of annoying."
    gf "That's not a thought. That's a noise."
    maya "You sent [player_name] a picture and I only get half a curtain? I'm the one who picked it!"
    gf "That's different. He's— that's different. And half a curtain is all anyone's getting."
    # Subtle Day Two tint (lc_leia_tint): shy by default; the stat furthest over its bar colours the line.
    $ d2_tint = lc_leia_tint(ch01_d2_route_lane())
    if d2_tint == "love":
        gf "Don't look at my face. I'm so red right now, aren't I? And he's already got the picture, so he's definitely doing his stupid happy face over there."
    elif d2_tint == "exhibitionism":
        gf "Don't look at my face, I can feel how red it is. Is it bad? Like, actually bad, or just bad because it's me in it?"
    else:
        gf "Don't look at my face. I'm so red right now. I can feel it in my ears."
    maya "You're red because you look like this, babe. That's allowed."
    maya "I'm serious, I'm actually jealous. I picked the wrong dress for myself and the right one for you, and now I have to live with that."
    gf "Maya, it's a size too small. I'm literally holding it on. Should I just try the bigger one?"
    maya "No! Absolutely not. The bigger one won't do this. This is the one."
    gf "It's not doing anything, it's barely staying on. If I pull the bottom down, the top comes with it."
    maya "Okay, so here's what we do. I hold the top up for you, from behind. You hold the bottom down. Two people, one dress. Easy."
    gf "That's a terrible plan."
    maya "It's a great plan. You look this hot and you don't want to show it off? Come on. Two steps. The mirror out here is way better anyway."
    gf "The mirror in here is fine."
    maya "The mirror in there is a little sad and you know it."
    "[girlfriend_name] looked at her for a long moment. Then, very slowly, she let go of the curtain and it swung open the rest of the way."

    scene cg ch01_d2_shop_showoff
    with dissolve
    # Hidden POV (darryn 2026-11-17): the stranger by the racks on the left; his view
    # is ShopShowOffCloseup_01. Optional cue only; no stats or story change.
    $ lc_pov_begin("d2_boutique_stranger")

    "Maya got her as far as the big mirror outside the changing rooms. [girlfriend_name] planted herself in front of it, back to the whole shop, and refused to go one step farther."
    maya "You're facing the wrong way."
    gf "I'm facing the mirror. That's what mirrors are for."
    maya "The mirror's not the one who needs to see you, babe."
    gf "Nobody needs to see me. I'm good right here. This is a great spot."
    maya "It's a terrible spot. You're showing the whole shop your back."
    gf "Wait— my back? What's happening back there? Is something happening?"
    maya "Nothing! It's a very good back. Relax."
    gf "Okay, but you've got the top, right? Like, actually got it? Not just sort of touching it?"
    "Maya took the back of the dress in both hands and lifted, so the neckline sat higher and stayed where it was supposed to."
    "[girlfriend_name] let go of her chest one finger at a time, like she didn't trust it, then grabbed the front of the hem and pulled it as low as it would go."
    maya "Got it. Top's mine, bottom's yours. Nothing's going anywhere. Now turn around."
    gf "And then what? I just stand there?"
    maya "You just stand there and let them look. That's the whole job."
    gf "People are already looking, Maya. I can literally feel them looking at me."
    maya "Because you look like that! That's my entire point, babe!"
    "Behind them, a man over by the racks had stopped pretending to look at shirts a while ago."
    gf "Oh my God. Okay. Fine. Fine, I'll turn around, but if you let go, I'm— I don't know what I'm doing yet, but it's going to be bad. For you."
    maya "I'm not letting go. Hand on my heart. Well. Hands on your dress. Same thing."

    $ lc_pov_end()
    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve
    # Both in their try-on dresses (Leia's Latex Dress and Maya's Red Dress sprites,
    # darryn 2026-11-18).
    $ cast(ryan="casual", leia="latex_dress", maya="red_dress")
    $ face("leia", "shy")
    $ face("maya", "smile")

    "From my chair by the window, I watched [girlfriend_name] turn around."
    "Even from across the shop, the dress was a lot. She had both hands pulling the hem down at the front, and Maya was right behind her, holding the top up for her."

    maya "[player_name]! Get over here! You need to see this up close!"

    "Maya's voice carried across the entire boutique. Every head that hadn't already turned toward the changing rooms turned now."
    "A woman at the shoe wall stopped halfway into a sandal. Two guys by the jeans gave up pretending to look at jeans."
    "[girlfriend_name] went red from her collarbones up. She looked at the floor like she was hoping it would open up for her."
    $ face("leia", "flustered")
    gf "Maya! Why would you yell?"
    maya "So he'd hear me! And it worked, look, everyone heard me."
    gf "That's not the good part!"

    $ d2_mall_lane = ch01_d2_route_lane()
    $ set_story_value("ch01_d2_mall_entry_lane", d2_mall_lane)
    $ d2_mall_ryan_present = True

    if d2_mall_lane == "ntr_risk":
        $ d2_mall_go_text = format_choice("ch01_d2_mall_go_to_leia", "Go see what she wants.")
        $ d2_mall_leave_text = format_choice("ch01_d2_mall_leave_to_maya", "Let Maya handle it. She's better at clothes.")

        menu:
            "[d2_mall_go_text]":
                $ apply_choice("ch01_d2_mall_go_to_leia")
                $ set_story_value("ch01_d2_mall_ryan_response", "reconnected")
                "Whatever distance had been building between us, she was standing over there in front of half the shop."
                "I went over."

            "[d2_mall_leave_text]":
                $ apply_choice("ch01_d2_mall_leave_to_maya")
                $ set_story_value("ch01_d2_mall_ryan_response", "ignored")
                $ d2_mall_ryan_present = False
                mc "You two are fine! Maya's better at this than me. I'll just get in the way."
                "There was a short pause from over by the mirror."
                gf "...Okay."
    else:
        $ set_story_value("ch01_d2_mall_ryan_response", "came_over")
        "I was already out of the chair."

    if d2_mall_ryan_present:
        "I crossed the shop. By the time I got there, [girlfriend_name] still had both hands on the hem, and Maya was still holding the top up for her."
        $ d2_selfie_reply = get_story_value("ch01_d2_boutique_selfie_reply")
        $ face("leia", "shy")
        if d2_selfie_reply == "affection":
            gf "Don't say it again. If you say incredible again in front of all these people, I'm going to die. Right here, by the mirror."
            mc "I wasn't going to say it again."
            "I was absolutely going to say it again. She could tell, and she went even redder."
        elif d2_selfie_reply == "open":
            gf "Don't. I can see you thinking it. 'Didn't know you had that in you.'"
            mc "I'm thinking it a little."
            maya "He's thinking it a lot. Look at him."
        elif d2_selfie_reply == "tease":
            gf "Yes. She did this to me. You can see that now. In person."
            maya "You're welcome. Both of you."
        elif d2_selfie_reply == "flat":
            $ face("leia", "pout")
            gf "Still just nice?"
            mc "It's more than nice. Up close it's way more than nice. I just didn't know how to type it."
            gf "Okay. Thanks."
            "She tugged the hem down again and didn't quite look at me."
        else:
            gf "Well? Say something, I'm dying here."
        "People were still looking. She knew it, too. She kept her eyes on me like I was the only safe place left to put them."

    else:
        maya "Fine! [friend_name]!"
        gf "Maya—"
        maya "What? We need a second opinion, and he's right there."

        $ cast_add(julian="evening")
        "[friend_name] appeared from the next section holding two nearly identical shirts."

        friend "Oh."
        maya "'Oh'? That's all you've got?"
        friend "I— sorry, I wasn't ready for a test. I came over here about shirts. Nobody said there'd be a test."
        gf "Don't encourage her. Please."
        friend "You look good, though. Really. Okay. I'm going back to the shirts."
        gf "...Thanks."

    # Wardrobe malfunction (darryn 2026-11-18): ShopShowOff_02-05, shared by both witness
    # branches (Ryan or Julian is off-frame, watching); the branches differ in text only.
    $ enter_cinematic_mode()
    scene cg ch01_d2_shop_showoff_02
    with dissolve

    "The man from the racks had drifted closer while all that was going on. He wasn't looking at [girlfriend_name] now, though. He was looking at Maya."
    boutique_stranger "Sorry, I'm not trying to be weird. I just have to say, that red is unreal on you."
    maya "Oh my God. Stop. Really?"
    boutique_stranger "Really. You should get it."
    maya "I'm getting it! I was getting it anyway, but now I'm definitely getting it. Wait, say that again, slower."

    scene cg ch01_d2_shop_showoff_03
    with dissolve

    maya "Okay, but look at how it sits, though. Look."
    "She hooked her thumbs under her own straps and tugged them up to show him the fit, laughing, completely delighted with herself."
    "Her thumbs had been the only thing holding [girlfriend_name]'s top up."
    "The top of [girlfriend_name]'s dress peeled down with a soft squeak of latex and caught just below her nipples."
    "For one long second, she just stood there with both hands still on the hem, like her brain hadn't caught up yet."

    scene cg ch01_d2_shop_showoff_04
    with dissolve

    gf "Maya!" with lc_punch()
    "Both her hands flew up to cover her chest, and the hem she'd been holding down went straight back up her thighs."
    "The whole corridor saw it. The stranger saw it. The woman at the shoe wall saw it."

    if d2_mall_ryan_present:
        "I saw it. She looked straight at me while it happened, eyes huge, like I could somehow undo it from where I was standing."
        "Maya spun around, horrified."

        scene cg ch01_d2_shop_showoff_05
        with dissolve

        "She threw both arms around [girlfriend_name] and pulled her in close, front to front, covering her the only way she could."
        "From behind, it did absolutely nothing for either of them."
        maya "Sorry! Sorry sorry sorry, I've got you, I've got you."
        gf "Maya! You were holding it, you were literally standing there holding it and you just let go!"
        maya "I know! He was being nice to me, and I got distracted, and my hands just went."
        gf "I can't believe this is happening in a shop."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve
        $ set_story_value("ch01_d2_boutique_slip_witness", "ryan")

    else:
        "[friend_name] hadn't made it back to the shirts yet. He was still standing right there when it happened."
        "He looked, and he kept looking for a moment after he should have stopped."
        "Then he caught himself. His eyes jerked up to the ceiling lights, and the red was already climbing his neck before [girlfriend_name] lifted her head."
        "She looked up in time to catch the end of it: [friend_name], bright red, looking anywhere but at her."
        "She didn't say anything. She just held her arms a little tighter across herself, and he saw her do it."

        scene cg ch01_d2_shop_showoff_05
        with dissolve

        "Maya threw both arms around [girlfriend_name] and pulled her in close, front to front, covering her the only way she could."
        "From behind, it did absolutely nothing for either of them."
        "Maya, focused entirely on covering her up, missed the exchange."

        maya "Sorry! Sorry sorry sorry, I've got you, I've got you."
        gf "Maya. You were holding it."
        maya "I know! He was being nice to me, and I got distracted, and my hands just went."
        gf "I can't believe this is happening in a shop."
        friend "Sorry. I'm so sorry, I wasn't— I didn't mean to, I was just standing here with the shirts and then it was— sorry. I'm really sorry, [girlfriend_name]."
        "He held up the two shirts, one in each hand, and didn't look at either of them."
        friend "Which one of these is better? The blue one or the, um. The other blue one. I honestly can't tell anymore."
        maya "They're the same shirt, [friend_name]."
        "He took both of them back toward menswear, walking a lot faster than he needed to."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve
        $ set_story_flag("ch01_d2_leia_noticed_julian_stare")
        $ set_story_value("ch01_d2_boutique_slip_witness", "julian")

    $ face("leia", "flustered")
    $ face("maya", "shy")
    "The man from the racks had already found somewhere else in the shop to be."
    maya "In my defense, he had really good taste."
    gf "I'm changing. Into my own clothes. Right now."
    maya "So that's a maybe."
    gf "That's a no, Maya."

    $ cast_add(leia="casual", maya="green_tube_top")
    $ face("leia", "neutral")
    "A few minutes later they emerged in their normal clothes. Maya had bought the red dress without hesitation."
    "[girlfriend_name] still had the black mini over one arm."

    if d2_mall_ryan_present:
        $ set_story_flag("ch01_d2_boutique_shop_open")
        if LC_SHOP_ENABLED:
            "The boutique's catalog was available through the Shop on my phone. Buying something would add it to [girlfriend_name]'s wardrobe. Whether it ever left her suitcase was up to her, though Maya clearly had opinions about that."
            $ last_shop_message = "Boutique visit: the Black Cutout Mini is now available."
            call screen shop_screen
        else:
            # The Shop is switched off while it's under development
            # (LC_SHOP_ENABLED); the purchase happens as an in-story choice.
            "I could buy it for her. Whether it ever came out of the suitcase was her call. Maya's opinion was already on record."
            menu:
                "Buy the black mini for her." if can_afford(get_outfit("boutique_cutout_mini")["cost"]):
                    $ purchase_outfit("boutique_cutout_mini")
                "Leave it.":
                    pass
        if owns_outfit("boutique_cutout_mini"):
            $ set_story_value("ch01_d2_mall_outfit_source", "ryan")
            $ set_story_flag("ch01_d2_boutique_outfit_owned")
            gf "Wait, you actually bought it? When did you— you actually bought it."
            mc "You looked really good in it. And you kept looking at it."
            gf "That doesn't mean I'm wearing it outside."
            maya "Not yet, you're not."
            "[girlfriend_name] gave Maya a look and said nothing."
        else:
            # Ryan chose not to buy it, so Leia buys the Black Cutout Mini herself.
            # (Ryan buying it still stands; there is no "nobody buys it" outcome.)
            if LC_SHOP_ENABLED:
                "I closed the Shop without buying anything."
            else:
                "I left the dress where it was."
            "[girlfriend_name] looked back at the black dress for several seconds, then carried it to the counter herself."
            $ grant_story_outfit("boutique_cutout_mini", equip=False)
            $ set_story_value("ch01_d2_mall_outfit_source", "leia")
            $ set_story_flag("ch01_d2_boutique_outfit_owned")
            mc "Wait, you're buying it?"
            gf "I'm not wearing it outside. I just— I don't know. I want to own it."
            maya "Mm-hm. Not yet."
            "[girlfriend_name] gave Maya a look and said nothing."
    else:
        "[girlfriend_name] looked down at the black dress for several seconds before carrying it to the counter herself."
        # If Ryan already owns it, his purchase stands (source "ryan"); otherwise Leia buys it.
        if owns_outfit("boutique_cutout_mini"):
            $ set_story_value("ch01_d2_mall_outfit_source", "ryan")
        else:
            $ grant_story_outfit("boutique_cutout_mini", equip=False)
            $ set_story_value("ch01_d2_mall_outfit_source", "leia")
        $ set_story_flag("ch01_d2_boutique_outfit_owned")

        mc "You bought it? The black one?"
        gf "Yeah. Don't look at me like that."
        mc "I thought you said it was too much."
        gf "I said I wasn't wearing it outside. That's a different thing."
        maya "She said 'outside.' I heard 'yet.'"
        "[girlfriend_name] gave Maya a look and said nothing."

    $ cast_add(julian="evening")
    "[friend_name] eventually returned with a shopping bag."

    maya "That's literally the shirt you're already wearing."
    friend "No, this one's different."
    maya "How? Tell me one way it's different."
    friend "It's... new. It's a new one."

    "We stepped back outside into the early-afternoon heat with considerably more shopping than [friend_name]'s five-minute shirt stop had promised."

    maya "Drink before we go back? I'm melting."
    gf "Please. Yes. Something with ice."

    # Drinks at a mall café before heading back (darryn renders the BG; placeholder for now).
    scene bg ch01_d2_mall_drinks
    with dissolve
    $ cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")

    "We found a table nearby and dropped the shopping bags around our feet."

    maya "Okay, that went way better than I expected."
    gf "For who? Better for who, exactly?"
    maya "For me. Obviously."
    gf "Trying something on and wearing it are completely different things."
    maya "That's what fitting rooms are for, though. That's the whole point of them."

    friend "For what it's worth, I think you should keep it. Even if it just lives in your suitcase."
    "He said it mostly to his drink."
    gf "Thanks, [friend_name]."
    maya "See? He agrees with me."
    gf "You're impossible, you know that? He was being nice."
    "She was laughing when she said it."

    "Maya and [friend_name] started arguing over whether his new shirt was actually different from the one he'd arrived in."
    "[girlfriend_name] leaned slightly closer to me."

    # Day One echo: the sticky bra at dinner (ch01_bra_response). A private aside:
    # Leia kept the bra out of Julian's hearing on Day One, so she still does.
    if get_story_value("ch01_bra_response") == "playful_open":
        gf "This trip has it out for my clothes. Last night my bra quit on me at dinner, and today Maya tried to put me in two napkins and a string."
        mc "Last night you were smiling, though."
        gf "That was my stressed face! I told you it was my stressed face."
        "She was smiling now, too."
    elif get_story_value("ch01_bra_response") == "reassuring":
        gf "If I ever wear that thing, don't tell me 'you'll be fine.' You said that about the sticky bra last night."
        mc "And you were fine."
        gf "I was fine. I was also braless in a restaurant, babe."
        mc "Fine and braless. Those aren't opposites."
        "She laughed into her drink and nearly choked on the ice."
    elif get_story_value("ch01_bra_response") == "cautious":
        gf "If I ever do wear that thing out, you're on lookout duty again. Like last night with the bra."
        mc "I mostly watched the bathroom door."
        gf "Very professionally, though. It was sweet. I noticed."
    elif get_story_value("ch01_bra_response") == "distracted":
        gf "If I ever do wear that thing, I'm telling you first, and you're putting the menu down. Last night you told the menu to go for it."
        mc "I said sorry."
        gf "You did. I'm still bringing it up."

    if get_story_value("ch01_d2_boutique_slip_witness") == "ryan":
        gf "You saw that, right? In there?"
        mc "The dress? Yeah, I saw the dress."
        gf "No, when it slipped. When Maya let go."
        mc "Yeah. I saw."
        gf "I wanted to disappear. Like, into the floor. Just gone."
        if get_story_value("ch01_d2_mall_ryan_response") == "reconnected" or get_story_value("ch01_d2_mall_entry_lane") != "ntr_risk":
            mc "You covered up really fast, though. And Maya was on you in about half a second."
            gf "Barely. My whole soul left my body."
            "Her embarrassment had already softened enough for her to roll her eyes at herself."
        else:
            mc "It was an accident. Maya was fixing it."
            gf "I know. I know it was."

        # Day One echo: "Did he see?" after the towel (ch01_towel_followup).
        if get_story_value("ch01_towel_followup") == "honest":
            gf "Did anyone else see? Not-nice version, please. Like yesterday."
            mc "Just me and Maya. I actually checked, because I knew you'd ask."
            gf "You checked. Okay. That's— thank you."
            gf "This is why I ask you, you know. You're the one who doesn't give me the nice version."
        elif get_story_value("ch01_towel_followup") == "reassured":
            gf "Did anyone else see? And don't do the 'he looked away pretty much immediately' thing again."
            mc "Nobody was looking. Actually nobody this time. I checked."
            gf "Actually nobody. Okay. I can live with actually nobody."
        elif get_story_value("ch01_towel_followup") == "teased":
            gf "And if you say one word about curtains, I'm leaving you here with the mannequins."
            mc "I wasn't going to say curtains."
            gf "You were thinking curtains. I can see you thinking curtains."
        elif get_story_value("ch01_towel_followup") == "brushed_off":
            gf "And before you say it, it's a big deal. To me. A little bit."
            "She said it before I'd even opened my mouth, like she already knew what was coming."
            mc "I wasn't going to say it wasn't."
            "I had been, a little."
    else:
        mc "So what happened in there? After I, um. After I stayed out."
        gf "Nothing. Nothing dramatic."
        "She turned her cup slowly between her hands."
        gf "The top came down. Like, all the way. Some guy started complimenting Maya, and she just let go."
        mc "Oh."
        gf "[friend_name] was there."
        "I looked at her."
        gf "He looked away. He'd already looked away by the time I looked up, actually, and he went really red. And then he said sorry. Like, a lot."
        "She didn't sound defensive about it, just like someone handing me the version of events she had been left to work through without me."

    # Flow (darryn 2026-11-19): a Ryan who has been warm all day gets an attentive check-in about
    # last night, not "you've been quiet". The detached version stays for dismissive/withdrawn picks.
    $ d2_ryan_detached = (choice_tag_count("dismissive", ch01_d2_choice_ids()) + choice_tag_count("withdrawal", ch01_d2_choice_ids())) > 0
    if d2_ryan_detached:
        gf "You've been kind of quiet today, though. Not in a bad way. Just quiet."
    else:
        gf "Hey. Did you actually sleep last night, though? You were tossing around a lot. Like, a lot a lot."

    $ d2_postshop_sleep_text = format_choice("ch01_d2_postshop_sleep", "I didn't sleep well.")
    $ d2_postshop_head_text = format_choice("ch01_d2_postshop_head", "I've just got a lot in my head.")
    $ d2_postshop_shut_text = format_choice("ch01_d2_postshop_shut_down", "I'm fine.")
    # Extra replies (new mechanics program). Leia's version (B1): only when the slip played with
    # Julian there. The dream (B3): only when Ryan kept the Day One dream thought. Old saves: neither.
    $ d2_postshop_dream_text = format_choice("ch01_d2_postshop_dream", "I had a weird dream last night.")
    $ d2_postshop_version_text = format_choice("ch01_d2_boutique_her_version", "Hang on. Did he really look away that fast?")
    $ d2_dream_thought_kept = lc_thought_kept("ch01_d1") == "d1_dream"
    $ d2_leia_version_offered = get_story_value("ch01_d2_boutique_slip_witness") == "julian" and has_story_flag("ch01_d2_leia_noticed_julian_stare")

    menu:
        "[d2_postshop_sleep_text]":
            $ apply_choice("ch01_d2_postshop_sleep")
            mc "I didn't sleep well."
            gf "Yeah, I noticed. You kept doing the thing with the pillow."
            mc "Sorry. I didn't mean to keep you up."
            gf "You don't have to apologize for being tired, babe. I just wanted to know you're okay."
            "It wasn't the whole truth, but at least I had stopped pretending there was nothing to explain."

        "[d2_postshop_dream_text]" if d2_dream_thought_kept:
            $ apply_choice("ch01_d2_postshop_dream")
            mc "I had a weird dream last night. I never told you about it. It's kind of stupid."
            gf "A weird dream? What kind of weird?"
            mc "The guy from dinner. The drink guy. He was there, and you were there, and I couldn't move or say anything. I just had to watch."
            "[girlfriend_name] stared at me for a second."
            $ d2_tint = lc_leia_tint(ch01_d2_route_lane())
            if d2_tint == "temptation":
                gf "Okay, babe, that's a pretty weird dream."
                gf "It was just a guy with a drink. He said sorry, like, nine times."
                mc "I know. I know it was."
                "She patted my hand and went back to her drink. It was nice of her. It just wasn't what I'd been hoping for."
            else:
                "Then she laughed at me. Properly, with her whole face."
                gf "The drink guy? You've been carrying the drink guy around since last night? Come here, you."
                "She leaned over and hugged me, right there at the table, shopping bags and all."
                gf "He apologized to me about nine times and went back to his table. That's the whole story. That's all he ever gets to be."
                think "She laughed at me, and then she hugged me. I'd known she would. I just hadn't let her."

        "[d2_postshop_head_text]":
            $ apply_choice("ch01_d2_postshop_head")
            mc "I've just got a lot in my head."
            gf "Anything you want to talk about? You don't have to."
            mc "Not yet. Maybe later? I don't really know how to say it yet."
            gf "Okay. Later's fine."
            "She didn't push. She just bumped her knee against mine under the table and left it there."

        "[d2_postshop_shut_text]":
            $ apply_choice("ch01_d2_postshop_shut_down")
            mc "I'm fine."
            "[girlfriend_name] watched me for a second."
            gf "Okay."
            "This time the word meant she was done asking."

        "[d2_postshop_version_text]" if d2_leia_version_offered:
            $ apply_choice("ch01_d2_boutique_her_version")
            mc "Hang on. Back up a second. Did he really look away that fast?"
            "[girlfriend_name] stopped turning her cup."
            gf "Technically, yeah. By the time I looked up he was staring at the ceiling."
            gf "But nobody goes that red from looking at a ceiling. He looked, babe. I don't know for how long, and I keep wondering. And he knew I knew, and I honestly thought he was going to pass out into the shirts."
            $ d2_tint = lc_leia_tint(ch01_d2_route_lane())
            if d2_tint == "love":
                gf "And the whole time I just kept wishing it was you standing there instead. Is that dumb? That's dumb."
                mc "It's not dumb. I should've been there."
                "She hooked her ankle around mine under the table and left it there."
            elif d2_tint == "exhibitionism":
                gf "And I didn't hate it as much as I probably should have. Mostly I kept wondering what your face would've done. Don't make that face, I'm telling you, aren't I?"
                "She was pink to the ears, and she still didn't look away from me."
            elif d2_tint == "temptation":
                gf "It was nothing. He said sorry about fifty times. I don't even know why I told it the other way first."
                "She shrugged and went back to her drink, like that was the end of it."
            else:
                gf "I don't know why I told it the other way first. I think I just wanted it to be smaller than it was."
                mc "Thanks for telling me the real one."
                gf "You asked for the real one. I like it when you ask."
            gf "You totally dodged my question, though. Don't think I didn't notice."
            mc "...Later?"
            gf "Later. I'm holding you to later."

    "[friend_name] stood and picked up his shopping bag."
    friend "I'm getting another drink before we go. Anyone want anything? [player_name], come help me carry."
    mc "Yeah, I'll come."

    "We left [girlfriend_name] and Maya at the table for a minute."
    "[friend_name] was still losing an argument with the card machine when the first two drinks came up, so I carried them back on my own."
    "There was a big potted palm between the counter and our table. I was a couple of steps behind it when I heard my name."

    # Day Two incident (v0.2.0): Ryan overhears the talk. The milder version plays when he has
    # been present today (a repair pick, or he went to her at the mall): then Leia confides in
    # Maya because she cares (darryn 2026-11-19). The worried version keeps "he's somewhere else".
    if choice_tag_count("repair", ch01_d2_choice_ids()) >= 1 or get_story_value("ch01_d2_mall_ryan_response") in ("reconnected", "came_over"):
        $ set_story_value("ch01_d2_overheard_talk", "mild")
        gf "Can I tell you something kind of dumb? About [player_name]?"

        "I stopped walking."

        maya "Always. Dumb is my favorite kind."
        if "ch01_d2_postshop_dream" in choice_history:
            gf "He had a bad dream last night. About the guy who spilled the drink on me at dinner. He just told me, and he looked so embarrassed telling me."
        else:
            gf "I think he had a bad dream last night. He kept waking up and doing this thing with his pillow, and this morning he just said he was tired."
        gf "And yesterday was a lot. People kept looking at me, like, all day. At dinner, at the pool. I think it got to him more than he lets on."
        maya "And you want to fix it."
        gf "No. Not fix him. I just want him to know I noticed. I want to do something nice for him tonight."
        maya "Oh my God, that's so cute I might throw up. He's always been like that, you know. He goes quiet, and then he comes back. Just stay close."
        gf "I can do close. Close I'm good at."
        think "She'd noticed all of it. The bad night, the looks, me pretending I was fine. She wasn't worried about me. She was looking after me."
    else:
        $ set_story_value("ch01_d2_overheard_talk", "worried")
        maya "Hey. Everything okay?"
        gf "With the dress? I mean, I bought it, so."
        maya "No. With [player_name]."

        "I stopped walking."

        gf "I don't know. Honestly, I don't know."
        "She glanced toward the counter, where she thought I still was."
        gf "He's been somewhere else all morning."
        maya "Did something happen?"
        # Leia's line follows Day One's upstairs talk (the anchor key, read again here).
        if get_story_value("ch01_upstairs_response") == "honest":
            gf "Not today. Last night he actually told me stuff, real stuff, and today it's like that never happened."
        elif get_story_value("ch01_upstairs_response") == "liked":
            gf "No, that's the thing. We had a really good talk last night, a proper one, and today he's gone quiet again and I don't know why."
        elif get_story_value("ch01_upstairs_response") == "swallowed":
            gf "Not that I know of. I ask, and he says he's fine. He said that last night too."
        elif get_story_value("ch01_upstairs_response") == "snapped":
            if get_story_value("ch01_dream_response") == "withdrew":
                gf "Last night he said something kind of mean. Then in the dark he said he didn't mean it, and that's all I've got. Today he just says he's fine."
            else:
                gf "He apologized this morning, which, good. I just still don't know what it was actually about."
        else:
            gf "Not that I know of. He says he's fine."
        maya "Then maybe give him a little time. And if he's still doing it tonight, tell him. Out loud. He's always been better once somebody makes him say it."
        gf "Yeah. Okay."
        "For once, [girlfriend_name] let the problem sit instead of immediately trying to solve it."
        "Maya, who I'd known for years, was explaining me to my girlfriend, who'd met her at lunch."
        think "Neither of them had said one unfair thing. Somehow that was the part that stung."

    # Ryan comes back to the table first; what he does with it is between him and Leia, said low
    # so Maya isn't part of it (darryn 2026-11-19). Same choice ids and story values as before.
    "I came around the palm and put the drinks down. Maya suddenly got very interested in her straw."

    $ d2_overheard_own_text = format_choice("ch01_d2_overheard_own", "Lean in and tell her quietly you heard, and that you'll talk later.")
    $ d2_overheard_joke_text = format_choice("ch01_d2_overheard_joke", "Lean in and whisper: 'Were you two talking about me?'")
    $ d2_overheard_pretend_text = format_choice("ch01_d2_overheard_pretend", "Say nothing. Act like you didn't hear.")

    menu:
        "[d2_overheard_own_text]":
            $ apply_choice("ch01_d2_overheard_own")
            $ set_story_value("ch01_d2_overheard_response", "owned")
            "I sat down beside [girlfriend_name] and leaned in close, under the noise of the café."
            mc "I heard some of that. Sorry. I didn't mean to listen."
            if get_story_value("ch01_d2_overheard_talk") == "mild":
                mc "The dream, and yesterday. You're right about both. Can I tell you about it later? Just us?"
                gf "Oh my God, you heard all of it? The 'cute' part too?"
                mc "Mostly the part where you noticed."
                gf "...Later. Just us. I'm holding you to it."
                "She found my hand under the table and squeezed it."
            else:
                mc "You're right, I've been weird today. Can I tell you about it later? Just us?"
                gf "How much did you hear?"
                mc "Enough. It's fair."
                gf "...Later. Just us. I'm holding you to it."
                "She didn't let go of my sleeve for a while after that."

        "[d2_overheard_joke_text]":
            $ apply_choice("ch01_d2_overheard_joke")
            $ set_story_value("ch01_d2_overheard_response", "joked")
            "I sat down and leaned close to [girlfriend_name]'s ear."
            mc "Were you two just talking about me?"
            if get_story_value("ch01_d2_overheard_talk") == "mild":
                gf "Maybe. Only good things. Don't let it go to your head."
            else:
                gf "Maybe. Drink your drink."
            "She laughed, went a little red, and kissed my cheek. Nobody said anything real after that."

        "[d2_overheard_pretend_text]":
            $ apply_choice("ch01_d2_overheard_pretend")
            $ set_story_value("ch01_d2_overheard_response", "pretended")
            mc "Drinks. [friend_name]'s still fighting the card machine."
            "[girlfriend_name] smiled up at me like nothing had happened."
            if get_story_value("ch01_d2_overheard_talk") == "mild":
                think "She'd been looking after me, and I'd heard it from behind a plant. I didn't know how to say that, so I didn't."
            else:
                think "If she had something to say, she could say it to me. Apparently Maya got to hear it first."

    "By the time [friend_name] got back with the rest, Maya had deliberately moved the conversation back to clothes."
    maya "For the record, I'm still saying the black one."
    gf "And I'm still saying fitting room only. Fitting room and suitcase."
    maya "For now. Fitting room for now."
    gf "You're exhausting. I love it, but you're exhausting."

    $ set_story_flag("ch01_d2_scene_11b_boutique_complete")
    jump ch01_day2_scene_12_villa_pool_plan


label ch01_day2_scene_12_villa_pool_plan:

    # The walk back to the villa (darryn renders the BG; placeholder for now). Everyone is
    # still in their café clothes.
    scene bg ch01_d2_walk_back
    with dissolve
    $ cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")

    "We headed back toward [friend_name]'s place with Maya and [girlfriend_name] a few steps ahead of us."

    if choice_tag_count("repair", ch01_d2_choice_ids()) >= 1:
        "[girlfriend_name] drifted back toward me before long and slipped her hand into mine."
    elif ch01_d2_route_lane() == "exhibitionism":
        gf "[player_name]. Tell her she's insane. Please."
        maya "He doesn't get a vote, he's biased."
        gf "He gets an advisory vote. Like a little advisor."
        mc "As your advisor, I think you're both insane."
        "[girlfriend_name] turned forward again, still laughing with Maya but keeping me inside the conversation."
    elif ch01_d2_route_lane() == "ntr_risk":
        "[girlfriend_name] looked back once."
        "I was half a step behind, somewhere else again."
        if get_story_value("ch01_d2_overheard_response") == "pretended" and get_story_value("ch01_d2_overheard_talk") == "worried":
            think "I kept hearing it. 'Tell him. Out loud.' Like I was something that needed handling."
        "She turned back to Maya."
        "She didn't look back a second time."

    scene bg ch01_villa_living
    with fade
    # Everyone is still in their café clothes from the mall.
    $ cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")

    "Maya stopped just inside."

    maya "Wait. Wait, wait."
    maya "This is where you're staying? This? All of this?"
    friend "It's a booking. It's not, like, mine, it's just something we booked. Do you want a drink? We have drinks. We have a lot of drinks, actually."

    "She looked around the living room, then back at [friend_name]."

    maya "The sunglasses make sense now."
    friend "Can we not do the sunglasses again? Please? Thank you."
    maya "That wasn't a compliment, but you're welcome."

    gf "Come on, I'll show you around. Wait till you see the bathroom, it's ridiculous."
    "Yesterday [girlfriend_name] had been the newcomer. Today she was the one leading Maya through the villa like she'd already learned its shape."

    scene bg ch01_pool_day
    with dissolve
    $ cast(ryan="casual", leia="casual", julian="evening", maya="green_tube_top")

    "They made it as far as the view outside before Maya stopped again."

    maya "Hold on. Is that a private pool?"
    friend "Yeah. I mean, it's not that big."
    maya "You didn't think that was relevant information? You let me talk about the resort pool for ten minutes."
    friend "Relevant to what? I didn't wanna be a weirdo and flex and be like, hi, I'm [friend_name] and I'm staying in a villa with a private pool, wanna come over? I might as well ask you if you're down to hook up."
    $ face("maya", "shy")
    maya "Well..."
    $ face("maya", "neutral")

    gf "We were in it all afternoon yesterday."
    maya "And nobody told me to bring a swimsuit?"

    "Maya paused, then looked down at the day bag she'd been carrying since the café."

    maya "Actually—wait. I did bring one."
    gf "Wait, you just carry a swimsuit around with you?"
    maya "We're on an island, [girlfriend_name]. I always have a swimsuit. Always."
    gf "That's actually really smart. Can I steal that? I'm going to be a swimsuit-everywhere person now."

    maya "Come change with me? You can show me where everything is."
    gf "Sure, but I barely know where anything is either. I've been here one day."
    maya "One day more than me. That makes you the tour guide."

    "[girlfriend_name] led her upstairs while [friend_name] and I dealt with drinks outside."

    $ set_story_flag("ch01_d2_scene_12_complete")
    jump ch01_day2_scene_13_girls_upstairs


label ch01_day2_scene_13_girls_upstairs:

    scene bg ch01_master_bedroom
    with dissolve

    "Upstairs, [girlfriend_name] laid both bikinis across the bed while Maya changed beside her."
    "Both were two-piece tie bikinis. The difference was coverage: one familiar and safer, the other cut noticeably smaller."

    maya "Oh, you brought options. Okay, I see you."
    gf "One is comfortable, and one requires a lot of confidence. Like, a lot."
    maya "The little one. Obviously the little one, I'm not even going to pretend I'm neutral about this."
    maya "So say it. Out loud. Which one are you putting on?"

    "[girlfriend_name] had asked me that same question yesterday, and today she had to answer it herself."

    if lc_stat("exhibitionism") >= LC_T["d2_pool_outfit_bold"]:
        $ set_story_value("ch01_d2_pool_outfit", "pool_bolder")
        # Subtle Day Two tint (lc_leia_tint): shy by default; the stat furthest over its bar colours the line.
        $ d2_tint = lc_leia_tint(ch01_d2_route_lane())
        if d2_tint == "exhibitionism":
            gf "The smaller one. Yeah. The smaller one, before I talk myself out of it. I kind of want to see who notices."
        elif d2_tint == "temptation":
            gf "The smaller one. I think. Yeah. I'm not running this one past [player_name], either, I'm just deciding."
        else:
            gf "The smaller one. I think. Yeah. The smaller one, before I talk myself out of it."
        maya "Then wear the smaller one."
        gf "That's it? That's your advice?"
        maya "That's it. You already knew. I just say it back to people, it's a whole service."
    else:
        $ set_story_value("ch01_d2_pool_outfit", "pool_conservative")
        # Subtle Day Two tint (lc_leia_tint): shy by default; the stat furthest over its bar colours the line.
        $ d2_tint = lc_leia_tint(ch01_d2_route_lane())
        if d2_tint == "temptation":
            gf "I think the more covered one today? Yesterday was a lot. I want a normal pool day. And I'm not even asking [player_name] this time, it's my bikini."
        else:
            gf "I think the more covered one today? Yesterday was a lot. I want a normal pool day."
        maya "Boo. The little one was right there, and it's so cute. Fine. Normal pool day."
        gf "Wait, that's it? You're surprisingly reasonable."
        maya "I'm not reasonable, I'm patient. That little one isn't going anywhere, and neither am I."

    $ grant_story_outfit(get_story_value("ch01_d2_pool_outfit"), equip=True)
    $ set_story_flag("ch01_d2_scene_13_complete")
    jump ch01_day2_scene_14_tie_foreshadow


label ch01_day2_scene_14_tie_foreshadow:

    if get_story_value("ch01_d2_pool_outfit") == "pool_bolder":
        "[girlfriend_name] changed into the bolder tie bikini while still talking to Maya, fastening the top with less attention than the knot deserved."
        maya "Hey, double-knot that."
        gf "It's fine, it's a bikini, not a parachute."
        maya "Famous last words."
        gf "It's held up so far."
        maya "So far you haven't had me talking at you the whole time you tied it."
    else:
        "[girlfriend_name] changed into the more covered tie bikini while Maya borrowed the mirror and most of the counter space."
        "She tied the top while answering Maya, gave the knot one quick tug, and moved on."
        maya "Double-knot that, though."
        gf "This is the safe one! It's been to, like, three beaches."
        maya "A knot doesn't know that."
        gf "It's fine. I tugged it. Look, tugged."

    # Either bikini can come loose during the later pool commotion. Route choice
    # changes how much skin it normally shows, not whether it uses ties.
    $ set_story_flag("ch01_d2_bikini_tie_loose")
    $ set_story_flag("ch01_d2_scene_14_complete")
    jump ch01_day2_scene_15_pool_group


label ch01_day2_scene_15_pool_group:

    scene bg ch01_pool_day
    with fade

    "The four of us spent the first half hour together."
    "Maya immediately discovered [friend_name]'s hatred of being splashed. [girlfriend_name] immediately used that information against him."

    maya "Wait, you guys did this all day yesterday? Without me?"
    gf "Most of the afternoon. Before the whole dinner thing."
    friend "They bullied me yesterday too, for the record. This is a pattern. I want that noted somewhere."
    mc "If it helps, they do this to me too. You never really get used to it."

    "Then [friend_name] sent me inside for towels. When I came back out, Maya and [girlfriend_name] had their heads together on one lounger."
    maya "—so he has no idea? None at all?"
    gf "None. And you are not allowed to—"
    "They both saw me at the same time and stopped."
    gf "Hi! Towels. Amazing. Thank you."
    maya "We were talking about sunscreen."
    gf "Very boring sunscreen stuff."
    "She was grinning at me over the towels, the way she does when she's planning something and is terrible at hiding it."
    think "Whatever it was, I was going to be the last person at this pool to find out. That seemed about right."

    "After that the afternoon went slow and warm. We drifted between the water and the loungers, and somebody's drink was always going flat on the edge of the pool."

    $ set_story_value("ch01_d2_route_lane_pre_split", ch01_d2_route_lane())

    # Door A (new mechanics program, approved by Darryn): Ryan spots the scene 14 knot
    # working loose. Placed after the lane record above, so it can't change today's pool split.
    "Later, [girlfriend_name] was standing in the shallow end with her back to me, laughing at something Maya had said."
    "The knot at the back of her top had worked itself half loose. One string hung a lot lower than the other."
    think "Nobody else had noticed yet. Maya was busy splashing [friend_name], and [girlfriend_name] had no idea."

    $ d2_knot_fix_text = format_choice("ch01_d2_knot_fix", "Swim over and fix it quietly.")
    $ d2_knot_tell_text = format_choice("ch01_d2_knot_tell", "Lean in and tell her.")
    $ d2_knot_watch_text = format_choice("ch01_d2_knot_watch", "Say nothing. See how long it holds.")

    menu:
        "[d2_knot_fix_text]":
            $ apply_choice("ch01_d2_knot_fix")
            $ set_story_value("ch01_d2_knot_response", "fixed")
            $ lc_discovery_mark("d2_knot_door")
            "I waded over behind her, caught both strings before anything could happen, and tied them again. Double knot, this time."
            gf "Oh! What are you— wait. Was it coming undone?"
            mc "A little. It's fine now. Nobody saw."
            "She reached back, found the new knot, and squeezed my fingers over it for a second before she let go."

        "[d2_knot_tell_text]":
            $ apply_choice("ch01_d2_knot_tell")
            $ set_story_value("ch01_d2_knot_response", "told")
            "I leaned in close to her ear."
            mc "Babe. Your knot's coming undone. At the back."
            "She tied it again with both hands behind her, glancing at Maya the whole time to make sure she hadn't seen."
            gf "Thank you. If Maya asks, it was double-knotted all along."

        "[d2_knot_watch_text]":
            $ apply_choice("ch01_d2_knot_watch")
            $ set_story_value("ch01_d2_knot_response", "watched")
            $ lc_discovery_mark("d2_knot_door")
            "I didn't say anything."
            "Every time she laughed, the loose string slipped a little further, and every time it somehow held."
            # Love lane (scene 16's else: Ryan and Leia stay at the pool): ends playful and warm.
            if get_story_value("ch01_d2_route_lane_pre_split", "love") not in ("ntr_risk", "exhibitionism"):
                "She turned around halfway through a laugh and caught me."
                gf "What? Why are you staring at me like that?"
                mc "No reason. Just looking."
                "She splashed me for it, then swam over and kissed me anyway. The knot held through that too."
            else:
                think "I should have said something. Part of me just wanted to see how long it would hold."

    $ set_story_flag("ch01_d2_scene_15_complete")

    jump ch01_day2_scene_16_forced_split



