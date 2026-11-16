# Phone input blocker - absorb clicks behind the open phone
#
# Purpose: Transparent full-screen button under the phone overlay so clicks never reach the story or
#   menu controls behind the handset. Registered as an overlay.
#
# Public API (call these from scenes/screens):
#   screen phone_input_blocker()              the click guard (zorder 309, only while phone_screen
#       shows)
#
# Example:
#   (nothing to call: it shows by itself whenever phone_screen is up)
#
# Depends on: screens/phone_sweetheart.rpy (phone_screen)
# Hooks: none (appends itself to config.overlay_screens)
# Load order: default (init 0 registration)
# Docs: docs/ARCHITECTURE.md   Tests: none directly (lint)

init python:
    if "phone_input_blocker" not in config.overlay_screens:
        config.overlay_screens.append("phone_input_blocker")


screen phone_input_blocker():

    zorder 309

    if renpy.get_screen("phone_screen"):
        button:
            xfill True
            yfill True
            background Solid("#00000000")
            hover_background Solid("#00000000")
            action NullAction()
