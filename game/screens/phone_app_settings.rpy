# Phone Settings app - choice mode and phone options on the handset
#
# Purpose: The Settings app (opened from the phone home grid): the choice-transparency mode cards
#   and the phone's own options.
#
# Public API (call these from scenes/screens):
#   screen lc_phone_settings()                Settings app
#
# Example:
#   action ShowMenu("lc_phone_settings")    (phone home grid, screens/phone_sweetheart.rpy)
#
# Depends on: screens/phone_sweetheart.rpy (handset styles and helpers), systems/choice_engine.rpy
#   (transparency modes)
# Hooks: none
# Load order: default (screens at init -500)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_phone_layout.py, tests/test_sprite_match_ui.py

screen lc_phone_settings_mode(mode_id):
    $ _selected = current_choice_mode() == mode_id
    $ _info = transparency_mode_info(mode_id)
    button:
        style "lc_sw_hit"
        xfill True
        yminimum 96
        padding (16, 12)
        background Frame("gui/phone/sprite_match/key.png" if _selected else "gui/phone/sprite_match/card.png", 18, 18)
        hover_background Frame("gui/phone/sprite_match/key.png" if _selected else "gui/phone/sprite_match/row_hover.png", 18, 18)
        action Function(lc_phone_set_information_mode, mode_id)
        vbox:
            spacing 4
            xfill True
            # Mode name on the left; the selected mode gets a bold "On" in a
            # white pill, flush right (darryn 2026-11-08).
            # Fixed height: yfit with yalign-ed children takes the whole
            # available height, which blew the card up (#160).
            fixed:
                xfill True
                ysize 40
                text _info["label"]:
                    style "lc_sw_hand"
                    size 26
                    color ("#FFFFFF" if _selected else "#293C53")
                    xalign 0.0
                    yalign 0.5
                if _selected:
                    frame:
                        xalign 1.0
                        yalign 0.5
                        background Frame("gui/phone/sprite_match/pill_white.png", 15, 15)
                        padding (14, 1, 14, 3)
                        text "On":
                            style "lc_sw_hand"
                            size 22
                            bold True
                            color "#2E74B0"
                            yalign 0.5
            text _info["tagline"]:
                style "lc_sw_hand"
                size 22
                color ("#EAF4FF" if _selected else "#6E8399")
                xmaximum 420
            text _info["description"]:
                style "lc_sw_hand"
                size 22
                color ("#EAF4FF" if _selected else "#6E8399")
                xmaximum 420


screen lc_phone_settings():
    modal True
    zorder 340
    key "K_ESCAPE" action Function(lc_phone_back)
    key "game_menu" action Function(lc_phone_back)

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
            ypos 92
            xysize (56, 56)
            action Function(lc_phone_back)
            add "gui/phone/sprite_match/chevron.png" xalign 0.5 yalign 0.5
        text "Settings":
            style "lc_sw_hand"
            size 36
            color "#293C53"
            xpos 76
            ypos 98
        viewport:
            ypos 168
            xpos LC_PHONE_CONTENT_LEFT
            xsize LC_PHONE_VIEWPORT_WIDTH
            ysize 810
            mousewheel True
            draggable True
            scrollbars None
            vbox:
                spacing 12
                xsize LC_PHONE_CONTENT_WIDTH
                text "These settings only change what the interface reveals. They never alter stats, story outcomes, or difficulty.":
                    style "lc_sw_hand"
                    size 24
                    color "#6E8399"
                    text_align 0.5
                    xalign 0.5
                    xmaximum 440
                use lc_phone_settings_mode("normal")
                use lc_phone_settings_mode("insight")
                use lc_phone_settings_mode("full")
                if config.developer or not LC_IS_RELEASE:
                    use lc_phone_settings_mode("developer")
                textbutton "Open status":
                    style "lc_phone_btn"
                    action [Hide("lc_phone_settings"), Show("lc_phone_status")]
                text "Wallpaper: open any photo and tap Set as wallpaper.":
                    style "lc_sw_hand"
                    size 22
                    color "#6E8399"
                    text_align 0.5
                    xalign 0.5
                    xmaximum 440
                textbutton "Reset wallpaper":
                    style "lc_phone_btn"
                    action (Function(lc_phone_wallpaper_reset) if lc_phone_wallpaper_active() else None)
                if current_choice_mode() == "developer":
                    text "Developer exposes internal IDs, stat keys, route tendencies, and debug information.":
                        style "lc_sw_hand"
                        size 22
                        color "#6E8399"
                        xmaximum 440
                null height 16
