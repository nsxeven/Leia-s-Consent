"""Route simulation for Days 1-2 under stat model v2 (pure Python, no Ren'Py).

Plays representative choice sequences through the EFFECTIVE choice effects and
the same resolvers the story calls (lc_stat_model.d1_route_pressure,
d1_love_bedtime, d2_route_lane, d2_love_exhib_blend), following the Day 2
branch structure (pool suspicion on the NTR lane, the sunset soft gate, the
dinner wink, the bedroom menus). Asserts every Day 1 / Day 2 end state is
reachable and that each play style lands on its intended route. Retune
lc_stat_model.THRESHOLDS until this passes.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import lc_leia_side as L  # noqa: E402
import lc_stat_model as m  # noqa: E402
from lc_effective_effects import effective_effects  # noqa: E402

EFF = effective_effects()

# Day 1 menus in play order (ch01_main, scenes 04-06, 07-13, 14-30 up to the Day 1 resolver).
D1 = [
    ["ch01_outfit_bolder", "ch01_outfit_comfort", "ch01_outfit_conservative", "ch01_outfit_rush"],
    ["ch01_photo_support", "ch01_photo_more", "ch01_photo_exit", "ch01_photo_rush"],
    ["ch01_towel_laugh", "ch01_towel_boundary", "ch01_towel_forget"],
    ["ch01_towel_reassure", "ch01_towel_honest", "ch01_towel_tease", "ch01_towel_shrug"],
    ["ch01_bra_reassure", "ch01_bra_playful", "ch01_bra_cover", "ch01_bra_distracted"],
    ["ch01_stranger_proud", "ch01_stranger_territorial", "ch01_stranger_encourage"],
    ["ch01_catch_ignore", "ch01_catch_check", "ch01_catch_joke", "ch01_catch_boundary"],
    ["ch01_friend_reassure", "ch01_friend_tease", "ch01_friend_boundary"],
    ["ch01_julian_reassure", "ch01_julian_honest", "ch01_julian_joke", "ch01_julian_fine"],
    ["ch01_carry_brush", "ch01_carry_lookaway", "ch01_carry_fix", "ch01_carry_joke"],
    ["ch01_upstairs_honest", "ch01_upstairs_liked", "ch01_upstairs_swallow", "ch01_upstairs_snap"],
    ["ch01_movie_stop", "ch01_movie_subtle", "ch01_movie_tease_presence", "ch01_movie_dismiss_concern"],
    ["ch01_can_tell_behave", "ch01_can_tell_tease", "ch01_can_tell_push", "ch01_can_tell_dismiss"],
    ["ch01_private_apologize", "ch01_private_playful", "ch01_private_curiosity", "ch01_private_dismiss"],
    ["ch01_noblanket_behave", "ch01_noblanket_test", "ch01_noblanket_tease", "ch01_noblanket_phone"],
    ["ch01_watch_claim", "ch01_watch_tease", "ch01_watch_check", "ch01_watch_ignore"],
    ["ch01_micro_warn", "ch01_micro_silent", "ch01_micro_open", "ch01_micro_dismiss"],
    ["ch01_philosophy_couple", "ch01_philosophy_trust", "ch01_philosophy_jealousy_fun", "ch01_philosophy_dont_care"],
    ["ch01_julian_change_subject", "ch01_julian_let_play", "ch01_julian_put_spot", "ch01_julian_dont_care"],
    ["ch01_compliment_affirm", "ch01_compliment_tease", "ch01_compliment_enjoy", "ch01_compliment_shrug"],
    ["ch01_alone_apologize", "ch01_alone_curiosity", "ch01_alone_open", "ch01_alone_dismiss"],
    ["ch01_private_claim", "ch01_private_open", "ch01_private_jealous", "ch01_private_indifferent"],
]
DREAM = ["ch01_dream_ground", "ch01_dream_curiosity", "ch01_dream_withdraw"]
# Day 2 menus before the pre-split lane snapshot, as they play. The scene 3
# "Is she pretty?" menu plays inside ch01_day2_scene_03_maya_message. The
# boutique go/leave menu only shows on the NTR-risk lane. The reveal menu is Ryan's reply
# to her changing-room selfie: it always plays, before the go/leave menu (handled in
# play()). The post-shop "I'm fine."
# menu is flavor since v0.2.0; the cafe overheard incident is scored in its place.
D2_PRE = [
    ["ch01_d2_morning_reassure", "ch01_d2_morning_tease", "ch01_d2_morning_dismiss"],
    ["ch01_d2_maya_reassure", "ch01_d2_maya_tease_jealousy", "ch01_d2_maya_open_honest"],
    ["ch01_d2_maya_include", "ch01_d2_maya_catchup", "ch01_d2_maya_dismiss_leia"],
    ["ch01_d2_mall_go_to_leia", "ch01_d2_mall_leave_to_maya"],
    ["ch01_d2_mall_reveal_affection", "ch01_d2_mall_reveal_open", "ch01_d2_mall_reveal_tease",
     "ch01_d2_mall_reveal_flat"],
    ["ch01_d2_postshop_sleep", "ch01_d2_postshop_head", "ch01_d2_postshop_shut_down"],
    ["ch01_d2_overheard_own", "ch01_d2_overheard_joke", "ch01_d2_overheard_pretend"],
]
MALL_GO, MALL_REVEAL = 3, 4
POOL = ["ch01_d2_pool_reassure", "ch01_d2_pool_honest_jealous", "ch01_d2_pool_accuse"]
SUNSET = ["ch01_d2_sunset_connect", "ch01_d2_sunset_partial", "ch01_d2_sunset_ignore_gate"]
BED = {"ch01_d2_bed_pool_love": "love", "ch01_d2_bed_pool_exhibition": "exhibitionism",
       "ch01_d2_bed_pool_accuse": "mixed_unresolved"}
WINK = ["ch01_d2_wink_repair", "ch01_d2_wink_accuse_hard", "ch01_d2_wink_reject_hard"]

# Leia's errand (Leia's side design, Day Two): it plays between 19b and 19c, after the post-pool
# lane record. Her picks per (post-pool lane, first stop) in play order; on the NTR lane the shop has
# no menu (canon call K3) and her second pick is the walk back (WALK_BACK). Every id below is left
# out of today's lanes and end route (CH01_D2_ERRAND_EXEMPT_CHOICES, read from the game source).
ERRAND_DAY = "ch01_d2"
ERRAND_MENUS = {
    ("love", "cafe"): [["ch01_d2_errand_cafe_love_thank", "ch01_d2_errand_cafe_love_brush"],
                       ["ch01_d2_errand_shop_tell", "ch01_d2_errand_shop_keep"]],
    ("love", "shop"): [["ch01_d2_errand_shop_tell", "ch01_d2_errand_shop_keep"],
                       ["ch01_d2_errand_cafe_love_thank", "ch01_d2_errand_cafe_love_brush"]],
    ("exhibitionism", "cafe"): [["ch01_d2_errand_cafe_exhib_linger", "ch01_d2_errand_cafe_exhib_mention"],
                                ["ch01_d2_errand_shop_mirror_leave", "ch01_d2_errand_shop_mirror_fix"]],
    ("exhibitionism", "shop"): [["ch01_d2_errand_shop_tell", "ch01_d2_errand_shop_keep"],
                                ["ch01_d2_errand_cafe_exhib_linger", "ch01_d2_errand_cafe_exhib_mention"]],
    ("ntr_risk", "cafe"): [["ch01_d2_errand_cafe_ntr_linger", "ch01_d2_errand_cafe_ntr_shut"]],
    ("ntr_risk", "shop"): [["ch01_d2_errand_cafe_ntr_linger", "ch01_d2_errand_cafe_ntr_shut"]],
}
WALK_BACK = ["ch01_d2_errand_walk_tell", "ch01_d2_errand_walk_keep"]
CONFESSION = ["ch01_d2_confession_ask", "ch01_d2_confession_protect", "ch01_d2_confession_brush"]
FEED_OPTIONS = {
    "love": ["ch01_d2_feed_love_tease", "ch01_d2_feed_let_go"],
    "exhibitionism": ["ch01_d2_feed_exhib_show", "ch01_d2_feed_let_go"],
    "told": ["ch01_d2_feed_told_aside", "ch01_d2_feed_let_go"],
    "kept": ["ch01_d2_feed_kept_ask", "ch01_d2_feed_kept_silent"],
}


def _errand_exempt():
    src = (ROOT / "game" / "chapters" / "ch01" / "day2" / "ch01_day2_registrations.rpy").read_text(encoding="utf-8")
    found = re.search(r"CH01_D2_ERRAND_EXEMPT_CHOICES = \(([^)]*)\)", src, re.S)
    return frozenset(re.findall(r'"(\w+)"', found.group(1))) if found else frozenset()


ERRAND_EXEMPT = _errand_exempt()

LOVE = ("Love", "Repair", "Neutral")
LE = ("Love+Exhib", "Love")
NTR = ("NTR", "May lead to NTR", "Locks NTR", "Neutral")


def tag(choice_id):
    return m.choice_route_tag(choice_id, EFF[choice_id])


def pick(menu, prefs):
    if isinstance(prefs, str):
        return prefs if prefs in menu else pick(menu, (prefs,))
    for want in prefs:
        for choice_id in menu:
            if choice_id == want or tag(choice_id) == want:
                return choice_id
    return menu[0]


def per_menu(prefs, index):
    return prefs[index] if isinstance(prefs, list) else prefs


def play(d1, d2, pool=None, sunset=None, bed=None, wink=None, errand=None):
    """Returns (day1_pressure, day1_love_bedtime, day2_end_route, love_exhib_blend, stats, info).

    errand: None (an old save past 19b: no errand) or Leia's errand picks (see ERRAND_MENUS):
    {"order": "cafe"|"shop", "picks": (i, j), "told": bool, "reply": k, "feed": f or None}.
    info: {"post_pool": lane, "dinner": lane, "leia_gain": her capped gains, "leia_registered": ...}.
    """
    stats = {s: m.DEFAULTS[m.STAT_GROUPS[s]][s] for s in m.STAT_ORDER}
    history = []          # (choice_id, applied effects)
    exempt = []           # (choice_id, applied effects) left out of today's lanes and end route
    leia_state = {}
    info = {"leia_gain": 0, "leia_registered": 0}

    def apply(choice_id, capped=False):
        effects = list(EFF[choice_id])
        if capped:
            nonlocal leia_state
            info["leia_registered"] += sum(a for _g, _s, a in effects if a > 0)
            effects = L.cap_effects(leia_state, ERRAND_DAY, effects)
            leia_state = L.record_gain(leia_state, ERRAND_DAY, choice_id, effects)
        for _group, stat, amount in effects:
            stats[stat] = m.clamp(stats[stat] + amount)
        history.append((choice_id, effects))
        if choice_id in ERRAND_EXEMPT:
            exempt.append((choice_id, effects))

    def gained_today():
        return sum(a for c, eff in history if c.startswith("ch01_d2_") for _g, s, a in eff if s == "exhibitionism")

    def lane_inputs():
        """Stats and today's Exhibitionism without the exempt picks (CH01_D2_ERRAND_EXEMPT_CHOICES)."""
        flat, gained = dict(stats), gained_today()
        for _cid, effects in exempt:
            for _group, stat, amount in effects:
                flat[stat] -= amount
                if stat == "exhibitionism":
                    gained -= amount
        return flat, gained

    for i, menu in enumerate(D1):
        apply(pick(menu, per_menu(d1, i)))
    pressure = m.d1_route_pressure(stats)
    bedtime = m.d1_love_bedtime(pressure, stats)
    apply(pick(DREAM, per_menu(d2, 0)))
    for i, menu in enumerate(D2_PRE):
        if i == MALL_GO:
            # The selfie reply (reveal menu) plays first on every lane, then Maya's shout.
            apply(pick(D2_PRE[MALL_REVEAL], per_menu(d2, MALL_REVEAL + 1)))
            if m.d2_route_lane(stats, pressure, gained_today()) != "ntr_risk":
                continue
            apply(pick(menu, per_menu(d2, i + 1)))
            continue
        if i == MALL_REVEAL:
            continue
        apply(pick(menu, per_menu(d2, i + 1)))

    lane = m.d2_route_lane(stats, pressure, gained_today())          # pre_split
    pool_suspicion = lane == "ntr_risk"
    if pool_suspicion:
        apply(pick(POOL, pool or per_menu(d2, -1)))
    lane = m.d2_route_lane(stats, pressure, gained_today())          # post_pool
    info["post_pool"] = lane
    told = None
    if errand is not None:
        # 19b -> Leia's errand (her picks share the +2 cap) -> 19c confession (Ryan's, uncapped).
        menus = ERRAND_MENUS[(lane, errand["order"])]
        for menu, index in zip(menus, errand["picks"]):
            apply(menu[index], capped=True)
        if lane == "ntr_risk":
            told = errand["told"]
            apply(WALK_BACK[0 if told else 1], capped=True)
            if told:
                apply(CONFESSION[errand["reply"]])
        info["leia_gain"] = L.gained(leia_state, ERRAND_DAY)
    soft_gate = False
    if lane == "ntr_risk":
        choice = pick(SUNSET, sunset or per_menu(d2, -1))
        apply(choice)
        soft_gate = choice == "ch01_d2_sunset_ignore_gate"
    flat, gained = lane_inputs()
    lane = m.d2_route_lane(flat, pressure, gained)                   # post_sunset / dinner
    info["dinner"] = lane
    wink_seen = soft_gate and lane == "ntr_risk"
    blend = m.d2_love_exhib_blend(lane, *lane_inputs())
    if errand is not None and errand.get("feed") is not None:
        # Scene 30 "saw a post": wording follows the errand lane, before every bedroom gate.
        key = info["post_pool"] if info["post_pool"] != "ntr_risk" else ("told" if told else "kept")
        apply(FEED_OPTIONS[key][errand["feed"]])
    if soft_gate and wink_seen:
        choice = pick(WINK, wink or per_menu(d2, -1))
        apply(choice)
        end = "love_repaired" if choice == "ch01_d2_wink_repair" else "ntr_confirmed"
    elif pool_suspicion and not soft_gate and lane == "ntr_risk":
        choice = pick(list(BED), bed or per_menu(d2, -1))
        apply(choice)
        end = BED[choice]
    elif lane == "exhibitionism" or blend:
        end = "love" if (blend and lane == "love") else "exhibitionism"
    else:
        end = "love"
    return pressure, bedtime, end, blend, dict(stats), info


