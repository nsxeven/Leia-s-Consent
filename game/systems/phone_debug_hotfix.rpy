# Hotfix for developer phone actions.
# Ren'Py Function actions treat a non-None function return as an interaction result.
# Returning True from the seed helper could therefore advance the underlying say/menu
# interaction even while the phone was open. Keep these developer actions returning
# None so they only mutate phone test state and refresh the phone UI.

init 10 python:

    def phone_debug_seed_messages():
        """Add a fresh developer-only test batch without advancing story/UI behind the phone."""
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
        )

        renpy.store.modified_save = True
        renpy.notify("Added developer phone message batch {}.".format(batch))
        return None


    def phone_debug_clear_messages():
        """Clear developer phone state without returning an interaction result."""
        renpy.store.phone_messages = {
            "leia": [],
            "julian": [],
            "group": [],
        }
        renpy.store.phone_last_open_thread = None
        renpy.store.modified_save = True
        renpy.notify("Developer phone messages cleared.")
        return None
