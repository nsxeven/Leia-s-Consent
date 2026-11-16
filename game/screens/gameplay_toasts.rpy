# Gameplay toasts - phone notification and choice feedback state
#
# Purpose: State and helpers for the two lightweight notifications: phone banners (upper left) and
#   choice/stat feedback (upper right), both styled like the phone UI. The overlay screens
#   themselves live in screens/scrapbook_ui.rpy; this file registers them.
#
# Public API (call these from scenes/screens):
#   phone_show_notification(title, body) -> None
#       queue one diegetic phone banner
#   clear_phone_notification(serial) -> None  screen action: hide a banner by serial
#   transform gameplay_toast_appear           toast entrance transform
#   default choice_feedback_payload           save state: current choice toast
#   default phone_notification_payload        save state: current phone banner
#
# Example:
#   phone_show_notification("Trip Group", "Okay this one's actually good.")
#
# Depends on: screens/scrapbook_ui.rpy (choice_feedback_overlay, phone_notification_overlay)
# Hooks: none (registers both overlays in config.overlay_screens)
# Load order: default (init 0)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_choice_toast_fade.py,
#   tests/test_behaviour_freeze.py

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

