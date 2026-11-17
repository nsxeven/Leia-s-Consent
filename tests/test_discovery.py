"""Discovery registry, the save-local Hidden POV seen record and the Moments strip.

Pure rules: game/python-packages/lc_discovery.py. Ren'Py side: game/systems/discovery.rpy
(registry, save-local found set, persistent days cleared via the review_finished hook) and
game/systems/hidden_pov.rpy (lc_pov_open marks the moment found). The strip is drawn by
game/screens/day_review_screen.rpy.
"""
import pickle
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_discovery  # noqa: E402
from lc_rpy_harness import load, load_blocks  # noqa: E402


def _registry(*rows):
    reg = {}
    for row in rows:
        lc_discovery.register(reg, *row)
    return reg


class RegisterTests(unittest.TestCase):
    def test_entries_keep_registration_order_per_day(self):
        reg = _registry(("ch01_d2", "b", "notice", "Terrace", "someone watching"),
                        ("ch01_d2", "a", "pov", "Julian, breakfast", "noticed"),
                        ("ch01_d1", "c", "door", "Pool", "a choice"))
        self.assertEqual([e["id"] for e in reg["ch01_d2"]], ["b", "a"])
        self.assertEqual([e["id"] for e in reg["ch01_d1"]], ["c"])

    def test_duplicate_id_is_rejected_even_on_another_day(self):
        reg = _registry(("ch01_d2", "a", "pov", "Breakfast", "noticed"))
        with self.assertRaises(ValueError):
            lc_discovery.register(reg, "ch01_d2", "a", "pov", "Again", "noticed")
        with self.assertRaises(ValueError):
            lc_discovery.register(reg, "ch01_d3", "a", "notice", "Elsewhere", "")

    def test_unknown_kind_and_empty_ids_or_label_are_rejected(self):
        reg = {}
        for row in (("ch01_d2", "a", "magnifier", "Label", "mood"),
                    ("", "a", "pov", "Label", "mood"),
                    ("ch01_d2", "", "pov", "Label", "mood"),
                    ("ch01_d2", "a", "pov", "", "mood"),
                    ("ch01_d2", "a", "pov", "Label", None)):
            with self.assertRaises(ValueError, msg=repr(row)):
                lc_discovery.register(reg, *row)
        self.assertEqual(reg, {})

    def test_every_documented_kind_registers(self):
        reg = {}
        for i, kind in enumerate(lc_discovery.KINDS):
            lc_discovery.register(reg, "ch01_d2", "m%d" % i, kind, "Label", "mood")
        self.assertEqual(lc_discovery.KINDS, ("pov", "notice", "door", "phone"))
        self.assertEqual(len(reg["ch01_d2"]), 4)

    def test_find_returns_the_entry_or_none(self):
        reg = _registry(("ch01_d2", "a", "pov", "Breakfast", "noticed"))
        self.assertEqual(lc_discovery.find(reg, "a")["kind"], "pov")
        self.assertIsNone(lc_discovery.find(reg, "zzz"))


