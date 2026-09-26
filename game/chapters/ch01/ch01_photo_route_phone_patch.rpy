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

    def ch01_pool_capture_assets():
        """Return the actual saved Capture photos earned during Scene 5."""
        outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
        suffix = "b" if outfit == "pool_bolder" else "a"
        count = int(get_story_value("ch01_pool_capture_count", 1) or 1)
        count = max(1, min(3, count))
        return ["ch01_photo_capture_{:02d}_{}".format(i, suffix) for i in range(1, count + 1)]


    def ch01_share_pool_photos_to_trip_group():
        """Julian sends every earned Capture; attachments persist in Photos."""
        if has_story_flag("ch01_pool_photos_shared_to_group"):
            return None

        assets = ch01_pool_capture_assets()
        for index, asset_id in enumerate(assets):
            final = index == len(assets) - 1
            phone_add_message(
                "group",
                "julian",
                text=("Am I the best photographer or what?" if final else ""),
                message_id="ch01_trip_group_pool_capture_{:02d}".format(index + 1),
                attachment_id=asset_id,
                attachment_label="Leia pool photo {:02d}".format(index + 1),
                mark_unread=True,
                notify=final,
                notification_title="Trip Group",
            )
            # Index explicitly because the active phone_add_message compatibility
            # wrapper does not expose the newer save_attachment keyword.
            phone_add_photo(
                asset_id,
                asset_id,
                "Leia pool photo {:02d}".format(index + 1),
                source_thread="group",
                source_message_id="ch01_trip_group_pool_capture_{:02d}".format(index + 1),
            )

        set_story_value("ch01_pool_phone_solo_photo_count", len(assets))
        set_story_value("ch01_pool_phone_attachment_count", len(assets))
        set_story_flag("ch01_pool_photos_shared_to_group")
        return None


# Capture assets are defined in ch01_scenes_04_06_visuals.rpy.
