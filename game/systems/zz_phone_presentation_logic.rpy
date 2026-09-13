# Phone presentation logic. This file sorts after phone_state.rpy so it can
# safely wrap the core message writer without changing Phone V1 internals.

init python:

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
