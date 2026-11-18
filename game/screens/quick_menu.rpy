# Quick menu - the keycap row under the dialogue box
#
# Purpose: Replaces Ren'Py's stock quick_menu (desktop and touch variants): Back, Log, Skip, Auto,
#   Save, Q.Save, Q.Load, Prefs keycaps plus the time-of-day caption. Hidden while a journal page or
#   the phone covers the scene.
#
# Public API (call these from scenes/screens):
#   screen quick_menu()                       keycap quick menu (desktop and touch variants)
#
# Example:
#   (nothing to call: config.always_shown_screens shows it, screens/scrapbook_ui.rpy)
#
# Depends on: screens/scrapbook_ui.rpy (lc_keycap_button, lc_day_caption, lc_journal_menu_open,
#   lc_phone_covers_scene)
# Hooks: none
# Load order: default (screens at init -500); defined only here, so it replaces the stock screen
# Docs: docs/DIALOGUE_STYLE.md   Tests: tests/test_scrapbook_ui.py, tests/test_glass_menu.py

## Quick menu #################################################################

screen quick_menu():
    zorder 100

    if quick_menu and not lc_journal_menu_open() and not lc_phone_covers_scene():
        # Same layout under the box for sprites and CGs. Keys stay opaque;
        # only unavailable ones dim (lc_keycap_state).
        $ ghost = False
        hbox:
            xpos 132
            ypos 1040
            spacing 0
            use lc_keycap_button(lc_day_caption(), NullAction(), ghost=ghost)

        hbox:
            xpos 1788
            xanchor 1.0
            ypos 1040
            spacing 8
            use lc_keycap_button("BACK", Rollback(), "gui/scrapbook/icon_back.png", ghost=ghost)
            use lc_keycap_button("LOG", ShowMenu("history"), "gui/scrapbook/icon_log.png", ghost=ghost)
            use lc_keycap_button("SKIP", Skip(), "gui/scrapbook/icon_skip.png", ghost=ghost)
            use lc_keycap_button("AUTO", Preference("auto-forward", "toggle"), "gui/scrapbook/icon_auto.png", selected_on=preferences.afm_enable, ghost=ghost)
            use lc_keycap_button("SAVE", ShowMenu("save"), "gui/scrapbook/icon_save.png", ghost=ghost)
            use lc_keycap_button("Q.SAVE", QuickSave(), "gui/scrapbook/icon_qsave.png", ghost=ghost)
            use lc_keycap_button("Q.LOAD", QuickLoad(), "gui/scrapbook/icon_qload.png", ghost=ghost)
            use lc_keycap_button("PREFS", ShowMenu("preferences"), "gui/scrapbook/icon_prefs.png", ghost=ghost)


screen quick_menu():
    variant "touch"
    zorder 100

    if quick_menu and not lc_journal_menu_open() and not lc_phone_covers_scene():
        hbox:
            xalign 0.5
            ypos 1020
            spacing 10
            use lc_keycap_button("BACK", Rollback(), "gui/scrapbook/icon_back.png")
            use lc_keycap_button("SKIP", Skip(), "gui/scrapbook/icon_skip.png")
            use lc_keycap_button("AUTO", Preference("auto-forward", "toggle"), "gui/scrapbook/icon_auto.png")
            use lc_keycap_button("MENU", ShowMenu("save"), "gui/scrapbook/icon_save.png")
