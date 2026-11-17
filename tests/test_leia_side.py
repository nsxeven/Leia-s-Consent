"""Leia's side: the errand map, the visit log, named outcomes and the +2/day gain cap.

Pure rules: game/python-packages/lc_leia_side.py. Ren'Py side: game/systems/leia_side.rpy
(store binding, choice-effect hooks, segment frame), the map screen in
game/screens/leia_map_screen.rpy, and the hook points in game/systems/choice_engine.rpy
(choice_effects filter, choice_applied run). Docs: docs/LEIA_SIDE.md.
"""
import pickle
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_discovery  # noqa: E402
import lc_leia_side as L  # noqa: E402
import lc_stat_model  # noqa: E402
import lc_ui_logic  # noqa: E402
from lc_rpy_harness import load, load_blocks  # noqa: E402

DAY = "ch01_d2"


def _registry():
    reg = {}
    L.register_place(reg, DAY, "cafe", "Cafe", "bg cafe", "His frappuccino.")
    L.register_place(reg, DAY, "shop", "Resort shop", "bg shop", "Chocolate muffins.")
    L.register_place(reg, DAY, "bar", "Resort bar", "bg bar", "Cocktails.",
                     locked_reason="A bar, on my own, at four in the afternoon?")
    L.register_place(reg, DAY, "boutique", "Boutique", "bg boutique", "Clothes.",
                     locked_reason="I've had enough of that boutique for one day.")
    return reg


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class RegisterPlaceTests(unittest.TestCase):
    def test_places_keep_registration_order_per_day(self):
        reg = _registry()
        self.assertEqual([p["id"] for p in L.places(reg, DAY)], ["cafe", "shop", "bar", "boutique"])
        self.assertEqual(L.places(reg, "other_day"), [])

    def test_places_can_be_picked_and_ordered_by_id(self):
        reg = _registry()
        self.assertEqual([p["id"] for p in L.places(reg, DAY, ["shop", "cafe"])], ["shop", "cafe"])
        with self.assertRaises(ValueError):
            L.places(reg, DAY, ["cafe", "nowhere"])

    def test_bad_registrations_are_rejected(self):
        reg = _registry()
        with self.assertRaises(ValueError):
            L.register_place(reg, DAY, "cafe", "Again", "bg x", "dup")
        with self.assertRaises(ValueError):
            L.register_place(reg, DAY, "", "Empty", "bg x", "hint")
        with self.assertRaises(ValueError):
            L.register_place(reg, DAY, "x", "", "bg x", "hint")
        with self.assertRaises(ValueError):
            L.register_place(reg, DAY, "x", "Label", "", "hint")
        with self.assertRaises(ValueError):
            L.register_place(reg, DAY, "x", "Label", "bg x", "hint", locked_reason="   ")

    def test_a_map_holds_at_most_four_places(self):
        reg = _registry()
        with self.assertRaises(ValueError):
            L.register_place(reg, DAY, "fifth", "Fifth", "bg x", "One too many.")
        self.assertEqual(len(L.places(reg, DAY)), L.MAX_PLACES)

    def test_moment_ids_are_stable_and_per_day(self):
        self.assertEqual(L.moment_id(DAY, "cafe"), "leia_ch01_d2_cafe")
        self.assertNotEqual(L.moment_id("ch01_d3", "cafe"), L.moment_id(DAY, "cafe"))


