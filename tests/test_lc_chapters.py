"""Chapter registry (one chapter per day): completeness, wiring, route mapping.

Run: PYTHONPATH=game/python-packages python -m unittest discover -s tests
"""
import ast
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
sys.path.insert(0, str(GAME / "python-packages"))
import lc_chapters  # noqa: E402


def review_routes_keys():
    src = (GAME / "systems" / "day_review.rpy").read_text(encoding="utf-8")
    block = src.split("LC_REVIEW_ROUTES = {", 1)[1].split("\n    }\n", 1)[0]
    return set(re.findall(r'^\s*"([a-z_]+)":', block, re.M))


def review_days():
    src = (GAME / "systems" / "day_review.rpy").read_text(encoding="utf-8")
    block = src.split("LC_REVIEW_DAYS = {", 1)[1].split("\n    }\n", 1)[0]
    return dict(re.findall(r'"(ch01_d\d+)": \{[^}]*"chapter": "([a-z0-9]+)"', block))


class ChapterRegistryTests(unittest.TestCase):

    def test_registry_is_complete(self):
        self.assertEqual(lc_chapters.CHAPTER_ORDER, ("prologue", "day1", "day2", "day3", "day4", "day5"))
        self.assertEqual(set(lc_chapters.CHAPTER_ORDER), set(lc_chapters.CHAPTERS))
        for n, cid in enumerate(lc_chapters.CHAPTER_ORDER):
            c = lc_chapters.CHAPTERS[cid]
            self.assertEqual(c["number"], n, cid)
            self.assertTrue(c["title"].strip(), cid)
            self.assertEqual(set(c["routes"]), set(lc_chapters.FAMILIES), cid)
            if cid == "prologue":
                self.assertIsNone(c["day"])
                continue
            # Chapter N is Day N.
            self.assertEqual(c["day"], n, cid)
            self.assertEqual(c["day_word"], c["number_word"], cid)
            self.assertTrue(c["number_word"], cid)
            self.assertEqual(c["review_day"], "ch01_d%d" % n, cid)
            for fam in lc_chapters.FAMILIES:
                self.assertTrue((c["routes"][fam] or "").strip(), (cid, fam))

    def test_display_title_function(self):
        self.assertEqual(lc_chapters.chapter_title("day2"), lc_chapters.CHAPTERS["day2"]["title"])
        self.assertEqual(lc_chapters.chapter_title("day2", None), lc_chapters.CHAPTERS["day2"]["title"])
        self.assertEqual(lc_chapters.chapter_title("day2", "ntr"), lc_chapters.CHAPTERS["day2"]["routes"]["ntr"])
        self.assertEqual(lc_chapters.chapter_title("prologue", "love"), lc_chapters.CHAPTERS["prologue"]["title"])
        self.assertEqual(lc_chapters.chapter_title_for_route("day3", "mixed"), lc_chapters.CHAPTERS["day3"]["title"])
        self.assertEqual(lc_chapters.chapter_heading("day3"), "Chapter Three")
        self.assertEqual(lc_chapters.review_label("day3"), "Chapter Three \u00b7 Day Three")
        self.assertEqual(lc_chapters.save_name("day3"), "Chapter 3 \u00b7 Day Three")
        self.assertEqual(lc_chapters.save_name("prologue"), "Prologue")
        self.assertIn("CHAPTER FOUR", lc_chapters.card_text("day4"))
        self.assertNotIn("[", lc_chapters.card_text("day4"))

    def test_route_mapping_covers_every_review_route(self):
        keys = review_routes_keys()
        self.assertGreaterEqual(len(keys), 12)
        missing = keys - set(lc_chapters.ROUTE_FAMILY)
        self.assertFalse(missing, "map these LC_REVIEW_ROUTES keys in lc_chapters.ROUTE_FAMILY: %s" % sorted(missing))
        for key, fam in lc_chapters.ROUTE_FAMILY.items():
            self.assertIn(fam, lc_chapters.FAMILIES + (None,), key)
        for key in ("mixed", "mixed_unresolved"):
            self.assertIsNone(lc_chapters.route_family(key))
        self.assertIsNone(lc_chapters.route_family("unknown_future_key"))
        self.assertTrue(set(lc_chapters.UNSURE_ROUTE_KEYS) <= set(lc_chapters.ROUTE_FAMILY))

    def test_review_days_point_at_registry(self):
        days = review_days()
        self.assertEqual(days, {"ch01_d%d" % n: "day%d" % n for n in range(1, 6)})
        for day_id, cid in days.items():
            self.assertEqual(lc_chapters.chapter_for_review_day(day_id), cid)

    def test_every_chapter_card_is_wired(self):
        text = "\n".join(p.read_text(encoding="utf-8") for p in (GAME / "chapters").rglob("*.rpy"))
        for n in range(1, 6):
            self.assertEqual(text.count('centered "[lc_chapter_card_day%d]"' % n), 1, n)
        self.assertIn('centered "[lc_chapter_complete_card_day4]', text)
        # Every card variable used is defined in the bridge, as a plain name
        # (config.interpolate_exprs evaluates [x[y]] as Python, so no indexing).
        rpy = (GAME / "systems" / "lc_chapters.rpy").read_text(encoding="utf-8")
        used = set(re.findall(r"\[(lc_chapter_(?:complete_)?card[^\]]*)\]", text))
        self.assertTrue(used)
        for name in used:
            self.assertRegex(name, r"^lc_chapter_(complete_)?card_[a-z0-9]+$")
            self.assertIn("define %s = " % name, rpy)

    def test_no_hardcoded_chapter_one_in_player_strings(self):
        """'CHAPTER ONE' / 'Chapter One \u00b7' may only appear in the registry, not in
        quoted strings anywhere in game/ (comments are fine)."""
        bad = []
        pattern = re.compile(r"CHAPTER ONE|Chapter One \u00b7")
        for p in GAME.rglob("*.rpy"):
            if "tl" in p.relative_to(GAME).parts:
                continue
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                code = line.split("#", 1)[0] if not line.lstrip().startswith("#") else ""
                for s in re.findall(r'"((?:[^"\\]|\\.)*)"', code):
                    if pattern.search(s):
                        bad.append("%s:%d" % (p.relative_to(ROOT), i))
        self.assertEqual(bad, [])

    def test_registry_bridge_and_save_names(self):
        rpy = (GAME / "systems" / "lc_chapters.rpy").read_text(encoding="utf-8")
        self.assertIn("import lc_chapters", rpy)
        for cid in lc_chapters.CHAPTER_ORDER[1:]:
            self.assertIn('define lc_chapter_card_%s = lc_chapters.card_text("%s")' % (cid, cid), rpy)
        self.assertIn("config.start_callbacks", rpy)
        review = (GAME / "systems" / "day_review.rpy").read_text(encoding="utf-8")
        self.assertIn("store.save_name = lc_chapters.save_name(chapter_id)", review)
        select = (GAME / "systems" / "chapter_select.rpy").read_text(encoding="utf-8")
        for n in range(2, 6):
            self.assertIn('lc_chapters.select_label("day%d")' % n, select)

    def test_review_reveals_route_title_only_for_decided_routes(self):
        sys.path.insert(0, str(ROOT / "tests"))
        import test_day_review
        harness = test_day_review.DayReviewTests("test_baseline_is_copy_and_reentry_does_not_reset")
        harness.setUp()
        env, store = harness.env, harness.store
        env["lc_review_begin"]("ch01_d2")
        self.assertEqual(store.save_name, "Chapter 2 \u00b7 Day Two")
        # Before the day ends: neutral.
        self.assertEqual(env["lc_review_night_copy"]("ch01_d2")["title"],
                         lc_chapters.CHAPTERS["day2"]["title"].upper())
        harness.values["ch01_d2_end_route"] = "ntr_confirmed"
        env["lc_review_finish"]("ch01_d2")
        night = env["lc_review_night_copy"]("ch01_d2")
        self.assertEqual(night["title"], lc_chapters.CHAPTERS["day2"]["routes"]["ntr"].upper())
        self.assertEqual(night["chapter"], "CHAPTER TWO")
        # Mixed / unresolved endings keep the neutral title.
        env["lc_review_begin"]("ch01_d4")
        harness.values["ch01_d4_end_route"] = "ntr_unresolved"
        env["lc_review_finish"]("ch01_d4")
        self.assertEqual(env["lc_review_night_copy"]("ch01_d4")["title"],
                         lc_chapters.CHAPTERS["day4"]["title"].upper())

    def test_registry_module_is_pure_python(self):
        tree = ast.parse((GAME / "python-packages" / "lc_chapters.py").read_text(encoding="utf-8"))
        imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
        self.assertEqual(imports, [])


if __name__ == "__main__":
    unittest.main()
