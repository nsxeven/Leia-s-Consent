# Day Two Scene 30 route-order revision.
# If Ryan experienced the suspicious Leia/Julian pool return and did NOT take
# the sunset soft gate, bedtime always resolves that incident before the day
# can settle back onto Love / Exhibitionism. This is independent of whether
# later attentive choices already improved the live route score.

init 999 python:
    _ch01_d2_scene30_previous_label_callback = config.label_callback

    def _ch01_d2_scene30_label_callback(name, abnormal):
        if _ch01_d2_scene30_previous_label_callback is not None:
            _ch01_d2_scene30_previous_label_callback(name, abnormal)

        if name == "ch01_day2_scene_30_bedroom":
            renpy.jump("ch01_day2_scene_30_bedroom_revision")

    config.label_callback = _ch01_d2_scene30_label_callback


label ch01_day2_scene_30_bedroom_revision:

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
