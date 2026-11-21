# Leia's Consent — Chapter One: Something Different
# Day Two, Scenes 16–30.


label ch01_day2_scene_16_forced_split:

    $ d2_lane = get_story_value("ch01_d2_route_lane_pre_split", "love")

    "Eventually all four of us climbed out. [friend_name] and I took the table by the cooler, and the girls claimed the lounger next to it, kneeling up on the cushion side by side."
    "[friend_name] handed out what was left in the cooler, and Maya had hers raised before he'd even sat down."

    maya "Wait, toast. To unexpected shopping trips."
    gf "Absolutely not, I'm not toasting that. My feet still hurt from that shopping trip."
    friend "To my new shirt, then. It's a good shirt. Nobody's said one nice thing about it all day."
    maya "Because it's worse! That's so much worse than the shopping."
    mc "To surviving day two? Most of it, anyway."
    gf "Yes. That one. To surviving."

    "Four glasses met over the gap between the table and the lounger."

    # StrangersStare_Red_01 / _White_01 (darryn 2026-11-19): Ryan's view of the girls kneeling on
    # the lounger, Maya whispering behind her hand, two guys leaning on the low stone wall by the
    # villa gate behind them. Hidden POV: the guy without sunglasses (StrangersStare_*Closeup_01),
    # the girls from behind. Bikini follows her pick upstairs.
    $ enter_cinematic_mode()
    if get_story_value("ch01_d2_pool_outfit") == "pool_bolder":
        scene cg ch01_d2_strangers_stare_red
        with dissolve
        $ lc_pov_begin("d2_pool_strangers_red")
    else:
        scene cg ch01_d2_strangers_stare_white
        with dissolve
        $ lc_pov_begin("d2_pool_strangers_white")
    "Then Maya cupped a hand over her mouth and leaned into [girlfriend_name]'s ear, eyes sliding past her toward the wall."
    maya "Don't look now, but there are two guys at the wall behind you. They've been leaning on it for, like, ten minutes."
    "[girlfriend_name] went pink and stared straight ahead at me, very carefully not turning around."
    gf "Behind me? As in, behind behind me?"
    maya "We're kneeling on a lounger with our butts pointed right at the gate, babe. Yes. Behind behind."
    "Over their heads I could see them: two guys from somewhere outside the villa, arms folded on top of the low stone wall like it was a balcony seat."
    "One had sunglasses on. The other didn't bother pretending."
    $ lc_pov_end()
    $ exit_cinematic_mode()
    scene bg ch01_pool_day
    with dissolve

    "[girlfriend_name] lasted about two seconds before she looked over her shoulder."
    maya "Every single time! Why does nobody ever just not look?"
    gf "Because you say it like that! You say it like there's a celebrity behind me."
    "The one with the sunglasses looked away, not quite fast enough."
    gf "Maybe they're looking at you. You're the one in the, like, the strappy thing."
    maya "Babe. They have four eyes between them, and none of them are on me."

    # Kiss vs stretch (darryn 2026-11-19): NTR gets the stretch for the strangers, no kiss. Only
    # the NTS seed (warm NTR, red, the pool admission in 15b) gets the kiss (Kiss_Red_01-02).
    $ d2_nts_kiss = d2_lane == "ntr_risk" and get_story_value("ch01_d2_nts_seed") == "pool_admission"
    $ d2_kiss_red = get_story_value("ch01_d2_pool_outfit") == "pool_bolder"
    if d2_lane == "ntr_risk" and not d2_nts_kiss:
        "[girlfriend_name] looked toward me first."
        "I'd drifted half a step back from the table with my phone out, nodding along to whatever [friend_name] was saying without really hearing any of it."
        "She waited a second for me to look up. I only worked that out later. At the time I was still looking at my phone."
        "Then she turned back toward the strangers."

        # LeiaStretch_Red_01 / _White_01 (darryn 2026-11-19): Leia standing at the end of the
        # lounger, back to the wall, arms up in a long stretch; Maya sitting on the lounger looking
        # back over her shoulder with a knowing smile. Bikini follows her pick upstairs.
        $ enter_cinematic_mode()
        if get_story_value("ch01_d2_pool_outfit") == "pool_bolder":
            scene cg ch01_d2_leia_stretch_red
            with dissolve
        else:
            scene cg ch01_d2_leia_stretch_white
            with dissolve
        "[girlfriend_name] got up off the lounger, stood with her back to the wall and raised both arms over her head in a slow stretch, extending through her shoulders and back."
        "She held it there. A lot longer than a stretch needed."
        "Maya sat back on the lounger and glanced over her shoulder at the wall, then at [girlfriend_name], and smiled like she'd just been let in on something."
        "The same man kept looking."
        $ exit_cinematic_mode()
        scene bg ch01_pool_day
        with dissolve
        "Maya noticed. I didn't, and apart from that loose string I didn't notice much of anything that afternoon until Maya started pointing it out."
        $ set_story_value("ch01_d2_pool_attention", "leia_stretched_without_ryan")

    else:
        "By then I'd given up the table and stretched out on the empty lounger beside theirs."
        "[girlfriend_name] looked from the strangers to me. Then she climbed across onto my lounger on her hands and knees."

        # Kiss_White/Red_01-03 (darryn 2026-11-19): 01 Ryan's POV, her leaning in over him with the
        # two guys at the wall behind her (Hidden POV: the guy on the right); 02 kissing, his hand on
        # her ass; 03 (Exhibitionism + red only) he grabs, her bottoms slip aside, her eyes open.
        $ enter_cinematic_mode()
        if d2_kiss_red:
            scene cg ch01_d2_kiss_red_01
            with dissolve
            $ lc_pov_begin("d2_pool_kiss_stranger_red")
        else:
            scene cg ch01_d2_kiss_white_01
            with dissolve
        "She leaned over me, hair spilling off one shoulder, and smiled like she knew exactly what she was doing."
        if d2_nts_kiss:
            "She didn't check whether they were still watching. She didn't have to. She checked whether I'd noticed they were watching."
            "I had. I put my phone face down on the cushion."
        "Behind her, both guys at the wall had stopped pretending to talk to each other."
        if d2_kiss_red:
            $ lc_pov_end()
        if d2_kiss_red:
            scene cg ch01_d2_kiss_red_02
            with dissolve
        else:
            scene cg ch01_d2_kiss_white_02
            with dissolve
        "Without saying anything, she leaned in and kissed me."
        "I kissed her back and let one hand settle firmly on her ass."
        "[girlfriend_name] made a small surprised sound against my mouth."
        $ d2_kiss_slip = d2_lane == "exhibitionism" and d2_kiss_red
        if d2_kiss_slip:
            "She didn't pull away. She pushed back into my hand instead."
            "So I squeezed."
            scene cg ch01_d2_kiss_red_03
            with dissolve
            "My fingers sank in, and the red bikini, already barely there, slid right off to one side."
            "[girlfriend_name]'s eyes flew open mid-kiss. Neither of us moved."
            "Up on her knees like that, there was exactly one direction it was all on show: straight back at the wall."
            gf "...[player_name]. My bottoms."
            mc "I know."
            gf "They can see. Like, all of it."
            mc "I know. Want me to fix it?"
            "Her lips were still brushing mine. She didn't answer right away."
            gf "...In a second."
            "She counted to about three under her breath before she reached back and tugged the red fabric into place."
        $ exit_cinematic_mode()
        scene bg ch01_pool_day
        with dissolve

        "When we separated, Maya was staring at us. [friend_name] had suddenly become very interested in his drink. The strangers had seen everything."

        if d2_lane == "exhibitionism":
            if d2_kiss_slip:
                "[girlfriend_name]'s face was burning, but she still glanced at the wall once more before she looked back at me."
                maya "Hi, sorry, we're all still here. And I saw a lot more of you than I signed up for, babe."
                gf "Oh my God. It slipped! It just slipped. Nobody asked you to look, Maya."
                maya "It slipped for, like, three whole seconds. I counted. So did they."
                $ set_story_value("ch01_d2_pool_attention", "couple_display_slip")
            else:
                "[girlfriend_name]'s face warmed, but she glanced toward the strangers once more before looking back at me."
                maya "Hi, sorry, we're all still here. Just so you know. All of us."
                gf "Oh my God. Nobody asked you to watch, Maya. You could've, like, looked somewhere else?"
                maya "You did it right in front of me! Where was I supposed to look, at [friend_name]?"
                $ set_story_value("ch01_d2_pool_attention", "couple_display_open")
        elif d2_nts_kiss:
            "[girlfriend_name] stayed where she was for a moment, forehead against mine."
            gf "They're still looking."
            mc "I know."
            gf "...Do you mind?"
            "I thought about it longer than I should have needed to."
            mc "No. That's the weird part again."
            "She smiled against my cheek like I'd given the right answer to a question she hadn't asked out loud."
            $ set_story_value("ch01_d2_pool_attention", "couple_display_nts")
        else:
            "[girlfriend_name]'s face went pink the moment she remembered we had an audience."
            mc "Not that I'm complaining, but... what was that for?"
            gf "I don't— I just wanted to? Like, I just really wanted to. And they were staring, and it was getting weird, so."
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
        if get_story_value("ch01_d2_pool_attention") == "couple_display_nts":
            maya "That kiss was cute. Those two guys at the wall thought so too. You saw them, right?"
            mc "I saw them."
            maya "And you just... let them have the show."
            think "I hadn't thought of it like that. I hadn't stopped it, either."
        else:
            maya "[girlfriend_name] keeps checking whether you're still in the room. You're standing right next to her, and she keeps checking."
            think "Was she? I hadn't seen her do it once, and I'd been standing right there."
        maya "Just look at her once in a while. Like, actually look. That's it, that's the whole speech."
        mc "That's the whole speech?"
        maya "I had a longer one. You looked like you were going to throw up, so I cut it."

        "Back at the pool, [friend_name] glanced toward the path we'd disappeared down."
        friend "That was not about drinks. Nobody needs help carrying four drinks."
        gf "Yeah, no, I noticed. She didn't even pretend very hard."
        friend "She does this, apparently. I met her today, and I already know she does this."
        gf "What, kidnaps people's boyfriends?"
        friend "Interrogates them. She asked me about my sunglasses for ten minutes. Where I got them, why, whether I sleep in them."
        "[girlfriend_name] laughed despite herself."
        gf "Does he always get this quiet? Like, when he's stuck in his head about something? Because I can't tell if it's me or if it's just... a him thing."
        friend "Sometimes, yeah. Since college. He goes quiet, and then like two days later he tells you what it was, like it's no big deal. I wouldn't— I mean, I really wouldn't assume it's you."
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
        maya "For science. Come on, who am I going to tell? [friend_name]? He'd pass out."
        "[girlfriend_name] laughed, embarrassed, and glanced toward the strangers."
        maya "So... want to give them something to look at? He's staring anyway, babe. Might as well give him something worth staring at."
        "[girlfriend_name] looked toward the villa, where I'd gone, then back at Maya."
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
        maya "We'll go. You two keep the pool. Babe, if you feel like doing that again while I'm gone, the guys down there would not complain. Encore. I'm just saying."
        maya "[friend_name], you're carrying. Come on, up."
        friend "Why am I always the one carrying? I'm coming, I'm coming."
        "Maya caught [friend_name] by the arm and steered him toward the villa, leaving [girlfriend_name] and me beside the pool."
        # Ryan's thoughts (B3): the Day One carry thought, if he kept it. Otherwise nothing extra.
        if lc_thought_kept("ch01_d1") == "d1_julian_carry":
            think "Last night he'd carried her in from the car while I held the keys. Today he got the drinks, and I got to stay right here with her. I'd take that trade every time."
        "[girlfriend_name] shook her head at Maya's back, red to the ears, and didn't so much as glance at the wall. Once they were gone, she leaned into me instead."
        gf "I really like her. Like, I didn't expect to like her this much."
        mc "Good. I was a bit nervous about that, after yesterday. You had about eleven questions about her."
        gf "That was due diligence. That's different. I was being thorough."
        mc "No, you were. More than me. I've known her for years and I couldn't tell you her middle name."
        "She kissed my shoulder, still visibly embarrassed whenever she remembered the audience at the wall."
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
        friend "Because if I can't see it, it can't see me! I don't know! I panicked!"
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

        "[girlfriend_name] folded her arms across herself, then instinctively rushed behind [friend_name] and clung to his back, using him to shield herself from the guys at the wall."
        "[friend_name] went rigid with surprise, keeping his hands clear and his eyes turned away."
        gf "Don't look!"
        friend "I'm not! I'm looking at the— there's a tree. I'm looking at the tree."
        gf "Where's my top?! Can you see it?"
        friend "Okay, okay. Stay behind me. I'll— I'll find it, just stay behind me."

        "[friend_name] spotted the bikini top floating several feet away."
        friend "It's over there. By the steps."
        gf "GET IT!"
        friend "Why me?! I can't look at anything!"
        gf "[friend_name!u]!"

        "[girlfriend_name] stayed tucked behind [friend_name] as he edged toward the floating top, still holding on to his shoulders."
        "Over his shoulder, she caught sight of the strangers at the wall."
        "They were staring."
        gf "Oh my God. Oh no."
        friend "What? What now? Is it the bee?"
        gf "No, the guys. They saw. They definitely saw."
        friend "Then don't look at them. That's what I'm doing. It's working great."
        gf "I already looked!"

        "Maya didn't bring it up again on the walk back. She just handed me the heavier drinks."
        "Maya and I rounded the corner carrying the drinks."
        "Then I stopped."

        $ enter_cinematic_mode()
        scene cg ch01_d2_pool_top_accident
        with dissolve

        "[girlfriend_name] was clinging to [friend_name]'s back in the pool, hiding behind his shoulders while he kept his hands away from her."
        "Her bikini top floated several feet away. The strangers from earlier were still watching."
        "I had arrived at the exact moment that explained the least."
        # Door A echo (sc 15 knot): one line per answer; nothing plays when unset (old saves).
        if get_story_value("ch01_d2_knot_response") == "fixed":
            think "I'd tied that knot again myself an hour ago. Double. Apparently that meant nothing to a bee."
        elif get_story_value("ch01_d2_knot_response") == "told":
            think "I'd told her it was coming loose, and she'd fixed it. It hadn't made any difference at all."
        elif get_story_value("ch01_d2_knot_response") == "watched":
            think "I'd watched that knot slip all afternoon and said nothing. I just hadn't pictured it going like this."
        elif get_story_value("ch01_d2_knot_response") == "touched":
            think "An hour ago I'd had my hands all over her and left that knot exactly how it was. I hadn't been thinking about the knot."

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

        "[girlfriend_name] looked straight at me after that, still mortified, waiting for me to say something. I stood there holding the drinks and didn't."
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
        "She darted behind Maya and clung to her back, using her friend as a shield from the strangers at the wall."
        "Maya steadied herself, startled, then turned her attention toward the floating top."
        maya "I've got you. Stay behind me."
        "The strangers they had been teasing moments earlier were still watching."

        "[friend_name] and I returned with the drinks to find [girlfriend_name] still hiding against Maya's back while Maya tried to reach the floating top."
        "[girlfriend_name] saw us, let go of Maya, and sank lower into the water with her arms across herself."
        maya "So. There was a bee."
        gf "Don't. Don't tell it like that."
        maya "I'm explaining! It's a very short story!"
        "There was no mystery about what had happened. Maya had seen the whole thing."
        # Door A echo (sc 15 knot): one line per answer; nothing plays when unset (old saves).
        if get_story_value("ch01_d2_knot_response") == "fixed":
            gf "And you'd even fixed it earlier! You tied it yourself, and it still came off. That's so unfair."
        elif get_story_value("ch01_d2_knot_response") == "told":
            gf "And I retied it! [player_name] told me it was loose and I retied it, so this isn't even my fault."
        elif get_story_value("ch01_d2_knot_response") == "watched":
            gf "Wait, why don't you look surprised? You saw it was loose earlier, didn't you?"
            mc "...Maybe a little."
        elif get_story_value("ch01_d2_knot_response") == "touched":
            gf "Don't look at me like that. You were right behind me earlier, you could've fixed it."
            mc "I was busy."
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
        "I kept myself between her and the wall as I moved toward the floating top."
        "She let go just long enough for me to retrieve it."
        # Door A echo (sc 15 knot): one line per answer; nothing plays when unset (old saves).
        if get_story_value("ch01_d2_knot_response") == "fixed":
            gf "You literally fixed it this afternoon. Double knot and everything. It didn't even matter."
        elif get_story_value("ch01_d2_knot_response") == "told":
            gf "You even told me it was loose. I fixed it! I fixed it properly!"
        elif get_story_value("ch01_d2_knot_response") == "watched":
            gf "That's why you were staring at me earlier! You saw it coming, didn't you? You're terrible."
        elif get_story_value("ch01_d2_knot_response") == "touched":
            gf "You were right there earlier. Your hands were literally right there. And you just left it."
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

        gf "You're being quiet. You're doing the quiet thing. Babe, can you just— say something? Anything?"

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
                mc "Well, he did jump in first. And I was off carrying four drinks, so I don't think either of us gets a medal."
                friend "In my defense, the bee had a plan, and I didn't. I just reacted."

            "[d2_pool_honest_text]":
                $ apply_choice("ch01_d2_pool_honest_jealous")
                $ set_story_value("ch01_d2_pool_response", "honest_jealous")
                mc "I believe you. I still didn't like walking in on it."
                gf "That's... yeah. I wouldn't have liked it either."
                mc "I'm not blaming you. I just— I'm saying it now so I'm not weird about it later."
                gf "I know. I know you're not. I'd way rather you just say it than, like, sit on it all night."
                "She squeezed my hand once before letting go."

            "[d2_pool_accuse_text]":
                $ apply_choice("ch01_d2_pool_accuse")
                $ set_story_value("ch01_d2_pool_response", "accused")
                mc "I don't know. It just looked... convenient."
                "[girlfriend_name] stared at me."
                gf "Are you serious right now?"
                mc "No, I— I don't know. I'm saying what it looked like."
                gf "And I'm telling you what happened. There was a bee, and I panicked, and I wasn't— God, [player_name]. I wasn't trying to do anything."
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
        gf "Not the bee. Everything. The whole afternoon, like, all of it."

        "She lowered her voice."
        gf "The strings thing was on purpose. Like, I want you to know that part was me."
        mc "What strings thing?"
        gf "My bottoms. I pulled them up. Higher. While they were looking. Maya asked if I wanted to, and I said yes."
        "She glanced toward the strangers again, then back at me."
        gf "But that? The top?"
        gf "That was so not on purpose. I need you to know that."

        mc "I know. I know it wasn't."
        "Some of the tension left her shoulders."

        gf "You saw them looking before you left."
        mc "Yeah. Kind of hard to miss."
        "She searched my face, like the answer might already be on it."
        gf "I kept thinking about it after you went inside. What if you came back and it was weird?"
        mc "It's not weird. I, um. I kind of liked it, actually. Knowing they were looking at you."

        "[girlfriend_name]'s embarrassment didn't disappear, but the small smile that followed belonged to me."
        gf "Okay. Good."
        gf "Because I think I liked that part."
        "She immediately covered her face for half a second."
        gf "Not the losing-my-top part."
        mc "Right. Not that part."
        gf "Very much not that part. That part can go in the trash forever."

        "Maya called something unhelpful from the pool. [girlfriend_name] ignored her and stayed beside me."
        "She didn't move from my side until Maya climbed out and dripped on both of us on purpose."
        $ set_story_flag("ch01_d2_exhibition_pool_shared_with_ryan")
    else:
        "Once [girlfriend_name] had retied her top, she stayed close enough that our shoulders kept touching."
        "The strangers had seen more than either of us intended."
        "Maya spent the next five minutes trying to convince [friend_name] that the bee had already left."
        friend "That's exactly what the bee wants me to think."

    $ set_story_value("ch01_d2_route_lane_post_pool", ch01_d2_route_lane())
    $ set_story_flag("ch01_d2_scene_18_complete")
    scene black
    with fade
    call lc_part_card("day2", 3)
    jump ch01_day2_scene_19_change_for_evening


