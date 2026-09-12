# Temporary systems sandbox.
# This will be removed/replaced once the core mechanics are proven.

image bg dev = Solid("#17151a")


label dev_name_setup:

    scene bg dev

    centered "Personalize your development playthrough"

    $ entered_player_name = renpy.input("Your name", default=player_name, exclude="{}[]", length=20).strip()
    $ player_name = entered_player_name if entered_player_name else "Ryan"

    $ entered_girlfriend_name = renpy.input("Your girlfriend's name", default=girlfriend_name, exclude="{}[]", length=20).strip()
    $ girlfriend_name = entered_girlfriend_name if entered_girlfriend_name else "Leia"

    $ entered_friend_name = renpy.input("Your friend's name", default=friend_name, exclude="{}[]", length=20).strip()
    $ friend_name = entered_friend_name if entered_friend_name else "Julian"

    "You: [player_name]\nGirlfriend: [girlfriend_name]\nFriend: [friend_name]"

    menu:
        "Use these names":
            jump dev_systems_menu

        "Change them again":
            jump dev_name_setup


label dev_sandbox:
    jump dev_systems_menu


label dev_systems_menu:

    scene bg dev
    $ dev_systems_action = renpy.call_screen("dev_systems_menu_screen")

    if dev_systems_action == "vertical_slice":
        jump dev_vertical_slice

    elif dev_systems_action == "gallery":
        jump dev_gallery_test

    elif dev_systems_action == "settings":
        call screen player_settings_screen
        jump dev_systems_menu

    elif dev_systems_action == "status":
        call screen status_screen
        jump dev_systems_menu

    elif dev_systems_action == "sprite":
        jump dev_sprite_test

    elif dev_systems_action == "economy":
        jump dev_economy_wardrobe_test

    elif dev_systems_action == "choice":
        jump dev_choice_intro

    elif dev_systems_action == "developer":
        call screen dev_panel
        jump dev_systems_menu

    elif dev_systems_action == "verify":
        jump dev_verify_state

    else:
        return


label dev_gallery_test:

    scene bg dev

    "The Gallery shell uses persistent unlocks. These belong to the player profile rather than one save slot."
    "Final CG art and replay labels do not exist yet, so this test uses placeholder cards and previews."

    jump dev_gallery_lab


label dev_gallery_lab:

    $ gallery_action = renpy.call_screen("dev_gallery_lab_screen")

    if gallery_action == "open":
        call screen gallery_screen
        jump dev_gallery_lab

    elif gallery_action == "unlock_one":
        $ debug_unlock_gallery_entry("ch01_cg01")
        jump dev_gallery_lab

    elif gallery_action == "unlock_all":
        $ debug_unlock_all_gallery()
        jump dev_gallery_lab

    elif gallery_action == "reset":
        $ debug_reset_gallery()
        jump dev_gallery_lab

    elif gallery_action == "persistence_help":
        "Unlock at least one CG, quit the game completely, reopen it, start or load any playthrough, and return here. The Gallery unlock should still be present."
        "Gallery unlocks are intentionally persistent across save slots and New Game."
        jump dev_gallery_lab

    else:
        jump dev_systems_menu


label dev_sprite_test:

    scene bg dev
    show leia

    gf "This is placeholder art. We're testing whether my pose, expression, and wardrobe state can work as one sprite system."
    "Pose and expression belong to the sprite controller. Outfit is deliberately inherited from the existing Wardrobe system."

    jump dev_sprite_lab


label dev_sprite_lab:

    $ sprite_action = renpy.call_screen("dev_sprite_lab_screen")

    if sprite_action == "controls":
        call screen sprite_lab_controls
        jump dev_sprite_lab

    elif sprite_action == "wardrobe":
        call screen wardrobe_screen
        jump dev_sprite_lab

    elif sprite_action == "developer":
        call screen dev_panel
        jump dev_sprite_lab

    elif sprite_action == "outfit_help":
        "Unlock or purchase an outfit, then equip it through Wardrobe. When the Wardrobe closes, the placeholder clothing layer on [girlfriend_name] should already be different."
        "If After Hours Dress is refused, either satisfy one of its wear paths or use the Developer Panel to raise the required stats."
        jump dev_sprite_lab

    elif sprite_action == "verify":
        jump dev_verify_state

    else:
        hide leia
        jump dev_systems_menu


