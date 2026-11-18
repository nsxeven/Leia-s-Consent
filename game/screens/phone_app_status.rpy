# Phone Status app - Leia's stats, outfit and notes on the handset
#
# Purpose: The Status app (opened from the phone home grid): stat rows with tooltips, sections and
#   the "Things I noticed" pins.
#
# Public API (call these from scenes/screens):
#   screen lc_phone_status()                  Status app
#
# Example:
#   action ShowMenu("lc_phone_status")      (phone home grid, screens/phone_sweetheart.rpy)
#
# Depends on: screens/phone_sweetheart.rpy (handset styles and helpers), systems/status_display.rpy,
#   screens/stat_tooltip_screen.rpy, systems/notice.rpy + screens/notice_screen.rpy
# Hooks: none
# Load order: default (screens at init -500)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_phone_layout.py, tests/test_sprite_match_ui.py

screen lc_phone_status_row(row):
    button:
        style "lc_sw_hit"
        xfill True
        # Padding clears the hover art's rounded 18px border so the bar sits
        # fully inside the highlight (darryn 2026-11-08).
        padding (14, 8, 14, 12)
        hover_background Frame("gui/phone/sprite_match/row_hover.png", 18, 18)
        tooltip row.get("tooltip")
        action NullAction()
        vbox:
            spacing 4
            xfill True
            $ _cs = lc_status_colour_stat(row)
            $ _icon = LC_STAT_ICON.get(row["stat"]) or LC_STAT_ICON.get(_cs)
            hbox:
                xfill True
                spacing 8
                if _icon:
                    add Transform("images/ui/scrapbook/icon_{}.png".format(_icon), xysize=(28, 28)) yalign 0.5
                text row["label"]:
                    style "lc_sw_hand"
                    size 24
                    color "#293C53"
                    yalign 0.5
                if row["detail"]:
                    text row["detail"]:
                        style "lc_sw_hand"
                        size 20
                        color LC_STAT_COLOUR[_cs]["phone"]
                        xalign 1.0
                        yalign 0.5
            # Stat colours, softened for the white phone cards (darryn 2026-11-09).
            bar:
                value StaticValue(row["value"], 100)
                xfill True
                ysize 10
                left_bar Frame(Solid(LC_STAT_COLOUR[_cs]["phone"]), 0, 0)
                right_bar Solid("#E2E7EF")
            if row["internal_key"]:
                text row["internal_key"]:
                    style "lc_sw_hand"
                    size 18
                    color "#6E8399"


screen lc_phone_status_section(title, rows):
    frame:
        style "lc_sw_frame"
        xfill True
        background Frame("gui/phone/sprite_match/card.png", 18, 18)
        padding (14, 12)
        vbox:
            spacing 10
            xfill True
            text title:
                style "lc_sw_hand"
                size 20
                color "#6E8399"
            for row in rows:
                use lc_phone_status_row(row)


screen lc_phone_status():
    modal True
    zorder 340
    key "K_ESCAPE" action Function(lc_phone_back)
    key "game_menu" action Function(lc_phone_back)

    $ _mode = current_choice_mode()
    $ _relationship_rows = status_relationship_rows(_mode)
    $ _leia_rows = status_leia_rows(_mode)
    $ _ryan_rows = status_ryan_rows(_mode)
    $ _route_rows = status_route_rows(_mode)
    $ _notice_pins = lc_notice_pins()

    use lc_phone_backdrop(Function(lc_phone_close))
    fixed:
        xalign 0.5
        yalign 0.5
        xysize (540, 1040)
        use lc_phone_body_blocker
        add "gui/phone/sprite_match/phone_app.png"
        text "[lc_phone_clock_text()]":
            style "lc_sw_pixel_bold"
            size 22
            color "#303B51"
            xpos 40
            ypos 16
        button:
            style "lc_sw_hit"
            xpos 28
            ypos 88
            xysize (56, 56)
            action Function(lc_phone_back)
            add "gui/phone/sprite_match/chevron.png" xalign 0.5 yalign 0.5
        text "Status":
            style "lc_sw_hand"
            size 36
            color "#293C53"
            xpos 76
            ypos 96
        text transparency_mode_label():
            style "lc_sw_hand"
            size 20
            color "#6E8399"
            xpos 76
            ypos 138
            xmaximum 420
        viewport:
            ypos 176
            xpos LC_PHONE_CONTENT_LEFT
            xsize LC_PHONE_VIEWPORT_WIDTH
            ysize 800
            mousewheel True
            draggable True
            scrollbars None
            vbox:
                spacing 12
                xsize LC_PHONE_CONTENT_WIDTH
                if not getattr(persistent, "status_page_intro_seen", False):
                    frame:
                        style "lc_sw_frame"
                        xfill True
                        background Frame("gui/phone/sprite_match/card.png", 18, 18)
                        padding (14, 12)
                        vbox:
                            spacing 8
                            text "Your live dashboard":
                                style "lc_sw_hand"
                                size 26
                                color "#3D8FD4"
                            text "Status tracks the relationship, [girlfriend_name], and [player_name]. Settings chooses how much of it you can see.":
                                style "lc_sw_hand"
                                size 24
                                color "#293C53"
                                xmaximum 440
                            textbutton "Got it":
                                style "lc_phone_btn_primary"
                                xfill False
                                xminimum 160
                                action Function(lc_mark_status_intro_seen)
                frame:
                    style "lc_sw_frame"
                    xfill True
                    background Frame("gui/phone/sprite_match/card.png", 18, 18)
                    padding (14, 12)
                    vbox:
                        spacing 6
                        text "[girlfriend_name] right now":
                            style "lc_sw_hand"
                            size 26
                            color "#293C53"
                        text "[leia_overview_text()]":
                            style "lc_sw_hand"
                            size 24
                            color "#6E8399"
                            xmaximum 440
                use lc_phone_status_section("Relationship", _relationship_rows)
                use lc_phone_status_section(girlfriend_name, _leia_rows)
                use lc_phone_status_section(player_name, _ryan_rows)
                if _route_rows:
                    use lc_phone_status_section("Route tendencies", _route_rows)
                if _notice_pins:
                    use lc_phone_notice_pins(_notice_pins)
                textbutton "Open settings":
                    style "lc_phone_btn"
                    action [Hide("lc_phone_status"), Show("lc_phone_settings")]
                text "[status_mode_note()]":
                    style "lc_sw_hand"
                    size 22
                    color "#6E8399"
                    text_align 0.5
                    xalign 0.5
                    xmaximum 440
                text "Hover over a stat to see what it means.":
                    style "lc_sw_hand"
                    size 22
                    color "#6E8399"
                    text_align 0.5
                    xalign 0.5
                    xmaximum 440
                null height 16
    use lc_stat_tip(GetTooltip("lc_phone_status"), look="phone")
