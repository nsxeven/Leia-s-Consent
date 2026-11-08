"""Stat model v2: names, defaults, save migration, colours and the Day 3 mixed_unresolved fix."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
sys.path.insert(0, str(GAME / "python-packages"))

import lc_stat_model as m  # noqa: E402

OLD_DEFAULTS = (
    {"love": 50, "trust": 50, "boredom": 10, "momentum": 0},
    {"curiosity": 20, "temptation": 10, "exhibitionism": 10, "boundary_looseness": 10, "secrecy": 5},
    {"jealousy": 20, "acceptance": 10},
)


def read(rel):
    return (GAME / rel).read_text(encoding="utf-8")


class StatModelTests(unittest.TestCase):

    def test_five_stats_one_name_each(self):
        self.assertEqual(m.STAT_ORDER, ("love", "trust", "exhibitionism", "sharing", "temptation"))
        self.assertEqual(sorted(m.STAT_LABELS.values()), ["Exhibitionism", "Love", "Sharing", "Temptation", "Trust"])
        self.assertIn("STAT_LABELS = dict(lc_stat_model.STAT_LABELS)", read("systems/choice_engine.rpy"))
        self.assertIn("STAT_LABELS.get(stat_name", read("systems/wardrobe_logic.rpy"))

    def test_new_game_defaults_match_the_model(self):
        defaults = read("defaults.rpy")
        self.assertIn('"sharing": 0,', defaults)
        self.assertIn('"temptation": 10,', defaults)
        self.assertIn("default player_stats = {}", defaults)
        for retired in m.RETIRED_STATS:
            self.assertNotIn('"{}"'.format(retired), defaults)

    def test_retired_names_are_not_shown_anywhere(self):
        shown = ["systems/status_display.rpy", "systems/transparency_display.rpy", "systems/stat_tooltips.rpy",
                 "systems/full_transparency_route_explorer.rpy", "screens/choice_mode_screen.rpy",
                 "screens/route_explorer_screen.rpy", "screens/debug_screen.rpy"]
        words = r"\b(Boredom|Curiosity|Acceptance|Jealousy|Momentum|Secrecy|Boundary Flexibility|Boundary Looseness|Comfort Being Seen|Affection|NTS Tendency|NTR Tendency|Distance)\b"
        for rel in shown:
            code = "\n".join(l for l in read(rel).splitlines() if not l.lstrip().startswith("#"))
            self.assertIsNone(re.search(words, code), rel)

    def test_migration_formulas(self):
        rel, par, ply, legacy = m.migrate_stats(*OLD_DEFAULTS)
        self.assertEqual(rel, {"love": 50, "trust": 50, "sharing": 0, "temptation": 10})
        self.assertEqual(par, {"exhibitionism": 10})
        self.assertEqual(ply, {})
        self.assertEqual(legacy["player"]["jealousy"], 20)
        old = ({"love": 61, "trust": 57, "boredom": 22, "momentum": 6},
               {"curiosity": 33, "temptation": 16, "exhibitionism": 38, "boundary_looseness": 14, "secrecy": 9},
               {"jealousy": 25, "acceptance": 24})
        rel, par, _ply, _legacy = m.migrate_stats(*old)
        # Exhibitionism = 10 + (38-10) + ((33-20) + (24-10)) / 2 = 51.5 -> 52 (rounded half to even = 52)
        self.assertEqual(par["exhibitionism"], 52)
        # Temptation = 22 + (16-10) + (9-5) + (14-10) = 36
        self.assertEqual(rel["temptation"], 36)
        self.assertEqual((rel["love"], rel["trust"], rel["sharing"]), (61, 57, 0))
        rel, par, _p, _l = m.migrate_stats({"love": 5, "trust": 5, "boredom": 90}, {"temptation": 90, "secrecy": 90}, {})
        self.assertEqual(rel["temptation"], 100)

    def test_legacy_detection_and_snapshots(self):
        self.assertTrue(m.is_legacy_stats(*OLD_DEFAULTS))
        new = m.DEFAULTS
        self.assertFalse(m.is_legacy_stats(new["relationship"], new["partner"], new["player"]))
        snap = m.migrate_snapshot({"relationship": OLD_DEFAULTS[0], "partner": OLD_DEFAULTS[1], "player": OLD_DEFAULTS[2]})
        self.assertEqual(snap["relationship"]["temptation"], 10)
        self.assertIs(m.migrate_snapshot(None), None)
        deltas = m.migrate_deltas([("relationship", "love", 2), ("relationship", "boredom", -2), ("partner", "secrecy", -1)])
        self.assertEqual(deltas, [("relationship", "love", 2), ("relationship", "temptation", -3)])

    def test_after_load_migration_is_registered_and_keeps_routes(self):
        stats = read("systems/stats.rpy")
        self.assertIn("config.after_load_callbacks.append(lc_migrate_stats_v2)", stats)
        body = stats.split("def lc_migrate_stats_v2", 1)[1].split("\n    if lc_migrate_stats_v2", 1)[0]
        self.assertIn('set_story_value("ch01_d2_lane_migrated", lane)', body)
        for untouched in ("story_values =", "choice_history =", "ch01_d2_end_route", "story_flags ="):
            self.assertNotIn(untouched, body)
        self.assertIn('migrated_lane=migrated', read("chapters/ch01/ch01_day2_scenes_01_15.rpy"))

    def test_legacy_lane_matches_the_old_resolver(self):
        rel, par, ply = OLD_DEFAULTS
        self.assertEqual(m.legacy_d2_lane(rel, par, ply, "mixed", 0, 0, 0, 0), "love")
        self.assertEqual(m.legacy_d2_lane(dict(rel, boredom=20), par, ply, "ntr_seeded", 3, 1, 0, 0), "ntr_risk")
        self.assertEqual(m.legacy_d2_lane(rel, dict(par, exhibitionism=25, curiosity=26), dict(ply, acceptance=16),
                                          "nts_seeded", 0, 0, 1, 0), "exhibitionism")

    def test_legacy_tuples_fold_at_runtime(self):
        folded = m.fold_legacy_effects([("partner", "curiosity", 1), ("partner", "exhibitionism", 2),
                                        ("player", "acceptance", 1), ("relationship", "momentum", 1)])
        self.assertEqual(folded, [("partner", "exhibitionism", 3)])
        self.assertIn("lc_stat_model.fold_legacy_effects(CHOICE_EFFECTS[choice_id])", read("systems/choice_engine.rpy"))

    def test_delta_colours_follow_meaning(self):
        self.assertEqual(m.delta_kind("love", 1), "good")
        self.assertEqual(m.delta_kind("trust", -1), "bad")
        self.assertEqual(m.delta_kind("temptation", 2), "bad")
        self.assertEqual(m.delta_kind("temptation", -2), "good")
        self.assertEqual(m.delta_kind("exhibitionism", 3), "exhibitionism")
        self.assertEqual(m.delta_kind("exhibitionism", -1), "exhibitionism")
        self.assertEqual(m.delta_kind("sharing", 1), "sharing")
        self.assertEqual(m.stat_id_for_label("Temptation"), "temptation")

    def test_full_lean_uses_the_route_resolvers(self):
        stats = read("systems/stats.rpy")
        lean = stats.split("def lc_current_lean():", 1)[1].split("def lc_current_lean_label", 1)[0]
        self.assertIn("ch01_d2_route_lane()", lean)
        self.assertIn("lc_d1_route_pressure()", lean)
        self.assertIn("lc_d1_route_pressure()", read("chapters/ch01/ch01_scenes_14_30.rpy"))
        status = read("systems/status_display.rpy")
        self.assertIn("lc_current_lean()", status)
        self.assertNotIn("nts_score", status)
        self.assertNotIn("ntr_score", status)

    def test_day4_day5_thresholds_and_track_names_are_overridden(self):
        late = read("systems/stat_model_v2_later_days.rpy")
        self.assertIn("init 5 python:", late)
        for name in ("D4_EXHIBITION_BRIEF_REVEAL_MIN", "D5_BOLDER_SWIM_MIN", "D5_COMFORTABLE_MIN", "D5_COMFORTABLE_MIN_AFTER_BRIEF"):
            self.assertIn(name + " = LC_T[", late)
        self.assertIn('("TRACK: SHARED EXHIBITION (NTS)", "TRACK: LOVE + EXHIBITIONISM")', late)

    def test_mixed_unresolved_starts_day3_as_strained_love(self):
        day3 = read("chapters/ch01/ch01_day3_scenes.rpy")
        self.assertIn('$ d3_lane = "ntr" if d3_end == "ntr_confirmed" else', day3)
        self.assertNotIn('("ntr_confirmed", "mixed_unresolved")', day3)
        self.assertIn('set_story_value("ch01_d3_strained_love", d3_strained)', day3)
        club = day3.split("label ch01_day3_club:", 1)[1].split("label ch01_day3_hairclip:", 1)[0]
        self.assertIn('get_story_value("ch01_d3_strained_love", False)', club)
        self.assertIn('set_story_value("ch01_d3_lane", "ntr")', club)
        # flags others read are still written
        for kept in ('set_story_value("ch01_d3_lane", d3_lane)', 'set_story_value("ch01_d3_ntr_repair_effort", "none")'):
            self.assertIn(kept, day3)
        self.assertNotIn('set_story_value("ch01_d2_end_route"', day3)


if __name__ == "__main__":
    unittest.main()
