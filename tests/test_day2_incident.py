"""Day Two incident (v0.2.0, darryn): "Overheard at the cafe" is the scored beat.

- Option 1: Ryan overhears Leia and Maya at the cafe (scene 11b). One menu:
  own it (Repair: Trust +1, Temptation -1, in REPAIR_CHOICES), joke (flavor, no
  stats), pretend (slip: Love -1, Temptation +1). Story value
  ch01_d2_overheard_response = owned / joked / pretended.
- Leia's overheard line follows Day One's upstairs talk (ch01_upstairs_response).
- The post-shop "I'm fine." menu is flavor now: lines kept, stats dropped, its
  repair tags kept (they still pick which talk Ryan overhears).
- Options 2 (the photographer) and 3 (the hushed secret) are flavor beats: no
  menu, no choices, no stats.
- Scene 1 no longer contradicts the Day One echoes E1 (liked: the talk happened),
  E2 (honest: he did carry her) and E4 (snapped: no repeat of her line).
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import lc_stat_model as m  # noqa: E402
from lc_effective_effects import effective_effects  # noqa: E402

CH = ROOT / "game" / "chapters" / "ch01"
SCENES = (CH / "ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
S19B = (CH / "ch01_day2_scene_19b_leia_asks_maya.rpy").read_text(encoding="utf-8")


def label_body(src, name):
    body = src.split("label {}:".format(name), 1)[1]
    return re.split(r"\nlabel \w+:", body, 1)[0]


def deltas(effects):
    return m.effect_deltas(effects)


class OverheardIncidentTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.eff = effective_effects()
        cls.cafe = label_body(SCENES, "ch01_day2_scene_11b_boutique")

    def test_scores_match_the_approved_proposal(self):
        self.assertEqual(deltas(self.eff["ch01_d2_overheard_own"]), {"trust": 1, "temptation": -1})
        self.assertEqual(self.eff["ch01_d2_overheard_joke"], [])
        self.assertEqual(deltas(self.eff["ch01_d2_overheard_pretend"]), {"love": -1, "temptation": 1})

    def test_path_tags(self):
        tag = lambda cid: m.choice_route_tag(cid, self.eff[cid])
        self.assertIn("ch01_d2_overheard_own", m.REPAIR_CHOICES)
        self.assertEqual(tag("ch01_d2_overheard_own"), "Repair")
        self.assertEqual(tag("ch01_d2_overheard_joke"), "Neutral")
        self.assertEqual(tag("ch01_d2_overheard_pretend"), "May lead to NTR")

    def test_choice_tags(self):
        self.assertIn('"ch01_d2_overheard_own": ("attentive", "honest", "repair")', SCENES)
        self.assertRegex(SCENES, r'"ch01_d2_overheard_pretend": \([^)]*"withdrawal"')
        self.assertNotRegex(SCENES, r'"ch01_d2_overheard_pretend": \([^)]*"repair"')

    def test_one_menu_three_options_with_story_values(self):
        start = self.cafe.index("I stopped walking.")
        end = self.cafe.index("By the time [friend_name] got back with the rest")
        block = self.cafe[start:end]
        self.assertEqual(block.count("menu:"), 1)
        for cid, value in (("own", "owned"), ("joke", "joked"), ("pretend", "pretended")):
            self.assertIn('format_choice("ch01_d2_overheard_{}"'.format(cid), block)
            self.assertIn('apply_choice("ch01_d2_overheard_{}")'.format(cid), block)
            self.assertIn('set_story_value("ch01_d2_overheard_response", "{}")'.format(value), block)

    def test_incident_comes_before_the_pre_split_snapshot(self):
        self.assertLess(SCENES.index('apply_choice("ch01_d2_overheard_own")'),
                        SCENES.index('set_story_value("ch01_d2_route_lane_pre_split"'))

    def test_leia_line_follows_day_one_upstairs(self):
        worried = self.cafe.split('set_story_value("ch01_d2_overheard_talk", "worried")', 1)[1].split("menu:", 1)[0]
        for value in ("honest", "liked", "swallowed", "snapped"):
            self.assertIn('get_story_value("ch01_upstairs_response") == "{}"'.format(value), worried)
        self.assertIn('get_story_value("ch01_dream_response") == "withdrew"', worried)
        self.assertIn("    else:\n            gf \"Not that I know of. He says he's fine.\"", worried)
        self.assertIn("Out loud.", worried)

    def test_milder_talk_when_ryan_has_been_present(self):
        mild = self.cafe.split('set_story_value("ch01_d2_overheard_talk", "mild")', 1)[1].split("else:", 1)[0]
        self.assertIn("He goes quiet, and then he comes back.", mild)
        self.assertIn("from behind a plant", mild)

    def test_pov_slip_fixed(self):
        self.assertNotIn("where [player_name] and [friend_name] were waiting", SCENES)

    def test_route_simulation_scores_the_incident_not_postshop(self):
        src = (ROOT / "tests" / "test_route_simulation.py").read_text(encoding="utf-8")
        self.assertIn('"ch01_d2_overheard_own", "ch01_d2_overheard_joke", "ch01_d2_overheard_pretend"', src)
        self.assertNotIn('["ch01_d2_postshop_sleep"', src)


class PostshopIsFlavorTests(unittest.TestCase):

    def test_postshop_has_no_stats_but_keeps_its_lines_and_repair_tags(self):
        eff = effective_effects()
        for cid in ("ch01_d2_postshop_sleep", "ch01_d2_postshop_head", "ch01_d2_postshop_shut_down"):
            self.assertEqual(eff[cid], [], cid)
            self.assertNotIn(cid, m.REPAIR_CHOICES)
            self.assertIn('apply_choice("{}")'.format(cid), SCENES)
        self.assertIn('"ch01_d2_postshop_sleep": ("supportive", "attentive", "honest", "repair")', SCENES)
        self.assertIn('"ch01_d2_postshop_head": ("attentive", "honest", "repair")', SCENES)
        self.assertIn('mc "I\'m fine."\n            "[girlfriend_name] watched me for a second."', SCENES)


class FlavorBeatsTests(unittest.TestCase):

    def test_photographer_beat_has_no_menu_and_keeps_julian_loyal(self):
        body = label_body(SCENES, "ch01_day2_scene_07_leia_maya_click")
        self.assertIn("lock screen", body)
        self.assertIn("She was mostly looking past me at [player_name]", body)
        self.assertNotIn("menu:", body)
        self.assertNotIn("apply_choice", body)

    def test_hushed_secret_has_no_menu_and_pays_off_innocently(self):
        body = label_body(SCENES, "ch01_day2_scene_15_pool_group")
        self.assertIn("Very boring sunscreen stuff.", body)
        self.assertNotIn("menu:", body)
        self.assertNotIn("apply_choice", body)
        self.assertLess(body.index("Very boring sunscreen stuff."), body.index("ch01_d2_route_lane_pre_split"))
        payoff = label_body(S19B, "ch01_day2_scene_19c_back_outside")
        self.assertIn("Getting you on your own before dinner was the secret.", payoff)
        self.assertNotIn("menu:", payoff)


class SceneOneReconcileTests(unittest.TestCase):

    def setUp(self):
        self.body = label_body(SCENES, "ch01_day2_scene_01_morning_after")

    def test_e2_honest_he_did_carry_her(self):
        self.assertNotIn("You never had to carry me", self.body)
        self.assertNotIn("you still owe me one bad carry", self.body)
        self.assertIn("carried me up those stairs", self.body)

    def test_e1_liked_builds_on_the_talk_they_had(self):
        self.assertNotIn("We still haven't had our talk", self.body)
        self.assertNotIn("Daylight doesn't cancel it", self.body)
        self.assertIn("our talk last night", self.body)

    def test_e4_snapped_does_not_repeat_her_line(self):
        self.assertNotIn("I wasn't trying to fall asleep on you", self.body)
        self.assertIn("in the dark", self.body)


if __name__ == "__main__":
    unittest.main()
