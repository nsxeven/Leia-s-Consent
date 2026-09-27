# Chapter One — diegetic Phone story moments.
#
# Keep Phone beats separate from visible scene dialogue where possible so the
# handset feels like a living background system rather than an exposition stop.
# Stable message IDs + story flags make these moments rollback/load safe.

init python:

    if "ch01_phone_story_triggers" not in config.overlay_screens:
        config.overlay_screens.append("ch01_phone_story_triggers")


    # Pool-photo delivery is defined once in ch01_photo_route_phone_patch.rpy.
    # Keep this file responsible only for the story trigger/timing.



screen ch01_phone_story_triggers():

    # Scene 7 starts immediately after the towel incident. Waiting until Ryan
    # has answered Leia's question makes Julian's unrelated photo drop land
    # naturally during the couple's getting-ready window without adding any
    # on-screen narration or dialogue.
    if (
        phone_unlocked
        and has_story_flag("ch01_scene_06_complete")
        and has_story_value("ch01_towel_followup")
        and not has_story_flag("ch01_pool_photos_shared_to_group")
    ):
        timer 0.10 action Function(ch01_share_pool_photos_to_trip_group)
