# Leia's Consent — Chapter One: Something Different
# Day Two, Scenes 16–30.

label ch01_day2_scene_16_forced_split:

    $ d2_lane = get_story_value("ch01_d2_route_lane_pre_split", "love")

    "Eventually all four of us climbed out together and collapsed around the poolside table."
    "Julian distributed the remaining drinks while Maya lifted hers."

    maya "To unexpected shopping trips."
    gf "Absolutely not."
    friend "To my new shirt."
    maya "Even worse."
    mc "To surviving day two."
    gf "There we go."

    "Four glasses met in the middle."

    "A little farther down the pool deck, a couple of guys had been glancing our way often enough for Maya to notice."
    maya "Don't look now."
    "Leia looked immediately."
    maya "Every time."
    gf "Then stop saying it like that."
    "One of the men looked away a fraction too late."
    gf "Maybe he's looking at you."
    maya "He has two eyes."

    if d2_lane == "ntr_risk":
        "Leia looked toward me first."
        "I was distracted, only half following whatever Julian had just said."
        "She waited for my attention for a beat. It never came."
        "Then she turned back toward the strangers."
        "Leia raised both arms over her head in a slow stretch, extending through her shoulders and back before letting them fall again."
        "The same man kept looking."
        "Maya noticed. I didn't."
        $ set_story_value("ch01_d2_pool_attention", "leia_stretched_without_ryan")

    else:
        "Leia looked from the strangers to me, then crossed the few steps between us."
        "Without saying anything, she leaned in and kissed me."
        "I kissed her back and let one hand settle firmly on her ass."
        "Leia made a small surprised sound against my mouth."
        "When we separated, Maya was staring at us. Julian had suddenly become very interested in his drink. The strangers had seen everything."

        if d2_lane == "exhibitionism":
            "Leia's face warmed, but she glanced toward the strangers once more before looking back at me."
            maya "Okay. We are all still here."
            gf "Nobody asked you to watch."
            maya "Kind of difficult not to."
            $ set_story_value("ch01_d2_pool_attention", "couple_display_open")
        else:
            "Leia's face went pink the moment she remembered we had an audience."
            mc "What was that for?"
            gf "Do I need a reason?"
            "She stayed close anyway."
            $ set_story_value("ch01_d2_pool_attention", "couple_display_love")

    "Julian reached for the cooler again, found it empty and stared into it as if more drinks might appear."
    friend "We're out."
    maya "Already?"
    friend "Apparently none of you understand moderation."

    if d2_lane == "ntr_risk":
        maya "Ryan, come with me. Four drinks."
        mc "You need help carrying four drinks?"
        maya "Yes."

        "Leia stayed beside Julian while Maya led me back toward the villa."
        "Once the pool was out of earshot, I looked at her."
        mc "This isn't about drinks, is it?"
        maya "No."
        maya "What's going on with you today?"
        mc "What do you mean?"
        maya "Leia keeps checking whether you're still in the room even when you're standing right beside her."
        "That landed harder than I wanted it to."

        "Back at the pool, Julian glanced toward the path we'd disappeared down."
        friend "That wasn't about drinks."
        gf "Nope."
        friend "She does this."
        gf "Kidnaps people's boyfriends?"
        friend "Interrogates people."
        "Leia laughed despite herself."
        gf "Does he always get this quiet when he's stuck in his own head?"
        friend "Sometimes."
        "Julian didn't dress the answer up or use it against me. He simply knew me longer than Leia did."

        $ set_story_value("ch01_d2_split", "ryan_maya_leia_julian")

    elif d2_lane == "exhibitionism":
        friend "I'll get them."
        mc "I'll help."
        "Julian and I headed toward the villa while Leia and Maya stayed beside the pool."

        "Maya waited until we were far enough away, then looked at Leia."
        maya "Okay. Are you two experimenting?"
        gf "What makes you say that?"
        maya "You just kissed him in front of everybody and let him grab your ass while those guys were staring."
        "Leia's face warmed again."
        gf "Maybe... a little."
        maya "Seriously?"
        gf "We're figuring it out."
        maya "So how far does experimenting go?"
        gf "Maya."
        maya "I'm asking."
        "Leia laughed, embarrassed, and glanced toward the strangers."
        maya "Want to give them something else to look at?"
        "Leia looked toward the villa where Ryan had gone, then back at Maya."
        gf "...Okay."
        "She hooked her fingers under the side strings of her bikini bottoms and pulled them a little higher over her hips."
        "The stranger noticed immediately."
        gf "Oh my God. He's actually looking."
        maya "Obviously."
        maya "Ready?"
        gf "For wha—"
        "Maya gave her a quick playful spank."
        gf "Maya!"
        "Maya burst out laughing. Leia was bright red, but laughing too."
        "The strangers had seen it."
        $ set_story_value("ch01_d2_split", "ryan_julian_leia_maya")
        $ set_story_flag("ch01_d2_exhibition_pool_tease")

    else:
        maya "We'll get them."
        friend "Works for me."
        "Maya caught Julian by the arm and steered him toward the villa, leaving Leia and me beside the pool."
        "Leia watched them disappear, then leaned against me."
        gf "I really like her."
        mc "Yesterday you were conducting a background check."
        gf "Due diligence."
        mc "Of course."
        "She kissed my shoulder, still visibly embarrassed whenever she remembered the audience farther down the deck."
        $ set_story_value("ch01_d2_split", "ryan_leia_julian_maya")

    $ set_story_flag("ch01_d2_scene_16_complete")
    jump ch01_day2_scene_17_pool_return


