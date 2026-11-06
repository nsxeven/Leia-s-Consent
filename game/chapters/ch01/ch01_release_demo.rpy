# Release-only demo switch. MAIN is the unrestricted development build.
# Versioned release branches opt into the Day One demo gate independently.
define LC_DAY1_DEMO_BUILD = False

default persistent.ch01_day1_demo_completed = False
default persistent.lc_adult_notice_accepted = False

label lc_adult_notice:
    call screen lc_adult_notice_screen
    return

label ch01_day1_demo_complete:
    $ persistent.ch01_day1_demo_completed = True
    $ renpy.save_persistent()
    # Thank-you card with upcoming releases, Patreon and Discord (darryn).
    $ phone_hud_enabled = False
    $ quick_menu = False
    window hide
    scene black
    with fade
    call screen lc_demo_end_screen
    $ lc_bgm_stop(1.5)
    return
