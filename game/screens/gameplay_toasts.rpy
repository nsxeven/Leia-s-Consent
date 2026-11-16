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


# Generic gameplay popup treatment. Keep this as the default for future
# choice/stat/system toasts so new popups inherit the same soft fade language.
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

