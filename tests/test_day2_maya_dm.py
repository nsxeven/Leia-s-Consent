"""Day Two phone moment: Maya's late DM in scene 30 (ch01_d2_maya_dm).

Content lives in game/chapters/ch01/day2/ch01_day2_registrations.rpy (the init block) and ch01_day2_scenes_16_30.rpy (
the beat in ch01_day2_scene_30_bedroom, the end-of-day settle in ch01_day2_scene_30_finish).
The phone system itself is tested in tests/test_phone_moments.py.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_stat_model as m  # noqa: E402
from lc_effective_effects import applied_choice_ids, effective_effects  # noqa: E402
from lc_rpy_harness import load  # noqa: E402
from test_phone_moments import load_phone  # noqa: E402

SCENES = ((ROOT / "game/chapters/ch01/day2/ch01_day2_scenes_16_30.rpy").read_text(encoding="utf-8") + "\n"
          + (ROOT / "game/chapters/ch01/day2/ch01_day2_registrations.rpy").read_text(encoding="utf-8"))
IDS = ("ch01_d2_maya_dm_reply", "ch01_d2_maya_dm_read", "ch01_d2_maya_dm_show",
       "ch01_d2_maya_dm_reply_late")


def block(label):
    return SCENES.split("label %s:" % label, 1)[1].split("\nlabel ", 1)[0]


def load_dm(**kw):
    env, story, store, marked, shown = load_phone(**kw)
    flags, applied, clock = set(), [], []
    env.update({
        "has_story_flag": lambda f: f in flags,
        "set_story_flag": lambda f, value=True: flags.add(f),
        "apply_choice": applied.append,
        "lc_phone_set_story_time": clock.append,
        "lc_phone_clear_story_time": lambda: clock.append(None),
        "format_choice": lambda cid, text: text,
        "girlfriend_name": "Leia",
    })
    load(["CH01_D2_MAYA_DM_SHOW", "ch01_d2_maya_dm_mood", "ch01_d2_maya_dm_offer",
          "ch01_d2_maya_dm_end_show", "ch01_d2_maya_dm_settle", "ch01_d2_maya_dm_review_lines"], env)
    env["lc_phone_moment_register"]("ch01_d2_maya_dm", "ch01_d2", "Maya, a late text", "nosy",
                                    found_on=("reply", "show"))
    return env, story, store, marked, applied, clock


class ScoringTests(unittest.TestCase):
    def test_choices_are_registered_small_and_legal(self):
        effects = effective_effects()
        self.assertEqual(effects["ch01_d2_maya_dm_reply"], [("relationship", "trust", 1)])
        self.assertEqual(effects["ch01_d2_maya_dm_show"], [("relationship", "love", 1)])
        self.assertEqual(effects["ch01_d2_maya_dm_read"], [])
        self.assertEqual(effects["ch01_d2_maya_dm_reply_late"], [])  # nobody on screen sees it
        for cid in IDS:
            self.assertEqual(m.scoring_violations(cid, effects[cid]), [], cid)
            self.assertIn(cid, applied_choice_ids())
        self.assertEqual(m.choice_route_tag("ch01_d2_maya_dm_read", []), "Neutral")
        self.assertEqual(m.choice_route_tag("ch01_d2_maya_dm_show", effects["ch01_d2_maya_dm_show"]), "Love")

    def test_moment_is_registered_as_a_phone_moment(self):
        self.assertIn('lc_phone_moment_register("ch01_d2_maya_dm", "ch01_d2", "Maya, a late text", "nosy",\n'
                      '                             found_on=("reply", "show"))', SCENES)


class MoodTests(unittest.TestCase):
    def setUp(self):
        self.mood = load_dm()[0]["ch01_d2_maya_dm_mood"]

    def test_mood_follows_the_next_bedroom_branch(self):
        mood = self.mood
        self.assertEqual(mood("love", "shy", False, False, False, False), "love")
        self.assertEqual(mood("love", "love", True, False, False, False), "love")  # soft gate, no wink
        self.assertEqual(mood("exhibitionism", "exhibitionism", False, False, False, False), "exhib")
        self.assertEqual(mood("love", "love", False, False, False, True), "exhib")  # Love + Exhib blend
        self.assertEqual(mood("ntr_risk", "shy", True, True, False, False), "cool")  # nightmare
        self.assertEqual(mood("ntr_risk", "shy", False, False, True, False), "cool")  # pool talk
        self.assertEqual(mood("exhibitionism", "temptation", False, False, False, False), "cool")
        self.assertEqual(mood("ntr_risk", "shy", False, False, False, False), "shy")
        self.assertEqual(mood("mixed", "shy", False, False, False, False), "shy")

    def test_love_lane_is_never_cool(self):
        for soft_gate in (False, True):
            for suspicion in (False, True):
                for tint in ("shy", "love", "trust", "exhibitionism"):
                    self.assertIn(self.mood("love", tint, soft_gate, False, suspicion, False), ("love", "exhib"))


class OfferAndSettleTests(unittest.TestCase):
    def test_offer_posts_two_messages_and_a_three_option_card(self):
        env, story, store, marked, applied, clock = load_dm()
        banners = []
        env["phone_queue_notification"] = lambda *a, **kw: banners.append(a)
        env["ch01_d2_maya_dm_offer"]("love")
        msgs = store.phone_messages["maya"]
        self.assertEqual([x["id"] for x in msgs], ["ch01_d2_maya_dm_01", "ch01_d2_maya_dm_02"])
        self.assertTrue(msgs[0]["text"].startswith("you two okay in there?"))
        self.assertIn("through this wall", msgs[1]["text"])  # Julian's room is next door
        self.assertEqual(len(banners), 1)  # one banner for one DM
        self.assertEqual(clock, ["23:52"])
        card = env["phone_pending_reply"]("maya")
        self.assertEqual(card["id"], "ch01_d2_maya_dm")
        self.assertEqual(card["default"], "read")
        opts = {o["id"]: o for o in card["options"]}
        self.assertEqual(list(opts), ["reply", "read", "show"])
        self.assertTrue(opts["reply"]["hesitate"])
        self.assertTrue(opts["reply"]["draft"])
        self.assertTrue(opts["read"]["leave_on_read"])
        self.assertNotIn("followups", opts["read"])  # an unopened default must not read "seen"
        self.assertEqual(opts["reply"]["draft"], "why are you listening through the w")
        # The card says what the option does; the bubble posts what Leia types.
        self.assertEqual(opts["show"]["text"], "Show [girlfriend_name]")
        self.assertEqual(opts["show"]["send"], env["CH01_D2_MAYA_DM_SHOW"]["love"][0])
        self.assertEqual({k: o["choice_id"] for k, o in opts.items()},
                         {k: "ch01_d2_maya_dm_" + k for k in opts})

    def test_every_mood_has_leia_text_and_a_maya_answer(self):
        env = load_dm()[0]
        self.assertEqual(set(env["CH01_D2_MAYA_DM_SHOW"]), {"love", "exhib", "shy", "cool"})
        for leia, maya in env["CH01_D2_MAYA_DM_SHOW"].values():
            self.assertIn("[girlfriend_name]", leia)
            self.assertTrue(maya)
            self.assertIsNone(re.search(r"\b(Ryan|Leia|Julian)\b", leia + maya))

    def test_show_is_scored_once_and_marks_the_moment(self):
        env, story, store, marked, applied, clock = load_dm()
        env["ch01_d2_maya_dm_offer"]("shy")
        env["phone_choose_reply"]("maya", "show")
        env["ch01_d2_maya_dm_settle"]()
        env["ch01_d2_maya_dm_settle"](close=True)
        self.assertEqual(applied, ["ch01_d2_maya_dm_show"])
        self.assertEqual(marked, ["ch01_d2_maya_dm"])
        ids = [x["id"] for x in store.phone_messages["maya"]]
        self.assertEqual(ids[-2:], ["ch01_d2_maya_dm_ryan", "ch01_d2_maya_dm_followup_01"])
        self.assertEqual(store.phone_messages["maya"][-2]["text"], env["CH01_D2_MAYA_DM_SHOW"]["shy"][0])
        self.assertEqual(clock[-1], None)

    def test_ignored_card_runs_out_as_unopened_read_at_the_end_of_the_day(self):
        env, story, store, marked, applied, clock = load_dm()
        env["ch01_d2_maya_dm_offer"]("cool")
        env["ch01_d2_maya_dm_settle"]()  # scene 30 beat: nothing picked yet, nothing scored
        self.assertEqual(applied, [])
        self.assertIsNotNone(env["phone_pending_reply"]("maya"))
        env["ch01_d2_maya_dm_settle"](close=True)
        self.assertEqual(story["ch01_d2_maya_dm"], "read")
        self.assertEqual(applied, ["ch01_d2_maya_dm_read"])
        self.assertIsNone(env["phone_pending_reply"]("maya"))
        self.assertTrue(env["lc_phone_left_on_read"]("ch01_d2_maya_dm"))
        self.assertEqual(marked, [])
        self.assertEqual([x["id"] for x in store.phone_messages["maya"]],
                         ["ch01_d2_maya_dm_01", "ch01_d2_maya_dm_02"])

    def test_after_the_beat_show_is_gone_and_read_stays_the_default(self):
        env, story, store, marked, applied, clock = load_dm()
        env["ch01_d2_maya_dm_offer"]("love")
        env["ch01_d2_maya_dm_end_show"]()
        card = env["phone_pending_reply"]("maya")
        self.assertEqual([o["id"] for o in card["options"]], ["reply", "read"])
        self.assertEqual(card["default"], "read")
        # The card's stat label tells the truth about a late reply: no stats.
        self.assertEqual(card["options"][0]["choice_id"], "ch01_d2_maya_dm_reply_late")
        self.assertFalse(env["phone_choose_reply"]("maya", "show"))

    def test_a_late_reply_is_settled_neutrally(self):
        env, story, store, marked, applied, clock = load_dm()
        env["ch01_d2_maya_dm_offer"]("exhib")
        env["ch01_d2_maya_dm_end_show"]()
        env["ch01_d2_maya_dm_settle"]()
        env["phone_choose_reply"]("maya", "reply")
        env["ch01_d2_maya_dm_settle"](close=True)
        self.assertEqual(applied, ["ch01_d2_maya_dm_reply_late"])
        self.assertEqual(marked, ["ch01_d2_maya_dm"])

    def test_a_reply_during_the_beat_keeps_trust_and_end_show_is_a_no_op(self):
        env, story, store, marked, applied, clock = load_dm()
        env["ch01_d2_maya_dm_offer"]("love")
        env["phone_choose_reply"]("maya", "reply")
        env["ch01_d2_maya_dm_end_show"]()
        env["ch01_d2_maya_dm_settle"]()
        self.assertEqual(applied, ["ch01_d2_maya_dm_reply"])
        self.assertEqual(clock[-1], None)  # nothing pending: the phone goes back to its clock

    def test_an_open_card_keeps_the_late_clock_until_the_day_ends(self):
        env, story, store, marked, applied, clock = load_dm()
        env["ch01_d2_maya_dm_offer"]("cool")
        env["ch01_d2_maya_dm_end_show"]()
        env["ch01_d2_maya_dm_settle"]()
        self.assertEqual(clock, ["23:52"])

    def test_settle_on_an_old_save_does_nothing(self):
        env, story, store, marked, applied, clock = load_dm()
        env["ch01_d2_maya_dm_settle"](close=True)
        self.assertEqual(applied, [])
        self.assertNotIn("ch01_d2_maya_dm", story)

    def test_review_lines_cover_every_choice(self):
        env = load_dm()[0]
        self.assertEqual(len(env["ch01_d2_maya_dm_review_lines"]()), 4)
        for cid in IDS:
            self.assertIn('format_choice("%s", ' % cid, SCENES)


class PlacementTests(unittest.TestCase):
    def test_beat_sits_where_every_lane_passes(self):
        body = block("ch01_day2_scene_30_bedroom")
        order = ["$ d2_tint = lc_leia_tint(d2_lane, lane_scene=True)",
                 "$ ch01_d2_maya_dm_offer(d2_dm_mood)",
                 '"My phone lit up on the nightstand. Maya, from the other side of the wall."',
                 'if get_story_value("ch01_d2_maya_dm") == "show":',
                 'elif get_story_value("ch01_d2_maya_dm") == "reply":',
                 "$ ch01_d2_maya_dm_end_show()",
                 "$ ch01_d2_maya_dm_settle()",
                 "if d2_soft_gate and d2_wink:"]
        offsets = [body.index(part) for part in order]
        self.assertEqual(offsets, sorted(offsets))
        self.assertEqual(SCENES.count("ch01_d2_maya_dm_offer(d2_dm_mood)"), 1)

    def test_nothing_says_maya_is_downstairs(self):
        # Canon: Julian's room is next door on the second floor (ch01_main.rpy).
        dm = SCENES.split("def ch01_d2_maya_dm_offer", 1)[1].split("def ch01_d2_maya_dm_settle", 1)[0]
        for phrase in ("up there", "down here", "down th", "down the corridor"):
            self.assertNotIn(phrase, dm)
        self.assertNotIn("Maya, from somewhere down the corridor", SCENES)

    def test_the_love_reaction_does_not_repeat_the_echo(self):
        beat = block("ch01_day2_scene_30_bedroom").split("ch01_d2_maya_dm_offer(d2_dm_mood)", 1)[1]
        self.assertNotIn("weird parts", beat.split("$ ch01_d2_maya_dm_settle()", 1)[0])

    def test_day_end_settles_before_the_review(self):
        body = block("ch01_day2_scene_30_finish")
        self.assertLess(body.index("$ ch01_d2_maya_dm_settle(close=True)"),
                        body.index('call lc_day_review("ch01_d2")'))

    def test_new_lines_use_name_variables(self):
        beat = block("ch01_day2_scene_30_bedroom").split("ch01_d2_maya_dm_offer(d2_dm_mood)", 1)[1]
        beat = beat.split("$ ch01_d2_maya_dm_settle()", 1)[0]
        self.assertIsNone(re.search(r"\b(Ryan|Leia|Julian)\b", beat))
        self.assertIn("[girlfriend_name]", beat)


if __name__ == "__main__":
    unittest.main()
