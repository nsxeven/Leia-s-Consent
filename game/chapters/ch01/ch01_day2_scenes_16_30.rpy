# Leia's Consent — Chapter One: Something Different
# Day Two, Scenes 16–30.

label ch01_day2_scene_16_forced_split:

    $ d2_lane = get_story_value("ch01_d2_route_lane_pre_split", "love")

    "Eventually all four of us climbed out together and collapsed around the poolside table."
    "[friend_name] handed out what was left in the cooler, and Maya had hers raised before he'd even sat down."

    maya "Wait, toast. To unexpected shopping trips."
    gf "Absolutely not, I'm not toasting that. My feet still hurt from that shopping trip."
    friend "To my new shirt, then. It's a good shirt. Nobody's said one nice thing about it all day."
    maya "Because it's worse! That's so much worse than the shopping."
    mc "To surviving day two? Most of it, anyway."
    gf "Yes. That one. To surviving."

    "Four glasses met in the middle."

    "A little farther down the pool deck, a couple of guys had been glancing our way often enough for Maya to notice."
    maya "Don't look now, but—"
    "[girlfriend_name] looked immediately."
    maya "Every single time! Why does nobody ever just not look?"
    gf "Because you say it like that! You say it like there's a celebrity behind me."
    "One of the men looked away, not quite fast enough."
    gf "Maybe he's looking at you. You're the one in the, like, the strappy thing."
    maya "Babe. He has two eyes, and neither of them is on me."

    if d2_lane == "ntr_risk":
        "[girlfriend_name] looked toward me first."
        "I was distracted, only half following whatever [friend_name] had just said."
        "She waited a second for me to look up. I didn't."
        "Then she turned back toward the strangers."
        "[girlfriend_name] raised both arms over her head in a slow stretch, extending through her shoulders and back before letting them fall again."
        "The same man kept looking."
        "Maya noticed. I didn't."
        $ set_story_value("ch01_d2_pool_attention", "leia_stretched_without_ryan")

    else:
        "[girlfriend_name] looked from the strangers to me, then crossed the few steps between us."
        "Without saying anything, she leaned in and kissed me."
        "I kissed her back and let one hand settle firmly on her ass."
        "[girlfriend_name] made a small surprised sound against my mouth."
        "When we separated, Maya was staring at us. [friend_name] had suddenly become very interested in his drink. The strangers had seen everything."

        if d2_lane == "exhibitionism":
            "[girlfriend_name]'s face warmed, but she glanced toward the strangers once more before looking back at me."
            maya "Hi, sorry, we're all still here. Just so you know. All of us."
            gf "Nobody asked you to watch, Maya."
            maya "You did it right in front of me! Where was I supposed to look, at [friend_name]?"
            $ set_story_value("ch01_d2_pool_attention", "couple_display_open")
        else:
            "[girlfriend_name]'s face went pink the moment she remembered we had an audience."
            mc "Not that I'm complaining, but... what was that for?"
            gf "Do I need a reason? I wanted to. Also they were staring and it was getting weird."
            "She stayed close anyway."
            $ set_story_value("ch01_d2_pool_attention", "couple_display_love")

    "[friend_name] reached for the cooler again, found it empty and stared into it as if more drinks might appear."
    friend "So, bad news. We're out. Completely out. I'm looking at the bottom of the cooler right now."
    maya "Already? There were like twelve in there."
    friend "There were nine, and I had two, so I'm not taking the blame for this one."

    if d2_lane == "ntr_risk":
        maya "[player_name], come help me carry. Four drinks."
        mc "You need help carrying four drinks?"
        maya "Yes. Big drinks. Up you get."

        "[girlfriend_name] stayed beside [friend_name] while Maya led me back toward the villa."
        "Once the pool was out of earshot, I looked at her."
        mc "This isn't about drinks, is it?"
        maya "Nope. Well, a bit. We do actually need drinks."
        maya "But what's going on with you today? And don't say nothing, I've known you way too long for nothing."
        mc "What do you mean? I'm just... I'm here. I'm hanging out."
        maya "[girlfriend_name] keeps checking whether you're still in the room. You're standing right next to her, and she keeps checking."
        think "Was she? I hadn't noticed. That was probably the problem."

        "Back at the pool, [friend_name] glanced toward the path we'd disappeared down."
        friend "That was not about drinks. Nobody needs help carrying four drinks."
        gf "Nope. Not even a little bit."
        friend "She does this, apparently. I met her today, and I already know she does this."
        gf "What, kidnaps people's boyfriends?"
        friend "Interrogates them. She asked me about my sunglasses for ten minutes. Where I got them, why, whether I sleep in them."
        "[girlfriend_name] laughed despite herself."
        gf "Does he always get this quiet when he's stuck in his own head?"
        friend "Sometimes, yeah. Since college. He goes quiet, and then a couple of days later he tells you what it was, like it's no big deal."
        "[friend_name] didn't dress it up or use it against me. He'd just known me longer than she had."

        $ set_story_value("ch01_d2_split", "ryan_maya_leia_julian")

    elif d2_lane == "exhibitionism":
        friend "I'll get them. There's a second fridge in the pantry nobody else has found yet."
        mc "I'll come. I want to see this secret fridge."
        "[friend_name] and I headed toward the villa while [girlfriend_name] and Maya stayed beside the pool."

        "Maya waited until we were far enough away, then looked at [girlfriend_name]."
        maya "Okay, wait, I have to ask. Are you two, like... experimenting? Is that what this is?"
        gf "What? What makes you say that?"
        maya "You just kissed him in front of everybody and let him grab your ass while those guys were staring."
        "[girlfriend_name]'s face warmed again."
        gf "Maybe? A little. It's new. We're kind of... seeing what we like."
        maya "Seriously? Oh my God. I love that."
        gf "Don't make it a whole thing. We're figuring it out."
        maya "I'm not making it a thing! I'm asking. How far does figuring it out go?"
        gf "Maya."
        maya "For science. You can totally tell me to shut up."
        "[girlfriend_name] laughed, embarrassed, and glanced toward the strangers."
        maya "So... want to give them something to look at? Only if you want to. I'm serious."
        "[girlfriend_name] looked toward the villa where [player_name] had gone, then back at Maya."
        gf "...Okay. A little. Just a little bit."
        "She hooked her fingers under the side strings of her bikini bottoms and pulled them a little higher over her hips."
        "The stranger noticed immediately."
        gf "Oh my God, he's actually looking. Maya, he's looking, he's actually—"
        maya "Of course he's looking. Have you seen you?"
        maya "One more thing. Ready?"
        gf "For wha—"
        "Maya gave her a quick playful spank."
        gf "Maya!"
        "Maya burst out laughing. [girlfriend_name] was bright red, but laughing too."
        "The strangers had seen it."
        $ set_story_value("ch01_d2_split", "ryan_julian_leia_maya")
        $ set_story_flag("ch01_d2_exhibition_pool_tease")

    else:
        maya "We'll go. [friend_name], you're carrying. Come on, up."
        friend "Why am I always the one carrying? I'm coming, I'm coming."
        "Maya caught [friend_name] by the arm and steered him toward the villa, leaving [girlfriend_name] and me beside the pool."
        "[girlfriend_name] watched them disappear, then leaned against me."
        gf "I really like her. Like, I didn't expect to like her this much."
        mc "Yesterday you had about eleven questions about her."
        gf "That was due diligence. That's different. I was being thorough."
        mc "I'm just saying. Eleven questions."
        "She kissed my shoulder, still visibly embarrassed whenever she remembered the audience farther down the deck."
        $ set_story_value("ch01_d2_split", "ryan_leia_julian_maya")

    $ set_story_flag("ch01_d2_scene_16_complete")
    jump ch01_day2_scene_17_pool_return


