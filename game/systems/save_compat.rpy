# Save compatibility: old names kept only so older saves and rollback still resolve.
#
# Ren'Py saves remember where the player is by label name (and, mid-scene, by
# statement identity). When a scene changes its label, an older save or the
# rollback log may still point at the old name, so the old name stays here as a
# one-line `jump` to the label that owns the scene now.
#
# Rules:
# - Never jump to or call these names from story code; use the target label.
# - Never delete an entry: the saves listed beside it would stop loading.
# - New entries say which saves need them.
# - Every entry here is a single `jump`, so tests/lc_rpy_model.py resolves it to its
#   target and the label fingerprints stay pinned to the code that really runs.


# Clean-up PR 3 folded the five config.label_overrides back into the labels they
# replaced. Until then these were the bodies that actually ran, so a save or rollback
# made inside those scenes names them.

# Needed by: saves made inside Day Two scene 3 (Maya's breakfast message) before clean-up PR 3.
label ch01_day2_scene_03_maya_message_v2:
    jump ch01_day2_scene_03_maya_message

# Needed by: saves made inside Day Two scene 8 (Maya meets Julian) before clean-up PR 3.
label ch01_day2_scene_08_maya_julian_v2:
    jump ch01_day2_scene_08_maya_julian

# Needed by: saves made inside Day Two scene 13 (the girls upstairs) before clean-up PR 3.
label ch01_day2_scene_13_girls_upstairs_v2:
    jump ch01_day2_scene_13_girls_upstairs

# Needed by: saves made inside Day Two scene 14 (bikini tie foreshadow) before clean-up PR 3.
label ch01_day2_scene_14_tie_foreshadow_v2:
    jump ch01_day2_scene_14_tie_foreshadow

# Needed by: saves made inside Day One scene 27 (late photo drop) before clean-up PR 3.
label ch01_scene_27_late_photo_drop_staged:
    jump ch01_scene_27_late_photo_drop


# Needed by: development saves made while the Scene 13 source-level override existed
# (formerly zz_ch01_scene_13_asleep_revision.rpy). Scene 13 lives in ch01_scenes_07_13.rpy.
label ch01_scene_13_back_at_villa_asleep_revision:
    jump ch01_scene_13_back_at_villa

# Needed by: development saves that reference the old Day Two outfit-control scene
# (formerly zzzzz_ch01_love_outfit_control.rpy). Outfit selection is integrated into the
# canonical Day Two scene 21 flow in ch01_day2_scenes_16_30.rpy.
label ch01_day2_scene_20_dinner_outfit_love_control:
    jump ch01_day2_scene_20_dinner_outfit

# Needed by: development saves created before Pacing Revision v2 (Day One scenes 17 and 24
# were merged into 18 and 25; formerly at the end of ch01_scenes_14_30.rpy).
label ch01_scene_17_julian_notices:
    jump ch01_scene_18_private_under_blanket

label ch01_scene_24_looking_counts:
    jump ch01_scene_25_julian_put_on_spot


# Needed by: saves from the 2026-11-10 to 11-14 builds (formerly in the root
# zzzz_ch01_breakfast_presentation.rpy; screens register at init -500 wherever they live).
# Old-save compatibility (builds from 2026-11-10 to 11-14 used a blocking
# `call screen lc_breakfast_julian_pov`). A save made while that screen was up
# still names it in its screen stack, so the screen must exist. This stub draws
# nothing, takes no input and immediately returns None (= "keep reading"), so
# the story carries on with the shared Hidden POV cue. Do not use it for new
# content.
screen lc_breakfast_julian_pov(*args, **kwargs):
    zorder 0
    timer 0.01 action Return(None)
