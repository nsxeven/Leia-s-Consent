# Leia's Consent — Chapter One: Something Different
# First playable production chunk: Scenes 1–3.

label chapter_one_start:
    $ lc_review_begin("ch01_d1")

    $ set_story_flag("ch01_started")
    $ set_phone_hud_enabled(True)
    # Sprites come from the cast (systems/cast_staging.rpy).

    jump ch01_scene_01_arrival


label ch01_scene_01_arrival:

    scene bg ch01_car_day
    with fade
    $ lc_amb("car_day")
    $ lc_bgm("sunny_island")
    $ cast(ryan="casual", leia="casual", julian="travel")

    "By the time the transfer car turned into the villa's driveway, [girlfriend_name] had taken thirty-seven photos."
    "Thirty-eight, if the blurry one of [friend_name] asleep in the transfer car counted."

    $ face("leia", "smile")
    gf "This place doesn't look real. Like, at all. It looks like a screensaver."
    mc "You've said that about the airport, the boat, and a coconut."
    $ face("leia", "pout")
    gf "The coconut was very photogenic. I stand by that."

    with dissolve

    "A member of staff greeted [friend_name] by name as the car pulled up outside the villa."
    "Our bags disappeared onto a cart. Cold towels appeared. So did three drinks none of us remembered ordering."

    mc "Should I be worried that everyone here knows you?"
    friend "They know the booking, not me. I mean, it's that kind of place, they're like that with everybody. Probably."
    $ face("leia", "skeptical")
    gf "The booking has a face? He said your name like you two go way back."
    friend "It's on the reservation, that's all, it's really not a big deal. Can we— oh, look, cold towels. Everybody take a cold towel."

    "He said it like the private transfer, waiting staff, and seamless arrival were ordinary."
    "That was very [friend_name]: arranging something ridiculous, then acting like it had just sort of happened by accident."

    $ face("leia", "smile")
    gf "Wait—don't move. Both of you."
    mc "Another one? That's like thirty-nine."
    gf "First proper holiday photo. Try to look happy. Especially you, [friend_name], it's your villa, you have to look the happiest."
    friend "It's not, like, my villa. It's a booking. I just clicked a button. Can you take it before I blink? I always blink."

    $ lc_photo()
    "I laughed just as she took it."
    "For once, she lowered the phone without checking the result ten times."

    $ set_story_flag("ch01_scene_01_complete")


    jump ch01_scene_02_villa


label ch01_scene_02_villa:

    scene bg ch01_villa_exterior
    with dissolve
    $ lc_amb("villa_day")
    $ cast(ryan="casual", leia="casual", julian="travel")

    "The cart followed a narrow path through palms and stopped in front of a two-storey villa facing the ocean."

    $ face("leia", "skeptical")
    gf "[friend_name]."
    friend "Yes?"
    $ face("leia", "smile")
    gf "This is not a villa. This is, like, a small country. Does it have its own flag? It should have a flag."
    friend "The listing said 'intimate'... I think they meant the vibe? I just looked at the pictures."
    mc "Intimate compared to what? An airport?"

    $ enter_cinematic_mode()
    scene cg ch01_villa_arrival at lc_push_in
    with dissolve
    $ lc_sfx("leia_gasp")  # darryn: Leia's gasp at the villa reveal

    "Inside, the living room opened straight toward a private pool, an outdoor lounge, and a strip of beach beyond it."
    gf "Look at that view."
    "Glass, pale wood, soft furniture—everything looked expensive without trying to announce it."

    $ exit_cinematic_mode()
    scene bg ch01_villa_corridor
    with dissolve
    $ lc_amb("villa_day")
    $ cast(ryan="casual", leia="casual", julian="travel")

    friend "There are two rooms upstairs. You two take the master."
    mc "You booked the place. You take it."
    friend "Nah, it's fine, it's one room and I'm one guy. And I don't want to lie there listening to you two argue through the wall about who got the smaller room."
    $ face("leia", "skeptical")
    gf "We don't argue! We— okay, we discuss. Sometimes loudly."
    mc "I mean, she discusses. I mostly lose."
    $ face("leia", "pout")
    gf "He does mostly lose. It's kind of his thing, I've made my peace with it."

    "[friend_name] waved us toward the stairs before I could object again."


    scene bg ch01_villa_master_enter
    with dissolve
    $ lc_amb("room_tone")
    $ cast(ryan="casual", leia="casual", julian="travel")

    "The master bedroom took up most of the second floor."
    "One wall was almost entirely glass, looking down over the pool and past it to the ocean."
    "Light curtains softened the view without quite hiding it. Decorative, more than private."
    "A sliding glass doorway opened onto a small balcony overlooking the pool below."

    with dissolve

    mc "Yeah. Wow. I'm looking."
    $ face("leia", "skeptical")
    gf "You're looking at me. The ocean's over there, it's literally the whole wall."
    mc "I mean... I can see it from here."

    "She caught my reflection in the glass and rolled her eyes, smiling anyway."

    gf "Wait, where's [friend_name] even sleeping? Is his room, like, a cupboard?"
    mc "Next door. Same view, slightly less country-sized."
    gf "And he still gave us this one? That's so sweet, now I kind of feel bad."
    mc "Yeah, he's always been like that. You can't win that one with him."

    "Below us, sunlight moved across the water in the private pool."

    $ set_story_flag("ch01_villa_geography_established")
    $ set_story_flag("ch01_scene_02_complete")

    jump ch01_scene_03_outfit_choice


