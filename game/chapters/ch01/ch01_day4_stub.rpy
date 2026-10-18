# Leia's Consent — Chapter 1 Day 4 PLACEHOLDER.
#
# PLACEHOLDER ONLY. This stub is NOT story content. It exists so that the
# Day 3 -> Day 4 link has a real target and the build ends cleanly.
# Replace it with the Scriptwriter's approved Day Four script:
#   1. Keep the label name ch01_day4_start (Day Three jumps to it), or change the
#      jump at the end of ch01_day3_bedroom in ch01_day3_scenes.rpy.
#   2. Delete this file once the real Day Four entry label exists.
#   3. Follow the Day 1 -> 2 pattern: title card, set ch01_day_04_started, then scenes.

label ch01_day4_start:

    scene black
    with fade

    centered "{size=36}End of the current build. Day Four continues in the next update.{/size}"

    # End of the playable build: return with an empty call stack ends the game
    # and goes back to the main menu.
    return
