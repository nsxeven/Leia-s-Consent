"""Day Two: Leia's errand (Leia's side PR 3, LC-Brain `Plans/2026-11-17 Leia's side design.md`).

Source and harness checks for the errand content: the 19b -> errand -> 19c flow, choice scoring
and path stamps (canon calls K4/K5), her +2/day cap, the lane and end-route exemption, the feed
posts and their gated release, the scene 30 option before the bedroom gates, placeholders, and old
saves already past 19b. Route outcomes over every lane are in tests/test_route_simulation.py.
"""
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
sys.path.insert(0, str(GAME / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import lc_leia_side as L  # noqa: E402
import lc_stat_model as m  # noqa: E402
from lc_effective_effects import effective_effects  # noqa: E402
from lc_rpy_harness import load  # noqa: E402

DAY2 = GAME / "chapters" / "ch01" / "day2"
ERRAND = DAY2 / "ch01_day2_leia_errand.rpy"
SC19B = DAY2 / "ch01_day2_scene_19b_leia_asks_maya.rpy"
SC16_30 = DAY2 / "ch01_day2_scenes_16_30.rpy"
SC01_15 = DAY2 / "ch01_day2_scenes_01_15.rpy"
REG = DAY2 / "ch01_day2_registrations.rpy"  # Day Two choice rows, exempt lists, places
FEED = DAY2 / "ch01_day2_feed.rpy"
VISUALS = DAY2 / "ch01_day2_visuals.rpy"
GALLERY = GAME / "chapters" / "ch01" / "day2" / "ch01_day2_gallery.rpy"

R, P = "relationship", "partner"
# The approved table (script.md section 4, canon call K5 for scene 30).
LEIA_IDS = {
    "ch01_d2_errand_cafe_love_thank": [(R, "love", 1)],
    "ch01_d2_errand_cafe_love_brush": [],
    "ch01_d2_errand_cafe_exhib_linger": [(P, "exhibitionism", 1)],
    "ch01_d2_errand_cafe_exhib_mention": [],
    "ch01_d2_errand_cafe_ntr_linger": [(R, "temptation", 1)],
    "ch01_d2_errand_cafe_ntr_shut": [],
    "ch01_d2_errand_shop_tell": [(R, "love", 1)],
    "ch01_d2_errand_shop_keep": [],
    "ch01_d2_errand_shop_mirror_leave": [(P, "exhibitionism", 1)],
    "ch01_d2_errand_shop_mirror_fix": [],
    "ch01_d2_errand_walk_tell": [(R, "sharing", 1)],
    "ch01_d2_errand_walk_keep": [(R, "temptation", 1)],
}
RYAN_IDS = {
    "ch01_d2_confession_ask": [(R, "sharing", 1)],
    "ch01_d2_confession_protect": [(R, "love", 1), (R, "trust", 1)],
    "ch01_d2_confession_brush": [],
    "ch01_d2_feed_love_tease": [(R, "love", 1)],
    "ch01_d2_feed_exhib_show": [(P, "exhibitionism", 1)],
    "ch01_d2_feed_told_aside": [(R, "trust", 1)],
    "ch01_d2_feed_kept_ask": [(R, "trust", 1)],
    "ch01_d2_feed_kept_silent": [(R, "temptation", 1)],
    "ch01_d2_feed_let_go": [],
}
ALL_IDS = dict(LEIA_IDS, **RYAN_IDS)
STAMPS = {
    "ch01_d2_errand_cafe_love_thank": "Love",
    "ch01_d2_errand_cafe_exhib_linger": "Love+Exhib",
    "ch01_d2_errand_cafe_ntr_linger": "May lead to NTR",
    "ch01_d2_errand_shop_tell": "Love",
    "ch01_d2_errand_shop_mirror_leave": "Love+Exhib",
    "ch01_d2_errand_walk_tell": "NTS",
    "ch01_d2_errand_walk_keep": "NTR",            # K4: route flag, not the one-step slip stamp
    "ch01_d2_confession_ask": "NTS",
    "ch01_d2_confession_protect": "Love",
    "ch01_d2_feed_love_tease": "Love",
    "ch01_d2_feed_exhib_show": "Love+Exhib",
    "ch01_d2_feed_told_aside": "Love",
    "ch01_d2_feed_kept_ask": "Love",
    "ch01_d2_feed_kept_silent": "May lead to NTR",
}
POSTS = ("d2_feed_love_poolguy", "d2_feed_love_shop", "d2_feed_exhib_poolguy", "d2_feed_exhib_poolguy_linger",
         "d2_feed_ntr_clip", "d2_feed_ntr_clip_linger")


def _read(path):
    return path.read_text(encoding="utf-8")


def _label(path, name):
    src = _read(path)
    body = src.split("label %s:" % name, 1)[1]
    body = re.split(r"\n(?:label |init |define |default |image |screen )", body, 1)[0]
    lines = body.rstrip().split("\n")
    while lines and lines[-1].startswith("#"):   # the next label's lead comment
        lines.pop()
    return "\n".join(lines)


def _labels(path):
    return re.findall(r"(?m)^label (\w+)", _read(path))


def _tuple(src, name):
    found = re.search(r"%s = \(([^)]*)\)" % name, src, re.S)
    return re.findall(r'"(\w+)"', found.group(1)) if found else []


class FlowTests(unittest.TestCase):
    def test_19b_bridges_into_the_doze_then_the_errand(self):
        sc19b = _label(SC19B, "ch01_day2_scene_19b_leia_asks_maya")
        self.assertTrue(sc19b.rstrip().endswith("jump ch01_day2_scene_19b2_ryan_dozes"))
        doze = _label(ERRAND, "ch01_day2_scene_19b2_ryan_dozes")
        self.assertTrue(doze.rstrip().endswith("jump ch01_day2_leia_errand"))

    def test_every_errand_path_leaves_only_into_19c(self):
        """Walk every jump/call from the bridge: all targets exist, the only exit is 19c."""
        labels = set(_labels(ERRAND))
        exits, todo, seen = set(), ["ch01_day2_scene_19b2_ryan_dozes"], set()
        while todo:
            name = todo.pop()
            if name in seen:
                continue
            seen.add(name)
            body = _label(ERRAND, name)
            for target in re.findall(r"(?m)^\s*(?:jump|call) (\w+)", body):
                if target in labels:
                    todo.append(target)
                elif not target.startswith("lc_leia_segment_"):
                    exits.add(target)
            for target in re.findall(r'call expression "(\w+)" \+', body):
                todo.extend(t for t in labels if t.startswith(target))
        self.assertEqual(exits, {"ch01_day2_scene_19c_back_outside"})
        self.assertEqual(labels - seen, set(), "unreachable errand labels")
        self.assertTrue(_label(SC19B, "ch01_day2_scene_19c_back_outside").rstrip()
                        .endswith("jump ch01_day2_scene_20_dinner_outfit"))

    def test_segment_frame_is_called_and_ends_before_19c(self):
        src = _read(ERRAND)
        self.assertIn('call lc_leia_segment_begin("ch01_d2") from ', src)
        walk = _label(ERRAND, "ch01_day2_errand_walk_back")
        self.assertLess(walk.index("call lc_leia_segment_end from "),
                        walk.index("jump ch01_day2_scene_19c_back_outside"))
        for line in src.splitlines():
            if re.match(r"\s*call (?!expression)", line):
                self.assertIn(" from ", line, line)

    def test_shop_branches_use_the_visit_helpers(self):
        src = _read(ERRAND)
        self.assertIn('lc_leia_visited_first("ch01_d2", "shop")', src)
        self.assertNotRegex(src, r"== \[")

    def test_lane_is_read_once_from_the_post_pool_record(self):
        opening = _label(ERRAND, "ch01_day2_leia_errand")
        self.assertIn('get_story_value("ch01_d2_route_lane_post_pool", ch01_d2_route_lane())', opening)
        self.assertIn('set_story_value("ch01_d2_errand_lane", d2_errand_lane)', opening)
        self.assertIn('"dream" if "ch01_d2_postshop_dream" in choice_history else "off"', opening)   # K1


class OldSaveTests(unittest.TestCase):
    def test_19c_keeps_the_original_line_when_the_errand_never_played(self):
        sc19c = _label(SC19B, "ch01_day2_scene_19c_back_outside")
        self.assertIn('$ d2_errand_lane = get_story_value("ch01_d2_errand_lane")', sc19c)
        old = sc19c.split("if d2_errand_lane is None:", 1)[1].split("else:", 1)[0]
        self.assertIn('"When [girlfriend_name] came back outside, [friend_name] checked the time and stood."', old)

    def test_later_errand_beats_need_the_errand_record(self):
        sc24 = _label(SC16_30, "ch01_day2_scene_24_dinner_aftermath")
        self.assertIn('if get_story_value("ch01_d2_errand_lane"):', sc24)
        confession = _label(SC19B, "ch01_day2_scene_19c_back_outside")
        self.assertIn('if get_story_value("ch01_d2_leia_told") == "told":', confession)
        sc20 = _label(SC16_30, "ch01_day2_scene_20_dinner_outfit")
        self.assertIn('if get_story_value("ch01_d2_leia_told") == "told":', sc20)

    def test_feed_posts_need_the_errand_lane(self):
        src = _read(FEED)
        for post in POSTS:
            call = re.search(r'lc_feed_register\(\s*"%s",.*?\)\n\n' % post, src + "\n\n", re.S)
            self.assertIsNotNone(call, post)
            self.assertRegex(call.group(0), r'unlock=\{"ch01_d2_errand_lane": "(love|exhibitionism|ntr_risk)"', post)


class ScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eff = effective_effects()

    def test_effects_match_the_approved_table(self):
        for cid, want in ALL_IDS.items():
            self.assertEqual([tuple(e) for e in self.eff.get(cid, [None])], want, cid)

    def test_full_mode_stamps(self):
        for cid, want in STAMPS.items():
            self.assertEqual(m.choice_route_tag(cid, self.eff[cid]), want, cid)
        for cid, effects in ALL_IDS.items():
            if not effects:
                self.assertEqual(m.choice_route_tag(cid, self.eff[cid]), "Neutral", cid)

    def test_lean_flag_stamps_the_plain_lean(self):
        self.assertEqual(m.route_tag([(R, "temptation", 1)]), "May lead to NTR")
        self.assertEqual(m.route_tag([(R, "temptation", 1)], "lean"), "NTR")
        self.assertEqual(m.CHOICE_ROUTE_FLAGS["ch01_d2_errand_walk_keep"], "lean")

    def test_only_her_choices_share_the_cap(self):
        src = _read(REG)
        call = re.search(r'lc_leia_register_choices\(\s*"ch01_d2",(.*?)\)', src, re.S)
        self.assertIsNotNone(call)
        self.assertEqual(set(re.findall(r'"(\w+)"', call.group(1))), set(LEIA_IDS))

    def test_her_side_never_gains_more_than_two_on_any_path(self):
        menus = {   # lane -> [(menu, ...)] in play order for each visit order
            ("love", "cafe"): [["ch01_d2_errand_cafe_love_thank", "ch01_d2_errand_cafe_love_brush"],
                               ["ch01_d2_errand_shop_tell", "ch01_d2_errand_shop_keep"]],
            ("love", "shop"): [["ch01_d2_errand_shop_tell", "ch01_d2_errand_shop_keep"],
                               ["ch01_d2_errand_cafe_love_thank", "ch01_d2_errand_cafe_love_brush"]],
            ("exhibitionism", "cafe"): [["ch01_d2_errand_cafe_exhib_linger", "ch01_d2_errand_cafe_exhib_mention"],
                                        ["ch01_d2_errand_shop_mirror_leave", "ch01_d2_errand_shop_mirror_fix"]],
            ("exhibitionism", "shop"): [["ch01_d2_errand_shop_tell", "ch01_d2_errand_shop_keep"],
                                        ["ch01_d2_errand_cafe_exhib_linger", "ch01_d2_errand_cafe_exhib_mention"]],
            ("ntr_risk", "cafe"): [["ch01_d2_errand_cafe_ntr_linger", "ch01_d2_errand_cafe_ntr_shut"],
                                   ["ch01_d2_errand_walk_tell", "ch01_d2_errand_walk_keep"]],
            ("ntr_risk", "shop"): [["ch01_d2_errand_cafe_ntr_linger", "ch01_d2_errand_cafe_ntr_shut"],
                                   ["ch01_d2_errand_walk_tell", "ch01_d2_errand_walk_keep"]],
        }
        from itertools import product
        for key, seq in menus.items():
            for picks in product(*seq):
                state = {}
                for cid in picks:
                    applied = L.cap_effects(state, "ch01_d2", self.eff[cid])
                    self.assertEqual(applied, self.eff[cid], (key, picks))   # Day Two never needs the cap
                    state = L.record_gain(state, "ch01_d2", cid, applied)
                self.assertLessEqual(L.gained(state, "ch01_d2"), L.DAILY_GAIN_CAP, (key, picks))

    def test_ntr_shop_has_no_menu_and_menus_stay_small(self):
        shop_first = _label(ERRAND, "ch01_day2_errand_shop_first")
        ntr = shop_first.split('if d2_errand_lane == "ntr_risk":', 1)[1].split("return", 1)[0]
        self.assertNotIn("menu", ntr)                                                  # K3
        self.assertNotIn("menu", _label(ERRAND, "ch01_day2_errand_shop_after_ntr"))


class ExemptionTests(unittest.TestCase):
    def test_every_new_id_is_lane_and_end_route_exempt(self):
        src = _read(REG)
        errand = _tuple(src, "CH01_D2_ERRAND_EXEMPT_CHOICES")
        self.assertEqual(set(errand), set(ALL_IDS))
        self.assertIn("CH01_D2_LANE_EXEMPT_CHOICES = (\"ch01_d2_knot_watch\",) + CH01_D2_ERRAND_EXEMPT_CHOICES", src)

    def _env(self, history, ledger=()):
        effects = {cid: list(e) for cid, e in ALL_IDS.items()}
        effects["ch01_d2_knot_watch"] = [(P, "exhibitionism", 1)]
        effects["ch01_d2_morning_tease"] = [(R, "love", 1), (P, "exhibitionism", 2)]
        state = {}
        for cid, applied in ledger:
            state = L.record_gain(state, "ch01_d2", cid, applied)
        store = SimpleNamespace(choice_history=list(history))
        leia = set(LEIA_IDS)
        env = {
            "renpy": SimpleNamespace(store=store),
            "CHOICE_EFFECTS": effects,
            "lc_stats_flat": lambda: {"love": 60, "trust": 60, "sharing": 0, "temptation": 10, "exhibitionism": 24},
            "lc_leia_is_side_choice": lambda cid: cid in leia,
            "lc_choice_applied_effects": lambda cid: (L.applied_effects(state, cid) if cid in leia
                                                      else list(effects[cid])),
            "lc_stat_model": m,
        }
        load(["CH01_D2_ERRAND_EXEMPT_CHOICES", "lc_exhib_gained", "ch01_d2_love_exhib_blend"], env)
        return env

    def test_end_route_blend_ignores_her_errand(self):
        threshold = m.THRESHOLDS["d2_love_exhib_blend"]
        # Raw stats sit on the blend line only because of her café linger; without it, no blend.
        env = self._env(["ch01_d2_errand_cafe_exhib_linger"],
                        [("ch01_d2_errand_cafe_exhib_linger", [(P, "exhibitionism", 1)])])
        flat = env["lc_stats_flat"]()
        flat["exhibitionism"] = threshold
        env["lc_stats_flat"] = lambda: dict(flat)
        self.assertTrue(m.d2_love_exhib_blend("love", flat, 1))
        self.assertFalse(env["ch01_d2_love_exhib_blend"]("love"))

    def test_end_route_blend_still_counts_door_a(self):
        threshold = m.THRESHOLDS["d2_love_exhib_blend"]
        env = self._env(["ch01_d2_knot_watch"])
        env["lc_stats_flat"] = lambda: {"love": 60, "trust": 60, "sharing": 0, "temptation": 10,
                                        "exhibitionism": threshold}
        self.assertTrue(env["ch01_d2_love_exhib_blend"]("love"))

    def test_scene_30_and_the_lean_readout_use_the_exempt_blend(self):
        sc30 = _label(SC16_30, "ch01_day2_scene_30_bedroom")
        self.assertIn("d2_love_exhib_blend = ch01_d2_love_exhib_blend(d2_lane)", sc30)
        self.assertNotIn("lc_stat_model.d2_love_exhib_blend(", sc30)
        reg = _read(REG)  # Day Two's Full "Current lean" reader (current_lean hook)
        lean = reg.split("def ch01_d2_current_lean(", 1)[1].split("def ch01_d2_keep_legacy_lane", 1)[0]
        self.assertIn("ch01_d2_love_exhib_blend(lane)", lean)


class ConfessionAndSceneTests(unittest.TestCase):
    def test_confession_sits_before_the_19c_jump_and_reply_is_ryans(self):
        sc19c = _label(SC19B, "ch01_day2_scene_19c_back_outside")
        anchor = sc19c.index("Don't tell her it worked.")
        confession = sc19c.index('\n    if get_story_value("ch01_d2_leia_told") == "told":')
        self.assertLess(anchor, confession)
        self.assertLess(confession, sc19c.index("jump ch01_day2_scene_20_dinner_outfit"))
        for cid in ("ch01_d2_confession_ask", "ch01_d2_confession_protect", "ch01_d2_confession_brush"):
            self.assertIn('apply_choice("%s")' % cid, sc19c)

    def test_scene_20_told_lead_in(self):
        sc20 = _label(SC16_30, "ch01_day2_scene_20_dinner_outfit")
        told = sc20.split('if get_story_value("ch01_d2_leia_told") == "told":', 1)[1]
        self.assertIn('gf "So I told you my thing. Can I ask you something now? It\'s only fair."', told)
        self.assertIn('gf "Hey. Can I ask you something?"', told.split("else:", 1)[1])

    def test_scene_30_option_sits_before_every_bedroom_gate(self):
        sc30 = _label(SC16_30, "ch01_day2_scene_30_bedroom")
        option = sc30.index('lc_feed_seen("d2_feed_love_poolguy")')
        self.assertLess(sc30.index("$ ch01_d2_maya_dm_settle()"), option)
        self.assertLess(option, sc30.index("if d2_soft_gate and d2_wink:"))
        self.assertLess(sc30.index("call lc_feed_reaction_runner"), option)
        for cid in RYAN_IDS:
            if cid.startswith("ch01_d2_feed_"):
                self.assertIn('apply_choice("%s")' % cid, sc30)


class FeedTests(unittest.TestCase):
    def test_lane_posts_release_once_after_dinner_on_the_story_clock(self):
        sc24 = _label(SC16_30, "ch01_day2_scene_24_dinner_aftermath")
        block = sc24.split('if get_story_value("ch01_d2_errand_lane"):', 1)[1]
        self.assertLess(sc24.index("let the night follow us home."), sc24.index('if get_story_value("ch01_d2_errand_lane"):'))
        self.assertEqual(len(re.findall(r"lc_feed_release\(", sc24)), 1)
        release = re.search(r"lc_feed_release\(([^)]*)\)", block).group(1)
        self.assertEqual(set(re.findall(r'"(\w+)"', release)), set(POSTS))
        self.assertLess(block.index("lc_phone_set_story_time("), block.index("lc_feed_release("))
        self.assertLess(block.index("lc_feed_release("), block.index("lc_phone_clear_story_time()"))

    def test_posts_follow_her_choices_and_have_reactions(self):
        src = _read(FEED)
        labels = set(re.findall(r"(?m)^label (\w+)", src))
        for post in POSTS:
            call = re.search(r'lc_feed_register\(\s*"%s",.*?\)\n\n' % post, src + "\n\n", re.S).group(0)
            reaction = re.search(r'reaction="(\w+)"', call)
            self.assertIsNotNone(reaction, post)
            self.assertIn(reaction.group(1), labels, post)
        for base in ("d2_feed_exhib_poolguy", "d2_feed_ntr_clip"):
            plain = re.search(r'lc_feed_register\(\s*"%s",.*?\)\n\n' % base, src, re.S).group(0)
            linger = re.search(r'lc_feed_register\(\s*"%s_linger",.*?\)\n\n' % base, src, re.S).group(0)
            self.assertIn('"leia_did_not":', plain)
            self.assertIn('"leia_did":', linger)

    def test_clip_photo_is_the_mature_placeholder(self):
        src = _read(FEED)
        for post in ("d2_feed_ntr_clip", "d2_feed_ntr_clip_linger"):
            call = re.search(r'lc_feed_register\(\s*"%s",.*?\)\n\n' % post, src, re.S).group(0)
            self.assertIn('image="cg d2_feed_cafe_clip"', call)
            self.assertIn("mature=True", call)

    def test_scene_30_reads_both_variants(self):
        sc30 = _label(SC16_30, "ch01_day2_scene_30_bedroom")
        self.assertIn('lc_feed_any_seen("d2_feed_exhib_poolguy", "d2_feed_exhib_poolguy_linger")', sc30)
        self.assertIn('lc_feed_any_seen("d2_feed_ntr_clip", "d2_feed_ntr_clip_linger")', sc30)


class ArtTests(unittest.TestCase):
    def test_placeholders_are_defined_and_labelled(self):
        src = _read(VISUALS)
        for name in ("bg ch01_shop_day", "cg d2_cafe_stranger", "cg d2_feed_cafe_clip"):
            block = src.split("image %s = " % name, 1)
            self.assertEqual(len(block), 2, name)
            self.assertIn("PLACEHOLDER", block[1].split("\nimage ", 1)[0], name)
        self.assertNotIn("ch01_conveniencestore", _read(ERRAND))

    def test_cafe_cg_has_a_gallery_page(self):
        src = _read(GALLERY)
        self.assertRegex(src, r'gallery_row\("d2_cafe_stranger", "ch01_d2"')
        placeholders = src.split("GALLERY_PLACEHOLDER_IMAGES.update([", 1)[1].split("])", 1)[0]
        self.assertIn('"d2_cafe_stranger"', placeholders)

    def test_places_register_real_backgrounds(self):
        src = _read(REG)
        self.assertIn('lc_leia_register_places("ch01_d2", CH01_D2_ERRAND_PLACES)', src)
        bgs = re.findall(r'"bg":\s*"([^"]+)"', src)
        self.assertEqual(bgs, ["bg ch01_d2_cafe", "bg ch01_shop_day", "bg ch01_restaurant_bar", "bg ch01_d2_boutique"])


if __name__ == "__main__":
    unittest.main()
