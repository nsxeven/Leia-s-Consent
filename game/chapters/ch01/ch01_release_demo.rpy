# Release-only demo switch. MAIN is the unrestricted development build.
# Versioned release branches opt into the Day One demo gate independently.
define LC_DAY1_DEMO_BUILD = False

default persistent.ch01_day1_demo_completed = False
default persistent.lc_adult_notice_accepted = False

label lc_adult_notice:
    scene black
    with fade
    centered "{size=56}MATURE CONTENT — 18+{/size}\n{size=30}This fictional visual novel is intended only for adults.{/size}"
    menu:
        "I am 18 or older. Continue.":
            $ persistent.lc_adult_notice_accepted = True
            $ renpy.save_persistent()
        "Exit to the main menu.":
            pass
    return

label ch01_day1_demo_complete:
    $ persistent.ch01_day1_demo_completed = True
    $ renpy.save_persistent()
    scene black
    with fade
    centered "{size=56}THANK YOU FOR PLAYING{/size}\n{size=31}This demo includes the Prologue and Chapter One, Day One.{/size}\n{size=28}More of the story is in development.{/size}"
    return