label ch01_scene_03_outfit_choice:

    scene bg ch01_master_bedroom
    with dissolve
    $ lc_amb("room_tone")
    $ cast(ryan="casual", leia="casual", julian="travel")

    "Unpacking took less than five minutes. Deciding what to wear took considerably longer."

    $ face("leia", "smile")
    gf "Okay, I need an opinion. A real one, not a boyfriend one."
    mc "Uh-oh. Okay. What's a boyfriend one?"
    gf "The one where you just say 'you look great' so we can leave. So. I brought two swimsuits."
    gf "The usual one... and one I bought for this trip."

    "She held up the first: flattering, familiar, and comfortable."
    "The second was still normal resort swimwear, just a little bolder than anything she usually wore around our friends."

    # Sprites leave with the scene change itself (one dissolve), not a separate fade first.
    $ enter_cinematic_mode()
    scene cg ch01_swimsuit_choice
    with dissolve
    gf "Is this one too much with [friend_name] here?"

    $ ch01_outfit_bolder_text = format_choice("ch01_outfit_bolder", "Not at all. You'd look amazing in it.")
    $ ch01_outfit_comfort_text = format_choice("ch01_outfit_comfort", "Wear whichever one makes you comfortable.")
    $ ch01_outfit_conservative_text = format_choice("ch01_outfit_conservative", "I kinda like the other one on you more.")
    $ ch01_outfit_rush_text = format_choice("ch01_outfit_rush", ("They both look fine. " + friend_name + "'s waiting."))

    menu:
        "[ch01_outfit_bolder_text]":
            $ apply_choice("ch01_outfit_bolder")
            $ set_story_value("ch01_pool_outfit", "pool_bolder")
            $ set_story_value("ch01_outfit_stance", "encouraging")

            mc "Not at all. You'd look amazing in it."
            gf "You answered that, like, suspiciously fast."
            mc "You asked! That's my opinion."
            gf "I did."
            "She looked at the bolder swimsuit again, this time with the beginning of a smile."
            gf "Okay. Then I'm actually wearing it."

        "[ch01_outfit_comfort_text]":
            $ apply_choice("ch01_outfit_comfort")
            $ set_story_value("ch01_outfit_stance", "neutral")
            $ neutral_outfit = resolve_story_outcome("ch01_pool_outfit", ["pool_conservative", "pool_bolder"], weights=[65, 35])

            mc "Wear whichever one makes you comfortable."
            gf "That's so supportive and so completely useless, you know that?"
            mc "Yeah, I... heard it as I said it."

            if neutral_outfit == "pool_bolder":
                gf "...I think I want to try the new one."
                mc "Then try it."
                gf "If I spend the whole afternoon adjusting it, this is your fault."
            else:
                gf "I might save the new one for when I feel less like I'm wearing a spotlight."
                mc "You don't have to prove anything on day one."
                gf "Yeah. Okay. Usual one first, and the new one can wait until I'm feeling brave."

        "[ch01_outfit_conservative_text]":
            $ apply_choice("ch01_outfit_conservative")
            $ set_story_value("ch01_pool_outfit", "pool_conservative")
            $ set_story_value("ch01_outfit_stance", "protective")

            mc "I kinda like the other one on you more."
            gf "Wait, the safe one? Really?"
            mc "I mean... yeah. I already know that one looks good on you."
            gf "Aw. That's kind of sweet, actually. I did ask."
            "She folded the new swimsuit back into the suitcase without making it feel like a defeat."
            gf "I'll go with the usual one today."

        "[ch01_outfit_rush_text]":
            $ apply_choice("ch01_outfit_rush")
            $ set_story_value("ch01_pool_outfit", "pool_conservative")
            $ set_story_value("ch01_outfit_stance", "rushed")

            mc "They both look fine, babe. Honestly. [friend_name]'s already at the pool."
            gf "Wow. Okay. 'Fine.'"
            mc "Good! I meant good. They both look good."
            "She looked at the new one for another second, then put it back in the suitcase."
            gf "Usual one, then. It's quicker."

    $ selected_pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
    $ grant_story_outfit(selected_pool_outfit, equip=True)

    $ exit_cinematic_mode()
    scene bg ch01_master_bedroom
    with dissolve
    $ cast(ryan="casual", leia="casual", julian="travel")

    $ lc_sfx("door_close")
    "Swimsuit decided, [girlfriend_name] gathered it up and disappeared into the bathroom to change."
    gf "Two minutes! I swear, two minutes."

    $ cast_remove("leia")

    # Same room, a few minutes later: Ryan stays put and Leia walks back in.
    $ cast_add(leia="towel")
    $ face("leia", "neutral")

    $ lc_sfx("door_open")
    "A moment later, the bathroom door opened again."
    "[girlfriend_name] stepped back into the bedroom with a towel wrapped around herself and crossed to the glass wall."

    $ enter_cinematic_mode()
    scene cg ch01_bedroom_window
    with dissolve

    gf "Wait, wait. I'm closing these first. I'm not giving the whole beach a free show."

    $ lc_sfx("curtain")
    "She caught one of the light curtains and pulled it across the window."

    $ exit_cinematic_mode()
    scene bg ch01_master_bedroom_curtains
    with dissolve
    $ cast(ryan="casual", leia="towel", julian="travel")

    gf "...Okay, seriously?"
    mc "What?"
    gf "These are, like, see-through. What's even the point of a curtain you can see through?"
    mc "I think they're more of a... I mean, decorative? For the vibe?"
    gf "For the vibe. Great. Thank you, that's super helpful."

    "The thin fabric softened the view more than it actually blocked it."
    "I looked at the curtain, then at the towel wrapped around her."

    "{i}That barely covers anything either.{/i}"

    gf "What? Why are you looking at me like that?"
    mc "I'm not— okay, I was. Sorry. You just look really good, that's all."
    gf "I'm literally in a towel. My hair's dripping all over the floor, I look like a drowned cat."
    mc "Yeah. Still."
    $ face("leia", "smile")
    "She laughed and pulled the towel tighter, though she didn't look like she minded."
    gf "Oh my God, you're such a perv. Okay, I'm going to go put this on before you get any ideas."
    gf "Turn around. Or don't, whatever, it's not like you haven't seen it."
    mc "Turning. I'm turning. Mostly."

    $ lc_sfx("door_close")
    "She was smiling when she turned back toward the bathroom."
    mc "That's four minutes, by the way. Five. We're on five, babe."

    $ cast_remove("leia")

    $ set_story_flag("ch01_first_outfit_choice_complete")
    $ set_story_flag("ch01_scene_03_complete")

    if selected_pool_outfit == "pool_bolder":
        $ lc_sfx("door_open")
        "A few minutes later, [girlfriend_name] stepped out in the new swimsuit."
        $ enter_cinematic_mode()
        scene cg ch01_swimsuit_choice_blue
        with dissolve
        $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)
        gf "Well? Say something, I'm just standing here."
        mc "Wow. I don't— yeah. You look amazing."
        gf "Stop. ...But, like, really? Good."
        $ exit_cinematic_mode()
        scene bg ch01_master_bedroom_curtains
        with dissolve
        $ cast(ryan="casual", leia="blue_bikini", julian="travel")
        $ face("leia", "smile")
    else:
        $ lc_sfx("door_open")
        "A few minutes later, [girlfriend_name] stepped out in the swimsuit she already trusted."
        $ enter_cinematic_mode()
        scene cg ch01_swimsuit_choice_white
        with dissolve
        $ lc_breath_once()  # Leia's soft inhale on her CG (darryn)
        gf "Comfort first. I don't want to spend the whole day fixing straps."
        mc "You still look incredible. I mean it."
        gf "Good answer. You can carry the sunscreen."
        $ exit_cinematic_mode()
        scene bg ch01_master_bedroom_curtains
        with dissolve
        $ cast(ryan="casual", leia="white_ruffle", julian="travel")
        $ face("leia", "smile")

    "From downstairs, [friend_name] called that the pool—and the cold drinks—were waiting."

    if selected_pool_outfit == "pool_bolder":
        $ cast_remove("leia")
    else:
        $ cast_remove("leia")

    $ set_story_flag("ch01_scenes_01_03_complete")


    jump ch01_scene_04_pool_arrival