MIXED_D1 = [LE if i % 2 else LOVE for i in range(len(D1))]
TWO_SLIPS = [LOVE] * len(D1)
TWO_SLIPS[12] = TWO_SLIPS[19] = NTR          # can_tell + compliment
THREE_SLIPS = list(TWO_SLIPS)
THREE_SLIPS[13] = NTR                        # + private talk

# name, Day 1 prefs, Day 2 prefs, branch picks, expected (pressure, bedtime, Day 2 end, blend); None = any
PERSONAS = [
    ("pure Love", LOVE, LOVE, {}, ("mixed", True, "love", False)),
    ("Love + Exhibitionism", LE, LE, {}, ("nts_seeded", False, "exhibitionism", False)),
    ("Love with a playful edge", MIXED_D1, [("Love",)] + [LE] * 7, {}, ("mixed", None, "love", True)),
    ("Love, two slips on Day 1", TWO_SLIPS, LOVE, {}, ("mixed", False, "love", False)),
    ("three slips on Day 1, then Love", THREE_SLIPS, LOVE, {}, ("ntr_seeded", False, "love", False)),
    # Slow burn both ways: a loving Day 1 doesn't make Day 2 immune. Slipping on every
    # Day 2 answer (six slips) opens the NTR-risk lane; the sunset talk still repairs it.
    ("Love on Day 1, slips on half of Day 2", LOVE, [LOVE, NTR, LOVE, LOVE, LOVE, NTR, NTR, LOVE], {},
     ("mixed", True, "love", False)),
    ("Love on Day 1, slips all through Day 2", LOVE, NTR, {}, ("mixed", True, "ntr_confirmed", False)),
    ("Love on Day 1, slips all through Day 2, opens up at sunset", LOVE, NTR,
     {"sunset": "ch01_d2_sunset_connect", "bed": "ch01_d2_bed_pool_love"}, ("mixed", True, "love", False)),
    ("NTR, locked at the wink", NTR, NTR, {"wink": "ch01_d2_wink_reject_hard"}, ("ntr_seeded", False, "ntr_confirmed", False)),
    ("NTR, accuses at the wink", NTR, NTR, {"wink": "ch01_d2_wink_accuse_hard"}, ("ntr_seeded", False, "ntr_confirmed", False)),
    ("NTR, repaired at the wink", NTR, NTR, {"wink": "ch01_d2_wink_repair"}, ("ntr_seeded", False, "love_repaired", False)),
    ("NTR, pool suspicion left unresolved", NTR, NTR,
     {"sunset": "ch01_d2_sunset_partial", "bed": "ch01_d2_bed_pool_accuse"}, ("ntr_seeded", False, "mixed_unresolved", False)),
    ("NTR, believes her at bedtime", NTR, NTR,
     {"sunset": "ch01_d2_sunset_connect", "bed": "ch01_d2_bed_pool_love"}, ("ntr_seeded", False, "love", False)),
    ("NTR, admits the thrill at bedtime", NTR, NTR,
     {"sunset": "ch01_d2_sunset_partial", "bed": "ch01_d2_bed_pool_exhibition"}, ("ntr_seeded", False, "exhibitionism", False)),
]


