# Chapter Select screen - pick a day and a route preset, then start there
#
# Purpose: Menu page (tag menu) listing the days and route presets from systems/chapter_select.rpy;
#   Start stores the pick and starts a new game through ch01_chapter_select_entry. The days,
#   route lists and headings come from the presets the Day packs register (CHAPTER_SELECT_PRESETS). Shown only when
#   chapter_select_unlocked(). QA gallery buttons appear when gallery_qa_tools_enabled().
#
# Public API (call these from scenes/screens):
#   screen chapter_select()                   the Chapter Select page
#
# Example:
#   ShowMenu("chapter_select")      (journal tabs in screens/scrapbook_ui.rpy)
#
# Depends on: systems/chapter_select.rpy, systems/gallery.rpy, screens/scrapbook_ui.rpy (game_menu)
# Hooks: none
# Load order: default (screens at init -500)
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_lc_chapters.py, tests/test_release_from_main.py

screen chapter_select():

    tag menu

    default cs_day = chapter_select_default_day()
    default cs_route = "love"

    use game_menu(_("Chapter Select"), scroll="viewport"):

        vbox:
            spacing 22
            xfill True

            text "CHAPTERS" size 48 color "#3b2a30" font "fonts/Handjet-ExtraBold.ttf"
            text "DIARY DIVIDERS" size 24 color "#7a6266" font "fonts/Handjet-SemiBold.ttf"
            text _("Developer / QA shortcut. This starts a new game with a preset of the earlier story state; it does not play the skipped scenes.") size 28 color "#7a6266" font "fonts/Caveat[wght].ttf"

            text _("Chapter") size 30
            hbox:
                spacing 16
                box_wrap True
                for day_id, day_label, day_note in chapter_select_days():
                    textbutton day_label:
                        action [SetScreenVariable("cs_day", day_id), SetScreenVariable("cs_route", "love")]
                        selected (cs_day == day_id)

            $ cs_routes = CHAPTER_SELECT_PRESETS[cs_day]["routes"]
            text CHAPTER_SELECT_PRESETS[cs_day]["heading"] size 30
            vbox:
                spacing 8
                for route_id, route_label in cs_routes:
                    textbutton route_label:
                        action SetScreenVariable("cs_route", route_id)
                        selected (cs_route == route_id)

            textbutton _("Begin"):
                action [SetField(persistent, "ch01_chapter_select_pending", (cs_day, cs_route)), Start("ch01_chapter_select_entry")]
                text_size 36

            if gallery_qa_tools_enabled():
                text _("QA (developer only)") size 30
                hbox:
                    spacing 16
                    textbutton _("Unlock all Gallery entries") action Function(debug_unlock_all_gallery)
                    textbutton _("Reset Gallery unlocks and seen CGs") action Function(debug_reset_gallery)