class StripTests(unittest.TestCase):
    def setUp(self):
        self.reg = _registry(
            ("ch01_d2", "pov1", "pov", "Julian, breakfast", "noticed", "cg x_pov"),
            ("ch01_d2", "n1", "notice", "Terrace", "someone watching"),
            ("ch01_d2", "d1", "door", "Pool", "the knot"),
        )

    def ids(self, items):
        return [(i["id"], i["found"]) for i in items]

    def test_unfound_hidden_until_the_day_is_cleared(self):
        items = lc_discovery.strip(self.reg, "ch01_d2", {"n1"}, False, "full")
        self.assertEqual(self.ids(items), [("n1", True)])

    def test_cleared_day_shows_unfound_in_registration_order(self):
        items = lc_discovery.strip(self.reg, "ch01_d2", {"n1"}, True, "insight")
        self.assertEqual(self.ids(items), [("pov1", False), ("n1", True), ("d1", False)])
        self.assertEqual(set(items[0]), {"id", "kind", "label", "mood", "found", "image"})
        self.assertEqual((items[0]["label"], items[0]["mood"], items[0]["image"]),
                         ("Julian, breakfast", "noticed", "cg x_pov"))

    def test_day_without_registrations_or_old_save_found_set(self):
        self.assertEqual(lc_discovery.strip(self.reg, "ch01_d1", {"pov1"}, True, "full"), [])
        self.assertEqual(lc_discovery.strip(self.reg, "ch01_d2", None, False, "normal"), [])

    def test_immersive_drops_route_words(self):
        reg = _registry(("ch01_d3", "a", "door", "NTR door", "Love or not"),
                        ("ch01_d3", "b", "notice", "Terrace", "sharing a look"),
                        ("ch01_d3", "c", "phone", "Late text", "unread"))
        normal = lc_discovery.strip(reg, "ch01_d3", {"a", "b", "c"}, True, "normal")
        self.assertEqual([(i["label"], i["mood"]) for i in normal],
                         [(lc_discovery.KIND_LABELS["door"], ""), ("Terrace", ""), ("Late text", "unread")])
        for item in normal:
            self.assertFalse(lc_discovery.has_route_words(item["label"] + " " + item["mood"]))
        full = lc_discovery.strip(reg, "ch01_d3", {"a", "b", "c"}, True, "full")
        self.assertEqual(full[0]["label"], "NTR door")

    def test_route_word_matching_is_whole_word(self):
        for text in ("ntr", "Love", "exhibitionism", "NTS lane", "temptation", "the route"):
            self.assertTrue(lc_discovery.has_route_words(text), text)
        for text in ("Julian, breakfast", "glove", "plane", "noticed", ""):
            self.assertFalse(lc_discovery.has_route_words(text), text)


class CountLineTests(unittest.TestCase):
    def setUp(self):
        reg = _registry(*[("ch01_d2", "m%d" % i, "notice", "L", "m") for i in range(5)])
        self.items = lc_discovery.strip(reg, "ch01_d2", {"m0", "m2", "m4"}, True, "full")

    def test_insight_and_full_show_n_of_m(self):
        self.assertEqual(lc_discovery.count_line(self.items, "insight"), "3 of 5")
        self.assertEqual(lc_discovery.count_line(self.items, "full"), "3 of 5")
        self.assertEqual(lc_discovery.count_line(self.items, "developer"), "3 of 5")

    def test_immersive_and_empty_have_no_count(self):
        self.assertIsNone(lc_discovery.count_line(self.items, "normal"))
        self.assertIsNone(lc_discovery.count_line([], "full"))


class ClearedBeforeTests(unittest.TestCase):
    """Rule: a day counts as cleared before a review unless this playthrough cleared it first."""

    def test_not_cleared_on_the_profile(self):
        self.assertFalse(lc_discovery.cleared_before("ch01_d2", set(), {}, "runA"))
        self.assertFalse(lc_discovery.cleared_before("ch01_d2", None, None, None))

    def test_the_playthrough_that_first_cleared_it_still_reads_first_clear(self):
        self.assertFalse(lc_discovery.cleared_before("ch01_d2", {"ch01_d2"}, {"ch01_d2": "runA"}, "runA"))

    def test_another_playthrough_or_unknown_first_run_reads_cleared(self):
        self.assertTrue(lc_discovery.cleared_before("ch01_d2", {"ch01_d2"}, {"ch01_d2": "runA"}, "runB"))
        # Cleared before first-run ids existed (or migrated from older evidence).
        self.assertTrue(lc_discovery.cleared_before("ch01_d2", {"ch01_d2"}, {}, "runA"))
        self.assertTrue(lc_discovery.cleared_before("ch01_d2", {"ch01_d2"}, {"ch01_d2": "runA"}, None))


class StripLayoutTests(unittest.TestCase):
    """The Moments strip is ONE fixed-height row at any count (review I1)."""

    def test_height_never_grows_with_the_count(self):
        heights = {lc_discovery.strip_layout(n, 714)["height"] for n in range(1, 16)}
        self.assertEqual(heights, {lc_discovery.STRIP_HEIGHT})
        self.assertEqual(lc_discovery.STRIP_HEIGHT, 24 + 4 + lc_discovery.STRIP_TILE_H)

    def test_overflow_only_past_five_tiles_on_the_review_page(self):
        for n in range(1, 6):
            self.assertFalse(lc_discovery.strip_layout(n, 714)["overflow"], n)
        for n in (6, 7, 12):
            layout = lc_discovery.strip_layout(n, 714)
            self.assertTrue(layout["overflow"], n)
            self.assertEqual(layout["content_w"], n * 136 + (n - 1) * 8)


