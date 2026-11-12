# Leia's Consent — Chapter One: Something Different
# Day Two, Scenes 1–15.
#
# Day Two progression:
# - Love: Ryan stays attentive/protective without suppressing Leia's agency.
# - Exhibitionism: Ryan and Leia explore attention together.
# - NTR-risk: emotional disengagement, not consensual openness, creates pressure.

init 1 python:

    # Register Day Two choices with the existing central Choice Engine after it
    # has created CHOICE_EFFECTS / CHOICE_TAGS.
    CHOICE_EFFECTS.update({
        "ch01_dream_ground": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_dream_curiosity": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_dream_withdraw": [
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_morning_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_morning_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d2_morning_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        # Post-shop "You've been kind of quiet" menu: flavor since v0.2.0 (darryn).
        # Its question is now scored 25 lines later by the cafe incident below. The
        # repair tags stay, so these still pick which cafe talk Ryan overhears.
        "ch01_d2_postshop_sleep": [],  # Flavor: no stats
        "ch01_d2_postshop_head": [],  # Flavor: no stats
        "ch01_d2_postshop_shut_down": [],  # Flavor: no stats
        # Day Two incident (v0.2.0): Ryan overhears Leia and Maya at the cafe.
        "ch01_d2_overheard_own": [
            ("relationship", "trust", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d2_overheard_joke": [],  # Flavor: no stats
        "ch01_d2_overheard_pretend": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_maya_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_maya_tease_jealousy": [
            ("relationship", "love", 1),
        ],
        "ch01_d2_maya_open_honest": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_maya_include": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d2_maya_catchup": [],  # Neutral: no stats
        "ch01_d2_maya_dismiss_leia": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_photo_pair_encourage": [
            ("partner", "exhibitionism", 2),
        ],
        "ch01_d2_photo_pair_redirect": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_photo_pair_shrug": [
            ("relationship", "love", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_pool_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_d2_pool_honest_jealous": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_pool_accuse": [
            ("relationship", "trust", -2),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_sunset_connect": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_sunset_partial": [
            ("relationship", "trust", 1),
            ("relationship", "temptation", -1),
        ],
        "ch01_d2_sunset_ignore_gate": [
            ("relationship", "love", -3),
            ("relationship", "temptation", 5),
        ],
        "ch01_d2_bed_pool_love": [
            ("relationship", "love", 3),
            ("relationship", "temptation", -3),
        ],
        "ch01_d2_bed_pool_exhibition": [
            ("relationship", "love", 2),
            ("partner", "exhibitionism", 3),
        ],
        "ch01_d2_bed_pool_accuse": [
            ("relationship", "trust", -1),
            ("relationship", "temptation", 1),
        ],
        "ch01_d2_wink_repair": [
            ("relationship", "love", 3),
            ("relationship", "temptation", -3),
        ],
        "ch01_d2_wink_accuse_hard": [
            ("relationship", "love", -4),
            ("relationship", "trust", -5),
            ("relationship", "temptation", 5),
        ],
        "ch01_d2_wink_reject_hard": [
            ("relationship", "love", -5),
            ("relationship", "trust", -4),
            ("relationship", "temptation", 5),
        ],
    })

    CHOICE_TAGS.update({
        "ch01_dream_ground": ("supportive", "attentive", "love-route"),
        "ch01_dream_curiosity": ("open", "curious", "exhibitionism-seed"),
        "ch01_dream_withdraw": ("nonchalant", "withdrawal", "ntr-seed"),
        "ch01_d2_morning_reassure": ("supportive", "attentive", "love-route"),
        "ch01_d2_morning_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_d2_morning_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_postshop_sleep": ("supportive", "attentive", "honest", "repair"),
        "ch01_d2_postshop_head": ("attentive", "honest", "repair"),
        "ch01_d2_postshop_shut_down": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_overheard_own": ("attentive", "honest", "repair"),
        "ch01_d2_overheard_joke": ("neutral", "playful"),
        "ch01_d2_overheard_pretend": ("nonchalant", "withdrawal"),
        "ch01_d2_maya_reassure": ("supportive", "attentive", "reassuring"),
        "ch01_d2_maya_tease_jealousy": ("playful", "attentive"),
        "ch01_d2_maya_open_honest": ("open", "honest", "trusting"),
        "ch01_d2_maya_include": ("supportive", "attentive", "reassuring"),
        "ch01_d2_maya_catchup": ("neutral", "trusting"),
        "ch01_d2_maya_dismiss_leia": ("neutral", "nonchalant", "dismissive", "distracted"),
        "ch01_d2_photo_pair_encourage": ("encouraging", "open", "participating"),
        "ch01_d2_photo_pair_redirect": ("protective", "attentive", "boundary-setting"),
        "ch01_d2_photo_pair_shrug": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_pool_reassure": ("supportive", "attentive", "trusting"),
        "ch01_d2_pool_honest_jealous": ("protective", "honest", "attentive"),
        "ch01_d2_pool_accuse": ("protective", "nonchalant", "dismissive"),
        "ch01_d2_sunset_connect": ("supportive", "attentive", "love-route"),
        "ch01_d2_sunset_partial": ("attentive", "honest", "repair"),
        "ch01_d2_sunset_ignore_gate": ("neutral", "nonchalant", "dismissive", "distracted", "ntr-gate"),
        "ch01_d2_bed_pool_love": ("supportive", "attentive", "honest", "repair"),
        "ch01_d2_bed_pool_exhibition": ("encouraging", "open", "honest", "participating", "repair"),
        "ch01_d2_bed_pool_accuse": ("protective", "dismissive", "unresolved"),
        "ch01_d2_wink_repair": ("supportive", "attentive", "honest", "repair"),
        "ch01_d2_wink_accuse_hard": ("protective", "jealous", "accusatory", "ntr-confirm"),
        "ch01_d2_wink_reject_hard": ("neutral", "nonchalant", "dismissive", "ntr-confirm"),
    })


    def ch01_d2_choice_ids():
        return choice_ids_with_prefix("ch01_d2_")


    def ch01_d2_route_lane():
        """Resolve the active Day Two lane (stat model v2: lc_stat_model.d2_route_lane).

        NTR risk needs Temptation, with a Day One NTR seed or high enough on its
        own. The Love + Exhibitionism lane needs Exhibitionism plus some gained
        today. Protection and closeness never create NTR pressure. A save that
        was converted mid-Day-Two keeps its old lane until the day ends.
        """
        migrated = None
        if not has_story_flag("ch01_day_02_complete"):
            migrated = get_story_value("ch01_d2_lane_migrated", None)
        return lc_stat_model.d2_route_lane(
            lc_stats_flat(),
            get_story_value("ch01_day1_route_pressure", "mixed"),
            lc_exhib_gained("ch01_d2_"),
            focus=lc_route_explorer_for_lane(),
            migrated_lane=migrated,
        )


    def format_day2_risk_choice(choice_id, base_text, severity="soft"):
        """Risk-aware choice labels that respect the player's visibility mode."""
        mode = current_choice_mode()
        if mode == "normal":
            return base_text

        if severity == "hard":
            marker = "{color=#ff4242}◆◆{/color}"
            if mode == "insight":
                return "{} {}\n[Critical relationship choice]".format(marker, base_text)
            if mode == "full":
                return "{} {}\n[CRITICAL ROUTE CHOICE] [{}]".format(
                    marker, base_text, _choice_effect_text(choice_id, exact=True)
                )
            return "{} {}\n[CONFIRM NTR ROUTE] [{}]  [ID: {}]".format(
                marker, base_text, _choice_effect_text(choice_id, exact=True), choice_id
            )

        marker = "{color=#d85a5a}◆{/color}"
        if mode == "insight":
            return "{} {}\n[Major relationship consequence]".format(marker, base_text)
        if mode == "full":
            return "{} {}\n[MAJOR RELATIONSHIP CONSEQUENCE] [{}]".format(
                marker, base_text, _choice_effect_text(choice_id, exact=True)
            )
        return "{} {}\n[NTR GATE 1] [{}]  [ID: {}]".format(
            marker, base_text, _choice_effect_text(choice_id, exact=True), choice_id
        )


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
    think "Of course. He said eleven, so he'd set an alarm for eleven just to text us at eleven."

    "I eased out of bed as quietly as I could and looked back."

    scene cg ch01_d2_leia_sleeping
    with dissolve

    "[girlfriend_name] had claimed about three-quarters of the bed at some point in the night. One arm was flung over her head, the other was hanging off the edge, and her mouth was wide open like she was halfway through arguing with someone in her dream."
    "The duvet had lost the fight completely and was bunched somewhere around her knees."
    think "Four years, and she still sleeps like she fell out of a plane and landed here."
    mc "Hey. [friend_name]'s awake. Which means we're officially late."
    gf "Mmhh... five more... hours."
    mc "He sent 'Bro wake up.' That's the whole message. He's escalating."

    scene cg ch01_d2_leia_waking
    with dissolve

    "She dragged a fist across her face and blinked up at me, eyes not quite on duty yet."
    gf "Why are you standing? Why are you already standing, that's so aggressive."
    gf "And it's eleven-thirty. I negotiated eleven-thirty. He was there. You were there."
    mc "I'll tell him you said that."

    scene bg ch01_master_bedroom_curtains
    with dissolve
    $ cast(ryan="home", leia="camisole_panty")

    "I sat back down on the edge of the bed. She pulled half the duvet back over herself and looked at me like she'd just remembered something and hadn't decided yet whether to bring it up."

    if get_story_value("ch01_dream_response") == "grounded":
        "The dream still existed somewhere at the back of my mind, but daylight had put it back where it belonged."
    elif get_story_value("ch01_dream_response") == "curious":
        "The dream had lost its sharp edges by morning. The uncomfortable question it left behind had not."
    elif get_story_value("ch01_dream_response") == "withdrew":
        "I had managed not to think about the dream again. Mostly. Keeping it there felt easier than examining it."

    # Day One echo: the upstairs talk before movie night (ch01_upstairs_response).
    # honest/liked = the loving path, so Ryan thanks her (out loud and in his head).
    if get_story_value("ch01_upstairs_response") == "honest":
        "She caught me watching her and smiled into the pillow."
        gf "You know you carried me up those stairs like a sack of laundry last night, right? I had a whole step digging into my hip."
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
        gf "That sounded suspiciously easy. You didn't even zoom in."
        mc "I don't need to zoom in. You're asking me if I like a photo of my girlfriend, babe. It's not a hard question."
        gf "That's actually a good answer. Annoyingly."

    if len(d2_morning_pool_photos) >= 2:
        "[girlfriend_name] swiped to the next photo."
        $ renpy.scene()
        $ renpy.show("cg " + d2_morning_pool_photos[1])
        with dissolve

        if d2_morning_withdrew:
            "She studied it quietly this time, no longer asking me to judge it."
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
            "[girlfriend_name] lingered on it for a second, then locked the phone without asking."
        elif get_story_value("ch01_dream_response") == "curious":
            gf "I definitely wasn't this comfortable at the start. Not even close."
            mc "No. You really weren't."
            gf "Is that a bad thing?"
            "There was no accusation in the question. She genuinely wanted to know."
            mc "I don't know yet. I mean, I don't think so. I just don't know what it is yet."
            gf "That's honest, at least. I'll take honest."
        else:
            gf "That one. That's my favorite, final answer."
            mc "I thought the last one was your favorite."
            gf "I'm allowed to change my mind, it's my face."
            mc "In the last four seconds?"
            gf "That's called growth, babe."

    scene bg ch01_master_bedroom_curtains  # Day 2 morning: day art (darryn)
    with dissolve
    $ lc_phone_clear_story_time()
    $ cast(ryan="home", leia="camisole_panty")

    gf "You were a menace last night, by the way. During the movie. Don't think I forgot."
    mc "Good morning to you too."
    gf "I'm serious. I spent half that movie trying to act normal."
    mc "You were the one who kept checking if he was looking."

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
    gf "I'm showering before [friend_name] starts texting the group about us hibernating. He did say eleven."
    mc "He'd have to be awake first."
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
    "Breakfast started with the kind of easy rhythm we'd found by the end of yesterday."
    $ exit_cinematic_mode()
    scene bg ch01_d2_breakfast
    with dissolve
    with dissolve

    friend "Oh, look who's alive. I was about to send a search party. I had a whole message drafted and everything."
    gf "Barely. Your couch ate my back."
    friend "That's because you spent half the movie rearranging yourself every thirty seconds. I counted. Well, I stopped counting, but I started."

    "[girlfriend_name]'s eyes moved directly to mine."

    mc "Maybe your movie was making her uncomfortable. Did you think about that?"
    friend "My movie was art. It won awards. Small ones. Online ones, but still."
    gf "Your movie had a shark driving a speedboat, [friend_name]. Like, at the wheel."
    friend "And did anyone look away? No. Because it was art."

    "Breakfast settled into the easy rhythm we'd found by the end of yesterday."

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
        "Small, ordinary, automatic. Four years reduced to a gesture neither of us noticed anymore."
    else:
        gf "Coffee?"
        mc "Only if you're admitting you stole the duvet."
        gf "I admit nothing. The duvet came to me."
        "She poured it anyway."

    $ set_story_flag("ch01_d2_scene_02_complete")
    jump ch01_day2_scene_03_maya_message


label ch01_day2_scene_03_maya_message:

    "My phone buzzed beside the coffee."
    "Maya's name appeared on the screen."

    centered "MAYA: You people alive? I'm near the resort around lunch. Still meeting?"

    "[girlfriend_name] saw the name before I put the phone down."

    gf "Oh."
    mc "What?"
    gf "Nothing."
    friend "That was the loudest 'nothing' I've ever heard."

    gf "So this is the Maya I've heard about."
    mc "You've heard about her."
    gf "Mm."
    mc "What does that mean?"
    gf "Nothing."

    "[friend_name] lowered his coffee."
    friend "We're doing 'nothing' again?"

    gf "Shut up."
    "She looked back at me, trying and failing to make the next question sound casual."
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
            gf "Nobody asked you."

        "[d2_maya_honest_text]":
            $ apply_choice("ch01_d2_maya_open_honest")
            mc "Yeah. She's attractive. She's also just my friend."
            "[girlfriend_name] considered that for a second."
            gf "Okay."
            mc "Okay?"
            gf "I asked. You answered."
            "There was something almost deliberate about how easily she accepted it."

    if get_story_value("ch01_dream_response") == "withdrew":
        "Her answer should have reassured me. Instead, I found myself wondering whether I had been offering her the same honesty since I woke up."

    $ set_story_flag("ch01_d2_maya_meetup_confirmed")
    jump ch01_day2_scene_04_jealousy_callback


label ch01_day2_scene_04_jealousy_callback:

    with dissolve

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
        gf "Oh, so now I'm being reviewed. Great. No pressure."

    "Whatever tiny tension had been there stayed small enough to joke about."

    # If Ryan answered Maya while the phone prompt was available, the next two
    # breakfast stills show Leia softening and Julian realizing he was staring.
    if get_story_value("ch01_d2_maya_lunch_reply"):
        $ enter_cinematic_mode()
        scene cg ch01_d2_breakfast_03
        with dissolve
        "[girlfriend_name]'s pout softened despite herself."
        scene cg ch01_d2_breakfast_04
        with dissolve
        "[friend_name] suddenly became very interested in his mug."
        $ exit_cinematic_mode()
        scene bg ch01_d2_breakfast
        with dissolve

    $ set_story_flag("ch01_d2_scene_04_complete")
    jump ch01_day2_scene_05_meet_maya


label ch01_day2_scene_05_meet_maya:

    scene bg ch01_d2_cafe
    with fade
    # Café outfits only: Maya's green tube top and Leia's white camisole.
    # Maya's base includes her neutral face; her separate expression PNGs overlay it.
    $ cast(ryan="casual", leia="lounge", julian="travel", maya="green_tube_top")

    "Maya spotted us before I spotted her."
    $ enter_cinematic_mode()
    scene cg ch01_d2_maya_reveal
    with dissolve
    "A small day bag hung from one shoulder, looking more prepared for an island afternoon than the rest of us were."

    maya "[player_name]! Wait, you're tan? Since when do you tan?"

    $ exit_cinematic_mode()
    scene bg ch01_d2_cafe
    with dissolve
    $ cast(ryan="casual", leia="lounge", julian="travel", maya="green_tube_top")
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
    gf "Finally? Wait, how long have you been waiting?"
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
    gf "Bad stuff. There's a lot of bad stuff, where do I even start?"
    maya "Start here. I need to know one thing."
    gf "That sounds threatening. Okay. Go."
    maya "Has he always taken twenty minutes to decide what to eat?"
    gf "Oh my God. Yes. Every single time."
    $ exit_cinematic_mode()
    scene bg ch01_d2_cafe
    with dissolve
    $ cast(ryan="casual", leia="lounge", julian="travel", maya="green_tube_top")
    mc "This is character assassination. I'd like that on the record."
    gf "He reads the entire menu, picks something, changes his mind, asks the waiter what's good, and then orders the first thing anyway."
    $ face("maya", "skeptical")
    maya "He used to do that at lunch! With a sandwich menu. Six sandwiches."
    gf "He still does it at dinner. He did it last night."

    "They looked at each other like two people who'd been studying the same flaw from opposite ends for years."
    mc "I regret this meeting already. Can we go back to before you two met?"

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

    $ exit_cinematic_mode()
    scene bg ch01_d2_cafe
    with dissolve
    $ cast(ryan="casual", leia="lounge", julian="travel", maya="green_tube_top")
    maya "What about you? Holiday person or itinerary person?"
    $ face("leia", "smile")
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
    think "Yesterday I'd been the photographer in this relationship. Apparently that had a shelf life. At least I was the one she'd been looking at."

    "[friend_name] looked at me over his drink."

    friend "You know you've completely lost control of this, right? This is their table now. We're just sitting at it."
    mc "Yeah. I think introducing them was a mistake."
    gf "Too late. I like her, she's staying."
    maya "Same. I'm keeping her."

    "It was said jokingly, but [girlfriend_name]'s posture had changed. She wasn't [player_name]'s girlfriend meeting [player_name]'s friend anymore. She was talking to Maya on her own terms."

    $ set_story_value("ch01_d2_leia_maya_comfort", 2)
    $ set_story_flag("ch01_d2_scene_07_complete")
    jump ch01_day2_scene_08_maya_julian


label ch01_day2_scene_08_maya_julian:

    "Maya's attention eventually shifted to [friend_name]."

    maya "So you're the rich one."
    friend "Apparently that's my entire personality now."
    maya "No, the sunglasses are your personality. The money is supporting cast."

    "[friend_name] laughed despite himself. [girlfriend_name] leaned toward me."

    gf "They get along."
    mc "She insults people she likes."
    gf "That explains you."

    "A bee wandered close to the table."
    "[friend_name] stopped mid-sentence and leaned sharply away from it."

    maya "...Are you scared of bees?"
    friend "No."
    maya "You moved six inches without using your feet."
    friend "I respect bees. From a distance."
    gf "Oh my God."

    "The bee left. The information did not."

    maya "I'm remembering that."
    friend "For what possible reason?"
    maya "I don't know yet. That's what makes it exciting."
    gf "I support this."
    friend "[player_name]."
    mc "I can't help you anymore."

    "For the first time since Maya arrived, the four of us felt less like two existing friendships forced around one table and more like an actual group."

    $ set_story_flag("ch01_d2_julian_bee_fear_seeded")
    $ set_story_flag("ch01_d2_scene_08_complete")
    jump ch01_day2_scene_09_photo_walk


label ch01_day2_scene_09_photo_walk:

    scene bg ch01_d2_island_day
    with dissolve
    # No walk/pool/boutique outfits for Maya yet: avoid carrying the café cast.
    $ cast()

    "After brunch, Maya turned a walk through the island shops into a photography project."

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

    maya "Okay! Group photo first. Then combinations."
    friend "Combinations? What does that mean? How many combinations?"
    maya "All of them. You people took one decent photo yesterday, and now I have standards to live up to."

    "The first group photo took three attempts because [friend_name] blinked in two of them."
    friend "The sun is aggressive today. That's not on me."
    maya "It's your eyelids. Your eyelids are the problem."
    maya "Wait—can I join the Trip Group? And can we use this one for the picture, or do you want another try?"
    gf "Yes, add her! And use this one, because we're all in it and [friend_name] actually has his eyes open."
    friend "I do, somehow. Hang on, I'll add Maya and change the picture before we forget which one it was."
    $ phone_group_maya_member = True
    $ phone_add_message("group", "system", text=friend_name + " added Maya to the group.", message_id="ch01_trip_group_maya_added", mark_unread=False)
    $ phone_group_avatar_stage = "four"
    $ phone_add_message("group", "system", text=friend_name + " changed the group picture.", message_id="ch01_trip_group_four_photo", mark_unread=False)

    "Then Maya started assigning pairs like a teacher on school photo day."

    "We took the obvious ones first: all four of us, [girlfriend_name] and me, Maya and me, [friend_name] and Maya."

    $ set_story_flag("ch01_d2_photo_group")
    $ set_story_flag("ch01_d2_photo_ryan_leia")
    $ set_story_flag("ch01_d2_photo_ryan_maya")
    $ set_story_flag("ch01_d2_photo_julian_maya")

    jump ch01_day2_scene_10_leia_maya_photo


label ch01_day2_scene_10_leia_maya_photo:

    $ enter_cinematic_mode()
    scene cg ch01_d2_photo_leia_maya
    with dissolve

    "Maya hooked an arm around [girlfriend_name] and immediately ruined her attempt at a careful pose by making her laugh."
    "The resulting photo looked better than anything either of them had planned."

    maya "See? That's the one. You stopped thinking about the camera."
    gf "Easy for you to say, you look like that in every photo."
    maya "Correct. I'm extremely photogenic. It's a curse."
    gf "You made me laugh on purpose, though. That's cheating."
    maya "That's not cheating, that's technique. You owe me photography credit now."
    gf "Absolutely not. I'm not crediting you."

    "[girlfriend_name] was still smiling when she looked at the result."

    $ exit_cinematic_mode()
    scene bg ch01_d2_island_day
    with dissolve

    "[girlfriend_name] saved the photo immediately."

    $ set_story_flag("ch01_d2_photo_leia_maya")
    $ set_story_flag("ch01_d2_scene_10_complete")
    jump ch01_day2_scene_11_missing_pair


label ch01_day2_scene_11_missing_pair:

    maya "Wait, wait. We're missing one."
    friend "Are we? I think we got everybody. We got everybody, right?"
    maya "[girlfriend_name] and [friend_name]. You two haven't had one."

    "[girlfriend_name] looked at [friend_name], then at me."

    $ d2_pair_encourage_text = format_choice("ch01_d2_photo_pair_encourage", "Go on. Complete the set.")
    $ d2_pair_redirect_text = format_choice("ch01_d2_photo_pair_redirect", "We've got enough photos. Come here, babe.")
    $ d2_pair_shrug_text = format_choice("ch01_d2_photo_pair_shrug", "Mm? Yeah, sure. Go ahead.")

    menu:
        "[d2_pair_encourage_text]":
            $ apply_choice("ch01_d2_photo_pair_encourage")
            $ set_story_value("ch01_d2_leia_julian_photo", "taken")
            mc "Go on. Complete the set."
            gf "Wow, okay. You're very enthusiastic about this."
            mc "It's for the album. Historical documentation."
            friend "I hate all of you. Fine. Where do you want me? Here?"
            "[girlfriend_name] stood beside [friend_name] for the photo. It was harmless. The fact that she checked my reaction first was the more interesting part."

        "[d2_pair_redirect_text]":
            $ apply_choice("ch01_d2_photo_pair_redirect")
            $ set_story_value("ch01_d2_leia_julian_photo", "redirected")
            mc "We've got enough photos. Come here, babe."
            "[girlfriend_name] came back toward me without argument."
            gf "Possessive photographer. Okay. I'll allow it."
            mc "Sorry. I just wanted you over here."

        "[d2_pair_shrug_text]":
            $ apply_choice("ch01_d2_photo_pair_shrug")
            $ set_story_value("ch01_d2_leia_julian_photo", "shrugged")
            mc "Mm? Yeah, sure, go ahead."
            "I was still squinting at the map on my phone. [girlfriend_name]'s eyes stayed on me a little longer than they needed to."
            gf "Okay."
            "She took the photo with [friend_name]. It was ordinary. I just hadn't looked up for it."

    $ set_story_flag("ch01_d2_scene_11_complete")
    jump ch01_day2_scene_11b_boutique


label ch01_day2_scene_11b_boutique:

    friend "Before we head back, can we stop for a second? I need a shirt. The one I brought got sunscreen all down the front."
    maya "You're wearing a shirt. You own, like, twelve versions of that exact shirt, I can tell."
    friend "So this one would be the thirteenth. That's not the argument you think it is."

    $ enter_cinematic_mode()
    scene cg ch01_d2_mall_arrival
    with dissolve
    "The mall stop was supposed to take five minutes."
    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve
    "[friend_name] disappeared toward a menswear rack. Maya made it approximately three storefronts before stopping dead outside a boutique."

    maya "Oh. Oh, no."
    gf "Why did you say that like that?"
    maya "Come with me. Just come look, that's all."
    gf "No. I know that voice."
    maya "You haven't even seen what I'm looking at."
    gf "I've known you for, like, four hours, and I already know that voice."

    "[girlfriend_name] still followed her inside."

    "Maya chose a red asymmetric cutout mini almost immediately. [girlfriend_name] was slower."
    "She stopped in front of a rack and stared at one outfit long enough for Maya to notice."

    maya "That one. You want that one."
    gf "What? I'm just looking."
    maya "You've been staring at it for a full minute."
    gf "I have not! I was looking at the... the stitching."
    maya "The stitching. Okay. You absolutely have."

    "[girlfriend_name] had been looking at something daring but still recognizably within reach."
    "Maya looked beside it, found a much smaller black halter mini built from deep cutouts and two precarious front panels, and smiled."

    maya "Oh, no. No, actually, you're trying this one."
    gf "That's not even the one I was looking at."
    maya "I know. This one's better. Trust me."
    gf "Maya, no. Look at it. How does it even stay on?"
    maya "That's what the changing room is for. Go find out."

    "[girlfriend_name] stared at the black dress, then at Maya."
    gf "I'm not wearing that outside. Ever."
    maya "I didn't say outside! I said try it. Nobody's buying anything."
    gf "Why? What's the point if I'm not wearing it?"
    maya "Because you've been staring at that rack like it owes you money, and I want to see your face when you see yourself in it. Only if you want to, though. I'm serious."

    "[girlfriend_name] hesitated, then took the hanger from her."
    $ set_story_flag("ch01_d2_maya_pushed_boutique_tryon")
    $ set_story_value("ch01_d2_boutique_trial_outfit", "boutique_cutout_mini")

    $ enter_cinematic_mode()
    scene cg ch01_d2_boutique_changing_room
    with dissolve

    "Maya's red dress fit as if she'd picked it for herself a hundred times before."
    "[girlfriend_name]'s was another matter."
    "She stood in front of the mirror holding the two triangular front panels securely against herself while Maya worked out the straps behind her."

    gf "This isn't a dress. This is, like, a suggestion of a dress."
    maya "You're wearing it, so it's a dress. That's how dresses work."
    gf "If I move my hand, I'm getting banned from this mall."
    maya "Only because I haven't done the straps yet. Hang on. Don't move."
    gf "'Don't move' is not making me feel better, Maya."

    "Maya moved behind her, took over the tension in the straps and carefully pulled the top into place."

    gf "How is yours more revealing and somehow more secure?"
    maya "Years of practice. And tape. Mostly tape."
    gf "That's not how clothes work. That can't be how clothes work."
    maya "It's exactly how clothes work. Breathe in."

    "Maya's teasing softened when she looked at [girlfriend_name] in the mirror."

    maya "Hey. Seriously, though. You look really good."
    gf "I look terrified. Look at my face, that's a terrified face."
    maya "Both can be true. Terrified and hot. That's a whole look."

    "[girlfriend_name] looked at herself again. This time she didn't immediately cover more of the dress."

    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve

    gf "[player_name]? Are you still out there?"
    mc "Yeah, I'm here. What's up?"
    gf "Can you come here for a second? I need a second opinion. Yours."

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
                "Whatever distance had been building between us, she had asked for me."
                "I went over."

            "[d2_mall_leave_text]":
                $ apply_choice("ch01_d2_mall_leave_to_maya")
                $ set_story_value("ch01_d2_mall_ryan_response", "ignored")
                $ d2_mall_ryan_present = False
                mc "Maya's better at this than me. I'll just get in the way."
                "There was a short pause from behind the curtain."
                gf "...Okay."
    else:
        $ set_story_value("ch01_d2_mall_ryan_response", "came_over")
        "I headed toward the changing rooms."

    if d2_mall_ryan_present:
        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_reveal_ryan
        with dissolve

        "Maya opened the curtain while standing behind [girlfriend_name], both hands still responsible for keeping the black top properly tensioned."
        "[girlfriend_name] looked considerably less certain than Maya did."

        gf "Well? Say something, I'm dying here."

        $ d2_mall_affection_text = format_choice("ch01_d2_mall_reveal_affection", "You look incredible.")
        $ d2_mall_open_text = format_choice("ch01_d2_mall_reveal_open", "Didn't know you had that in you.")
        $ d2_mall_tease_text = format_choice("ch01_d2_mall_reveal_tease", "Maya really did this to you?")
        $ d2_mall_flat_text = format_choice("ch01_d2_mall_reveal_flat", "It's... nice.")

        menu:
            "[d2_mall_affection_text]":
                $ apply_choice("ch01_d2_mall_reveal_affection")
                mc "You look incredible."
                "[girlfriend_name]'s shoulders relaxed a little."
                gf "You have to say that. You're biased."
                mc "Very biased. Still true, though."

            "[d2_mall_open_text]":
                $ apply_choice("ch01_d2_mall_reveal_open")
                mc "Didn't know you had that in you."
                gf "I don't! I didn't. Maya put it there, this is all Maya."
                maya "You're welcome. Both of you."

            "[d2_mall_tease_text]":
                $ apply_choice("ch01_d2_mall_reveal_tease")
                mc "Maya really did this to you?"
                gf "Against my better judgment, yes. Very much against it."
                maya "Her judgment's getting better, actually. We're working on it."

            "[d2_mall_flat_text]":
                $ apply_choice("ch01_d2_mall_reveal_flat")
                mc "It's... yeah. It's nice."
                gf "Nice."
                maya "Nice? She looks like that and you've got 'nice'?"
                mc "I mean really nice. I just— I wasn't ready for it."
                "[girlfriend_name] tugged the top a little higher and didn't ask me again."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve

    else:
        maya "[friend_name]!"
        gf "Maya—"
        maya "What? We need a second opinion, and he's right there."

        "[friend_name] appeared from the next section holding two nearly identical shirts."

        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_reveal_julian
        with dissolve

        friend "Oh."
        maya "'Oh'? That's all you've got?"
        friend "I— sorry, I wasn't ready for a test. I came over here about shirts. Nobody said there'd be a test."
        gf "Don't encourage her. Please."
        friend "You look good, though. Really. Okay. I'm going back to the shirts."
        gf "...Thanks."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve

    "Maya was still holding [girlfriend_name]'s top securely when something over [girlfriend_name]'s shoulder caught her attention."
    maya "Wait— oh my God. Look. That one."
    gf "What?"
    maya "That. On the display. Look at it."

    "A metallic mesh mini hung on a nearby display in deep crimson: a plunging draped front, delicate chain straps and a slit cut almost to the hip."

    gf "You're already wearing red."
    maya "Not for me, for you! You, in that, at dinner."
    gf "Absolutely not. I'm still in this one."
    maya "[girlfriend_name], look at it—"

    "Maya turned and reached toward the display without properly releasing the tension she was holding."
    "One side of [girlfriend_name]'s black top immediately slipped."

    gf "Maya!"

    if d2_mall_ryan_present:
        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_slip_ryan
        with dissolve

        "[girlfriend_name] caught the loose panel almost immediately and clamped it back into place."
        "Maya froze, horrified."
        maya "Sorry! Sorry, sorry, I've got it, I've got it."
        gf "You had one job, Maya. One."
        maya "I know! I got distracted by the other dress, it's a very good dress."
        gf "I can't believe this is happening in a shop."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve
        $ set_story_value("ch01_d2_boutique_slip_witness", "ryan")

    else:
        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_slip_julian
        with dissolve

        "[girlfriend_name] caught the loose panel and pulled it back into place."
        "But [friend_name] had already seen the slip."
        "His eyes stayed there longer than they should have."
        "Then a second longer than that."
        "[girlfriend_name] looked up and caught him staring."
        "Their eyes met."
        "That was what finally made [friend_name] look away."

        "Maya, focused entirely on fixing the top, missed the exchange."

        maya "Sorry! Sorry, sorry, I've got it, I've got it."
        gf "You had one job, Maya. One."
        maya "I know! I got distracted by the other dress, it's a very good dress."
        gf "I can't believe this is happening in a shop."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve
        $ set_story_flag("ch01_d2_leia_noticed_julian_stare")
        $ set_story_value("ch01_d2_boutique_slip_witness", "julian")

    "Maya glanced back toward the crimson mesh dress."
    maya "I still think you'd look amazing in that one. Just saying."
    gf "I'm changing. Into my own clothes. Right now."
    maya "So that's a maybe."
    gf "That's a no, Maya."

    "A few minutes later they emerged in their normal clothes. Maya had bought the red dress without hesitation."
    "[girlfriend_name] still had the black mini over one arm."

    if d2_mall_ryan_present:
        $ set_story_flag("ch01_d2_boutique_shop_open")
        if LC_SHOP_ENABLED:
            "The boutique's catalogue was available through the Shop on my phone. Buying something would add it to [girlfriend_name]'s wardrobe; whether she actually agreed to wear it later was a separate question."
            $ last_shop_message = "Boutique visit: the Black Cutout Mini is now available."
            call screen shop_screen
        else:
            # The Shop is switched off while it's under development
            # (LC_SHOP_ENABLED); the purchase happens as an in-story choice.
            "I could buy it for her. Whether she actually agreed to wear it later was a separate question."
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

    "[friend_name] eventually returned with a shopping bag."

    maya "That's literally the shirt you're already wearing."
    friend "No, this one's different."
    maya "How? Tell me one way it's different."
    friend "It's... new. It's a new one."

    "We stepped back outside into the early-afternoon heat with considerably more shopping than [friend_name]'s five-minute shirt stop had promised."

    maya "Drink before we go back? I'm melting."
    gf "Please. Yes. Something with ice."

    "We found a table nearby and dropped the shopping bags around our feet."

    maya "Okay, that went way better than I expected."
    gf "For who? Better for who, exactly?"
    maya "For me. Obviously."
    gf "Trying something on and wearing it are completely different things."
    maya "That's what fitting rooms are for, though. That's the whole point of them."

    friend "For what it's worth, I think you should keep it. Even if it just lives in your suitcase. It's a nice thing to have."
    gf "Thanks, [friend_name]."
    maya "See? He agrees with me."
    gf "You don't get credit for his opinion. That's not how opinions work."

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
            mc "You caught it, though. Really fast."
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
        gf "The top slipped a little. When Maya was grabbing the other dress."
        mc "Oh."
        gf "[friend_name] was there."
        "I looked at her."
        gf "He looked away."
        "The way she said it wasn't defensive. It was simply the version of events she'd been left to process without me."

    gf "You've been kind of quiet today, though. Not in a bad way. Just quiet."

    $ d2_postshop_sleep_text = format_choice("ch01_d2_postshop_sleep", "I didn't sleep well.")
    $ d2_postshop_head_text = format_choice("ch01_d2_postshop_head", "I've just got a lot in my head.")
    $ d2_postshop_shut_text = format_choice("ch01_d2_postshop_shut_down", "I'm fine.")

    menu:
        "[d2_postshop_sleep_text]":
            $ apply_choice("ch01_d2_postshop_sleep")
            mc "I didn't sleep well."
            gf "Yeah, I noticed. You kept doing the thing with the pillow."
            mc "Sorry. I didn't mean to keep you up."
            gf "You don't have to apologize for being tired, babe. I just wanted to know you're okay."
            "It wasn't the whole truth, but at least I had stopped pretending there was nothing to explain."

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

    "[friend_name] stood and picked up his shopping bag."
    friend "I'm getting another drink before we go. Anyone want anything? [player_name], come help me carry."
    mc "Yeah, I'll come."

    "We left [girlfriend_name] and Maya at the table for a minute."
    "[friend_name] was still losing an argument with the card machine when the first two drinks came up, so I carried them back on my own."
    "There was a big potted palm between the counter and our table. I was a couple of steps behind it when Maya lowered her voice."

    maya "Hey. Everything okay?"
    gf "With the dress? I mean, I bought it, so."
    maya "No. With [player_name]."

    "I stopped walking."

    # Day Two incident (v0.2.0): Ryan overhears the talk. The milder version plays
    # when he has already been present today (a repair pick, or he went to her at the mall).
    if choice_tag_count("repair", ch01_d2_choice_ids()) >= 1 or get_story_value("ch01_d2_mall_ryan_response") in ("reconnected", "came_over"):
        $ set_story_value("ch01_d2_overheard_talk", "mild")
        gf "Yeah. I think so. He's just in his head today, he gets like that sometimes."
        maya "People are allowed weird days. He's always been a bit like that. He goes quiet, and then he comes back."
        gf "That's very insightful, actually."
        maya "I know. I'm extremely emotionally intelligent. It's my best feature after my legs."
        gf "Obviously. The legs are good."
        think "It was kind, and it was about me, and I was hearing it from behind a plant."
    else:
        $ set_story_value("ch01_d2_overheard_talk", "worried")
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
        "Maya, who I'd known for years, was explaining me to my girlfriend, who'd met her that morning."
        think "Neither of them had said one unfair thing. Somehow that was the part that stung."

    $ d2_overheard_own_text = format_choice("ch01_d2_overheard_own", "Put the drinks down and own it.")
    $ d2_overheard_joke_text = format_choice("ch01_d2_overheard_joke", "Walk in loud: 'Is this the support group? Do I get a badge?'")
    $ d2_overheard_pretend_text = format_choice("ch01_d2_overheard_pretend", "Step back, count to five, and come in like you heard nothing.")

    menu:
        "[d2_overheard_own_text]":
            $ apply_choice("ch01_d2_overheard_own")
            $ set_story_value("ch01_d2_overheard_response", "owned")
            "I put the drinks down in front of them."
            mc "So, I heard that. You're both right, which is annoying. I've been weird today. Can I tell you about it later? Just us."
            gf "Oh my God. How much did you hear?"
            mc "Enough. It's fair."
            "Maya picked up her drink and became extremely interested in the menu board."
            gf "...Later. Just us. I'm holding you to it."

        "[d2_overheard_joke_text]":
            $ apply_choice("ch01_d2_overheard_joke")
            $ set_story_value("ch01_d2_overheard_response", "joked")
            mc "Is this the [player_name] support group? Do I get a badge?"
            maya "You get a drink. Sit down."
            "[girlfriend_name] went red and laughed into her hands. I sat down, and nobody said anything real after that."

        "[d2_overheard_pretend_text]":
            $ apply_choice("ch01_d2_overheard_pretend")
            $ set_story_value("ch01_d2_overheard_response", "pretended")
            "I stepped back behind the palm, counted to five, and walked up like I'd come straight from the counter."
            mc "Drinks. [friend_name]'s still fighting the card machine."
            "[girlfriend_name] smiled up at me like nothing had happened."
            think "If she had something to say, she could say it to me. Apparently Maya got to hear it first."

    "By the time [friend_name] got back with the rest, Maya had deliberately moved the conversation back to clothes."
    maya "For the record, I'm still saying the black one."
    gf "And I'm still saying fitting room only. Fitting room and suitcase."
    maya "For now. Fitting room for now."
    gf "You're exhausting. I love it, but you're exhausting."

    $ set_story_flag("ch01_d2_scene_11b_boutique_complete")
    jump ch01_day2_scene_12_villa_pool_plan


label ch01_day2_scene_12_villa_pool_plan:

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

    "Maya stopped just inside."

    maya "Wait. Wait, wait."
    maya "This is where you're staying? This? All of this?"
    friend "Yeah. It's, um. Yeah. Do you want a drink? We have drinks."

    "She looked around the living room, then back at [friend_name]."

    maya "The sunglasses make sense now."
    friend "Can we not do the sunglasses again? Please? Thank you."
    maya "That wasn't a compliment, but you're welcome."

    gf "Come on, I'll show you around. Wait till you see the bathroom, it's ridiculous."
    "Yesterday [girlfriend_name] had been the newcomer. Today she was the one leading Maya through the villa like she'd already learned its shape."

    "They made it as far as the view outside before Maya stopped again."

    maya "Hold on. Is that a private pool?"
    friend "Yeah. I mean, it's not that big."
    maya "You didn't think that was relevant information? You let me talk about the resort pool for ten minutes."
    friend "Relevant to what? You didn't ask."
    maya "To everything! It's relevant to everything."

    gf "We were in it all afternoon yesterday."
    maya "And nobody told me to bring a swimsuit?"

    "Maya paused, then looked down at the day bag she'd been carrying since the café."

    maya "Actually—wait. I did bring one."
    gf "Wait, you just carry a swimsuit around with you?"
    maya "We're on an island, [girlfriend_name]. I always have a swimsuit. Always."
    gf "That's actually smart. I hate that it's smart."

    maya "Come change with me? You can show me where everything is."
    gf "Sure, but I barely know where anything is either. I've been here one day."
    maya "One day more than me. That makes you the tour guide."

    "[girlfriend_name] led her upstairs while [friend_name] and I dealt with drinks outside."

    $ set_story_flag("ch01_d2_scene_12_complete")
    jump ch01_day2_scene_13_girls_upstairs


label ch01_day2_scene_13_girls_upstairs:

    scene bg ch01_master_bedroom
    with dissolve

    "Upstairs, [girlfriend_name] laid both of her swimsuits across the bed while Maya pulled her own from the day bag and changed beside her."

    maya "You brought options."
    gf "One is safe. One requires confidence."
    maya "Which one do you want to wear?"

    "Yesterday [girlfriend_name] had asked me that question. Today she had to answer it herself."

    if lc_stat("exhibitionism") >= LC_T["d2_pool_outfit_bold"]:
        $ set_story_value("ch01_d2_pool_outfit", "pool_bolder")
        gf "The new one."
        maya "Oh."
        gf "What?"
        maya "Nothing. I'm updating my understanding of you."
        gf "Shut up."
    else:
        $ set_story_value("ch01_d2_pool_outfit", "pool_conservative")
        gf "I think the comfortable one today."
        maya "Then that one."
        gf "You're surprisingly reasonable."
        maya "Don't spread that around."

    $ grant_story_outfit(get_story_value("ch01_d2_pool_outfit"), equip=True)
    $ set_story_flag("ch01_d2_scene_13_complete")
    jump ch01_day2_scene_14_tie_foreshadow


label ch01_day2_scene_14_tie_foreshadow:

    if get_story_value("ch01_d2_pool_outfit") == "pool_bolder":
        "[girlfriend_name] tied the top while still talking to Maya, fingers moving faster than her attention."
        maya "That tie secure?"
        "[girlfriend_name] glanced down and gave it a small tug."
        gf "Should be fine."
        maya "Famous last words."
        gf "It's fine."
        $ set_story_flag("ch01_d2_bikini_tie_loose")
    else:
        "[girlfriend_name] changed into the swimsuit she already trusted while Maya borrowed the mirror and most of the counter space."
        maya "You know what I like about you?"
        gf "We've known each other four hours."
        maya "Exactly. Low sample size. No pressure."

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
    mc "You survived a bee today. You'll survive a splash."

    "Then [friend_name] sent me inside for towels. When I came back out, Maya and [girlfriend_name] had their heads together on one lounger."
    maya "—so he has no idea? None at all?"
    gf "None. And you are not allowed to—"
    "They both saw me at the same time and stopped."
    gf "Hi! Towels. Amazing. Thank you."
    maya "We were talking about sunscreen."
    gf "Very boring sunscreen stuff."
    "She was grinning at me over the towels, the way she does when she's planning something and is terrible at hiding it."
    think "Nobody in history has said 'very boring sunscreen stuff' about actual sunscreen."

    "The mood was easy. Whatever happened next would come from the choices already accumulating beneath it."

    $ set_story_value("ch01_d2_route_lane_pre_split", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_15_complete")

    jump ch01_day2_scene_16_forced_split

