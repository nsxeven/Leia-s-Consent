"""Run the production stat-model init code (systems/stats.rpy, Day 2 lane resolver)
with Ren'Py stubbed: save migration on load, the shared resolvers and Current lean."""
import sys
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
sys.path.insert(0, str(GAME / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lc_effective_effects import effective_effects  # noqa: E402

EFFECTS = effective_effects()


def _block(rel, header, end=None):
    src = (GAME / rel).read_text(encoding="utf-8")
    body = src.split(header, 1)[1]
    if end:
        body = body.split(end, 1)[0]
    return textwrap.dedent(body)


class StatRuntimeTests(unittest.TestCase):

    def setUp(self):
        self.flags = {}
        self.values = {}
        self.focus = None
        self.store = SimpleNamespace(
            relationship_stats={"love": 61, "trust": 57, "boredom": 22, "momentum": 6},
            partner_stats={"curiosity": 33, "temptation": 16, "exhibitionism": 38, "boundary_looseness": 14, "secrecy": 9},
            player_stats={"jealousy": 25, "acceptance": 24},
            choice_history=[],
            lc_review_days={"ch01_d2": {
                "start": {"relationship": {"love": 50, "trust": 50, "boredom": 10, "momentum": 0},
                          "partner": {"curiosity": 20, "temptation": 10, "exhibitionism": 10, "boundary_looseness": 10, "secrecy": 5},
                          "player": {"jealousy": 20, "acceptance": 10}},
                "end": None, "moments": [],
                "choices": [{"id": "ch01_d2_morning_tease", "deltas": [("relationship", "love", 1), ("partner", "exhibitionism", 1), ("player", "acceptance", 1)]}],
            }},
            modified_save=False,
        )
        self.config = SimpleNamespace(after_load_callbacks=[])
        env = dict(
            renpy=SimpleNamespace(store=self.store, notify=lambda *a: None, restart_interaction=lambda: None),
            config=self.config,
            CHOICE_EFFECTS=dict(EFFECTS), CHOICE_TAGS={},
            has_story_flag=lambda f: bool(self.flags.get(f)),
            get_story_value=lambda k, d=None: self.values.get(k, d),
            set_story_value=lambda k, v: self.values.__setitem__(k, v),
            choice_ids_with_prefix=lambda p, ids=None: [c for c in (self.store.choice_history if ids is None else ids) if c.startswith(p)],
            chapter_nonchalant_count=lambda chapter: 0,
            choice_tag_count=lambda tag, ids=None: 0,
            lc_route_explorer_for_lane=lambda: self.focus,
        )
        env["get_choice_effects"] = lambda cid: list(env["CHOICE_EFFECTS"][cid])
        # systems/leia_side.rpy: no Leia-side choices here, so applied = registered effects
        env["lc_leia_is_side_choice"] = lambda cid: False
        env["lc_choice_applied_effects"] = env["get_choice_effects"]
        exec(compile(_block("systems/stats.rpy", "init python:\n"), "stats_init", "exec"), env)
        from lc_rpy_harness import load_blocks
        load_blocks([], env, packs=("day1",))  # Day One route helpers (its Day pack)
        day2 = _block("chapters/ch01/day2/ch01_day2_registrations.rpy",
                      "# Scenes 1-15 (was ch01_day2_scenes_01_15.rpy): choice rows, lane helpers, the gate formatter.\ninit 1 python:\n",
                      "\n# Scenes 16-30")
        exec(compile(day2, "day2_init", "exec"), env)
        # Full "Current lean" readers and the Day Two save migration live in the Day packs (hooks).
        from lc_rpy_harness import load
        load(["_lc_hooks", "lc_hook_add", "lc_hook_run", "lc_hook_filter",
              "ch01_d1_current_lean", "ch01_d2_current_lean", "ch01_d2_keep_legacy_lane",
              "ch01_d3_current_lean", "ch01_d4_current_lean", "ch01_d5_current_lean"], env)
        self.env = env

    def test_migration_runs_on_load_once(self):
        self.assertIn(self.env["lc_migrate_stats_v2"], self.config.after_load_callbacks)
        self.env["lc_migrate_stats_v2"]()
        self.assertEqual(self.store.relationship_stats, {"love": 61, "trust": 57, "sharing": 0, "temptation": 36})
        self.assertEqual(self.store.partner_stats, {"exhibitionism": 52})
        self.assertEqual(self.store.player_stats, {})
        self.assertEqual(self.store.lc_legacy_stats["relationship"]["boredom"], 22)
        self.assertEqual(self.store.lc_stat_model_version, 2)
        day = self.store.lc_review_days["ch01_d2"]
        self.assertEqual(day["start"]["relationship"]["temptation"], 10)
        self.assertEqual(day["choices"][0]["deltas"], [("relationship", "love", 1), ("partner", "exhibitionism", 2)])
        self.env["lc_migrate_stats_v2"]()  # second load: nothing changes
        self.assertEqual(self.store.partner_stats, {"exhibitionism": 52})

    def test_mid_day2_save_keeps_its_old_lane(self):
        self.flags["ch01_day_02_started"] = True
        self.values["ch01_day1_route_pressure"] = "nts_seeded"
        self.store.player_stats["acceptance"] = 16
        self.store.partner_stats.update(exhibitionism=25, curiosity=26)
        self.env["lc_migrate_stats_v2"]()
        self.assertEqual(self.values["ch01_d2_lane_migrated"], "love")  # no Day 2 'open' tag yet
        self.assertEqual(self.env["ch01_d2_route_lane"](), "love")
        self.flags["ch01_day_02_complete"] = True
        self.assertEqual(self.values["ch01_d2_lane_migrated"], "love")

    def test_new_save_gets_missing_keys_and_resolvers_agree_with_lean(self):
        self.store.relationship_stats = {"love": 60, "trust": 60, "temptation": 10}
        self.store.partner_stats = {"exhibitionism": 10}
        self.store.player_stats = {}
        self.env["lc_migrate_stats_v2"]()
        self.assertEqual(self.store.relationship_stats["sharing"], 0)
        self.flags["ch01_started"] = True
        self.assertEqual(self.env["lc_d1_route_pressure"](), "mixed")
        self.assertEqual(self.env["lc_current_lean"](), "love")
        self.store.relationship_stats["temptation"] = 20
        self.assertEqual(self.env["lc_d1_route_pressure"](), "ntr_seeded")
        self.assertEqual(self.env["lc_current_lean"](), "ntr")
        self.values["ch01_day1_route_pressure"] = "ntr_seeded"
        self.flags["ch01_day_02_started"] = True
        self.assertEqual(self.env["ch01_d2_route_lane"](), "ntr_risk")
        self.assertEqual(self.env["lc_current_lean"](), "ntr")
        self.store.relationship_stats["temptation"] = 10
        self.store.partner_stats["exhibitionism"] = 40
        self.store.choice_history = ["ch01_d2_morning_tease"]
        self.assertEqual(self.env["ch01_d2_route_lane"](), "exhibitionism")
        self.assertEqual(self.env["lc_current_lean_label"](), "Love+Exhib")
        self.flags["ch01_day_02_complete"] = True
        self.flags["ch01_day_03_started"] = True
        self.values["ch01_d2_end_route"] = "mixed_unresolved"
        self.values["ch01_d3_lane"] = "love"
        self.values["ch01_d3_strained_love"] = True
        self.assertEqual(self.env["lc_current_lean_label"](), "Love (strained)")
        self.focus = "ntr_risk"
        self.flags.pop("ch01_day_02_complete")
        self.flags.pop("ch01_day_03_started")
        self.assertEqual(self.env["ch01_d2_route_lane"](), "ntr_risk")


    def test_door_a_watch_does_not_change_todays_lane(self):
        # Review C1 (2026-11-17): Door A sits after the scene 15 lane record; its Exhibitionism
        # must not flip a Love afternoon into the Exhibitionism sunset recap.
        import lc_stat_model
        self.store.relationship_stats = {"love": 55, "trust": 55, "sharing": 0, "temptation": 12}
        self.store.partner_stats = {"exhibitionism": 36}
        self.store.player_stats = {}
        self.flags["ch01_day_02_started"] = True
        self.values["ch01_day1_route_pressure"] = "mixed"
        self.store.choice_history = ["ch01_d2_knot_watch"]
        flat = {"love": 55, "trust": 55, "sharing": 0, "temptation": 12, "exhibitionism": 36}
        self.assertEqual(lc_stat_model.d2_route_lane(flat, "mixed", 1), "exhibitionism")  # without the exemption
        self.assertEqual(self.env["ch01_d2_route_lane"](), "love")

if __name__ == "__main__":
    unittest.main()
