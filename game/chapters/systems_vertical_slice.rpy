# Integrated Phase 9 systems vertical slice.
# This is intentionally a development story sequence, not Chapter 1 canon.
# It proves that the reusable systems can cooperate in one continuous flow.

label dev_vertical_slice:

    scene bg dev

    "PHASE 9 — INTEGRATED SYSTEMS SLICE"
    "This short non-canon sequence connects dialogue, choice effects, money, shopping, wardrobe acceptance, branching dialogue, Gallery unlocks, and save/load."


    gf "You said you wanted to pick something out for tonight?"
    mc "Only if you're actually comfortable with it."

    $ slice_choice_open = format_choice("dev_encourage_curiosity", "Encourage {} to explore something new".format(girlfriend_name))
    $ slice_choice_careful = format_choice("dev_be_protective", "Keep things familiar and comfortable")

    menu:
        "[slice_choice_open]":
            $ apply_choice("dev_encourage_curiosity")
            gf "Okay. Looking doesn't mean I have to wear anything, right?"
            mc "Right. You decide."

        "[slice_choice_careful]":
            $ apply_choice("dev_be_protective")
            gf "Maybe something simple, then. I like that you're not trying to rush me."

    $ renpy.notify("Choice applied and recorded in central choice history.")

    if not dev_vertical_slice_reward_claimed:
        $ earn_money(400, "Integrated slice wardrobe budget")
        $ dev_vertical_slice_reward_claimed = True
        $ renpy.notify("One-time $400 slice budget added. Money: ${}".format(money))
    else:
        $ renpy.notify("Slice budget already claimed. Money: ${}".format(money))

    mc "Let's see what's available."
    call screen shop_screen

    "Buy whichever outfit you want to test. Purchasing it only adds it to the Wardrobe; it does not bypass [girlfriend_name]'s comfort requirements."
    call screen wardrobe_screen

    if equipped_outfit == "after_hours_dress":
        gf "It's definitely bolder than what I'd normally pick... but I said yes."
        mc "And that's the part that matters."
    elif equipped_outfit == "date_night_dress":
        gf "This one feels like me. Just a little more dressed up."
        mc "You look good in it."
    else:
        gf "I think I'll stay in this for now."
        mc "That's completely fine."

    $ renpy.notify("Outfit state is now driving branch dialogue.")

    $ unlock_gallery("ch01_cg01")
    $ renpy.notify("Gallery unlocked: Chapter 1 — CG 01 placeholder.")

    call screen gallery_screen

    jump dev_vertical_slice_checkpoint


label dev_vertical_slice_checkpoint:

    scene bg dev

    $ dev_notify_checkpoint_state()
    $ checkpoint_action = renpy.call_screen("dev_vertical_slice_checkpoint_screen")

    if checkpoint_action == "status":
        call screen status_screen
        jump dev_vertical_slice_checkpoint
    elif checkpoint_action == "wardrobe":
        call screen wardrobe_screen
        jump dev_vertical_slice_checkpoint
    elif checkpoint_action == "shop":
        call screen shop_screen
        jump dev_vertical_slice_checkpoint
    elif checkpoint_action == "gallery":
        call screen gallery_screen
        jump dev_vertical_slice_checkpoint
    elif checkpoint_action == "settings":
        call screen player_settings_screen
        jump dev_vertical_slice_checkpoint
    elif checkpoint_action == "developer":
        call screen dev_panel
        jump dev_vertical_slice_checkpoint
    elif checkpoint_action == "save_help":
        "Open Save from the quick menu and save this exact checkpoint. Quit the game completely, reopen it, and load that save."
        "After loading, this checkpoint should resume with the same money, outfit, stats, and choice history. The Gallery unlock and transparency preference should also still exist because they are persistent."
        jump dev_vertical_slice_checkpoint
    elif checkpoint_action == "restart":
        jump dev_vertical_slice
    else:
        jump dev_systems_menu
