# Chapter 1 pool-photo Capture inventory + Phone delivery.
#
# Scene 5 stores ch01_pool_capture_count (1–3). This module is the single
# implementation that maps that count + selected swimsuit to actual Capture
# assets and sends the earned photos to Trip Group. The trigger/timing lives in
# ch01_phone_moments.rpy.

init 50 python:

    def ch01_pool_capture_assets():
        """Return the actual saved Capture photos earned during Scene 5."""
        outfit = get_story_value("ch01_pool_outfit", "pool_conservative")
        suffix = "b" if outfit == "pool_bolder" else "a"
        count = int(get_story_value("ch01_pool_capture_count", 1))
        count = max(0, min(3, count))
        # Zero is intentional: the early-stop branch deletes the only
        # solo photograph. Do not resurrect it by coercing 0 to 1.
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
                attachment_label="{} pool photo {:02d}".format(renpy.store.girlfriend_name, index + 1),
                mark_unread=True,
                notify=final,
                notification_title="Trip Group",
            )
            # phone_add_message() automatically indexes image attachments in Photos.

        set_story_value("ch01_pool_phone_solo_photo_count", len(assets))
        set_story_value("ch01_pool_phone_attachment_count", len(assets))
        set_story_flag("ch01_pool_photos_shared_to_group")
        return None


# Capture assets are defined in ch01_scenes_04_06_visuals.rpy.
