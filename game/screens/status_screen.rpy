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

                $ _cs = lc_status_colour_stat(row)
                $ _icon = LC_STAT_ICON.get(row["stat"]) or LC_STAT_ICON.get(_cs)
                if _icon:
                    add Transform("images/ui/scrapbook/icon_{}.png".format(_icon), xysize=(30, 30)) yalign 0.5
                text row["label"] size 23 color "#fff0dc" yalign 0.5

                if row["detail"]:
                    text row["detail"] size 20 color LC_STAT_COLOUR[_cs]["ink"] xalign 1.0 yalign 0.5

            # Immersive mode never exposes a numeric meter.
            if current_choice_mode() != "normal":
                bar:
                    value StaticValue(row["value"], 100)
                    xfill True
                    ysize 24
                    left_bar Frame("gui/glass/stat_{}.png".format(lc_status_colour_stat(row)), 10, 10)
                    right_bar Frame("gui/glass/stat_track.png", 10, 10)

            if row["internal_key"]:
                text row["internal_key"] size 15 color "#dbc8bd"


# Section header colours (Prefs glass look, darryn 2026-11-09).
define LC_STATUS_SECTION_INK = {"relationship": "#F5C568", "route": "#FF8FC0", "leia": "#FF8FC0", "ryan": "#C8ACEC"}

screen status_section(title, rows, ink="#F5C568"):

    frame:
        xfill True
        background Frame("gui/glass/panel.png", 16, 16)
        padding (24, 20)

        vbox:
            spacing 17
            xfill True

            hbox:
                spacing 12
                frame:
                    xysize (8, 30)
                    yalign 0.5
                    background Frame(Solid(ink), 0, 0)
                text title size 30 color ink font "fonts/Handjet-ExtraBold.ttf" yalign 0.5

            for row in rows:
                use status_stat_row(row)


# The journal art is 1920x1080: the binding occupies x=850..885.
# Keep both content lanes clear of the binding and the outer page edges.
define LC_STATUS_LEFT_X = 395
define LC_STATUS_LEFT_W = 690   # right edge 816, 34 px before binding
define LC_STATUS_RIGHT_X = 1110  # 35 px after binding
define LC_STATUS_RIGHT_W = 710  # right edge 1604

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

    use lc_glass_menu_backdrop()
    frame:
        xpos 354 ypos 42 xsize 1534 ysize 930
        background Frame("gui/glass/panel.png", 24, 24)

    # Left page: title, relationship, and the Full/Developer-only route lean.
    vbox:
        xpos LC_STATUS_LEFT_X
        ypos 80
        xsize LC_STATUS_LEFT_W
        spacing 3
        text "STATUS" size 46 color "#fff0dc"
        text "A snapshot of your relationship and where things currently stand.":
            size 19
            color "#dbc8bd"
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
                hbox:
                    spacing 14
                    box_wrap True
                    box_wrap_spacing 10
                    for (_who, _title, _ink) in ((player_name, lc_status_titles[0], "#ff8fc0"), (girlfriend_name, lc_status_titles[1], "#F5C568")):
                        frame:
                            background Frame("gui/glass/nav_active.png", 12, 12)
                            padding (16, 4, 16, 6)
                            text (_who + " · " + _title) size 26 color _ink font "fonts/Caveat-SemiBold.ttf" substitute False

            use status_section("RELATIONSHIP", relationship_rows, LC_STATUS_SECTION_INK["relationship"])

            if route_rows:
                use status_section("ROUTE LEAN", route_rows, LC_STATUS_SECTION_INK["route"])

            if lc_review_latest():
                textbutton "Review last completed day":
                    action Show("lc_review_history_screen", day_id=lc_review_latest())

            text "[status_mode_note()]" size 17 color "#dbc8bd"
            text "Hover over a stat to see what it means." size 17 color "#dbc8bd"
            null height 12

    # Right page: mode and close remain fixed while the summary/cards scroll.
    hbox:
        xpos LC_STATUS_RIGHT_X
        ypos 92
        xsize LC_STATUS_RIGHT_W
        text "Display: [transparency_mode_label()]" size 20 color "#dbc8bd" yalign 0.5
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
                background Frame("gui/glass/panel.png", 9, 9)
                padding (24, 20)

                vbox:
                    xfill True
                    spacing 9
                    text "[girlfriend_name] right now" size 27 color "#fff0dc"
                    text "Current outfit: [current_outfit_name()]" size 18 color "#F5C568" xfill True
                    text "[leia_overview_text()]" size 20 color "#fff0dc" line_spacing 4 xfill True

            use status_section(girlfriend_name.upper(), leia_rows, LC_STATUS_SECTION_INK["leia"])
            use status_section(player_name.upper(), ryan_rows, LC_STATUS_SECTION_INK["ryan"])
            null height 12

    # Keep this at screen level: nearrect needs full-screen tooltip geometry.
    use lc_stat_tip(GetTooltip("status_screen"))