class DiscoveryRuntimeTests(unittest.TestCase):
    """The production init block of game/systems/discovery.rpy with engine boundaries stubbed."""

    def setUp(self):
        self.persistent = SimpleNamespace(lc_days_cleared=set())
        self.store = SimpleNamespace(lc_discoveries_found=set(), lc_discovery_review_cleared={},
                                     lc_discovery_run_id="runA",
                                     LC_POV_OPPORTUNITIES={"p_unreg": {}})
        self.config = SimpleNamespace(developer=False)
        self.env = dict(store=self.store, persistent=self.persistent,
                        renpy=SimpleNamespace(store=self.store), config=self.config,
                        current_choice_mode=lambda: "full")
        load_blocks(["lc_discovery_register"], self.env)
        self.call("lc_discovery_register", "ch01_d2", "p1", "pov", "Julian, breakfast", "noticed",
                  image="cg x_pov")
        self.call("lc_discovery_register", "ch01_d2", "n1", "notice", "Terrace", "someone watching")

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def test_mark_is_idempotent_and_save_local(self):
        self.call("lc_discovery_mark", "p1")
        first = self.store.lc_discoveries_found
        self.call("lc_discovery_mark", "p1")
        self.assertIs(self.store.lc_discoveries_found, first)
        self.assertTrue(self.call("lc_discovery_found", "p1"))
        self.assertFalse(self.call("lc_discovery_found", "n1"))
        restored = pickle.loads(pickle.dumps(self.store.lc_discoveries_found))
        self.assertEqual(restored, {"p1"})

    def test_old_save_without_the_set_reads_as_nothing_found(self):
        del self.store.lc_discoveries_found
        del self.store.lc_discovery_review_cleared
        self.assertFalse(self.call("lc_discovery_found", "p1"))
        self.assertFalse(self.call("lc_pov_seen_in_save", "p1"))
        self.assertEqual(self.call("lc_discovery_strip", "ch01_d2"), [])
        self.call("lc_discovery_mark", "n1")
        self.assertEqual(self.store.lc_discoveries_found, {"n1"})

    def test_pov_seen_only_for_pov_moments(self):
        self.call("lc_discovery_mark", "p1")
        self.call("lc_discovery_mark", "n1")
        self.call("lc_discovery_mark", "p_unreg")
        self.assertTrue(self.call("lc_pov_seen_in_save", "p1"))
        self.assertFalse(self.call("lc_pov_seen_in_save", "n1"))
        # A Hidden POV registered without day_id is still a POV the save has seen.
        self.assertTrue(self.call("lc_pov_seen_in_save", "p_unreg"))
        self.assertFalse(self.call("lc_pov_seen_in_save", "never"))

    def test_first_finish_hides_unfound_and_later_saves_show_silhouettes(self):
        self.call("lc_discovery_mark", "n1")
        self.call("lc_hook_run", "review_finished", "ch01_d2")
        self.assertEqual(self.persistent.lc_days_cleared, {"ch01_d2"})
        self.assertEqual([i["id"] for i in self.call("lc_discovery_strip", "ch01_d2")], ["n1"])
        self.assertIsNone(self.call("lc_discovery_count_line", "ch01_d2"))
        # Re-entering the review on the same save (load, rollback) keeps that answer.
        self.call("lc_hook_run", "review_finished", "ch01_d2")
        self.assertEqual([i["id"] for i in self.call("lc_discovery_strip", "ch01_d2")], ["n1"])
        # Another playthrough of the day on this profile: unfound items appear greyed.
        self.store.lc_discovery_review_cleared = {}
        self.store.lc_discovery_run_id = "runB"
        self.call("lc_hook_run", "review_finished", "ch01_d2")
        items = self.call("lc_discovery_strip", "ch01_d2")
        self.assertEqual([(i["id"], i["found"]) for i in items], [("p1", False), ("n1", True)])
        self.assertEqual(self.call("lc_discovery_count_line", "ch01_d2"), "1 of 2")
        self.assertIsNone(self.call("lc_discovery_count_line", "ch01_d2", "normal"))

    def test_rollback_past_the_review_then_replay_stays_a_first_clear(self):
        # Review M1: persistent is not rolled back, the save-local snapshot is.
        self.call("lc_discovery_mark", "n1")
        self.call("lc_hook_run", "review_finished", "ch01_d2")
        self.store.lc_discovery_review_cleared = {}       # rollback to before lc_review_finish
        self.assertEqual([i["id"] for i in self.call("lc_discovery_strip", "ch01_d2")], ["n1"])
        self.call("lc_hook_run", "review_finished", "ch01_d2")   # play forward again
        self.assertEqual([i["id"] for i in self.call("lc_discovery_strip", "ch01_d2")], ["n1"])
        self.assertIsNone(self.call("lc_discovery_count_line", "ch01_d2"))
        self.assertEqual(self.store.lc_discovery_review_cleared, {"ch01_d2": False})

    def test_save_without_a_run_id_still_snapshots_once(self):
        del self.store.lc_discovery_run_id
        self.call("lc_hook_run", "review_finished", "ch01_d2")
        self.assertEqual(self.store.lc_discovery_review_cleared, {"ch01_d2": False})
        self.assertEqual(self.persistent.lc_days_cleared, {"ch01_d2"})

    def test_hook_failure_never_breaks_the_review_in_release(self):
        self.persistent.lc_days_cleared = None
        self.store.lc_discovery_review_cleared = None
        self.call("lc_hook_run", "review_finished", "ch01_d2")
        self.assertEqual(self.persistent.lc_days_cleared, {"ch01_d2"})
        self.persistent.lc_days_cleared = 5    # a real bug: not iterable
        self.call("lc_hook_run", "review_finished", "ch01_d3")

    def test_hook_failure_is_loud_in_developer_mode(self):
        # Review M5: a real bug must not vanish silently in dev.
        self.config.developer = True
        self.persistent.lc_days_cleared = 5
        with self.assertRaises(TypeError):
            self.call("lc_hook_run", "review_finished", "ch01_d2")

    def test_mark_unknown_id_raises_in_developer_mode(self):
        # Review M3: a typo'd id would otherwise be stored and never shown.
        self.config.developer = True
        with self.assertRaises(Exception) as ctx:
            self.call("lc_discovery_mark", "d2_breakfast_julain")
        self.assertIn("d2_breakfast_julain", str(ctx.exception))
        self.assertEqual(self.store.lc_discoveries_found, set())
        self.call("lc_discovery_mark", "p_unreg")      # registered Hidden POV without day_id
        self.assertEqual(self.store.lc_discoveries_found, {"p_unreg"})

    def test_mark_unknown_id_does_nothing_in_release(self):
        self.call("lc_discovery_mark", "d2_breakfast_julain")
        self.assertEqual(self.store.lc_discoveries_found, set())
        self.assertFalse(self.call("lc_discovery_found", "d2_breakfast_julain"))

    def test_days_without_discoveries_draw_nothing(self):
        self.call("lc_hook_run", "review_finished", "ch01_d1")
        self.store.lc_discovery_review_cleared = {}
        self.assertEqual(self.call("lc_discovery_strip", "ch01_d1"), [])
        self.assertIsNone(self.call("lc_discovery_count_line", "ch01_d1"))

    def test_count_line_reuses_the_strip_items(self):
        self.store.lc_discovery_review_cleared = {"ch01_d2": True}
        items = self.call("lc_discovery_strip", "ch01_d2")
        self.assertEqual(self.call("lc_discovery_count_line", "ch01_d2", "full", items), "0 of 2")


