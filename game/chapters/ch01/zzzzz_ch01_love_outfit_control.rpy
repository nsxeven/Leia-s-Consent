# Love-route outfit-control integration for Chapter 1.
#
# Day One Scene 3 already lets Ryan directly request either swimsuit before a
# route exists. From route-aware outfit prompts onward, Love can unlock the
# broader picker implemented in game/systems/love_outfit_control.rpy.

init 1005 python:
    config.label_overrides["ch01_day2_scene_20_dinner_outfit"] = "ch01_day2_scene_20_dinner_outfit_love_control"


label ch01_day2_scene_20_dinner_outfit_love_control:

    $ d2_lane = ch01_d2_route_lane()

    if d2_lane == "love":
        "Leia came downstairs with two outfits draped over one arm, Maya following behind her."

        gf "Babe, help me pick?"
        maya "Oh, we're outsourcing now?"
        gf "He has opinions. I may as well make them useful."

        menu:
            "Let me choose your outfit.":
                python:
                    d2_love_outfit_options = love_outfit_candidates(
                        story_ids=("resort_dinner_dress", "d2_loose_low_cut"),
                    )
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
                    set_story_flag("ch01_d2_love_outfit_control_used")

                mc "Wear the [outfit_name(d2_love_outfit_pick)]."
                gf "Okay."

                if love_outfit_is_daring(d2_love_outfit_pick):
                    maya "No argument?"
                    gf "I asked him to pick."
                    maya "Dangerous precedent."
                    gf "He'll enjoy it more than I will."
                    mc "Correct."
                else:
                    maya "Good choice."
                    gf "See? Occasionally useful."
                    mc "High praise."

            "Wear whatever you feel best in.":
                $ set_story_value("ch01_d2_dinner_outfit", "secure_date")
                $ set_story_value("ch01_d2_dinner_outfit_id", "resort_dinner_dress")
                $ grant_story_outfit("resort_dinner_dress", equip=True)

                mc "Wear whatever you feel best in."
                gf "Then I'm choosing comfort."
                maya "Healthy. Suspiciously healthy."
                gf "Ignore her."

    elif d2_lane in ("exhibitionism", "ntr_risk"):
        "Leia held up a loose, low-cut evening top with a fitted skirt. The neckline moved noticeably whenever she leaned forward."
        maya "That one is dangerous."
        gf "Dangerous?"
        maya "In the sense that you'll spend the whole night pretending you don't know exactly what it does."
        gf "I have no idea what you're talking about."
        maya "Sure."
        $ set_story_value("ch01_d2_dinner_outfit", "loose_low_cut")
        $ set_story_value("ch01_d2_dinner_outfit_id", "d2_loose_low_cut")

        # Final dedicated layer is pending; the base route continues using the
        # existing dinner-dress placeholder until that asset is replaced.
        $ grant_story_outfit("resort_dinner_dress", equip=True)

    else:
        "Leia chose a polished dinner outfit she could forget about once she put it on."
        maya "Cute."
        gf "Comfortable."
        maya "Also valid."
        $ set_story_value("ch01_d2_dinner_outfit", "secure_date")
        $ set_story_value("ch01_d2_dinner_outfit_id", "resort_dinner_dress")
        $ grant_story_outfit("resort_dinner_dress", equip=True)

    $ set_story_value("ch01_d2_route_lane_dinner", d2_lane)
    $ set_story_flag("ch01_d2_scene_20_complete")
    jump ch01_day2_scene_21_pre_sunset
