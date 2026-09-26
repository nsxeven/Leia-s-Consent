# Leia's Consent — Chapter One: Something Different
# Playable production chunk: Scenes 4–6.

label ch01_scene_04_pool_arrival:

    scene bg ch01_pool_day
    with fade

    with dissolve

    "[friend_name] had already claimed the shaded end of the pool by the time I came downstairs."

    friend "She changed her mind and unpacked another suitcase, didn't she?"
    mc "Give her a minute."
    friend "I've given her twelve."

    gf "No comments until I'm all the way outside."

    with dissolve

    mc "That sounds like you're expecting comments."
    gf "I know you."

    $ selected_pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")

    # The outfit reveal was already shown at the end of Scene 3. Do not replay
    # the sprite entrance transform here; keep Leia at her normal pool framing.
    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini shy at prologue_sprite_enter_center, leia_body_idle
        with dissolve
        "The new swimsuit was not outrageous. It was simply cut higher at the hips and showed more of her than [friend_name] had ever seen."
        "[girlfriend_name] stopped just beyond the doorway, pretending not to wait for my reaction."
        gf "Well?"
        mc "You already know."
        gf "I want to hear you say it."
        mc "You look incredible."
        "Some of the tension left her shoulders."
        show leia_blue_bikini smile
        with sprite_change
        gf "Better."
    else:
        show leia_white_ruffle neutral at prologue_sprite_enter_center, leia_body_idle
        with dissolve
        "She walked out in the swimsuit she already trusted—flattering, familiar, and comfortable enough that she did not need to think about it."
        mc "You look good."
        show leia_white_ruffle smile
        with sprite_change
        gf "I know. This one has already passed quality control."

    with dissolve

    friend "Are you two finished, or should I give you another minute?"
    gf "Jealous?"
    friend "Of the pool waiting while you flirt? Extremely."

    if selected_pool_outfit == "pool_bolder":
        hide leia_blue_bikini
        scene cg ch01_sunscreen_blue
    else:
        hide leia_white_ruffle
        scene cg ch01_sunscreen_white
    with dissolve

    "[girlfriend_name] dropped a bottle of sunscreen into my hand and turned her back to me."

    gf "Back."
    mc "Please?"
    gf "We've been together four years. 'Please' has expired."

    "I worked the sunscreen across her shoulders and down the centre of her back."
    "When my hands slowed near her waist, she looked back at me."

    gf "You are taking suspiciously long."
    mc "Thorough application prevents sun damage."
    gf "Very responsible."

    if selected_pool_outfit == "pool_bolder":
        hide leia_blue_bikini
        scene cg ch01_pool_hand_pull_blue
    else:
        hide leia_white_ruffle
        scene cg ch01_pool_hand_pull_white
    with dissolve

    "She caught my wrist, stepped backward—and pulled me into the pool with her."

    mc "Traitor."
    gf "You were taking too long."
    friend "For legal purposes, I saw nothing."

    "The next several minutes dissolved into splashing, bad attempts to push one another underwater, and [friend_name] protecting his drink with more commitment than he had shown anything else all day."

    $ set_story_flag("ch01_scene_04_complete")


    jump ch01_scene_05_photography