label ch01_day2_scene_17_pool_return:

    scene bg ch01_pool_day
    with dissolve

    $ d2_split = get_story_value("ch01_d2_split")

    if d2_split == "ryan_maya_leia_julian":
        "Back at the pool, [friend_name]'s attention snapped toward something buzzing near the loungers."
        friend "No. No no no."
        gf "What? What is it?"
        "He was already backing away."
        friend "Bee. Bee. There's a bee."
        gf "Where? I don't see a— oh."
        "The bee drifted toward him."
        friend "NOPE. Nope, I'm out, I'm sorry—"
        "[friend_name] jumped straight into the pool."
        gf "You just left me?!"
        "Then the bee changed direction."
        gf "Oh, come on, why me?!"
        "[girlfriend_name] jumped in after him."

        "For several seconds neither of them cared about anything except finding the bee."
        gf "Where is it?!"
        friend "I don't know, I had my eyes closed."
        gf "Why would you close your eyes?!"
        friend "Because if I can't see it, it isn't happening. That's how it works."
        gf "It's one bee, [friend_name]!"
        friend "Then why did YOU jump in?"

        "[friend_name] looked back at her."
        "His expression changed."
        "He immediately looked away."

        gf "...What?"
        friend "Uh. Okay. So."
        gf "What? Why are you looking at the sky?"
        friend "[girlfriend_name], I need you to not freak out."
        gf "Why would I freak out? What?!"
        friend "Your... top."

        "[girlfriend_name] froze."
        "She looked down."

        gf "OH MY GOD!"

        "[girlfriend_name] folded her arms across herself, then instinctively rushed behind [friend_name] and clung to his back, using him to shield herself from the people on the deck."
        "[friend_name] went rigid with surprise, keeping his hands clear and his eyes turned away."
        gf "Don't look!"
        friend "I'm not! I'm looking at the— there's a tree. I'm looking at the tree."
        gf "Where's my top?! Can you see it?"
        friend "Stay behind me. I'll find it."

        "[friend_name] spotted the bikini top floating several feet away."
        friend "It's over there. By the steps."
        gf "GET IT!"
        friend "Why me?! I can't look at anything!"
        gf "[friend_name!u]!"

        "[girlfriend_name] stayed tucked behind [friend_name] as he edged toward the floating top, still holding on to his shoulders."
        "Over his shoulder, she caught sight of the strangers on the deck."
        "They were staring."
        gf "Oh my God. Oh no."
        friend "What? What now? Is it the bee?"
        gf "No, the guys. They saw. They definitely saw."
        friend "Then don't look at them. That's what I'm doing. It's working great."
        gf "I already looked!"

        "Maya and I rounded the corner carrying the drinks."
        "Then I stopped."

        $ enter_cinematic_mode()
        scene cg ch01_d2_pool_top_accident
        with dissolve

        "[girlfriend_name] was clinging to [friend_name]'s back in the pool, hiding behind his shoulders while he kept his hands away from her."
        "Her bikini top floated several feet away. The strangers from earlier were still watching."
        "I had arrived at the exact moment that explained the least."

        $ exit_cinematic_mode()
        scene bg ch01_pool_day
        with dissolve

        "[girlfriend_name] saw me over [friend_name]'s shoulder. Her eyes widened."
        "She let go of him at once, sinking lower into the water and covering herself with her arms."
        gf "[player_name]—"
        maya "...What the hell happened? We were gone five minutes."
        gf "There was a bee and [friend_name] jumped in and then it came at me so I jumped in and I didn't know my top came off—"
        friend "There was a bee."
        "Maya looked at [friend_name]."
        maya "Of course there was. Of course it was a bee."

        "[girlfriend_name] looked directly at me after the explanation, still mortified and waiting for my reaction."
        "[friend_name] reached the top without turning back toward her."
        friend "Got it. I've got it. I'm not looking."
        "He pushed it across the water. [girlfriend_name] caught it awkwardly with one hand while keeping herself covered with the other."

        $ set_story_flag("ch01_d2_pool_suspicion")
        $ set_story_value("ch01_d2_pool_incident", "leia_julian_bee_top_off")

    elif d2_split == "ryan_julian_leia_maya":
        "Maya was still laughing about the strangers when a bee drifted toward the loungers."
        maya "Wait. Wait, don't move."
        gf "You're not doing the 'don't look now' thing again."
        maya "No, I'm serious. Bee."
        gf "What? Where?"

        "The bee moved closer. Both women backed toward the pool."
        gf "Nope. Nope, nope."
        "[girlfriend_name] jumped. Maya went in with her."

        "[girlfriend_name] surfaced, pushing wet hair from her face."
        maya "Babe. [girlfriend_name]. Don't panic."
        gf "Why would I panic? What?"
        "Maya pointed toward the bikini top floating away from them."
        "[girlfriend_name] looked down and folded her arms across herself."
        gf "...Oh my God."
        "She darted behind Maya and clung to her back, using her friend as a shield from the strangers on the deck."
        "Maya steadied herself, startled, then turned her attention toward the floating top."
        maya "I've got you. Stay behind me."
        "The strangers they had been teasing moments earlier were still watching."

        "[friend_name] and I returned with the drinks to find [girlfriend_name] still hiding against Maya's back while Maya tried to reach the floating top."
        "[girlfriend_name] saw us, let go of Maya, and sank lower into the water with her arms across herself."
        maya "So. There was a bee."
        gf "Don't. Don't tell it like that."
        maya "I'm explaining! It's a very short story!"
        "There was no mystery about what had happened. Maya had seen the whole thing."
        $ set_story_value("ch01_d2_pool_incident", "leia_maya_bee_top_off")

    else:
        "[girlfriend_name] and I were still beside the pool when a bee wandered too close to the loungers."
        gf "[player_name]. Babe. There's a bee."
        mc "Just don't move."
        gf "Why does 'don't move' always sound worse than the actual bee?"

        "It drifted closer."
        "[girlfriend_name] grabbed my arm, then dodged behind me when it changed direction."
        mc "[girlfriend_name], wait—"
        gf "NOPE."

        "She jumped into the pool."
        "I grabbed for her hand, missed, and went in after her."

        "[girlfriend_name] surfaced and looked around for the bee."
        "Her bikini top surfaced several feet away."
        "The strangers saw it at the same time I did."

        mc "Babe. Um. Babe."
        gf "What? Is it in here? Is it on me?"
        "I pointed."
        "[girlfriend_name] looked down, gasped and covered herself."
        gf "Oh my God. Oh my God, [player_name]."
        "Before I could say anything, she darted behind me and clung to my back, using me to block the strangers' view."
        mc "I've got you. Stay behind me."
        "I kept myself between her and the deck as I moved toward the floating top."
        "She let go just long enough for me to retrieve it."
        "By the time Maya and [friend_name] returned with the drinks, I was handing it back to her."
        maya "Wait, what happened? Why is everyone wet?"
        gf "Bee. Don't ask."
        friend "Where? Where's the bee?"
        "[friend_name] stopped dead and scanned the pool deck."
        maya "Relax, it's gone. It's long gone."
        friend "You don't know that. Nobody knows that. They come back."
        $ set_story_value("ch01_d2_pool_incident", "leia_ryan_bee_top_off")

    $ set_story_flag("ch01_d2_scene_17_complete")
    jump ch01_day2_scene_18_pool_aftermath


