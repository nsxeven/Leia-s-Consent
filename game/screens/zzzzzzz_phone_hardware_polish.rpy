# Final presentation layer for the current Phone prototype.
# Loaded after the iOS-inspired Phone screen so it can polish shared components
# without duplicating the story/message/shop logic.

init 300 python:
    if "lc_phone_hardware_overlay" not in config.overlay_screens:
        config.overlay_screens.append("lc_phone_hardware_overlay")


screen lc_phone_hardware_overlay():
    # Purely visual. The SVG center is transparent, so this adds a silver body
    # and black glass bezel without blocking the Phone's buttons/content.
    zorder 399

    if renpy.get_screen("phone_screen") or renpy.get_screen("lc_phone_status") or renpy.get_screen("lc_phone_settings"):
        add "gui/phone/phone_hardware_overlay.svg":
            xysize (690, 1070)
            xalign 0.5
            yalign 0.5


# Replace the temporary ST/SET tiles while preserving the same reusable app
# component for the existing Messages/Photos/Shop/Wallet/Delivery artwork.
screen lc_ios_app_tile(app_id, label, subtitle, action, icon_path=None, placeholder_text=None, badge_text=None):
    $ effective_icon = icon_path
    if effective_icon is None and app_id == "status":
        $ effective_icon = "gui/phone/icons/status.svg"
    elif effective_icon is None and app_id == "settings":
        $ effective_icon = "gui/phone/icons/settings.svg"

    fixed:
        xsize 172
        ysize 166

        button:
            xfill True
            yfill True
            padding (6, 6)
            background None
            hover_background Frame("gui/phone/rounded_white.png", 24, 24)
            action action

            vbox:
                xalign 0.5
                spacing 5

                fixed:
                    xsize 96
                    ysize 96
                    xalign 0.5

                    if effective_icon:
                        add effective_icon xysize (92, 92) xalign 0.5 yalign 0.5
                    else:
                        frame:
                            xysize (92, 92)
                            xalign 0.5
                            yalign 0.5
                            background Frame("gui/phone/rounded_light.png", 28, 28)
                            text (placeholder_text or "APP") size 25 color "#007aff" bold True xalign 0.5 yalign 0.5

                    if badge_text:
                        frame:
                            xpos 69
                            ypos -4
                            xminimum 27
                            ysize 27
                            padding (7, 2)
                            background Frame("gui/phone/unread_badge.svg", 12, 12)
                            text badge_text size 11 color "#ffffff" bold True xalign 0.5 yalign 0.5

                text label size 16 color "#1c1c1e" bold True xalign 0.5
                text subtitle size 11 color "#6d6d72" xalign 0.5 text_align 0.5 xmaximum 155


# More realistic status bar / camera island. The black island visually matches
# the black inner bezel added around the screen.
screen lc_ios_status_bar():
    fixed:
        xfill True
        ysize 48

        text "[lc_phone_clock_text()]" size 14 color "#1c1c1e" bold True xpos 16 yalign 0.5

        add "gui/phone/dynamic_island.svg":
            xysize (132, 31)
            xalign 0.5
            yalign 0.5

        hbox:
            xalign 0.965
            yalign 0.5
            spacing 7
            text "•••" size 15 color "#1c1c1e" bold True
            text "Wi-Fi" size 12 color "#1c1c1e"
            frame:
                xsize 30
                ysize 15
                yalign 0.5
                padding (2, 2)
                background Frame("gui/phone/rounded_light.png", 8, 8)
                frame:
                    xfill True
                    yfill True
                    background Solid("#1c1c1e")