class RouteSimulationTests(unittest.TestCase):

    def test_each_play_style_lands_on_its_route(self):
        for name, d1, d2, branch, want in PERSONAS:
            got = play(d1, d2, **branch)
            with self.subTest(name):
                for expected, actual, what in zip(want, got, ("Day 1 pressure", "Day 1 love bedtime", "Day 2 end", "blend")):
                    if expected is not None:
                        self.assertEqual(actual, expected, "{}: {} (stats {})".format(name, what, got[4]))

    def test_every_day1_and_day2_end_state_is_reachable(self):
        results = [play(d1, d2, **branch) for _name, d1, d2, branch, _want in PERSONAS]
        self.assertEqual({r[0] for r in results}, {"mixed", "nts_seeded", "ntr_seeded"})
        self.assertIn(True, {r[1] for r in results})
        self.assertEqual({r[2] for r in results},
                         {"love", "exhibitionism", "love_repaired", "mixed_unresolved", "ntr_confirmed"})
        self.assertIn(True, {r[3] for r in results})

    def test_a_single_slip_never_seeds_ntr(self):
        for index, menu in enumerate(D1):
            prefs = [LOVE] * len(D1)
            prefs[index] = NTR
            self.assertNotEqual(play(prefs, LOVE)[0], "ntr_seeded", menu)

    def test_any_two_slips_never_seed_ntr_and_any_three_do(self):
        # darryn (choice-sense pass): one Day 1 slip never seeds NTR, three do.
        # Two must not either, whichever two; and any three must.
        from itertools import combinations
        slips = [i for i, menu in enumerate(D1) if any(tag(c) in NTR for c in menu if EFF[c])]
        self.assertGreaterEqual(len(slips), 18)
        for n, want in ((2, False), (3, True)):
            for combo in combinations(slips, n):
                prefs = [LOVE] * len(D1)
                for i in combo:
                    prefs[i] = NTR
                got = play(prefs, LOVE)[0] == "ntr_seeded"
                self.assertEqual(got, want, [D1[i][0] for i in combo])

    def test_day1_and_day2_slips_are_small(self):
        # Slow burn: an ordinary Day 1-2 slip is Temptation +1 with at most a small
        # Love/Trust cost. Gates (sunset, wink) are the only big moves.
        menus = D1 + [DREAM] + D2_PRE + [POOL, SUNSET, list(BED), WINK]
        for menu in menus:
            for cid in menu:
                d = m.effect_deltas(EFF[cid])
                if d.get("temptation", 0) > 0 and cid not in m.CHOICE_GATES:
                    # darryn 2026-11-19: hearing Leia confide and pretending not to counts double
                    # (it replaced the cut pair-photo slip).
                    self.assertEqual(d["temptation"], 2 if cid == "ch01_d2_overheard_pretend" else 1, cid)
                    self.assertGreaterEqual(min(d.get("love", 0), d.get("trust", 0)), -2, cid)
                    self.assertIn(tag(cid), ("NTR",) if cid == "ch01_d2_overheard_pretend" else ("May lead to NTR",), cid)

    def test_every_day1_and_day2_menu_offers_a_slip(self):
        # Principle 5: each scored menu has a believable slip, so stamps show a real spread.
        # Menus without one on purpose: the towel aside with Julian (Leia is off-screen),
        # and the restored scene 3 "Is she pretty?" breakfast menu (original effects kept).
        skip = {"ch01_towel_laugh", "ch01_d2_maya_reassure"}
        for menu in D1 + [DREAM] + D2_PRE:
            if menu[0] in skip or menu[0] == "ch01_d2_mall_go_to_leia":
                continue
            self.assertTrue(any(tag(c) in NTR and tag(c) != "Neutral" for c in menu), menu)

    def test_thresholds_stay_ordered(self):
        t = m.THRESHOLDS
        self.assertLess(t["d1_love_bedtime_temptation_max"], t["d1_ntr_seed_temptation"])
        self.assertLessEqual(t["d2_risk_temptation"], t["d2_risk_temptation_unseeded"])
        self.assertLess(t["d2_love_exhib_blend"], t["d2_exhib_lane"])
        self.assertLess(t["d1_can_tell_unsure"], t["d1_can_tell_bold"])
        self.assertLess(t["d5_comfortable_after_brief"], t["d5_comfortable"])


