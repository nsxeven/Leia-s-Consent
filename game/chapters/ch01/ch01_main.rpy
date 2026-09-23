# Leia's Consent — Chapter One: Something Different
# First playable production chunk: Scenes 1–3.

label chapter_one_start:

    $ set_story_flag("ch01_started")
    $ set_phone_hud_enabled(True)

    jump ch01_scene_01_arrival


label ch01_scene_01_arrival:

    scene bg ch01_resort_arrival
    with fade

    "By the time the boat eased against the jetty, [girlfriend_name] had taken thirty-seven photos."
    "Thirty-eight, if the blurry one of [friend_name] asleep in the transfer car counted."

    gf "This place doesn't look real."
    mc "You've said that about the airport, the boat, and a coconut."
    gf "The coconut was very photogenic."

    with dissolve

    "A member of staff greeted [friend_name] by name before any of us reached the end of the jetty."
    "Our bags disappeared onto a cart. Cold towels appeared. So did three drinks none of us remembered ordering."

    mc "Should I be worried that everyone here knows you?"
    friend "They know the booking."
    gf "The booking has a face?"
    friend "Apparently a very trustworthy one."

    "He said it like the private transfer, waiting staff, and seamless arrival were ordinary."
    "That was [friend_name]'s version of showing off: arranging something ridiculous, then acting as though it had happened by accident."

    gf "Wait—don't move. Both of you."
    mc "Another photo?"
    gf "First proper holiday photo. Try to look happy."
    friend "I paid for the villa. I am contractually delighted."

    "I laughed just as she took it."
    "For once, she lowered the phone without checking the result ten times."

    $ set_story_flag("ch01_scene_01_complete")


    jump ch01_scene_02_villa


label ch01_scene_02_villa:

    scene bg ch01_villa_exterior
    with dissolve

    "The cart followed a narrow path through palms and stopped in front of a two-storey villa facing the ocean."

    gf "[friend_name]."
    friend "Yes?"
    gf "This is not a villa. This is a small country."
    friend "The listing said 'intimate.'"
    mc "Compared to what? An airport?"

    scene bg ch01_villa_living
    with dissolve

    "Inside, the living room opened straight toward a private pool, an outdoor lounge, and a strip of beach beyond it."
    "Glass, pale wood, soft furniture—everything looked expensive without trying to announce it."

    with dissolve

    friend "There are two rooms upstairs. You two take the master."
    mc "You booked the place. You take it."
    friend "And listen to you argue through the wall because your room is smaller? No."
    gf "We don't argue."
    mc "We conduct loud relationship reviews."
    gf "He gets poor performance ratings."

    "[friend_name] waved us toward the stairs before I could object again."


    scene bg ch01_master_bedroom
    with dissolve

    "The master bedroom took up most of the second floor."
    "One wall was almost entirely glass, looking down over the pool and past it to the ocean."
    "Light curtains softened the view without quite hiding it. Decorative, more than private."

    with dissolve

    gf "Look at that view."
    mc "I'm looking."
    gf "At the ocean."
    mc "Still looking."

    "She caught my reflection in the glass and rolled her eyes, smiling anyway."

    gf "Where's [friend_name]'s room?"
    mc "Next door. Same view, slightly less country-sized."
    gf "And he still gave us this one?"
    mc "That's [friend_name]."

    "Below us, sunlight moved across the water in the private pool."

    $ set_story_flag("ch01_villa_geography_established")
    $ set_story_flag("ch01_scene_02_complete")

    jump ch01_scene_03_outfit_choice


