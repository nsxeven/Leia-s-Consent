# Phone Home presentation patch.
# Replaces the temporary Status/Settings dock with two standalone app tiles.
# Final icon art can replace the placeholder rounded tiles later without changing
# any Status/Settings logic.

init 95 python:

    def lc_phone_hovered_app():
        phone = renpy.get_screen("phone_screen")
        if phone is None:
            return None
        scope = getattr(phone, "scope", None)
        if isinstance(scope, dict):
            return scope.get("hovered_app")
        return None


screen lc_phone_extra_apps():
    zorder 325

    if renpy.get_screen("phone_screen") and not renpy.get_screen("lc_phone_status") and not renpy.get_screen("lc_phone_settings"):
        if lc_phone_current_app() == "home":

            # Standalone app row positioned beneath the existing 3x2 Phone grid.
            # These intentionally mirror the size/hover treatment of the native
            # Messages / Photos / Shop / Wallet / Delivery app tiles.
            hbox:
                xalign 0.5
                yalign 0.775
                spacing 12

                fixed:
                    xsize 180
                    ysize 190

                    if lc_phone_hovered_app() == "status":
                        add "gui/phone/icon_glow.svg" xysize (132, 132) xalign 0.5 ypos -1
                        frame:
                            xysize (118, 118)
                            xalign 0.5
                            ypos 6
                            background Frame("gui/phone/rounded_pink.png", 28, 28)
                            text "S" size 55 color "#ffffff" bold True xalign 0.5 yalign 0.5
                    else:
                        frame:
                            xysize (108, 108)
                            xalign 0.5
                            ypos 11
                            background Frame("gui/phone/rounded_pink.png", 28, 28)
                            text "S" size 50 color "#ffffff" bold True xalign 0.5 yalign 0.5

                    text "Status" size 18 color "#1c1c1e" xalign 0.5 ypos 132
                    if not getattr(persistent, "status_page_intro_seen", False):
                        text "● New" size 12 color "#ff3b30" xalign 0.5 ypos 160
                    else:
                        text "Relationship" size 12 color "#8e8e93" xalign 0.5 ypos 160

                    button:
                        xfill True
                        yfill True
                        background None
                        hover_background None
                        action Show("lc_phone_status")
                        hovered SetScreenVariable("hovered_app", "status", screen="phone_screen")
                        unhovered SetScreenVariable("hovered_app", None, screen="phone_screen")

                fixed:
                    xsize 180
                    ysize 190

                    if lc_phone_hovered_app() == "settings":
                        add "gui/phone/icon_glow.svg" xysize (132, 132) xalign 0.5 ypos -1
                        frame:
                            xysize (118, 118)
                            xalign 0.5
                            ypos 6
                            background Frame("gui/phone/rounded_blue.png", 28, 28)
                            text "SET" size 31 color "#007aff" bold True xalign 0.5 yalign 0.5
                    else:
                        frame:
                            xysize (108, 108)
                            xalign 0.5
                            ypos 11
                            background Frame("gui/phone/rounded_blue.png", 28, 28)
                            text "SET" size 28 color "#007aff" bold True xalign 0.5 yalign 0.5

                    text "Settings" size 18 color "#1c1c1e" xalign 0.5 ypos 132
                    text "[transparency_mode_label()]" size 12 color "#8e8e93" xalign 0.5 ypos 160

                    button:
                        xfill True
                        yfill True
                        background None
                        hover_background None
                        action Show("lc_phone_settings")
                        hovered SetScreenVariable("hovered_app", "settings", screen="phone_screen")
                        unhovered SetScreenVariable("hovered_app", None, screen="phone_screen")
