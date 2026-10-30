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

        "Leia folded her arms across herself, then instinctively rushed behind Julian and clung to his back, using him to shield herself from the people on the deck."
        "Julian went rigid with surprise, keeping his hands clear and his eyes turned away."
        gf "Don't look!"
        friend "I'm not!"
        gf "Where is it?!"
        friend "Stay behind me. I'll find it."

        "Julian spotted the bikini top floating several feet away."
        friend "Over there."
        gf "GET IT!"
        friend "Why me?!"
        gf "JULIAN!"

        "Leia stayed tucked behind Julian as he edged toward the floating top, still holding on to his shoulders."
        "Over his shoulder, she caught sight of the strangers on the deck."
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

        "Leia was clinging to Julian's back in the pool, hiding behind his shoulders while he kept his hands away from her."
        "Her bikini top floated several feet away. The strangers from earlier were still watching."
        "I had arrived at the exact moment that explained the least."

        $ exit_cinematic_mode()
        scene bg ch01_pool_day
        with dissolve

        "Leia saw me over Julian's shoulder. Her eyes widened."
        "She let go of him at once, sinking lower into the water and covering herself with her arms."
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
        "Leia looked down and folded her arms across herself."
        gf "...Oh my God."
        "She darted behind Maya and clung to her back, using her friend as a shield from the strangers on the deck."
        "Maya steadied herself, startled, then turned her attention toward the floating top."
        maya "I've got you. Stay behind me."
        "The strangers they had been teasing moments earlier were still watching."

        "Julian and I returned with the drinks to find Leia still hiding against Maya's back while Maya tried to reach the floating top."
        "Leia saw us, let go of Maya, and sank lower into the water with her arms across herself."
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
        "Leia looked down, gasped and covered herself."
        gf "Oh my God."
        "Before I could say anything, she darted behind me and clung to my back, using me to block the strangers' view."
        mc "I've got you. Stay behind me."
        "I kept myself between her and the deck as I moved toward the floating top."
        "She let go just long enough for me to retrieve it."
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
        "Leia retied it beneath the surface before climbing out, still visibly red from what had happened."
        "Her eyes flicked toward the strangers. They were still there."
        "Then she came straight to me."

        gf "Okay."
        mc "Okay?"
        gf "That went way further than I meant it to."
        mc "The bee?"
        "Leia gave me a look."
        gf "Everything."

        "She lowered her voice."
        gf "The strings thing was on purpose."
        gf "Maya was being Maya, and I said yes."
        gf "I knew they were looking."
        "She glanced toward the strangers again, then back at me."
        gf "But that?"
        gf "That was not on purpose."

        mc "I know."
        "Some of the tension left her shoulders."

        gf "You saw them looking before you left."
        mc "Yeah."
        gf "And you were okay with... us playing with it?"
        mc "With what we were doing together? Yeah."

        "Leia's embarrassment didn't disappear, but the small smile that followed belonged to me."
        gf "Okay."
        gf "Because I think I liked that part."
        "She immediately covered her face for half a second."
        gf "Not the losing-my-top part."
        mc "Important distinction."
        gf "Very important."

        "Maya called something unhelpful from the pool. Leia ignored her and stayed beside me."
        "The attention had gone further than Leia intended, but she brought the experience back into our relationship instead of leaving Ryan outside it."
        $ set_story_flag("ch01_d2_exhibition_pool_shared_with_ryan")
    else:
        "Once Leia had retied her top, she stayed close enough that our shoulders kept touching."
        "The strangers had seen more than either of us intended. There was no ambiguity about how it happened."
        "Maya spent the next five minutes trying to convince Julian that the bee had already left."
        friend "That's exactly what the bee wants me to think."

    $ set_story_value("ch01_d2_route_lane_post_pool", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_18_complete")
    jump ch01_day2_scene_19_change_for_evening


label ch01_day2_scene_19_change_for_evening:

    # Post-pool decompression. Maya leaves before sunset so the route-specific
    # Ryan/Leia conversation can happen without an audience.
    scene bg ch01_pool_lounge
    with dissolve

    "The pool incident took most of the energy out of the afternoon."
    "For a while the four of us stayed around the table, drinking water, drying off, and letting the embarrassment turn back into something we could laugh about."

    maya "Okay. I actually need to go home if I'm supposed to look human tonight."
    friend "You look fine."
    maya "That is because your standards are compromised by sunglasses."
    gf "You're coming back for dinner, right?"
    maya "Obviously."

    "Leia walked Maya toward the villa entrance."
    maya "Text me if these two somehow manage to ruin the evening before I get back."
    gf "Which two?"
    maya "Yes."

    jump ch01_day2_scene_19b_leia_asks_maya


label ch01_day2_scene_20_dinner_outfit:

    # Sunset route payoff. The legacy label name is preserved for save
    # compatibility even though the scene now resolves sunset before outfits.
    scene bg ch01_d2_sunset
    with fade

    $ d2_lane = get_story_value("ch01_d2_route_lane_post_pool", ch01_d2_route_lane())

    "The sun had dropped low enough to turn the water orange."
    "For the first time since Maya arrived, there was nobody else filling the silence."

    if d2_lane == "love":
        "Leia leaned against the railing beside me, then glanced toward the upper floor."
        gf "Julian's still inside?"
        mc "Yeah."
        gf "And he can't see this side of the pool from his room?"
        mc "Not unless he's hanging out of the window."
        gf "Good."

        "She took my hand and pulled me toward the sheltered side of the pool, out of the sightline from Julian's room."
        mc "What are you doing?"
        gf "Something private."
        mc "Outside."
        gf "Private enough."

        $ enter_cinematic_mode()
        scene cg ch01_d2_love_pool_oral_01
        with dissolve

        "Leia dropped to her knees between me and the low wall, still checking the upper windows before looking back up at me."
        gf "Nobody can see us."
        mc "You checked?"
        gf "Obviously."

        scene cg ch01_d2_love_pool_oral_02
        with dissolve

        "What followed was quick, reckless and deliberately hidden from the rest of the villa."
        "The risk came from being outside, not from wanting an audience."
        "When we finally pulled ourselves back together, Leia was trying not to laugh at how absurdly pleased with herself she looked."

        $ exit_cinematic_mode()
        scene bg ch01_d2_sunset
        with dissolve

        gf "Nobody saw."
        mc "You keep saying that."
        gf "Because nobody did."

        "We sat together at the edge of the pool while the light faded."
        gf "Today was actually nice."
        mc "Even the bee?"
        gf "The bee is excluded from this review."
        mc "Maya?"
        gf "I like her."
        mc "You've made that very clear."
        gf "And..."
        "She bumped her shoulder into mine."
        gf "I like this."
        mc "The holiday?"
        gf "Us."
        "There was nothing complicated in the way she said it."

        $ set_story_value("ch01_d2_sunset_response", "love_connected")
        $ set_story_flag("ch01_d2_love_sunset_oral")

    elif d2_lane == "exhibitionism":
        "Leia sat beside me, knees drawn up, still thinking about the pool."

        gf "Maya is a terrible influence."
        mc "Which part are we blaming her for?"
        gf "The strings."
        mc "Ah. Those strings."
        gf "Don't."
        mc "You pulled them higher while two guys were staring at you."
        gf "When you say it like that, it sounds terrible."
        mc "I'm not complaining."

        "Leia covered her face for a second, then peeked at me through her fingers."

        gf "And then she smacked my ass."
        mc "You didn't look very angry."
        gf "I was embarrassed."
        mc "That's not what I said."
        gf "Ryan."
        mc "Leia."

        "She lasted another few seconds before giving up."

        gf "...Fine. It was kind of hot."
        mc "The spanking?"
        gf "The whole thing."
        gf "Knowing they were looking. Knowing you knew they were looking."
        mc "And losing your top?"
        gf "No."
        "She answered that one immediately."
        gf "I mean... not like that."
        gf "I was mortified."
        mc "Was?"
        gf "Don't start."
        "She stared out at the water."
        gf "Thinking about it now is different."
        mc "Different how?"
        gf "...You know how."

        mc "My girlfriend's secretly an exhibitionist."
        gf "I am not."
        "I looked at her."
        gf "...Shut up."

        mc "If it turns you on, it turns you on."
        mc "You don't have to be embarrassed telling me."

        "Her expression softened."

        gf "I think part of why I liked it was because you knew."

        "That mattered more than the strangers had."

        gf "What if I wanted to do something like that again?"
        mc "Tonight?"
        gf "I didn't say tonight."
        mc "You didn't say not tonight."

        "Leia smiled and leaned into me."

        $ set_story_value("ch01_d2_sunset_response", "exhibition_shared")
        $ set_story_flag("ch01_d2_exhibition_sunset_shared")

    else:
        "Leia stood beside me for a while before finally turning toward me."

        gf "Can I ask you something?"
        mc "Yeah?"
        gf "Are we okay?"
        "I looked at her."
        gf "Every time I look at you today, you're somewhere else."
        gf "If something's bothering you, just tell me."

        $ d2_sunset_connect_text = format_choice("ch01_d2_sunset_connect", "Tell her the truth.")
        $ d2_sunset_partial_text = format_choice("ch01_d2_sunset_partial", "I've just been in my own head.")
        $ d2_sunset_ignore_text = format_day2_risk_choice("ch01_d2_sunset_ignore_gate", "I'm fine.", severity="soft")

        menu:
            "[d2_sunset_connect_text]":
                $ apply_choice("ch01_d2_sunset_connect")
                $ set_story_value("ch01_d2_sunset_response", "opened_up")

                mc "I'm not okay."
                "Leia waited."
                mc "I slept badly. I've been jealous. The pool thing looked insane for about three seconds, and instead of saying any of that I've been acting like an idiot."
                gf "I know nothing happened with Julian."
                mc "I know."
                gf "Then talk to me when your brain decides otherwise."
                mc "Fair."
                "She took my hand."
                gf "That's all I wanted."

            "[d2_sunset_partial_text]":
                $ apply_choice("ch01_d2_sunset_partial")
                $ set_story_value("ch01_d2_sunset_response", "partial_honesty")

                mc "I've just been in my own head."
                gf "About me?"
                mc "About everything."
                "She studied me, then nodded."
                gf "Okay. Just don't disappear on me."
                mc "I won't."
                "It was not the whole truth, but it was enough that she stopped having to guess."

            "[d2_sunset_ignore_text]":
                $ apply_choice("ch01_d2_sunset_ignore_gate")
                $ set_story_value("ch01_d2_sunset_response", "ignored_gate")
                $ set_story_value("ch01_d2_ntr_soft_gate", True)

                mc "I'm fine."
                gf "Ryan."
                mc "I said I'm fine."

                "My phone buzzed against the table."
                "I checked it instead of looking at her."

                gf "...Okay."

                "Leia turned back toward the sunset."
                "She'd been checking for me all day. This time, when she looked away, she didn't look back."

                if current_choice_mode() == "developer":
                    centered "NTR SOFT GATE — ch01_d2_ntr_soft_gate = True"
                elif current_choice_mode() == "full":
                    centered "Major relationship consequence."
                elif current_choice_mode() == "insight":
                    centered "Leia stops repeatedly reaching back toward Ryan."

    "A few minutes later Julian came back downstairs, freshly changed and completely unaware of what had just happened."

    friend "Are we still doing dinner at eight?"

    if get_story_value("ch01_d2_ntr_soft_gate", False):
        gf "Yeah."
        "Leia answered without looking at me."
    else:
        gf "Yeah."
        "Leia looked at me as she answered, and I nodded."

    $ set_story_value("ch01_d2_route_lane_post_sunset", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_20_complete")
    jump ch01_day2_scene_21_pre_sunset


label ch01_day2_scene_21_pre_sunset:

    # Getting ready after sunset. The Black Cutout Mini bought at the boutique is
    # explicitly reserved for Day Three and is never used for this dinner.
    scene bg ch01_master_bedroom
    with dissolve

    $ d2_lane = get_story_value("ch01_d2_route_lane_post_sunset", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    if d2_soft_gate:
        "Leia came upstairs, opened her suitcase and chose without asking me."
        "She pulled out the bolder evening option she had already packed for the trip: a loose low-cut top with a fitted skirt."
        "The Black Cutout Mini from the boutique stayed folded in its bag."

        $ set_story_value("ch01_d2_dinner_outfit", "loose_low_cut")
        $ set_story_value("ch01_d2_dinner_outfit_id", "d2_loose_low_cut")
        $ grant_story_outfit("d2_loose_low_cut", equip=True)
        $ set_story_value("ch01_d2_dinner_outfit_source", "leia")

    elif d2_lane == "exhibitionism":
        "Leia held up the two evening options and looked at me."

        gf "After everything we just talked about..."
        gf "Which one?"
        mc "The low-cut one."
        "Her mouth curved into a small smile."
        gf "Thought so."
        mc "Too much?"
        gf "You tell me."
        mc "Wear it."
        gf "Okay."

        "She changed with the easy awareness that I had chosen the bolder option with her, not for an audience she was hiding from me."

        $ set_story_value("ch01_d2_dinner_outfit", "loose_low_cut")
        $ set_story_value("ch01_d2_dinner_outfit_id", "d2_loose_low_cut")
        $ grant_story_outfit("d2_loose_low_cut", equip=True)
        $ set_story_value("ch01_d2_dinner_outfit_source", "ryan")

    else:
        "Leia came upstairs with two outfits over one arm."

        gf "Babe, help me pick?"

        menu:
            "Let me choose your outfit.":
                python:
                    # The Black Cutout Mini is reserved for Day Three, so it is
                    # never offered in the Day Two dinner picker even when owned.
                    d2_love_outfit_options = [
                        outfit_id
                        for outfit_id in love_outfit_candidates(
                            story_ids=("resort_dinner_dress", "d2_loose_low_cut"),
                        )
                        if outfit_id != "boutique_cutout_mini"
                    ]
                    d2_love_outfit_pick = renpy.call_screen(
                        "leia_love_outfit_picker",
                        options=d2_love_outfit_options,
                        title_text="Pick Leia's Day Two dinner outfit",
                    )
                    love_route_wear_request(d2_love_outfit_pick, route_lane="love")
                    set_story_value("ch01_d2_dinner_outfit_id", d2_love_outfit_pick)
                    set_story_value(
                        "ch01_d2_dinner_outfit",
                        "loose_low_cut" if love_outfit_is_daring(d2_love_outfit_pick) else "secure_date",
                    )
                    set_story_value("ch01_d2_dinner_outfit_source", "ryan")

                mc "Wear the [outfit_name(d2_love_outfit_pick)]."
                gf "Okay."
                "She accepted the choice because she had invited it."

            "Wear whatever you feel best in.":
                $ set_story_value("ch01_d2_dinner_outfit", "secure_date")
                $ set_story_value("ch01_d2_dinner_outfit_id", "resort_dinner_dress")
                $ set_story_value("ch01_d2_dinner_outfit_source", "leia")
                $ grant_story_outfit("resort_dinner_dress", equip=True)

                mc "Wear whatever you feel best in."
                gf "Then I'm choosing comfort."

        "The Black Cutout Mini stayed in its boutique bag for another day."

    $ set_story_flag("ch01_d2_boutique_black_mini_reserved_day3")
    $ set_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_21_complete")
    jump ch01_day2_scene_22_sunset_couple


label ch01_day2_scene_22_sunset_couple:

    # Dinner arrival and ordinary group chemistry.
    scene bg ch01_d2_dinner
    with fade

    "Maya was already waiting when the three of us arrived, freshly changed and looking considerably more put together than when she left the pool."

    gf "Okay. So that's why you abandoned us."
    maya "Some of us require preparation."
    friend "You were gone for like two hours."
    maya "And look what I accomplished."

    "We took a rectangular table: Leia beside Maya, Julian beside me on the opposite side."
    "Leia sat directly across from me. Maya sat directly across from Julian."

    maya "Are you ordering anything with honey?"
    friend "Don't."
    gf "Careful. There might be a bee in it."
    friend "I hate all of you."
    gf "You jumped in first and left me with it."
    friend "And yet we're both alive."

    "Food arrived in waves. So did another round of drinks."
    "Maya asked everyone for their favourite part of the trip so far, then rejected Julian's answer because it involved room service."
    "Leia and Maya started planning what they wanted to see tomorrow."
    "Julian criticised my inability to choose from a menu. Maya immediately joined him."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if get_story_value("ch01_d2_ntr_soft_gate", False):
        "Leia was not hostile. She laughed with Maya, argued with Julian and enjoyed dinner."
        "What changed was smaller: she stopped checking whether I was following every moment."
    elif d2_lane == "exhibitionism":
        "Every so often Leia caught my eye across the table and smiled like we were carrying a private conversation nobody else could hear."
    else:
        "Leia and I fell into the small habits that came with four years together: passing the right sauce before the other asked, trading bites, finishing each other's complaints."

    $ set_story_flag("ch01_d2_scene_22_complete")
    jump ch01_day2_scene_23_dinner_reach


label ch01_day2_scene_23_dinner_reach:

    scene bg ch01_d2_dinner
    with dissolve

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    "Halfway through dinner, a shared dish landed near the middle of the table, slightly closer to our side."

    if d2_soft_gate and d2_lane == "ntr_risk":
        "Leia looked at the dish, then leaned across instead of asking me to pass it."

        $ enter_cinematic_mode()
        scene cg ch01_d2_dinner_reach
        with dissolve

        "The loose neckline shifted as she reached."
        "Julian noticed. Not dramatically. Just long enough that Leia caught him before he could look away."

        $ exit_cinematic_mode()
        scene bg ch01_d2_dinner
        with dissolve

        "Leia met his eyes."
        "Then she gave him a tiny wink."

        "Julian looked genuinely surprised."
        "He did not wink back."
        "Leia simply sat down and continued eating."

        "It lasted less than a second. Long enough that I knew I hadn't imagined it."

        $ set_story_value("ch01_d2_dinner_wink", True)
        $ set_story_value("ch01_d2_dinner_reach", "winked_julian")

    elif d2_lane == "exhibitionism" and get_story_value("ch01_d2_dinner_outfit") == "loose_low_cut":
        "Leia looked at the dish."
        "Then she looked at me."
        "She could have asked me to pass it. Instead, she leaned."

        $ enter_cinematic_mode()
        scene cg ch01_d2_dinner_reach
        with dissolve

        "The neckline shifted as she reached across the table."
        "Julian was in the same sightline, but Leia's eyes came straight back to mine."

        $ exit_cinematic_mode()
        scene bg ch01_d2_dinner
        with dissolve

        "I raised an eyebrow."
        "Leia gave me the smallest possible smile."

        maya "What?"
        mc "Nothing."
        gf "Nothing."

        $ set_story_value("ch01_d2_dinner_reach", "smiled_at_ryan")

    else:
        gf "Babe, can you pass that?"
        mc "This?"
        gf "Yeah, thanks."

        "I passed it across. Leia took it with an easy smile."

        $ set_story_value("ch01_d2_dinner_reach", "asked_ryan")

    $ set_story_flag("ch01_d2_scene_23_complete")
    jump ch01_day2_scene_24_dinner_aftermath


label ch01_day2_scene_24_dinner_aftermath:

    if get_story_value("ch01_d2_dinner_wink", False):
        "I did not confront Leia at the table."
        "Julian did not encourage the moment either. If anything, he became more careful about where he looked."
        "Leia never checked whether I had noticed."
    elif get_story_value("ch01_d2_dinner_reach") == "smiled_at_ryan":
        "Later Leia caught me looking again."
        "The satisfied little smile she gave me closed the loop without either of us saying a word."
    else:
        "Dinner stayed easy. Maya and Julian did most of the arguing while Leia and I enjoyed the show."

    "By the second round, everybody was noticeably looser."

    friend "I've got more back at the villa."
    maya "That sounds irresponsible."
    friend "You don't have to come."
    maya "I didn't say no."

    "Nobody suggested continuing the game at the restaurant. We paid, walked back together and let the night follow us home."

    $ set_story_flag("ch01_d2_scene_24_complete")
    jump ch01_day2_scene_25_maya_stays


label ch01_day2_scene_25_maya_stays:

    scene bg ch01_d2_game_night
    with fade

    "An hour later the coffee table was crowded with bottles, mixers, snacks and four glasses."
    "We had switched to water between drinks, but nobody was pretending the night was still sober."

    maya "We need a game."
    friend "No."
    maya "Never Have I Ever."
    friend "Even more no."
    gf "That means yes."

    maya "Normal rules. If you've done it, you drink."

    maya "Never have I ever missed a flight."
    "Julian drank immediately."
    maya "I knew it."
    friend "Private aviation has distorted your expectations of airports."
    maya "That sentence somehow made it worse."

    maya "Never have I ever stalked someone on social media before meeting them."
    "Maya drank."
    "Leia hesitated, then took a small drink too."
    gf "Research."
    mc "Due diligence?"
    gf "Exactly."

    maya "Never have I ever pretended to like food because someone else cooked it."
    "I drank. Leia stared at me."
    gf "Excuse me?"
    mc "This feels like a trap."
    gf "It is now."

    friend "Never have I ever lied about being busy because I didn't want to go somewhere."
    "Three glasses moved."
    maya "Julian."
    friend "I value honesty selectively."

    gf "Never have I ever had a holiday romance."
    "Maya drank."
    friend "That explains a lot."
    maya "It explains nothing."

    $ set_story_flag("ch01_d2_maya_stays_for_drinks")
    $ set_story_flag("ch01_d2_scene_25_complete")
    jump ch01_day2_scene_26_game_rules


label ch01_day2_scene_26_game_rules:

    "The harmless questions lasted long enough for everyone to get comfortable."

    maya "Okay. Dating questions."
    friend "There it is."
    maya "Never have I ever had a crush on someone I shouldn't have."

    "Maya drank without hesitation."
    "Julian studied his glass like it contained legal advice."

    maya "Never have I ever checked someone out while I was already in a relationship."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if d2_lane == "love":
        "Leia took a drink and looked at me sheepishly."
        gf "I'm not blind."
        mc "Devastating."
        gf "You'll recover."
    elif d2_lane == "exhibitionism":
        "Leia took a drink while looking straight at me."
        "After sunset, neither of us needed an explanation."
    else:
        "Leia took a drink."
        "She did not look at me."

    maya "Never have I ever enjoyed knowing someone was checking me out."

    "Maya drank."
    if d2_lane == "exhibitionism":
        "Leia drank too."
        "Her eyes flicked to mine over the rim."
    elif d2_lane == "ntr_risk" and (partner_stats["exhibitionism"] >= 18 or get_story_value("ch01_d2_ntr_soft_gate", False)):
        "Leia hesitated, then drank."
        "This time she kept her attention on the glass."
    else:
        "Leia left her drink on the table."

    maya "Never have I ever flirted just to see if I could."
    "Maya drank again."

    if get_story_value("ch01_d2_dinner_wink", False):
        "Leia's fingers rested against her glass, but she did not pick it up."
        "I noticed."
    elif d2_lane == "exhibitionism":
        "Leia looked at me, smiled, and took the smallest possible sip."
    else:
        "Leia shook her head."

    maya "These are getting boring."
    friend "That usually means you're about to make them worse."
    maya "Better."
    friend "Those are not synonyms."

    maya "New rule. Burning questions."
    maya "If you don't want to answer, and you don't want to drink, you lose something."

    friend "That is not how Never Have I Ever works."
    maya "It is now."

    gf "I'm in."
    mc "Fine."
    friend "I hate democracy."
    maya "Also yes."

    $ set_story_flag("ch01_d2_strip_penalty_agreed")
    $ set_story_flag("ch01_d2_scene_26_complete")
    jump ch01_day2_scene_27_game_escalates


label ch01_day2_scene_27_game_escalates:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    maya "Fine. Who here has found someone else in this room attractive?"

    "The room went quiet."
    "Leia stared at Maya."

    gf "That's not even Never Have I Ever."
    maya "Burning questions."
    gf "I'm not answering that."
    maya "Drink."
    gf "No."
    maya "Then you know the rule."

    "Leia looked down at herself, then stood."

    "She slipped out of her main dinner outfit and sat back down in her bra and panties, cheeks burning."

    if d2_lane == "exhibitionism":
        "Before sitting, she checked my face."
        "The embarrassment was real, but so was the little spark behind it."
    elif d2_soft_gate:
        "She did not ask whether I was okay with it."
        "She simply folded the dress beside her and sat down."
    else:
        "She immediately moved closer to me again once she sat."

    $ set_story_value("ch01_d2_nhie_leia_clothes", "bra_panties")

    friend "I cannot believe that worked."
    maya "Respect the rules."

    maya "Never have I ever hooked up with someone and forgotten their name."

    "Maya made a face."
    friend "Drink."
    maya "No."
    gf "Answer."
    maya "Also no."
    gf "Penalty."

    "Maya reached beneath her dress, wriggled for several seconds and pulled her panties free without removing the dress."

    friend "You somehow removed clothing and became no less dressed."
    maya "Skill."
    gf "Strategy."
    maya "Exactly."

    $ set_story_value("ch01_d2_nhie_maya_clothes", "dress_bra_no_panties")

    gf "Julian. Never have I ever been rejected after thinking I definitely had a chance."

    "Julian stared at her."

    friend "I'm not discussing this."
    maya "Then drink."
    friend "No."
    maya "Shirt."

    "He sighed, pulled his shirt over his head and threw it onto the arm of the sofa."

    $ set_story_value("ch01_d2_nhie_julian_clothes", "pants_underwear_shades")

    maya "Never have I ever deliberately worn something because I knew someone would look."

    "Maya drank."
    if d2_lane == "exhibitionism":
        "Leia drank too, looking at me."
    elif d2_soft_gate:
        "Leia took a slow drink without looking my way."
    else:
        "Leia considered it, then left her glass down."

    friend "Never have I ever done something sexual somewhere I could've been caught."

    if get_story_flag("ch01_d2_love_sunset_oral"):
        "Leia and I both drank."
        maya "Oh?"
        gf "Next question."
        maya "No, absolutely not. Explain."
        gf "I said next question."
    else:
        "Maya drank and refused to elaborate."

    maya "Never have I ever been turned on because someone was watching."

    "Maya drank casually."

    if d2_lane == "exhibitionism":
        "Leia looked at me, then drank."
        "We both knew exactly what she meant."
    elif d2_soft_gate and partner_stats["exhibitionism"] >= 18:
        "Leia drank after a pause."
        "She did not explain."
    else:
        "Leia did not move."

    maya "Okay. Leia."
    maya "Never have I ever enjoyed attention from someone I knew I probably shouldn't."

    "Leia's expression changed."

    if d2_lane == "love" and not d2_soft_gate:
        gf "No."
        maya "No?"
        gf "I'm answering this one. No."
        "She stayed in her bra and panties and reached for her water instead."
    else:
        gf "I'm not answering that."
        maya "Drink."
        gf "No."
        maya "Then..."

        "Leia exhaled and reached behind herself."

        if d2_lane == "exhibitionism":
            "She looked at me before unclasping her bra."
            "Once it came away, she immediately crossed both arms over her chest."
            "She was willing to participate. She was not yet comfortable simply sitting exposed in front of everyone."
        else:
            "She unclasped her bra without checking my reaction."
            "The moment it came away she crossed both arms tightly over her chest, still visibly self-conscious about being seen."

        $ set_story_value("ch01_d2_nhie_leia_clothes", "panties_covering_chest")
        $ set_story_flag("ch01_d2_nhie_leia_topless_covering")

    maya "Never have I ever sent someone a photo I regretted the next morning."

    "Maya's confidence disappeared for exactly one second."

    friend "Oh?"
    maya "No."
    friend "Drink."
    maya "Also no."

    "She reached beneath the dress again and removed her bra."

    friend "This is fraudulent."
    maya "Strategy."
    gf "You're still completely dressed."
    maya "I planned ahead."

    $ set_story_value("ch01_d2_nhie_maya_clothes", "dress_only")

    gf "Never have I ever hooked up with two people in the same twenty-four hours."

    "Maya froze."

    maya "Past Maya would like to invoke her right to silence."
    friend "Penalty."
    maya "Past Maya was an idiot."
    gf "You invented the stripping rule."
    maya "I know."

    "Maya looked down at the single dress she had left."

    maya "Fuck it."

    "She pulled it over her head and dropped back onto the sofa completely nude."

    maya "Happy?"
    friend "I have made a deliberate decision not to answer that."
    gf "Coward."

    $ set_story_value("ch01_d2_nhie_maya_clothes", "nude")
    $ set_story_flag("ch01_d2_nhie_maya_nude")

    $ set_story_flag("ch01_d2_scene_27_complete")
    jump ch01_day2_scene_28_julian_strips


label ch01_day2_scene_28_julian_strips:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    maya "Julian."
    maya "Never have I ever slept with someone I knew one of my friends liked."

    "Julian's joking expression flattened for a moment."

    friend "No."
    maya "No, you haven't?"
    friend "No, I'm not doing the follow-up."
    maya "Drink."
    friend "No."
    gf "Then pants."

    friend "This game is rigged."
    maya "Correct."

    "He stood, removed his trousers with considerably less dignity than he wanted, and sat back down in his underwear."

    $ enter_cinematic_mode()
    scene cg ch01_d2_julian_underwear_reveal
    with dissolve

    "For one beat the room became very quiet."

    if d2_lane == "love":
        "Leia looked because everyone looked, gave a surprised little laugh, then turned back toward me."
    elif d2_lane == "exhibitionism":
        "Leia looked."
        "Then she realised I had noticed her looking and met my eyes with a tiny, mischievous expression."
        "The moment came back to me instead of staying with Julian."
    elif d2_soft_gate:
        "Leia looked longer than she had on the other routes."
        "She did not immediately check whether I had noticed."

    $ exit_cinematic_mode()
    scene bg ch01_d2_game_night
    with dissolve

    maya "...Oh."
    friend "Don't."
    maya "I didn't say anything."
    friend "Your face did."

    $ set_story_value("ch01_d2_nhie_julian_clothes", "underwear_shades")
    $ set_story_flag("ch01_d2_julian_reveal_seen")

    "Maya recovered first."

    maya "Last one."
    maya "Never have I ever slept with someone whose name I didn't know."

    "Julian paused just slightly too long."

    maya "Oh my God."
    friend "What?"
    maya "Drink."
    friend "No."
    gf "Then answer."
    friend "Also no."
    maya "Then take something off."

    "Julian looked down at his underwear."
    "Then he reached up and removed his sunglasses."

    maya "No."
    maya "Absolutely not."
    friend "What?"
    maya "Those are not clothes!"
    friend "They were on my body."
    maya "That sounds like a rules problem."
    gf "He's technically got a point."
    maya "DO NOT ENABLE HIM."

    $ set_story_value("ch01_d2_nhie_julian_clothes", "underwear_no_shades")
    $ set_story_flag("ch01_d2_julian_shades_removed")

    "That killed the game more effectively than any official ending could have."

    $ set_story_flag("ch01_d2_scene_28_complete")
    jump ch01_day2_scene_29_game_winds_down


label ch01_day2_scene_29_game_winds_down:

    scene bg ch01_d2_game_night
    with dissolve

    maya "I'm done. This game is corrupt."
    friend "You made the rules."
    maya "Then the administration is corrupt."

    "Maya tried to stand, reconsidered halfway up and sat back down."

    gf "Yeah. You're not going home like this."
    maya "I'm perfectly capable of—"

    "She tried again."
    "Leia caught her arm before gravity could make the argument for her."

    gf "You're staying here."
    maya "Fine. Couch."

    friend "Take my room."
    maya "No, it's fine. I'll take the couch."
    friend "You're not sleeping on the couch."
    maya "Then where are you sleeping?"
    friend "The couch."
    maya "No."
    friend "Maya, take the room."
    maya "I'm not kicking you out of your own bed."
    friend "You're not. I'm offering."
    maya "Still no."
    friend "Seriously. Take it. I'll sleep out here."

    "Maya studied him with the concentration of someone solving a very difficult problem while very drunk."

    maya "Okay."

    "She pointed at him."

    maya "But you're sleeping with me then."

    "The room stopped."

    friend "...What?"

    "Maya grinned."

    maya "You're a rich boy, Julian. I'm not letting you pretend you know how to sleep on a couch."
    friend "I know how a couch works."
    maya "Do you?"
    friend "I've used one before."
    maya "For sleeping?"

    "Julian paused."

    maya "Exactly."

    "His expression softened from joking to careful."

    friend "You're sure?"
    maya "Julian."
    friend "I'm asking."
    maya "I told Leia I would."
    maya "Yes. Come on."

    "Maya scooped her dress off the floor, caught Julian by the wrist and started pulling him toward the corridor."

    maya "And bring water."
    friend "Romantic."
    maya "Don't make it weird."

    "Julian grabbed two bottles of water with his free hand and let her drag him away."
    "They disappeared into his room together."
    "Nothing about the exchange suggested an agreement beyond sharing the bed; Maya had been the one to invite him after he offered to sleep elsewhere."

    $ set_story_value("ch01_d2_maya_sleeping", "julian_room_shared_bed")
    $ set_story_value("ch01_d2_julian_sleeping", "julian_room_shared_bed")
    $ set_story_flag("ch01_d2_maya_julian_share_room")

    "The bedroom door closed somewhere down the corridor."
    "For the first time since we'd come back from dinner, the villa was quiet."

    "Just me and Leia."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if d2_lane == "love":
        "Leia found her dress, looked at it, then decided putting it back on for the walk upstairs was unnecessary."
        "She stayed in her bra and panties and came over to me."
    else:
        "Leia was still in her panties, both arms folded across her bare chest."
        "Even after the game ended she was not yet comfortable simply standing uncovered in the room."

    gf "Well."
    mc "Well."
    gf "That got out of hand."
    mc "Maya's naked."
    gf "Julian took off his sunglasses."
    mc "Honestly, that was more shocking."

    "Leia laughed, tired and tipsy."

    $ set_story_flag("ch01_d2_scene_29_complete")
    jump ch01_day2_scene_30_bedroom


label ch01_day2_scene_30_bedroom:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)
    $ d2_wink = get_story_value("ch01_d2_dinner_wink", False)
    $ d2_pool_suspicion = get_story_flag("ch01_d2_pool_suspicion")
    python:
        d2_love_exhib_blend = (
            d2_lane == "love"
            and partner_stats["exhibitionism"] >= 20
            and player_stats["acceptance"] >= 15
            and choice_tag_count("open", ch01_d2_choice_ids()) >= 1
        )

    scene bg ch01_villa_bedroom_night
    with fade

    "Upstairs, we drank water and took a few quiet minutes to let the alcohol and noise settle."
    "Neither of us was stumbling or confused by the time we got into bed."

    if d2_soft_gate and d2_wink:
        jump ch01_day2_scene_30_ntr_nightmare

    elif d2_pool_suspicion and not d2_soft_gate and d2_lane == "ntr_risk":
        "Leia sat on the edge of the bed and looked at me."

        gf "You're doing it again."
        mc "Doing what?"
        gf "Thinking loudly."

        $ d2_bed_love_text = format_choice("ch01_d2_bed_pool_love", "I didn't like seeing it, but I believe you.")
        $ d2_bed_ex_text = format_choice("ch01_d2_bed_pool_exhibition", "It bothered me... and I haven't stopped thinking about it.")
        $ d2_bed_accuse_text = format_choice("ch01_d2_bed_pool_accuse", "I still think it looked convenient.")

        menu:
            "[d2_bed_love_text]":
                $ apply_choice("ch01_d2_bed_pool_love")
                mc "I didn't like seeing it, but I believe you."
                gf "Nothing happened."
                mc "I know."
                "Her shoulders finally relaxed."
                $ set_story_value("ch01_d2_route_lane_dinner", "love")
                $ d2_lane = "love"
                jump ch01_day2_scene_30_love

            "[d2_bed_ex_text]":
                $ apply_choice("ch01_d2_bed_pool_exhibition")
                mc "It bothered me... and I haven't stopped thinking about it."
                gf "Because you were jealous?"
                mc "Partly."
                gf "And the other part?"
                mc "Complicated."
                "Understanding slowly reached her expression."
                gf "Oh."
                $ set_story_value("ch01_d2_route_lane_dinner", "exhibitionism")
                $ d2_lane = "exhibitionism"
                jump ch01_day2_scene_30_exhibition

            "[d2_bed_accuse_text]":
                $ apply_choice("ch01_d2_bed_pool_accuse")
                mc "I still think it looked convenient."
                gf "Then I don't know what else you want me to say."
                "We went to bed without resolving it."
                $ set_story_value("ch01_d2_end_route", "mixed_unresolved")
                # No bedroom payoff scene plays here (generic bedroom approach, then the
                # unresolved pool-suspicion exchange), so record that as the variant.
                $ set_story_value("ch01_d2_bedroom_variant", "pool_suspicion_unresolved")
                jump ch01_day2_scene_30_finish

    elif d2_lane == "exhibitionism" or d2_love_exhib_blend:
        jump ch01_day2_scene_30_exhibition

    else:
        jump ch01_day2_scene_30_love


label ch01_day2_scene_30_love:

    "Leia crossed to the window and pulled the curtains shut."

    gf "There."
    mc "You know those don't hide much."
    gf "They hide enough."
    mc "That's not what you said yesterday."
    gf "Shut up."

    "The thin fabric still let light and shapes through, but Leia had made the choice she wanted: tonight was private."

    gf "Come here."

    $ enter_cinematic_mode()
    scene cg ch01_d2_love_bedroom_01
    with dissolve

    "She pulled me onto the bed with her."
    "After the reckless little moment outside at sunset, this was slower and familiar: kisses, laughter, hands that already knew where they belonged."

    scene cg ch01_d2_love_bedroom_02
    with dissolve

    "We had sex with the curtains drawn, the rest of the villa reduced to distant sounds beyond the room."
    "Nothing about it needed an audience."

    $ exit_cinematic_mode()
    scene bg ch01_villa_bedroom_night
    with dissolve

    "Afterward Leia curled against me."

    gf "Today was a good day."
    mc "Yeah."
    gf "Even the bee?"
    mc "Especially the bee."
    gf "Idiot."

    $ set_story_value("ch01_d2_bedroom_variant", "love_private")
    $ set_story_value("ch01_d2_end_route", "love")
    jump ch01_day2_scene_30_finish


label ch01_day2_scene_30_exhibition:

    "Leia looked toward the glass wall."

    mc "Curtains?"

    "She followed my eyes to them."
    "For a second I expected her to close them."

    gf "Leave them."

    "The answer came with a blush, but it came."

    mc "You sure?"
    gf "Yes."

    $ enter_cinematic_mode()
    scene cg ch01_d2_exhib_bed_open_01
    with dissolve

    "We stayed on the bed. The window remained open to the dark pool and walkway beyond."
    "Nobody was actually standing outside. That was not the point."

    gf "You're staring."
    mc "You spent half the night making that difficult not to do."
    gf "Did you like it?"
    mc "Which part?"
    gf "You know which part."
    mc "Watching you take your clothes off in front of everyone?"
    "Leia's face heated again."
    gf "...Yeah."
    mc "Yeah."
    gf "I liked knowing you were watching too."

    scene cg ch01_d2_exhib_bed_open_02
    with dissolve

    "As we started having sex, Leia looked toward the uncovered window again."

    gf "What if someone walked past?"
    mc "Nobody's there."
    gf "I know."

    "She looked back at me."

    gf "Pretend."

    scene cg ch01_d2_exhib_bed_open_03
    with dissolve

    mc "Someone stopped outside."
    "Leia's eyes flicked toward the glass."
    mc "They can see the bed."
    "She instinctively drew one arm across her chest for a moment, the same reflex she'd had downstairs, then let it fall when she remembered this was only us."

    gf "Don't stop."

    "The fantasy was not that I disappeared from the scene."
    "It was that somebody else might see what Leia and I were choosing together."

    scene cg ch01_d2_exhib_bed_open_04
    with dissolve

    mc "They're still watching."
    "Leia hid her face against my shoulder, laughing once from embarrassment before looking back toward the window."

    gf "Ryan..."
    mc "Want me to stop?"
    gf "No."

    "We finished the game we had started, safely inside the room and fully aware that the imagined audience was only part of the roleplay."

    $ exit_cinematic_mode()
    scene bg ch01_villa_bedroom_night
    with dissolve

    "A few minutes later Leia looked at the still-open curtains."

    gf "Close them now."
    mc "Now?"
    gf "Ryan."

    "I laughed and pulled them across."

    gf "Still think I'm secretly an exhibitionist?"
    mc "Secretly?"
    gf "Shut up."

    if d2_love_exhib_blend:
        $ set_story_value("ch01_d2_bedroom_variant", "love_exhib_open_curtains")
        $ set_story_value("ch01_d2_end_route", "love")
    else:
        $ set_story_value("ch01_d2_bedroom_variant", "exhibition_open_curtains")
        $ set_story_value("ch01_d2_end_route", "exhibitionism")

    $ set_story_flag("ch01_d2_exhibition_bedroom_open_curtains")
    jump ch01_day2_scene_30_finish


label ch01_day2_scene_30_ntr_nightmare:

    "Leia gathered her things without looking at me for long."

    gf "I'm exhausted."
    mc "Yeah."
    gf "I'm going to bed."

    "There was something I could have said."
    "I let the moment pass."

    "Leia fell asleep quickly."
    "I didn't."

    scene black
    with fade

    "The day replayed itself behind my eyes."
    "Not accurately."

    $ enter_cinematic_mode()
    scene cg ch01_d2_ntr_dream_strangers
    with dissolve

    "The strangers were back at the pool."
    "Only this time Leia wasn't embarrassed."
    "In the dream she turned toward them and deliberately squeezed her breasts together for their attention, smiling as if she had been waiting for them to notice."

    mc "Leia."

    "She didn't hear me."

    scene cg ch01_d2_ntr_dream_julian_pool
    with dissolve

    "The scene changed."
    "Julian stood behind her in the pool."
    "Instead of looking away like he really had, he reached around and grabbed both of her breasts."
    "Dream-Leia leaned back into him."

    mc "Leia."

    "Still nothing."

    scene cg ch01_d2_ntr_dream_nhie
    with dissolve

    "The living room returned."
    "Reality had been Leia in panties, arms crossed tightly over her chest."
    "The nightmare stripped away even that boundary."
    "She sat completely nude in front of everyone, openly enjoying the attention and touching herself while I watched from somewhere nobody else seemed able to see."

    "She looked completely comfortable."
    "That was how I knew it wasn't her."

    scene cg ch01_d2_ntr_dream_wrong_room
    with dissolve

    "Then the end of the night replayed."

    "Maya should have taken Julian's hand."
    "Instead, Leia did."

    "She pulled him down the corridor."
    "I tried to follow."

    mc "Leia!"

    "Neither of them turned around."

    "The bedroom door closed."

    $ exit_cinematic_mode()
    scene black
    with hpunch
    pause 0.3

    scene bg ch01_villa_bedroom_night
    with fade

    "I woke hard enough to pull the sheet with me."

    "Leia was beside me."
    "The real Leia."
    "Asleep in our bed."

    "She stirred when I moved."

    gf "Ryan...?"
    "Her eyes barely opened."
    gf "You okay?"

    $ d2_wink_repair_text = format_choice("ch01_d2_wink_repair", "No. Tell her the truth.")
    $ d2_wink_accuse_text = format_day2_risk_choice("ch01_d2_wink_accuse_hard", "Ask what she really wants from Julian.", severity="hard")
    $ d2_wink_reject_text = format_day2_risk_choice("ch01_d2_wink_reject_hard", "I'm fine.", severity="hard")

    menu:
        "[d2_wink_repair_text]":
            $ apply_choice("ch01_d2_wink_repair")

            mc "No."

            "Leia woke properly."

            mc "I've been jealous all day."
            mc "The pool. Dinner. The game."
            mc "And instead of talking to you, I kept shutting you out."

            gf "Ryan..."
            mc "I saw you wink at Julian."

            "Leia went quiet."

            gf "I did."
            mc "Why?"

            "She stared at the ceiling for a few seconds."

            gf "I don't know."
            "Then she corrected herself."
            gf "No. That's not true."
            gf "Maybe because I was angry."
            gf "Maybe because I stopped thinking you'd care."

            mc "I cared."
            gf "You had a strange way of showing it."

            "That one landed because she was right."

            mc "It crossed a line for me."
            gf "I know."
            gf "It was stupid. I shouldn't have done it."
            mc "And I shouldn't have spent the whole day making you guess whether I even wanted to be around you."

            "Leia reached for my hand."

            gf "Then next time, talk to me."
            mc "You too."
            gf "Deal."

            "Nothing about the conversation erased the day."
            "It did put us back on the same side of it."

            $ set_story_value("ch01_d2_ntr_soft_gate_repaired", True)
            $ set_story_value("ch01_d2_end_route", "love_repaired")
            $ set_story_value("ch01_d2_bedroom_variant", "ntr_gate_repaired")

        "[d2_wink_accuse_text]":
            $ apply_choice("ch01_d2_wink_accuse_hard")
            $ set_story_value("ch01_d2_ntr_confirmed", True)
            $ set_story_value("ch01_d2_end_route", "ntr_confirmed")
            $ set_story_value("ch01_d2_bedroom_variant", "ntr_gate_accusation")

            mc "What do you actually want from Julian?"

            "Leia stared at me, suddenly awake."

            gf "What?"
            mc "The wink. The pool. Tonight."
            gf "Nothing happened at the pool."
            mc "That's not what I asked."
            gf "Then what are you asking?"
            mc "How long have you wanted his attention?"

            "Her expression hardened."

            gf "You've barely spoken to me properly all day."
            mc "So that makes the wink okay?"
            gf "I didn't say that."
            mc "Then what are you saying?"

            "Leia looked away."

            gf "I'm saying I'm tired of trying to guess whether you even want me here."

            "Neither of us repaired it."
            "We turned away from each other."

        "[d2_wink_reject_text]":
            $ apply_choice("ch01_d2_wink_reject_hard")
            $ set_story_value("ch01_d2_ntr_confirmed", True)
            $ set_story_value("ch01_d2_end_route", "ntr_confirmed")
            $ set_story_value("ch01_d2_bedroom_variant", "ntr_gate_withdrawal")

            mc "I'm fine."

            "Leia watched me for a few seconds."
            "It was the same answer I had given her all day."

            gf "...Okay."

            "This time she did not push."
            "She rolled onto her side."
            "I turned the other way."

    if get_story_value("ch01_d2_ntr_confirmed", False):
        if current_choice_mode() == "developer":
            centered "NTR ROUTE CONFIRMED — ch01_d2_ntr_confirmed = True"
        elif current_choice_mode() == "full":
            centered "NTR route confirmed."
        elif current_choice_mode() == "insight":
            centered "A major route boundary has been crossed."
        else:
            centered "Something changed tonight."

    jump ch01_day2_scene_30_finish


label ch01_day2_scene_30_finish:

    $ set_story_flag("ch01_d2_scene_30_complete")
    $ set_story_flag("ch01_day_02_complete")

    scene black
    with fade

    call lc_day_review("ch01_d2") from lc_review_return_ch01_d2

    # Day Two -> Day Three: same pattern as Day One -> Day Two (card, then jump).
    # ch01_d2_end_route and the rest of the stored Day Two state carry over untouched.
    jump ch01_day3_start