label ch01_scene_03_outfit_choice:

    scene bg ch01_master_bedroom
    with dissolve

    "Unpacking took less than five minutes. Deciding what to wear took considerably longer."

    gf "Okay. Opinion."
    mc "Dangerous opening."
    gf "I brought two swimsuits."
    gf "The usual one... and one I bought for this trip."

    "She held up the first: flattering, familiar, and comfortable."
    "The second was still normal resort swimwear, just a little bolder than anything she usually wore around our friends."

    gf "Is this one too much with [friend_name] here?"

    $ ch01_outfit_bolder_text = format_choice("ch01_outfit_bolder", "Not at all. You'd look amazing in it.")
    $ ch01_outfit_comfort_text = format_choice("ch01_outfit_comfort", "Wear whichever one makes you comfortable.")
    $ ch01_outfit_conservative_text = format_choice("ch01_outfit_conservative", "I kinda like the other one on you more.")

    menu:
        "[ch01_outfit_bolder_text]":
            $ apply_choice("ch01_outfit_bolder")
            $ set_story_value("ch01_pool_outfit", "pool_bolder")
            $ set_story_value("ch01_outfit_stance", "encouraging")

            mc "Not at all. You'd look amazing in it."
            gf "You answered that suspiciously fast."
            mc "You asked for my opinion."
            gf "I did."
            "She looked at the bolder swimsuit again, this time with the beginning of a smile."
            gf "Okay. Then I'm actually wearing it."

        "[ch01_outfit_comfort_text]":
            $ apply_choice("ch01_outfit_comfort")
            $ set_story_value("ch01_outfit_stance", "neutral")
            $ neutral_outfit = resolve_story_outcome("ch01_pool_outfit", ["pool_conservative", "pool_bolder"], weights=[65, 35])

            mc "Wear whichever one makes you comfortable."
            gf "That is supportive and completely unhelpful."
            mc "I'm talented."

            if neutral_outfit == "pool_bolder":
                gf "...I think I want to try the new one."
                mc "Then try it."
                gf "If I spend the whole afternoon adjusting it, this is your fault."
            else:
                gf "I might save the new one for when I feel less like I'm wearing a spotlight."
                mc "You don't have to prove anything on day one."
                gf "Exactly. Usual one first."

        "[ch01_outfit_conservative_text]":
            $ apply_choice("ch01_outfit_conservative")
            $ set_story_value("ch01_pool_outfit", "pool_conservative")
            $ set_story_value("ch01_outfit_stance", "protective")

            mc "I kinda like the other one on you more."
            gf "The safe one?"
            mc "The one I already know looks good on you."
            gf "Fair. I did ask."
            "She folded the new swimsuit back into the suitcase without making it feel like a defeat."
            gf "I'll go with the usual one today."

    $ selected_pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
    $ grant_story_outfit(selected_pool_outfit, equip=True)

    "Swimsuit decided, [girlfriend_name] gathered it up and disappeared into the bathroom to change."

    $ enter_cinematic_mode()
    scene cg ch01_pre_pool_towel_curtains
    with dissolve

    "A moment later, the bathroom door opened again."
    "[girlfriend_name] stepped back into the bedroom with a towel wrapped around herself and crossed to the glass wall."

    gf "Wait. I'm definitely closing these first."

    "She caught one of the light curtains and pulled it across the window."

    gf "...Seriously?"
    mc "What?"
    gf "These barely cover anything."

    "The thin fabric softened the view more than it actually blocked it."
    "I looked at the curtain, then at the towel wrapped around her."

    "{i}That barely covers anything either.{/i}"

    gf "What?"
    mc "Nothing."
    gf "You have that face."
    mc "I was just thinking you look good."
    gf "I'm wearing a towel."
    mc "Exactly."
    gf "Pervert."

    "She was smiling when she turned back toward the bathroom."

    $ exit_cinematic_mode()
    scene bg ch01_master_bedroom_curtains
    with dissolve

    $ set_story_flag("ch01_first_outfit_choice_complete")
    $ set_story_flag("ch01_scene_03_complete")

    if selected_pool_outfit == "pool_bolder":
        with dissolve
        "A few minutes later, [girlfriend_name] stepped out in the new swimsuit."
        gf "Well?"
        mc "Still think I answered too fast?"
        gf "Maybe not."
    else:
        with dissolve
        "A few minutes later, [girlfriend_name] stepped out in the swimsuit she already trusted."
        gf "Comfort first."
        mc "You still look incredible."
        gf "Correct answer."

    "From downstairs, [friend_name] called that the pool—and the cold drinks—were waiting."

    $ set_story_flag("ch01_scenes_01_03_complete")


    jump ch01_scene_04_pool_arrival