class CardTests(unittest.TestCase):
    def setUp(self):
        self.places = L.places(_registry(), DAY)

    def by_id(self, cards):
        return {c["id"]: c for c in cards}

    def test_states_open_visited_locked(self):
        cards = self.by_id(L.cards(self.places, ("cafe",), "normal"))
        self.assertEqual(cards["cafe"]["state"], "visited")
        self.assertEqual(cards["shop"]["state"], "open")
        self.assertEqual(cards["bar"]["state"], "locked")
        self.assertEqual([c["id"] for c in L.cards(self.places, (), "normal")],
                         ["cafe", "shop", "bar", "boutique"])

    def test_only_open_cards_can_be_activated(self):
        cards = self.by_id(L.cards(self.places, ("cafe",), "full"))
        self.assertTrue(cards["shop"]["activatable"])
        self.assertFalse(cards["cafe"]["activatable"])
        self.assertFalse(cards["bar"]["activatable"])

    def test_locked_reason_shows_in_every_mode(self):
        for mode in ("normal", "insight", "full", "developer"):
            bar = self.by_id(L.cards(self.places, (), mode))["bar"]
            self.assertIn("four in the afternoon", bar["reason"], mode)

    def test_later_day_hint_only_in_insight_full_and_developer(self):
        self.assertIsNone(self.by_id(L.cards(self.places, (), "normal"))["bar"]["lock_hint"])
        for mode in ("insight", "full", "developer"):
            self.assertEqual(self.by_id(L.cards(self.places, (), mode))["bar"]["lock_hint"],
                             "Opens on a later day.", mode)
        self.assertIsNone(self.by_id(L.cards(self.places, (), "full"))["shop"]["lock_hint"])
        self.assertIsNone(self.by_id(L.cards(self.places, (), "full"))["shop"]["reason"])

    def test_lock_hint_rule(self):
        self.assertEqual(L.lock_hint("locked", "full"), L.LATER_DAY_HINT)
        self.assertIsNone(L.lock_hint("locked", "normal"))
        self.assertIsNone(L.lock_hint("open", "full"))

    def test_old_save_visit_log_none_reads_all_open(self):
        states = [c["state"] for c in L.cards(self.places, None, "normal")]
        self.assertEqual(states, ["open", "open", "locked", "locked"])


class VisitTests(unittest.TestCase):
    def setUp(self):
        self.places = L.places(_registry(), DAY)

    def test_player_chosen_order_is_recorded(self):
        state = L.visit({}, self.places, DAY, "shop")
        state = L.visit(state, self.places, DAY, "cafe")
        self.assertEqual(L.visits(state, DAY), ("shop", "cafe"))
        self.assertEqual(L.visits(state, "ch01_d3"), ())

    def test_remaining_and_done(self):
        self.assertEqual(L.open_remaining(self.places, ()), ["cafe", "shop"])
        state = L.visit({}, self.places, DAY, "cafe")
        self.assertEqual(L.open_remaining(self.places, L.visits(state, DAY)), ["shop"])
        self.assertFalse(L.errand_done(self.places, L.visits(state, DAY)))
        state = L.visit(state, self.places, DAY, "shop")
        self.assertTrue(L.errand_done(self.places, L.visits(state, DAY)))

    def test_locked_or_unknown_places_cannot_be_visited(self):
        for place in ("bar", "boutique", "nowhere"):
            with self.assertRaises(ValueError, msg=place):
                L.visit({}, self.places, DAY, place)

    def test_visiting_twice_changes_nothing(self):
        state = L.visit({}, self.places, DAY, "cafe")
        self.assertIs(L.visit(state, self.places, DAY, "cafe"), state)

    def test_state_is_never_mutated_in_place(self):
        """Rollback restores the store's reference; old states must stay as they were."""
        empty = {}
        first = L.visit(empty, self.places, DAY, "cafe")
        second = L.visit(first, self.places, DAY, "shop")
        self.assertEqual(empty, {})
        self.assertEqual(L.visits(first, DAY), ("cafe",))
        self.assertEqual(L.visits(second, DAY), ("cafe", "shop"))
        marked = L.mark(second, "d2_cafe_thanked")
        self.assertFalse(L.did(second, "d2_cafe_thanked"))
        self.assertTrue(L.did(marked, "d2_cafe_thanked"))

    def test_old_save_state_none_reads_as_nothing_happened(self):
        self.assertEqual(L.visits(None, DAY), ())
        self.assertFalse(L.did(None, "anything"))
        self.assertEqual(L.gained(None, DAY), 0)
        self.assertEqual(L.visits(L.visit(None, self.places, DAY, "cafe"), DAY), ("cafe",))

    def test_state_survives_a_save_round_trip(self):
        state = L.visit({}, self.places, DAY, "cafe")
        state = L.mark(state, "d2_cafe_thanked")
        state = L.record_gain(state, DAY, "c1", [("relationship", "love", 1)])
        restored = pickle.loads(pickle.dumps(state))
        self.assertEqual(L.visits(restored, DAY), ("cafe",))
        self.assertTrue(L.did(restored, "d2_cafe_thanked"))
        self.assertEqual(L.gained(restored, DAY), 1)


