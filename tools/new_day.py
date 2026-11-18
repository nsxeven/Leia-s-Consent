"""Scaffold a new Day pack (docs/DAY_PACK.md).

    python tools/new_day.py 6              dry run: lists the files it would create
    python tools/new_day.py 6 --write      creates them

Creates, for Day N of Chapter One:
    game/chapters/ch01/dayN/ch01_dayN_scenes.rpy         start label stub (reads Day N-1's end route,
                                                          stores Day N's, runs the review)
    game/chapters/ch01/dayN/ch01_dayN_visuals.rpy        backgrounds / CG image stubs
    game/chapters/ch01/dayN/ch01_dayN_registrations.rpy  choice effects + tags, story-key ledger
    game/chapters/ch01/dayN/ch01_dayN_gallery.rpy        Gallery tab (rows go here)
    game/chapters/ch01/dayN/ch01_dayN_chapter.rpy        title card + end-of-day review row
    game/python-packages/lc_days/dayN.py                 chapter registry entry (titles)
    tests/test_ch01_dayN.py                              test stub
It never overwrites a file. Afterwards (printed at the end): add "dayN" to DAY_MODULES in
game/python-packages/lc_days/__init__.py and to CHAPTER_ORDER in lc_chapters.py, add the Day to
DAY_PACKS in tests/test_day_packs.py, and make Day N-1 jump to ch01_dayN_start.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS = ("Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
         "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen")
ACCENT = "#6b6478"


def word(n):
    return WORDS[n] if n < len(WORDS) else str(n)


def files_for(n, reads=None, writes=None):
    """{repo-relative path: text} of a Day N pack."""
    d, w = "day%d" % n, word(n)
    tag, prefix = "ch01_d%d" % n, "ch01_day%d" % n
    reads = reads or "ch01_d%d_end_route" % (n - 1)
    writes = writes or "%s_end_route" % tag
    folder = "game/chapters/ch01/%s/" % d
    out = {}
    out[folder + prefix + "_scenes.rpy"] = f'''# Leia's Consent - Chapter One, Day {w}.
# Entry: {prefix}_start (Day {word(n - 1)} jumps here). Reads Day {word(n - 1)}'s end route ({reads}).
# Exit: stores {writes}, runs the end-of-day review.
# Guide: docs/DAY_PACK.md.

label {prefix}_start:
    $ lc_review_begin("{tag}")
    $ set_story_flag("ch01_day_{n:02d}_started")
    scene black
    with fade
    centered "[lc_chapter_card_{d}]"

    $ {tag}_start_route = get_story_value("{reads}", "love")

    # Scenes go here: label {prefix}_scene_01_<name>: ... one label per scene.

    jump {prefix}_finish


label {prefix}_finish:
    $ set_story_value("{writes}", {tag}_start_route)
    $ set_story_flag("ch01_day_{n:02d}_complete")
    call lc_day_review("{tag}")
    return
'''
    out[folder + prefix + "_visuals.rpy"] = f'''# Day {w} pack - visuals: this Day's backgrounds and CG images.
#
# Backgrounds: game/images/backgrounds/chapter 1/ch01_<place>.webp, declared here as
#   image bg {tag}_<place> = "images/backgrounds/chapter 1/ch01_<place>.webp"
# CGs: game/images/cg/ch01/CH1D{n}_CG_<Moment>_NN.webp, declared here as
#   image cg {tag}_<moment>_NN = At("images/cg/ch01/CH1D{n}_CG_<Moment>_NN.webp", prologue_fullscreen)
# Show them with `scene bg ...` / `show cg ...`. Guide: docs/DAY_PACK.md.
'''
    out[folder + prefix + "_registrations.rpy"] = f'''# Day {w} pack - registrations: choice effects and tags, and the story-key ledger.
#
# Where every kind of content goes: docs/DAY_PACK.md. Scoring rules: docs/STAT_MODEL.md.
# Load order: init 1 (the engine tables exist at init <= 0).

init 1 python:

    # Stat effects per choice id: [(group, stat, amount), ...] (systems/choice_engine.rpy).
    CHOICE_EFFECTS.update({{
    }})

    # Behaviour tags per choice id (systems/choice_engine.rpy).
    CHOICE_TAGS.update({{
    }})

# ------------------------------------------------------------------ story-key ledger
# Every story flag / value this Day sets, one line each (tests/test_day_packs.py checks it):
#   # key <name>: read-by <who reads it>     or     # key <name>: pending <why nothing reads it yet>
# Patterns with * cover dynamic keys. Keys are save data: never rename one.
# key ch01_day_{n:02d}_started: pending set by {prefix}_scenes.rpy; nothing reads it yet
# key ch01_day_{n:02d}_complete: pending set by {prefix}_scenes.rpy; nothing reads it yet
# key {writes}: pending Day {word(n + 1)} reads it once it exists
'''
    out[folder + prefix + "_gallery.rpy"] = f'''# Day {w} pack - Gallery rows (the Day {n} tab).
#
# One gallery_row(...) per scene sequence; pages are the stable `cg <name>` images in display
#   order. Unlocks follow the CGs the player has seen. API and rules: systems/gallery_data.rpy;
#   guide: docs/DAY_PACK.md. Never rename a shipped entry id or an image name.
# Load order: init -2 (systems/gallery_data.rpy defines the helpers at init -3 and orders the
#   tabs and rows by Day at init -1).

init -2 python:

    gallery_tab("{tag}", "Day {n}", "ch01", {n}, accent="{ACCENT}")

    # gallery_row("{tag[5:]}_<moment>", "{tag}", "Title", "One line.",
    #     [("{tag}_<moment>_01", "Page label"), "{tag}_<moment>_02"])
'''
    out[folder + prefix + "_chapter.rpy"] = f'''# Day {w} pack - chapter: title-card text and the end-of-day review row. The chapter registry
#   entry (titles) is CHAPTER in game/python-packages/lc_days/{d}.py.
#
# Where every kind of content goes: docs/DAY_PACK.md.

# Opening title card (neutral title for everyone), shown by the Day's start label.
define lc_chapter_card_{d} = lc_chapters.card_text("{d}")

# End-of-day review: this Day's row (systems/day_review.rpy). route_key = the end-route story key.
init 1 python:
    import lc_chapters
    LC_REVIEW_DAYS["{tag}"] = {{"label": lc_chapters.review_label("{d}"), "chapter": "{d}", "route_key": "{writes}"}}
'''
    out["game/python-packages/lc_days/%s.py" % d] = f'''"""Day {w}: pure-Python Day pack data (see lc_days/__init__.py for the names).

