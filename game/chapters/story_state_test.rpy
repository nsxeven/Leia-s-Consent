# Development-only test flow for the story-state foundation.

label dev_story_state_test:

    scene bg dev

    $ story_action = renpy.call_screen("dev_story_state_screen")

    if story_action == "set_flag":
        $ set_story_flag("dev_demo_flag")
        $ renpy.notify("Story flag dev_demo_flag = True")
        jump dev_story_state_test

    elif story_action == "clear_flag":
        $ clear_story_flag("dev_demo_flag")
        $ renpy.notify("Story flag dev_demo_flag cleared")
        jump dev_story_state_test

    elif story_action == "resolve_pool":
        $ dev_pool_result = resolve_story_outcome("dev_pool_outfit", ["pool_conservative", "pool_bolder"], [60, 40])
        $ renpy.notify("Resolved pool outfit: {} (repeat clicks must stay the same)".format(dev_pool_result))
        jump dev_story_state_test

    elif story_action == "show_state":
        $ renpy.notify(story_state_summary())
        jump dev_story_state_test

    elif story_action == "choice_encourage":
        $ apply_choice("dev_encourage_curiosity")
        $ renpy.notify("Tagged choice recorded: encouraging / participating / open")
        jump dev_story_state_test

    elif story_action == "choice_protective":
        $ apply_choice("dev_be_protective")
        $ renpy.notify("Tagged choice recorded: protective / cautious")
        jump dev_story_state_test

    elif story_action == "show_tags":
        $ dev_tag_counts = choice_tag_counts()
        $ dev_tag_text = ", ".join("{}={}".format(key, dev_tag_counts[key]) for key in sorted(dev_tag_counts)) if dev_tag_counts else "None"
        $ renpy.notify("Stance: {} | Tags: {}".format(choice_stance(), dev_tag_text))
        jump dev_story_state_test

    elif story_action == "grant_conservative":
        $ grant_story_outfit("pool_conservative", equip=True)
        $ set_story_value("dev_pool_outfit", "pool_conservative")
        $ renpy.notify("Granted + equipped Classic Resort Swimwear")
        jump dev_story_state_test

    elif story_action == "grant_bolder":
        $ grant_story_outfit("pool_bolder", equip=True)
        $ set_story_value("dev_pool_outfit", "pool_bolder")
        $ renpy.notify("Granted + equipped Bolder Resort Swimwear")
        jump dev_story_state_test

    elif story_action == "wardrobe":
        call screen wardrobe_screen
        jump dev_story_state_test

    elif story_action == "reset":
        $ debug_reset_story_state()
        jump dev_story_state_test

    else:
        jump dev_systems_menu