class OutcomeTests(unittest.TestCase):
    def test_mark_is_idempotent(self):
        state = L.mark({}, "d2_shop_told_owner")
        self.assertIs(L.mark(state, "d2_shop_told_owner"), state)
        self.assertTrue(L.did(state, "d2_shop_told_owner"))
        self.assertFalse(L.did(state, "d2_shop_kept_quiet"))

    def test_outcome_ids_must_be_plain_ids(self):
        for bad in ("", "has space", None):
            with self.assertRaises(ValueError, msg=repr(bad)):
                L.mark({}, bad)


class CapLedgerTests(unittest.TestCase):
    LOVE = [("relationship", "love", 1)]
    LOVE_TRUST = [("relationship", "love", 1), ("relationship", "trust", 1)]

    def test_daily_cap_is_two(self):
        self.assertEqual(L.DAILY_GAIN_CAP, 2)

    def test_gains_pass_until_the_cap_then_clamp_to_zero(self):
        state = {}
        self.assertEqual(L.cap_effects(state, DAY, self.LOVE_TRUST), self.LOVE_TRUST)
        state = L.record_gain(state, DAY, "a", self.LOVE_TRUST)
        self.assertEqual(L.gained(state, DAY), 2)
        self.assertEqual(L.cap_effects(state, DAY, self.LOVE), [("relationship", "love", 0)])

    def test_partial_allowance_is_spent_in_effect_order(self):
        state = L.record_gain({}, DAY, "a", self.LOVE)
        self.assertEqual(L.cap_effects(state, DAY, self.LOVE_TRUST),
                         [("relationship", "love", 1), ("relationship", "trust", 0)])
        self.assertEqual(L.cap_effects({}, DAY, [("partner", "exhibitionism", 3)]),
                         [("partner", "exhibitionism", 2)])

    def test_losses_are_never_capped_and_do_not_refund(self):
        state = L.record_gain({}, DAY, "a", self.LOVE_TRUST)
        effects = [("relationship", "temptation", -1), ("relationship", "love", 1)]
        self.assertEqual(L.cap_effects(state, DAY, effects),
                         [("relationship", "temptation", -1), ("relationship", "love", 0)])
        state = L.record_gain(state, DAY, "b", [("relationship", "temptation", -1)])
        self.assertEqual(L.gained(state, DAY), 2)

    def test_cap_is_per_day(self):
        state = L.record_gain({}, DAY, "a", self.LOVE_TRUST)
        self.assertEqual(L.cap_effects(state, "ch01_d3", self.LOVE), self.LOVE)

    def test_record_gain_never_exceeds_the_cap_and_keeps_the_input(self):
        empty = {}
        state = L.record_gain(empty, DAY, "a", self.LOVE)
        self.assertEqual(empty, {})
        self.assertEqual(L.gained(state, DAY), 1)

    def test_applied_effects_sum_what_actually_landed(self):
        state = L.record_gain({}, DAY, "a", self.LOVE)
        state = L.record_gain(state, DAY, "b", [("relationship", "love", 1), ("relationship", "trust", 0)])
        self.assertEqual(L.applied_effects(state, "b"),
                         [("relationship", "love", 1), ("relationship", "trust", 0)])
        self.assertEqual(L.applied_effects(state, "a"), [("relationship", "love", 1)])
        self.assertEqual(L.applied_effects(state, "never"), [])
        self.assertEqual(L.applied_effects(None, "a"), [])

    def test_cap_effects_keeps_shape_and_input(self):
        effects = list(self.LOVE_TRUST)
        state = L.record_gain({}, DAY, "a", self.LOVE_TRUST)
        out = L.cap_effects(state, DAY, effects)
        self.assertEqual(len(out), len(effects))
        self.assertEqual(effects, self.LOVE_TRUST)


class CappedLabelTests(unittest.TestCase):
    def test_capped_label_keeps_the_stat_colour(self):
        self.assertEqual(lc_stat_model.stat_id_for_label("Love (capped)"), "love")
        self.assertEqual(lc_stat_model.stat_id_for_label("Temptation (capped)"), "temptation")
        self.assertEqual(lc_stat_model.stat_id_for_label("Love"), "love")

    def test_capped_label_text(self):
        self.assertEqual(L.capped_label("Love"), "Love (capped)")


