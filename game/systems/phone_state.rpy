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


    def phone_add_message(
        thread_id,
        sender_id,
        text="",
        message_id=None,
        attachment_id=None,
        attachment_label=None,
        mark_unread=True,
    ):
        """Add one story message, optionally with a future image attachment.

        Supplying a stable message_id makes the operation idempotent. This is
        important when story labels can be revisited after rollback/load.
        """
        thread = _phone_ensure_thread(thread_id)

        if message_id is None:
            message_id = "{}_{}".format(thread_id, len(thread) + 1)

        if phone_has_message(message_id):
            return False

        incoming = sender_id != "player"
        thread.append({
            "id": message_id,
            "sender": sender_id,
            "text": text,
            "attachment_id": attachment_id,
            "attachment_label": attachment_label or "Photo attachment",
            "incoming": incoming,
            "read": not (incoming and mark_unread),
        })
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


    def phone_debug_seed_messages():
        """Developer-only placeholder content for UI testing."""
        added_any = False

        added_any = phone_add_message(
            "leia",
            "leia",
            text="[DEV] Phone shell online. This thread can later hold story texts and selfies.",
            message_id="dev_phone_leia_01",
            mark_unread=True,
        ) or added_any

        added_any = phone_add_message(
            "group",
            "julian",
            text="[DEV] Placeholder group chat message.",
            message_id="dev_phone_group_01",
            mark_unread=True,
        ) or added_any

        added_any = phone_add_message(
            "leia",
            "leia",
            text="[DEV] Image attachments are scaffolded already.",
            message_id="dev_phone_leia_photo_01",
            attachment_id="dev_placeholder_photo",
            attachment_label="Placeholder Leia photo",
            mark_unread=True,
        ) or added_any

        if added_any:
            renpy.store.modified_save = True
        return added_any


    def phone_debug_clear_messages():
        renpy.store.phone_messages = {
            "leia": [],
            "julian": [],
            "group": [],
        }
        renpy.store.phone_last_open_thread = None
        renpy.store.modified_save = True
