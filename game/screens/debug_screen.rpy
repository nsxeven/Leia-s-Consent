# Internal development tools.
# This screen is intentionally functional rather than visually polished.

screen dev_panel():

    modal True
    zorder 200

    key "K_ESCAPE" action Return()

    add Solid("#000000aa")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        ysize 940
        padding (35, 30)

        vbox:
            spacing 14

            hbox:
                xfill True

                text "DEVELOPER PANEL" size 38

                textbutton "Close":
                    xalign 1.0
                    action Return()

            text "Prototype tools — values edited here mark the save as modified." size 20
            text "Choice Mode: [choice_mode_label()]   Choices Recorded: [len(choice_history)]" size 20

            if last_choice_id:
                text "Last Choice ID: [last_choice_id]" size 20

            hbox:
                spacing 50
                text "NTS Tendency: [nts_score()]" size 26
                text "NTR Tendency: [ntr_score()]" size 26
                text "Money: $[money]" size 26

            text "Equipped Outfit: [current_outfit_name()]   Owned Outfits: [len(valid_owned_outfit_ids())]" size 20
            if last_wear_route:
                text "Last Wear Path: [last_wear_route]" size 19

            if modified_save:
                text "MODIFIED SAVE" size 20 color "#ff9a9a"

            hbox:
                spacing 12

                textbutton "-$100":
                    action Function(debug_add_money, -100)

                textbutton "+$100":
                    action Function(debug_add_money, 100)

                textbutton "+$1,000":
                    action Function(debug_add_money, 1000)

            hbox:
                spacing 12

                textbutton "Unlock All Outfits":
                    action Function(debug_unlock_all_outfits)

                textbutton "Reset Wardrobe":
                    action Function(debug_reset_wardrobe)

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 12
                    xfill True

                    text "RELATIONSHIP" size 28

                    for stat_name, value in relationship_stats.items():
                        hbox:
                            spacing 12

                            text "[stat_name.replace('_', ' ').title()]: [value]" xminimum 430 size 23

                            textbutton "-5":
                                action Function(debug_change_stat, "relationship", stat_name, -5)

                            textbutton "+5":
                                action Function(debug_change_stat, "relationship", stat_name, 5)

                    null height 10
                    text "LEIA / PARTNER" size 28

                    for stat_name, value in partner_stats.items():
                        hbox:
                            spacing 12

                            text "[stat_name.replace('_', ' ').title()]: [value]" xminimum 430 size 23

                            textbutton "-5":
                                action Function(debug_change_stat, "partner", stat_name, -5)

                            textbutton "+5":
                                action Function(debug_change_stat, "partner", stat_name, 5)

                    null height 10
                    text "RYAN / PLAYER" size 28

                    for stat_name, value in player_stats.items():
                        hbox:
                            spacing 12

                            text "[stat_name.replace('_', ' ').title()]: [value]" xminimum 430 size 23

                            textbutton "-5":
                                action Function(debug_change_stat, "player", stat_name, -5)

                            textbutton "+5":
                                action Function(debug_change_stat, "player", stat_name, 5)
