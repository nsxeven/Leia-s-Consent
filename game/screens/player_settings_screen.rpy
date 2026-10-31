# Player-facing gameplay settings.
# V1 focuses on Information Transparency; audio/text preferences remain in Ren'Py Preferences for now.

screen transparency_mode_card(mode_id):

    $ current_mode = current_choice_mode()
    $ info = transparency_mode_info(mode_id)
    $ selected = current_mode == mode_id

    frame:
        xsize 520
        ysize 255
        background (Frame("gui/scrapbook/frame_card_on.png", 9, 9) if selected else Frame("gui/scrapbook/frame_card.png", 9, 9))
        padding (24, 22)

        vbox:
            spacing 11
            xfill True

            hbox:
                xfill True
                text info["label"].upper() size 27 color "#3b2a30"

                if selected:
                    text "SELECTED" size 15 color "#cc0066" xalign 1.0

            text info["tagline"] size 19 color "#d5c1cf"
            text info["description"] size 17 color "#7a6266" line_spacing 3

            null height 4

            if selected:
                text "Current mode" size 17 color "#cc0066"
            else:
                textbutton "Use this mode":
                    action Function(set_player_transparency_mode, mode_id)


screen transparency_detail_row(label, description):

    hbox:
        spacing 20
        xfill True

        text label size 19 color "#3b2a30" xsize 120
        text description size 17 color "#7a6266" xfill True


screen player_settings_screen():

    modal True
    zorder 185

    key "K_ESCAPE" action Return()

    $ current_mode = current_choice_mode()
    $ current_info = transparency_mode_info(current_mode)
    $ visibility_rows = transparency_visibility_rows(current_mode)

    add "gui/scrapbook/bg_game_menu.png"
    use lc_journal_tabs(1686)

    frame:
        xpos 70
        ypos 48
        xsize 1580
        ysize 900
        background None
        padding (28, 18)

        vbox:
            spacing 20
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "GAMEPLAY SETTINGS" size 46 color "#3b2a30"
                    text "Information Transparency" size 21 color "#d3c3cf"

                vbox:
                    xalign 1.0
                    spacing 7
                    text "Current: [transparency_mode_label()]" size 20 color "#7a6266" xalign 1.0
                    textbutton "Close":
                        xalign 1.0
                        action Return()

            use lc_scroll_body:

                vbox:
                    spacing 20
                    xfill True

                    text "Visibility modes change what information is shown. Full Transparency also offers an OPTIONAL Route Explorer which can deliberately change stats and upcoming story branches." size 19 color "#7a6266"

                    hbox:
                        spacing 18
                        xfill True

                        for mode_id in PLAYER_TRANSPARENCY_MODES:
                            use transparency_mode_card(mode_id)

                    use lc_review_settings

                    if current_mode == "full":
                        frame:
                            xfill True
                            background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
                            padding (20, 16)
                            vbox:
                                spacing 9
                                text "ROUTE EXPLORER" size 23 color "#3b2a30"
                                text "Switch Love / Exhibitionism / NTR direction while playing. This changes future route checks; past scenes are not replayed." size 17 color "#5a4030"
                                textbutton "Open Route Explorer":
                                    action Show("lc_route_explorer_screen")

                    if current_mode == "developer":
                        frame:
                            xfill True
                            background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
                            padding (20, 13)

                            text "Developer override is currently active. Selecting any player mode above will return to the normal player-facing transparency system." size 17 color "#6a2338"

                    elif current_mode == "full":
                        frame:
                            xfill True
                            background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
                            padding (20, 13)

                            text "Full Transparency can reveal relationship trends or progression requirements before they become obvious through the story." size 17 color "#5a4030"

                    hbox:
                        spacing 20
                        xfill True

                        frame:
                            xsize 760
                            background Frame("gui/scrapbook/frame_card.png", 9, 9)
                            padding (26, 22)

                            vbox:
                                spacing 17
                                xfill True

                                text "WHAT YOU'LL SEE" size 27 color "#3b2a30"
                                text current_info["description"] size 17 color "#7a6266" line_spacing 3

                                for label, description in visibility_rows:
                                    use transparency_detail_row(label, description)

                        frame:
                            xfill True
                            background Frame("gui/scrapbook/frame_card.png", 9, 9)
                            padding (26, 22)

                            vbox:
                                spacing 14
                                xfill True

                                text "LIVE EXAMPLES" size 27 color "#3b2a30"
                                text "These examples update immediately when you change modes." size 16 color "#7a6266"

                                frame:
                                    xfill True
                                    background Frame("gui/scrapbook/frame_card.png", 9, 9)
                                    padding (18, 15)

                                    vbox:
                                        spacing 7
                                        text "CHOICE" size 17 color "#cc0066"
                                        text "[transparency_choice_preview()]" size 18 color "#3b2a30" line_spacing 3

                                frame:
                                    xfill True
                                    background Frame("gui/scrapbook/frame_card.png", 9, 9)
                                    padding (18, 15)

                                    vbox:
                                        spacing 7
                                        text "STATUS" size 17 color "#cc0066"
                                        text "[transparency_status_preview()]" size 18 color "#3b2a30"

                                frame:
                                    xfill True
                                    background Frame("gui/scrapbook/frame_card.png", 9, 9)
                                    padding (18, 15)

                                    vbox:
                                        spacing 7
                                        text "WARDROBE" size 17 color "#cc0066"
                                        text "[transparency_wardrobe_preview()]" size 16 color "#3b2a30" line_spacing 3

                    null height 20