label ch01_day2_scene_18_pool_aftermath:

    if get_story_value("ch01_d2_pool_incident") == "leia_julian_bee_top_off":
        "Once [girlfriend_name] had retied her top and climbed out, she came straight to me."
        "The embarrassment still hadn't left her face."

        gf "You're being quiet. You're doing the quiet thing."

        $ d2_pool_reassure_text = format_choice("ch01_d2_pool_reassure", "I believe you. It just looked insane for a second.")
        $ d2_pool_honest_text = format_choice("ch01_d2_pool_honest_jealous", "I believe you. I still didn't like walking in on it.")
        $ d2_pool_accuse_text = format_choice("ch01_d2_pool_accuse", "I don't know. It just looked... convenient.")

        menu:
            "[d2_pool_reassure_text]":
                $ apply_choice("ch01_d2_pool_reassure")
                $ set_story_value("ch01_d2_pool_response", "reassured")
                mc "I believe you. It just looked insane for a second."
                "[girlfriend_name]'s shoulders relaxed."
                gf "It felt insane! I was hiding behind [friend_name], babe. [friend_name]. Out of everyone."
                mc "Who jumped in first and left you with the bee."
                friend "In my defense, the bee had a plan, and I didn't. I just reacted."

            "[d2_pool_honest_text]":
                $ apply_choice("ch01_d2_pool_honest_jealous")
                $ set_story_value("ch01_d2_pool_response", "honest_jealous")
                mc "I believe you. I still didn't like walking in on it."
                gf "That's... yeah. I wouldn't have liked it either."
                mc "I'm not blaming you. I just— I'm saying it now so I'm not weird about it later."
                gf "I know. Thank you for saying it."
                "She squeezed my hand once before letting go."

            "[d2_pool_accuse_text]":
                $ apply_choice("ch01_d2_pool_accuse")
                $ set_story_value("ch01_d2_pool_response", "accused")
                mc "I don't know. It just looked... convenient."
                "[girlfriend_name] stared at me."
                gf "Are you serious right now?"
                mc "No, I— I don't know. I'm saying what it looked like."
                gf "And I'm telling you what happened. There was a bee. I was there."
                "She stepped away before the conversation could turn into something larger in front of everyone."

    elif get_story_value("ch01_d2_pool_incident") == "leia_maya_bee_top_off":
        "Maya eventually retrieved [girlfriend_name]'s top and passed it back under the water."
        "[girlfriend_name] retied it beneath the surface before climbing out, still visibly red from what had happened."
        "Her eyes flicked toward the strangers. They were still there."
        "Then she came straight to me."

        gf "So."
        mc "So?"
        gf "That went way further than I meant it to."
        mc "The bee?"
        "[girlfriend_name] gave me a look."
        gf "Everything. The whole afternoon."

        "She lowered her voice."
        gf "The strings thing was on purpose. Like, I want you to know that part was me."
        gf "Maya was being Maya, and she asked, and I said yes, and I knew they were looking the whole time."
        "She glanced toward the strangers again, then back at me."
        gf "But that? The top?"
        gf "That was so not on purpose. I need you to know that."

        mc "I know. I know it wasn't."
        "Some of the tension left her shoulders."

        gf "You saw them looking before you left."
        mc "Yeah. Kind of hard to miss."
        gf "And you were okay with... us playing with it?"
        mc "With what we were doing together? Yeah."

        "[girlfriend_name]'s embarrassment didn't disappear, but the small smile that followed belonged to me."
        gf "Okay. Good."
        gf "Because I think I liked that part."
        "She immediately covered her face for half a second."
        gf "Not the losing-my-top part."
        mc "Right. Not that part."
        gf "Very much not that part. That part can go in the trash forever."

        "Maya called something unhelpful from the pool. [girlfriend_name] ignored her and stayed beside me."
        "It had gone further than she meant it to, and she'd still come straight back to me with it."
        $ set_story_flag("ch01_d2_exhibition_pool_shared_with_ryan")
    else:
        "Once [girlfriend_name] had retied her top, she stayed close enough that our shoulders kept touching."
        "The strangers had seen more than either of us intended. There was no ambiguity about how it happened."
        "Maya spent the next five minutes trying to convince [friend_name] that the bee had already left."
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

    maya "I actually have to go home if I'm going to look like a person tonight. I have pool hair. This is pool hair."
    friend "You look fine. I mean, you look good. You look like you, which is— yeah. Fine."
    maya "That's because you're looking at me through sunglasses. Everything looks fine through those."
    gf "You're coming back for dinner, right?"
    maya "Obviously. Somebody has to supervise."

    "[girlfriend_name] walked Maya toward the villa entrance."
    maya "Text me if these two somehow manage to ruin the evening before I get back."
    gf "Which two?"
    maya "Yes. Both of them. Bye, babe."

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
        "[girlfriend_name] leaned against the railing beside me, then glanced toward the upper floor."
        gf "Is [friend_name] still inside getting ready?"
        mc "Yeah, I think so. He said something about reservations."
        gf "And he can't see this side of the pool from his room?"
        mc "Not unless he's hanging out of the window."
        gf "Good. Okay. Good."

        "She took my hand and pulled me toward the sheltered side of the pool, out of the sightline from [friend_name]'s room."
        mc "Wait, what are you doing?"
        gf "Something private. Shh."
        mc "We're outside, babe."
        gf "Private enough. I checked. I checked twice."

        $ enter_cinematic_mode()
        scene cg ch01_d2_love_pool_oral_01
        with dissolve

        "[girlfriend_name] dropped to her knees between me and the low wall, still checking the upper windows before looking back up at me."
        gf "Nobody can see us."
        mc "You're really sure?"
        gf "I literally just told you I checked. Twice."

        scene cg ch01_d2_love_pool_oral_02
        with dissolve

        "What followed was quick, reckless and deliberately hidden from the rest of the villa."
        "The risk came from being outside, not from wanting an audience."
        "When we finally pulled ourselves back together, [girlfriend_name] was trying not to laugh at how absurdly pleased with herself she looked."

        $ exit_cinematic_mode()
        scene bg ch01_d2_sunset
        with dissolve

        gf "Nobody saw. Just so you know."
        mc "That's the fourth time you've said that."
        gf "Because nobody did! I'm just making sure you know."

        "We sat together at the edge of the pool while the light faded."
        gf "Today was actually really nice, you know? Like, weird, but nice."
        mc "Even the bee?"
        gf "The bee doesn't count. The bee's not part of today."
        mc "And Maya?"
        gf "I like her. I really like her. Is that weird? I've known her one day."
        mc "You might have mentioned that."
        gf "And..."
        "She bumped her shoulder into mine."
        gf "I like this."
        mc "This, as in the trip?"
        gf "Us, dummy. I like us."
        "There was nothing complicated in the way she said it."

        $ set_story_value("ch01_d2_sunset_response", "love_connected")
        $ set_story_flag("ch01_d2_love_sunset_oral")

    elif d2_lane == "exhibitionism":
        "[girlfriend_name] sat beside me, knees drawn up, still thinking about the pool."

        gf "Maya is such a bad influence. She's genuinely terrible."
        mc "Which part are we blaming her for?"
        gf "The strings. The bikini strings."
        mc "Oh. Those strings."
        gf "Don't. Don't say it like that."
        mc "You pulled them higher while two guys were staring at you."
        gf "When you say it like that, it sounds terrible."
        mc "I'm not complaining. I'm really, really not complaining."

        "[girlfriend_name] covered her face for a second, then peeked at me through her fingers."

        gf "And then she smacked my ass! In front of them!"
        mc "You didn't look that angry about it."
        gf "I was embarrassed. That's a different face."
        mc "I didn't say you weren't embarrassed."
        gf "[player_name]."
        mc "What? I'm just asking."

        "She lasted another few seconds before giving up."

        gf "...Fine. It was kind of hot."
        mc "Wait, the spanking part?"
        gf "No— I mean, kind of? The whole thing."
        gf "Knowing they were looking. Knowing you knew they were looking."
        mc "And losing your top?"
        gf "No."
        "She answered that one immediately."
        gf "I mean... not like that."
        gf "I was mortified. Actually mortified."
        mc "Was?"
        gf "Don't start. I see what you're doing."
        "She stared out at the water."
        gf "Thinking about it now is different."
        mc "Different how?"
        gf "...You know how."

        mc "So my girlfriend's secretly an exhibitionist."
        gf "I am not! I'm not. I'm just... curious."
        "I looked at her."
        gf "...Shut up."

        mc "If it turns you on, it turns you on."
        mc "You don't have to be embarrassed telling me."

        "Her expression softened."

        gf "I think part of why I liked it was because you knew."

        think "That part, I liked a lot."

        gf "What if I wanted to do something like that again? Not, like, losing my top. Something on purpose."
        mc "Like, tonight?"
        gf "I didn't say tonight."
        mc "You didn't say not tonight."

        "[girlfriend_name] smiled and leaned into me."

        $ set_story_value("ch01_d2_sunset_response", "exhibition_shared")
        $ set_story_flag("ch01_d2_exhibition_sunset_shared")

    else:
        "[girlfriend_name] stood beside me for a while before finally turning toward me."

        gf "Hey. Can I ask you something?"
        mc "Yeah, sure. What's up?"
        gf "Are we okay?"
        "I looked at her."
        gf "Because every time I look at you today, you're, like, somewhere else. You're here, but you're not here."
        gf "And if something's bothering you, you can just tell me. Even if it's dumb. Especially if it's dumb."

        $ d2_sunset_connect_text = format_choice("ch01_d2_sunset_connect", "Tell her the truth.")
        $ d2_sunset_partial_text = format_choice("ch01_d2_sunset_partial", "I've just been in my own head.")
        $ d2_sunset_ignore_text = format_day2_risk_choice("ch01_d2_sunset_ignore_gate", "I'm fine.", severity="soft")

        menu:
            "[d2_sunset_connect_text]":
                $ apply_choice("ch01_d2_sunset_connect")
                $ set_story_value("ch01_d2_sunset_response", "opened_up")

                mc "No. I'm not really okay."
                "[girlfriend_name] waited."
                mc "I slept badly. I've been jealous. The pool thing looked insane for about three seconds, and instead of saying any of that I've been acting like an idiot."
                gf "Babe. Nothing happened with [friend_name]. You know that, right?"
                mc "I know. I do know."
                gf "Then when your brain starts telling you something else, talk to me. Don't just go quiet on me."
                mc "Yeah. I can do that. I'll try."
                "She took my hand."
                gf "That's all I wanted. That's literally all."

            "[d2_sunset_partial_text]":
                $ apply_choice("ch01_d2_sunset_partial")
                $ set_story_value("ch01_d2_sunset_response", "partial_honesty")

                mc "I've just been in my own head."
                gf "About me? About us?"
                mc "About... everything, I guess. I don't know."
                "She studied me, then nodded."
                gf "Just... don't disappear on me, okay? I hate guessing."
                mc "I won't. I'm not going anywhere."
                "It was not the whole truth, but it was enough that she stopped having to guess."

            "[d2_sunset_ignore_text]":
                $ apply_choice("ch01_d2_sunset_ignore_gate")
                $ set_story_value("ch01_d2_sunset_response", "ignored_gate")
                $ set_story_value("ch01_d2_ntr_soft_gate", True)

                mc "I'm fine."
                gf "[player_name]."
                mc "I said I'm fine."

                "My phone buzzed against the table."
                "I checked it instead of looking at her."

                gf "...Okay."

                "[girlfriend_name] turned back toward the sunset."
                "She'd been checking for me all day. This time, when she looked away, she didn't look back."

                if current_choice_mode() == "developer":
                    centered "NTR SOFT GATE — ch01_d2_ntr_soft_gate = True"
                elif current_choice_mode() == "full":
                    centered "Major relationship consequence."
                elif current_choice_mode() == "insight":
                    centered "[girlfriend_name] stops repeatedly reaching back toward [player_name]."

    "A few minutes later [friend_name] came back downstairs, freshly changed and completely unaware of what had just happened."

    friend "Hey. Are we still doing dinner at eight? Because I told them eight, and they sounded very serious about it."

    if get_story_value("ch01_d2_ntr_soft_gate", False):
        gf "Yeah."
        "[girlfriend_name] answered without looking at me."
    else:
        gf "Yeah, eight. I'll be ready."
        "[girlfriend_name] looked at me as she answered, and I nodded."

    $ set_story_value("ch01_d2_route_lane_post_sunset", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_20_complete")
    jump ch01_day2_scene_21_pre_sunset


label ch01_day2_scene_21_pre_sunset:

    # Getting ready after sunset. The Black Cutout Mini bought at the boutique is
    # explicitly reserved for Day Three and is never used for this dinner.
    scene bg ch01_villa_bedroom_night  # after sunset: night art (darryn)
    with dissolve

    $ d2_lane = get_story_value("ch01_d2_route_lane_post_sunset", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    if d2_soft_gate:
        "[girlfriend_name] came upstairs, opened her suitcase and chose without asking me."
        "She pulled out the bolder evening option she had already packed for the trip: a loose low-cut top with a fitted skirt."
        "The Black Cutout Mini from the boutique stayed folded in its bag."

        $ set_story_value("ch01_d2_dinner_outfit", "loose_low_cut")
        $ set_story_value("ch01_d2_dinner_outfit_id", "d2_loose_low_cut")
        $ grant_story_outfit("d2_loose_low_cut", equip=True)
        $ set_story_value("ch01_d2_dinner_outfit_source", "leia")

    elif d2_lane == "exhibitionism":
        "[girlfriend_name] held up the two evening options and looked at me."

        gf "After everything we just talked about..."
        gf "Which one? And be honest."
        mc "The low-cut one. Obviously the low-cut one."
        "Her mouth curved into a small smile."
        gf "Yeah, I thought you'd say that."
        mc "Is that too much? For dinner?"
        gf "You tell me. You're the one who picked it."
        mc "Wear it. Seriously. You'll look amazing."
        gf "Then I'm wearing it."

        "She changed right there, still smiling, like we'd just agreed on something bigger than a top."

        $ set_story_value("ch01_d2_dinner_outfit", "loose_low_cut")
        $ set_story_value("ch01_d2_dinner_outfit_id", "d2_loose_low_cut")
        $ grant_story_outfit("d2_loose_low_cut", equip=True)
        $ set_story_value("ch01_d2_dinner_outfit_source", "ryan")

    else:
        "[girlfriend_name] came upstairs with two outfits over one arm."

        gf "Babe, help me pick? I've been holding these up for ten minutes and I hate both of them now."

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
                        title_text=('Pick ' + girlfriend_name + "'s Day Two dinner outfit"),
                    )
                    love_route_wear_request(d2_love_outfit_pick, route_lane="love")
                    set_story_value("ch01_d2_dinner_outfit_id", d2_love_outfit_pick)
                    set_story_value(
                        "ch01_d2_dinner_outfit",
                        "loose_low_cut" if love_outfit_is_daring(d2_love_outfit_pick) else "secure_date",
                    )
                    set_story_value("ch01_d2_dinner_outfit_source", "ryan")

                mc "Wear the [outfit_name(d2_love_outfit_pick)]."
                gf "Yeah, that one. Good call."
                "She'd asked me to pick, and she looked happy that I had."

            "Wear whatever you feel best in.":
                $ set_story_value("ch01_d2_dinner_outfit", "secure_date")
                $ set_story_value("ch01_d2_dinner_outfit_id", "resort_dinner_dress")
                $ set_story_value("ch01_d2_dinner_outfit_source", "leia")
                $ grant_story_outfit("resort_dinner_dress", equip=True)

                mc "Wear whatever you feel best in."
                gf "Then I'm picking the comfy one, and you're not allowed to say anything about it."

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

    gf "So this is why you abandoned us. You look amazing. I'm so mad."
    maya "Some of us need actual preparation. I had pool hair. You saw it."
    friend "You were gone for like two hours."
    maya "And look at what I did with them."

    "We took a rectangular table: [girlfriend_name] beside Maya, [friend_name] beside me on the opposite side."
    "[girlfriend_name] sat directly across from me. Maya sat directly across from [friend_name]."

    maya "So, [friend_name], are you getting anything with honey? Since you and bees are so close now."
    friend "Don't. Please. I've had a really long day."
    gf "Careful. There might be a bee in it."
    friend "I'm going to remember this. All of you. I'm writing it down."
    gf "In your defense, it was a really big bee."
    friend "Thank you. Finally. Somebody gets it."

    "Food arrived in waves. So did another round of drinks."
    "Maya asked everyone for their favorite part of the trip so far, then rejected [friend_name]'s answer because it involved room service."
    "[girlfriend_name] and Maya started planning what they wanted to see tomorrow."
    "[friend_name] complained that I still couldn't order from a menu in under ten minutes, which he's been saying since college. Maya immediately joined him."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if get_story_value("ch01_d2_ntr_soft_gate", False):
        "[girlfriend_name] was not hostile. She laughed with Maya, argued with [friend_name] and enjoyed dinner."
        "What changed was smaller: she stopped checking whether I was following every moment."
    elif d2_lane == "exhibitionism":
        "Every so often [girlfriend_name] caught my eye across the table and smiled like we were carrying a private conversation nobody else could hear."
    else:
        "[girlfriend_name] and I fell into the small habits that came with four years together: passing the right sauce before the other asked, trading bites, finishing each other's complaints."

    $ set_story_flag("ch01_d2_scene_22_complete")
    jump ch01_day2_scene_23_dinner_reach


label ch01_day2_scene_23_dinner_reach:

    scene bg ch01_d2_dinner
    with dissolve

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    "Halfway through dinner, a shared dish landed near the middle of the table, slightly closer to our side."

    if d2_soft_gate and d2_lane == "ntr_risk":
        "[girlfriend_name] looked at the dish, then leaned across instead of asking me to pass it."

        $ enter_cinematic_mode()
        scene cg ch01_d2_dinner_reach
        with dissolve

        "The loose neckline shifted as she reached."
        "[friend_name] noticed. He wasn't obvious about it, but it was long enough that [girlfriend_name] caught him before he could look away."

        $ exit_cinematic_mode()
        scene bg ch01_d2_dinner
        with dissolve

        "[girlfriend_name] met his eyes."
        "Then she gave him a tiny wink."

        "[friend_name] looked genuinely surprised."
        "He did not wink back."
        "[girlfriend_name] simply sat down and continued eating."

        "It lasted less than a second. Long enough that I knew I hadn't imagined it."

        $ set_story_value("ch01_d2_dinner_wink", True)
        $ set_story_value("ch01_d2_dinner_reach", "winked_julian")

    elif d2_lane == "exhibitionism" and get_story_value("ch01_d2_dinner_outfit") == "loose_low_cut":
        "[girlfriend_name] looked at the dish."
        "Then she looked at me."
        "She could have asked me to pass it. Instead, she leaned."

        $ enter_cinematic_mode()
        scene cg ch01_d2_dinner_reach
        with dissolve

        "The neckline shifted as she reached across the table."
        "[friend_name] was in the same sightline, but [girlfriend_name]'s eyes came straight back to mine."

        $ exit_cinematic_mode()
        scene bg ch01_d2_dinner
        with dissolve

        "I raised an eyebrow."
        "[girlfriend_name] gave me the smallest possible smile."

        maya "What? What was that? What are you two doing?"
        mc "Nothing."
        gf "Nothing! Eat your food."

        $ set_story_value("ch01_d2_dinner_reach", "smiled_at_ryan")

    else:
        gf "Babe, can you pass that?"
        mc "This one? The spicy one?"
        gf "Yeah, that one. Thank you."

        "I passed it across. [girlfriend_name] took it with an easy smile."

        $ set_story_value("ch01_d2_dinner_reach", "asked_ryan")

    $ set_story_flag("ch01_d2_scene_23_complete")
    jump ch01_day2_scene_24_dinner_aftermath


label ch01_day2_scene_24_dinner_aftermath:

    if get_story_value("ch01_d2_dinner_wink", False):
        "I did not confront [girlfriend_name] at the table."
        "[friend_name] did not encourage the moment either. If anything, he became more careful about where he looked."
        "[girlfriend_name] never checked whether I had noticed."
    elif get_story_value("ch01_d2_dinner_reach") == "smiled_at_ryan":
        "Later [girlfriend_name] caught me looking again."
        "The satisfied little smile she gave me closed the loop without either of us saying a word."
    else:
        "Dinner stayed easy. Maya and [friend_name] did most of the arguing while [girlfriend_name] and I enjoyed the show."

    "By the second round, everybody was noticeably looser."

    friend "There's more back at the villa, if anyone wants. No pressure. There's just, you know, a lot."
    maya "That sounds really irresponsible."
    friend "You don't have to come. I'm just saying it's there."
    maya "I didn't say no, [friend_name]. Don't put words in my mouth."

    "We paid, walked back to the villa together, and let the night follow us home."

    $ set_story_flag("ch01_d2_scene_24_complete")
    jump ch01_day2_scene_25_maya_stays


label ch01_day2_scene_25_maya_stays:

    scene bg ch01_d2_game_night
    with fade

    # Julian check-in (Day One car apology, ch01_julian_apology_response). Flavor only: no stats, no route.
    "Back at the villa, [friend_name] and I ended up at the kitchen counter on ice duty while Maya and [girlfriend_name] fought over whose playlist was less embarrassing."
    $ d2_julian_apology = get_story_value("ch01_julian_apology_response")
    $ d2_julian_pool = get_story_value("ch01_d2_pool_incident") == "leia_julian_bee_top_off"
    if d2_julian_apology == "trusted":
        friend "Hey, quick one, while they're busy. In the car yesterday you just said don't worry about it, and I've genuinely been trying not to. I'm just checking. We're good?"
        if d2_julian_pool:
            friend "Because today she also ended up hiding behind me in the pool without her top, which, again, the bee, but I'd get it if two days in a row is a lot."
        mc "We're good, man. I meant it in the car. I'd tell you if we weren't."
        friend "Okay. Good. You're kind of the one person on this trip I really don't want it to be weird with."
        "He went back to cracking ice into the bucket like we'd been talking about the weather."
    elif d2_julian_apology == "honest_discomfort":
        friend "So, you said yesterday it bothered you for a second, and I said I'd be careful. I just want you to know I've been careful, like, actively, all day. Maya asked me if something was wrong with my neck."
        if d2_julian_pool:
            friend "And then the pool happened, which was the opposite of careful, I know. I kept my hands up the whole time. I'm just saying it out loud so it's said."
        mc "I noticed. You've been looking at the ceiling a lot."
        friend "It's a good ceiling. Very good ceilings in this place."
        think "He'd taken one sentence from me in the car and carried it around all day. That was so him I almost laughed."
    elif d2_julian_apology == "joked":
        friend "So I've been thinking about your note from the car. 'Catch her with less enthusiasm.'"
        if d2_julian_pool:
            friend "And I want it on record that in the pool today I had zero enthusiasm. None. I kept my hands up and looked at a tree. Very professional."
        else:
            friend "And I want it on record that I've caught nobody today. Not one person. Zero catches."
        mc "Like a fireman."
        friend "Exactly like a fireman. But, for real, though. We're cool?"
        mc "We're cool. You know we're cool."
    elif d2_julian_apology == "said_fine":
        friend "Can I say something, and you don't do the voice?"
        mc "What voice?"
        friend "The 'it's fine' voice. You did it in the car yesterday, and I let it go, because she was asleep in the back and we were ten minutes from home. I'm not letting it go twice."
        friend "If something's bugging you, about me, about her, about any of it, just say it. I'd honestly rather have the awkward conversation than watch you be fine at me for a week."
        mc "It's... I don't know. It's mostly fine."
        friend "Mostly."
        mc "Mostly. I'll tell you if it stops being mostly."
        friend "That's all I'm asking."
        "He handed me the ice bucket, and that was the end of it, the way it usually is with us."
    else:
        friend "Grab the limes? Maya's going to want limes. She seems like a lime person."
        mc "How can you tell?"
        friend "I can't. I'm guessing. I just don't want to be the guy who forgot the limes."

    "An hour later the coffee table was crowded with bottles, mixers, snacks and four glasses."
    "We had switched to water between drinks, but nobody was pretending the night was still sober."

    maya "We need a game. I'm not just sitting here drinking like an adult."
    friend "No. Every time someone says that, I end up regretting something."
    maya "Never Have I Ever."
    friend "That's even worse. That's the worst one."
    gf "That means yes. When he says it like that, it means yes."

    maya "Normal rules. If you've done it, you drink. No lying, I'll know."

    maya "Never have I ever missed a flight."
    "[friend_name] drank immediately."
    maya "I knew it! I could feel it."
    friend "It was one time, and it wasn't my fault. The gate changed and nobody told me."
    maya "Everyone says that! That's what everyone who misses a flight says!"

    maya "Never have I ever stalked someone on social media before meeting them."
    "Maya drank."
    "[girlfriend_name] hesitated, then took a small drink too."
    gf "It's research! Everyone does research."
    mc "Is that what you're calling it?"
    gf "Yes. That's what it's called. Thank you."

    maya "Never have I ever pretended to like food because someone else cooked it."
    "I drank. [girlfriend_name] stared at me."
    gf "Excuse me? Whose food?"
    mc "I'm not answering that. That's a trap."
    gf "It's a trap now. It's a trap for later, actually."

    friend "Never have I ever lied about being busy because I didn't want to go somewhere."
    "Three glasses moved."
    maya "[friend_name]! You drank!"
    friend "I'm honest about lying. That has to count for something."

    gf "Never have I ever had a holiday romance."
    "Maya drank."
    friend "That actually explains a lot."
    maya "It explains nothing. You know nothing about it. It was Lisbon, and it was beautiful."

    $ set_story_flag("ch01_d2_maya_stays_for_drinks")
    $ set_story_flag("ch01_d2_scene_25_complete")
    jump ch01_day2_scene_26_game_rules


label ch01_day2_scene_26_game_rules:

    "The harmless questions lasted long enough for everyone to get comfortable."

    maya "Enough warm-up. Dating questions."
    friend "And here we go. I knew it was coming."
    maya "Never have I ever had a crush on someone I shouldn't have."

    "Maya drank without hesitation."
    "[friend_name] studied his glass like it contained legal advice."

    maya "Never have I ever checked someone out while I was already in a relationship."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if d2_lane == "love":
        "[girlfriend_name] took a drink and looked at me sheepishly."
        gf "What? I'm not blind. People are allowed to be cute."
        mc "I'm sitting right here, babe."
        gf "You'll survive. You're cute too, it's not a competition."
    elif d2_lane == "exhibitionism":
        "[girlfriend_name] took a drink while looking straight at me."
        "After everything we'd said at sunset, she didn't need to explain it to me."
    else:
        "[girlfriend_name] took a drink."
        "She did not look at me."

    # Day One looking rule (ch01_relationship_philosophy / ch01_looking_philosophy): Maya tests the line.
    $ d2_looking_rule = get_story_value("ch01_looking_philosophy")
    if d2_lane == "ntr_risk":
        if d2_looking_rule == "encouragement_boundary":
            think "Looking is looking. Encouraging it is different. I'd said that last night like it settled something."
        elif d2_looking_rule == "harmless":
            think "Trust matters more than arbitrary rules. That was my answer last night. Sitting here watching her not look at me, I wanted a rule."
        elif d2_looking_rule == "enjoy_attention":
            think "A little jealousy can actually be fun, I'd said. It didn't feel like fun from this side of the table."
        elif d2_looking_rule == "indifferent":
            think "I'd told her I try not to care about stuff like that. Maybe she'd believed me."
    elif d2_looking_rule == "encouragement_boundary":
        gf "Looking is looking, though. You said that last night, during the worst movie ever made."
        mc "I did say that. I stand by it."
        gf "And encouraging it is different. See? I was listening."
        maya "Wait, back up. You guys have a rule? Like, an actual rule?"
        gf "One rule. He made it up on the couch."
        maya "Okay. So looking's fine, encouraging isn't. Let's find out where that line actually is, then."
    elif d2_looking_rule == "harmless":
        gf "And someone looking doesn't matter, as long as nobody's hiding anything. That's the rule. I said it, he said yeah, so it counts."
        mc "As long as we're honest. I remember."
        friend "I said it was mature at the time, and I stand by it. I was expecting a joke."
        maya "Nobody hiding anything. Great. That makes the next ones so much more fun."
    elif d2_looking_rule == "enjoy_attention":
        gf "You said a little jealousy could actually be fun, remember? So. Is it fun yet?"
        mc "Ask me again after a few more of these."
        "She grinned at me over her glass like she'd won something."
        maya "Wait, he said that? Jealousy's fun? Oh, I'm absolutely testing that."
    elif d2_looking_rule == "indifferent":
        gf "You don't mind, though. You said you try not to care about stuff like that."
        "She said it lightly. She was watching my face the whole time she said it."
        mc "I mean... yeah. I said that."
        think "I'd said it on the couch like it cost me nothing. It sounded different with her waiting to see if I meant it."
        maya "Huh. You really don't care? Okay. Interesting."

    maya "Never have I ever enjoyed knowing someone was checking me out."

    "Maya drank."
    if d2_lane == "exhibitionism":
        "[girlfriend_name] drank too."
        "Her eyes flicked to mine over the rim."
    elif d2_lane == "ntr_risk" and (lc_stat("exhibitionism") >= LC_T["d2_game_drinks"] or get_story_value("ch01_d2_ntr_soft_gate", False)):
        "[girlfriend_name] hesitated, then drank."
        "This time she kept her attention on the glass."
    else:
        "[girlfriend_name] left her drink on the table."

    maya "Never have I ever flirted just to see if I could."
    "Maya drank again."

    if get_story_value("ch01_d2_dinner_wink", False):
        "[girlfriend_name]'s fingers rested against her glass, but she did not pick it up."
        "I noticed."
    elif d2_lane == "exhibitionism":
        "[girlfriend_name] looked at me, smiled, and took the smallest possible sip."
    else:
        "[girlfriend_name] shook her head."

    maya "These are getting boring. Nobody's drinking enough."
    friend "That usually means you're about to make them worse."
    maya "Better. I'm making them better."
    friend "Worse and better are opposites, Maya. That's the one thing they are."

    maya "New rule. Burning questions."
    maya "If you don't want to answer, and you don't want to drink, you lose something."

    friend "That is not how Never Have I Ever works."
    maya "It is now. I'm the rules person. Somebody has to be."

    gf "I'm in. Wait, are we sure? ...No, I'm in."
    mc "You're sure? ...Okay. Yeah, I'm in."
    friend "I'm outvoted, aren't I. I can feel it."
    maya "Completely outvoted. Welcome."

    $ set_story_flag("ch01_d2_strip_penalty_agreed")
    $ set_story_flag("ch01_d2_scene_26_complete")
    jump ch01_day2_scene_27_game_escalates


label ch01_day2_scene_27_game_escalates:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    maya "Fine. Burning question. Who here has found someone else in this room attractive?"

    "The room went quiet."
    "[girlfriend_name] stared at Maya."

    gf "That's not even Never Have I Ever."
    maya "Burning questions! I literally just made the rule."
    gf "I'm not answering that."
    maya "Then drink."
    gf "No! Then it's an answer. Drinking is an answer."
    maya "Then you know the rule. Only if you want to, though. You can just answer."

    "[girlfriend_name] looked down at herself, then stood."

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

    friend "I can't believe that actually worked. I didn't think the rule was real."
    maya "Everything's real if you commit. Respect the rules."

    maya "Never have I ever hooked up with someone and forgotten their name."

    "Maya made a face."
    friend "Drink, then."
    maya "No. Absolutely not."
    gf "Then answer!"
    maya "Also no. Next."
    gf "Penalty! You don't get to skip, you made the rule!"

    "Maya reached beneath her dress, wriggled for several seconds and pulled her panties free without removing the dress."

    friend "You somehow removed clothing and became no less dressed."
    maya "That's called skill. Years of practice."
    gf "That's cheating. That's so cheating."
    maya "It's strategy. There's a difference."

    $ set_story_value("ch01_d2_nhie_maya_clothes", "dress_bra_no_panties")

    gf "[friend_name]. Never have I ever been rejected after thinking I definitely had a chance."

    "[friend_name] stared at her."

    friend "I'm not discussing this. Nope. We're not doing this one."
    maya "Then drink."
    friend "No, because then it's a yes."
    maya "Then shirt. Off. Rules."

    "He sighed, pulled his shirt over his head and threw it onto the arm of the sofa."

    $ set_story_value("ch01_d2_nhie_julian_clothes", "pants_underwear_shades")

    maya "Never have I ever deliberately worn something because I knew someone would look."

    "Maya drank."
    if d2_lane == "exhibitionism":
        "[girlfriend_name] drank too, looking at me."
    elif d2_soft_gate:
        "[girlfriend_name] took a slow drink without looking my way."
    else:
        "[girlfriend_name] considered it, then left her glass down."

    friend "Never have I ever done something sexual somewhere I could've been caught."

    if get_story_flag("ch01_d2_love_sunset_oral"):
        "[girlfriend_name] and I both drank."
        maya "Oh? Oh. Both of you?"
        gf "Next question."
        maya "No, absolutely not, you don't get to drink together and say next question. Where?"
        gf "I said next question! [player_name], help me."
    else:
        "Maya drank and refused to elaborate."

    maya "Never have I ever been turned on because someone was watching."

    "Maya drank casually."

    if d2_lane == "exhibitionism":
        "[girlfriend_name] looked at me, then drank."
        "We both knew exactly what she meant."
    elif d2_soft_gate and lc_stat("exhibitionism") >= LC_T["d2_game_drinks"]:
        "[girlfriend_name] drank after a pause."
        "She did not explain."
    else:
        "[girlfriend_name] did not move."

    maya "[girlfriend_name]. This one's for you."
    maya "Never have I ever enjoyed attention from someone I knew I probably shouldn't."

    "[girlfriend_name]'s expression changed."

    if d2_lane == "love" and not d2_soft_gate:
        gf "No. Actually, no."
        maya "No? You're not even going to drink?"
        gf "I'm answering this one. No. I haven't."
        "She stayed in her bra and panties and reached for her water instead."
    else:
        gf "I'm not answering that."
        maya "Then drink. Or don't. Your call."
        gf "No. I'm not drinking for that one."
        maya "Then... I mean, you can pass. Seriously."

        "[girlfriend_name] exhaled and reached behind herself."

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

    friend "Oh? Oh, that's a face."
    maya "No. That's not a face."
    friend "Then drink."
    maya "Also no. I'm taking the penalty."

    "She reached beneath the dress again and removed her bra."

    friend "This is fraud. You're committing fraud right in front of us."
    maya "I told you. Strategy."
    gf "You're still completely dressed."
    maya "I planned ahead. Some of us think about these things."

    $ set_story_value("ch01_d2_nhie_maya_clothes", "dress_only")

    gf "Never have I ever hooked up with two people in the same twenty-four hours."

    "Maya froze."

    maya "Past Maya would like to invoke her right to silence."
    friend "Nope. Penalty. You made the rule."
    maya "Past Maya was an idiot."
    gf "You invented the stripping rule."
    maya "I know! I know I did. I hate it here."

    "Maya looked down at the single dress she had left."

    maya "Fuck it."

    "She pulled it over her head and dropped back onto the sofa completely nude."

    maya "Happy? Is everybody happy now?"
    friend "I have made a deliberate decision not to answer that."
    gf "Coward. Total coward."

    $ set_story_value("ch01_d2_nhie_maya_clothes", "nude")
    $ set_story_flag("ch01_d2_nhie_maya_nude")

    $ set_story_flag("ch01_d2_scene_27_complete")
    jump ch01_day2_scene_28_julian_strips


label ch01_day2_scene_28_julian_strips:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    maya "[friend_name]."
    maya "Never have I ever slept with someone I knew one of my friends liked."

    "[friend_name]'s joking expression flattened for a moment."

    friend "No. Nope."
    maya "No, you haven't?"
    friend "No, I'm not doing the follow-up."
    maya "Then drink."
    friend "Not drinking either."
    gf "Then pants! Pants, [friend_name]."

    friend "This game is rigged. This whole game is rigged against me specifically."
    maya "Yep. Totally rigged."

    "He stood, removed his trousers with considerably less dignity than he wanted, and sat back down in his underwear."

    $ enter_cinematic_mode()
    scene cg ch01_d2_julian_underwear_reveal
    with dissolve

    "For one beat the room became very quiet."

    if d2_lane == "love":
        "[girlfriend_name] looked because everyone looked, gave a surprised little laugh, then turned back toward me."
    elif d2_lane == "exhibitionism":
        "[girlfriend_name] looked."
        "Then she realized I had noticed her looking and met my eyes with a tiny, mischievous expression."
        "The moment came back to me instead of staying with [friend_name]."
    elif d2_soft_gate:
        "[girlfriend_name] looked longer than she had on the other routes."
        "She did not immediately check whether I had noticed."

    $ exit_cinematic_mode()
    scene bg ch01_d2_game_night
    with dissolve

    maya "...Oh."
    friend "Don't. Please don't."
    maya "I didn't say anything."
    friend "Your face said a lot. Can we— can we not?"

    $ set_story_value("ch01_d2_nhie_julian_clothes", "underwear_shades")
    $ set_story_flag("ch01_d2_julian_reveal_seen")

    "Maya recovered first."

    maya "Last one. Last one, I promise."
    maya "Never have I ever slept with someone whose name I didn't know."

    "[friend_name] paused just slightly too long."

    maya "Oh my God. [friend_name]."
    friend "What? I didn't do anything."
    maya "You paused! Drink."
    friend "No. I'm not drinking for a pause."
    gf "Then answer."
    friend "Also no. I'm not answering a pause either."
    maya "Then take something off."

    "[friend_name] looked down at his underwear."
    "Then he reached up and removed his sunglasses."

    maya "No. No, no."
    maya "Absolutely not."
    friend "What? What's wrong with that?"
    maya "Those are not clothes!"
    friend "They were on my body. Technically that's clothing. It's, like, face clothing."
    maya "That's a rules problem! There's no such thing as face clothing!"
    gf "I mean... he's kind of got a point."
    maya "DO NOT ENABLE HIM."

    $ set_story_value("ch01_d2_nhie_julian_clothes", "underwear_no_shades")
    $ set_story_flag("ch01_d2_julian_shades_removed")

    "That killed the game more effectively than any official ending could have."

    $ set_story_flag("ch01_d2_scene_28_complete")
    jump ch01_day2_scene_29_game_winds_down


label ch01_day2_scene_29_game_winds_down:

    scene bg ch01_d2_game_night
    with dissolve

    maya "I'm done. I'm out. This game is corrupt."
    friend "You made the rules, Maya. You made every single rule."
    maya "Then the administration is corrupt."

    "Maya tried to stand, reconsidered halfway up and sat back down."

    gf "Yeah, no. You're not going home like this."
    maya "I'm perfectly capable of—"

    "She tried again."
    "[girlfriend_name] caught her arm before gravity could make the argument for her."

    gf "You're staying here. That's not a question."
    maya "Fine. Fine. Couch, then."

    friend "Take my room. It's honestly not a big deal, I'll grab a pillow."
    maya "No, it's fine. I'll take the couch."
    friend "You're not sleeping on the couch."
    maya "Then where are you sleeping?"
    friend "The couch. Obviously."
    maya "No. No way."
    friend "Maya, take the room."
    maya "I'm not kicking you out of your own bed."
    friend "You're not. I'm offering."
    maya "Still no. That's still kicking you out."
    friend "Seriously. Take it. I'll sleep out here."

    "Maya squinted at him, very drunk and very focused, like he was a math problem."

    maya "Okay. Okay, fine."

    "She pointed at him."

    maya "But you're sleeping with me then."

    "The room stopped."

    friend "...What?"

    "Maya grinned."

    maya "You're a rich boy, [friend_name]. I'm not letting you pretend you know how to sleep on a couch."
    friend "I know how a couch works. It's not— it's not like that."
    maya "Do you?"
    friend "I've used one before."
    maya "For sleeping?"

    "[friend_name] paused."

    maya "See? That pause. That's what I thought."

    "His expression softened from joking to careful."

    friend "Wait. Are you sure? Actually sure?"
    maya "[friend_name]."
    friend "I'm asking. I'm just asking. You've had a lot to drink."
    maya "I'm sure. I told [girlfriend_name] this afternoon, way before any of this."
    maya "Yes. I'm sure. Come on."

    "Maya scooped her dress off the floor, caught [friend_name] by the wrist and started pulling him toward the corridor."

    maya "And bring water."
    friend "Very romantic. Okay."
    maya "Don't make it weird."

    "[friend_name] grabbed two bottles of water with his free hand and let her drag him away."
    "They disappeared into his room together."
    "Nothing about the exchange suggested an agreement beyond sharing the bed; Maya had been the one to invite him after he offered to sleep elsewhere."

    $ set_story_value("ch01_d2_maya_sleeping", "julian_room_shared_bed")
    $ set_story_value("ch01_d2_julian_sleeping", "julian_room_shared_bed")
    $ set_story_flag("ch01_d2_maya_julian_share_room")

    "The bedroom door closed somewhere down the corridor."
    "For the first time since we'd come back from dinner, the villa was quiet."

    "Just me and [girlfriend_name]."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if d2_lane == "love":
        "[girlfriend_name] found her dress, looked at it, then decided putting it back on for the walk upstairs was unnecessary."
        "She stayed in her bra and panties and came over to me."
    else:
        "[girlfriend_name] was still in her panties, both arms folded across her bare chest."
        "Even after the game ended she was not yet comfortable simply standing uncovered in the room."

    gf "So. Well."
    mc "Yeah."
    gf "That got so out of hand. That got really out of hand."
    mc "Maya got naked. All the way naked."
    gf "[friend_name] took off his sunglasses, though."
    mc "Yeah. I think that was the bigger shock."

    "[girlfriend_name] laughed, tired and tipsy."

    $ set_story_flag("ch01_d2_scene_29_complete")
    jump ch01_day2_scene_30_bedroom


label ch01_day2_scene_30_bedroom:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)
    $ d2_wink = get_story_value("ch01_d2_dinner_wink", False)
    $ d2_pool_suspicion = get_story_flag("ch01_d2_pool_suspicion")
    python:
        d2_love_exhib_blend = lc_stat_model.d2_love_exhib_blend(d2_lane, lc_stats_flat(), lc_exhib_gained("ch01_d2_"))

    scene bg ch01_villa_bedroom_night  # after game night: night art (darryn)
    with fade

    "Upstairs, we drank water and took a few quiet minutes to let the alcohol and noise settle."

    # Day One upstairs echo (ch01_upstairs_response): the same bedroom as last night's talk.
    # honest/liked = loving, and Ryan says thank you; a strained evening gets a quieter memory instead.
    $ d2_upstairs = get_story_value("ch01_upstairs_response")
    $ d2_bed_strained = d2_soft_gate or (d2_pool_suspicion and d2_lane == "ntr_risk")
    if d2_upstairs in ("honest", "liked") and d2_bed_strained:
        if d2_upstairs == "honest":
            think "Last night, in this same room, I'd told her the carrying thing bothered me, and she'd just wrapped her arms around me for it."
        else:
            think "Last night, in this same room, I'd told her I didn't hate people noticing her, and she'd made me promise we'd actually talk about it."
        think "Tonight I couldn't even find the start of the sentence."
    elif d2_upstairs == "honest":
        "[girlfriend_name] came out of the bathroom with her hair half tied up, and for a second it was last night again: me standing in the middle of this room, her asking what was going on."
        think "I'd told her the carrying thing bothered me. She hadn't laughed, or made it a thing. She'd just put her arms around me and said she liked it when I told her stuff."
        think "Thirty seconds of that, and I'd been grateful for it all day without saying so."
        mc "Hey. Thanks for last night. Up here, I mean. When I was being weird about the carrying thing."
        gf "You weren't being weird, you were being honest. Those are, like, different things."
        gf "And you don't have to thank me for that, babe. You tell me something, I hug you. That's kind of the whole deal."
        mc "I know. I'm still saying thanks."
        "She stopped fussing with her hair and looked at me properly, the way she does when she's deciding not to tease me."
        gf "...Okay. You're welcome. Come here."
    elif d2_upstairs == "liked":
        "[girlfriend_name] caught me watching her from the bathroom doorway and gave me the same look she'd given me last night, right here, when I'd admitted I didn't hate people noticing her."
        think "She could've laughed at me. Or gone quiet and wondered what kind of guy says that. Instead she'd checked my face to make sure I meant it, and made me promise we'd talk properly."
        think "She'd made it something we were in on together, instead of something I had to keep to myself. I still didn't know how to tell her how much that mattered."
        mc "Hey. Thank you. For last night. For not thinking I was a weirdo."
        gf "Oh, I definitely thought you were a weirdo."
        "She laughed at her own line before I could."
        gf "Good weird, though. I told you. I'm just really glad you said it, instead of being all mysterious and making me guess."
        mc "Me too."
        "She dropped onto the bed next to me and bumped her knee against mine, like we were still in on something."
    elif d2_upstairs == "swallowed":
        "[girlfriend_name] brushed her teeth with the bathroom door open, in the same doorway she'd stood in last night asking me what was going on."
        think "It's fine. Just a long day. That was what I'd told her, standing right about here."
        think "She'd believed me because I asked her to. A couple of times today I'd caught her looking at me and deciding not to ask."
        "I almost said something. Then she switched off the bathroom light, and the moment went with it."
    elif d2_upstairs == "snapped":
        "[girlfriend_name] picked her clothes up off the chair and folded them, carefully, without really looking at them."
        think "She'd folded the dinner dress like that last night too. Right after I told her to stay awake next time."
        if d2_bed_strained:
            think "I hadn't apologized for that either."
        else:
            mc "Hey. What I said last night, up here. The staying awake thing. That was a crappy thing to say."
            gf "...Yeah. It kind of was."
            "She set the clothes down."
            gf "I know you didn't mean it like that. I just thought about it a few times today. That's all."
            mc "I'm sorry. I really am."
            gf "Thank you. Really."
            "She didn't make me say it twice. She came and sat next to me, close enough that our knees touched."

    "Neither of us was stumbling or confused by the time we got into bed."

    if d2_soft_gate and d2_wink:
        jump ch01_day2_scene_30_ntr_nightmare

    elif d2_pool_suspicion and not d2_soft_gate and d2_lane == "ntr_risk":
        "[girlfriend_name] sat on the edge of the bed and looked at me."

        gf "You're doing it again."
        mc "Doing what?"
        gf "Thinking really loudly. I can hear it from here."

        $ d2_bed_love_text = format_choice("ch01_d2_bed_pool_love", "I didn't like seeing it, but I believe you.")
        $ d2_bed_ex_text = format_choice("ch01_d2_bed_pool_exhibition", "It bothered me... and I haven't stopped thinking about it.")
        $ d2_bed_accuse_text = format_choice("ch01_d2_bed_pool_accuse", "I want to believe you. I just keep seeing it.")

        menu:
            "[d2_bed_love_text]":
                $ apply_choice("ch01_d2_bed_pool_love")
                mc "I didn't like seeing it, but I believe you."
                gf "Nothing happened. I need you to actually believe that."
                mc "I know. I do."
                "Her shoulders finally relaxed."
                $ set_story_value("ch01_d2_route_lane_dinner", "love")
                $ d2_lane = "love"
                jump ch01_day2_scene_30_love

            "[d2_bed_ex_text]":
                $ apply_choice("ch01_d2_bed_pool_exhibition")
                mc "It bothered me... and I haven't stopped thinking about it."
                gf "Because you were jealous?"
                mc "Partly. Yeah."
                gf "And the other part?"
                mc "It's... complicated. I don't know how to say it."
                "Understanding slowly reached her expression."
                gf "Oh. Oh."
                $ set_story_value("ch01_d2_route_lane_dinner", "exhibitionism")
                $ d2_lane = "exhibitionism"
                jump ch01_day2_scene_30_exhibition

            "[d2_bed_accuse_text]":
                $ apply_choice("ch01_d2_bed_pool_accuse")
                mc "I want to believe you. I just keep seeing it."
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

    "[girlfriend_name] crossed to the window and pulled the curtains shut."

    gf "There. Better."
    mc "You know those don't really hide anything."
    gf "They hide enough. It's the thought that counts."
    mc "That's not what you said yesterday."
    gf "Shut up. Yesterday was different."

    "The thin fabric still let light and shapes through, but [girlfriend_name] had made the choice she wanted: tonight was private."

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
    scene bg ch01_villa_bedroom_night  # night art (darryn)
    with dissolve

    "Afterward [girlfriend_name] curled against me."

    gf "Today was a really good day."
    mc "Yeah. It was."
    gf "Even the bee?"
    mc "Especially the bee."
    gf "You're such an idiot."

    $ set_story_value("ch01_d2_bedroom_variant", "love_private")
    $ set_story_value("ch01_d2_end_route", "love")
    jump ch01_day2_scene_30_finish


