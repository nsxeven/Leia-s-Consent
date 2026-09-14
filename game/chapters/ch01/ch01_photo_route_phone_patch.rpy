# Chapter 1 pool-photo route continuity patch.
#
# Scene 5 has materially different photo inventories:
# - confident / "try one sitting by the edge" route: Leia takes a posed shot,
#   then explicitly asks Julian to take another one. Two solo photos therefore
#   exist for later Phone delivery.
# - relaxed/supportive and protective-but-continues routes: one keeper solo photo.
# - stopped route: only the group photo survives.
#
# Keep the Trip Group beat rollback/load safe with stable message IDs and one
# notification total, regardless of how many attachments the route earned.

init 50 python:

    def ch01_pool_bonus_photo_asset():
        """Return the extra solo-photo asset earned only on the confident route."""
        if get_story_value("ch01_photo_outcome") != "confident":
            return None

        pool_outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
        suffix = "b" if pool_outfit == "pool_bolder" else "a"
        return "ch01_photo_more_second_{}".format(suffix)


    def ch01_share_pool_photos_to_trip_group():
        """Share exactly the pool photos that exist on the selected Scene 5 route."""
        if has_story_flag("ch01_pool_photos_shared_to_group"):
            return None

        selected_photo = get_story_value(
            "ch01_selected_photo_asset",
            "ch01_photo_group",
        )
        bonus_photo = ch01_pool_bonus_photo_asset()

        # The shared group photo always exists.
        # On branches with solo photos, keep this first message quiet and put
        # the single notification on the final earned solo attachment.
        if selected_photo != "ch01_photo_group":
            phone_add_message(
                "group",
                "julian",
                text="",
                message_id="ch01_trip_group_pool_photo_group",
                attachment_id="ch01_photo_group",
                attachment_label="Pool photo — the three of us",
                mark_unread=True,
                notify=False,
            )

            phone_add_message(
                "group",
                "julian",
                text=("" if bonus_photo else "Am I the best photographer or what?"),
                message_id="ch01_trip_group_pool_photo_favourite",
                attachment_id=selected_photo,
                attachment_label="Leia's favourite pool photo",
                mark_unread=True,
                notify=(bonus_photo is None),
                notification_title="Trip Group",
            )

            # Only the confident route earned this additional shot because Leia
            # explicitly asked for another photo after the first directed pose.
            if bonus_photo:
                phone_add_message(
                    "group",
                    "julian",
                    text="Am I the best photographer or what?",
                    message_id="ch01_trip_group_pool_photo_bonus",
                    attachment_id=bonus_photo,
                    attachment_label="Leia's second pool favourite",
                    mark_unread=True,
                    notify=True,
                    notification_title="Trip Group",
                )
                set_story_value("ch01_pool_phone_solo_photo_count", 2)
            else:
                set_story_value("ch01_pool_phone_solo_photo_count", 1)

        else:
            # If Leia stopped the solo shoot, only the group image exists.
            phone_add_message(
                "group",
                "julian",
                text="Am I the best photographer or what?",
                message_id="ch01_trip_group_pool_photo_group",
                attachment_id="ch01_photo_group",
                attachment_label="Pool photo — the three of us",
                mark_unread=True,
                notify=True,
                notification_title="Trip Group",
            )
            set_story_value("ch01_pool_phone_solo_photo_count", 0)

        set_story_value(
            "ch01_pool_phone_attachment_count",
            1 + get_story_value("ch01_pool_phone_solo_photo_count", 0),
        )
        set_story_flag("ch01_pool_photos_shared_to_group")
        return None


# Placeholder assets for the extra confident-route photo. Final ComfyUI art can
# replace these IDs without changing story/Phone state.
image cg ch01_photo_more_second_a = Text(
    "CH01 POOL PHOTO — CONFIDENT ROUTE\nSECOND SOLO SHOT — CONSERVATIVE SWIMWEAR\n\nPlaceholder",
    size=42,
    color="#ffffff",
    text_align=0.5,
    xalign=0.5,
    yalign=0.5,
)

image cg ch01_photo_more_second_b = Text(
    "CH01 POOL PHOTO — CONFIDENT ROUTE\nSECOND SOLO SHOT — BOLDER SWIMWEAR\n\nPlaceholder",
    size=42,
    color="#ffffff",
    text_align=0.5,
    xalign=0.5,
    yalign=0.5,
)
