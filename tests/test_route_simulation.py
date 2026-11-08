"""Route simulation for Days 1-2 under stat model v2 (pure Python, no Ren'Py).

Plays representative choice sequences through the EFFECTIVE choice effects and
the same resolvers the story calls (lc_stat_model.d1_route_pressure,
d1_love_bedtime, d2_route_lane, d2_love_exhib_blend), following the Day 2
branch structure (pool suspicion on the NTR lane, the sunset soft gate, the
dinner wink, the bedroom menus). Asserts every Day 1 / Day 2 end state is
reachable and that each play style lands on its intended route. Retune
lc_stat_model.THRESHOLDS until this passes.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

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
# Day 2 menus before the pre-split lane snapshot, as they play. The scene 3 Maya
# menu (ch01_d2_maya_reassure/...) sits in a label overridden by
# zzzz_ch01_day2_polish_revision.rpy, so it never plays and is left out. The
# boutique go/leave menu only shows on the NTR-risk lane, and the reveal menu
# only when Ryan went over (both handled in play()).
D2_PRE = [
    ["ch01_d2_morning_reassure", "ch01_d2_morning_tease", "ch01_d2_morning_dismiss"],
    ["ch01_d2_maya_include", "ch01_d2_maya_catchup", "ch01_d2_maya_dismiss_leia"],
    ["ch01_d2_photo_pair_encourage", "ch01_d2_photo_pair_redirect", "ch01_d2_photo_pair_shrug"],
    ["ch01_d2_mall_go_to_leia", "ch01_d2_mall_leave_to_maya"],
    ["ch01_d2_mall_reveal_affection", "ch01_d2_mall_reveal_open", "ch01_d2_mall_reveal_tease",
     "ch01_d2_mall_reveal_flat"],
    ["ch01_d2_postshop_sleep", "ch01_d2_postshop_head", "ch01_d2_postshop_shut_down"],
]
MALL_GO, MALL_REVEAL = 3, 4
POOL = ["ch01_d2_pool_reassure", "ch01_d2_pool_honest_jealous", "ch01_d2_pool_accuse"]
SUNSET = ["ch01_d2_sunset_connect", "ch01_d2_sunset_partial", "ch01_d2_sunset_ignore_gate"]
BED = {"ch01_d2_bed_pool_love": "love", "ch01_d2_bed_pool_exhibition": "exhibitionism",
       "ch01_d2_bed_pool_accuse": "mixed_unresolved"}
WINK = ["ch01_d2_wink_repair", "ch01_d2_wink_accuse_hard", "ch01_d2_wink_reject_hard"]

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


def play(d1, d2, pool=None, sunset=None, bed=None, wink=None):
    """Returns (day1_pressure, day1_love_bedtime, day2_end_route, love_exhib_blend, stats)."""
    stats = {s: m.DEFAULTS[m.STAT_GROUPS[s]][s] for s in m.STAT_ORDER}
    history = []

    def apply(choice_id):
        for _group, stat, amount in EFF[choice_id]:
            stats[stat] = m.clamp(stats[stat] + amount)
        history.append(choice_id)

    def gained_today():
        return sum(a for c in history if c.startswith("ch01_d2_") for _g, s, a in EFF[c] if s == "exhibitionism")

    for i, menu in enumerate(D1):
        apply(pick(menu, per_menu(d1, i)))
    pressure = m.d1_route_pressure(stats)
    bedtime = m.d1_love_bedtime(pressure, stats)
    apply(pick(DREAM, per_menu(d2, 0)))
    ryan_at_reveal = True
    for i, menu in enumerate(D2_PRE):
        if i == MALL_GO:
            if m.d2_route_lane(stats, pressure, gained_today()) != "ntr_risk":
                continue
            choice = pick(menu, per_menu(d2, i + 1))
            ryan_at_reveal = choice == "ch01_d2_mall_go_to_leia"
            apply(choice)
            continue
        if i == MALL_REVEAL and not ryan_at_reveal:
            continue
        apply(pick(menu, per_menu(d2, i + 1)))

    lane = m.d2_route_lane(stats, pressure, gained_today())          # pre_split
    pool_suspicion = lane == "ntr_risk"
    if pool_suspicion:
        apply(pick(POOL, pool or per_menu(d2, -1)))
    lane = m.d2_route_lane(stats, pressure, gained_today())          # post_pool
    soft_gate = False
    if lane == "ntr_risk":
        choice = pick(SUNSET, sunset or per_menu(d2, -1))
        apply(choice)
        soft_gate = choice == "ch01_d2_sunset_ignore_gate"
    lane = m.d2_route_lane(stats, pressure, gained_today())          # post_sunset / dinner
    wink_seen = soft_gate and lane == "ntr_risk"
    blend = m.d2_love_exhib_blend(lane, stats, gained_today())
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
    return pressure, bedtime, end, blend, dict(stats)


MIXED_D1 = [LE if i % 2 else LOVE for i in range(len(D1))]
TWO_SLIPS = [LOVE] * len(D1)
TWO_SLIPS[11] = TWO_SLIPS[18] = NTR          # can_tell + compliment
THREE_SLIPS = list(TWO_SLIPS)
THREE_SLIPS[12] = NTR                        # + private talk

# name, Day 1 prefs, Day 2 prefs, branch picks, expected (pressure, bedtime, Day 2 end, blend); None = any
PERSONAS = [
    ("pure Love", LOVE, LOVE, {}, ("mixed", True, "love", False)),
    ("Love + Exhibitionism", LE, LE, {}, ("nts_seeded", False, "exhibitionism", False)),
    ("Love with a playful edge", MIXED_D1, [("Love",)] + [LE] * 6, {}, ("mixed", None, "love", True)),
    ("Love, two slips on Day 1", TWO_SLIPS, LOVE, {}, ("mixed", False, "love", False)),
    ("three slips on Day 1, then Love", THREE_SLIPS, LOVE, {}, ("ntr_seeded", False, "love", False)),
    # Slow burn both ways: a loving Day 1 doesn't make Day 2 immune. Slipping on every
    # Day 2 answer (six slips) opens the NTR-risk lane; the sunset talk still repairs it.
    ("Love on Day 1, slips on half of Day 2", LOVE, [LOVE, NTR, LOVE, NTR, LOVE, NTR, LOVE], {},
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
                    self.assertEqual(d["temptation"], 1, cid)
                    self.assertGreaterEqual(min(d.get("love", 0), d.get("trust", 0)), -2, cid)
                    self.assertIn(tag(cid), ("May lead to NTR",), cid)

    def test_every_day1_and_day2_menu_offers_a_slip(self):
        # Principle 5: each scored menu has a believable slip, so stamps show a real spread.
        # Menus without one on purpose: the towel aside with Julian (Leia is off-screen).
        skip = {"ch01_towel_laugh"}
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


if __name__ == "__main__":
    unittest.main()
