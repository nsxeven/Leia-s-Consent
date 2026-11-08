# Leia's Consent — Chapter One: Something Different
# Playable production chunk: Scenes 4–6.

label ch01_scene_04_pool_arrival:

    scene bg ch01_pool_day
    with fade
    $ lc_amb("pool_day")
    $ lc_bgm("sunny_island")
    # Ryan is on screen from the start; Leia joins when she comes outside.
    $ cast(ryan="pool", julian="pool")

    "[friend_name] had already claimed the shaded end of the pool by the time I came downstairs."

    friend "Is she still changing? Dude, I've been out here so long I've got a tan line from my sunglasses."
    mc "She's almost done. I think. She said \"two minutes\"."
    friend "She said \"two minutes\" before I'd even found the shade."

    gf "No comments until I'm all the way outside."

    with dissolve

    mc "That sounds like you're expecting comments."
    gf "I know you. You've already got one ready, I can see it. You're doing the thing with your mouth."

    $ selected_pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")

    # The outfit reveal was already shown at the end of Scene 3. Do not replay
    # the sprite entrance transform here; keep Leia at her normal pool framing.
    if selected_pool_outfit == "pool_bolder":
        $ cast_add(leia="blue_bikini")
        $ face("leia", "shy")
        with dissolve
        "The new swimsuit was not outrageous. It was simply cut higher at the hips and showed more of her than [friend_name] had ever seen."
        "[girlfriend_name] stopped just beyond the doorway, pretending not to wait for my reaction."
        gf "Well?"
        mc "Do I have to? I mean, you already know."
        gf "Yes, you have to. I want to hear it out loud. With your mouth."
        mc "You look... wow. Okay. Incredible, you look incredible."
        "Some of the tension left her shoulders."
        $ face("leia", "smile")
        $ lc_sfx("leia_sigh")  # darryn: relieved sigh with "Phew"
        gf "Good. Phew. I was kind of nervous about this one."
    else:
        $ cast_add(leia="white_ruffle")
        $ face("leia", "neutral")
        with dissolve
        "She walked out in the swimsuit she already trusted—flattering, familiar, and comfortable enough that she did not need to think about it."
        mc "You look good."
        $ face("leia", "smile")
        gf "I know. This one's safe, it's been to like three beaches already."

    with dissolve

    friend "Are you two finished, or should I give you another minute?"
    gf "Why, are you jealous?"
    friend "No, I just feel bad for the pool. It's been waiting for you two this whole time. It's a very patient pool."

    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_sunscreen_blue
    else:
        scene cg ch01_sunscreen_white
    with dissolve

    "[girlfriend_name] dropped a bottle of sunscreen into my hand and turned her back to me."

    gf "Can you do my back? I always miss the part right in the middle and then I look like a zebra."
    mc "Is there a magic word?"
    gf "We've been together four years, I'm not saying please. Just do it before I melt."

    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_sunscreen_apply_blue
    else:
        scene cg ch01_sunscreen_apply_white
    with dissolve
    $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)
    $ lc_sfx_loop("sunscreen_rub")  # darryn's Squishing Squirt, while he rubs it in

    "I worked the sunscreen across her shoulders and down the center of her back."
    "When my hands slowed near her waist, she looked back at me."

    gf "You're taking a really long time. It's just my back, you know."
    mc "I'm being thorough. Sun damage is, like, a real thing."
    gf "Mm-hm. Very responsible of you."

    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_pool_hand_pull_blue
    else:
        scene cg ch01_pool_hand_pull_white
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)
    $ lc_sfx_loop_stop(0.3)

    $ lc_flash("#e6f6ff", 0.45, 0.5)
    $ lc_sfx("splash_big")
    "She caught my wrist, stepped backward—and pulled me into the pool with her." with lc_shake("m")

    mc "Seriously? I was just— okay. Traitor."
    gf "You were taking forever! And it's so hot, I was basically doing you a favor."
    friend "I saw nothing. I'd like that on the record. I was looking at my drink the whole time."

    $ lc_sfx("splash_small")
    "The next several minutes dissolved into splashing, bad attempts to push one another underwater, and [friend_name] protecting his drink with more commitment than he had shown anything else all day."

    $ set_story_flag("ch01_scene_04_complete")


    jump ch01_scene_05_photography