label ch01_day2_scene_19_change_for_evening:

    # Post-pool decompression. Maya leaves before sunset so the route-specific
    # Ryan/Leia conversation can happen without an audience.
    scene bg ch01_pool_lounge
    with dissolve

    "The pool incident took most of the energy out of the afternoon."
    # Flow: after "It just looked... convenient" nobody laughs it off.
    if get_story_value("ch01_d2_pool_response") == "accused":
        "For a while the four of us stayed around the table, drinking water and drying off. Maya and [friend_name] did most of the talking. [girlfriend_name] sat at the far end and didn't look at me much."
    else:
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
    "[friend_name] still hadn't come back down."

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
        "I glanced up at the windows anyway. I couldn't help it."
        gf "I checked. Twice. Eyes down here, babe, not up there."

        scene cg ch01_d2_love_pool_oral_02
        with dissolve

        "What followed was quick and reckless, and she'd picked the one spot the rest of the villa couldn't see."
        "When we finally pulled ourselves back together, [girlfriend_name] was trying very hard not to look as pleased with herself as she obviously was."

        $ exit_cinematic_mode()
        scene bg ch01_d2_sunset
        with dissolve

        gf "Nobody saw. Just so you know."
        mc "You've said that about four times now. It's kind of cute."
        gf "Because nobody did! I'm just making sure you know."

        "We sat together at the edge of the pool while the light faded."
        gf "Today was actually really nice, you know? Like, weird, but nice."
        mc "Even the bee?"
        gf "The bee doesn't count. The bee's not part of today."
        mc "And Maya?"
        gf "I like her. I really like her. Is that weird? I've known her one day."
        mc "I'm really glad. I was kind of hoping you would."
        gf "And..."
        "She bumped her shoulder into mine."
        gf "I like this."
        mc "This, as in the trip?"
        # Subtle Day Two tint (lc_leia_tint): shy by default; the stat furthest over its bar colours the line.
        $ d2_tint = lc_leia_tint(d2_lane, lane_scene=True)
        if d2_tint == "love":
            gf "Us, babe. I like us. I like us so much, like, a lot. Is that a weird thing to say on a holiday?"
        elif d2_tint == "exhibitionism":
            gf "Us, dummy. I like us. And maybe— okay, maybe a little bit the being-outside part, too."
        else:
            gf "Us. I— I like us. That's all."
        "She kept her eyes on the water while she said it, and her shoulder stayed against mine."

        $ set_story_value("ch01_d2_sunset_response", "love_connected")
        $ set_story_flag("ch01_d2_love_sunset_oral")

    elif d2_lane == "exhibitionism":
        "[girlfriend_name] sat beside me, knees drawn up, still thinking about the pool."

        # Flow: this lane is read after the pool, so it can follow any split. She only brings up
        # what happened on this save's split (ch01_d2_split); old saves keep the strings version.
        # Reads what this save actually saw at the wall (ch01_d2_pool_attention); old saves without
        # it keep the split-based fallback.
        $ d2_pool_att = get_story_value("ch01_d2_pool_attention", "")
        if d2_pool_att == "couple_display_slip":
            gf "Okay, so. The pool. When I kissed you in front of those guys."
            mc "You started that."
            gf "I know I started it! And then you grabbed my ass, and my bottoms slipped, and they saw everything, and I didn't fix it. Not straight away."
            mc "You counted to three."
            gf "I counted to three. That's the part I keep thinking about."
            mc "The part where they were watching?"
            gf "Knowing they were looking. Knowing you knew they were looking."
        elif d2_pool_att.startswith("couple_display") or (not d2_pool_att and get_story_value("ch01_d2_split") == "ryan_leia_julian_maya"):
            gf "Okay, so. The pool. When I kissed you in front of those guys."
            mc "You started that."
            gf "I know I started it! And then you grabbed my ass, and they were all watching, and I didn't hate it. That's the part I keep thinking about."
            mc "The part where they were watching?"
            gf "Knowing they were looking. Knowing you knew they were looking."
        elif d2_pool_att == "leia_stretched_without_ryan" or (not d2_pool_att and get_story_value("ch01_d2_split") == "ryan_maya_leia_julian"):
            gf "Before the bee. When I stretched by the table? One of those guys watched me the whole time."
            mc "I didn't even see that."
            gf "I know. You were on your phone. And I kind of liked it anyway. Them looking."
        else:
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
        gf "It's just... thinking about it now, it's different. I don't know."
        mc "Different how?"
        gf "...You know how."

        mc "So my girlfriend's secretly an exhibitionist."
        gf "I am not! I'm not. I'm just... curious."
        "I looked at her."
        gf "...Shut up."

        mc "I mean, if it turns you on, it turns you on. I'm not going to make it weird."
        mc "If it helps, I'm the one sitting here getting kind of worked up just hearing about it."

        "She laughed, and some of the red went out of her face."

        if get_story_value("ch01_d2_split") == "ryan_leia_julian_maya":
            gf "I think the part I liked most was, like... that it was you. That you were right there, and you knew."
        elif get_story_value("ch01_d2_split") == "ryan_maya_leia_julian":
            gf "I think the part I liked most is, like... telling you now. That you know."
        else:
            gf "I think the part I liked most was, like... that I got to come back and tell you. That you'd know."

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

        # Told path (Leia's errand): one lead-in line; the soft-gate menu below is unchanged.
        if get_story_value("ch01_d2_leia_told") == "told":
            gf "So I told you my thing. Can I ask you something now? It's only fair."
        else:
            gf "Hey. Can I ask you something?"
        mc "Yeah, sure. What's up?"
        gf "Are we okay?"
        "I looked at her."
        # Flow: Ryan's mood when she left on her errand (ch01_d2_errand_ryan_mood, the café test); a
        # brushed-off confession counts as distant. Old saves keep the original line.
        if get_story_value("ch01_d2_errand_ryan_mood") == "warm" and "ch01_d2_confession_brush" not in choice_history:
            gf "Because you've been really sweet today, and I still keep feeling like you're, like, a step behind your own face. You're here, but you're not all the way here."
        else:
            gf "Because every time I look at you today, you're, like, somewhere else. You're here, but you're not here."
        gf "And if something's bothering you, you can just tell me. Even if it's dumb. Especially if it's dumb."

        # Café incident payoff (scene 11b): Maya's "out loud" advice only exists in the worried talk.
        if get_story_value("ch01_d2_overheard_response") == "pretended" and get_story_value("ch01_d2_overheard_talk") == "worried":
            think "Out loud. Tonight. I'd stood behind a plant and heard Maya tell her to ask me exactly this. It should have made answering easier. It made it feel like a script."
        elif get_story_value("ch01_d2_overheard_response") == "owned":
            think "I'd told her at the café I'd explain later. This was later."

        $ d2_sunset_connect_text = format_choice("ch01_d2_sunset_connect", "Tell her the truth.")
        $ d2_sunset_partial_text = format_choice("ch01_d2_sunset_partial", "I've just been in my own head.")
        $ d2_sunset_ignore_text = format_day2_risk_choice("ch01_d2_sunset_ignore_gate", "I'm fine.", severity="soft")

        menu:
            "[d2_sunset_connect_text]":
                $ apply_choice("ch01_d2_sunset_connect")
                $ set_story_value("ch01_d2_sunset_response", "opened_up")

                mc "No. I'm not really okay."
                "[girlfriend_name] waited."
                # Flow: the pool and [friend_name] only come up if her top came off with him there.
                if get_story_value("ch01_d2_pool_incident") == "leia_julian_bee_top_off":
                    mc "I slept badly, and then the pool thing looked insane for about three seconds, and I think I've been... jealous? Kind of? And instead of just saying any of that, I've been acting like an idiot all day."
                    gf "Babe. Nothing happened with [friend_name]. You know that, right?"
                else:
                    mc "I slept badly, and then I spent the whole day stuck in my own head about stuff I couldn't even explain to myself. And instead of just saying any of that, I've been acting like an idiot."
                    gf "Babe. You could've just said that. You know that, right?"
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

    # Things Ryan noticed (docs/NOTICES.md): every lane reaches this point after its sunset talk.
    # One extra, scored option when a Day Two morning notice was made; not after "I'm fine".
    if lc_noticed_any("d2_notice_bed_hand", "d2_notice_breakfast_smile") and not get_story_value("ch01_d2_ntr_soft_gate", False):
        $ d2_sunset_noticed_text = format_choice("ch01_d2_sunset_noticed", "Tell her what you noticed this morning.")
        menu:
            "[d2_sunset_noticed_text]":
                $ apply_choice("ch01_d2_sunset_noticed")
                $ set_story_value("ch01_d2_sunset_noticed", True)
                if lc_noticed("d2_notice_bed_hand"):
                    mc "This morning, when I got up. Did you know your hand went straight over to my side of the bed? Palm up, right at the edge, like you were looking for me."
                else:
                    mc "At breakfast, while [friend_name] was busy defending his movie, you just looked over at me and smiled. Like nobody else was even at the table."
                if d2_lane == "love":
                    gf "Wait, you saw that? Oh my God, I didn't even know I did that."
                    gf "No, don't make it weird, I like that you saw it. I really, really like that you saw it."
                    mc "I notice most of what you do. I just don't usually say it out loud."
                    gf "Then say it out loud more. All of it, every dumb little thing. I want the whole list."
                    "She tucked herself under my arm and stayed there while the last of the light went."
                elif d2_lane == "exhibitionism":
                    gf "You were watching me that closely, huh?"
                    mc "Hard not to."
                    gf "Good. I like knowing it's you watching. That's my favorite part, actually."
                    "She bumped her knee against mine, very pleased with herself."
                else:
                    gf "...You noticed that?"
                    mc "I notice you. I've just been bad at saying it today."
                    gf "Then say that stuff. That's exactly the stuff I want to hear from you."
                    "She leaned her head on my shoulder, and for a minute it was just the two of us again."
            "Keep it to yourself.":
                pass

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

        "She changed right there in front of me, still smiling, and didn't turn her back to do it."

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
                gf "Yeah? Okay, yeah, that one. See, this is why I ask you. Good call, babe."
                "She held it up against herself one more time and went off to change, humming something."

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
    "Maya asked everyone for their favorite part of the trip so far, then rejected [friend_name]'s answer because it was his new shirt. He went a bit red and insisted it was a genuinely good shirt."
    "[girlfriend_name] and Maya started planning what they wanted to see tomorrow."
    "[friend_name] complained that I still couldn't order from a menu in under ten minutes, which he's been saying since college. Maya immediately joined him."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if get_story_value("ch01_d2_ntr_soft_gate", False):
        "[girlfriend_name] laughed with Maya and argued with [friend_name] and had a good time, with no edge in any of it."
        "What changed was smaller: she stopped checking whether I was following every moment. I let her stop, and I didn't really register it until somewhere around dessert."
    elif d2_lane == "exhibitionism":
        "Every so often [girlfriend_name] caught my eye across the table and smiled like we were carrying a private conversation nobody else could hear."
    else:
        "[girlfriend_name] and I fell into the small habits that came with four years together: passing the right sauce before the other asked, trading bites, finishing each other's complaints."

    # Ryan's thoughts (B3): the Day One dinner thought, if he kept it. Otherwise nothing extra.
    if lc_thought_kept("ch01_d1") == "d1_dinner_stranger":
        if get_story_value("ch01_d2_ntr_soft_gate", False):
            think "Every time a waiter passed with a full tray, I thought about last night. Mostly about where her eyes had gone afterwards."
        elif d2_lane == "exhibitionism":
            think "Last night some guy went out of his way to tell her the dress still looked incredible. Tonight, every time she caught my eye across the table, I wondered who else in here had noticed her. I didn't mind one bit."
        else:
            think "Every time a waiter came past with a full tray, I watched it all the way to the next table. Nobody was spilling anything on her tonight, not if I could help it."

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
        "[friend_name] noticed. He caught himself almost straight away and went to look anywhere else, already going red, but [girlfriend_name] caught his eye before he got there."

        $ exit_cinematic_mode()
        scene bg ch01_d2_dinner
        with dissolve

        "She didn't look away."
        "Then she gave him a tiny wink."

        "[friend_name] looked genuinely surprised."
        "He did not wink back."
        "[girlfriend_name] simply sat down and continued eating."

        "It was over before I'd even put my glass down, less than a second from start to finish, and it was still long enough that I knew I hadn't imagined it."

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
        "I didn't say anything at the table. I didn't say much of anything for the rest of dinner, and Maya talked enough for both of us."
        "[friend_name] did not encourage the moment either. If anything, he became more careful about where he looked."
        "[girlfriend_name] never checked whether I had noticed."
    elif get_story_value("ch01_d2_dinner_reach") == "smiled_at_ryan":
        "Later [girlfriend_name] caught me looking again."
        "She gave me a small, satisfied smile, and neither of us said a word about it."
    else:
        "Dinner stayed easy. Maya and [friend_name] did most of the arguing while [girlfriend_name] and I enjoyed the show."

    "By the second round, everybody was noticeably looser."

    friend "There's more back at the villa, if anyone wants. No pressure. There's just, you know, a lot."
    maya "That sounds really irresponsible."
    friend "You don't have to come. I'm just saying it's there."
    maya "I didn't say no, [friend_name]. Don't put words in my mouth."

    "We paid, walked back to the villa together, and let the night follow us home."

    # Leia's errand posts (ch01_day2_feed.rpy): released side by side, only the lane's matching
    # ones come out, one banner. A save without the errand gets none.
    if get_story_value("ch01_d2_errand_lane"):
        $ lc_phone_set_story_time("21:40")
        $ lc_feed_release("d2_feed_love_poolguy", "d2_feed_love_shop", "d2_feed_exhib_poolguy", "d2_feed_exhib_poolguy_linger", "d2_feed_ntr_clip", "d2_feed_ntr_clip_linger")
        "Somewhere on the walk my phone buzzed in my pocket. [LC_FEED_APP_NAME]: new posts from around the resort. I left it for later."
        $ lc_phone_clear_story_time()

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
        think "He'd carried one sentence of mine around all day, neck and all. I felt a bit guilty about that, and really fond of him."
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
    maya "It explains nothing. You know nothing about it. His name was Jake, and it was beautiful."
    gf "Jake. Oh my god, of course it was a Jake."
    maya "Excuse me? What's wrong with Jake?"
    gf "Guys with J names are red flags. Everybody knows that. Jake, Josh, Jason, Jordan, every single one of them has a story where you go, wait, he did what?"
    if friend_name[:1].upper() == "J":
        "There was a pause, and then every head at the table turned to [friend_name] at exactly the same time."
        friend "I'm literally sitting right here. I can hear all of this."
        maya "Huh. [friend_name]. With a J."
        friend "It's a coincidence. It's a really common letter. Half the alphabet is basically J if you think about it."
        mc "Hey, he's not a red flag. The worst thing he's ever done is one parking ticket, and I was in the car for that, so..."
        "[friend_name] went pink and started explaining it to the whole table."
        friend "It was a loading zone. The sign was behind a tree, you couldn't see it until you were right next to it, and he said it looked fine. So if it's a red flag, it's, um. It's kind of a shared one."
        maya "Jake would never have dragged his friend down with him like that."
    else:
        maya "Jake was a perfectly nice red flag, thank you. He made me breakfast twice."
        gf "Twice. In a whole holiday."
        maya "It was a short holiday!"

    $ set_story_flag("ch01_d2_maya_stays_for_drinks")
    $ set_story_flag("ch01_d2_scene_25_complete")
    jump ch01_day2_scene_26_game_rules


