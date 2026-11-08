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

            # Immersive mode never exposes a numeric meter.
            if current_choice_mode() != "normal":
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


# The journal art is 1920x1080: the binding occupies x=850..885.
# Keep both content lanes clear of the binding and the outer page edges.
define LC_STATUS_LEFT_X = 112
define LC_STATUS_LEFT_W = 704   # right edge 816, 34 px before binding
define LC_STATUS_RIGHT_X = 920  # 35 px after binding
define LC_STATUS_RIGHT_W = 684  # right edge 1604

define LC_STATUS_BODY_Y = 200
define LC_STATUS_BODY_H = 740   # ends at 940, inside the paper

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

    # Left page: title, relationship, and the Full/Developer-only route lean.
    vbox:
        xpos LC_STATUS_LEFT_X
        ypos 80
        xsize LC_STATUS_LEFT_W
        spacing 3
        text "STATUS" size 46 color "#3b2a30"
        text "A snapshot of your relationship and where things currently stand.":
            size 19
            color "#7a6266"
            xsize LC_STATUS_LEFT_W

    viewport:
        xpos LC_STATUS_LEFT_X
        ypos LC_STATUS_BODY_Y
        xsize LC_STATUS_LEFT_W
        ysize LC_STATUS_BODY_H
        mousewheel True
        draggable True
        pagekeys True
        scrollbars "vertical"
        side_yfill True

        vbox:
            xsize (LC_STATUS_LEFT_W - 28)
            spacing 20

            if persistent.lc_title_style != "off":
                $ lc_status_titles = lc_current_titles()
                text (player_name + " · " + lc_status_titles[0]) size 21 color "#cc0066" substitute False
                text (girlfriend_name + " · " + lc_status_titles[1]) size 21 color "#cc0066" substitute False

            use status_section("RELATIONSHIP", relationship_rows)

            if route_rows:
                use status_section("ROUTE TENDENCIES", route_rows)

            if lc_review_latest():
                textbutton "Review last completed day":
                    action Show("lc_review_history_screen", day_id=lc_review_latest())

            text "[status_mode_note()]" size 17 color "#7a6266"
            text "Hover over a stat to see what it means." size 17 color "#7a6266"
            null height 12

    # Right page: mode and close remain fixed while the summary/cards scroll.
    hbox:
        xpos LC_STATUS_RIGHT_X
        ypos 92
        xsize LC_STATUS_RIGHT_W
        text "Display: [transparency_mode_label()]" size 20 color "#7a6266" yalign 0.5
        null width 1 xfill True
        textbutton "Close":
            xalign 1.0
            action _status_close

    viewport:
        xpos LC_STATUS_RIGHT_X
        ypos LC_STATUS_BODY_Y
        xsize LC_STATUS_RIGHT_W
        ysize LC_STATUS_BODY_H
        mousewheel True
        draggable True
        pagekeys True
        scrollbars "vertical"
        side_yfill True

        vbox:
            xsize (LC_STATUS_RIGHT_W - 28)
            spacing 20

            frame:
                xfill True
                background Frame("gui/scrapbook/frame_card.png", 9, 9)
                padding (24, 20)

                vbox:
                    xfill True
                    spacing 9
                    text "[girlfriend_name] right now" size 27 color "#3b2a30"
                    text "Current outfit: [current_outfit_name()]" size 18 color "#7a6266" xfill True
                    text "[leia_overview_text()]" size 20 color "#3b2a30" line_spacing 4 xfill True

            use status_section(girlfriend_name.upper(), leia_rows)
            use status_section(player_name.upper(), ryan_rows)
            null height 12

    # Keep this at screen level: nearrect needs full-screen tooltip geometry.
    use lc_stat_tip(GetTooltip("status_screen"))