Ren'Py side: game/chapters/ch01/{d}/. Guide: docs/DAY_PACK.md.
"""

# Chapter registry entry (lc_chapters.CHAPTERS["{d}"]).
CHAPTER = {{
    "number": {n}, "number_word": "{w}", "day": {n}, "day_word": "{w}",
    "review_day": "{tag}",
    "title": 'Day {w}',
    "routes": {{
        "love": None,
        "love_exhib": None,
        "nts": None,
        "ntr": None,
        "repair": None,
    }},
}}
'''
    out["tests/test_ch01_%s.py" % d] = f'''"""Day {w} pack: story checks. Add one test per rule the Day must keep."""
import unittest
from pathlib import Path

DAY = Path(__file__).resolve().parents[1] / "game" / "chapters" / "ch01" / "{d}"


class Day{w}Tests(unittest.TestCase):
    def test_start_label_exists(self):
        self.assertIn("label {prefix}_start:", (DAY / "{prefix}_scenes.rpy").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
'''
    return out


def next_steps(n):
    d = "day%d" % n
    return [
        'add "%s" to DAY_MODULES in game/python-packages/lc_days/__init__.py' % d,
        'add "%s" to CHAPTER_ORDER in game/python-packages/lc_chapters.py' % d,
        "add Day %d to DAY_PACKS in tests/test_day_packs.py (start label, reads, writes, review)" % n,
        "make Day %d's last scene jump to ch01_day%d_start" % (n - 1, n),
        "fill in the titles in game/python-packages/lc_days/%s.py, then run the unit tests and lint" % d,
    ]


def main(argv=None, root=ROOT, out=sys.stdout):
    ap = argparse.ArgumentParser(description="Scaffold a new Day pack (dry run unless --write).")
    ap.add_argument("day", type=int, help="day number, e.g. 6")
    ap.add_argument("--write", action="store_true", help="create the files (default: dry run)")
    ap.add_argument("--reads", help="story key with the previous Day's end route")
    ap.add_argument("--writes", help="story key this Day stores its end route in")
    args = ap.parse_args(argv)
    if args.day < 2:
        ap.error("day must be 2 or more (the Prologue and Day 1 exist)")
    root = Path(root)
    files = files_for(args.day, args.reads, args.writes)
    clash = [rel for rel in files if (root / rel).exists()]
    if clash:
        print("refusing: these already exist:\n  " + "\n  ".join(clash), file=out)
        return 1
    for rel, text in files.items():
        if args.write:
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
        print(("created " if args.write else "would create ") + rel, file=out)
    if not args.write:
        print("dry run: nothing written (add --write)", file=out)
    print("then:\n  - " + "\n  - ".join(next_steps(args.day)), file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
