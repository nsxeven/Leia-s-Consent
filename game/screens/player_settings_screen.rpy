# Player-facing gameplay settings.
# V1 focuses on Information Transparency; audio/text preferences remain in Ren'Py Preferences for now.

screen transparency_mode_card(mode_id):

    $ current_mode = current_choice_mode()
    $ info = transparency_mode_info(mode_id)
    $ selected = current_mode == mode_id

    frame:
        xsize 520
        ysize 255
        background (Solid("#3b2a38") if selected else Solid("#211c25"))
        padding (24, 22)

        vbox:
            spacing 11
            xfill True

            hbox:
                xfill True
                text info["label"].upper() size 27 color "#ffffff"

                if selected:
                    text "SELECTED" size 15 color "#f1a8c8" xalign 1.0

            text info["tagline"] size 19 color "#d5c1cf"
            text info["description"] size 17 color "#b9aabb" line_spacing 3

            null height 4

            if selected:
                text "Current mode" size 17 color "#f1a8c8"
            else:
                textbutton "Use this mode":
                    action Function(set_player_transparency_mode, mode_id)


screen transparency_detail_row(label, description):

    hbox:
        spacing 20
        xfill True

        text label size 19 color "#ffffff" xsize 120
        text description size 17 color "#c8b8c5" xfill True


screen player_settings_screen():

    modal True
    zorder 185

    key "K_ESCAPE" action Return()

    $ current_mode = current_choice_mode()
    $ current_info = transparency_mode_info(current_mode)
    $ visibility_rows = transparency_visibility_rows(current_mode)

    add Solid("#141117")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1740
        ysize 980
        background Solid("#19151d")
        padding (42, 34)

        vbox:
            spacing 20
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "GAMEPLAY SETTINGS" size 46 color "#ffffff"
                    text "Information Transparency" size 21 color "#d3c3cf"

                vbox:
                    xalign 1.0
                    spacing 7
                    text "Current: [transparency_mode_label()]" size 20 color "#e0d4df" xalign 1.0
                    textbutton "Close":
                        xalign 1.0
                        action Return()

            use lc_scroll_body:

                vbox:
                    spacing 20
                    xfill True

                    text "Choose how much of the game's underlying relationship system you want to see. This changes only the information shown to you — never story outcomes, stat changes, or difficulty." size 19 color "#b9aabb"

                    hbox:
                        spacing 18
                        xfill True

                        for mode_id in PLAYER_TRANSPARENCY_MODES:
                            use transparency_mode_card(mode_id)

                    if current_mode == "developer":
                        frame:
                            xfill True
                            background Solid("#3b252d")
                            padding (20, 13)

                            text "Developer override is currently active. Selecting any player mode above will return to the normal player-facing transparency system." size 17 color "#f0cbd8"

                    elif current_mode == "full":
                        frame:
                            xfill True
                            background Solid("#30242e")
                            padding (20, 13)

                            text "Full Transparency can reveal relationship trends or progression requirements before they become obvious through the story." size 17 color "#d7c1cf"

                    hbox:
                        spacing 20
                        xfill True

                        frame:
                            xsize 760
                            background Solid("#211c25")
                            padding (26, 22)

                            vbox:
                                spacing 17
                                xfill True

                                text "WHAT YOU'LL SEE" size 27 color "#ffffff"
                                text current_info["description"] size 17 color "#a99ba8" line_spacing 3

                                for label, description in visibility_rows:
                                    use transparency_detail_row(label, description)

                        frame:
                            xfill True
                            background Solid("#211c25")
                            padding (26, 22)

                            vbox:
                                spacing 14
                                xfill True

                                text "LIVE EXAMPLES" size 27 color "#ffffff"
                                text "These examples update immediately when you change modes." size 16 color "#a99ba8"

                                frame:
                                    xfill True
                                    background Solid("#2b242e")
                                    padding (18, 15)

                                    vbox:
                                        spacing 7
                                        text "CHOICE" size 17 color "#f1a8c8"
                                        text "[transparency_choice_preview()]" size 18 color "#eee7ed" line_spacing 3

                                frame:
                                    xfill True
                                    background Solid("#2b242e")
                                    padding (18, 15)

                                    vbox:
                                        spacing 7
                                        text "STATUS" size 17 color "#f1a8c8"
                                        text "[transparency_status_preview()]" size 18 color "#eee7ed"

                                frame:
                                    xfill True
                                    background Solid("#2b242e")
                                    padding (18, 15)

                                    vbox:
                                        spacing 7
                                        text "WARDROBE" size 17 color "#f1a8c8"
                                        text "[transparency_wardrobe_preview()]" size 16 color "#eee7ed" line_spacing 3

                    null height 20
