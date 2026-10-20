# Called from the existing scene spine; no label overrides.

label ch01_day4_confirmed_wall:
    "Leia slid her cup along the wall to make room for me. The ice had melted."
    mc "About last night. I keep trying to leave it alone, and I can't."
    gf "Then don't leave it alone. Ask me something."
    if get_story_value("ch01_d3_ntr_repair_effort") == "talk":
        mc "We said we'd try. At the club. I meant it."
        gf "So did I, when I said it."
        "She picked at the paper label on her cup."
        gf "Then you looked at me in that corridor like the conversation had never happened."
    elif get_story_value("ch01_d3_ntr_repair_effort") == "enjoy":
        gf "We had half an hour where you weren't looking through me. I wanted the rest of the night to be like that."
    else:
        gf "I asked you to stay with me. You went to the bar. I don't know how many ways I'm supposed to ask."
    if get_story_value("ch01_d4_morning_reply") == "joined":
        mc "I came down this morning."
        gf "I know. I liked having coffee with you. It doesn't make the rest disappear."
    else:
        gf "Even this morning, I was waiting to see whether you'd come down."
    $ d4_wall_fear = format_choice("ch01_d4_wall_name_fear", "I'm scared you don't want to be here with me.")
    $ d4_wall_times = format_choice("ch01_d4_wall_demand_timeline", "Tell me where you went after I left the sofa.")
    menu:
        "[d4_wall_fear]":
            $ apply_choice("ch01_d4_wall_name_fear")
            $ set_story_value("ch01_d4_harbor_approach", "fear")
            mc "I'm scared you don't want to be here with me."
            gf "I don't know how to answer that today. Yesterday I would've said yes before you finished asking."
            "I heard yesterday. Everything else went quiet."
            if ch01_disclosure_eligible():
                gf "There's something I need to tell you. I don't want you finding out from somebody else."
                $ d4_listen = format_choice("ch01_d4_disclosure_listen", "Let her finish, even if it hurts.")
                $ d4_check = format_choice("ch01_d4_disclosure_crosscheck", "Ask whether Maya would tell the same story.")
                menu:
                    "[d4_listen]":
                        $ apply_choice("ch01_d4_disclosure_listen")
                        jump ch01_day4_voluntary_disclosure
                    "[d4_check]":
                        $ apply_choice("ch01_d4_disclosure_crosscheck")
                        pass
        "[d4_wall_times]":
            $ apply_choice("ch01_d4_wall_demand_timeline")
            $ set_story_value("ch01_d4_harbor_approach", "timeline")
            mc "Tell me where you went after I left the sofa."
            gf "Upstairs. Then the bathroom. I've told you that."
            mc "You've told me two places. Not what happened in between."
    "She turned toward me. For a moment it looked as though she might finally say something different."
    mc "Would Maya give me the same story?"
    "Leia put the cup down carefully."
    gf "You want to check my answer against hers?"
    mc "I want something I can believe."
    gf "Then why ask me at all?"
    "I could have taken the question back. Instead I watched her face for what it gave away."
    gf "I'm tired of trying to get you to talk, then wishing you hadn't."
    mc "Leia. Did something happen with him? Adrian?"
    gf "You don't get to disappear on me for days and turn up as an investigator."
    mc "That isn't an answer."
    gf "I know."
    "She stood, leaving the cup beside mine."
    gf "I'm not doing this here. I'm not asking you to make tonight better either. You can decide what you want to do."
    "Maya was coming back. I lowered my voice, though I had nothing left to say."
    "I wanted a version of last night that didn't depend on Leia deciding to tell me. The thought stayed when she walked away."
    $ set_story_flag("ch01_d4_leia_stopped_repair_bids")
    $ set_story_flag("ch01_d4_monitoring_considered")
    $ set_story_flag("ch01_d4_scene_08_complete")
    jump ch01_day4_scene_09_getting_ready

label ch01_day4_hike_photos:
    "At the villa we stopped for water. Leia unlaced her shoes while I found two clean glasses."
    "We lingered in the kitchen for a while. By the time I'd finished my water, Maya and Julian had sent a message saying they'd reached the lookout."
    "Leia's phone chimed. She read, then laughed once in surprise."
    gf "Maya. You did not."
    mc "What did she send?"
    gf "Photos from the path."
    "Her thumb stopped over the screen."
    mc "Bad photos?"
    gf "Very good ones, apparently. Hang on. They're private."
    "She typed a question. This time she left the phone face up between us while we waited."
    gf "She says he's fine with you seeing. No forwarding."
    $ set_story_flag("ch01_d4_maya_photos_shown")
    call screen ch01_evidence("hike")
    $ enter_cinematic_mode()
    scene cg ch01_d4_hike_private
    with dissolve
    "Julian had one hand over the lens in the first frame. In the next he'd forgotten the camera and was kissing Maya."
    $ exit_cinematic_mode()
    scene bg ch01_villa_kitchen_night
    with dissolve
    mc "He looks happy."
    gf "He does, doesn't he?"
    "She studied the second picture a little longer. Then she took the phone back."
    if ch01_covert_trajectory():
        "I felt foolish for watching the angle of her screen at dinner. She'd just handed me something Maya hadn't meant for the whole group."
        "For a few minutes, that was enough."
        "Leia enlarged the picture, smiled to herself, and returned to her messages. I went to refill the glasses."
    else:
        gf "I'm never letting her complain that he can't take a hint again."
        mc "You're going to need that in writing."
        "She kept the phone beside her, still smiling at the photographs."
    return

