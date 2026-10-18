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
            ("partner", "curiosity", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_dream_withdraw": [
            ("relationship", "boredom", 1),
        ],
        "ch01_d2_morning_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_morning_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_d2_morning_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
        ],
        "ch01_d2_postshop_sleep": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
            ("relationship", "boredom", -1),
        ],
        "ch01_d2_postshop_head": [
            ("relationship", "trust", 1),
            ("relationship", "boredom", -1),
        ],
        "ch01_d2_postshop_shut_down": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
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
            ("relationship", "boredom", -1),
        ],
        "ch01_d2_maya_catchup": [
            ("relationship", "trust", 1),
        ],
        "ch01_d2_maya_dismiss_leia": [
            ("relationship", "love", -2),
            ("relationship", "boredom", 2),
            ("partner", "temptation", 1),
        ],
        "ch01_d2_photo_pair_encourage": [
            ("partner", "curiosity", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_d2_photo_pair_redirect": [
            ("relationship", "trust", 1),
            ("player", "jealousy", 1),
        ],
        "ch01_d2_photo_pair_shrug": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
        ],
        "ch01_d2_pool_reassure": [
            ("relationship", "trust", 2),
            ("relationship", "love", 1),
            ("relationship", "boredom", -1),
        ],
        "ch01_d2_pool_honest_jealous": [
            ("relationship", "trust", 1),
            ("player", "jealousy", 2),
        ],
        "ch01_d2_pool_accuse": [
            ("relationship", "trust", -2),
            ("relationship", "love", -1),
            ("relationship", "boredom", 2),
            ("partner", "temptation", 1),
        ],
        "ch01_d2_sunset_connect": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
            ("relationship", "boredom", -2),
        ],
        "ch01_d2_sunset_tease": [
            ("relationship", "love", 1),
            ("partner", "curiosity", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_d2_sunset_partial": [
            ("relationship", "trust", 1),
            ("relationship", "boredom", -1),
        ],
        "ch01_d2_sunset_ignore_gate": [
            ("relationship", "love", -3),
            ("relationship", "trust", -2),
            ("relationship", "boredom", 4),
            ("partner", "temptation", 2),
            ("partner", "secrecy", 1),
        ],
        "ch01_d2_game_reassure": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_game_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_d2_game_ignore": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
            ("partner", "temptation", 1),
        ],
        "ch01_d2_bed_pool_love": [
            ("relationship", "love", 3),
            ("relationship", "trust", 3),
            ("relationship", "boredom", -3),
            ("partner", "boundary_looseness", -1),
        ],
        "ch01_d2_bed_pool_exhibition": [
            ("relationship", "love", 2),
            ("relationship", "trust", 2),
            ("relationship", "boredom", -2),
            ("partner", "curiosity", 2),
            ("partner", "exhibitionism", 3),
            ("player", "acceptance", 2),
        ],
        "ch01_d2_bed_pool_accuse": [
            ("relationship", "trust", -2),
            ("relationship", "love", -1),
            ("relationship", "boredom", 2),
        ],
        "ch01_d2_wink_repair": [
            ("relationship", "love", 3),
            ("relationship", "trust", 3),
            ("relationship", "boredom", -3),
            ("partner", "secrecy", -1),
        ],
        "ch01_d2_wink_accuse_hard": [
            ("relationship", "love", -4),
            ("relationship", "trust", -5),
            ("relationship", "boredom", 4),
            ("player", "jealousy", 3),
            ("partner", "temptation", 3),
            ("partner", "secrecy", 2),
        ],
        "ch01_d2_wink_reject_hard": [
            ("relationship", "love", -5),
            ("relationship", "trust", -4),
            ("relationship", "boredom", 5),
            ("partner", "temptation", 3),
            ("partner", "secrecy", 3),
            ("partner", "boundary_looseness", 2),
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
        "ch01_d2_sunset_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_d2_sunset_partial": ("attentive", "honest", "repair"),
        "ch01_d2_sunset_ignore_gate": ("neutral", "nonchalant", "dismissive", "distracted", "ntr-gate"),
        "ch01_d2_game_reassure": ("supportive", "attentive"),
        "ch01_d2_game_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_d2_game_ignore": ("neutral", "nonchalant", "distracted"),
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
        """Resolve the active Day Two lane from accumulated behavior and stats.

        Protection by itself never creates NTR pressure. Risk requires boredom /
        emotional disengagement. Consensual openness instead resolves toward the
        exhibitionism lane.
        """
        day1_pressure = get_story_value("ch01_day1_route_pressure", "mixed")
        d2_nonchalant = choice_tag_count("nonchalant", ch01_d2_choice_ids())
        d2_open = choice_tag_count("open", ch01_d2_choice_ids())
        d2_attentive = choice_tag_count("attentive", ch01_d2_choice_ids())

        risk_seed = (
            day1_pressure == "ntr_seeded"
            or chapter_nonchalant_count("ch01") >= 4
            or relationship_stats["boredom"] >= 17
        )
        risk_now = (
            risk_seed
            and relationship_stats["boredom"] >= 15
            and (d2_nonchalant >= 1 or relationship_stats["love"] <= 48)
            and d2_attentive <= d2_nonchalant + 2
        )
        if risk_now:
            return "ntr_risk"

        exhibition_now = (
            partner_stats["exhibitionism"] >= 22
            and partner_stats["curiosity"] >= 24
            and player_stats["acceptance"] >= 15
            and d2_open >= 1
        )
        if exhibition_now:
            return "exhibitionism"

        return "love"


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

    $ set_story_flag("ch01_day_02_started")
    $ set_story_value("ch01_d2_ntr_soft_gate", False)
    $ set_story_value("ch01_d2_ntr_confirmed", False)
    $ set_story_value("ch01_d2_dinner_wink", False)

    scene black
    with fade
    centered "{size=50}CHAPTER ONE — DAY TWO{/size}"

    jump ch01_day2_scene_01_morning_after


label ch01_day2_scene_01_morning_after:

    scene bg ch01_villa_bedroom_night
    with fade

    "Morning arrived slowly through the useless decorative curtains."
    "Leia was already awake, buried beneath half the duvet and staring at me with the expression of somebody remembering something inconvenient."

    if get_story_value("ch01_dream_response") == "grounded":
        "The dream still existed somewhere at the back of my mind, but daylight had put it back where it belonged."
    elif get_story_value("ch01_dream_response") == "curious":
        "The dream had lost its sharp edges by morning. The uncomfortable question it left behind had not."
    elif get_story_value("ch01_dream_response") == "withdrew":
        "I had managed not to think about the dream again. Mostly. Keeping it there felt easier than examining it."

    # Day One continuity: Julian already sent every earned solo pool Capture to
    # Trip Group last night. Review that same inventory here instead of creating
    # a second photo-count/route state for the morning.
    $ d2_morning_pool_photos = ch01_pool_capture_assets()
    $ d2_morning_withdrew = get_story_value("ch01_dream_response") == "withdrew"

    "Leia reached for her phone and opened the photos Julian had sent the night before."
    gf "Okay. I still think he was way too pleased with himself, but..."
    gf "This one's actually not bad."

    $ renpy.scene()
    $ renpy.show("cg " + d2_morning_pool_photos[0])
    with dissolve

    gf "What do you think?"

    if d2_morning_withdrew:
        "I looked at the photo. For a second, yesterday and the dream tried to occupy the same space in my head."
        mc "Yeah. It's nice."
        gf "...That's it?"
        mc "What?"
        gf "Nothing."
        "Her eyes returned to the phone before mine did."
    elif get_story_value("ch01_dream_response") == "curious":
        "She looked more comfortable in the photo than she had while Julian was taking it."
        mc "You look good."
        gf "Just good?"
        mc "Confident."
        gf "I was trying very hard to look confident."
        mc "It worked."
    else:
        mc "I like it."
        gf "That sounded suspiciously easy."
        mc "You're asking me whether I like a photo of my girlfriend."
        gf "Fair."

    if len(d2_morning_pool_photos) >= 2:
        "Leia swiped to the next photo."
        $ renpy.scene()
        $ renpy.show("cg " + d2_morning_pool_photos[1])
        with dissolve

        if d2_morning_withdrew:
            "She studied it quietly this time, no longer asking me to judge it."
        elif get_story_value("ch01_dream_response") == "curious":
            gf "I actually like this one more."
            mc "You look more relaxed."
            gf "Maybe I was getting used to it."
            "The admission seemed to surprise her slightly less than it surprised me."
        else:
            gf "Wait. This one might be better."
            mc "You're going to make me rank them, aren't you?"
            gf "Obviously."

    if len(d2_morning_pool_photos) >= 3:
        "Her thumb moved again."
        $ renpy.scene()
        $ renpy.show("cg " + d2_morning_pool_photos[2])
        with dissolve

        if d2_morning_withdrew:
            "Another good photo. Another moment where she seemed more interested in sharing it with me than I was capable of being."
            "Leia lingered on it for a second, then locked the phone without asking."
        elif get_story_value("ch01_dream_response") == "curious":
            gf "Okay. I definitely wasn't this comfortable at the start."
            mc "No."
            gf "Is that a bad thing?"
            "There was no accusation in the question. She genuinely wanted to know."
            mc "I don't know yet."
            gf "Honest."
        else:
            gf "There. That's my favourite."
            mc "I thought the last one was your favourite."
            gf "I've changed my mind."
            mc "In the last four seconds?"
            gf "Growth."

    scene bg ch01_villa_bedroom_night
    with dissolve

    gf "You were a menace last night."
    mc "Good morning to you too."
    gf "I'm serious."
    mc "You were the one checking if he was looking."

    if partner_stats["exhibitionism"] < 18:
        gf "I was checking that he wasn't."
    elif partner_stats["exhibitionism"] < 26:
        gf "That is not the same thing."
        mc "Sure."
        gf "It isn't."
    else:
        gf "You have no evidence."
        mc "I have eyes."
        gf "Circumstantial."

    $ d2_morning_reassure_text = format_choice("ch01_d2_morning_reassure", "Relax. I was only teasing you.")
    $ d2_morning_tease_text = format_choice("ch01_d2_morning_tease", "I liked seeing you curious.")
    $ d2_morning_dismiss_text = format_choice("ch01_d2_morning_dismiss", "It wasn't a big deal.")

    menu:
        "[d2_morning_reassure_text]":
            $ apply_choice("ch01_d2_morning_reassure")
            mc "Relax. I was only teasing you."
            gf "I know."
            "She moved closer and rested her forehead briefly against my shoulder."

        "[d2_morning_tease_text]":
            $ apply_choice("ch01_d2_morning_tease")
            mc "I liked seeing you curious."
            gf "Curious about what?"
            mc "Exactly."
            gf "You're impossible."
            "She was smiling when she said it."

        "[d2_morning_dismiss_text]":
            $ apply_choice("ch01_d2_morning_dismiss")
            mc "It wasn't a big deal."
            gf "Right."
            "The subject died more quickly than it needed to."

    "For a moment neither of us said anything."

    if get_story_value("ch01_dream_response") == "withdrew":
        "Leia shifted closer anyway, her shoulder settling against mine."
        "I felt the invitation in it. I just didn't quite know what to do with it."
        gf "You okay?"
        mc "Yeah. Just didn't sleep that well."
        "She watched me for another second, then let me have the answer."
    elif get_story_value("ch01_dream_response") == "curious":
        "Leia shifted closer, warm and familiar against my side."
        "The contrast with the dream should have made the whole thing easier to dismiss. Somehow, it only made my reaction to it stranger."
    else:
        "Leia shifted closer and stole the last corner of duvet I still technically owned."
        mc "Seriously?"
        gf "You weren't using it."
        mc "It was on me."
        gf "Exactly. Storage."

    "A few minutes later, Leia finally pushed herself out of bed and stretched."
    gf "I'm showering before Julian starts accusing us of hibernating."
    mc "He'd have to be awake first."
    gf "Unfortunately, he always is when there's food involved."

    "She disappeared toward the bathroom, leaving me with a quiet room and far too much time inside my own head."

    if get_story_value("ch01_dream_response") == "withdrew":
        "I picked up my phone mostly so I would have something else to look at."
    elif get_story_value("ch01_dream_response") == "curious":
        "I caught myself thinking about the photos again, and about how quickly Leia had gone from awkward to comfortable in front of the camera."
        "The thought wasn't jealousy. That was what made it harder to file away."
    else:
        "By the time I checked my phone, the dream had already started to feel like something that belonged to the night before."

    $ set_story_flag("ch01_d2_scene_01_complete")
    jump ch01_day2_scene_02_breakfast


label ch01_day2_scene_02_breakfast:

    scene bg ch01_d2_breakfast
    with dissolve

    friend "Look who survived the night."
    gf "Barely."
    friend "You spent half the movie rearranging yourself every thirty seconds."

    "Leia's eyes moved directly to mine."

    mc "Maybe your movie was making her uncomfortable."
    friend "My movie was art."
    gf "Your movie had a shark driving a speedboat."
    friend "Exactly. Art."

    "Breakfast settled into the easy rhythm we'd found by the end of yesterday."

    friend "So what's the plan today?"
    gf "Something that doesn't involve me wearing dinner."
    friend "One accident."
    gf "One very wet accident."
    mc "You did recover."
    gf "Eventually."

    "Julian pointed at the spread between us."
    friend "Eat first. Decide later. That's a plan."
    gf "That's not a plan."
    friend "It's worked for me so far."

    if get_story_value("ch01_dream_response") == "withdrew":
        "My attention drifted somewhere between the table and the remains of the dream."
        gf "Ryan?"
        mc "Hm?"
        gf "Coffee."
        "She was holding the pot slightly toward me."
        gf "I asked if you wanted some."
        mc "Oh. Yeah. Thanks."
        "She poured it without commenting, but I caught the brief look she gave me before turning back to Julian."
    elif get_story_value("ch01_dream_response") == "curious":
        gf "Coffee?"
        mc "Please."
        "She poured mine before her own without thinking about it."
        "Small, ordinary, automatic. Four years reduced to a gesture neither of us noticed anymore."
    else:
        gf "Coffee?"
        mc "Only if you're admitting you stole the duvet."
        gf "I admit nothing."
        "She poured it anyway."

    $ set_story_flag("ch01_d2_scene_02_complete")
    jump ch01_day2_scene_03_maya_message


label ch01_day2_scene_03_maya_message:

    "My phone buzzed beside the coffee."
    "Maya's name appeared on the screen."

    centered "MAYA: You people alive? I'm near the resort around lunch. Still meeting?"

    "Leia saw the name before I put the phone down."

    gf "Oh."
    mc "What?"
    gf "Nothing."
    friend "That was the loudest 'nothing' I've ever heard."

    gf "So this is the Maya I've heard about."
    mc "You've heard about her."
    gf "Mm."
    mc "What does that mean?"
    gf "Nothing."

    "Julian lowered his coffee."
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
            "Leia considered that for a second."
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

    "The subject should have ended there, but Leia's curiosity survived breakfast."

    if get_story_value("ch01_female_friend_response") == "teased_jealousy":
        gf "And for the record, I'm still not jealous."
        mc "I didn't say anything."
        gf "Your face did."
    elif get_story_value("ch01_female_friend_response") == "asserted_boundary":
        gf "I'm glad she's meeting all of us, by the way."
        mc "Me too."
        gf "Good."
    else:
        gf "I am curious to finally meet her."
        mc "That's allowed."
        gf "How generous."

    "Whatever tiny tension had been there stayed small enough to joke about."

    $ set_story_flag("ch01_d2_scene_04_complete")
    jump ch01_day2_scene_05_meet_maya


label ch01_day2_scene_05_meet_maya:

    scene bg ch01_d2_cafe
    with fade

    "Maya spotted us before I spotted her."
    "A small day bag hung from one shoulder, looking more prepared for an island afternoon than the rest of us were."

    maya "Ryan!"

    "She greeted me with the uncomplicated familiarity of somebody I'd known long enough not to perform politeness around."
    "Leia watched the greeting carefully."

    maya "And this has to be Leia. Finally."
    gf "Finally?"
    maya "I've heard about you for years."

    "Leia slowly turned toward me."

    gf "Years?"
    mc "Apparently I've been discussing you."
    maya "Constantly. It's exhausting."
    friend "Good. Somebody else can suffer now."

    "Maya introduced herself to Julian and, within thirty seconds, had already made fun of his sunglasses."

    maya "Those cost more than my flight, don't they?"
    friend "They're very good sunglasses."
    maya "That's a yes."

    "We ordered drinks and found a table near the open side of the café."
    maya "So. Four years."
    gf "Four years."
    maya "I need to know something."
    gf "That sounds threatening."
    maya "Has he always taken twenty minutes to decide what to eat?"
    gf "Oh my God."
    mc "This is character assassination."
    gf "He reads the entire menu, picks something, changes his mind, then orders the first thing."
    maya "He used to do that at lunch."
    gf "He still does it at dinner."

    "They looked at each other with the immediate recognition of two people who had independently discovered the same flaw."
    mc "I regret this meeting already."

    maya "Good. That means it's going well."

    $ set_story_flag("ch01_d2_scene_05_complete")
    jump ch01_day2_scene_06_jealousy_test


label ch01_day2_scene_06_jealousy_test:

    "Maya and I fell briefly into the shorthand of old stories and mutual friends."
    "Leia listened rather than interrupting. The quiet was subtle enough that Maya did not notice. I did."

    $ d2_maya_include_text = format_choice("ch01_d2_maya_include", "Pull Leia into the conversation.")
    $ d2_maya_catchup_text = format_choice("ch01_d2_maya_catchup", "Keep catching up normally.")
    $ d2_maya_dismiss_text = format_choice("ch01_d2_maya_dismiss_leia", "She's fine. Keep talking to Maya.")

    menu:
        "[d2_maya_include_text]":
            $ apply_choice("ch01_d2_maya_include")
            mc "Tell her the story about the airport."
            maya "No. You tell her. You're the one who caused it."
            gf "Now I need to hear this."
            "Leia shifted closer to the conversation instead of sitting outside it."

        "[d2_maya_catchup_text]":
            $ apply_choice("ch01_d2_maya_catchup")
            "I kept catching up with Maya. Leia stayed quiet for another minute before Maya turned to her directly."

        "[d2_maya_dismiss_text]":
            $ apply_choice("ch01_d2_maya_dismiss_leia")
            "Leia looked at me once. I let the moment pass and kept talking to Maya."
            "By the time Maya turned the conversation toward her, Leia was smiling again, but the delay had registered."

    "Maya eventually rescued me from my own old stories by turning to Leia."

    maya "Okay, enough Ryan history. Tell me something about you that he wouldn't think to tell me."
    gf "That's a dangerous amount of freedom."
    mc "I object to the premise."
    maya "Overruled."

    if get_story_value("ch01_dream_response") == "withdrew":
        "Leia glanced at me before answering. It was brief, but after the morning we'd had, I noticed it."
    else:
        "Leia thought about it with the seriousness of somebody selecting evidence for court."

    gf "I hate folding laundry."
    maya "That's it?"
    gf "I mean I really hate it. I will live out of a clean laundry basket for a week."
    mc "Two weeks."
    gf "Nobody asked for corroborating testimony."
    maya "Perfect. Humanising. Continue."

    "The conversation stopped being mine and Maya's reunion after that."

    $ set_story_flag("ch01_d2_scene_06_complete")
    jump ch01_day2_scene_07_leia_maya_click


label ch01_day2_scene_07_leia_maya_click:

    "The awkwardness lasted considerably less time than I'd expected."
    "Maya asked Leia one question about the resort. Leia answered with a story. One story became three."

    maya "Wait. You actually like travelling with him?"
    gf "Most of the time."
    mc "Most?"
    gf "Airports bring out the worst in you."
    maya "Thank you."
    gf "He becomes convinced every queue is the wrong queue."
    maya "THANK you."
    mc "I have instincts."
    maya "You have anxiety with luggage."

    "Leia laughed hard enough to cover her mouth."
    "Whatever caution she'd brought into meeting Maya was disappearing quickly."

    maya "What about you? Holiday person or itinerary person?"
    gf "I like having a plan."
    mc "She likes having a spreadsheet."
    gf "A spreadsheet is a plan that respects you."
    maya "We're going to get along."

    "The conversation wandered from travel to food, then clothes, then the photos on Leia's phone."

    maya "Wait, you took this?"
    gf "Yes."
    maya "Ryan told me he was the photographer."
    gf "Ryan lies."
    mc "I am sitting right here."
    maya "We know."

    maya "You photograph well, by the way."
    gf "Only when I forget somebody's taking one."
    maya "That's everybody. The second people see a camera they start manually operating their face."
    gf "That's exactly what I do."
    maya "Then don't pose next time."

    "Leia scrolled back to one of yesterday's pool photos."
    gf "I got better eventually."
    maya "See? This one's good."
    gf "Julian took that."
    maya "Annoying. I was hoping I could insult his photography too."

    "Julian looked at me over his drink."

    friend "You've lost control of the situation."
    mc "I made a mistake introducing them."
    gf "Too late. I like her."
    maya "Same."

    "It was said jokingly, but Leia's posture had changed. She wasn't Ryan's girlfriend meeting Ryan's friend anymore. She was talking to Maya on her own terms."

    $ set_story_value("ch01_d2_leia_maya_comfort", 2)
    $ set_story_flag("ch01_d2_scene_07_complete")
    jump ch01_day2_scene_08_maya_julian


label ch01_day2_scene_08_maya_julian:

    "Maya's attention eventually shifted to Julian."

    maya "So you're the rich one."
    friend "Apparently that's my entire personality now."
    maya "No, the sunglasses are your personality. The money is supporting cast."

    "Julian laughed despite himself. Leia leaned toward me."

    gf "They get along."
    mc "She insults people she likes."
    gf "That explains you."

    "A bee wandered close to the table."
    "Julian stopped mid-sentence and leaned sharply away from it."

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
    friend "Ryan."
    mc "I can't help you anymore."

    "For the first time since Maya arrived, the four of us felt less like two existing friendships forced around one table and more like an actual group."

    $ set_story_flag("ch01_d2_julian_bee_fear_seeded")
    $ set_story_flag("ch01_d2_scene_08_complete")
    jump ch01_day2_scene_09_photo_walk


label ch01_day2_scene_09_photo_walk:

    scene bg ch01_d2_island_day
    with dissolve

    "After brunch, Maya turned a walk through the island shops into a photography project."

    "There was no urgency to it. We drifted between shaded storefronts, stopped whenever somebody saw something interesting, and argued about whether Julian needed another pair of sunglasses."

    friend "They're different."
    maya "They're black."
    friend "The frames are completely different."
    gf "They're also black."
    friend "I expected more from you, Leia."
    gf "We've known each other for two days."
    friend "And already the betrayal."

    "Maya had started walking beside Leia without anybody arranging it."
    "Every few minutes one of them would stop to point something out, and the rest of us would realise we'd walked several steps ahead."

    if get_story_value("ch01_dream_response") == "withdrew":
        "Watching Leia settle so easily into somebody else's company should have been reassuring."
        "Instead, I was uncomfortably aware of how little effort it had taken for someone else to give her the attention I'd been withholding all morning."
    elif get_story_value("ch01_dream_response") == "curious":
        "Leia seemed lighter around Maya already. Less concerned with how she was being perceived, more willing to just react."
    else:
        "Seeing Leia relax around Maya removed the last trace of tension from breakfast."

    maya "Okay. Group photo first. Then combinations."
    friend "Combinations?"
    maya "You people took one decent photo yesterday and suddenly I have standards."

    "The first group photo took three attempts because Julian blinked in two of them."
    friend "The sun is aggressive."
    maya "Your eyelids are aggressive."

    "Then Maya started assigning pairs with the authority of somebody organising school photos."

    "We took the obvious ones first: all four of us, Leia and me, Maya and me, Julian and Maya."

    $ set_story_flag("ch01_d2_photo_group")
    $ set_story_flag("ch01_d2_photo_ryan_leia")
    $ set_story_flag("ch01_d2_photo_ryan_maya")
    $ set_story_flag("ch01_d2_photo_julian_maya")

    jump ch01_day2_scene_10_leia_maya_photo


label ch01_day2_scene_10_leia_maya_photo:

    $ enter_cinematic_mode()
    scene cg ch01_d2_photo_leia_maya
    with dissolve

    "Maya hooked an arm around Leia and immediately ruined her attempt at a careful pose by making her laugh."
    "The resulting photo looked better than anything either of them had planned."

    maya "See? Stop thinking about the camera."
    gf "Easy for you to say."
    maya "Correct. I'm extremely photogenic."
    gf "You made me laugh."
    maya "Exactly. Now you owe me photography credit."
    gf "Absolutely not."

    "Leia was still smiling when she looked at the result."

    $ exit_cinematic_mode()
    scene bg ch01_d2_island_day

    "Leia saved the photo immediately."

    $ set_story_flag("ch01_d2_photo_leia_maya")
    $ set_story_flag("ch01_d2_scene_10_complete")
    jump ch01_day2_scene_11_missing_pair


label ch01_day2_scene_11_missing_pair:

    maya "Wait. We're missing one."
    friend "Are we?"
    maya "Leia and Julian."

    "Leia looked at Julian, then at me."

    $ d2_pair_encourage_text = format_choice("ch01_d2_photo_pair_encourage", "Go on. Complete the set.")
    $ d2_pair_redirect_text = format_choice("ch01_d2_photo_pair_redirect", "We've got enough photos. Come here, babe.")
    $ d2_pair_shrug_text = format_choice("ch01_d2_photo_pair_shrug", "Do whatever you want.")

    menu:
        "[d2_pair_encourage_text]":
            $ apply_choice("ch01_d2_photo_pair_encourage")
            $ set_story_value("ch01_d2_leia_julian_photo", "taken")
            mc "Go on. Complete the set."
            gf "You're very enthusiastic about this."
            mc "Historical documentation."
            friend "I hate all of you."
            "Leia stood beside Julian for the photo. It was harmless. The fact that she checked my reaction first was the more interesting part."

        "[d2_pair_redirect_text]":
            $ apply_choice("ch01_d2_photo_pair_redirect")
            $ set_story_value("ch01_d2_leia_julian_photo", "redirected")
            mc "We've got enough photos. Come here, babe."
            "Leia came back toward me without argument."
            gf "Possessive photographer."
            mc "Occupational hazard."

        "[d2_pair_shrug_text]":
            $ apply_choice("ch01_d2_photo_pair_shrug")
            $ set_story_value("ch01_d2_leia_julian_photo", "shrugged")
            mc "Do whatever you want."
            "Leia's eyes stayed on me for a fraction longer than necessary."
            gf "Okay."
            "She took the photo with Julian. It was ordinary. My indifference was not."

    $ set_story_flag("ch01_d2_scene_11_complete")
    jump ch01_day2_scene_11b_boutique


label ch01_day2_scene_11b_boutique:

    scene bg ch01_d2_boutique
    with dissolve

    friend "Before we go back, I need a shirt."
    maya "You own twelve versions of the same shirt."
    friend "Exactly. I need the thirteenth."

    "The mall stop was supposed to take five minutes."
    "Julian disappeared toward a menswear rack. Maya made it approximately three storefronts before stopping dead outside a boutique."

    maya "Oh."
    gf "Why did you say that like that?"
    maya "Come with me."
    gf "No."
    maya "You haven't even seen what I'm looking at."
    gf "I know you well enough now."

    "Leia still followed her inside."

    "Maya chose a red asymmetric cutout mini almost immediately. Leia was slower."
    "She stopped in front of a rack and stared at one outfit long enough for Maya to notice."

    maya "That one."
    gf "What?"
    maya "You've been staring at it."
    gf "I have not."
    maya "You absolutely have."

    "Leia had been looking at something daring but still recognisably within reach."
    "Maya looked beside it, found a much smaller black halter mini built from deep cutouts and two precarious front panels, and smiled."

    maya "Oh, no. You're trying this."
    gf "That's not even the one I was looking at."
    maya "I know."
    gf "Maya."
    maya "Changing room."

    "Leia stared at the black dress, then at Maya."
    gf "I'm not wearing that outside."
    maya "I didn't say outside. Try it."
    gf "Why?"
    maya "Because you've been staring at this rack for thirty seconds."

    "Leia hesitated, then took the hanger from her."
    $ set_story_flag("ch01_d2_maya_pushed_boutique_tryon")
    $ set_story_value("ch01_d2_boutique_trial_outfit", "boutique_cutout_mini")

    $ enter_cinematic_mode()
    scene cg ch01_d2_boutique_changing_room
    with dissolve

    "Maya's red dress fit as if she'd picked it for herself a hundred times before."
    "Leia's was another matter."
    "She stood in front of the mirror holding the two triangular front panels securely against herself while Maya worked out the straps behind her."

    gf "This isn't a dress."
    maya "You're wearing it. Therefore: dress."
    gf "If I move my hand, I'm getting banned from this mall."
    maya "Only because I haven't secured it properly yet."
    gf "That is not making me feel better."

    "Maya moved behind her, took over the tension in the straps and carefully pulled the top into place."

    gf "How is yours more revealing and somehow more secure?"
    maya "Skill."
    gf "That's not how clothes work."
    maya "Sounds like a you problem."

    "Maya's teasing softened when she looked at Leia in the mirror."

    maya "Seriously. You look good."
    gf "I look terrified."
    maya "Both can be true."

    "Leia looked at herself again. This time she didn't immediately cover more of the dress."

    $ exit_cinematic_mode()
    scene bg ch01_d2_boutique
    with dissolve

    gf "[player_name]?"
    mc "Yeah?"
    gf "Can you come here for a second?"

    $ d2_mall_lane = ch01_d2_route_lane()
    $ set_story_value("ch01_d2_mall_entry_lane", d2_mall_lane)
    $ d2_mall_ryan_present = True

    if d2_mall_lane == "ntr_risk":
        $ d2_mall_go_text = format_choice("ch01_d2_mall_go_to_leia", "Go see what she wants.")
        $ d2_mall_leave_text = format_choice("ch01_d2_mall_leave_to_maya", "Let Maya handle it.")

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
                mc "Maya's already in there. Let her handle it."
                "There was a short pause from behind the curtain."
                gf "...Okay."
    else:
        $ set_story_value("ch01_d2_mall_ryan_response", "came_over")
        "I headed toward the changing rooms."

    if d2_mall_ryan_present:
        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_reveal_ryan
        with dissolve

        "Maya opened the curtain while standing behind Leia, both hands still responsible for keeping the black top properly tensioned."
        "Leia looked considerably less certain than Maya did."

        gf "Well?"

        $ d2_mall_affection_text = format_choice("ch01_d2_mall_reveal_affection", "You look incredible.")
        $ d2_mall_open_text = format_choice("ch01_d2_mall_reveal_open", "Didn't know you had that in you.")
        $ d2_mall_tease_text = format_choice("ch01_d2_mall_reveal_tease", "Maya really did this to you?")

        menu:
            "[d2_mall_affection_text]":
                $ apply_choice("ch01_d2_mall_reveal_affection")
                mc "You look incredible."
                "Leia's shoulders relaxed a little."
                gf "You're biased."
                mc "Very."

            "[d2_mall_open_text]":
                $ apply_choice("ch01_d2_mall_reveal_open")
                mc "Didn't know you had that in you."
                gf "I don't. Maya put it there."
                maya "You're welcome."

            "[d2_mall_tease_text]":
                $ apply_choice("ch01_d2_mall_reveal_tease")
                mc "Maya really did this to you?"
                gf "Against my better judgement."
                maya "Her judgement is improving."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve

    else:
        maya "Julian!"
        gf "Maya—"
        maya "What? We need an opinion."

        "Julian appeared from the next section holding two nearly identical shirts."

        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_reveal_julian
        with dissolve

        friend "Oh."
        maya "That's all you've got?"
        friend "I wasn't prepared for a test."
        gf "Don't encourage her."
        friend "You look good."
        gf "...Thanks."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve

    "Maya was still holding Leia's top securely when something over Leia's shoulder caught her attention."
    maya "Wait—oh my God. That one."
    gf "What?"
    maya "That."

    "A metallic mesh mini hung on a nearby display in deep crimson: a plunging draped front, delicate chain straps and a slit cut almost to the hip."

    gf "You're already wearing red."
    maya "Not for me. For you."
    gf "Absolutely not."
    maya "Leia, look at it—"

    "Maya turned and reached toward the display without properly releasing the tension she was holding."
    "One side of Leia's black top immediately slipped."

    gf "Maya!"

    if d2_mall_ryan_present:
        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_slip_ryan
        with dissolve

        "Leia caught the loose panel almost immediately and clamped it back into place."
        "Maya froze, horrified."
        maya "Sorry. Sorry."
        gf "You had one job."
        maya "I got distracted."
        gf "Clearly."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve
        $ set_story_value("ch01_d2_boutique_slip_witness", "ryan")

    else:
        $ enter_cinematic_mode()
        scene cg ch01_d2_boutique_slip_julian
        with dissolve

        "Leia caught the loose panel and pulled it back into place."
        "But Julian had already seen the slip."
        "His gaze stayed there a beat too long."
        "Then another."
        "Leia looked up and caught him staring."
        "Their eyes met."
        "That was what finally made Julian look away."

        "Maya, focused entirely on fixing the top, missed the exchange."

        maya "Sorry. Sorry."
        gf "You had one job."
        maya "I got distracted."
        gf "Clearly."

        $ exit_cinematic_mode()
        scene bg ch01_d2_boutique
        with dissolve
        $ set_story_flag("ch01_d2_leia_noticed_julian_stare")
        $ set_story_value("ch01_d2_boutique_slip_witness", "julian")

    "Maya glanced back toward the crimson mesh dress."
    maya "Still think you'd look amazing in it."
    gf "I'm changing."
    maya "So that's a maybe."
    gf "That's a no."

    "A few minutes later they emerged in their normal clothes. Maya had bought the red dress without hesitation."
    "Leia still had the black mini over one arm."

    if d2_mall_ryan_present:
        "The boutique's catalogue was available through the Shop on my phone. Buying something would add it to Leia's wardrobe; whether she actually agreed to wear it later was a separate question."
        $ last_shop_message = "Boutique visit: the Black Cutout Mini is now available."
        call screen shop_screen
        if owns_outfit("boutique_cutout_mini"):
            $ set_story_value("ch01_d2_mall_outfit_source", "ryan")
            $ set_story_flag("ch01_d2_boutique_outfit_owned")
            gf "You actually bought it?"
            mc "You looked good in it."
            gf "That doesn't mean I'm wearing it outside."
            maya "Yet."
            "Leia gave Maya a look and said nothing."
        else:
            # Ryan chose not to buy it, so Leia buys the Black Cutout Mini herself.
            # (Ryan buying it still stands; there is no "nobody buys it" outcome.)
            "I closed the Shop without buying anything."
            "Leia looked back at the black dress for several seconds, then carried it to the counter herself."
            $ grant_story_outfit("boutique_cutout_mini", equip=False)
            $ set_story_value("ch01_d2_mall_outfit_source", "leia")
            $ set_story_flag("ch01_d2_boutique_outfit_owned")
            mc "You're buying it?"
            gf "I'm not wearing it outside."
            maya "Yet."
            "Leia gave Maya a look and said nothing."
    else:
        "Leia looked down at the black dress for several seconds before carrying it to the counter herself."
        $ grant_story_outfit("boutique_cutout_mini", equip=False)
        $ set_story_value("ch01_d2_mall_outfit_source", "leia")
        $ set_story_flag("ch01_d2_boutique_outfit_owned")

        mc "You bought it?"
        gf "Yeah."
        mc "Thought you said it was too much."
        gf "I said I wasn't wearing it outside."
        maya "Yet."
        "Leia gave Maya a look and said nothing."

    "Julian eventually returned with a shopping bag."

    maya "That's basically the shirt you were already wearing."
    friend "This one's different."
    maya "How?"
    friend "It's new."

    "We stepped back outside into the early-afternoon heat with considerably more shopping than Julian's five-minute shirt stop had promised."

    maya "Drink before we go?"
    gf "Please."

    "We found a table nearby and dropped the shopping bags around our feet."

    maya "That went significantly better than expected."
    gf "For who?"
    maya "Me."
    gf "Trying something on and wearing it are completely different things."
    maya "That's what fitting rooms are for."

    friend "For what it's worth, I thought it looked good."
    gf "Thanks."
    maya "See?"
    gf "You don't get credit for his opinion."

    "Maya and Julian started arguing over whether his new shirt was actually different from the one he'd arrived in."
    "Leia leaned slightly closer to me."

    if get_story_value("ch01_d2_boutique_slip_witness") == "ryan":
        gf "You saw that, right?"
        mc "The dress?"
        gf "No. When it slipped."
        mc "Yeah."
        gf "I wanted to disappear."
        if get_story_value("ch01_d2_mall_ryan_response") == "reconnected" or get_story_value("ch01_d2_mall_entry_lane") != "ntr_risk":
            mc "You caught it."
            gf "Barely."
            "Her embarrassment had already softened enough for her to roll her eyes at herself."
        else:
            mc "It was an accident."
            gf "I know."
    else:
        mc "So what happened in there after I stayed out?"
        gf "Nothing dramatic."
        "She turned her cup slowly between her hands."
        gf "The top slipped a little."
        mc "Oh."
        gf "Julian was there."
        "I looked at her."
        gf "He looked away."
        "The way she said it wasn't defensive. It was simply the version of events she'd been left to process without me."

    gf "You've been quiet today."

    $ d2_postshop_sleep_text = format_choice("ch01_d2_postshop_sleep", "I didn't sleep well.")
    $ d2_postshop_head_text = format_choice("ch01_d2_postshop_head", "I've just got a lot in my head.")
    $ d2_postshop_shut_text = format_choice("ch01_d2_postshop_shut_down", "I'm fine.")

    menu:
        "[d2_postshop_sleep_text]":
            $ apply_choice("ch01_d2_postshop_sleep")
            mc "I didn't sleep well."
            gf "I noticed."
            mc "Sorry."
            gf "You don't have to apologise for being tired."
            "It wasn't the whole truth, but at least I had stopped pretending there was nothing to explain."

        "[d2_postshop_head_text]":
            $ apply_choice("ch01_d2_postshop_head")
            mc "I've just got a lot in my head."
            gf "Anything you want to talk about?"
            mc "Not yet."
            gf "Okay."
            "She didn't push. The important part was that I'd finally admitted there was something there."

        "[d2_postshop_shut_text]":
            $ apply_choice("ch01_d2_postshop_shut_down")
            mc "I'm fine."
            "Leia watched me for a second."
            gf "Okay."
            "This time the word meant she was done asking."

    "Julian stood and picked up his shopping bag."
    friend "I'm getting another drink before we go."
    mc "I'll come with you."

    "We left Leia and Maya at the table for a minute."

    maya "Everything okay?"
    gf "With the dress?"
    maya "With Ryan."

    if choice_tag_count("repair", ch01_d2_choice_ids()) >= 1 or get_story_value("ch01_d2_mall_ryan_response") in ("reconnected", "came_over"):
        gf "Yeah. I think he's just in his head today."
        maya "People are allowed weird days."
        gf "Very insightful."
        maya "I'm extremely emotionally intelligent."
        gf "Obviously."
    else:
        gf "I don't know."
        "Leia looked toward the counter, where Ryan and Julian were waiting."
        gf "He's been somewhere else all morning."
        maya "Did something happen?"
        gf "Not that I know of. He says he's fine."
        maya "Then give him a little time."
        gf "Yeah."
        "For once, Leia let the problem sit instead of immediately trying to solve it."

    "By the time we returned, Maya had deliberately moved the conversation back to clothes."
    maya "I'm still saying the black one."
    gf "I'm still saying fitting room only."
    maya "For now."
    gf "You're exhausting."

    $ set_story_flag("ch01_d2_scene_11b_boutique_complete")
    jump ch01_day2_scene_12_villa_pool_plan


label ch01_day2_scene_12_villa_pool_plan:

    "We headed back toward Julian's place with Maya and Leia a few steps ahead of us."

    if choice_tag_count("repair", ch01_d2_choice_ids()) >= 1:
        "Leia drifted back toward me before long and slipped her hand into mine."
    elif ch01_d2_route_lane() == "exhibitionism":
        gf "Ryan, tell her she's insane."
        maya "He doesn't get a vote."
        gf "He gets an advisory position."
        mc "I accept the appointment."
        "Leia turned forward again, still laughing with Maya but keeping me inside the conversation."
    elif ch01_d2_route_lane() == "ntr_risk":
        "Leia looked back once."
        "I was half a step behind, somewhere else again."
        "She turned back to Maya."
        "She didn't look back a second time."

    scene bg ch01_villa_living
    with fade

    "Maya stopped just inside."

    maya "Wait."
    maya "This is where you're staying?"
    friend "Yeah."

    "She looked around the living room, then back at Julian."

    maya "The sunglasses make sense now."
    friend "Thank you."
    maya "That wasn't a compliment."

    gf "Come on. I'll show you around."
    "Yesterday Leia had been the newcomer. Today she was the one leading Maya through the villa like she'd already learned its shape."

    "They made it as far as the view outside before Maya stopped again."

    maya "Is that a private pool?"
    friend "Yes."
    maya "You didn't think that was relevant information?"
    friend "Relevant to what?"
    maya "Everything."

    gf "We went in yesterday."
    maya "And nobody told me to bring a swimsuit?"

    "Maya paused, then looked down at the day bag she'd been carrying since the café."

    maya "Actually—wait. I did bring one."
    gf "You just carry a swimsuit around?"
    maya "We're on an island."
    gf "...Fair."

    maya "Come change with me."
    gf "You know where nothing is."
    maya "You do."

    "Leia led her upstairs while Julian and I dealt with drinks outside."

    $ set_story_flag("ch01_d2_scene_12_complete")
    jump ch01_day2_scene_13_girls_upstairs


label ch01_day2_scene_13_girls_upstairs:

    scene bg ch01_master_bedroom
    with dissolve

    "Upstairs, Leia laid both of her swimsuits across the bed while Maya pulled her own from the day bag and changed beside her."

    maya "You brought options."
    gf "One is safe. One requires confidence."
    maya "Which one do you want to wear?"

    "Yesterday Leia had asked me that question. Today she had to answer it herself."

    if partner_stats["exhibitionism"] >= 22 or partner_stats["curiosity"] >= 27:
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
        "Leia tied the top while still talking to Maya, fingers moving faster than her attention."
        maya "That tie secure?"
        "Leia glanced down and gave it a small tug."
        gf "Should be fine."
        maya "Famous last words."
        gf "It's fine."
        $ set_story_flag("ch01_d2_bikini_tie_loose")
    else:
        "Leia changed into the swimsuit she already trusted while Maya borrowed the mirror and most of the counter space."
        maya "You know what I like about you?"
        gf "We've known each other four hours."
        maya "Exactly. Low sample size. No pressure."

    $ set_story_flag("ch01_d2_scene_14_complete")
    jump ch01_day2_scene_15_pool_group


label ch01_day2_scene_15_pool_group:

    scene bg ch01_pool_day
    with fade

    "The four of us spent the first half hour together."
    "Maya immediately discovered Julian's hatred of being splashed. Leia immediately used that information against him."

    maya "You two did this yesterday?"
    gf "Most of the afternoon."
    friend "They bullied me yesterday too."
    mc "You own the villa. You'll survive."

    "The mood was easy. Whatever happened next would come from the choices already accumulating beneath it."

    $ set_story_value("ch01_d2_route_lane_pre_split", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_15_complete")

    jump ch01_day2_scene_16_forced_split