label ch01_day2_scene_17_pool_return:

    scene bg ch01_pool_day
    with dissolve

    $ d2_split = get_story_value("ch01_d2_split")

    if d2_split == "ryan_maya_leia_julian":
        "Back at the pool, Julian's attention snapped toward something buzzing near the loungers."
        friend "No."
        gf "What?"
        "He was already backing away."
        friend "Bee."
        gf "Where?"
        "The bee drifted toward him."
        friend "NOPE."
        "Julian jumped straight into the pool."
        gf "You left me?!"
        "Then the bee changed direction."
        gf "Oh, come on!"
        "Leia jumped in after him."

        "For several seconds neither of them cared about anything except finding the bee."
        gf "Where is it?!"
        friend "I don't know."
        gf "What do you mean you don't know?!"
        friend "I mean I value my life."
        gf "It's a bee!"
        friend "Then why did YOU jump in?"

        "Julian looked back at her."
        "His expression changed."
        "He immediately looked away."

        gf "...What?"
        friend "Uh."
        gf "What?"
        friend "Leia."
        gf "What?!"
        friend "Your... top."

        "Leia froze."
        "She looked down."

        gf "OH MY GOD!"

        "She dropped lower into the water and crossed both arms tightly over her chest, face burning."
        gf "Don't look!"
        friend "I'm not!"
        gf "Where is it?!"

        "Julian found the bikini top floating several feet away."
        friend "Over there."
        gf "GET IT!"
        friend "Why me?!"
        gf "JULIAN!"

        "As Julian started toward it, Leia glanced toward the strangers on the pool deck."
        "They were staring."
        gf "Oh my God."
        friend "What now?"
        gf "They saw."
        friend "Don't look at them."
        gf "I already looked!"

        "Maya and I rounded the corner carrying the drinks."
        "Then I stopped."

        $ enter_cinematic_mode()
        scene cg ch01_d2_pool_top_accident
        with dissolve

        "Leia was chest-deep in the pool, flushed bright red, both arms locked across herself."
        "Julian was in the water with her, swimming toward the bikini top floating several feet away."
        "The same strangers from earlier were still watching."
        "I had arrived at the exact moment that explained the least."

        $ exit_cinematic_mode()
        scene bg ch01_pool_day
        with dissolve

        "Leia saw me. Her eyes widened."
        gf "Ryan—"
        maya "...What the hell happened?"
        gf "There was a bee and Julian jumped in and then it came at me so I jumped in and I didn't know my top came off—"
        friend "Bee."
        "Maya looked at Julian."
        maya "Of course."

        "Leia looked directly at me after the explanation, still mortified and waiting for my reaction."
        "Julian reached the top without turning back toward her."
        friend "Got it."
        "He pushed it across the water. Leia caught it awkwardly with one hand while keeping herself covered with the other."

        $ set_story_flag("ch01_d2_pool_suspicion")
        $ set_story_value("ch01_d2_pool_incident", "leia_julian_bee_top_off")

    elif d2_split == "ryan_julian_leia_maya":
        "Maya was still laughing about the strangers when a bee drifted toward the loungers."
        maya "Wait."
        gf "You're not doing that again."
        maya "No. Bee."
        gf "What?"

        "The bee moved closer. Both women backed toward the pool."
        gf "Nope."
        "Leia jumped. Maya went in with her."

        "Leia surfaced, pushing wet hair from her face."
        maya "Leia."
        gf "What?"
        "Maya pointed toward the bikini top floating away from them."
        "Leia looked down and immediately folded her arms across herself."
        gf "...Oh my God."
        "The strangers they had been teasing moments earlier were still watching."

        "Julian and I returned with the drinks to find Maya trying to reach the floating top while Leia hid lower in the water."
        maya "Bee."
        gf "Don't."
        maya "I'm explaining!"
        "There was no mystery about what had happened. Maya had seen the whole thing."
        $ set_story_value("ch01_d2_pool_incident", "leia_maya_bee_top_off")

    else:
        "Leia and I were still beside the pool when a bee wandered too close to the loungers."
        gf "Ryan."
        mc "Don't move."
        gf "That is never reassuring."

        "It drifted closer."
        "Leia grabbed my arm, then dodged behind me when it changed direction."
        mc "Leia, wait—"
        gf "NOPE."

        "She jumped into the pool."
        "I reached for her a fraction too late, then went in after her."

        "Leia surfaced and looked around for the bee."
        "Her bikini top surfaced several feet away."
        "The strangers saw it at the same time I did."

        mc "Babe."
        gf "What?"
        "I pointed."
        "Leia looked down, gasped and immediately covered herself."
        gf "Oh my God."
        "I moved between her and the strangers while reaching for the floating top."
        "By the time Maya and Julian returned with the drinks, I was handing it back to her."
        maya "What happened?"
        gf "Bee."
        friend "Where?"
        "Julian stopped dead and scanned the pool deck."
        maya "Relax. It's gone."
        friend "You don't know that."
        $ set_story_value("ch01_d2_pool_incident", "leia_ryan_bee_top_off")

    $ set_story_flag("ch01_d2_scene_17_complete")
    jump ch01_day2_scene_18_pool_aftermath