class RuntimeTests(unittest.TestCase):
    """The production init block of game/systems/leia_side.rpy with engine boundaries stubbed."""

    def setUp(self):
        self.marked = []
        self.screen_calls = []
        self.screen_result = None
        self.logged = []
        self.store = SimpleNamespace(lc_leia_side_state={}, lc_leia_segment_day=None)
        self.config = SimpleNamespace(developer=False)
        self.mode = "normal"
        test = self

        def call_screen(name, **kw):
            test.screen_calls.append((name, kw))
            return test.screen_result

        self.renpy = SimpleNamespace(store=self.store, call_screen=call_screen,
                                     log=self.logged.append, has_image=lambda n, exact=False: n.startswith("bg "))
        self.discoveries = {}
        self.env = dict(
            store=self.store, renpy=self.renpy, config=self.config,
            current_choice_mode=lambda: test.mode,
            lc_discovery_register=lambda day, mid, kind, label, mood, image=None:
                lc_discovery.register(self.discoveries, day, mid, kind, label, mood, image=image),
            lc_discovery_mark=self.marked.append,
        )
        load_blocks(["lc_leia_visit"], self.env)
        for args, kw in (((DAY, "cafe", "Cafe", "bg ch01_d2_cafe", "His frappuccino."), {}),
                         ((DAY, "shop", "Resort shop", "images/x/shop.webp", "Muffins."), {}),
                         ((DAY, "bar", "Resort bar", "bg ch01_restaurant_bar", "Cocktails."),
                          {"locked_reason": "Not on day two."})):
            self.call("lc_leia_place", *args, **kw)
        self.call("lc_leia_register_choices", DAY, "c_cafe", "c_shop", "c_walk")

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def test_open_places_register_a_moment_and_locked_ones_do_not(self):
        ids = [e["id"] for e in self.discoveries[DAY]]
        self.assertEqual(ids, ["leia_ch01_d2_cafe", "leia_ch01_d2_shop"])
        kinds = {e["kind"] for e in self.discoveries[DAY]}
        self.assertEqual(kinds, {"errand"})
        images = {e["id"]: e["image"] for e in self.discoveries[DAY]}
        self.assertEqual(images["leia_ch01_d2_cafe"], "bg ch01_d2_cafe")
        self.assertIsNone(images["leia_ch01_d2_shop"])  # a file path is not an image name

    def test_visit_records_order_and_marks_the_moment(self):
        self.call("lc_leia_visit", DAY, "shop")
        self.call("lc_leia_visit", DAY, "cafe")
        self.assertEqual(self.call("lc_leia_visits", DAY), ("shop", "cafe"))
        self.assertEqual(self.marked, ["leia_ch01_d2_shop", "leia_ch01_d2_cafe"])

    def test_visiting_a_locked_place_raises_in_developer_and_is_ignored_in_release(self):
        self.call("lc_leia_visit", DAY, "bar")
        self.assertEqual(self.call("lc_leia_visits", DAY), ())
        self.assertEqual(self.marked, [])
        self.config.developer = True
        with self.assertRaises(Exception):
            self.call("lc_leia_visit", DAY, "bar")

    def test_rollback_restores_visits_outcomes_and_cap(self):
        before = self.store.lc_leia_side_state
        self.call("lc_leia_visit", DAY, "cafe")
        self.call("lc_leia_mark", "d2_cafe_thanked")
        self.call("_lc_leia_choice_applied", "c_cafe", [("relationship", "love", 1)])
        self.assertTrue(self.call("lc_leia_did", "d2_cafe_thanked"))
        self.store.lc_leia_side_state = before   # what Ren'Py rollback does to the store
        self.assertEqual(self.call("lc_leia_visits", DAY), ())
        self.assertFalse(self.call("lc_leia_did", "d2_cafe_thanked"))
        self.assertEqual(self.call("lc_leia_cap_effects", DAY, [("relationship", "love", 2)]),
                         [("relationship", "love", 2)])

    def test_old_save_without_the_state_reads_empty(self):
        del self.store.lc_leia_side_state
        del self.store.lc_leia_segment_day
        self.assertEqual(self.call("lc_leia_visits", DAY), ())
        self.assertFalse(self.call("lc_leia_did", "x"))
        self.assertFalse(self.call("lc_leia_segment_active"))
        self.call("lc_leia_visit", DAY, "cafe")
        self.assertEqual(self.call("lc_leia_visits", DAY), ("cafe",))

    def test_choice_effects_filter_caps_only_registered_leia_choices(self):
        f = self.env["_lc_leia_choice_effects"]
        two = [("relationship", "love", 1), ("relationship", "trust", 1)]
        self.assertEqual(f(two, "c_cafe"), two)
        self.call("_lc_leia_choice_applied", "c_cafe", two)
        self.assertEqual(f([("relationship", "love", 1)], "c_shop"), [("relationship", "love", 0)])
        self.assertEqual(f([("relationship", "love", 1)], "ch01_d2_morning_reassure"),
                         [("relationship", "love", 1)])
        self.call("_lc_leia_choice_applied", "ch01_d2_morning_reassure", [("relationship", "love", 1)])
        self.assertEqual(self.call("lc_leia_applied_effects", "ch01_d2_morning_reassure"), [])
        self.assertEqual(self.call("lc_leia_applied_effects", "c_cafe"), two)

    def test_a_choice_registered_twice_for_different_days_is_rejected(self):
        with self.assertRaises(ValueError):
            self.call("lc_leia_register_choices", "ch01_d3", "c_cafe")

    def test_map_returns_none_without_a_screen_when_nothing_is_open(self):
        self.call("lc_leia_visit", DAY, "cafe")
        self.call("lc_leia_visit", DAY, "shop")
        self.assertTrue(self.call("lc_leia_errand_done", DAY))
        self.assertIsNone(self.call("lc_leia_map", DAY))
        self.assertEqual(self.screen_calls, [])

    def test_map_shows_the_cards_and_returns_the_pick(self):
        self.mode = "full"
        self.call("lc_leia_visit", DAY, "cafe")
        self.screen_result = "shop"
        self.assertEqual(self.call("lc_leia_map", DAY), "shop")
        name, kw = self.screen_calls[0]
        self.assertEqual(name, "lc_leia_map_screen")
        states = [(c["id"], c["state"], c["lock_hint"]) for c in kw["cards"]]
        self.assertEqual(states, [("cafe", "visited", None), ("shop", "open", None),
                                  ("bar", "locked", "Opens on a later day.")])

    def test_map_never_returns_a_closed_place(self):
        self.screen_result = "bar"
        self.assertIsNone(self.call("lc_leia_map", DAY))
        self.config.developer = True
        with self.assertRaises(Exception):
            self.call("lc_leia_map", DAY)

    def test_segment_flag(self):
        self.assertFalse(self.call("lc_leia_segment_active"))
        self.store.lc_leia_segment_day = DAY
        self.assertTrue(self.call("lc_leia_segment_active"))


