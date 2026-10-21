# Compatibility entry for saves made while the Scene 13 source-level override existed.
# The single authoritative Scene 13 now lives in ch01_scenes_07_13.rpy.
# Keep this alias for older development save entry points. No config.label_callback
# or runtime redirection is needed for fresh playthroughs.

label ch01_scene_13_back_at_villa_asleep_revision:
    jump ch01_scene_13_back_at_villa
