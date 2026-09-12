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


# Compatibility entry point retained from the first development milestone.
label dev_sandbox:
    jump dev_systems_menu


label dev_systems_menu:

    scene bg dev

    gf "The Leia's Consent development sandbox is running."
    mc "Choose which system you want to test."

    menu:
        "Integrated systems slice (Phase 9)":
            jump dev_vertical_slice

        "Gallery shell test":
            jump dev_gallery_test

        "Player Settings / Transparency test":
            call screen player_settings_screen
            jump dev_systems_menu

        "Player Status screen test":
            call screen status_screen
            jump dev_systems_menu

        "Sprite System test":
            jump dev_sprite_test

        "Economy + Wardrobe test":
            jump dev_economy_wardrobe_test

        "Choice Engine test":
            jump dev_choice_intro

        "Open Developer Panel":
            call screen dev_panel
            jump dev_systems_menu

        "Open verification / save-state menu":
            jump dev_verify_state

        "Finish systems test and return to the main menu":
            return


label dev_gallery_test:

    scene bg dev

    "The Gallery shell uses persistent unlocks. These belong to the player profile rather than one save slot."
    "Final CG art and replay labels do not exist yet, so this test uses placeholder cards and previews."

    jump dev_gallery_lab


label dev_gallery_lab:

    menu:
        "Open Gallery":
            call screen gallery_screen
            jump dev_gallery_lab

        "Unlock Chapter 1 — CG 01":
            $ debug_unlock_gallery_entry("ch01_cg01")
            jump dev_gallery_lab

        "Unlock all placeholder CGs":
            $ debug_unlock_all_gallery()
            jump dev_gallery_lab

        "Reset all Gallery unlocks":
            $ debug_reset_gallery()
            jump dev_gallery_lab

        "Show Gallery unlock state":
            $ unlocked_gallery_names = [get_gallery_entry(gallery_id)["title"] for gallery_id in gallery_all_ids() if is_gallery_unlocked(gallery_id)]
            $ unlocked_gallery_text = ", ".join(unlocked_gallery_names) if unlocked_gallery_names else "None"
            "Unlocked: [gallery_unlocked_count()] / [gallery_total_count()]\nEntries: [unlocked_gallery_text]"
            jump dev_gallery_lab

        "How do I test persistence?":
            "Unlock at least one CG, quit the game completely, reopen it, start or load any playthrough, and return here. The Gallery unlock should still be present."
            "Gallery unlocks are intentionally persistent across save slots and New Game."
            jump dev_gallery_lab

        "Back to systems menu":
            jump dev_systems_menu


label dev_sprite_test:

    scene bg dev
    show leia

    gf "This is placeholder art. We're testing whether my pose, expression, and wardrobe state can work as one sprite system."

    "Pose and expression belong to the sprite controller. Outfit is deliberately inherited from the existing Wardrobe system."

    jump dev_sprite_lab


label dev_sprite_lab:

    menu:
        "Open pose + expression controls":
            call screen sprite_lab_controls
            jump dev_sprite_lab

        "Open Wardrobe to change the visible outfit":
            call screen wardrobe_screen
            jump dev_sprite_lab

        "Unlock all current outfits for sprite testing":
            $ debug_unlock_all_outfits()
            "All current outfits are now owned. Use Wardrobe to equip one. Normal wear requirements still apply."
            jump dev_sprite_lab

        "Open Developer Panel":
            call screen dev_panel
            jump dev_sprite_lab

        "Show exact sprite state":
            "Pose: [leia_pose] ([leia_pose_label()])\nExpression: [leia_expression] ([leia_expression_label()])\nOutfit ID: [equipped_outfit]\nOutfit: [current_outfit_name()]"
            jump dev_sprite_lab

        "How do I test outfit switching?":
            "Unlock or purchase an outfit, then equip it through Wardrobe. When the Wardrobe closes, the placeholder clothing layer on [girlfriend_name] should already be different."
            "If After Hours Dress is refused, either satisfy one of its wear paths or use the Developer Panel to raise the required stats."
            jump dev_sprite_lab

        "Continue to save/load verification":
            jump dev_verify_state

        "Back to systems menu":
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

    "The choice was applied using the central choice-effect table rather than hard-coded stat changes in this scene."
    call screen dev_panel
    jump dev_verify_state