def _choice_env(mode, leia_state):
    """format_choice / _choice_effect_text / apply_choice from choice_engine.rpy with the real
    Leia-side filter wired through real lc_hooks."""
    applied = []
    store = SimpleNamespace(persistent=SimpleNamespace(choice_display_mode=mode),
                            choice_history=[], last_choice_id=None,
                            lc_leia_side_state=leia_state, lc_leia_segment_day=None)
    env = {
        "renpy": SimpleNamespace(store=store, call_screen=None, log=lambda m: None,
                                 has_image=lambda n, exact=False: False),
        "store": store, "config": SimpleNamespace(developer=True),
        "lc_stat_model": lc_stat_model, "lc_ui_logic": lc_ui_logic,
        "CHOICE_EFFECTS": {"c_cafe": [("relationship", "love", 1), ("relationship", "trust", 1)],
                           "c_shop": [("relationship", "love", 1)],
                           "c_ryan": [("relationship", "love", 1)]},
        "lc_choice_route_tag": lambda cid: "Love",
        "get_choice_tags": lambda cid: (),
        "change_stat": lambda g, s, a: applied.append((g, s, a)),
        "lc_review_stats": lambda: (),
        "lc_review_note_choice": lambda cid, before: None,
        "maybe_show_status_choice_tutorial": lambda cid: None,
        "current_choice_mode": lambda: store.persistent.choice_display_mode,
        "lc_discovery_register": lambda *a, **kw: None,
        "lc_discovery_mark": lambda mid: None,
    }
    feedback = []
    env["show_choice_feedback"] = lambda cid, effects=None: feedback.append((cid, effects))
    load(["_lc_hooks", "lc_hook_add", "lc_hook_run", "lc_hook_filter", "CHOICE_MODES", "STAT_LABELS",
          "get_choice_effects", "lc_choice_effective_effects", "_choice_effect_text", "format_choice",
          "apply_choice"], env)
    load_blocks(["lc_leia_visit"], env)
    env["lc_leia_register_choices"](DAY, "c_cafe", "c_shop")
    return env, applied, feedback