label ch01_day2_scene_30_exhibition:

    "[girlfriend_name] looked toward the glass wall."

    mc "Curtains?"

    "She followed my eyes to them."
    "For a second I expected her to close them."

    gf "Leave them."

    "The answer came with a blush, but it came."

    mc "You sure? We can close them."
    gf "Yes. I'm sure. Leave them."

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
    "[girlfriend_name]'s face heated again."
    gf "...Yeah."
    mc "Yeah. I really did."
    gf "I liked knowing you were watching too."

    scene cg ch01_d2_exhib_bed_open_02
    with dissolve

    "As we started having sex, [girlfriend_name] looked toward the uncovered window again."

    gf "What if someone walked past?"
    mc "Nobody's there."
    gf "I know."

    "She looked back at me."

    gf "Pretend."

    scene cg ch01_d2_exhib_bed_open_03
    with dissolve

    mc "Someone stopped outside."
    "[girlfriend_name]'s eyes flicked toward the glass."
    mc "They can see the bed."
    "She instinctively drew one arm across her chest for a moment, the same reflex she'd had downstairs, then let it fall when she remembered this was only us."

    gf "Don't stop."

    "The fantasy was not that I disappeared from the scene."
    "It was that somebody else might see what [girlfriend_name] and I were choosing together."

    scene cg ch01_d2_exhib_bed_open_04
    with dissolve

    mc "They're still watching."
    "[girlfriend_name] hid her face against my shoulder, laughing once from embarrassment before looking back toward the window."

    gf "[player_name]..."
    mc "Want me to stop?"
    gf "No. Keep going."

    "We finished the game we had started, safely inside the room and fully aware that the imagined audience was only part of the roleplay."

    $ exit_cinematic_mode()
    scene bg ch01_villa_bedroom_night  # night art (darryn)
    with dissolve

    "A few minutes later [girlfriend_name] looked at the still-open curtains."

    gf "Close them now."
    mc "Now? Now you're shy?"
    gf "[player_name]."

    "I laughed and pulled them across."

    gf "Still think I'm secretly an exhibitionist?"
    mc "I don't think it's a secret anymore, babe."
    gf "Shut up. Go to sleep."

    if d2_love_exhib_blend:
        $ set_story_value("ch01_d2_bedroom_variant", "love_exhib_open_curtains")
        $ set_story_value("ch01_d2_end_route", "love")
    else:
        $ set_story_value("ch01_d2_bedroom_variant", "exhibition_open_curtains")
        $ set_story_value("ch01_d2_end_route", "exhibitionism")

    $ set_story_flag("ch01_d2_exhibition_bedroom_open_curtains")
    jump ch01_day2_scene_30_finish