label dev_economy_wardrobe_test:

    scene bg dev

    "This test keeps buying and wearing separate. An outfit can be owned even when [girlfriend_name] is not yet comfortable wearing it."

    if not dev_wardrobe_reward_claimed:
        $ earn_money(250, "Wardrobe test allowance")
        $ dev_wardrobe_reward_claimed = True
        "Economy test: you received a one-time $250 wardrobe allowance. You now have $[money]."
    else:
        "The one-time wardrobe allowance was already claimed. Current money: $[money]."

    "Open the shop. Try buying Date Night Dress and After Hours Dress."
    call screen shop_screen

    "Date Night Dress has no comfort gate. After Hours Dress is intentionally more demanding and should be refused at the default stats."
    jump dev_wardrobe_lab


label dev_wardrobe_lab:

    menu:
        "Open Outfit Shop":
            call screen shop_screen
            jump dev_wardrobe_lab

        "Open Wardrobe":
            call screen wardrobe_screen
            jump dev_wardrobe_lab

        "Open Player Transparency Settings":
            call screen player_settings_screen
            jump dev_wardrobe_lab

        "Open Developer Panel":
            call screen dev_panel
            jump dev_wardrobe_lab

        "Show current economy + wardrobe state":
            $ owned_name_list = ", ".join(outfit_name(outfit_id) for outfit_id in valid_owned_outfit_ids())
            "Money: $[money]\nOwned: [owned_name_list]\nEquipped: [current_outfit_name()]\nLast wear path: [last_wear_route]"
            if last_money_reason:
                "Last money change: [last_money_change] ([last_money_reason])"
            jump dev_wardrobe_lab

        "How do I test the gated outfit?":
            "First buy After Hours Dress, then ask [girlfriend_name] to wear it at the default stats. It should be refused."
            "Use Player Transparency Settings to compare Immersive, Insight, and Full Transparency. For the internal PASS/FAIL view, use Developer mode from the Choice Engine test."
            "For the quickest successful path, raise Curiosity to at least 30 and Exhibitionism to at least 20 in the Developer Panel, then ask her to wear it again."
            jump dev_wardrobe_lab

        "Continue to save/load verification":
            jump dev_verify_state

        "Back to systems menu":
            jump dev_systems_menu


label dev_verify_state:

    menu:
        "Open Integrated systems slice":
            jump dev_vertical_slice

        "Open Gallery":
            call screen gallery_screen
            jump dev_verify_state

        "Open Player Settings / Transparency":
            call screen player_settings_screen
            jump dev_verify_state

        "Open Player Status screen":
            call screen status_screen
            jump dev_verify_state

        "Show current character names":
            "You: [player_name]\nGirlfriend: [girlfriend_name]\nFriend: [friend_name]"
            jump dev_verify_state

        "Open Sprite System test":
            jump dev_sprite_test

        "Show sprite state":
            "Pose: [leia_pose] ([leia_pose_label()])\nExpression: [leia_expression] ([leia_expression_label()])\nOutfit ID: [equipped_outfit]\nOutfit: [current_outfit_name()]"
            jump dev_verify_state

        "Open Developer Panel":
            call screen dev_panel
            jump dev_verify_state

        "Open Developer Choice Display controls":
            call screen choice_mode_screen
            jump dev_verify_state

        "Show recorded choice state":
            "Last choice ID: [last_choice_id]\nChoices recorded this playthrough: [len(choice_history)]"
            jump dev_verify_state

        "Open Outfit Shop":
            call screen shop_screen
            jump dev_verify_state

        "Open Wardrobe":
            call screen wardrobe_screen
            jump dev_verify_state

        "Show economy + wardrobe state":
            $ owned_name_list = ", ".join(outfit_name(outfit_id) for outfit_id in valid_owned_outfit_ids())
            "Money: $[money]\nOwned: [owned_name_list]\nEquipped: [current_outfit_name()]\nLast wear path: [last_wear_route]"
            jump dev_verify_state

        "Repeat save/load instructions":
            "While this verification menu is active, open Save from the quick menu. Save to a slot, quit the game completely, reopen it, choose Load, and load that slot."
            "After loading, confirm your names, money, owned outfits, equipped outfit, sprite pose/expression, stats, and choice history all survived."
            "Transparency and Gallery unlocks are player-wide preferences/progression, so confirm they also survive restarting the game and moving between save slots."
            jump dev_verify_state

        "Back to systems menu":
            jump dev_systems_menu

        "Finish systems test and return to the main menu":
            return