label ch01_day2_scene_26_game_rules:

    "The harmless questions lasted long enough for everyone to get comfortable."

    maya "Enough warm-up. Dating questions."
    friend "And here we go. I knew it was coming."
    maya "Never have I ever had a crush on someone I shouldn't have."

    "Maya drank without hesitation."
    "[friend_name] suddenly found the ice in his glass very interesting and didn't look up from it."

    maya "Never have I ever checked someone out while I was already in a relationship."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    if d2_lane == "love":
        "[girlfriend_name] took a drink and looked at me sheepishly."
        gf "Don't look at me like that. People are allowed to be cute. I'm only noticing, I'm not, like, doing anything about it."
        mc "I'm sitting right here, babe."
        gf "I know, I know. You're cute too. You're— I mean, it's not even a competition. You'd win."
        "She leaned into my side like that settled it."
    elif d2_lane == "exhibitionism":
        "[girlfriend_name] took a drink while looking straight at me."
        if get_story_flag("ch01_d2_exhibition_sunset_shared"):
            "After everything we'd said at sunset, she didn't need to explain it to me."
        else:
            "She didn't need to explain it to me."
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

    # Subtle Day Two tint (lc_leia_tint): shy by default; the stat furthest over its bar colours the line.
    $ d2_tint = lc_leia_tint(d2_lane) if d2_lane != "ntr_risk" else "shy"
    if d2_tint == "exhibitionism":
        gf "I'm in."
        "She said it fast, then glanced at me with a tiny grin she clearly hadn't meant to let out."
    elif d2_tint == "sharing":
        gf "Well, I'm not letting Maya do this on her own. I'm in."
        "She looked at me when she said it, like it was something the two of us were signing up for together."
    else:
        gf "I'm in. Wait, what counts as something? Like, does a hair tie count? ...No, okay. I'm in."
    mc "Yeah. I'm in too. I really should've worn more layers for this."
    friend "I'm outvoted, aren't I. I can feel it."
    maya "Completely outvoted. Welcome."

    $ set_story_flag("ch01_d2_strip_penalty_agreed")
    $ set_story_flag("ch01_d2_scene_26_complete")
    jump ch01_day2_scene_27_game_escalates


