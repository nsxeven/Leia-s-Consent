# Lightweight gameplay notifications.
# Phone notifications use the upper-left corner; choice/stat feedback uses upper-right.
# Both intentionally mirror the clean rounded surfaces of the in-game Phone UI.

default choice_feedback_payload = None
default choice_feedback_serial = 0

default phone_notification_payload = None
default phone_notification_serial = 0

init python:

    if "choice_feedback_overlay" not in config.overlay_screens:
        config.overlay_screens.append("choice_feedback_overlay")

    if "phone_notification_overlay" not in config.overlay_screens:
        config.overlay_screens.append("phone_notification_overlay")


    def clear_choice_feedback(serial):
        payload = renpy.store.choice_feedback_payload
        if payload and payload.get("serial") == serial:
            renpy.store.choice_feedback_payload = None
        return None


    def show_choice_feedback(choice_id):
        """Show post-choice feedback without leaking more than the selected mode allows."""
        effects = get_choice_effects(choice_id)
        if not effects:
            return None

        mode = current_choice_mode()

        if mode == "normal":
            title = "CHOICE"
            body = "Your response has been remembered."
        elif mode == "insight":
            title = "CHOICE IMPACT"
            body = _choice_effect_text(choice_id, exact=False)
        elif mode == "full":
            title = "STAT CHANGES"
            body = _choice_effect_text(choice_id, exact=True)
        else:
            title = "DEBUG CHOICE"
            tags = get_choice_tags(choice_id)
            tag_text = ", ".join(tags) if tags else "none"
            body = "{}\nID: {}\nTags: {}".format(
                _choice_effect_text(choice_id, exact=True),
                choice_id,
                tag_text,
            )

        renpy.store.choice_feedback_serial += 1
        renpy.store.choice_feedback_payload = {
            "serial": renpy.store.choice_feedback_serial,
            "title": title,
            "body": body,
        }
        return None


    def clear_phone_notification(serial):
        payload = renpy.store.phone_notification_payload
        if payload and payload.get("serial") == serial:
            renpy.store.phone_notification_payload = None
        return None


    def phone_show_notification(title, body):
        """Queue one lightweight diegetic Phone notification."""
        renpy.store.phone_notification_serial += 1
        renpy.store.phone_notification_payload = {
            "serial": renpy.store.phone_notification_serial,
            "title": title or "Phone",
            "body": body or "New message",
        }
        return None


transform gameplay_toast_appear:
    on show:
        alpha 0.0
        yoffset -18
        parallel:
            linear 0.20 alpha 1.0
        parallel:
            easeout 0.20 yoffset 0
    on hide:
        linear 0.25 alpha 0.0


screen choice_feedback_overlay():
    zorder 295

    if choice_feedback_payload:
        $ _choice_toast = choice_feedback_payload
        $ _choice_toast_serial = _choice_toast.get("serial", 0)

        frame at gameplay_toast_appear:
            xalign 0.985
            yalign 0.045
            xmaximum 520
            background Frame("gui/phone/rounded_white.png", 24, 24)
            padding (20, 16)

            vbox:
                spacing 5
                text "[_choice_toast['title']]" size 13 color "#8e8e93" bold True
                text "[_choice_toast['body']]" size 17 color "#1c1c1e" line_spacing 3

        timer 3.20 action Function(clear_choice_feedback, _choice_toast_serial)


screen phone_notification_overlay():
    zorder 294

    if phone_notification_payload:
        $ _phone_toast = phone_notification_payload
        $ _phone_toast_serial = _phone_toast.get("serial", 0)

        frame at gameplay_toast_appear:
            xalign 0.015
            yalign 0.045
            xmaximum 520
            background Frame("gui/phone/rounded_white.png", 24, 24)
            padding (18, 15)

            hbox:
                spacing 12
                add "gui/phone/icons/messages.png" xysize (48, 48) yalign 0.5

                vbox:
                    spacing 3
                    yalign 0.5
                    text "[_phone_toast['title']]" size 14 color "#1c1c1e" bold True
                    text "[_phone_toast['body']]" size 15 color "#6d6d72" line_spacing 2

        timer 3.60 action Function(clear_phone_notification, _phone_toast_serial)
