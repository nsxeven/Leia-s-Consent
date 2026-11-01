# Leia's Consent — main entry point.
# Keep this file intentionally small; story content lives in chapter files.

label start:
    # Capture harness only. A normal launch never sets LC_SHOT.
    python:
        import os
        if os.environ.get("LC_SHOT"):
            renpy.jump("lc_scrapbook_preview")
    # One gate for a normal new game, in the full build and the demo.
    # Accepting stores a persistent flag, so a later Start does not show it again.
    # Declining returns here with the flag still clear and leaves for the main menu.
    if not persistent.lc_adult_notice_accepted:
        call lc_adult_notice
    if not persistent.lc_adult_notice_accepted:
        return
    jump prologue_name_setup
