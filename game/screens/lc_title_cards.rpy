# Title cards - the polaroid Chapter card and the ticket-stub Part card
#
# Purpose: Animated, skippable title cards (darryn 2026-11-19). The Chapter card opens each day as a
#   taped polaroid (drops in with a small tilt, holds, lifts away); the Part card marks a part inside
#   a day as a ticket stub in the day's accent colour (slides in, holds, slides out). Display only:
#   chapter ids, saves and gallery keys never change.
#
# Public API (call these from scenes):
#   label lc_chapter_card(chapter_id)          polaroid: 'CHAPTER TWO / Plus One / Day Two' (call it)
#   label lc_part_card(chapter_id, number)
#       ticket stub: 'PART 3 | DAY TWO / Evening / Just Us' (call it); title and route subtitle
#       come from the Day pack's CHAPTER["parts"]; also names new saves after the part
#   lc_title_card_accent(chapter_id) -> str    the day's accent colour
#
# Example:
#   scene black
#   with fade
#   call lc_chapter_card("day2")
#   call lc_part_card("day2", 1)
#
# Notes: a click skips the hold at once and the exit still plays (input never waits on a wind-up).
#   Text is live Ren'Py text, so titles change in lc_chapters / the Day pack, never in art.
#
# Depends on: systems/lc_chapters.rpy (lc_part_begin, lc_chapters), gui/scrapbook/*.png,
#   screens/scrapbook_ui.rpy (lc_ui_play)
# Hooks: none
# Load order: any (labels and screens only; the accent table at init 0)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_day2_parts.py, tests/test_lc_chapters.py

init -5 python:
    import lc_chapters

    # One accent per day, matching its gallery tab: each Day pack's *_chapter.rpy defines
    # lc_title_card_accent_<chapter_id>.
    def lc_title_card_accent(chapter_id):
        return getattr(store, "lc_title_card_accent_" + chapter_id, "#70566f")


transform lc_polaroid_motion:
    on show:
        alpha 0.0 rotate -9 zoom 0.92 yoffset 60
        easein 0.6 alpha 1.0 rotate -3 zoom 1.0 yoffset 0
    on hide:
        easeout 0.5 alpha 0.0 rotate 2 zoom 0.97 yoffset -70

transform lc_ticket_motion:
    on show:
        alpha 0.0 xoffset 220
        easein 0.5 alpha 1.0 xoffset 0
    on hide:
        easeout 0.45 alpha 0.0 xoffset -260

transform lc_card_backdrop:
    on show:
        alpha 0.0
        linear 0.4 alpha 1.0
    on hide:
        linear 0.45 alpha 0.0


screen lc_chapter_card_screen(heading, title, day, accent):
    zorder 150
    add Solid("#140e1c99") at lc_card_backdrop
    fixed at lc_polaroid_motion:
        xysize (760, 560)
        align (0.5, 0.5)
        add Frame("gui/scrapbook/frame_polaroid.png", 12, 12) xysize (760, 560)
        add Transform("gui/scrapbook/tape_pink_h.png", zoom=1.4, rotate=4) align (0.5, 0.0) yoffset -26
        vbox:
            align (0.5, 0.42)
            spacing 10
            text heading.upper() font "fonts/Nunito-ExtraBold.ttf" size 26 color accent kerning 6 xalign 0.5
            text title font "fonts/PatrickHand-Regular.ttf" size 84 color "#2a1f33" xalign 0.5 textalign 0.5
            if day:
                text day font "fonts/Caveat-SemiBold.ttf" size 40 color "#70566f" xalign 0.5


screen lc_part_card_screen(day, number, title, subtitle, accent):
    zorder 150
    add Solid("#140e1c80") at lc_card_backdrop
    hbox at lc_ticket_motion:
        align (0.5, 0.5)
        frame:
            xysize (210, 230)
            padding (0, 0)
            background Solid(accent)
            vbox:
                align (0.5, 0.5)
                text "PART" font "fonts/Nunito-ExtraBold.ttf" size 22 color "#f4ebdc" kerning 5 xalign 0.5
                text str(number) font "fonts/PatrickHand-Regular.ttf" size 110 color "#f4ebdc" xalign 0.5
        # Perforation between the stub and the ticket.
        vbox:
            spacing 10
            yalign 0.5
            for _i in range(12):
                add Solid("#f4ebdc") xysize (4, 9)
        frame:
            xysize (620, 230)
            padding (48, 0, 40, 0)
            background Frame("gui/scrapbook/frame_ticket.png", 18, 18)
            vbox:
                yalign 0.5
                spacing 4
                if day:
                    text day.upper() font "fonts/Nunito-ExtraBold.ttf" size 22 color accent kerning 6
                text title font "fonts/PatrickHand-Regular.ttf" size (76 if not subtitle else 66) color "#2a1f33"
                if subtitle:
                    text subtitle font "fonts/Caveat-SemiBold.ttf" size 44 color accent


label lc_chapter_card(chapter_id):
    $ lc_ui_play("paper")
    show screen lc_chapter_card_screen(lc_chapters.chapter_heading(chapter_id), lc_chapters.chapter_title(chapter_id), lc_chapters.day_label(chapter_id), lc_title_card_accent(chapter_id))
    $ renpy.pause(2.6)
    hide screen lc_chapter_card_screen
    $ renpy.pause(0.55, hard=True)
    return


label lc_part_card(chapter_id, number):
    # Title + route subtitle from the Day pack (CHAPTER["parts"]); every mode shows the subtitle.
    $ _lc_part = lc_part_title(chapter_id, number)
    $ lc_part_begin(chapter_id, number, _lc_part[0], _lc_part[1])
    $ lc_ui_play("paper")
    show screen lc_part_card_screen(lc_chapters.day_label(chapter_id), number, _lc_part[0], _lc_part[1], lc_title_card_accent(chapter_id))
    $ renpy.pause(2.2)
    hide screen lc_part_card_screen
    $ renpy.pause(0.5, hard=True)
    return