class LegacyClearedTests(unittest.TestCase):
    """Review M2: a profile that finished Day Two before discoveries existed counts as cleared.
    The evidence is persistent.ch01_chapter_select_unlocked (set on the first finished Day Two,
    systems/chapter_select.rpy), read once at init so this PR's own first clear is unaffected."""

    def boot(self, **persistent):
        self.persistent = SimpleNamespace(**persistent)
        self.store = SimpleNamespace(lc_discoveries_found=set(), lc_discovery_review_cleared={},
                                     lc_discovery_run_id="runA", LC_POV_OPPORTUNITIES={})
        self.env = dict(store=self.store, persistent=self.persistent,
                        renpy=SimpleNamespace(store=self.store),
                        config=SimpleNamespace(developer=False),
                        current_choice_mode=lambda: "full")
        load_blocks(["lc_discovery_register"], self.env)
        self.env["lc_discovery_register"]("ch01_d2", "n1", "notice", "Terrace", "someone watching")

    def test_profile_that_finished_day_two_before_reads_cleared(self):
        self.boot(ch01_chapter_select_unlocked=True)
        self.assertIn("ch01_d2", self.persistent.lc_days_cleared)
        self.env["lc_hook_run"]("review_finished", "ch01_d2")
        self.assertEqual([(i["id"], i["found"]) for i in self.env["lc_discovery_strip"]("ch01_d2")],
                         [("n1", False)])
        self.assertEqual(self.env["lc_discovery_count_line"]("ch01_d2"), "0 of 1")

    def test_fresh_profile_first_clear_is_unaffected_by_the_unlock_flag(self):
        self.boot(lc_days_cleared=set())
        self.assertEqual(self.persistent.lc_days_cleared, set())
        # Day Two's finish sets the unlock flag just before its review: too late to count.
        self.persistent.ch01_chapter_select_unlocked = True
        self.env["lc_discovery_migrate_legacy"]()
        self.env["lc_hook_run"]("review_finished", "ch01_d2")
        self.assertEqual(self.env["lc_discovery_strip"]("ch01_d2"), [])
        self.assertEqual(self.persistent.lc_days_cleared, {"ch01_d2"})


