# Prologue + Day One standalone public demo gate.
# Set to False in a later full-chapter release after Days 2+ are approved.
define LC_DAY1_DEMO_BUILD = True

default persistent.ch01_day1_demo_completed = False

label ch01_day1_demo_complete:
    $ persistent.ch01_day1_demo_completed = True
    $ renpy.save_persistent()
    scene black
    with fade
    centered "{size=56}THANK YOU FOR PLAYING{/size}\n{size=31}This demo includes the Prologue and Chapter One, Day One.{/size}\n{size=28}More of the story is in development.{/size}"
    return