label ch01_scene_05_photography:

    $ enter_cinematic_mode()
    $ selected_pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_group_blue
    else:
        scene cg ch01_photo_group_white
    with dissolve
    $ lc_amb("pool_day")

    "Eventually, [girlfriend_name] commandeered [friend_name]'s phone and decided the afternoon required photographic evidence."
    $ lc_photo()
    "Her first group selfie caught me blinking and [friend_name] looking as if he had been summoned against his will."

    gf "How are both of you bad at having faces?"
    gf "Wait, I want this as our Trip Group picture. You two look terrible and I love it."
    friend "If you really want to use the one where I look half asleep, go ahead. It is your phone."
    $ phone_group_avatar_stage = "trio"
    $ phone_add_message("group", "leia", text="Changed the group picture to our pool selfie.", message_id="ch01_trip_group_trio_photo", mark_unread=False)

    $ exit_cinematic_mode()
    scene bg ch01_pool_day
    with dissolve
    $ cast(ryan="pool", julian="pool")
    if selected_pool_outfit == "pool_bolder":
        $ cast_add(leia="blue_bikini")
        $ face("leia", "neutral")
    else:
        $ cast_add(leia="white_ruffle")
        $ face("leia", "neutral")

    friend "Here, give me the phone. I'll prop it up somewhere."

    $ lc_sfx("timer_beeps")
    $ lc_photo()
    "He propped it against a glass, set the timer, and somehow produced a picture in which all three of us looked human."

    if selected_pool_outfit == "pool_bolder":
        $ cast_add(leia="blue_bikini")
        $ face("leia", "shy")
    else:
        $ cast_add(leia="white_ruffle")
        $ face("leia", "shy")
    gf "Wait. Why do I actually look good?"
    mc "You say that like it's unusual."
    gf "Rude, but also yes. Every photo you've ever taken of me, I've got a double chin or my eyes are shut."

    "She enlarged the picture, studied it, and looked at [friend_name]."

    gf "Can you take one of just me?"
    friend "Sure, yeah. Of course."

    $ enter_cinematic_mode()
    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_awkward_b
    else:
        scene cg ch01_photo_awkward_a
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    "Her first attempt looked less like a holiday photograph and more like evidence for a passport renewal."

    # The shutter fires only after the setup CG has had a full dialogue beat.
    $ lc_sfx("camera_shutter")
    scene lc_photo_flash_white
    with Dissolve(0.06)
    pause 0.04
    if selected_pool_outfit == "pool_bolder":
        scene cg ch01_photo_capture_01_b
    else:
        scene cg ch01_photo_capture_01_a
    with Dissolve(0.08)
    $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)
    $ set_story_value("ch01_pool_capture_count", 1)

    friend "Relax your shoulders."
    gf "They are relaxed! This is how I relax, this is my relaxed."
    mc "They're almost touching your ears."
    gf "Okay, but what do I do with my hands? I never know what to do with my hands, it's so weird."
    mc "I don't know. They've been there the whole time, though."

    $ lc_sfx("leia_laugh")
    "She laughed despite herself."

    friend "Shift your weight onto one leg. Turn a little toward the water."
    friend "Good. Now look back here."

    $ exit_cinematic_mode()
    scene bg ch01_pool_day
    with dissolve
    $ cast(ryan="pool", julian="pool")

    if selected_pool_outfit == "pool_bolder":
        $ cast_add(leia="blue_bikini")
        $ face("leia", "neutral")
    else:
        $ cast_add(leia="white_ruffle")
        $ face("leia", "neutral")

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
            gf "Actually good, or boyfriend good? Be honest. No, don't be honest. Okay, be a little honest."
            mc "Both. Actually good. Boyfriend good too."
            gf "One more, then I'm done. Probably."

            $ enter_cinematic_mode()

            "This time she stopped posing long enough to enjoy herself."
            $ lc_sfx("leia_laugh")
            "She turned beside the pool, then looked back when I made her laugh."
            "The camera caught the smile before she could replace it with something practiced."

            $ lc_sfx("camera_shutter")
            scene lc_photo_flash_white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_02_b
            else:
                scene cg ch01_photo_capture_02_a
            with Dissolve(0.08)
            $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)
            $ set_story_value("ch01_pool_capture_count", 2)

            # Hold the successful second capture on screen for a dialogue beat.
            # Without this, the branch exits cinematic mode immediately and the
            # photo is visible for only the transition frame.
            "The second shot was different. She looked relaxed this time—caught mid-smile instead of trying to pose."
            gf "Oh, wait, I actually like that one. Look, my arms aren't even weird!"

            $ exit_cinematic_mode()

        "[ch01_photo_more_text]":
            $ apply_choice("ch01_photo_more")
            $ set_story_value("ch01_photo_stance", "encouraging")
            $ set_story_value("ch01_photo_outcome", "confident")
            $ set_story_value("ch01_selected_photo_asset", "ch01_photo_capture_03_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))

            mc "Try one sitting by the edge."
            gf "Since when are you the photographer? I thought that was [friend_name]'s job."
            mc "I'm more like... the creative director. I have opinions."
            friend "So I'm the assistant, then. Great. Does that come with a lanyard?"
            gf "You're both getting way too into this."

            $ enter_cinematic_mode()

            # Capture 02 is the actual second photograph. Flash directly into it
            # rather than showing the obsolete pool-edge placeholder first.
            $ lc_sfx("camera_shutter")
            scene lc_photo_flash_white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_02_b
            else:
                scene cg ch01_photo_capture_02_a
            with Dissolve(0.08)
            $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)

            "She turned beside the pool, angling her body away from the camera before looking back over her shoulder."
            "The pose came more naturally this time. Less instruction, less stiffness."
            "Then she checked my face and smiled."

            gf "Wait. Take another one."
            friend "Your creative director approves?"
            mc "She doesn't need my approval."
            gf "Good answer. Slightly lucky answer, but good."

            "This time she chose the pose herself, stretching out across one of the loungers and settling into it with a confidence she had not had five minutes ago."

            $ lc_sfx("camera_shutter")
            scene lc_photo_flash_white
            with Dissolve(0.06)
            pause 0.04
            if selected_pool_outfit == "pool_bolder":
                scene cg ch01_photo_capture_03_b
            else:
                scene cg ch01_photo_capture_03_a
            with Dissolve(0.08)
            $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)
            $ set_story_value("ch01_pool_capture_count", 3)

            # Hold the photograph without invoking say/centered dialogue UI.
            # Normal dismiss input (click, Space, Enter) advances.
            $ renpy.pause()
            $ exit_cinematic_mode()

        "[ch01_photo_exit_text]":
            $ apply_choice("ch01_photo_exit")
            $ set_story_value("ch01_photo_stance", "protective")

            mc "You look uncomfortable. We can stop."
            gf "Do I look that awkward? Be honest. I feel like I look like I'm waiting for a bus."
            mc "No, you don't. I just think you're thinking about it a lot. It's easier when you stop."

            $ ch01_photo_confidence = partner_stats["curiosity"] + player_stats["acceptance"] + (5 if selected_pool_outfit == "pool_bolder" else 0)
            $ ch01_photo_continues = ch01_photo_confidence >= 38

            if ch01_photo_continues:
                $ set_story_value("ch01_photo_outcome", "chose_to_continue")
                $ set_story_value("ch01_selected_photo_asset", "ch01_photo_capture_02_" + ("b" if selected_pool_outfit == "pool_bolder" else "a"))
                gf "No. I want one good one."
                mc "All right. One more, then."
                gf "Thank you! One, and then I'll stop complaining. I promise."

                $ enter_cinematic_mode()

                "She took a breath, forgot about the camera for a moment, and finally got the photograph she wanted."

                $ lc_sfx("camera_shutter")
                scene lc_photo_flash_white
                with Dissolve(0.06)
                pause 0.04
                if selected_pool_outfit == "pool_bolder":
                    scene cg ch01_photo_capture_02_b
                else:
                    scene cg ch01_photo_capture_02_a
                with Dissolve(0.08)
                $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)
                $ set_story_value("ch01_pool_capture_count", 2)
                $ exit_cinematic_mode()
            else:
                $ set_story_value("ch01_photo_outcome", "stopped")
                # Capture 01 was deleted at Leia's request, so it cannot be
                # delivered to Messages / Photos. Group selfies still exist.
                $ set_story_value("ch01_pool_capture_count", 0)
                $ set_story_value("ch01_selected_photo_asset", "ch01_photo_group_" + ("blue" if selected_pool_outfit == "pool_bolder" else "white"))
                gf "Yeah, please delete that first one. I look like I'm getting arrested."
                friend "Done. The passport photo is gone, I promise."
                "She slid back into the water beside me, visibly relieved that nobody tried to change her mind."

    scene bg ch01_pool_day
    with dissolve
    $ cast(ryan="pool", julian="pool")

    if selected_pool_outfit == "pool_bolder":
        $ cast_add(leia="blue_bikini")
        $ face("leia", "neutral")
    else:
        $ cast_add(leia="white_ruffle")
        $ face("leia", "neutral")

    "[friend_name] lowered the phone after the last shot."

    if get_story_value("ch01_photo_outcome") == "confident":
        gf "Did you get it?"
        friend "I got it. I think you'll like it."
        gf "Good. You can show me later."
    elif get_story_value("ch01_photo_outcome") in ("relaxed", "chose_to_continue"):
        gf "Those better not all be terrible."
        friend "You'll find out later. They're good, I promise."
    else:
        gf "At least tell me the group one was decent."
        friend "It was decent! Everyone had their eyes open. Mostly."

    if get_story_value("ch01_photo_outcome") == "stopped":
        "The solo photos were gone, just as he'd promised. Our first group selfie stayed on [friend_name]'s phone for now."
    else:
        "The photos stayed on [friend_name]'s phone for now."

    # Pacing Revision v2 — an ordinary friendship beat before the towel incident.
    # Leia and Julian should become friends through more than accidents and exposure.
    if selected_pool_outfit == "pool_bolder":
        $ cast_add(leia="blue_bikini")
        $ face("leia", "smile")
    else:
        $ cast_add(leia="white_ruffle")
        $ face("leia", "smile")
    gf "Can I ask you something?"
    mc "That's never a good way to start."
    gf "Was [friend_name] this ridiculous before I knew him?"
    friend "I'm standing right here."
    mc "Define 'ridiculous.'"
    gf "The villa. The photos. Acting like all of this is completely normal."
    mc "Before you knew him? Oh, so much worse."
    friend "That sounded judgmental."
    mc "He once booked a private room for six people because the normal table was 'too loud.'"
    friend "It really was loud, okay? There was a birthday."
    gf "Of course you did."
    friend "It's honestly not a big deal. It was one dinner. Can we, like, not?"
    gf "You're blushing! I'm just teasing. I love the villa. I'm just going to keep making fun of you anyway."

    "She looked at [friend_name], amused."

    gf "Four years, and I still can't decide if you're charming or a problem."
    friend "That's... almost nice? I'm going to take that as nice."
    gf "Don't get used to it."
    mc "Give it a day. She gets meaner on holiday."
    if selected_pool_outfit == "pool_bolder":
        $ cast_add(leia="blue_bikini")
        $ face("leia", "pout")
    else:
        $ cast_add(leia="white_ruffle")
        $ face("leia", "pout")
    gf "Excuse me?"
    friend "Good. It means the trip's working."

    gf "I'm going to go shower before dinner. Try not to drown while I'm gone."

    if selected_pool_outfit == "pool_bolder":
        $ cast_remove("leia")
    else:
        $ cast_remove("leia")

    $ set_story_flag("ch01_scene_05_complete")


    jump ch01_scene_06_friendship_and_towel


