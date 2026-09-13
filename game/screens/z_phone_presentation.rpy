# Phone presentation layer: story unlock, cinematic HUD visibility, notifications,
# and first-use tutorial. Native Ren'Py UI only; no image assets required.

default phone_unlocked = False
default phone_hud_enabled = True
default phone_notification_current = None
default phone_notification_queue = []
default persistent.phone_tutorial_seen = False

init python:

    def set_phone_unlocked(value=True):
        renpy.store.phone_unlocked = bool(value)
        renpy.restart_interaction()

    def set_phone_hud_enabled(value=True):
        renpy.store.phone_hud_enabled = bool(value)
        renpy.restart_interaction()

    def enter_cinematic_mode():
        renpy.store.phone_hud_enabled = False
        renpy.restart_interaction()

    def exit_cinematic_mode():
        renpy.store.phone_hud_enabled = True
        renpy.restart_interaction()

    def phone_queue_notification(app, title, body, kind="message"):
        item = {
            "app": app,
            "title": title,
            "body": body,
            "kind": kind,
        }
        renpy.store.phone_notification_queue.append(item)
        if renpy.store.phone_notification_current is None:
            phone_show_next_notification()
        return None

    def phone_show_next_notification():
        if renpy.store.phone_notification_current is not None:
            return None
        if not renpy.store.phone_notification_queue:
            return None
        renpy.store.phone_notification_current = renpy.store.phone_notification_queue.pop(0)
        renpy.show_screen("phone_notification_banner")
        renpy.restart_interaction()
        return None

    def phone_finish_notification():
        renpy.store.phone_notification_current = None
        renpy.hide_screen("phone_notification_banner")
        renpy.restart_interaction()
        if renpy.store.phone_notification_queue:
            phone_show_next_notification()
        return None

    # Preserve the Phone V1 message writer and wrap it so story messages can
    # optionally create native notification banners without duplicating unread state.
    _phone_add_message_base = phone_add_message

    def phone_add_message(
        thread_id,
        sender_id,
        text="",
        message_id=None,
        attachment_id=None,
        attachment_label=None,
        mark_unread=True,
        notify=False,
        notification_app="Messages",
        notification_title=None,
    ):
        added = _phone_add_message_base(
            thread_id,
            sender_id,
            text=text,
            message_id=message_id,
            attachment_id=attachment_id,
            attachment_label=attachment_label,
            mark_unread=mark_unread,
        )

        if added and notify and sender_id != "player":
            title = notification_title or phone_thread_label(thread_id)
            if attachment_id:
                preview = text.strip() if text.strip() else "Sent a photo"
                kind = "photo"
            else:
                preview = text.strip() if text.strip() else "New message"
                kind = "message"
            phone_queue_notification(notification_app, title, preview, kind=kind)

        return added

    def phone_unlock_with_tutorial():
        set_phone_unlocked(True)
        if not persistent.phone_tutorial_seen:
            renpy.show_screen("phone_first_use_tutorial")
        else:
            renpy.notify("Phone unlocked.")
        return None


transform phone_notification_slide:
    alpha 0.0
    yoffset -170
    easeout 0.30 alpha 1.0 yoffset 28
    pause 3.2
    easein 0.25 alpha 0.0 yoffset -170


# Override the original quick-access overlay. The Phone does not exist as a
# player-facing HUD element until story-unlocked, and cinematic scenes can hide it.
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
            xsize 680
            padding (24, 18)
            background Solid("#17171df2")

            vbox:
                spacing 5
                xfill True

                hbox:
                    xfill True
                    text "[phone_notification_current['app']]" size 17 color "#d7d7dd" bold True
                    text "now" size 15 color "#9999a2" xalign 1.0

                text "[phone_notification_current['title']]" size 23 color "#ffffff" bold True
                text "[phone_notification_current['body']]" size 19 color "#eeeeF2" line_spacing 2

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
                action [SetField(persistent, "phone_tutorial_seen", True), Hide("phone_first_use_tutorial")]
