# Phone overlay registration - register the phone HUD overlay
#
# Purpose: Only registers the phone_quick_access overlay (screens/phone_hud.rpy). The handset screen
#   phone_screen lives in screens/phone_sweetheart.rpy.
#
# Public API: none - registration only
#
# Example:
#   (nothing to call)
#
# Depends on: screens/phone_hud.rpy
# Hooks: none (appends phone_quick_access to config.overlay_screens)
# Load order: default (init 0); keeps the overlay's place in config.overlay_screens
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_effective_fingerprints.py (overlay order)

init python:
    if "phone_quick_access" not in config.overlay_screens:
        config.overlay_screens.append("phone_quick_access")

