# Phone Photos app - the full-screen photo viewer
#
# Purpose: The Photos app's full-screen viewer (opened from the Photos grid and from photo
#   attachments in a chat). The grid itself is part of phone_screen (screens/phone_sweetheart.rpy).
#
# Public API (call these from scenes/screens):
#   screen lc_phone_photo_viewer(photo_asset)
#       full-screen photo
#
# Example:
#   action Show("lc_phone_photo_viewer", photo_asset=asset_id)
#
# Depends on: screens/phone_sweetheart.rpy (handset styles and helpers, phone_screen),
#   systems/phone_state.rpy (photo assets)
# Hooks: none
# Load order: default (screens at init -500)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_phone_layout.py

screen lc_phone_photo_viewer(photo_asset):
    modal True
    zorder 380

    key "K_ESCAPE" action Function(lc_phone_back)
    key "game_menu" action Function(lc_phone_back)
    key "mouseup_3" action Function(lc_phone_back)

    add Solid("#12080e")

    if photo_asset and renpy.has_image(photo_asset):
        add photo_asset:
            xalign 0.5
            yalign 0.5
            fit "contain"
            xysize (1760, 960)

    button:
        style "lc_sw_hit"
        xfill True
        yfill True
        action Function(lc_phone_close)

    button:
        style "lc_sw_hit"
        xpos 1680
        ypos 36
        xminimum 150
        ysize 54
        background Frame("gui/phone/sprite_match/key.png", 18, 18)
        hover_background Frame("gui/phone/sprite_match/key.png", 18, 18)
        action Function(lc_phone_back)
        text "Done":
            style "lc_sw_hand"
            size 28
            color "#FFFFFF"
            xalign 0.5
            yalign 0.5

    if photo_asset and renpy.has_image(photo_asset):
        textbutton "Set as wallpaper":
            style "lc_phone_btn"
            xfill False
            xsize 250
            xpos 1414
            ypos 37
            action [Function(lc_ui_play, "app_tap"), Show("lc_phone_wallpaper_editor", photo_asset=photo_asset)]
