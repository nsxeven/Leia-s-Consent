# Phone quick-access overlay registration.
# The active handset screen (phone_screen) lives in phone_sweetheart.rpy;
# the old base copy that used to sit here was dead code and was removed in the
# clean-up (it was always replaced by the later definition).

# Diegetic in-game phone hub.
# Bright, playful presentation with rounded mobile UI surfaces.

init python:
    if "phone_quick_access" not in config.overlay_screens:
        config.overlay_screens.append("phone_quick_access")