label ch01_day2_scene_18_pool_aftermath:

    if get_story_value("ch01_d2_pool_incident") == "leia_julian_bee_top_off":
        "Once Leia had retied her top and climbed out, she came straight to me."
        "The embarrassment still hadn't left her face."

        gf "You're being quiet."

        $ d2_pool_reassure_text = format_choice("ch01_d2_pool_reassure", "I believe you. It just looked insane for a second.")
        $ d2_pool_honest_text = format_choice("ch01_d2_pool_honest_jealous", "I believe you. I still didn't like walking in on it.")
        $ d2_pool_accuse_text = format_choice("ch01_d2_pool_accuse", "That was a very convenient explanation.")

        menu:
            "[d2_pool_reassure_text]":
                $ apply_choice("ch01_d2_pool_reassure")
                $ set_story_value("ch01_d2_pool_response", "reassured")
                mc "I believe you. It just looked insane for a second."
                "Leia's shoulders relaxed."
                gf "It felt insane too."
                mc "Especially Julian abandoning you."
                friend "The bee had positional advantage."

            "[d2_pool_honest_text]":
                $ apply_choice("ch01_d2_pool_honest_jealous")
                $ set_story_value("ch01_d2_pool_response", "honest_jealous")
                mc "I believe you. I still didn't like walking in on it."
                gf "Okay."
                mc "I'm not blaming you."
                gf "I know."
                "She squeezed my hand once before letting go."

            "[d2_pool_accuse_text]":
                $ apply_choice("ch01_d2_pool_accuse")
                $ set_story_value("ch01_d2_pool_response", "accused")
                mc "That was a very convenient explanation."
                "Leia stared at me."
                gf "Are you serious?"
                mc "I'm saying what it looked like."
                gf "And I'm telling you what happened."
                "She stepped away before the conversation could turn into something larger in front of everyone."

    elif get_story_value("ch01_d2_pool_incident") == "leia_maya_bee_top_off":
        "Maya eventually retrieved Leia's top and passed it back under the water."
        "Once Leia had recovered, she looked toward the strangers and then toward me."
        gf "That went further than planned."
        mc "The bee?"
        gf "Everything."
        "Her embarrassment was real. So was the fact that she chose to process the attention with me."
    else:
        "Once Leia had retied her top, she stayed close enough that our shoulders kept touching."
        "The strangers had seen more than either of us intended. There was no ambiguity about how it happened."
        "Maya spent the next five minutes trying to convince Julian that the bee had already left."
        friend "That's exactly what the bee wants me to think."

    $ set_story_value("ch01_d2_route_lane_post_pool", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_18_complete")
    jump ch01_day2_scene_19_change_for_evening


label ch01_day2_scene_19_change_for_evening:

    scene bg ch01_master_bedroom
    with dissolve

    "Later, Maya followed Leia upstairs again while everyone changed for dinner."

    gf "Was Ryan always like this?"
    maya "Define 'this.'"
    gf "Annoying."
    maya "Yes."
    gf "That was fast."
    maya "You asked an easy one."

    "Maya told her a story about a younger version of me getting hopelessly lost while insisting I knew where I was going."

    gf "He still does that."
    maya "Some things are foundational."

    "By then, Leia wasn't treating Maya like Ryan's mysterious female friend anymore. She was treating her like somebody she might actually keep."

    $ set_story_value("ch01_d2_leia_maya_comfort", 4)
    $ set_story_flag("ch01_d2_scene_19_complete")
    jump ch01_day2_scene_20_dinner_outfit


label ch01_day2_scene_20_dinner_outfit:

    $ d2_lane = ch01_d2_route_lane()

    if d2_lane in ("exhibitionism", "ntr_risk"):
        "Leia held up a loose, low-cut evening top with a fitted skirt. The neckline moved noticeably whenever she leaned forward."
        maya "That one is dangerous."
        gf "Dangerous?"
        maya "In the sense that you'll spend the whole night pretending you don't know exactly what it does."
        gf "I have no idea what you're talking about."
        maya "Sure."
        $ set_story_value("ch01_d2_dinner_outfit", "loose_low_cut")
    else:
        "Leia chose a polished dinner outfit she could forget about once she put it on."
        maya "Cute."
        gf "Comfortable."
        maya "Also valid."
        $ set_story_value("ch01_d2_dinner_outfit", "secure_date")

    # Final Day Two outfit art is pending. Reuse the existing dinner-dress layer
    # while narrative state tracks the actual Day Two cut.
    $ grant_story_outfit("resort_dinner_dress", equip=True)

    $ set_story_value("ch01_d2_route_lane_dinner", d2_lane)
    $ set_story_flag("ch01_d2_scene_20_complete")
    jump ch01_day2_scene_21_pre_sunset


label ch01_day2_scene_21_pre_sunset:

    scene bg ch01_d2_sunset
    with fade

    "We left early enough to walk along the water before dinner."
    "Maya and Julian drifted ahead of us, still arguing about music."

    maya "Your playlist has finance-bro energy."
    friend "You heard three songs."
    maya "Three too many."

    "Leia watched them for a few seconds, then slipped her hand into mine."

    $ set_story_flag("ch01_d2_scene_21_complete")
    jump ch01_day2_scene_22_sunset_couple


label ch01_day2_scene_22_sunset_couple:

    with dissolve

    gf "Those two are getting pretty friendly."

    $ d2_sunset_connect_text = format_choice("ch01_d2_sunset_connect", "Good. Means I get you to myself for five minutes.")
    $ d2_sunset_tease_text = format_choice("ch01_d2_sunset_tease", "What, jealous of Julian now?")

    if ch01_d2_route_lane() == "ntr_risk":
        $ d2_sunset_ignore_text = format_day2_risk_choice("ch01_d2_sunset_ignore_gate", "Ignore it and check your phone.", severity="soft")
        menu:
            "[d2_sunset_connect_text]":
                $ apply_choice("ch01_d2_sunset_connect")
                $ set_story_value("ch01_d2_sunset_response", "connected")
                mc "Good. Means I get you to myself for five minutes."
                "Leia looked at me, then smiled and moved closer."
                gf "Better answer than I expected."

            "[d2_sunset_tease_text]":
                $ apply_choice("ch01_d2_sunset_tease")
                $ set_story_value("ch01_d2_sunset_response", "teased")
                mc "What, jealous of Julian now?"
                gf "No."
                mc "Fast answer."
                gf "Don't start."
                "She nudged my arm and stayed beside me."

            "[d2_sunset_ignore_text]":
                $ apply_choice("ch01_d2_sunset_ignore_gate")
                $ set_story_value("ch01_d2_sunset_response", "ignored_gate")
                $ set_story_value("ch01_d2_ntr_soft_gate", True)
                "I looked at my phone instead of answering."
                "Leia waited beside me."
                gf "...Never mind."
                scene black
                with fade
                centered "[girlfriend_name] will remember this..."
                scene bg ch01_d2_sunset
                with fade
    else:
        menu:
            "[d2_sunset_connect_text]":
                $ apply_choice("ch01_d2_sunset_connect")
                $ set_story_value("ch01_d2_sunset_response", "connected")
                mc "Good. Means I get you to myself for five minutes."
                gf "Smooth."
                mc "Worked."
                "She moved closer."

            "[d2_sunset_tease_text]":
                $ apply_choice("ch01_d2_sunset_tease")
                $ set_story_value("ch01_d2_sunset_response", "teased")
                mc "What, jealous of Julian now?"
                gf "I was making an observation."
                mc "Of course."
                gf "Stop smiling."

    $ set_story_value("ch01_d2_route_lane_post_sunset", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_22_complete")
    jump ch01_day2_scene_23_dinner_reach


label ch01_day2_scene_23_dinner_reach:

    scene bg ch01_d2_dinner
    with fade

    "The table was rectangular. Leia and Maya sat side by side. Julian sat beside me on the opposite side."
    "Leia was directly across from me. Julian had almost the same viewing angle."

    $ d2_lane = get_story_value("ch01_d2_route_lane_post_sunset", ch01_d2_route_lane())

    if d2_lane == "love" or get_story_value("ch01_d2_dinner_outfit") != "loose_low_cut":
        "Halfway through dinner Leia pointed toward a dish in the middle of the table."
        gf "Babe, can you pass that?"
        mc "This?"
        gf "Yeah, thanks."
        "I passed it across. She smiled and continued talking to Maya."
        $ set_story_value("ch01_d2_dinner_reach", "asked_ryan")

    else:
        "Halfway through dinner Leia reached toward a dish in the centre of the table."
        "She could easily have asked me to pass it. She didn't."

        $ enter_cinematic_mode()
        scene cg ch01_d2_dinner_reach
        with dissolve

        "She leaned forward far enough for the loose neckline to shift, making the inner edge of her bra visible from our side of the table."
        "There was nothing hurried about the reach."

        $ exit_cinematic_mode()
        scene bg ch01_d2_dinner

        if get_story_value("ch01_d2_ntr_soft_gate", False) and d2_lane == "ntr_risk":
            "Leia sat back upright."
            "She looked at me first. Then her eyes moved to Julian."
            "A tiny wink. Quick enough that Maya missed it."
            "Julian's expression changed from casual to surprised."
            "Mine did too."
            $ set_story_value("ch01_d2_dinner_wink", True)
            $ set_story_value("ch01_d2_dinner_reach", "winked_julian")
        else:
            "Leia sat back upright and looked directly at me."
            "She gave me a small, innocent smile that made the pretence worse."
            mc "Subtle."
            gf "What?"
            "She knew. I knew she knew."
            $ set_story_value("ch01_d2_dinner_reach", "smiled_at_ryan")

    $ set_story_flag("ch01_d2_scene_23_complete")
    jump ch01_day2_scene_24_dinner_aftermath


label ch01_day2_scene_24_dinner_aftermath:

    if get_story_value("ch01_d2_dinner_wink", False):
        "I did not confront Leia at the table."
        "Julian did not encourage it either. If anything, he seemed unsure what to do with the moment and turned his attention back to Maya."
        "That somehow gave the wink more weight, not less."
    elif get_story_value("ch01_d2_dinner_reach") == "smiled_at_ryan":
        "For the rest of dinner Leia occasionally caught me looking toward her and smiled as though she had no idea why."
    else:
        "Dinner remained easy. Maya and Julian carried most of the argument while Leia and I enjoyed watching them."

    maya "I'm not going home yet."
    friend "Was anyone asking you to?"
    maya "Good. Drinks at the villa."
    gf "Obviously."

    $ set_story_flag("ch01_d2_scene_24_complete")
    jump ch01_day2_scene_25_maya_stays


label ch01_day2_scene_25_maya_stays:

    scene bg ch01_d2_game_night
    with fade

    "There was no discussion about whether Maya was staying for drinks. She simply came back with us."
    "An hour later the coffee table was crowded with bottles, mixers, snacks, and four glasses in various states of neglect."

    maya "We need a game."
    friend "No."
    maya "Never Have I Ever."
    friend "Even more no."
    gf "That means yes."

    "Maya was not drunk enough to slur. She was drunk enough to become dramatically more interested in everybody else's private life."

    $ set_story_flag("ch01_d2_maya_stays_for_drinks")
    $ set_story_flag("ch01_d2_scene_25_complete")
    jump ch01_day2_scene_26_game_rules


label ch01_day2_scene_26_game_rules:

    maya "Normal rules first. If you've done it, you drink."
    friend "I know how the game works."
    maya "You look like someone who reads instruction manuals."
    friend "That doesn't even make sense."

    "The first few rounds were harmless: missed flights, terrible dates, lying about liking someone's cooking."
    "Then Maya's questions became increasingly personal."

    maya "New rule. If you don't want to answer, and you don't want to drink, you lose one piece of clothing."
    friend "That is not a rule."
    maya "It is if everyone agrees."

    "She looked around the room."

    gf "I'm in."
    mc "Fine."
    friend "I hate democracy."
    maya "That is also a yes."

    $ set_story_flag("ch01_d2_strip_penalty_agreed")
    $ set_story_flag("ch01_d2_scene_26_complete")
    jump ch01_day2_scene_27_game_escalates


label ch01_day2_scene_27_game_escalates:

    maya "Never have I ever been jealous of someone who technically wasn't doing anything wrong."

    "Leia looked directly at her drink."
    maya "Oh, that's adorable. Drink."
    gf "I hate you."
    maya "You met me today. Give it time."

    "Leia drank. I knew exactly which conversation she was thinking about."

    maya "Never have I ever enjoyed somebody checking me out."

    if partner_stats["exhibitionism"] >= 22:
        "Leia hesitated, then took a small drink."
        "Maya's eyebrows rose. Julian looked toward his own glass instead."
        "Leia looked at me last."
    else:
        "Leia did not drink. Maya accepted that without comment and moved on."

    maya "Never have I ever deliberately tried to make somebody jealous."

    if get_story_value("ch01_d2_dinner_wink", False):
        "Leia's fingers tightened around her glass. She did not drink."
        "I noticed."
    else:
        "Nobody moved for a second. Maya laughed and changed the question."

    maya "Okay. Better one. Never have I ever been attracted to somebody I probably shouldn't be."

    "The room went noticeably quieter."

    friend "Absolutely not."
    maya "Not drinking?"
    friend "No."
    maya "Then you know the penalty."

    $ set_story_flag("ch01_d2_scene_27_complete")
    jump ch01_day2_scene_28_julian_strips


label ch01_day2_scene_28_julian_strips:

    "Julian stared at Maya, then pulled his shirt over his head."

    friend "Happy?"
    maya "Immensely."
    gf "You could have just taken a drink."
    friend "I am pacing myself."

    "Three questions later, Maya found another one Julian refused to answer."

    maya "Drink."
    friend "No."
    maya "Answer."
    friend "Also no."
    maya "Then pants."

    "Julian looked down at himself."

    friend "This game is rigged."
    maya "Correct."

    "He stood, removed his trousers with considerably less dignity than he wanted, and dropped back onto the sofa in his underwear."

    $ enter_cinematic_mode()
    scene cg ch01_d2_julian_underwear_reveal
    with dissolve

    "The joke stalled for a beat. His underwear made the room go unexpectedly quiet for reasons nobody needed to explain out loud."

    $ exit_cinematic_mode()
    scene bg ch01_d2_game_night

    maya "...Oh."
    friend "Don't."
    maya "I didn't say anything."
    friend "Your face did."

    $ set_story_value("ch01_d2_julian_clothes", "underwear")
    $ set_story_flag("ch01_d2_julian_reveal_seen")

    $ d2_game_reassure_text = format_choice("ch01_d2_game_reassure", "Save Leia from the awkward silence and change the subject.")
    $ d2_game_tease_text = format_choice("ch01_d2_game_tease", "Catch Leia looking and tease her quietly.")
    $ d2_game_ignore_text = format_choice("ch01_d2_game_ignore", "Say nothing and let the moment sit.")

    menu:
        "[d2_game_reassure_text]":
            $ apply_choice("ch01_d2_game_reassure")
            mc "Next question before Julian starts charging admission."
            friend "Thank you."
            maya "Cowards."
            "Leia laughed and the room moved on."
            $ set_story_value("ch01_d2_julian_reveal_response", "redirected")

        "[d2_game_tease_text]":
            $ apply_choice("ch01_d2_game_tease")
            "Leia glanced once, looked away, then realised I'd caught her."
            mc "Subtle."
            gf "I looked because everyone looked."
            mc "Of course."
            gf "Stop."
            "Her embarrassment was directed at me, not away from me."
            $ set_story_value("ch01_d2_julian_reveal_response", "couple_tease")

        "[d2_game_ignore_text]":
            $ apply_choice("ch01_d2_game_ignore")
            "I said nothing."
            "Leia looked once because everyone had looked. A few questions later, she looked again when nobody was talking about it anymore."
            $ set_story_value("ch01_d2_julian_reveal_response", "looked_again")

    $ set_story_flag("ch01_d2_scene_28_complete")
    jump ch01_day2_scene_29_game_winds_down


label ch01_day2_scene_29_game_winds_down:

    "The game eventually collapsed under the weight of its own rules. Maya had lost one layer, Julian was still refusing to put his trousers back on out of principle, and Leia was laughing hard enough to need water."

    maya "I win."
    friend "There was no winner."
    maya "Spoken like somebody who lost his pants."

    "Julian collected empty glasses while Maya followed him toward the kitchen, still teasing him about the bee."

    if get_story_value("ch01_d2_ntr_soft_gate", False):
        "Leia watched them leave together. Her expression was difficult to read."
    else:
        gf "They're definitely flirting."
        mc "Probably."
        gf "Good for them."

    "A few minutes later the four of us split for the night. Maya took the spare sofa rather than attempting the trip back after drinking."

    $ set_story_flag("ch01_d2_scene_29_complete")
    jump ch01_day2_scene_30_bedroom


label ch01_day2_scene_30_bedroom:

    scene bg ch01_villa_bedroom_night
    with fade

    "The bedroom door closed behind us. For the first time since breakfast, there was nobody else in the conversation."

    $ d2_lane = ch01_d2_route_lane()
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)
    $ d2_wink = get_story_value("ch01_d2_dinner_wink", False)
    $ d2_pool_suspicion = get_story_flag("ch01_d2_pool_suspicion")

    if d2_soft_gate and d2_wink:
        "Leia came closer first. I didn't respond immediately."

        gf "Ryan?"

        $ d2_wink_repair_text = format_choice("ch01_d2_wink_repair", "Why did you do that at dinner?")
        $ d2_wink_reject_text = format_day2_risk_choice("ch01_d2_wink_reject_hard", "Not tonight. Turn away from her.", severity="hard")

        menu:
            "[d2_wink_repair_text]":
                $ apply_choice("ch01_d2_wink_repair")
                mc "Why did you do that at dinner?"
                "Leia knew immediately what I meant."
                gf "The wink."
                mc "Yeah."
                gf "I was annoyed."
                mc "At me?"
                gf "You barely spoke to me at sunset. I said something and you just disappeared into your phone."
                mc "So you wanted a reaction."
                gf "Maybe. It was stupid."
                mc "It bothered me."
                gf "I know. I'm sorry."
                "For once neither of us tried to turn the discomfort into a joke."
                mc "Talk to me next time."
                gf "You too."
                $ set_story_value("ch01_d2_ntr_soft_gate_repaired", True)
                $ set_story_value("ch01_d2_end_route", "love_repaired")
                "They reconnect, and the rest of the night stays private between them."
                scene black
                with dissolve

            "[d2_wink_reject_text]":
                $ apply_choice("ch01_d2_wink_reject_hard")
                $ set_story_value("ch01_d2_ntr_confirmed", True)
                $ set_story_value("ch01_d2_end_route", "ntr_confirmed")
                mc "Not tonight."
                "I turned away from her."
                "Leia stood beside the bed for a few seconds without saying anything."
                gf "Okay."
                "She climbed in on her side and faced the other direction."
                "No argument followed. The silence was worse."
                scene black
                with fade
                if current_choice_mode() == "developer":
                    centered "NTR ROUTE CONFIRMED — ch01_d2_ntr_confirmed = True"
                elif current_choice_mode() == "full":
                    centered "NTR route confirmed."
                elif current_choice_mode() == "insight":
                    centered "A major route boundary has been crossed."
                else:
                    centered "Something changed tonight."

    elif d2_pool_suspicion and not d2_soft_gate:
        "Leia came closer, but I was still thinking about the pool."

        gf "You're doing it again."
        mc "Doing what?"
        gf "Thinking loudly."
        mc "What actually happened at the pool?"

        "Leia blinked."

        gf "The bee?"
        mc "Yeah."
        gf "Exactly what I told you. Julian panicked, jumped in, it came toward me, I jumped in too, and my top came loose."
        mc "I know what you told me."
        gf "Then what are you asking?"

        $ d2_bed_love_text = format_choice("ch01_d2_bed_pool_love", "I didn't like seeing it, but I believe you.")
        $ d2_bed_ex_text = format_choice("ch01_d2_bed_pool_exhibition", "It bothered me... and I haven't stopped thinking about it.")
        $ d2_bed_accuse_text = format_choice("ch01_d2_bed_pool_accuse", "I still think it looked convenient.")

        menu:
            "[d2_bed_love_text]":
                $ apply_choice("ch01_d2_bed_pool_love")
                mc "I didn't like seeing it, but I believe you."
                "Leia's expression softened immediately."
                gf "Nothing happened."
                mc "I know."
                gf "And if something ever did happen that mattered, I'd tell you."
                mc "I know that too."
                $ set_story_value("ch01_d2_end_route", "love")
                "The tension finally leaves the room, and they reconnect before the scene fades out."
                scene black
                with dissolve

            "[d2_bed_ex_text]":
                $ apply_choice("ch01_d2_bed_pool_exhibition")
                mc "It bothered me... and I haven't stopped thinking about it."
                gf "Because you were jealous?"
                mc "Partly."
                "She stared at me for a second longer. Then understanding arrived."
                gf "Wait. You found some part of it exciting?"
                mc "I liked knowing nothing happened. The rest of it was... complicated."
                gf "You're weird."
                mc "You were checking if he was looking yesterday."
                gf "We're not talking about me."
                "She was smiling again."
                $ set_story_value("ch01_d2_end_route", "exhibitionism")
                "The near-miss becomes something they discuss together instead of something separating them. The scene fades out on reconciliation."
                scene black
                with dissolve

            "[d2_bed_accuse_text]":
                $ apply_choice("ch01_d2_bed_pool_accuse")
                mc "I still think it looked convenient."
                "Leia stepped back."
                gf "Then I don't know what else you want me to say."
                "They go to bed without resolving it. The route has not broken, but neither has it healed."
                $ set_story_value("ch01_d2_end_route", "mixed_unresolved")
                scene black
                with fade

    elif d2_lane == "exhibitionism":
        "Leia had barely closed the bedroom door before I looked at her."

        mc "You knew exactly what you were doing at dinner."
        gf "I have no idea what you're talking about."
        mc "You could've asked me to pass that dish."
        gf "Could have."
        mc "You leaned across half the table."
        "She fought the smile for several seconds and lost."
        gf "...Maybe."
        mc "Maybe?"
        gf "I wanted to know what it felt like when it wasn't an accident."
        mc "And?"
        gf "Different."
        mc "Bad different?"
        gf "No."

        "They finally acknowledge that Leia is choosing some of these moments on purpose, and that Ryan is part of the exploration rather than outside it. The scene fades on their reconciliation."
        $ set_story_value("ch01_d2_end_route", "exhibitionism")
        scene black
        with dissolve

    else:
        "Leia dropped onto the edge of the bed and looked up at me."

        gf "Okay. I like Maya."
        mc "Yesterday you were interrogating me about her."
        gf "Due diligence."
        mc "You've used that excuse twice now."
        gf "Because it's good."

        "I sat beside her. She leaned into me almost immediately."
        "The day had been noisy, ridiculous, and occasionally embarrassing. None of it had put distance between us."

        gf "Come here."
        "They reconnect, and the scene fades out on a secure relationship beat."
        $ set_story_value("ch01_d2_end_route", "love")
        scene black
        with dissolve

    $ set_story_flag("ch01_d2_scene_30_complete")
    $ set_story_flag("ch01_day_02_complete")

    centered "{size=46}CHAPTER ONE — DAY TWO COMPLETE{/size}\n\n{size=25}Current development build ends here{/size}"

    return
