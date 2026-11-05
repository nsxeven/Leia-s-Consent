# Phone presentation screens using the custom phone icon set.

default phone_unlocked = False
default phone_hud_enabled = True
default phone_notification_current = None
default lc_phone_deep_link = None
default phone_notification_queue = []
default persistent.phone_tutorial_seen = False


# Shared popup motion: movement is always accompanied by a soft opacity ramp.
transform phone_notification_slide:
    alpha 0.0
    yoffset -170
    parallel:
        easeout 0.30 yoffset 15
    parallel:
        linear 0.45 alpha 1.0
    pause 3.2
    parallel:
        easein 0.25 yoffset -170
    parallel:
        linear 0.40 alpha 0.0

transform lc_popup_soft_fade:
    alpha 0.0
    linear 0.45 alpha 1.0

transform lc_popup_soft_fade_hide:
    on show:
        alpha 0.0
        linear 0.45 alpha 1.0
    on hide:
        linear 0.40 alpha 0.0


# Override the original quick-access overlay. The Phone is absent before its
# story introduction and can be hidden during full-screen cinematic CGs.
screen phone_quick_access():

    zorder 110
    default hud_hovered = False
    # Hidden on every full-screen CG (same detection as the see-through text box),
    # so CGs never show the button whether or not a scene called enter_cinematic_mode().
    $ _hud_on = phone_unlocked and phone_hud_enabled and quick_menu and not lc_cg_on_screen() and not renpy.get_screen("main_menu") and not renpy.get_screen("phone_screen") and not renpy.get_screen("lc_phone_status") and not renpy.get_screen("lc_phone_settings") and not renpy.get_screen("lc_phone_photo_viewer")

    # Pixel iPhone, centred on the old 108x108 slot (centre 1839, 939).
    # The art is 114x150 with padding; the drawn phone is 84x126. The hit
    # target is 90x132 around that phone, clear of the dialogue box and the
    # quick menu.
    if _hud_on:
        $ _btn_theme = "night" if store.lc_dialogue_theme == "night" else "day"
        # The highlight comes from the button's own focus state (idle/hover art),
        # so it can never stick when the phone opens and hides the button before
        # an "unhovered" arrives. The hit area is the drawn phone itself.
        imagebutton:
            idle Transform("gui/phone/sweetheart/phone_btn_%s_idle.png" % _btn_theme, nearest=True)
            hover Transform("gui/phone/sweetheart/phone_btn_%s_hover.png" % _btn_theme, nearest=True)
            xpos 1785
            ypos 858
            focus_mask True
            action [SetScreenVariable("hud_hovered", False), Show("phone_screen")]
            hovered [SetScreenVariable("hud_hovered", True), Function(lc_ui_play, "tick")]
            unhovered SetScreenVariable("hud_hovered", False)

        if phone_total_unread() > 0:
            $ _badge = phone_unread_badge_label()
            $ _badge_w = 39 if len(_badge) <= 1 else (18 + 15 * len(_badge))
            fixed:
                xpos (1893 - _badge_w)
                ypos (861 if hud_hovered else 864)
                xysize (_badge_w, 39)
                add Transform("gui/phone/sweetheart/badge_%s.png" % _btn_theme, nearest=True, xysize=(_badge_w, 39))
                text "[_badge]":
                    style "lc_sw_pixel_bold"
                    color "#faf4e8"
                    xalign 0.5
                    yalign 0.55


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

    add Solid("#00000066") at lc_popup_soft_fade

    frame at lc_popup_soft_fade_hide:
        xalign 0.5
        yalign 0.5
        xsize 700
        padding (36, 32)
        background Frame("gui/phone/rounded_white.png", 28, 28)

        vbox:
            spacing 16
            xfill True

            add Transform("gui/phone/sweetheart/phone_btn_day_idle.png", nearest=True) xysize (114, 150) xalign 0.5
            text "PHONE UNLOCKED" size 31 color "#1c1c1e" bold True xalign 0.5
            text "Messages, photos, purchases, deliveries, and other updates can appear on [player_name]'s phone as the story progresses." size 20 color "#3a3a3c" text_align 0.5 xalign 0.5 line_spacing 5
            text "New activity can appear as a notification at the top of the screen. The badge on the Phone shows how many unread messages are waiting." size 18 color "#8e8e93" text_align 0.5 xalign 0.5 line_spacing 4

            null height 4

            textbutton "Got it":
                xalign 0.5
                xsize 220
                ysize 56
                padding (0, 0)
                background Frame("gui/phone/rounded_button_blue.png", 24, 24)
                hover_background Frame("gui/phone/rounded_button_blue_hover.png", 24, 24)
                text_idle_color "#ffffff"
                text_hover_color "#ffffff"
                text_xalign 0.5
                text_yalign 0.5
                action [SetField(persistent, "phone_tutorial_seen", True), Hide("phone_first_use_tutorial")]
