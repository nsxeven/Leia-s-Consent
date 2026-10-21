# Leia's Consent — Chapter One: Something Different
# Playable production chunk: Scenes 4–6.

label ch01_scene_04_pool_arrival:

    show ryan_pool at prologue_other_enter_left, leia_body_idle
    with sprite_enter_exit

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
        show leia_blue_bikini shy at prologue_leia_enter_right, leia_body_idle
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
        show leia_white_ruffle neutral at prologue_leia_enter_right, leia_body_idle
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

    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_sunscreen_apply_blue
    else:
        scene cg ch01_sunscreen_apply_white
    with dissolve

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

    show ryan_pool at prologue_other_enter_left, leia_body_idle
    with sprite_enter_exit

    $ enter_cinematic_mode()
    $ selected_pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_group_blue
    else:
        scene cg ch01_photo_group_white
    with dissolve

    "Eventually, [girlfriend_name] decided the afternoon required photographic evidence."
    "Her first group selfie caught me blinking and [friend_name] looking as if he had been summoned against his will."

    gf "How are both of you bad at having faces?"

    $ exit_cinematic_mode()
    scene bg ch01_pool_day
    with dissolve
    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini neutral at prologue_leia_enter_right, leia_body_idle
    else:
        show leia_white_ruffle neutral at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    friend "Give me the phone."

    "He propped it against a glass, set the timer, and somehow produced a picture in which all three of us looked human."

    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini shy
    else:
        show leia_white_ruffle shy
    with sprite_change
    gf "Wait. Why do I actually look good?"
    mc "You say that like it's unusual."
    gf "When you take the photo, it is."

    "She enlarged the picture, studied it, and looked at [friend_name]."

    gf "Can you take one of just me?"
    friend "Sure."

    $ enter_cinematic_mode()
    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_awkward_b
    else:
        scene cg ch01_photo_awkward_a
    with dissolve

    "Her first attempt looked less like a holiday photograph and more like evidence for a passport renewal."

    # The shutter fires only after the setup CG has had a full dialogue beat.
    scene lc_photo_flash_white
    with Dissolve(0.06)
    pause 0.04
    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_capture_01_b
    else:
        scene cg ch01_photo_capture_01_a
    with Dissolve(0.08)
    $ set_story_value("ch01_pool_capture_count", 1)

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
        show leia_blue_bikini neutral at prologue_leia_enter_right, leia_body_idle
    else:
        show leia_white_ruffle neutral at prologue_leia_enter_right, leia_body_idle
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
            $ set_story_value("ch01_selected_photo_asset", "ch01_photo_capture_02_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))

            mc "That one looks really good."
            gf "Actually good, or boyfriend good?"
            mc "Both."
            gf "Okay. One more."

            $ enter_cinematic_mode()

            "This time she stopped posing long enough to enjoy herself."
            "She turned beside the pool, then looked back when I made her laugh."
            "The camera caught the smile before she could replace it with something practiced."

            scene lc_photo_flash_white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_02_b
            else:
                scene cg ch01_photo_capture_02_a
            with Dissolve(0.08)
            $ set_story_value("ch01_pool_capture_count", 2)

            # Hold the successful second capture on screen for a dialogue beat.
            # Without this, the branch exits cinematic mode immediately and the
            # photo is visible for only the transition frame.
            "The second shot was different. She looked relaxed this time—caught mid-smile instead of trying to pose."
            gf "Okay. I actually like that one."

            $ exit_cinematic_mode()

        "[ch01_photo_more_text]":
            $ apply_choice("ch01_photo_more")
            $ set_story_value("ch01_photo_stance", "encouraging")
            $ set_story_value("ch01_photo_outcome", "confident")
            $ set_story_value("ch01_selected_photo_asset", "ch01_photo_capture_03_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))

            mc "Try one sitting by the edge."
            gf "Since when are you the photographer?"
            mc "Creative director."
            friend "Unpaid assistant."
            gf "Both of you are getting very confident."

            $ enter_cinematic_mode()

            # Capture 02 is the actual second photograph. Flash directly into it
            # rather than showing the obsolete pool-edge placeholder first.
            scene lc_photo_flash_white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_02_b
            else:
                scene cg ch01_photo_capture_02_a
            with Dissolve(0.08)

            "She turned beside the pool, angling her body away from the camera before looking back over her shoulder."
            "The pose came more naturally this time. Less instruction, less stiffness."
            "Then she checked my face and smiled."

            gf "Wait. Take another one."
            friend "Your creative director approves?"
            mc "She doesn't need my approval."
            gf "Correct answer."

            "This time she chose the pose herself, stretching out across one of the loungers and settling into it with a confidence she had not had five minutes ago."

            scene lc_photo_flash_white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_03_b
            else:
                scene cg ch01_photo_capture_03_a
            with Dissolve(0.08)
            $ set_story_value("ch01_pool_capture_count", 3)

            # Hold the photograph without invoking say/centered dialogue UI.
            # Normal dismiss input (click, Space, Enter) advances.
            $ renpy.pause()
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
                $ set_story_value("ch01_selected_photo_asset", "ch01_photo_capture_02_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))
                gf "No. I want one good one."
                mc "All right. One more, then."
                gf "Exactly."

                $ enter_cinematic_mode()

                "She took a breath, forgot about the camera for a moment, and finally got the photograph she wanted."

                scene lc_photo_flash_white
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
                # Capture 01 was deleted at Leia's request, so it cannot be
                # delivered to Messages / Photos. Group selfies still exist.
                $ set_story_value("ch01_pool_capture_count", 0)
                $ set_story_value("ch01_selected_photo_asset", "ch01_photo_group_" + ("blue" if selected_pool_outfit == "pool_bolder" else "white"))
                gf "Okay. Save me."
                friend "Your passport photo has been safely deleted."
                "She slid back into the water beside me, visibly relieved that nobody tried to change her mind."

    scene bg ch01_pool_day
    with dissolve

    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini neutral at prologue_leia_enter_right, leia_body_idle
    else:
        show leia_white_ruffle neutral at prologue_leia_enter_right, leia_body_idle
    with sprite_enter_exit

    "[friend_name] lowered the phone after the last shot."

    if get_story_value("ch01_photo_outcome") == "confident":
        gf "Did you get it?"
        friend "I got it."
        gf "Good. You can show me later."
    elif get_story_value("ch01_photo_outcome") in ("relaxed", "chose_to_continue"):
        gf "Those better not all be terrible."
        friend "You'll find out later."
    else:
        gf "At least tell me the group one was decent."
        friend "You'll survive."

    if get_story_value("ch01_photo_outcome") == "stopped":
        "The solo photos were gone, just as he'd promised. Our first group selfie stayed on [friend_name]'s phone for now."
    else:
        "The photos stayed on [friend_name]'s phone for now."

    # Pacing Revision v2 — an ordinary friendship beat before the towel incident.
    # Leia and Julian should become friends through more than accidents and exposure.
    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini smile
    else:
        show leia_white_ruffle smile
    with sprite_change
    gf "Can I ask you something?"
    mc "Dangerous opening."
    gf "Has [friend_name] always been like this?"
    friend "I'm standing right here."
    mc "Define 'this.'"
    gf "The villa. The photos. Acting like all of this is completely normal."
    mc "Oh. Yes."
    friend "That sounded judgmental."
    mc "He once booked a private room for six people because the normal table was 'too loud.'"
    friend "It was too loud."
    gf "Of course you did."
    friend "You enjoyed the villa."
    gf "I can enjoy it and still make fun of you."

    "She looked at me, amused."

    gf "I can see why you two are friends."
    friend "Careful. That's almost nice."
    gf "Don't get used to it."
    mc "Give it a day. She gets meaner when she's comfortable."
    if selected_pool_outfit == "pool_bolder":
        show leia_blue_bikini pout
    else:
        show leia_white_ruffle pout
    with sprite_change
    gf "Excuse me?"
    friend "Good. You'll fit in."

    "It was the first time their teasing sounded less like my girlfriend talking to my friend and more like the beginning of a friendship of their own."

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
    "One hand held it closed as she leaned out to find us."

    gf "Dinner is at seven!"
    mc "What time is it?"
    friend "Six twenty-three."
    gf "Why are both of you still sitting there?"
    mc "Because dinner isn't for another thirty-seven minutes."
    gf "Exactly. You haven't even changed."

    "She stepped farther out, still far more interested in hurrying us along than in how the towel looked from below."

    # Shift_01 (hands down, towel already less secure) shows earlier.
    scene cg ch01_towel_shift_01
    with dissolve

    "From below, the towel was already sitting lower than she seemed to realize."

    gf "I'm serious. Go shower."
    mc "I already showered."
    gf "Pool water doesn't count."
    friend "She's got you there."
    mc "Whose side are you on?"
    friend "The side that gets to dinner on time."

    "She lifted an arm as if that settled the argument."

    # Shift_02 is the raised-hand frame.
    scene cg ch01_towel_shift_02
    with dissolve

    "The movement shifted the towel further."

    mc "[girlfriend_name]."
    gf "What?"
    mc "Your towel."

    "Her eyes followed mine downward."
    "The argument disappeared from her face as she finally understood the angle."

    gf "...Oh."

    scene cg ch01_towel_shift_03
    with dissolve

    "She grabbed the towel tighter against herself, cheeks flushing as she looked from me to [friend_name]."
    "Beside me, [friend_name] turned deliberately toward the pool."

    scene cg ch01_towel_realization
    with dissolve

    friend "I'm looking at the water."
    gf "You weren't two seconds ago!"
    friend "I didn't know there was going to be a test!"
    mc "Just go inside."
    gf "I was trying to tell you to get ready!"
    mc "Message received."
    gf "Shut up."

    "[girlfriend_name] disappeared inside, still clutching the towel against herself, and pulled the sheer curtain across the glass."
    "A moment later she retreated farther into the room."

    $ exit_cinematic_mode()
    scene bg ch01_pool_lounge
    with dissolve

    $ ch01_pre_towel_stance = chapter_stance("ch01")

    if ch01_pre_towel_stance == "encouraging":
        "[friend_name] cleared his throat, still facing the water."
    elif ch01_pre_towel_stance == "protective":
        "[friend_name] kept his eyes on the pool longer than necessary."

    $ ch01_towel_laugh_text = format_choice("ch01_towel_laugh", "Well. She found out what the curtains are for.")
    $ ch01_towel_boundary_text = format_choice("ch01_towel_boundary", "Eyes on the pool, mate.")
    $ ch01_towel_forget_text = format_choice("ch01_towel_forget", "Let's pretend that didn't happen.")

    menu:
        "[ch01_towel_laugh_text]":
            $ apply_choice("ch01_towel_laugh")
            mc "Well. She found out what the curtains are for."
            friend "I'm going to go... not be here."

        "[ch01_towel_boundary_text]":
            $ apply_choice("ch01_towel_boundary")
            mc "Eyes on the pool, mate."
            friend "Already done."

        "[ch01_towel_forget_text]":
            $ apply_choice("ch01_towel_forget")
            mc "Let's pretend that didn't happen."
            friend "Agreed."

    $ set_story_flag("ch01_scene_06_complete")

    jump ch01_scene_07_did_he_see
