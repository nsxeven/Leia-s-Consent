# Phone presentation screens using the custom phone icon set.

default phone_unlocked = False
default phone_hud_enabled = True
default phone_notification_current = None
default phone_notification_queue = []
default persistent.phone_tutorial_seen = False


transform phone_notification_slide:
    alpha 0.0
    yoffset -170
    easeout 0.30 alpha 1.0 yoffset 28
    pause 3.2
    easein 0.25 alpha 0.0 yoffset -170


# Override the original quick-access overlay. The Phone is absent before its
# story introduction and can be hidden during full-screen cinematic CGs.
screen phone_quick_access():

    zorder 110
    default hud_hovered = False

    if phone_unlocked and phone_hud_enabled and quick_menu and not renpy.get_screen("main_menu") and not renpy.get_screen("phone_screen"):
        fixed:
            xalign 0.985
            yalign 0.91
            xsize 108
            ysize 108

            if hud_hovered:
                add "gui/phone/icon_glow.svg":
                    xysize (106, 106)
                    xalign 0.5
                    yalign 0.5

                add "gui/phone/icons/phone.png":
                    xysize (84, 84)
                    xalign 0.5
                    yalign 0.5
            else:
                add "gui/phone/icons/phone.png":
                    xysize (74, 74)
                    xalign 0.5
                    yalign 0.5
                    alpha 0.94

            button:
                xfill True
                yfill True
                background None
                hover_background None
                action Show("phone_screen")
                hovered SetScreenVariable("hud_hovered", True)
                unhovered SetScreenVariable("hud_hovered", False)

            if phone_total_unread() > 0:
                fixed:
                    xpos 61
                    ypos 1
                    xsize 42
                    ysize 32

                    add "gui/phone/unread_badge.svg"

                    text "[phone_unread_badge_label()]":
                        size 12
                        color "#ffffff"
                        bold True
                        xalign 0.5
                        yalign 0.5


screen phone_notification_banner():

    zorder 620

    if phone_notification_current:
        fixed:
            at phone_notification_slide
            xalign 0.5
            yalign 0.0
            xsize 700
            ysize 116

            add "gui/phone/notification_card.svg"

            vbox:
                xpos 24
                ypos 13
                xsize 652
                spacing 2

                fixed:
                    xfill True
                    ysize 25

                    hbox:
                        xalign 0.0
                        yalign 0.5
                        spacing 7

                        add phone_app_icon_path(phone_notification_current["app"]):
                            xysize (22, 22)
                            yalign 0.5

                        text "[phone_notification_current['app']]":
                            size 17
                            color "#6e6e73"
                            bold True
                            yalign 0.5

                    text "now":
                        size 15
                        color "#8e8e93"
                        xalign 1.0
                        yalign 0.5

                text "[phone_notification_current['title']]" size 22 color "#111111" bold True
                text "[phone_notification_current['body']]" size 18 color "#2c2c2e"

        timer 3.75 action Function(phone_finish_notification)


screen phone_first_use_tutorial():

    modal True
    zorder 650

    add Solid("#00000066")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        padding (36, 32)
        background Solid("#fafafd")

        vbox:
            spacing 16
            xfill True

            add "gui/phone/icons/phone.png" xysize (92, 92) xalign 0.5
            text "PHONE UNLOCKED" size 31 color "#1c1c1e" bold True xalign 0.5
            text "Messages, photos, purchases, deliveries, and other updates can appear on Ryan's phone as the story progresses." size 20 color "#3a3a3c" text_align 0.5 xalign 0.5 line_spacing 5
            text "New activity can appear as a notification at the top of the screen. The badge on the Phone shows how many unread messages are waiting." size 18 color "#8e8e93" text_align 0.5 xalign 0.5 line_spacing 4

            null height 4

            textbutton "Got it":
                xalign 0.5
                xsize 220
                ysize 56
                padding (0, 0)
                background Solid("#0a84ff")
                hover_background Solid("#409cff")
                text_idle_color "#ffffff"
                text_hover_color "#ffffff"
                text_xalign 0.5
                text_yalign 0.5
                action [SetField(persistent, "phone_tutorial_seen", True), Hide("phone_first_use_tutorial")]