class HiddenPovDiscoveryTests(unittest.TestCase):
    """lc_pov_open writes the save-local seen record; day_id registers a pov discovery."""

    def setUp(self):
        self.calls = []
        self.store = SimpleNamespace(lc_pov_active=None, lc_pov_viewed=False,
                                     lc_discoveries_found=set(), lc_discovery_review_cleared={})
        renpy = SimpleNamespace(
            store=self.store,
            stop_skipping=lambda: self.calls.append("stop_skipping"),
            mark_image_seen=lambda image: self.calls.append(("seen", image)),
            save_persistent=lambda: self.calls.append("save_persistent"),
            retain_after_load=lambda: self.calls.append("retain_after_load"),
            show_screen=lambda name, **kw: self.calls.append(("show", name, kw)),
        )
        self.env = load(["LC_POV_LEGACY_SLOT", "LC_POV_OPPORTUNITIES", "lc_pov_register", "lc_pov_open",
                         "LC_DISCOVERIES", "lc_discovery_register", "lc_discovery_mark",
                         "lc_discovery_found", "lc_pov_seen_in_save"],
                        dict(renpy=renpy, store=self.store, lc_discovery=lc_discovery,
                             persistent=SimpleNamespace(), config=SimpleNamespace(developer=True),
                             lc_pov_available=lambda: True))
        self.store.LC_POV_OPPORTUNITIES = self.env["LC_POV_OPPORTUNITIES"]

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def test_day_id_registers_a_pov_discovery(self):
        self.call("lc_pov_register", "m1", image="cg m1_pov", source="cg m1", center=(400, 300),
                  title="Julian's POV", day_id="ch01_d2", label="Julian, breakfast", mood="noticed")
        self.call("lc_pov_register", "m2", image="cg m2_pov", source="cg m2", center=(400, 300))
        entry = lc_discovery.find(self.env["LC_DISCOVERIES"], "m1")
        self.assertEqual((entry["day_id"], entry["kind"], entry["label"], entry["mood"], entry["image"]),
                         ("ch01_d2", "pov", "Julian, breakfast", "noticed", "cg m1_pov"))
        self.assertIsNone(lc_discovery.find(self.env["LC_DISCOVERIES"], "m2"))

    def test_open_marks_found_once_and_survives_a_store_round_trip(self):
        self.call("lc_pov_register", "m1", image="cg m1_pov", source="cg m1", center=(400, 300),
                  day_id="ch01_d2", label="Julian, breakfast", mood="noticed")
        self.assertFalse(self.call("lc_pov_seen_in_save", "m1"))
        # Not the active moment: nothing is recorded.
        self.call("lc_pov_open", "m1")
        self.assertFalse(self.call("lc_discovery_found", "m1"))
        self.store.lc_pov_active = "m1"
        self.call("lc_pov_open", "m1")
        self.assertTrue(self.call("lc_pov_seen_in_save", "m1"))
        self.assertIn("retain_after_load", self.calls)
        self.assertIn(("seen", "cg m1_pov"), self.calls)
        saved = pickle.loads(pickle.dumps(vars(self.store)))
        self.assertEqual(saved["lc_discoveries_found"], {"m1"})
        # Rollback restores the earlier store: the record goes with it.
        self.store.lc_discoveries_found = set()
        self.assertFalse(self.call("lc_pov_seen_in_save", "m1"))