label ch01_day2_scene_27_game_escalates:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)

    maya "Fine. Burning question. Who here has found someone else in this room attractive?"

    "Nobody laughed this time."
    "[girlfriend_name] stared at Maya."

    gf "That's not even Never Have I Ever."
    maya "Burning questions! I literally just made the rule."
    gf "I'm not answering that."
    maya "Then drink."
    gf "No! Then it's an answer. Drinking is an answer."
    maya "Then you know the rule, babe. No answer, no drink, something comes off. I made it up five minutes ago and I'm already so proud of it."

    "[girlfriend_name] looked down at herself, then stood."

    # Flow: what comes off is what she wore to dinner (ch01_d2_dinner_outfit_id).
    if get_story_value("ch01_d2_dinner_outfit_id") == "d2_loose_low_cut":
        "She pulled her top over her head, stepped out of her skirt, and stood there for a second in just her bra and panties, cheeks burning."
    elif get_story_value("ch01_d2_dinner_outfit_id") in (None, "resort_dinner_dress"):
        "She slipped out of her dinner dress and stood there for a second in just her bra and panties, cheeks burning."
    else:
        "She slipped out of what she'd worn to dinner and stood there for a second in just her bra and panties, cheeks burning."
    gf "Okay. Okay, nobody say anything. Literally nobody."

    if d2_lane == "exhibitionism":
        "Before she sat back down, she checked my face."
        "She was pink all the way down her neck, and under the embarrassment I could see a little spark of something else."
    elif d2_soft_gate:
        "She didn't look over at me first. I only realized that afterwards."
        "She simply folded her clothes beside her and sat down."
    else:
        "She sat back down and scooted straight over to my side again, like being next to me made it better."

    # Ryan's thoughts (B3): the Day One sofa thought, if he kept it. Otherwise nothing extra.
    if lc_thought_kept("ch01_d1") == "d1_sofa_glance":
        if d2_lane == "exhibitionism":
            think "Last night on the sofa she'd checked where [friend_name] was looking before she settled. Tonight she checked me first. I liked that a lot more than I could explain."
        elif d2_soft_gate:
            think "Last night on the sofa she'd checked where [friend_name] was looking before she settled. Tonight she didn't check where anyone was looking."
        else:
            think "Last night she'd checked where [friend_name] was looking before she settled against me. Tonight she didn't check anything. She just came straight back to my side."

    $ set_story_value("ch01_d2_nhie_leia_clothes", "bra_panties")

    friend "I, uh. Wow. Okay. I genuinely didn't think the rule was real, I thought it was a bit."
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

    friend "That's, um. That's a really specific question, and you're asking it like you already know the answer, which you don't. I'm not discussing it."
    maya "Then drink."
    friend "No, because then it's a yes."
    maya "Then shirt. Off. Rules."

    "He went red, didn't look at anyone, got the shirt caught on his sunglasses on the way over his head, and finally dropped it on the arm of the sofa."

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
        "I could feel my ears going warm, because I knew exactly what she was thinking about."
    elif d2_soft_gate and lc_stat("exhibitionism") >= LC_T["d2_game_drinks"]:
        "[girlfriend_name] drank after a pause."
        "She did not explain."
    else:
        "[girlfriend_name] did not move."

    maya "[girlfriend_name]. This one's for you."
    maya "Never have I ever enjoyed attention from someone I knew I probably shouldn't."

    "[girlfriend_name]'s expression changed."
    if d2_soft_gate:
        "Before she said anything, her eyes came to me. It was the first time she'd looked my way since the game started."
    else:
        "Before she said anything, her eyes came to me."

    # Door B (program design Part A): Ryan only signals. The lane branch below plays as before;
    # ch01_d2_dare_signal only changes her lines and my narration inside it. Shrug = today's text.
    $ d2_dare_nod_text = format_choice("ch01_d2_dare_nod", "Nod, go on.")
    $ d2_dare_shrug_text = format_choice("ch01_d2_dare_shrug", "Shrug, your call.")
    $ d2_dare_lap_text = format_choice("ch01_d2_dare_lap", "Pull her onto your lap instead.")

    menu:
        "[d2_dare_nod_text]":
            $ apply_choice("ch01_d2_dare_nod")
            $ set_story_value("ch01_d2_dare_signal", "nod")
            $ lc_discovery_mark("d2_dare_door")
            "I gave her the smallest nod."

        "[d2_dare_shrug_text]":
            $ apply_choice("ch01_d2_dare_shrug")
            $ set_story_value("ch01_d2_dare_signal", "shrug")
            "I gave her a little shrug."

        "[d2_dare_lap_text]":
            $ apply_choice("ch01_d2_dare_lap")
            $ set_story_value("ch01_d2_dare_signal", "lap")
            $ lc_discovery_mark("d2_dare_door")
            "I hooked an arm around her waist and pulled her over onto my lap."
            "She came with a surprised little squeak and didn't try to get up."

    $ d2_dare_signal = get_story_value("ch01_d2_dare_signal", "shrug")

    if d2_lane == "love" and not d2_soft_gate:
        if d2_dare_signal == "nod":
            "She narrowed her eyes at me, and then she started laughing."
            gf "Not a chance, babe."
            "She leaned over and kissed me, quick and firm, before Maya could get a word in."
            maya "Oh, come on! He literally nodded at you! You're not even going to drink?"
            gf "I'm answering this one. No. I haven't."
            "She stayed in her bra and panties and reached for her water instead."
        elif d2_dare_signal == "lap":
            "She settled back against my chest and pulled my arms tighter around her."
            gf "No. Actually, no."
            maya "You can't just hide on his lap and say no! You're not even going to drink? Look at you two. It's disgusting."
            gf "I'm answering this one. No. I haven't."
            "She turned her head, kissed my jaw, and reached past me for her water."
        else:
            gf "No. Actually, no."
            maya "No? Not even a sip? Oh my God, you're so in love it's gross. Fine. I'll find one you'll drink for, babe. Just wait."
            gf "I'm answering this one. No. I haven't."
            "She stayed in her bra and panties and reached for her water instead."
    else:
        gf "I'm not answering that."
        maya "Then drink."
        gf "No. I'm not drinking for that one."
        maya "Then rules are rules, babe."
        "Maya didn't add anything. She propped her chin on her hand and waited, grinning."

        if d2_dare_signal == "lap":
            "[girlfriend_name] exhaled, sat forward on my knees and reached behind herself."
        else:
            "[girlfriend_name] exhaled and reached behind herself."

        if d2_lane == "exhibitionism":
            if d2_dare_signal == "nod":
                "She held my eyes the whole time she unclasped her bra."
                "Once it came away, she crossed both arms over her chest, but she couldn't keep the grin off her face."
                gf "You're enjoying this way too much."
            elif d2_dare_signal == "lap":
                "She looked back at me over her shoulder before unclasping her bra."
                "Once it came away, she crossed both arms over her chest and pulled mine up over them too, laughing at herself."
            else:
                "She looked at me before unclasping her bra."
                "Once it came away, she immediately crossed both arms over her chest."
                "She laughed at herself, a little breathless, and snuck another look at me over her arms."
        else:
            if d2_dare_signal == "nod":
                "She'd seen me nod. She didn't look at me again while she unclasped her bra."
            elif d2_dare_signal == "lap":
                "She unclasped her bra without leaning back into me."
            else:
                "She unclasped her bra without checking my reaction."
            "The moment it came away she crossed both arms tightly over her chest and hunched in a little, like that could make her smaller."

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
    friend "I'm going to look at the lamp now. I'm just— I'm going to look at this lamp for a while. It's a nice lamp."
    "[girlfriend_name] burst out laughing and folded forward over her knees."
    gf "It's a nice lamp. Oh my God. You're such a coward, [friend_name], I love it."

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
    "[girlfriend_name] couldn't stop giggling."
    gf "Then... pants? That's the rule, right, Maya? Pants, [friend_name]."

    friend "This game's rigged. I'm not complaining, I'm just— I'm noticing that it's rigged against me, specifically."
    maya "Yep. Totally rigged."

    "He stood up, red to the collar, kept his eyes on the floor, got out of his trousers as fast as he could and sat straight back down in his underwear."

    $ enter_cinematic_mode()
    scene cg ch01_d2_julian_underwear_reveal
    with dissolve

    "The whole room went quiet. Somebody's ice clinked in a glass, and that was the only sound."

    if d2_lane == "love":
        "[girlfriend_name] looked because everyone looked, gave a surprised little laugh, then turned back toward me."
    elif d2_lane == "exhibitionism":
        "[girlfriend_name] looked."
        "Then she realized I had noticed her looking and met my eyes with a tiny, mischievous expression."
        "After that she kept her eyes on me, not on him."
    elif d2_soft_gate:
        "[girlfriend_name] was still looking when I glanced over."
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

    "[friend_name] started to shake his head, then stopped halfway."

    maya "Oh my God. [friend_name]."
    friend "What? I didn't do anything."
    maya "You paused! Drink."
    friend "It wasn't a pause, I was thinking. You're allowed to think about a question. It's a weird question, so obviously you'd— no. I'm not drinking."
    gf "Then answer."
    "[friend_name] went another shade redder."
    friend "Also no. Not answering either."
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
    friend "You're not. I'm the one offering, so it doesn't count as kicking me out. I'm pretty sure that's how it works."
    maya "Still no. That's still kicking you out."
    friend "Seriously, take it. The sheets are clean, the fan actually works, and I'll just grab a blanket and sleep out here."

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

    "[friend_name] opened his mouth, shut it again, and looked at me like I might have a ruling on this."

    friend "I— okay. The couch is genuinely fine. It's a good couch."
    maya "[friend_name]."
    friend "And I'm not a rich boy. I've slept on couches. Some of them were basically floors."
    friend "Wait. Are you sure? Actually sure? You've had a lot to drink, and the room's still going to be there tomorrow, and so is the couch, so you could just decide then. I'm not putting a deadline on it. There isn't a deadline."
    maya "I told [girlfriend_name] this afternoon. Way before any of this. Come on."
    "[girlfriend_name] nodded at him, very seriously, like a witness."
    "He went red all the way to his ears."

    "Maya scooped her dress off the floor, caught [friend_name] by the wrist and started pulling him toward the corridor."

    maya "And bring water."
    friend "Water. Yes. Okay, I can— yeah. I can bring water."
    maya "Don't make it weird."

    "[friend_name] grabbed two bottles of water with his free hand and let her drag him away."
    "They disappeared into his room together."
    "He didn't look back at us once. I was fairly sure that was so we wouldn't see his face."

    $ set_story_value("ch01_d2_maya_sleeping", "julian_room_shared_bed")
    $ set_story_value("ch01_d2_julian_sleeping", "julian_room_shared_bed")
    $ set_story_flag("ch01_d2_maya_julian_share_room")

    "The bedroom door closed somewhere down the corridor."
    "For the first time since we'd come back from dinner, the villa was quiet."

    "Just me and [girlfriend_name]."

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())

    # Flow: what she's wearing follows the game (ch01_d2_nhie_leia_clothes), not only the lane: on the
    # Love lane after "I'm fine" at sunset she went topless too. Old saves (no value) keep the lane split.
    if d2_lane == "love" and get_story_value("ch01_d2_nhie_leia_clothes") != "panties_covering_chest":
        "[girlfriend_name] picked up her clothes, looked at them, then decided putting them back on for the walk upstairs was unnecessary."
        if get_story_value("ch01_d2_dare_signal") == "lap":
            "She stayed in her bra and panties and slid back onto my lap like she'd never left it."
        else:
            "She stayed in her bra and panties and came over to me."
    else:
        "[girlfriend_name] was still in her panties, both arms folded across her bare chest."
        "The game was over, and she still hadn't uncrossed them."

    gf "So. Well."
    mc "Yeah."
    gf "That got so out of hand. Like, really out of hand. When did it even get like that?"
    mc "I don't know. Somewhere around Maya getting naked. Like, all the way naked."
    gf "And [friend_name] took his sunglasses off. I didn't even know they came off."
    mc "Yeah. Honestly, I think that was the bigger shock."

    "[girlfriend_name] laughed, tired and tipsy."

    $ set_story_flag("ch01_d2_scene_29_complete")
    jump ch01_day2_scene_30_bedroom