label ch01_scene_06_friendship_and_towel:

    scene bg ch01_pool_lounge
    with dissolve
    $ lc_amb("pool_day")
    $ lc_bgm("sunny_island")
    # Leia is upstairs; Ryan stays on screen by the pool.
    $ cast(ryan="pool", julian="pool")

    "With [girlfriend_name] upstairs, the villa became unexpectedly quiet."
    "[friend_name] passed me a cold drink and sank back into the lounger."

    mc "Seriously, though, this place is ridiculous. I keep walking into rooms I didn't know existed."
    friend "Ha, yeah. You've said that, like, four times."
    mc "And you gave us the master bedroom. You really didn't have to do that."
    friend "Have you seen how much [girlfriend_name] packed? You needed the floor space. I'm just being practical."

    mc "Still. Thanks. I mean it."

    "The joke left his face for a moment."

    friend "Honestly? We've been talking about doing a trip for like four years. I just wanted it to be good. For you guys."
    mc "It is. It's really good."
    friend "Plus, you know, you two wouldn't even be together if I hadn't—"
    mc "If you hadn't dared me. One terrible dare."
    friend "A terrible dare that worked, though. Four years!"
    mc "You take way too much credit for that kiss."
    friend "Maybe. But I'd like a plaque. A small one."

    "I laughed. This was [friend_name]—the same person who had been there before [girlfriend_name] and me, and who had helped make us possible without ever asking for anything in return."

    $ lc_sfx("sliding_door")
    gf "[player_name]!"

    "We both looked up."

    $ enter_cinematic_mode()
    $ lc_bgm("cheeky")  # towel mishap
    scene cg ch01_towel_call_down
    with dissolve

    "[girlfriend_name] stood in the open upstairs glass doorway to our pool-facing balcony, wet hair over one shoulder and a small towel wrapped around her body."
    "One hand held it closed as she leaned out to find us."

    gf "Dinner is at seven!"
    mc "What time is it?"
    friend "Six twenty-three."
    gf "Why are both of you still sitting there?"
    mc "Because it's six twenty-three. Dinner's not for like thirty-seven minutes."
    gf "Thirty-seven minutes is nothing! You haven't even changed, and you know how long you take."

    "She stepped farther out, still far more interested in hurrying us along than in how the towel looked from below."

    # Shift_01 (hands down, towel already less secure) shows earlier.
    scene cg ch01_towel_shift_01
    with dissolve

    "From below, the towel was already sitting lower than she seemed to realize."

    gf "I'm serious. Go shower."
    mc "I already showered."
    gf "Pool water doesn't count! You smell like chlorine."
    friend "She's got a point, man."
    mc "Whose side are you on?"
    friend "The side that eats soon. I'm starving."

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

    $ lc_duck()
    $ lc_sfx("leia_gasp")  # she realises what the towel was showing
    gf "...Oh."

    $ lc_bgm_cut()  # comic beat: music stops dead on the scratch
    $ lc_sfx("record_scratch")  # darryn: scratch + shake on TowelShift_03
    scene cg ch01_towel_shift_03
    with dissolve

    "She grabbed the towel tighter against herself, cheeks flushing as she looked from me to [friend_name]." with lc_shake("s")
    "Beside me, [friend_name] turned deliberately toward the pool."

    scene cg ch01_towel_realization
    with dissolve
    $ lc_bgm_resume(1.5)

    friend "I'm looking at the water. I'm so interested in this water."
    $ lc_sfx("leia_angry_laugh")
    gf "You weren't two seconds ago!"
    friend "I didn't know there was going to be a test!"
    mc "Just go inside."
    gf "I was trying to tell you to get ready!"
    mc "Yeah, we got the message. Loud and clear."
    gf "Oh my God, shut up. Shut up, both of you."

    $ lc_sfx("sliding_door")
    $ lc_sfx("curtain")
    "[girlfriend_name] disappeared inside, still clutching the towel against herself, and pulled the sheer curtain across the glass."
    "A moment later she retreated farther into the room."

    $ exit_cinematic_mode()
    scene bg ch01_pool_lounge
    with dissolve
    $ lc_unduck()
    $ cast(ryan="pool", julian="pool")

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
            friend "Yeah, I'm— yep. Looking at the pool. It's a good pool."

        "[ch01_towel_forget_text]":
            $ apply_choice("ch01_towel_forget")
            mc "Let's pretend that didn't happen."
            friend "Yeah. Yes. Agreed. What towel?"

    $ set_story_flag("ch01_scene_06_complete")

    jump ch01_scene_07_did_he_see
