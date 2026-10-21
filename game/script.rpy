# Leia's Consent — main entry point.
# Keep this file intentionally small; story content lives in chapter files.

label start:
    if LC_DAY1_DEMO_BUILD and not persistent.lc_adult_notice_accepted:
        call lc_adult_notice
    if LC_DAY1_DEMO_BUILD and not persistent.lc_adult_notice_accepted:
        return
    jump prologue_name_setup
