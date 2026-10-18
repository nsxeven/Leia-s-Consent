# In-game phone state and helpers.
# The phone is a reusable diegetic hub for messages, online shopping, photos,
# and future apps. Story code should add messages through the helpers below
# instead of mutating the save-state lists directly.

# Save-specific phone state. Thread IDs remain stable even when display names
# are customized by the player.
default phone_messages = {
    "leia": [],
    "julian": [],
    "group": [],
}
default phone_last_open_thread = None

# Photos are lightweight metadata entries. Story attachments are auto-indexed
# here so the Photos app can become a persistent camera roll rather than a stub.
default phone_photos = []


init python:

    PHONE_THREAD_ORDER = (
        "leia",
        "julian",
        "group",
    )


    def phone_thread_label(thread_id):
        """Return the current player-facing thread name."""
        if thread_id == "leia":
            return renpy.store.girlfriend_name
        if thread_id == "julian":
            return renpy.store.friend_name
        if thread_id == "group":
            return "Trip Group"
        return thread_id.replace("_", " ").title()


    def phone_sender_label(sender_id):
        """Resolve stable sender IDs to the player's customized names."""
        if sender_id == "player":
            return renpy.store.player_name
        if sender_id == "leia":
            return renpy.store.girlfriend_name
        if sender_id == "julian":
            return renpy.store.friend_name
        if sender_id == "system":
            return "System"
        return sender_id.replace("_", " ").title()


    def _phone_ensure_thread(thread_id):
        """Gracefully add a missing thread to older saves."""
        if thread_id not in renpy.store.phone_messages:
            renpy.store.phone_messages[thread_id] = []
        return renpy.store.phone_messages[thread_id]


    def phone_messages_for_thread(thread_id):
        return list(_phone_ensure_thread(thread_id))


    def phone_has_message(message_id):
        """Return True when a stable message ID already exists anywhere."""
        for thread_id in list(renpy.store.phone_messages.keys()):
            for message in _phone_ensure_thread(thread_id):
                if message.get("id") == message_id:
                    return True
        return False


    def phone_has_photo(photo_id):
        return any(photo.get("id") == photo_id for photo in renpy.store.phone_photos)


    def phone_add_photo(photo_id, asset_id, label, source_thread=None, source_message_id=None):
        """Add a persistent Phone Photos entry once."""
        if not photo_id or not asset_id or phone_has_photo(photo_id):
            return False

        renpy.store.phone_photos.append({
            "id": photo_id,
            "asset_id": asset_id,
            "label": label or "Photo",
            "source_thread": source_thread,
            "source_message_id": source_message_id,
        })
        return True


    def phone_photo_items():
        return list(renpy.store.phone_photos)


    def phone_add_message(
        thread_id,
        sender_id,
        text="",
        message_id=None,
        attachment_id=None,
        attachment_label=None,
        mark_unread=True,
        notify=False,
        notification_title=None,
        save_attachment=True,
    ):
        """Add one story message, optionally with an image attachment.

        Supplying a stable message_id makes the operation idempotent. This is
        important when story labels can be revisited after rollback/load.
        `notify=True` uses the lightweight diegetic notification toast. Image
        attachments are also indexed into Phone Photos by default.
        """
        thread = _phone_ensure_thread(thread_id)

        if message_id is None:
            message_id = "{}_{}".format(thread_id, len(thread) + 1)

        if phone_has_message(message_id):
            return False

        incoming = sender_id != "player"
        resolved_attachment_label = attachment_label or "Photo attachment"

        thread.append({
            "id": message_id,
            "sender": sender_id,
            "text": text,
            "attachment_id": attachment_id,
            "attachment_label": resolved_attachment_label,
            "incoming": incoming,
            "read": not (incoming and mark_unread),
        })

        if attachment_id and save_attachment:
            phone_add_photo(
                "message:{}".format(message_id),
                attachment_id,
                resolved_attachment_label,
                source_thread=thread_id,
                source_message_id=message_id,
            )

        if notify and incoming:
            notification_body = text.strip() if text and text.strip() else resolved_attachment_label
            phone_show_notification(
                notification_title or phone_thread_label(thread_id),
                notification_body,
            )

        return True


    def phone_send_player_message(thread_id, text, message_id=None):
        """Convenience wrapper for Ryan/player-authored messages."""
        return phone_add_message(
            thread_id,
            "player",
            text=text,
            message_id=message_id,
            mark_unread=False,
        )


    def phone_mark_thread_read(thread_id):
        """Mark every currently delivered message in a thread as read."""
        thread = _phone_ensure_thread(thread_id)
        for message in thread:
            message["read"] = True
        renpy.store.phone_last_open_thread = thread_id


    def phone_thread_unread_count(thread_id):
        return sum(
            1 for message in _phone_ensure_thread(thread_id)
            if message.get("incoming", False) and not message.get("read", False)
        )


    def phone_total_unread():
        return sum(phone_thread_unread_count(thread_id) for thread_id in PHONE_THREAD_ORDER)


    def phone_thread_preview(thread_id):
        thread = _phone_ensure_thread(thread_id)
        if not thread:
            return "No messages yet"

        message = thread[-1]
        text = message.get("text", "").strip()
        if text:
            return text if len(text) <= 42 else text[:39] + "..."
        if message.get("attachment_id"):
            return "Photo attachment"
        return "Message"


    def _phone_next_debug_batch():
        """Return the next developer seed number based on currently stored test batches."""
        batch_numbers = []

        for thread_id in list(renpy.store.phone_messages.keys()):
            for message in _phone_ensure_thread(thread_id):
                message_id = message.get("id", "")
                if message_id.startswith("dev_phone_seed_"):
                    parts = message_id.split("_")
                    if len(parts) >= 5:
                        try:
                            batch_numbers.append(int(parts[3]))
                        except ValueError:
                            pass

        return (max(batch_numbers) + 1) if batch_numbers else 1


    def phone_debug_seed_messages():
        """Add a fresh batch of developer-only messages every time this is pressed.

        Story messages remain idempotent when they use stable IDs. Repeated batches
        are only for stress-testing unread counts, scrolling, notifications, and
        image attachments / Photos indexing.
        """
        batch = _phone_next_debug_batch()
        batch_tag = "{:03d}".format(batch)

        phone_add_message(
            "leia",
            "leia",
            text="[DEV {}] Phone shell test message from {}.".format(batch_tag, renpy.store.girlfriend_name),
            message_id="dev_phone_seed_{}_leia_text".format(batch_tag),
            mark_unread=True,
        )

        phone_add_message(
            "group",
            "julian",
            text="[DEV {}] Placeholder group chat message.".format(batch_tag),
            message_id="dev_phone_seed_{}_group_text".format(batch_tag),
            mark_unread=True,
        )

        phone_add_message(
            "leia",
            "leia",
            text="[DEV {}] Image attachment stress test.".format(batch_tag),
            message_id="dev_phone_seed_{}_leia_photo".format(batch_tag),
            attachment_id="dev_placeholder_photo_{}".format(batch_tag),
            attachment_label="Placeholder Leia photo — batch {}".format(batch),
            mark_unread=True,
            notify=True,
            notification_title=phone_thread_label("leia"),
        )

        renpy.store.modified_save = True
        return None


    def phone_debug_clear_messages():
        """Clear developer phone state without advancing the underlying interaction."""
        renpy.store.phone_messages = {
            "leia": [],
            "julian": [],
            "group": [],
        }
        renpy.store.phone_last_open_thread = None
        renpy.store.phone_photos = []
        renpy.store.modified_save = True
        renpy.notify("Developer phone messages and Photos cleared.")
        return None
