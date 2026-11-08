# Player-facing status screen.
# The active transparency mode controls how much of the internal state is revealed.

screen status_stat_row(row):

    # Focusable so the stat explanation shows on hover and keyboard/controller
    # focus; the card itself is drawn by lc_stat_tip at the end of the screen.
    button:
        style "lc_stat_tip_row"
        tooltip row.get("tooltip")
        action NullAction()

        vbox:
            spacing 5
            xfill True

            hbox:
                xfill True
                spacing 8

                if row["stat"] in LC_STAT_ICON:
                    add Transform("images/ui/scrapbook/icon_{}.png".format(LC_STAT_ICON[row["stat"]]), xysize=(28, 28)) yalign 0.5
                text row["label"] size 21 color "#3b2a30" yalign 0.5

                if row["detail"]:
                    text row["detail"] size 18 color "#7a6266" xalign 1.0

            bar:
                value StaticValue(row["value"], 100)
                xfill True
                ysize 16
                left_bar Frame("gui/scrapbook/bar_love.png", 6, 6)
                right_bar Frame("gui/scrapbook/bar_track.png", 6, 6)

            if row["internal_key"]:
                text row["internal_key"] size 15 color "#7a6266"


screen status_section(title, rows):

    frame:
        xfill True
        background Frame("gui/scrapbook/frame_card.png", 9, 9)
        padding (24, 22)

        vbox:
            spacing 17
            xfill True

            text title size 26 color "#3b2a30"

            for row in rows:
                use status_stat_row(row)


screen status_screen(return_to=None):
    tag menu
    modal (not lc_ui_shooting)
    zorder 180

    # A menu tab replaces its previous menu page; a call screen still returns.
    $ _status_close = ShowMenu(return_to) if return_to else Return()
    key "K_ESCAPE" action _status_close
    key "game_menu" action _status_close

    $ mode = current_choice_mode()
    $ relationship_rows = status_relationship_rows(mode)
    $ leia_rows = status_leia_rows(mode)
    $ ryan_rows = status_ryan_rows(mode)
    $ route_rows = status_route_rows(mode)

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
            spacing 22
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "STATUS" size 46 color "#3b2a30"
                    text "A snapshot of your relationship and where things currently stand." size 19 color "#7a6266"

                vbox:
                    xalign 1.0
                    spacing 8

                    text "Display: [transparency_mode_label()]" size 20 color "#7a6266" xalign 1.0

                    textbutton "Close":
                        xalign 1.0
                        action _status_close

            use lc_scroll_body:

                vbox:
                    spacing 22
                    xfill True

                    frame:
                        xfill True
                        background Frame("gui/scrapbook/frame_card.png", 9, 9)
                        padding (26, 20)

                        vbox:
                            spacing 9

                            hbox:
                                xfill True
                                text "[girlfriend_name] right now" size 27 color "#3b2a30"
                                text "Current outfit: [current_outfit_name()]" size 18 color "#7a6266" xalign 1.0

                            text "[leia_overview_text()]" size 20 color "#3b2a30" line_spacing 4

                    if persistent.lc_title_style != "off":
                        $ lc_status_titles = lc_current_titles()
                        text (player_name + " · " + lc_status_titles[0]) size 21 color "#cc0066" substitute False
                        text (girlfriend_name + " · " + lc_status_titles[1]) size 21 color "#cc0066" substitute False
                    if lc_review_latest():
                        textbutton "Review last completed day":
                            action Show("lc_review_history_screen", day_id=lc_review_latest())

                    text "[status_mode_note()]" size 17 color "#7a6266"
                    text "Hover over a stat to see what it means." size 17 color "#7a6266"

                    hbox:
                        spacing 20
                        xfill True

                        vbox:
                            spacing 20
                            xsize 525

                            use status_section("RELATIONSHIP", relationship_rows)

                        vbox:
                            spacing 20
                            xsize 525

                            use status_section(girlfriend_name.upper(), leia_rows)

                        vbox:
                            spacing 20
                            xsize 525

                            use status_section(player_name.upper(), ryan_rows)

                            if route_rows:
                                use status_section("ROUTE TENDENCIES", route_rows)

                    null height 20

    # Stat explanation card for the focused row (status_stat_row tooltips).
    use lc_stat_tip(GetTooltip("status_screen"))