label ch01_day4_confirmed_walk:
    scene bg ch01_villa_bedroom_night
    with fade
    gf "I'm going for a walk."
    mc "Now?"
    gf "I need to be out of this room for a bit."
    "She took a jacket from the chair and went into the bathroom to change. Her phone stayed on the bed, its screen still awake."
    "Adrian's name was above the last message. I knew it before I picked the phone up."
    "There was no accidental glance to hide behind. I opened the conversation."
    $ ch01_d4_discover_club()
    call screen ch01_evidence("club")
    $ enter_cinematic_mode()
    scene cg ch01_d4_club_evidence
    with dissolve
    "The picture was from upstairs at the club. Leia was kissing him. Below it, her own words said she'd chosen to stay."
    "I read the date twice. It didn't change."
    $ exit_cinematic_mode()
    scene bg ch01_villa_bedroom_night
    with dissolve
    "The bathroom tap stopped. I put her phone exactly where she'd left it."
    "I could ask her now. I could hear another answer while knowing what she'd left out."
    "Instead I decided I wanted to see what she did when she thought I wasn't looking."
    $ d4_m_truth = format_choice("ch01_d4_monitor_need_truth", "Keep watching. I want the whole truth before I speak.")
    $ d4_m_loss = format_choice("ch01_d4_monitor_fear_loss", "Keep watching. I'm afraid she'll leave if I ask.")
    "I had made the decision. I was still choosing what to call it."
    menu:
        "[d4_m_truth]":
            $ apply_choice("ch01_d4_monitor_need_truth")
            $ ch01_d4_enable_monitoring("need_truth")
            "I called it waiting until I knew enough. I already knew more than I wanted to."
        "[d4_m_loss]":
            $ apply_choice("ch01_d4_monitor_fear_loss")
            $ ch01_d4_enable_monitoring("fear_loss")
            "If I said her name now, I would have to hear what came after it. I couldn't make myself do that."
    # Deliberate story ellipsis: no installation steps or real technical process.
    "Later, my screen held a quiet copy of a conversation that wasn't mine. I'd arranged it without telling her."
    gf "I'll be back in a while."
    mc "Take your key."
    "She patted her jacket pocket. Such an ordinary thing to remember."
    scene bg ch01_d4_terrace_night
    with fade
    "I heard the gate close. For a long time, nothing arrived."
    "I opened the group's messages about breakfast, then closed them. I wasn't reading."
    $ ch01_d4_record_second_meeting()
    call screen ch01_evidence("meeting")
    $ enter_cinematic_mode()
    scene cg ch01_d4_meeting_evidence
    with dissolve
    "The new picture had the closed kiosk behind them. Leia's jacket was the one missing from our chair."
    "This was tonight. No dream, no missing piece of last night I could rearrange."
    $ exit_cinematic_mode()
    scene bg ch01_villa_bedroom_night
    with fade
    "When she came back, I was sitting on the bed with my own phone dark in my hand."
    gf "You're still up."
    mc "Wasn't tired."
    gf "It's cooler outside."
    "She hung the jacket over the chair. I watched her do it."
    if get_story_value("ch01_d4_monitoring_reason") == "fear_loss":
        mc "Are you coming to bed?"
        gf "In a minute."
        "I'd asked whether she was staying. She'd answered a different question."
    else:
        gf "Did Maya and Julian get back?"
        mc "I heard them downstairs."
        "I could still answer questions. Apparently that part worked."
    $ set_story_flag("ch01_d4_scene_13_complete")
    jump ch01_day4_scene_14_night_after