label ch01_day2_scene_30_ntr_nightmare:

    "[girlfriend_name] gathered her things without looking at me for long."

    gf "I'm so tired."
    mc "Yeah."
    gf "I'm just going to go to sleep."

    "There was something I could have said."
    "I let the moment pass."

    "[girlfriend_name] fell asleep quickly."
    "I didn't."

    scene black
    with fade

    "The day replayed itself behind my eyes."
    "Not accurately."

    $ enter_cinematic_mode()
    scene cg ch01_d2_ntr_dream_strangers
    with dissolve

    "The strangers were back at the pool."
    "Only this time [girlfriend_name] wasn't embarrassed."
    "In the dream she turned toward them and deliberately squeezed her breasts together for their attention, smiling as if she had been waiting for them to notice."

    mc "[girlfriend_name]."

    "She didn't hear me."

    scene cg ch01_d2_ntr_dream_julian_pool
    with dissolve

    "The scene changed."
    "[friend_name] stood behind her in the pool."
    "Instead of looking away like he really had, he reached around and grabbed both of her breasts."
    "Dream-[girlfriend_name] leaned back into him."

    mc "[girlfriend_name]."

    "Still nothing."

    scene cg ch01_d2_ntr_dream_nhie
    with dissolve

    "The living room returned."
    "Reality had been [girlfriend_name] in panties, arms crossed tightly over her chest."
    "The nightmare stripped away even that boundary."
    "She sat completely nude in front of everyone, openly enjoying the attention and touching herself while I watched from somewhere nobody else seemed able to see."

    "She looked completely comfortable."
    "That was how I knew it wasn't her."

    scene cg ch01_d2_ntr_dream_wrong_room
    with dissolve

    "Then the end of the night replayed."

    "Maya should have taken [friend_name]'s hand."
    "Instead, [girlfriend_name] did."

    "She pulled him down the corridor."
    "I tried to follow."

    mc "[girlfriend_name]!"

    "Neither of them turned around."

    "The bedroom door closed."

    $ exit_cinematic_mode()
    scene black
    with lc_shake("m")
    pause 0.3

    scene bg ch01_villa_bedroom_night  # woken in the night: night art (darryn)
    with fade

    "I woke hard enough to pull the sheet with me."

    "[girlfriend_name] was beside me."
    "The real [girlfriend_name]."
    "Asleep in our bed."

    "She stirred when I moved."

    gf "[player_name]...?"
    "Her eyes barely opened."
    gf "You okay?"

    $ d2_wink_repair_text = format_choice("ch01_d2_wink_repair", "No. Tell her the truth.")
    $ d2_wink_accuse_text = format_day2_risk_choice("ch01_d2_wink_accuse_hard", ('Ask what she really wants from ' + friend_name + '.'), severity="hard")
    $ d2_wink_reject_text = format_day2_risk_choice("ch01_d2_wink_reject_hard", "I'm fine.", severity="hard")

    menu:
        "[d2_wink_repair_text]":
            $ apply_choice("ch01_d2_wink_repair")

            mc "No. Not really."

            "[girlfriend_name] woke properly."

            mc "I've been jealous all day."
            mc "The pool. Dinner. The game."
            mc "And instead of talking to you, I kept shutting you out."

            gf "[player_name]..."
            mc "I saw you wink at [friend_name]."

            "[girlfriend_name] went quiet."

            gf "I did."
            mc "Why?"

            "She stared at the ceiling for a few seconds."

            gf "I don't know."
            "Then she corrected herself."
            gf "No. That's not true."
            gf "Maybe because I was angry."
            gf "Maybe because I stopped thinking you'd care."

            mc "I cared. I do care."
            gf "You had a strange way of showing it."

            "I didn't have an answer to that, because she was right."

            mc "It crossed a line for me."
            gf "I know."
            gf "It was stupid. I shouldn't have done it."
            mc "And I shouldn't have spent the whole day making you guess whether I even wanted to be around you."

            "[girlfriend_name] reached for my hand."

            gf "Then next time, talk to me. Even if it's ugly. Just talk to me."
            mc "You too. If you're angry, tell me you're angry."
            gf "Deal. Okay. Deal."

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

            mc "What do you actually want from [friend_name]?"

            "[girlfriend_name] stared at me, suddenly awake."

            gf "What? What are you talking about?"
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

            "[girlfriend_name] looked away."

            gf "I'm saying I'm tired of trying to guess whether you even want me here."

            "Neither of us repaired it."
            "We turned away from each other."

        "[d2_wink_reject_text]":
            $ apply_choice("ch01_d2_wink_reject_hard")
            $ set_story_value("ch01_d2_ntr_confirmed", True)
            $ set_story_value("ch01_d2_end_route", "ntr_confirmed")
            $ set_story_value("ch01_d2_bedroom_variant", "ntr_gate_withdrawal")

            mc "I'm fine."

            "[girlfriend_name] watched me for a few seconds."
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

