# Non-intrusive developer feedback helpers.
# These replace temporary dialogue lines for state inspection so testing does
# not require clicking through say screens or reopening development tools.

init python:

    def _dev_notify(text):
        renpy.notify(text)
        return None


    def dev_notify_character_names():
        return _dev_notify(
            "You: {} | Girlfriend: {} | Friend: {}".format(
                renpy.store.player_name,
                renpy.store.girlfriend_name,
                renpy.store.friend_name,
            )
        )


    def dev_notify_sprite_state():
        return _dev_notify(
            "Sprite: {} / {} | Outfit: {}".format(
                leia_pose_label(),
                leia_expression_label(),
                current_outfit_name(),
            )
        )


    def dev_notify_choice_state():
        last_choice = renpy.store.last_choice_id or "None"
        return _dev_notify(
            "Last choice: {} | Recorded: {}".format(
                last_choice,
                len(renpy.store.choice_history),
            )
        )


    def dev_notify_economy_state():
        return _dev_notify(
            "Money: ${} | Equipped: {} | Owned: {} | Wear path: {}".format(
                renpy.store.money,
                current_outfit_name(),
                len(valid_owned_outfit_ids()),
                renpy.store.last_wear_route or "None",
            )
        )


    def dev_notify_gallery_state():
        return _dev_notify(
            "Gallery unlocked: {} / {}".format(
                gallery_unlocked_count(),
                gallery_total_count(),
            )
        )


    def dev_notify_checkpoint_state():
        last_choice = renpy.store.last_choice_id or "None"
        return _dev_notify(
            "Checkpoint — ${} | {} | {} / {} | Last choice: {} | Choices: {}".format(
                renpy.store.money,
                current_outfit_name(),
                leia_pose_label(),
                leia_expression_label(),
                last_choice,
                len(renpy.store.choice_history),
            )
        )