label ch01_day4_roleplay_evening:
    scene bg ch01_d4_terrace_night
    with fade
    "Leia stopped me at the terrace door."
    gf "Pretend we haven't met."
    mc "I was hoping you'd remember me."
    gf "I mean for five minutes. You're allowed to flirt."
    mc "With you?"
    gf "We're off to a worrying start."
    $ d4_r_play = format_choice("ch01_d4_roleplay_play", "Play the stranger at the next table.")
    $ d4_r_watch = format_choice("ch01_d4_roleplay_watch", "Let her make the first move.")
    $ d4_r_private = format_choice("ch01_d4_exhib_private", "I'd rather just be us tonight.")
    menu:
        "[d4_r_play]":
            $ apply_choice("ch01_d4_roleplay_play")
            $ set_story_value("ch01_d4_exhib_variant", "shared_roleplay")
            mc "Is this seat taken?"
            gf "I'm waiting for someone."
            mc "He sounds unreliable."
            gf "He's terrible at pretending he doesn't know me."
        "[d4_r_watch]":
            $ apply_choice("ch01_d4_roleplay_watch")
            $ set_story_value("ch01_d4_exhib_variant", "leia_leads_roleplay")
            "I leaned against the rail and tried to look interesting."
            gf "You look like you need rescuing."
            mc "I've been waiting for a woman with a better opening line."
            gf "Keep waiting, then."
            "She made it two steps before laughing."
        "[d4_r_private]":
            $ apply_choice("ch01_d4_exhib_private")
            $ set_story_value("ch01_d4_exhib_variant", "opt_out_private")
            $ set_story_value("ch01_d4_end_variant", "exhib_private_optout")
            $ set_story_value("ch01_d4_end_route_pending", "love")
            mc "I'd rather just be us tonight."
            gf "Okay. I like us."
            "She took my hand and kissed my knuckles."
    if get_story_value("ch01_d4_exhib_variant") != "opt_out_private":
        gf "Can I kiss you, mysterious man on my terrace?"
        mc "Please."
        "She kissed me, smiling enough to make us both break character."
        gf "You were supposed to be difficult to impress."
        mc "That was never going to work."
        $ set_story_value("ch01_d4_end_route_pending", "exhibitionism")
        $ set_story_value("ch01_d4_exposure_step", "roleplay_only")
        $ set_story_value("ch01_d4_end_variant", "exhib_" + get_story_value("ch01_d4_exhib_variant"))
    $ set_story_flag("ch01_d4_terrace_roleplay_complete")
    "We stayed outside until the lights along the path began going out."
    $ set_story_flag("ch01_d4_scene_13_complete")
    jump ch01_day4_scene_14_night_after

label ch01_day4_final_evening:
    if get_story_value("ch01_d4_betrayal_disclosed", False):
        scene bg ch01_villa_bedroom_night
        with dissolve
        if ch01_nts_agreed():
            "Leia put her phone on the dresser. This time I didn't have to wonder what conversation she'd left unfinished."
            gf "Can we talk again tomorrow, before we decide anything?"
            mc "Yes. I might feel differently in the morning."
            gf "So might I."
            "She sat beside me, leaving enough space for me to choose whether to close it."
            mc "I still want to know you. Even the things I don't know what to do with yet."
            gf "Then I'll tell you. No making you guess."
            "I took her hand. It wasn't forgiveness, and it wasn't a promise about anyone else. It was somewhere to begin talking again."
        elif get_story_value("ch01_d4_end_route_pending") == "exhibitionism":
            gf "We don't have to prove we're all right by doing anything tonight."
            mc "Good. I'm terrible at acting normal."
            gf "I've noticed."
            "Her smile was tentative. I kissed her once, and we left the curtains closed."
            "We could find our shared jokes again. Tonight, being honest was enough."
        elif get_story_value("ch01_d4_end_route_pending") == "love_repaired":
            gf "Would you rather I slept downstairs?"
            mc "I'd rather you stayed. I'm still angry. Both can be true."
            gf "Okay."
            "She stayed on her side of the bed. After a while I reached across the space between us."
            "We didn't pretend we'd fixed it. We had agreed to try."
        else:
            "We agreed not to settle the future while we were exhausted. Leia took a pillow downstairs."
            "I knew what had happened. Knowing what to do next was harder."
    elif ch01_covert_trajectory():
        scene black
        with fade
        "In my sleep the ferry steps led into the nightclub corridor. Every door opened onto the same photograph."
        "I tried to turn the screen off. Another message arrived before I could."
        $ enter_cinematic_mode()
        scene cg ch01_d4_discovery_nightmare
        with dissolve
        "The dates changed. The faces blurred. The certainty I'd had while awake became something I couldn't hold still."
        $ exit_cinematic_mode()
        scene bg ch01_villa_bedroom_night
        with fade
        "I woke with my hand closed around the edge of the sheet. Leia was awake too, her phone dimmed almost to nothing."
        "On it was Maya's photograph of Julian at the lookout. Leia swiped back to it after looking at the next one."
        "Adrian was a fact. Whatever this meant about Julian was a question. I couldn't let myself turn one into the other."
        gf "Can't sleep?"
        mc "Not really."
        "She put the phone down and shifted to make room. I lay beside her without saying what I knew."
        $ set_story_flag("ch01_d4_maya_photos_revisited")
        $ set_story_value("ch01_d4_julian_suspicion", "unconfirmed")
    elif get_story_value("ch01_d4_lane") in ("love", "exhibitionism"):
        scene bg ch01_villa_bedroom_night
        with dissolve
        if get_story_value("ch01_d4_lane") == "exhibitionism" and get_story_value("ch01_d4_exhib_variant") != "opt_out_private":
            gf "Do I get to know your name now?"
            mc "I thought we broke character."
            gf "I liked you. I wanted a second date."
            "She closed the terrace doors and came back to kiss me."
        else:
            gf "Come here. You've been on the other side of the room for ages."
            mc "I was putting a glass down."
            gf "Ages."
            "I kissed her before she could start timing me."
        $ enter_cinematic_mode()
        scene cg ch01_d4_love_night_02
        with dissolve
        "Leia reached for the lamp. We let the conversation end there and kept the rest of the night to ourselves."
        $ exit_cinematic_mode()
    return
