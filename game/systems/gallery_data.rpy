# Gallery data - the engine half: the helpers every Day pack's *_gallery.rpy uses
#
# Purpose: Each Day pack registers its Gallery tab and rows in its own *_gallery.rpy
#   (game/chapters/<day folder>/, init -2): one gallery_row per scene sequence (moment), pages =
#   the stable `cg <name>` images in display order. Unlocks follow the CGs the player has seen, so
#   story files need no unlock lines. This file defines the helpers (init -3) and, once every Day
#   has registered, puts the tabs in Day order and each Day's rows after the previous Day's
#   (init -1). Never rename a shipped entry id or an image name. Rules in systems/gallery.rpy;
#   guide: docs/DAY_PACK.md.
#
# Public API (call these from scenes/screens):
#   gallery_tab(tab_id, label, chapter, day, accent) -> None
#       register a Day's tab: (tab id, label, chapter, day number), tile tint
#   gallery_row(entry_id, tab, title, description, pages, mature=False, dream=False, route="All routes") -> None
#       build one entry (id, tab, title, description, pages, mature/dream/route)
#   GALLERY_TABS                              (tab id, label, chapter, day) rows in Day order
#   GALLERY_TABLE                             the gallery_row(...) entries in Day order
#   GALLERY_TAB_ACCENTS                       {tab id: card/preview tint}
#   GALLERY_PLACEHOLDER_IMAGES                CGs still shown as text placeholders (each Day pack
#       adds its own with GALLERY_PLACEHOLDER_IMAGES.update([...]))
#
# Internal (helpers for this file and its screens; do not call from scenes): _gallery_tab_rows,
#   _gallery_finish
#
# Example:
#   init -2 python:
#       gallery_tab("ch01_d2", "Day 2", "ch01", 2, accent="#70566f")
#       gallery_row("d2_morning", "ch01_d2", "Sleeping beauty", "Day Two, 11:00.",
#           [("ch01_d2_leia_sleeping", "Asleep"), ("ch01_d2_leia_waking", "Waking up")])
#
# Notes: To add an entry: add one gallery_row(...) to the Day's *_gallery.rpy (a new Day also
#   calls gallery_tab once), list text-placeholder CGs in GALLERY_PLACEHOLDER_IMAGES there (remove
#   them when final art lands), then run lint and the unit tests. A page is "image" or ("image",
#   "Page label"); mature=True masks the grid cover, dream=True marks a dream.
#
# Depends on: nothing at init (systems/gallery.rpy reads it)
# Hooks: none
# Load order: init -3 helpers; the Day packs register at init -2; init -1 orders tabs and rows by
#   Day, before systems/gallery.rpy builds the registry at init 0
# Docs: docs/DAY_PACK.md   Tests: tests/test_gallery_flags.py, tests/test_title_screen.py,
#   tests/test_hidden_pov.py

init -3 python:

    # (tab id, tab label, chapter, day). Chapter groups the counts; day is the sub-tab.
    GALLERY_TABS = ()
    GALLERY_TAB_ACCENTS = {}
    _gallery_tab_rows = []

    # Images that are still Composite text placeholders (final art pending).
    GALLERY_PLACEHOLDER_IMAGES = set()  # each Day pack adds its own (*_gallery.rpy)

    GALLERY_TABLE = []

    def gallery_tab(tab_id, label, chapter, day, accent):
        _gallery_tab_rows.append((tab_id, label, chapter, day, accent))

    def gallery_row(entry_id, tab, title, description, pages, mature=False, dream=False, route="All routes"):
        GALLERY_TABLE.append(dict(
            id=entry_id, tab=tab, title=title, description=description,
            pages=pages, mature=mature, dream=dream, route=route,
        ))


# load order: init -1: every Day pack has registered (init -2); systems/gallery.rpy builds at init 0.
init -1 python:

    def _gallery_finish():
        """Tabs in Day order (accents in the same order); each Day's rows after the previous
        Day's, in the order the Day registered them."""
        global GALLERY_TABS
        rows = sorted(_gallery_tab_rows, key=lambda row: row[3])
        GALLERY_TABS = tuple(row[:4] for row in rows)
        GALLERY_TAB_ACCENTS.clear()
        for row in rows:
            GALLERY_TAB_ACCENTS[row[0]] = row[4]
        position = dict((row[0], i) for i, row in enumerate(rows))
        GALLERY_TABLE.sort(key=lambda entry: position.get(entry["tab"], len(rows)))

    _gallery_finish()
