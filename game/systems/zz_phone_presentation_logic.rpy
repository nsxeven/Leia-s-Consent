# Phone presentation logic. This file sorts after phone_state.rpy so it can
# safely wrap the core message writer without changing Phone V1 internals.

init python:

    PHONE_NOTIFICATION_BODY_MAX = 72
    PHONE_NOTIFICATION_TITLE_MAX = 32

    PHONE_APP_ICON_PATHS = {
        "Phone": "gui/phone/icons/phone.png",
        "Messages": "gui/phone/icons/messages.png",
        "Photos": "gui/phone/icons/photos.png",
        "Shop": "gui/phone/icons/shop.png",
        "Online Shop": "gui/phone/icons/shop.png",
        "Delivery": "gui/phone/icons/delivery.png",
        "Orders": "gui/phone/icons/delivery.png",
        "Wallet": "gui/phone/icons/wallet.png",
    }

    def phone_notification_preview(text, max_chars=PHONE_NOTIFICATION_BODY_MAX):
        """Return a compact single-line notification preview with a clean ellipsis."""
        clean = " ".join((text or "").split())
        if len(clean) <= max_chars:
            return clean

        cutoff = max(4, max_chars - 3)
        shortened = clean[:cutoff].rstrip()

        # Prefer ending at a word boundary when that does not throw away too much text.
        if " " in shortened:
            word_boundary = shortened.rsplit(" ", 1)[0].rstrip()
            if len(word_boundary) >= int(cutoff * 0.72):
                shortened = word_boundary

        return shortened.rstrip(" ,.;:-") + "..."

    def phone_app_icon_path(app):
        """Return the custom UI icon for a phone app, with Phone as fallback."""
        clean = (app or "Phone").strip()
        return PHONE_APP_ICON_PATHS.get(clean, PHONE_APP_ICON_PATHS["Phone"])

    def phone_unread_badge_label(count=None):
        """Return a compact unread badge value suitable for the Phone HUD."""
        value = phone_total_unread() if count is None else int(count)
        if value > 99:
            return "99+"
        return str(max(0, value))

    def set_phone_unlocked(value=True):
        renpy.store.phone_unlocked = bool(value)
        renpy.restart_interaction()
        return None

    def set_phone_hud_enabled(value=True):
        renpy.store.phone_hud_enabled = bool(value)
        renpy.restart_interaction()
        return None

    def enter_cinematic_mode():
        renpy.store.phone_hud_enabled = False
        renpy.restart_interaction()
        return None

    def exit_cinematic_mode():
        renpy.store.phone_hud_enabled = True
        renpy.restart_interaction()
        return None

    def phone_queue_notification(app, title, body, kind="message"):
        item = {
            "app": app,
            "title": phone_notification_preview(title, PHONE_NOTIFICATION_TITLE_MAX),
            "body": phone_notification_preview(body, PHONE_NOTIFICATION_BODY_MAX),
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

    def debug_reset_phone_tutorial():
        persistent.phone_tutorial_seen = False
        renpy.notify("Phone tutorial reset. It will appear at the next Phone unlock.")
        return None

    def phone_unlock_with_tutorial():
        set_phone_unlocked(True)

        # Release behaviour: tutorial is shown once globally.
        # Developer behaviour: always show it so repeated New Game tests can verify the flow.
        if (not persistent.phone_tutorial_seen) or bool(config.developer):
            renpy.show_screen("phone_first_use_tutorial")
        else:
            renpy.notify("Phone unlocked.")
        return None