label ch01_day2_scene_30_bedroom:

    $ d2_lane = get_story_value("ch01_d2_route_lane_dinner", ch01_d2_route_lane())
    $ d2_soft_gate = get_story_value("ch01_d2_ntr_soft_gate", False)
    $ d2_wink = get_story_value("ch01_d2_dinner_wink", False)
    $ d2_pool_suspicion = get_story_flag("ch01_d2_pool_suspicion")
    python:
        # End route: Leia's errand and its follow-ups never count tonight (CH01_D2_ERRAND_EXEMPT_CHOICES).
        d2_love_exhib_blend = ch01_d2_love_exhib_blend(d2_lane)

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
            think "Last night, in this same room, I'd told her I didn't hate people noticing her, and she'd made me promise we'd actually talk about it. We had, too, on the couch after [friend_name] went up."
        think "Tonight I couldn't even find the start of the sentence."
    elif d2_upstairs == "honest":
        "[girlfriend_name] came out of the bathroom with her hair half tied up, and for a second it was last night again: me standing in the middle of this room, her asking what was going on."
        think "I'd told her the carrying thing bothered me. She hadn't laughed, or made it a thing. She'd just put her arms around me and said she liked it when I told her stuff."
        think "I'd thanked her for it this morning. All day it had felt like the kind of thing you should say more than once."
        mc "You know you're kind of the best part of this trip, right?"
        gf "Kind of? Wow. Okay."
        "She stopped fussing with her hair and looked at me properly, the way she does when she's deciding not to tease me."
        gf "...You're the best part too, babe. Even the weird parts. Come here."
    elif d2_upstairs == "liked":
        "[girlfriend_name] caught me watching her from the bathroom doorway and gave me the same look she'd given me last night, right here, when I'd admitted I didn't hate people noticing her."
        think "She could've laughed at me. Or gone quiet and wondered what kind of guy says that."
        think "Instead she'd checked my face to make sure I meant it, and then actually sat me down and made me talk about it once [friend_name] had gone to bed."
        "She'd turned it into something we were both in on, and I still hadn't worked out how to tell her how glad I was about that."
        mc "We should do that more. Say the stuff out loud, I mean. Instead of me being all mysterious."
        gf "Oh my god. Are you quoting me to me?"
        "She laughed at herself before I could."
        gf "Yes. Obviously yes. Last night was a good start, but that was, like, the first episode. I want the rest of it, and you don't get to go all mysterious on me again."
        mc "I'll try. I'm not great at it yet, but I'll try."
        "She dropped onto the bed next to me and bumped her knee against mine, like we were still in on something."
    elif d2_upstairs == "swallowed":
        "[girlfriend_name] brushed her teeth with the bathroom door open, in the same doorway she'd stood in last night asking me what was going on."
        think "It's fine. Just a long day. That was what I'd told her, standing right about here."
        think "She'd believed me because I asked her to. A couple of times today I'd caught her looking at me and deciding not to ask."
        "I almost said something. Then she switched off the bathroom light, and the moment went with it."
    elif d2_upstairs == "snapped":
        "[girlfriend_name] picked her clothes up off the chair and folded them, carefully, without really looking at them."
        think "She'd folded the dinner dress like that last night too. Right after I told her to stay awake next time."
        # Scene 1 has Ryan apologize in the morning unless he pushed the dream away.
        if get_story_value("ch01_dream_response") != "withdrew":
            think "I'd apologized this morning, and she'd let it go. Mostly. Watching her fold that dress, I wasn't sure mostly was the same as all the way."
            if not d2_bed_strained:
                "When she was done, she sat down next to me, close enough that our knees touched. That part, at least, was all the way."
        elif d2_bed_strained:
            think "I hadn't apologized for that either."
        else:
            mc "Hey. What I said last night, up here. The staying awake thing. That was a crappy thing to say."
            gf "...Yeah. It kind of was."
            "She set the clothes down."
            gf "I know you didn't mean it like that. I just thought about it a few times today. That's all."
            mc "I'm sorry. I really am."
            gf "Thank you. Really."
            "She didn't make me say it twice. She came and sat next to me, close enough that our knees touched."

    # Subtle Day Two tint (lc_leia_tint): shy by default; the stat furthest over its bar colours the line.
    $ d2_tint = lc_leia_tint(d2_lane, lane_scene=True)
    if d2_tint == "love":
        "[girlfriend_name] pulled her hair loose, then leaned in and kissed my shoulder, like she'd been saving it up all night."
    elif d2_tint == "temptation":
        "[girlfriend_name] pulled her hair loose with one hand and scrolled her phone with the other, not really looking up."
    else:
        "[girlfriend_name] pulled her hair loose and let it fall, yawning into the back of her hand."

    # Maya's late DM (phone moment ch01_d2_maya_dm, docs/PHONE_MOMENTS.md). Optional and never
    # blocks: ignored, it runs out as "left on read" at the end of the day. Leia reacts here
    # only if he showed her before this line ends; the pick is scored once (Day Two file init).
    $ d2_dm_mood = ch01_d2_maya_dm_mood(d2_lane, d2_tint, d2_soft_gate, d2_wink, d2_pool_suspicion, d2_love_exhib_blend)
    $ lc_sfx("phone_notify")
    $ ch01_d2_maya_dm_offer(d2_dm_mood)
    "My phone lit up on the nightstand. Maya, texting from [friend_name]'s room."

    if get_story_value("ch01_d2_maya_dm") == "show":
        if d2_dm_mood == "love":
            "I'd tipped the screen toward [girlfriend_name]. She read it, laughed through her nose, and took the phone out of my hand to answer it herself."
            "Then she gave it back and tucked herself against my side."
            gf "I'm so glad it's you up here with me. Like, so glad. I don't say it enough."
            "She kissed my cheek and got very interested in the ceiling."
        elif d2_dm_mood == "exhib":
            "I'd tipped the screen toward [girlfriend_name]. She read it, grinned, and had the phone out of my hand before I could ask."
            mc "What did you tell her?"
            gf "Nothing bad! You can read it, I'm just not saying it out loud."
            "She handed it back with pink cheeks, very pleased with herself."
            gf "Everybody's going to know. Like, she's going to make sure everybody knows."
            gf "...I don't really mind that."
            if d2_love_exhib_blend:
                gf "And for the record, I'm really, really happy. With us, I mean."
        elif d2_dm_mood == "cool":
            "[girlfriend_name] glanced at the screen, typed a quick answer with one thumb and handed the phone back."
            gf "She's just drunk."
            "She was already looking at something else."
        else:
            "[girlfriend_name] read it over my shoulder and went pink."
            gf "Oh my god. She's so..."
            "She took the phone anyway, typed something short and gave it back face-down."
            gf "Don't read it out loud."
    elif get_story_value("ch01_d2_maya_dm") == "reply":
        "I sent Maya something short and put the phone face-down. [girlfriend_name] saw me do it and didn't have to ask."
    $ ch01_d2_maya_dm_end_show()
    $ ch01_d2_maya_dm_settle()

    # Leia's errand posts (ch01_day2_feed.rpy): "saw a post" bring-up, before every bedroom gate
    # (the nightmare jump and the pool-suspicion menu). Wording follows the ERRAND lane, not the
    # bedroom variant. Moves stats only; every id is left out of tonight's lane and end route.
    $ d2_feed_pending = bool(lc_feed_reaction_queue)
    call lc_feed_reaction_runner from d2_feed_reactions_sc30
    $ d2_errand_lane = get_story_value("ch01_d2_errand_lane")
    $ d2_seen_love_pool = lc_feed_seen("d2_feed_love_poolguy")
    $ d2_seen_love_shop = lc_feed_seen("d2_feed_love_shop")
    $ d2_feed_letgo_text = format_choice("ch01_d2_feed_let_go", "Let it go.")

    if d2_errand_lane == "love" and (d2_seen_love_pool or d2_seen_love_shop):
        if d2_seen_love_pool and not d2_feed_pending:
            think "That café post was still sitting in my head."
        if d2_seen_love_shop and not d2_feed_pending:
            think "So was the one from the shop."
        $ d2_feed_love_text = format_choice("ch01_d2_feed_love_tease", "Tease her about the post.")
        menu:
            "[d2_feed_love_text]":
                $ apply_choice("ch01_d2_feed_love_tease")
                $ set_story_value("ch01_d2_feed_bringup", "love_tease")
                if d2_seen_love_pool:
                    mc "So. I hear you've been busy at the café."
                else:
                    mc "So. Somebody at that shop really, really likes you."
                gf "What? Who said that?"
                "I turned the phone around. [girlfriend_name] read it and went red from her collarbones up."
                if d2_seen_love_pool:
                    gf "He posted it? He actually posted it? Oh my God, I'm going to die."
                    mc "You didn't tell me any of that happened."
                    gf "Because it was nothing, and somebody stopped him, and I didn't want your frappuccino story to be about some creep. It was supposed to be about you."
                    mc "Well, it's kind of about me now. I come out of it looking great."
                    gf "You do look great in it. You're not even in it and you look great. Write that down somewhere."
                if d2_seen_love_shop:
                    gf "Oh my God, that's Margaret! From the shop! She's so sweet. She told me she's been married to Harold for forty-one years. That's going to be us, by the way. You're going to be Harold."
                    mc "I'd be a good Harold."
                    gf "You'd be a great Harold."
                "She took my phone, liked everything on it, and gave it back."
            "[d2_feed_letgo_text]":
                $ apply_choice("ch01_d2_feed_let_go")
                $ set_story_value("ch01_d2_feed_bringup", "let_go")
                "I put the phone down. Whatever else had happened on that walk, she'd come back with my frappuccino and the last box of muffins, and that was good enough for me tonight."

    elif d2_errand_lane == "exhibitionism" and lc_feed_any_seen("d2_feed_exhib_poolguy", "d2_feed_exhib_poolguy_linger"):
        think "The café post was still open on my phone. I'd read the comments under it more times than I wanted to admit."
        $ d2_feed_exhib_text = format_choice("ch01_d2_feed_exhib_show", "Show her the comments.")
        menu:
            "[d2_feed_exhib_text]":
                $ apply_choice("ch01_d2_feed_exhib_show")
                $ set_story_value("ch01_d2_feed_bringup", "exhib_show")
                mc "So, you're a little bit famous."
                "I handed her the phone. She scrolled, and her mouth fell open, and then she kept scrolling."
                gf "Oh my God. That's me. They're talking about me. They're actually sitting there talking about me."
                mc "You don't sound that upset about it."
                gf "I'm mortified. I'm... okay, I'm mortified and I'm reading every single one of them."
                gf "I was going to tell you about him tonight, I swear. I wanted to see your face. He just got there first."
                mc "My face is doing this, if that helps."
                "She looked at me, and whatever she saw made her bite her lip."
                gf "Yeah. That helps."
            "[d2_feed_letgo_text]":
                $ apply_choice("ch01_d2_feed_let_go")
                $ set_story_value("ch01_d2_feed_bringup", "let_go")
                "I put the phone down. If she wanted to tell me about the café, she would. From the look on her face, she was already planning how."

    elif d2_errand_lane == "ntr_risk" and lc_feed_any_seen("d2_feed_ntr_clip", "d2_feed_ntr_clip_linger"):
        think "The post was still open on my phone. I'd known it was her before I'd even finished looking at it."
        if get_story_value("ch01_d2_leia_told") == "told":
            think "She told me. She sat on the end of my lounger and told me before I ever saw this."
            $ d2_feed_told_text = format_choice("ch01_d2_feed_told_aside", "Show her, and say you're glad she told you first.")
            menu:
                "[d2_feed_told_text]":
                    $ apply_choice("ch01_d2_feed_told_aside")
                    $ set_story_value("ch01_d2_feed_bringup", "told_aside")
                    mc "Somebody posted it, by the way. The café thing."
                    "[girlfriend_name] sat up so fast the bed bounced."
                    gf "What? Let me see."
                    "She looked at it for a long time. Long enough that I could hear Maya laughing at something through the wall."
                    gf "Oh, great. Amazing. Thanks so much, Kayla, whoever you are."
                    mc "I'm really glad I heard it from you first. If I'd just found this..."
                    gf "Yeah. I know. That's kind of why I told you."
                    if get_story_value("ch01_d2_confession_reply") == "asked":
                        "She looked at the photo again, and something in her face went pink and quiet, and she didn't hand the phone back straight away."
                "[d2_feed_letgo_text]":
                    $ apply_choice("ch01_d2_feed_let_go")
                    $ set_story_value("ch01_d2_feed_bringup", "let_go")
                    "I put the phone face-down. She'd already told me. There wasn't anything in that post she hadn't said first."
        else:
            think "The café. She'd come back from the café with my frappuccino, sat on the end of my lounger and talked about muffins."
            $ d2_feed_ask_text = format_choice("ch01_d2_feed_kept_ask", "Ask her about the café.")
            $ d2_feed_silent_text = format_choice("ch01_d2_feed_kept_silent", "Put the phone away and say nothing.")
            menu:
                "[d2_feed_ask_text]":
                    $ apply_choice("ch01_d2_feed_kept_ask")
                    $ set_story_value("ch01_d2_feed_bringup", "kept_asked")
                    mc "Hey. What happened at the café today?"
                    "[girlfriend_name] went still."
                    gf "What do you mean? I got your drink."
                    "I turned the phone around. She looked at the screen and didn't say anything for a while."
                    gf "It was nothing. Some gross guy. It was one second, and then I left."
                    mc "You didn't tell me."
                    gf "Because it was nothing! I didn't want it to be a whole thing. You've been in your own head all day, I didn't want to put something else in there."
                    "It sounded true. I just couldn't tell if it was all of it."
                    gf "...I'm sorry. I should've told you."
                    "She put the phone down on the nightstand, screen-down, and neither of us picked it up again."
                "[d2_feed_silent_text]":
                    $ apply_choice("ch01_d2_feed_kept_silent")
                    $ set_story_value("ch01_d2_feed_bringup", "kept_silent")
                    "I locked the screen and put the phone face-down on the nightstand."
                    "[girlfriend_name] was right there, and I didn't ask her anything."
                    think "If it was nothing, she'd have told me. If it was something, I didn't want to hear it tonight."

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
                "I watched her work it out. It took a second, and then it was all over her face."
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

    # Flow: a strained night (pool suspicion talked down, "I'm fine" at sunset, or the café post found
    # the hard way) skips the curtain joke and the "really good day" ending.
    $ d2_love_strained = "ch01_d2_bed_pool_love" in choice_history or get_story_value("ch01_d2_ntr_soft_gate", False) or get_story_value("ch01_d2_feed_bringup") in ("kept_asked", "kept_silent")

    if d2_love_strained:
        "[girlfriend_name] pulled the curtains shut and didn't make a joke about them."
        "For a while neither of us said anything."
        gf "Can we just... not do today for a minute? Just this bit."
        mc "Yeah. Just this bit."
    else:
        "[girlfriend_name] crossed to the window and pulled the curtains shut."

        gf "There. Better."
        mc "You know those don't really hide anything."
        gf "They hide enough. Okay, they hide, like, the general idea. It's the thought that counts."
        mc "That's not what you said yesterday."
        gf "Shut up. Yesterday was different, and I'm not explaining why."

        "The thin fabric still let the light and the shapes through. [girlfriend_name] didn't look at it again."

    gf "Come here."

    $ enter_cinematic_mode()
    scene cg ch01_d2_love_bedroom_01
    with dissolve

    "She pulled me onto the bed with her."
    if d2_love_strained:
        "It was slow and quiet, and neither of us had to work out where our hands went."
    elif get_story_flag("ch01_d2_love_sunset_oral"):
        "After the reckless little moment outside at sunset, this was slower and familiar, a lot of kissing and a bit of laughter, and neither of us had to work out where our hands went."
    else:
        "It was slow and familiar, a lot of kissing and a little laughter, and neither of us had to work out where our hands went."

    scene cg ch01_d2_love_bedroom_02
    with dissolve

    "We had sex with the curtains drawn, the rest of the villa reduced to distant sounds beyond the room."
    "Neither of us thought about the curtains again."

    $ exit_cinematic_mode()
    scene bg ch01_villa_bedroom_night  # night art (darryn)
    with dissolve

    "Afterward [girlfriend_name] curled against me."

    if d2_love_strained:
        gf "Today was a really weird day."
        mc "Yeah. It was."
        gf "This bit was good, though. Can we keep this bit?"
        mc "We're keeping this bit."
    else:
        gf "Today was a really good day."
        mc "Yeah. It really was. Weirdly good, actually."
        gf "Even the bee?"
        mc "Especially the bee."
        gf "You're such an idiot."

    $ set_story_value("ch01_d2_bedroom_variant", "love_private")
    $ set_story_value("ch01_d2_end_route", "love")
    jump ch01_day2_scene_30_finish


