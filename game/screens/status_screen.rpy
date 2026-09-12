# Player-facing status screen.
# The active transparency mode controls how much of the internal state is revealed.

screen status_stat_row(row):

    vbox:
        spacing 5
        xfill True

        hbox:
            xfill True

            text row["label"] size 21 color "#f3edf4"

            if row["detail"]:
                text row["detail"] size 18 color "#d7c8d4" xalign 1.0

        bar:
            value StaticValue(row["value"], 100)
            xfill True
            ysize 16
            left_bar Solid("#cc5d91")
            right_bar Solid("#3a303d")

        if row["internal_key"]:
            text row["internal_key"] size 15 color "#8f8291"


screen status_section(title, rows):

    frame:
        xfill True
        background Solid("#211c25")
        padding (24, 22)

        vbox:
            spacing 17
            xfill True

            text title size 26 color "#ffffff"

            for row in rows:
                use status_stat_row(row)


screen status_screen():

    modal True
    zorder 180

    key "K_ESCAPE" action Return()

    $ mode = current_choice_mode()
    $ relationship_rows = status_relationship_rows(mode)
    $ leia_rows = status_leia_rows(mode)
    $ ryan_rows = status_ryan_rows(mode)
    $ route_rows = status_route_rows(mode)

    add Solid("#141117")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1740
        ysize 980
        background Solid("#19151d")
        padding (42, 34)

        vbox:
            spacing 22
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "STATUS" size 46 color "#ffffff"
                    text "A snapshot of your relationship and where things currently stand." size 19 color "#aa9dab"

                vbox:
                    xalign 1.0
                    spacing 8

                    text "Display: [choice_mode_label()]" size 20 color "#e0d4df" xalign 1.0

                    textbutton "Close":
                        xalign 1.0
                        action Return()

            frame:
                xfill True
                background Solid("#2a222c")
                padding (26, 20)

                vbox:
                    spacing 9

                    hbox:
                        xfill True
                        text "[girlfriend_name] right now" size 27 color "#ffffff"
                        text "Current outfit: [current_outfit_name()]" size 18 color "#b9aabb" xalign 1.0

                    text "[leia_overview_text()]" size 20 color "#e8dfe7" line_spacing 4

            text "[status_mode_note()]" size 17 color "#8f8291"

            hbox:
                spacing 20
                xfill True
                yfill True

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