label ch01_scene_05_photography:

    $ enter_cinematic_mode()
    scene cg ch01_photo_group
    with dissolve

    "Eventually, [girlfriend_name] decided the afternoon required photographic evidence."
    "Her first group selfie caught me blinking and [friend_name] looking as if he had been summoned against his will."

    gf "How are both of you bad at having faces?"
    friend "Give me the phone."

    "He propped it against a glass, set the timer, and somehow produced a picture in which all three of us looked human."

    gf "Wait. Why do I actually look good?"
    mc "You say that like it's unusual."
    gf "When you take the photo, it is."

    "She enlarged the picture, studied it, and looked at [friend_name]."

    gf "Can you take one of just me?"
    friend "Sure."

    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_awkward_b
    else:
        scene cg ch01_photo_awkward_a
    with dissolve

    # Every saved Capture photograph gets the same quick shutter-flash reveal.
    scene white
    with Dissolve(0.06)
    pause 0.04
    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_capture_01_b
    else:
        scene cg ch01_photo_capture_01_a
    with Dissolve(0.08)
    $ set_story_value("ch01_pool_capture_count", 1)

    "Her first attempt looked less like a holiday photograph and more like evidence for a passport renewal."

    friend "Relax your shoulders."
    gf "They are relaxed."
    mc "They're almost touching your ears."
    gf "I don't know what to do with my hands."
    mc "You normally have hands. What changed?"

    "She laughed despite herself."

    friend "Shift your weight onto one leg. Turn a little toward the water."
    friend "Good. Now look back here."

    $ exit_cinematic_mode()
    scene bg ch01_pool_day
    with dissolve

    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini neutral at prologue_sprite_enter_center, leia_body_idle
    else:
        show leia_white_ruffle neutral at prologue_sprite_enter_center, leia_body_idle
    with sprite_enter_exit

    "She was improving, but every time she noticed the camera she became stiff again."

    $ ch01_photo_support_text = format_choice("ch01_photo_support", "That one looks really good.")
    $ ch01_photo_more_text = format_choice("ch01_photo_more", "Try one sitting by the edge.")
    $ ch01_photo_exit_text = format_choice("ch01_photo_exit", "You look uncomfortable. We can stop.")

    menu:
        "[ch01_photo_support_text]":
            $ apply_choice("ch01_photo_support")
            $ set_story_value("ch01_photo_stance", "supportive")
            $ set_story_value("ch01_photo_outcome", "relaxed")
            $ set_story_value("ch01_selected_photo_asset", "ch01_photo_support_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))

            mc "That one looks really good."
            gf "Actually good, or boyfriend good?"
            mc "Both."
            gf "Okay. One more."

            $ enter_cinematic_mode()
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_support_b
            else:
                scene cg ch01_photo_support_a
            with dissolve

            "This time she stopped posing long enough to enjoy herself."
            "Wet hair rested over one shoulder as she turned toward the water, then looked back when I made her laugh."
            "The camera caught the smile before she could replace it with something practiced."

            scene white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_02_b
            else:
                scene cg ch01_photo_capture_02_a
            with Dissolve(0.08)
            $ set_story_value("ch01_pool_capture_count", 2)
            $ exit_cinematic_mode()

        "[ch01_photo_more_text]":
            $ apply_choice("ch01_photo_more")
            $ set_story_value("ch01_photo_stance", "encouraging")
            $ set_story_value("ch01_photo_outcome", "confident")
            $ set_story_value("ch01_selected_photo_asset", "ch01_photo_more_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))

            mc "Try one sitting by the edge."
            gf "Since when are you the photographer?"
            mc "Creative director."
            friend "Unpaid assistant."
            gf "Both of you are getting very confident."

            $ enter_cinematic_mode()
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_more_b
            else:
                scene cg ch01_photo_more_a
            with dissolve

            "She sat at the pool's edge with her legs in the water, body angled away before glancing back over her shoulder."
            "It was more suggestive than anything [girlfriend_name] would normally pose for—and for a second she seemed surprised by herself."
            "Then she checked my face and smiled."

            gf "Wait. Take another one."
            friend "Your creative director approves?"
            mc "She doesn't need my approval."
            gf "Correct answer."

            "She brushed her wet hair back, adjusted the pose herself, and held it until the camera clicked."

            scene white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_02_b
            else:
                scene cg ch01_photo_capture_02_a
            with Dissolve(0.08)

            "She checked the result, then looked back at [friend_name]."
            gf "One more."
            friend "Now you're enjoying this."
            gf "Just take it."

            scene white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_03_b
            else:
                scene cg ch01_photo_capture_03_a
            with Dissolve(0.08)
            $ set_story_value("ch01_pool_capture_count", 3)
            $ exit_cinematic_mode()

        "[ch01_photo_exit_text]":
            $ apply_choice("ch01_photo_exit")
            $ set_story_value("ch01_photo_stance", "protective")

            mc "You look uncomfortable. We can stop."
            gf "Do I look that awkward?"
            mc "Only because you're thinking about it too much."

            $ ch01_photo_confidence = partner_stats["curiosity"] + player_stats["acceptance"] + (5 if selected_pool_outfit == "pool_bolder" else 0)
            $ ch01_photo_continues = ch01_photo_confidence >= 38

            if ch01_photo_continues:
                $ set_story_value("ch01_photo_outcome", "chose_to_continue")
                $ set_story_value("ch01_selected_photo_asset", "ch01_photo_support_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))
                gf "No. I want one good one."
                mc "Then we keep going because you want to."
                gf "Exactly."

                $ enter_cinematic_mode()
                if selected_pool_outfit == "pool_bolder":
                    scene cg ch01_photo_support_b
                else:
                    scene cg ch01_photo_support_a
                with dissolve

                "She took a breath, forgot about the camera for a moment, and finally got the photograph she wanted."

                scene white
                with Dissolve(0.06)
                pause 0.04
                if selected_pool_outfit == "pool_bolder":
                    scene cg ch01_photo_capture_02_b
                else:
                    scene cg ch01_photo_capture_02_a
                with Dissolve(0.08)
                $ set_story_value("ch01_pool_capture_count", 2)
                $ exit_cinematic_mode()
            else:
                $ set_story_value("ch01_photo_outcome", "stopped")
                $ set_story_value("ch01_selected_photo_asset", "ch01_photo_group")
                gf "Okay. Save me."
                friend "Your passport photo has been safely deleted."
                "She slid back into the water beside me, visibly relieved that nobody tried to change her mind."

    scene bg ch01_pool_day
    with dissolve

    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini neutral at prologue_sprite_enter_center, leia_body_idle
    else:
        show leia_white_ruffle neutral at prologue_sprite_enter_center, leia_body_idle
    with sprite_enter_exit

    "[girlfriend_name] took her phone back and scrolled through the results."

    if get_story_value("ch01_photo_outcome") == "confident":
        gf "Okay... that one is actually kind of hot."
        mc "Kind of?"
        gf "Don't make me take it back."
    elif get_story_value("ch01_photo_outcome") in ("relaxed", "chose_to_continue"):
        gf "I like this one. I look like I'm not trying."
        friend "That's because you finally weren't."
    else:
        gf "The group one is cute."
        mc "Even with my face?"
        gf "Your face gives it character."

    "She saved her favourite without posting it anywhere."

    gf "I'm showering before dinner. Try not to drown while I'm gone."

    if selected_pool_outfit == "pool_bolder":
        hide leia_blue_bikini
    else:
        hide leia_white_ruffle
    with sprite_enter_exit

    $ set_story_flag("ch01_scene_05_complete")


    jump ch01_scene_06_friendship_and_towel


label ch01_scene_06_friendship_and_towel:

    scene bg ch01_pool_lounge
    with dissolve

    "With [girlfriend_name] upstairs, the villa became unexpectedly quiet."
    "[friend_name] passed me a cold drink and sank back into the lounger."

    mc "This place is ridiculous."
    friend "You've mentioned that."
    mc "You gave us the master bedroom."
    friend "I've heard the two of you pack. You need the additional floor space."

    mc "Still. Thanks."

    "The joke left his face for a moment."

    friend "We've been trying to make this trip happen for four years. I wanted it to be worth waiting for."
    mc "You succeeded."
    friend "Besides, without me, neither of you would be here."
    mc "You issued one terrible dare."
    friend "A historically successful terrible dare."
    mc "You've taken too much credit for that kiss."
    friend "Not enough, actually."

    "I laughed. This was [friend_name]—the same person who had been there before [girlfriend_name] and me, and who had helped make us possible without ever asking for anything in return."

    gf "[player_name]!"

    "We both looked up."

    $ enter_cinematic_mode()
    scene cg ch01_towel_call_down
    with dissolve

    "[girlfriend_name] stood in the open upstairs doorway with wet hair and a small towel wrapped around her body."
    "One hand held it closed. The other braced against the frame as she leaned out to find us."
    "From where she stood, she probably thought she was covered. From the pool below, the towel looked considerably shorter."

    gf "Dinner is at seven!"
    mc "What time is it?"
    friend "Six twenty-three."
    gf "Why are both of you still sitting there?"

    "She stepped farther out and leaned over the railing, exposing most of one thigh as the towel rode higher over her hip."

    scene cg ch01_towel_shift
    with Dissolve(3.0)

    "When she lifted an arm to gesture toward the room, the top loosened just enough to reveal the side and lower curve of her breast."
    "Not everything. More than she intended."

    mc "[girlfriend_name]."
    gf "What?"
    mc "Your towel."

    scene cg ch01_towel_realization
    with dissolve

    "She looked down. Then she looked at us—and finally understood the angle."

    gf "...Oh."

    "She clamped the towel against her chest. That fixed one problem while leaving most of her thighs exposed."
    "Beside me, [friend_name] turned deliberately toward the pool."

    friend "I'm looking at the water."
    gf "You weren't two seconds ago!"
    friend "I didn't know there was going to be a test!"

    # No dedicated CG here: remain on the established upstairs pool-view background.
    scene bg ch01_pool_lounge
    with dissolve

    "[girlfriend_name] disappeared inside and grabbed at the sheer curtain."
    "Then she retreated farther into the room, away from the glass."

    $ exit_cinematic_mode()
    scene bg ch01_pool_lounge
    with dissolve

    $ ch01_pre_towel_stance = chapter_stance("ch01")

    if ch01_pre_towel_stance == "encouraging":
        "It happened so quickly that it was more funny than threatening. One moment she was rushing us; the next she looked as if she wanted the curtains to swallow her."
    elif ch01_pre_towel_stance == "protective":
        "I knew it was an accident. I knew [friend_name] had done nothing wrong. That did not stop the discomfort arriving before the reasonable part of me could catch up."
    else:
        "It was awkward. Nothing more than that—or at least, that was what I told myself when I registered that [friend_name] had looked up too."

    $ ch01_towel_laugh_text = format_choice("ch01_towel_laugh", "Well. She found out what the curtains are for.")
    $ ch01_towel_boundary_text = format_choice("ch01_towel_boundary", "Eyes on the pool, mate.")
    $ ch01_towel_forget_text = format_choice("ch01_towel_forget", "Let's pretend that didn't happen.")

    menu:
        "[ch01_towel_laugh_text]":
            $ apply_choice("ch01_towel_laugh")
            $ set_story_value("ch01_towel_response", "laughed")
            mc "Well. She found out what the curtains are for."
            friend "I am never looking at that window again."

        "[ch01_towel_boundary_text]":
            $ apply_choice("ch01_towel_boundary")
            $ set_story_value("ch01_towel_response", "playful_boundary")
            mc "Eyes on the pool, mate."
            friend "Already there."
            mc "Just checking."
            friend "Fair."

        "[ch01_towel_forget_text]":
            $ apply_choice("ch01_towel_forget")
            $ set_story_value("ch01_towel_response", "uncomfortable")
            mc "Let's pretend that didn't happen."
            friend "Was already planning to."

    "Whatever my reaction, [friend_name] did not argue, tease her, or try to turn the accident into something it was not."

    $ set_story_flag("ch01_towel_incident_complete")
    $ set_story_flag("ch01_scene_06_complete")
    $ set_story_flag("ch01_scenes_04_06_complete")


    scene bg ch01_master_bedroom_curtains
    with dissolve

    "I headed upstairs to change. The bedroom door was open, but [girlfriend_name] had retreated into the bathroom."

    gf "[player_name]?"
    mc "Yeah?"
    gf "...Did he see anything?"

    jump ch01_scene_07_did_he_see