class ChoiceEngineIntegrationTests(unittest.TestCase):
    def test_uncapped_leia_choice_reads_like_any_choice(self):
        env, _a, _f = _choice_env("full", {})
        _line, chips = lc_ui_logic.parse_choice_caption(env["format_choice"]("c_cafe", "Thank him"))
        self.assertEqual(chips, [("Love", 1, True), ("Trust", 1, True)])

    def test_capped_gain_is_labelled_truthfully_in_full_and_insight(self):
        spent = L.record_gain({}, DAY, "earlier", [("relationship", "love", 2)])
        env, _a, _f = _choice_env("full", spent)
        caption = env["format_choice"]("c_shop", "Tell her")
        _line, chips = lc_ui_logic.parse_choice_caption(caption)
        self.assertEqual(chips, [("Love (capped)", 0, True)])
        env, _a, _f = _choice_env("insight", spent)
        _line, chips = lc_ui_logic.parse_choice_caption(env["format_choice"]("c_shop", "Tell her"))
        self.assertEqual(chips, [("Love (capped)", 0, False)])
        env, _a, _f = _choice_env("normal", spent)
        self.assertEqual(env["format_choice"]("c_shop", "Tell her"), "Tell her")

    def test_ryan_choices_are_never_capped(self):
        spent = L.record_gain({}, DAY, "earlier", [("relationship", "love", 2)])
        env, applied, _f = _choice_env("full", spent)
        _line, chips = lc_ui_logic.parse_choice_caption(env["format_choice"]("c_ryan", "x"))
        self.assertEqual(chips, [("Love", 1, True)])
        env["apply_choice"]("c_ryan")
        self.assertEqual(applied, [("relationship", "love", 1)])

    def test_apply_choice_applies_the_capped_effects_and_records_them(self):
        env, applied, feedback = _choice_env("full", {})
        env["apply_choice"]("c_cafe")
        env["apply_choice"]("c_shop")
        self.assertEqual(applied, [("relationship", "love", 1), ("relationship", "trust", 1),
                                   ("relationship", "love", 0)])
        self.assertEqual(feedback[-1], ("c_shop", [("relationship", "love", 0)]))
        state = env["store"].lc_leia_side_state
        self.assertEqual(L.gained(state, DAY), 2)
        # the toast text is built from what was applied, so it can't disagree with the stats
        self.assertEqual(env["_choice_effect_text"]("c_shop", exact=True, effects=feedback[-1][1]),
                         "Love (capped) +0")


class ToastChipTests(unittest.TestCase):
    """The post-choice toast must not read a capped +0 as a loss."""

    def test_toast_parses_a_capped_insight_chip(self):
        env = load(["lc_effect_chips"], {})
        self.assertEqual(env["lc_effect_chips"]("Love (capped) \u2192"), [("Love (capped)", 0, False)])
        self.assertEqual(env["lc_effect_chips"]("Love \u2191 \u2022 Trust (capped) +0"),
                         [("Love", 1, False), ("Trust (capped)", 0, True)])

    def test_a_zero_chip_is_drawn_neutral(self):
        src = _read("game/screens/scrapbook_ui.rpy")
        chip = src[src.index("\nscreen lc_chip("):src.index("\nscreen lc_keycap_button(")]
        self.assertIn("flat = amount == 0", chip)
        self.assertIn("gui/scrapbook/frame_paper.png", chip)
        self.assertIn("if not flat:", chip)