def errand_variants(lane):
    """Every errand a save on this post-pool lane can play: visit order x her picks x told/kept x
    Ryan's confession reply x the scene 30 feed option (None = he never opened the feed)."""
    from itertools import product
    for order in ("cafe", "shop"):
        for picks in product(range(2), repeat=len(ERRAND_MENUS[(lane, order)])):
            for told in ((True, False) if lane == "ntr_risk" else (None,)):
                for reply in (range(len(CONFESSION)) if told else (None,)):
                    key = lane if lane != "ntr_risk" else ("told" if told else "kept")
                    for feed in (None,) + tuple(range(len(FEED_OPTIONS[key]))):
                        yield {"order": order, "picks": picks, "told": told, "reply": reply, "feed": feed}


class ErrandRouteTests(unittest.TestCase):
    """Leia's errand (Day Two, between 19b and 19c) and its follow-ups never change tonight's
    lane or end route: every lane x visit order x told/kept x reply x feed option."""

    def test_every_errand_id_is_exempt(self):
        ids = set(WALK_BACK) | set(CONFESSION) | {c for menus in ERRAND_MENUS.values() for mn in menus for c in mn}
        ids |= {c for opts in FEED_OPTIONS.values() for c in opts}
        self.assertEqual(ERRAND_EXEMPT, ids)

    def test_personas_reach_every_errand_lane(self):
        lanes = {play(d1, d2, **branch)[5]["post_pool"] for _n, d1, d2, branch, _w in PERSONAS}
        self.assertEqual(lanes, {"love", "exhibitionism", "ntr_risk"})

    def test_errand_never_changes_tonights_lane_or_end_route(self):
        for name, d1, d2, branch, _want in PERSONAS:
            base = play(d1, d2, **branch)
            runs = 0
            for errand in errand_variants(base[5]["post_pool"]):
                got = play(d1, d2, errand=errand, **branch)
                runs += 1
                with self.subTest(name, errand=errand):
                    self.assertEqual(got[2], base[2], "end route")
                    self.assertEqual(got[3], base[3], "love+exhib blend")
                    self.assertEqual(got[5]["dinner"], base[5]["dinner"], "dinner lane")
                    self.assertLessEqual(got[5]["leia_gain"], L.DAILY_GAIN_CAP)
                    # Day Two's errand never needs the cap: two scored picks of +1 at most.
                    self.assertEqual(got[5]["leia_gain"], got[5]["leia_registered"])
            self.assertGreaterEqual(runs, 12, name)

    def test_errand_stats_still_count_from_day_three(self):
        name, d1, d2, branch, _want = PERSONAS[0]
        base = play(d1, d2, **branch)
        warm = play(d1, d2, errand={"order": "cafe", "picks": (0, 0), "told": None, "reply": None, "feed": 0},
                    **branch)
        self.assertEqual(base[5]["post_pool"], "love")
        self.assertEqual(warm[4]["love"], min(100, base[4]["love"] + 3))   # thank, tell, tease
        self.assertEqual(warm[2], base[2])


if __name__ == "__main__":
    unittest.main()
