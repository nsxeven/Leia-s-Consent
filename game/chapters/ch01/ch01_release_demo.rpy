# Release-only demo switch. MAIN is the unrestricted development build.
# Versioned release branches opt into the Day One demo gate independently.
# release/prologue-day1-demo-v1.0.0: first public Prologue + Day One demo, gate ON.
define LC_DAY1_DEMO_BUILD = True

default persistent.ch01_day1_demo_completed = False
default persistent.lc_adult_notice_accepted = False

label lc_adult_notice:
    call screen lc_adult_notice_screen
    return

# Demo build: the Gallery only lists the Prologue and Day 1 tabs, so later-day
# entries (titles, counts, placeholders) are not shown. Runs after gallery.rpy
# (init 0) has built GALLERY_ENTRIES.
init 1 python:
    if LC_DAY1_DEMO_BUILD:
        LC_DEMO_GALLERY_TABS = ("prologue", "ch01_d1")
        GALLERY_TABS = tuple(t for t in GALLERY_TABS if t[0] in LC_DEMO_GALLERY_TABS)
        GALLERY_TAB_IDS = tuple(t[0] for t in GALLERY_TABS)
        GALLERY_ENTRIES = dict((k, v) for k, v in GALLERY_ENTRIES.items() if v["tab"] in LC_DEMO_GALLERY_TABS)

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