label dev_choice_intro:

    scene bg dev

    "You can switch between all four choice display modes and watch the live preview change."
    call screen choice_mode_screen
    jump dev_choice_test


label dev_choice_test:

    $ encourage_choice_text = format_choice("dev_encourage_curiosity", "Encourage {}'s curiosity".format(girlfriend_name))
    $ protective_choice_text = format_choice("dev_be_protective", "Be more protective")

    menu:
        "[encourage_choice_text]":
            $ apply_choice("dev_encourage_curiosity")
            gf "You're surprisingly open-minded about this."

        "[protective_choice_text]":
            $ apply_choice("dev_be_protective")
            gf "You're being a little protective today."

    $ renpy.notify("Choice applied and recorded in central choice history.")
    call screen dev_panel
    jump dev_verify_state


label dev_economy_wardrobe_test:

    scene bg dev

    "This test keeps buying and wearing separate. An outfit can be owned even when [girlfriend_name] is not yet comfortable wearing it."

    if not dev_wardrobe_reward_claimed:
        $ earn_money(250, "Wardrobe test allowance")
        $ dev_wardrobe_reward_claimed = True
        $ renpy.notify("One-time wardrobe allowance added. Money: ${}".format(money))
    else:
        $ renpy.notify("Wardrobe allowance already claimed. Money: ${}".format(money))

    "Open the shop. Try buying Date Night Dress and After Hours Dress."
    call screen shop_screen

    "Date Night Dress has no comfort gate. After Hours Dress is intentionally more demanding and should be refused at the default stats."
    jump dev_wardrobe_lab


label dev_wardrobe_lab:

    $ wardrobe_action = renpy.call_screen("dev_wardrobe_lab_screen")

    if wardrobe_action == "shop":
        call screen shop_screen
        jump dev_wardrobe_lab

    elif wardrobe_action == "wardrobe":
        call screen wardrobe_screen
        jump dev_wardrobe_lab

    elif wardrobe_action == "settings":
        call screen player_settings_screen
        jump dev_wardrobe_lab

    elif wardrobe_action == "developer":
        call screen dev_panel
        jump dev_wardrobe_lab

    elif wardrobe_action == "gated_help":
        "First buy After Hours Dress, then ask [girlfriend_name] to wear it at the default stats. It should be refused."
        "Use Player Transparency Settings to compare Immersive, Insight, and Full Transparency. For the internal PASS/FAIL view, use Developer mode from the Choice Engine test."
        "For the quickest successful path, raise Curiosity to at least 30 and Exhibitionism to at least 20 in the Developer Panel, then ask her to wear it again."
        jump dev_wardrobe_lab

    elif wardrobe_action == "verify":
        jump dev_verify_state

    else:
        jump dev_systems_menu


label dev_verify_state:

    $ verify_action = renpy.call_screen("dev_verify_state_screen")

    if verify_action == "vertical_slice":
        jump dev_vertical_slice

    elif verify_action == "gallery":
        call screen gallery_screen
        jump dev_verify_state

    elif verify_action == "settings":
        call screen player_settings_screen
        jump dev_verify_state

    elif verify_action == "status":
        call screen status_screen
        jump dev_verify_state

    elif verify_action == "sprite":
        jump dev_sprite_test

    elif verify_action == "developer":
        call screen dev_panel
        jump dev_verify_state

    elif verify_action == "choice_controls":
        call screen choice_mode_screen
        jump dev_verify_state

    elif verify_action == "shop":
        call screen shop_screen
        jump dev_verify_state

    elif verify_action == "wardrobe":
        call screen wardrobe_screen
        jump dev_verify_state

    elif verify_action == "save_help":
        "While this verification menu is active, open Save from the quick menu. Save to a slot, quit the game completely, reopen it, choose Load, and load that slot."
        "After loading, confirm your names, money, owned outfits, equipped outfit, sprite pose/expression, stats, and choice history all survived."
        "Transparency and Gallery unlocks are player-wide preferences/progression, so confirm they also survive restarting the game and moving between save slots."
        jump dev_verify_state

    elif verify_action == "finish":
        return

    else:
        jump dev_systems_menu