class SourceContractTests(unittest.TestCase):
    def test_choice_engine_has_the_two_hook_points(self):
        src = _read("game/systems/choice_engine.rpy")
        self.assertIn('lc_hook_filter("choice_effects"', src)
        self.assertIn('lc_hook_run("choice_applied"', src)

    def test_hooks_are_registered_in_the_leia_side_file(self):
        src = _read("game/systems/leia_side.rpy")
        self.assertIn('lc_hook_add("choice_effects", _lc_leia_choice_effects)', src)
        self.assertIn('lc_hook_add("choice_applied", _lc_leia_choice_applied)', src)

    def test_state_is_save_local_with_defaults(self):
        src = _read("game/systems/leia_side.rpy")
        self.assertRegex(src, r"(?m)^default lc_leia_side_state = \{\}")
        self.assertRegex(src, r"(?m)^default lc_leia_segment_day = None")

    def test_leia_think_is_styled_like_ryans_think(self):
        src = _read("game/characters.rpy")
        self.assertRegex(src, r"(?m)^define leia_think = Character\(None, show_think=True\)")

    def test_segment_title_card_names_her_by_the_typed_name(self):
        self.assertEqual(L.TITLE_CARD, "Meanwhile \u2014 [girlfriend_name]")
        src = _read("game/systems/leia_side.rpy")
        self.assertIn("label lc_leia_segment_begin(day):", src)
        self.assertIn('centered "%s"' % L.TITLE_CARD, src)
        self.assertIn("label lc_leia_segment_end:", src)

    def test_say_box_is_tinted_during_her_segment(self):
        src = _read("game/screens/scrapbook_ui.rpy")
        say = src[src.index("screen say(who, what, think=False):"):src.index("transform lc_input_bg_in")]
        self.assertIn("lc_leia_segment_active()", say)
        self.assertIn("LC_LEIA_BOX_TINT", say)

    def test_errand_kind_is_a_discovery_kind(self):
        self.assertIn("errand", lc_discovery.KINDS)
        self.assertFalse(lc_discovery.has_route_words(lc_discovery.KIND_LABELS["errand"]))


class MapScreenTests(unittest.TestCase):
    def setUp(self):
        self.src = _read("game/screens/leia_map_screen.rpy")

    def test_screen_signature(self):
        self.assertIn("screen lc_leia_map_screen(day, cards):", self.src)

    def test_locked_and_visited_cards_focus_but_do_not_activate(self):
        self.assertIn("NullAction()", self.src)
        self.assertIn('Return(card["id"])', self.src)
        self.assertRegex(self.src, r'card\["activatable"\]')

    def test_no_invisible_full_screen_button(self):
        self.assertNotRegex(self.src, r"(?m)^\s*(?:text|image)?button:\s*\n(?:\s+.*\n){0,3}\s+(?:xfill|yfill) True")
        self.assertNotIn("Return()", self.src)   # no dismiss: she visits every open place
        self.assertIn("modal True", self.src)

    def test_scrapbook_look_and_reduced_motion(self):
        for needed in ("gui/scrapbook/frame_choice.png", "gui/scrapbook/frame_kraft.png",
                       "fonts/Handjet-ExtraBold.ttf", "fonts/PatrickHand-Regular.ttf",
                       "lc_pov_reduce_motion()", "lc_ui_play"):
            self.assertIn(needed, self.src, needed)

    def test_reason_and_hint_are_drawn(self):
        self.assertIn('card["reason"]', self.src)
        # the hint follows the live mode, so switching mode with the map open updates it
        self.assertIn('lc_leia_side.lock_hint(card["state"], current_choice_mode())', self.src)
        self.assertIn('card["hint"]', self.src)

    def test_keyboard_number_keys_only_pick_open_cards(self):
        self.assertRegex(self.src, r'key "K_%d" % \(i \+ 1\) action Return\(card\["id"\]\)')


class DevDemoTests(unittest.TestCase):
    def test_demo_is_developer_only_and_uses_the_four_backgrounds(self):
        src = _read("game/dev/dev_leia_side.rpy")
        self.assertIn("config.developer", src)
        for bg in ("bg ch01_d2_cafe", "bg ch01_shop_night", "bg ch01_restaurant_bar", "bg ch01_d2_boutique"):
            self.assertIn(bg, src)
        self.assertEqual(len(re.findall(r"locked_reason=", src)), 2)
        self.assertIn("call lc_leia_segment_begin(", src)
        self.assertIn("leia_think", src)
        self.assertIn("lc_leia_map(", src)
        menu = _read("game/dev/dev_systems_menu_screen.rpy")
        self.assertIn('Return("leia_side")', menu)


if __name__ == "__main__":
    unittest.main()