class SourceContractTests(unittest.TestCase):
    def test_breakfast_pov_registers_as_a_day_two_discovery(self):
        visuals = (ROOT / "game/chapters/ch01/day2/ch01_day2_visuals.rpy").read_text(encoding="utf-8")
        start = visuals.index('"d2_breakfast_julian",')
        block = visuals[start:visuals.index("\n    )", start)]
        for needed in ('day_id="ch01_d2"', 'label="Julian, breakfast"', 'mood="noticed"'):
            self.assertIn(needed, block)

    def test_pov_open_marks_the_discovery_in_the_click_handler_only(self):
        source = (ROOT / "game/systems/hidden_pov.rpy").read_text(encoding="utf-8")
        self.assertEqual(source.count("lc_discovery_mark("), 1)
        start = source.index("    def lc_pov_open(")
        body = source[start:source.index("\n    def ", start + 10)]
        self.assertIn("lc_discovery_mark(moment_id)", body)

    def test_cleared_days_use_the_review_hook_not_a_wrapper(self):
        source = (ROOT / "game/systems/discovery.rpy").read_text(encoding="utf-8")
        self.assertIn('lc_hook_add("review_finished", lc_discovery_on_review_finished)', source)
        self.assertIn("default lc_discoveries_found = set()", source)
        self.assertIn("default persistent.lc_days_cleared = set()", source)
        self.assertNotIn("_orig", source)


class ReviewStripScreenTests(unittest.TestCase):
    """The strip sits in the right-page footer and draws nothing without items."""

    def setUp(self):
        text = (ROOT / "game/screens/day_review_screen.rpy").read_text(encoding="utf-8")
        start = text.index("\nscreen lc_day_review_screen(")
        self.screen = text[start:text.index("\nscreen ", start + 10)]
        self.text = text

    def test_strip_is_drawn_only_when_items_exist(self):
        self.assertIn("$ moments = lc_discovery_strip(day_id, mode)", self.screen)
        self.assertIn("$ moments_count = lc_discovery_count_line(day_id, mode, moments)", self.screen)
        self.assertIn("if moments:", self.screen)
        self.assertIn("use lc_review_moments(moments, moments_count, text_w)", self.screen)

    def strip(self):
        start = self.text.index("\nscreen lc_review_moments(")
        return self.text[start:self.text.index("\nscreen ", start + 10)]

    def test_strip_is_one_fixed_height_row(self):
        # Review I1: the footer reserves the same height at any count, so "WHAT I SAID" keeps
        # its space; extra tiles scroll sideways in a viewport instead of wrapping.
        self.assertIn('$ footer_h += lc_discovery.strip_layout(len(moments), text_w)["height"]', self.screen)
        self.assertNotIn("moments_rows", self.screen)
        strip = self.strip()
        self.assertNotIn("box_wrap", strip)
        self.assertIn('viewport id "lc_review_moments"', strip)
        self.assertIn('mousewheel ("horizontal" if overflow else False)', strip)
        self.assertIn("draggable overflow", strip)
        self.assertIn("ysize lc_discovery.STRIP_TILE_H", strip)
        # The scrollbar sits in the header row and only when the tiles overflow.
        self.assertIn('if overflow:\n                bar value XScrollValue("lc_review_moments")', strip)

    def test_strip_uses_scrapbook_look_and_custom_names(self):
        strip = self.strip()
        self.assertIn("lc_discovery_thumb(item,", strip)
        self.assertIn("gallery_customize_names(item[\"label\"])", strip)
        self.assertIn("if count:", strip)
        self.assertIn('style "lc_pixel"', strip)
        self.assertIn('style "lc_hand"', strip)


if __name__ == "__main__":
    unittest.main()
