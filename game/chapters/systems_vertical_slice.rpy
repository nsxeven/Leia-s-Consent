# Integrated Phase 9 systems vertical slice.
# This is intentionally a development story sequence, not Chapter 1 canon.
# It proves that the reusable systems can cooperate in one continuous flow.

label dev_vertical_slice:

    scene bg dev
    show leia

    "PHASE 9 — INTEGRATED SYSTEMS SLICE"
    "This short non-canon sequence connects dialogue, choice effects, money, shopping, wardrobe acceptance, sprite state, branching dialogue, Gallery unlocks, and save/load."

    $ set_leia_sprite("p01", "neutral")

    gf "You said you wanted to pick something out for tonight?"
    mc "Only if you're actually comfortable with it."

    $ slice_choice_open = format_choice("dev_encourage_curiosity", "Encourage {} to explore something new".format(girlfriend_name))
    $ slice_choice_careful = format_choice("dev_be_protective", "Keep things familiar and comfortable")

    menu:
        "[slice_choice_open]":
            $ apply_choice("dev_encourage_curiosity")
            $ set_leia_expression("smile")
            gf "Okay. Looking doesn't mean I have to wear anything, right?"
            mc "Right. You decide."

        "[slice_choice_careful]":
            $ apply_choice("dev_be_protective")
            $ set_leia_expression("neutral")
            gf "Maybe something simple, then. I like that you're not trying to rush me."

    "The choice has now changed the real central stats and has been recorded in choice history."

    if not dev_vertical_slice_reward_claimed:
        $ earn_money(400, "Integrated slice wardrobe budget")
        $ dev_vertical_slice_reward_claimed = True
        "For this development slice, you receive a one-time $400 wardrobe budget. Current money: $[money]."
    else:
        "The development wardrobe budget was already claimed. Current money: $[money]."

    mc "Let's see what's available."
    call screen shop_screen

    "Buy whichever outfit you want to test. Purchasing it only adds it to the Wardrobe; it does not bypass [girlfriend_name]'s comfort requirements."
    call screen wardrobe_screen

    if equipped_outfit == "after_hours_dress":
        $ set_leia_pose("p02")
        $ set_leia_expression("teasing")
        gf "It's definitely bolder than what I'd normally pick... but I said yes."
        mc "And that's the part that matters."
    elif equipped_outfit == "date_night_dress":
        $ set_leia_pose("p02")
        $ set_leia_expression("smile")
        gf "This one feels like me. Just a little more dressed up."
        mc "You look good in it."
    else:
        $ set_leia_pose("p03")
        $ set_leia_expression("embarrassed")
        gf "I think I'll stay in this for now."
        mc "That's completely fine."

    "The dialogue above branched from the actual equipped outfit, and the same outfit state is controlling the visible Leia sprite."

    $ unlock_gallery("ch01_cg01")
    "Development Gallery milestone unlocked: Chapter 1 — CG 01 placeholder."

    call screen gallery_screen

    jump dev_vertical_slice_checkpoint


label dev_vertical_slice_checkpoint:

    scene bg dev
    show leia

    "INTEGRATION CHECKPOINT"
    "Current state: $[money] • [current_outfit_name()] • [leia_pose_label()] • [leia_expression_label()]"
    "Last choice: [last_choice_id] • Recorded choices: [len(choice_history)]"

    menu:
        "Open Status":
            call screen status_screen
            jump dev_vertical_slice_checkpoint

        "Open Wardrobe":
            call screen wardrobe_screen
            jump dev_vertical_slice_checkpoint

        "Open Shop":
            call screen shop_screen
            jump dev_vertical_slice_checkpoint

        "Open Gallery":
            call screen gallery_screen
            jump dev_vertical_slice_checkpoint

        "Open Transparency Settings":
            call screen player_settings_screen
            jump dev_vertical_slice_checkpoint

        "Open Developer Panel":
            call screen dev_panel
            jump dev_vertical_slice_checkpoint

        "Save/load checkpoint instructions":
            "Open Save from the quick menu and save this exact checkpoint. Quit the game completely, reopen it, and load that save."
            "After loading, this checkpoint should resume with the same money, outfit, Leia pose/expression, stats, and choice history. The Gallery unlock and transparency preference should also still exist because they are persistent."
            jump dev_vertical_slice_checkpoint

        "Restart the integrated slice":
            jump dev_vertical_slice

        "Back to systems menu":
            hide leia
            jump dev_systems_menu
