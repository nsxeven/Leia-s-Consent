# Phone presentation screens: native Ren'Py UI, no image-generation assets required.

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

    if phone_unlocked and phone_hud_enabled and quick_menu and not renpy.get_screen("main_menu") and not renpy.get_screen("phone_screen"):
        button:
            xalign 0.985
            yalign 0.91
            xsize 86
            ysize 116
            padding (8, 8)
            background Solid("#171319")
            hover_background Solid("#3a2a37")
            action Show("phone_screen")

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 4

                frame:
                    xalign 0.5
                    xsize 38
                    ysize 58
                    background Solid("#29222c")
                    padding (4, 4)
                    text "P" size 24 color "#f1a8c8" xalign 0.5 yalign 0.5

                text "PHONE" size 11 color "#ffffff" xalign 0.5

                if phone_total_unread() > 0:
                    frame:
                        xalign 0.5
                        background Solid("#d94a67")
                        padding (7, 3)
                        text "[phone_total_unread()]" size 11 color "#ffffff" xalign 0.5


screen phone_notification_banner():

    zorder 620

    if phone_notification_current:
        frame:
            at phone_notification_slide
            xalign 0.5
            yalign 0.0
            xsize 720
            padding (26, 20)
            background Frame("gui/phone/notification_card.svg", 28, 28)

            vbox:
                spacing 5
                xfill True

                hbox:
                    xfill True
                    text "[phone_notification_current['app']]" size 17 color "#6e6e73" bold True
                    text "now" size 15 color "#8e8e93" xalign 1.0

                text "[phone_notification_current['title']]" size 23 color "#111111" bold True
                text "[phone_notification_current['body']]" size 19 color "#2c2c2e" line_spacing 2

        timer 3.75 action Function(phone_finish_notification)


screen phone_first_use_tutorial():

    modal True
    zorder 650

    add Solid("#00000099")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        padding (34, 30)
        background Solid("#17171df7")

        vbox:
            spacing 16
            xfill True

            text "PHONE UNLOCKED" size 32 color "#ffffff" bold True xalign 0.5
            text "Messages, photos, purchases, deliveries, and other updates can appear on Ryan's phone as the story progresses." size 20 color "#dedee4" text_align 0.5 xalign 0.5 line_spacing 5
            text "New activity can appear as a notification at the top of the screen. The badge on the Phone shows how many unread messages are waiting." size 18 color "#bdbdc6" text_align 0.5 xalign 0.5 line_spacing 4

            null height 4

            textbutton "Got it":
                xalign 0.5
                xsize 220
                text_xalign 0.5
                action [SetField(persistent, "phone_tutorial_seen", True), Hide("phone_first_use_tutorial")]