label ch01_day2_scene_30_exhibition:

    # Flow: after "I haven't stopped thinking about it" (ch01_d2_bed_pool_exhibition) she works out the
    # other part herself at the glass, instead of a cut straight to the curtain.
    $ d2_exhib_from_pool_talk = "ch01_d2_bed_pool_exhibition" in choice_history
    if d2_exhib_from_pool_talk:
        "She sat with that for a second. Then she got up, went to the glass wall, and put her hand on the curtain without closing it."
        gf "So if I left these open... is that the other part?"
        mc "...Maybe. Yeah."
        gf "Okay. Then I'm leaving them."
        "She was blushing hard. She came back to the bed and pulled me down with her."
    else:
        "[girlfriend_name] looked toward the glass wall."

        "I got up and reached for the edge of the curtain."

        "She was off the bed before I'd pulled it an inch, her hand over mine on the fabric."
        "For a second I thought she was going to finish closing it herself."

        gf "Leave them."

        "She was blushing hard, and she didn't let go of my hand."

        "She tugged me away from the window and back toward the bed."
        gf "Come back here. I want them open."

    $ enter_cinematic_mode()
    scene cg ch01_d2_exhib_bed_open_01
    with dissolve

    "We stayed on the bed, the curtains still pushed back, the lit pool and the walkway right there past the glass."

    gf "You're staring."
    if d2_exhib_from_pool_talk:
        mc "I've been staring all night. I just wasn't saying why."
    else:
        mc "I mean... yeah. You've kind of been making that really hard not to do all night."
    gf "Did you like it?"
    mc "Which part?"
    gf "You know which part."
    if has_story_flag("ch01_d2_nhie_leia_topless_covering"):
        mc "Watching you take your clothes off in front of everyone?"
    else:
        mc "Watching you sit there in your underwear in front of everyone, playing it cool?"
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
    "She drew one arm across her chest on reflex, then let it fall."

    gf "Don't stop."

    scene cg ch01_d2_exhib_bed_open_04
    with dissolve

    mc "They're still watching."
    "[girlfriend_name] hid her face against my shoulder, laughing once from embarrassment before looking back toward the window."

    gf "[player_name]..."
    "I slowed down without meaning to, just to look at her."
    "She caught the back of my neck and pulled me down to her."
    gf "Keep going."

    $ exit_cinematic_mode()
    scene bg ch01_villa_bedroom_night  # night art (darryn)
    with dissolve

    "A few minutes later [girlfriend_name] looked at the still-open curtains."

    gf "Close them now."
    mc "Now? Now you're shy?"
    gf "[player_name]."

    "I laughed and pulled them across."

    if get_story_flag("ch01_d2_exhibition_sunset_shared"):
        gf "Still think I'm secretly an exhibitionist?"
        mc "I don't think it's a secret anymore, babe."
    else:
        gf "Don't say it. Whatever you're about to say, don't."
        mc "I wasn't going to say anything, babe. I'm just smiling."
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
    if get_story_value("ch01_d2_pool_incident") == "leia_julian_bee_top_off":
        "[friend_name] stood behind her in the pool."
        "Instead of looking away like he really had, he reached around and grabbed both of her breasts."
    else:
        "[friend_name] was in the water with her, standing close behind her."
        "In the dream he reached around and grabbed both of her breasts."
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

            mc "I've been... jealous. All day, kind of."
            mc "At the pool, and at dinner, and then the whole game."
            mc "And instead of just saying it, I kept going quiet on you."

            gf "[player_name]..."
            mc "I saw you wink at [friend_name]."

            "[girlfriend_name] went quiet."

            gf "I did."
            mc "Why?"

            "She stared at the ceiling for a few seconds."

            gf "I don't know."
            "Then she corrected herself."
            gf "No. That's not true."
            gf "I think I was angry. Like, really angry, and I didn't know what to do with it."
            gf "And I kind of stopped thinking you'd even care. Which... I know. That's not an excuse."

            mc "I cared. I do care."
            gf "Well, it didn't feel like it. Not from where I was sitting all day."

            "I didn't have an answer to that, because she was right."

            mc "It crossed a line for me."
            gf "I know."
            gf "It was stupid. I shouldn't have done it."
            mc "And I shouldn't have spent the whole day making you guess whether I even wanted to be around you."

            "[girlfriend_name] reached for my hand."

            gf "Then next time, talk to me. Even if it's ugly. Just talk to me."
            mc "You too. If you're angry, tell me you're angry."
            gf "Deal. Okay. Deal."

            "The wink and the long quiet day were still sitting there between us."
            "But her hand was in mine, and we were on the same side of it again."

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
    $ ch01_d2_maya_dm_settle(close=True)
    $ set_story_flag("ch01_day_02_complete")

    scene black
    with fade

    call lc_day_review("ch01_d2") from lc_review_return_ch01_d2

    # Day Two -> Day Three: same pattern as Day One -> Day Two (card, then jump).
    # ch01_d2_end_route and the rest of the stored Day Two state carry over untouched.
    jump ch01_day3_start

