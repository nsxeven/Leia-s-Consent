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

    def test_one_capped_suffix_shared_by_cards_and_colours(self):
        self.assertEqual(lc_stat_model.CAPPED_SUFFIX, " (capped)")
        self.assertFalse(hasattr(L, "capped_label"))
        src = _read("game/systems/choice_engine.rpy")
        self.assertIn("label += lc_stat_model.CAPPED_SUFFIX", src)
        self.assertNotIn('" (capped)"', src)


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
                                     log=self.logged.append, has_image=lambda n, exact=False: n.startswith("bg "),
                                     loadable=lambda p: p.startswith("images/"))
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
        self.assertIn("matrixcolor=lc_leia_box_matrix(theme)", say)

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


# ---------------------------------------------------------------- review fixes (PR #230)

def _dicts():
    return [
        {"id": "cafe", "label": "Café", "bg": "bg ch01_d2_cafe", "hint": "Cold and sweet.",
         "done": "Frappuccino: got it."},
        {"id": "shop", "label": "Resort shop", "bg": "bg ch01_shop_night", "hint": "Muffins."},
        {"id": "bar", "label": "Resort bar", "bg": "bg ch01_restaurant_bar", "locked": True,
         "locked_reason": "Not on day two."},
    ]


class PlaceInputTests(unittest.TestCase):
    """lc_leia_map / lc_leia_register_places take a list OR tuple of ids or place dicts."""

    def test_register_places_takes_a_list_or_a_tuple_of_dicts(self):
        for seq in (_dicts(), tuple(_dicts())):
            reg = {}
            L.register_places(reg, DAY, seq)
            self.assertEqual([p["id"] for p in L.places(reg, DAY)], ["cafe", "shop", "bar"])
            self.assertEqual(L.places(reg, DAY)[2]["locked_reason"], "Not on day two.")

    def test_register_places_rejects_a_single_dict_or_string(self):
        for bad in (_dicts()[0], "cafe", None, 3):
            with self.assertRaises(ValueError):
                L.register_places({}, DAY, bad)

    def test_place_dict_keys_are_checked(self):
        with self.assertRaisesRegex(ValueError, "unknown key"):
            L.register_places({}, DAY, [dict(_dicts()[0], colour="red")])
        with self.assertRaisesRegex(ValueError, "locked_reason"):
            L.register_places({}, DAY, [{"id": "bar", "label": "Bar", "bg": "bg x", "locked": True}])
        with self.assertRaisesRegex(ValueError, "missing"):
            L.register_places({}, DAY, [{"id": "cafe", "label": "Café", "hint": "x"}])
        with self.assertRaises(ValueError):   # an open place needs a hint
            L.register_places({}, DAY, [{"id": "cafe", "label": "Café", "bg": "bg x"}])

    def test_places_take_a_list_or_tuple_of_ids_or_the_registered_dicts(self):
        reg = {}
        L.register_places(reg, DAY, _dicts())
        for picked in (["shop", "cafe"], ("shop", "cafe"), [_dicts()[1], _dicts()[0]],
                       (_dicts()[1], "cafe")):
            self.assertEqual([p["id"] for p in L.places(reg, DAY, picked)], ["shop", "cafe"])

    def test_places_reject_strings_unregistered_and_differing_dicts(self):
        reg = {}
        L.register_places(reg, DAY, _dicts())
        with self.assertRaisesRegex(ValueError, "list/tuple"):
            L.places(reg, DAY, "cafe")
        with self.assertRaisesRegex(ValueError, "list/tuple"):
            L.places(reg, DAY, _dicts()[0])
        with self.assertRaisesRegex(ValueError, "lc_leia_register_places"):
            L.places(reg, DAY, [{"id": "pier", "label": "Pier", "bg": "bg x", "hint": "x"}])
        with self.assertRaisesRegex(ValueError, "differs"):
            L.places(reg, DAY, [dict(_dicts()[0], bg="ch01_d2_cafe")])

    def test_done_line_replaces_the_hint_once_visited(self):
        reg = {}
        L.register_places(reg, DAY, _dicts())
        cards = {c["id"]: c for c in L.cards(L.places(reg, DAY), ("cafe", "shop"), "full")}
        self.assertEqual(cards["cafe"]["hint"], "Frappuccino: got it.")
        self.assertEqual(cards["shop"]["hint"], "Muffins.")   # no done line: keeps its hint
        fresh = {c["id"]: c for c in L.cards(L.places(reg, DAY), (), "full")}
        self.assertEqual(fresh["cafe"]["hint"], "Cold and sweet.")


class PlaceImageTests(unittest.TestCase):
    def test_text_that_cannot_be_an_image_name_is_rejected_at_registration(self):
        with self.assertRaisesRegex(ValueError, "'shop'.*neither an image name"):
            L.register_place({}, DAY, "shop", "Shop", "ch01_shop_day_or_night (see C3)", "x")
        with self.assertRaises(ValueError):
            L.register_place({}, DAY, "shop", "Shop", "bg  double_space", "x")

    def test_bad_images_names_the_day_place_and_bg(self):
        reg = {}
        L.register_place(reg, DAY, "cafe", "Café", "ch01_d2_cafe", "x")       # tag left off
        L.register_place(reg, DAY, "shop", "Shop", "bg nowhere", "x")
        L.register_place(reg, DAY, "pier", "Pier", "images/missing.webp", "x")
        L.register_place(reg, DAY, "ok", "Ok", "bg ch01_d2_boutique", "x")
        defined = {"bg ch01_d2_cafe", "bg ch01_d2_boutique"}
        problems = L.bad_images(reg, defined.__contains__, lambda p: False)
        self.assertEqual(len(problems), 3)
        self.assertIn("ch01_d2/cafe: bg 'ch01_d2_cafe' is not a defined image (did you mean \"bg ch01_d2_cafe\"?)",
                      problems)
        self.assertIn("ch01_d2/shop: bg 'bg nowhere' is not a defined image", problems)
        self.assertIn("ch01_d2/pier: bg file 'images/missing.webp' is not loadable", problems)


class VisitOrderTests(unittest.TestCase):
    def setUp(self):
        self.places = _registry()[DAY]

    def _visit(self, *ids):
        state = {}
        for place_id in ids:
            state = L.visit(state, self.places, DAY, place_id)
        return state

    def test_visits_is_always_a_tuple(self):
        for state in (None, {}, self._visit("shop")):
            self.assertIsInstance(L.visits(state, DAY), tuple)
        self.assertNotEqual(L.visits(self._visit("shop"), DAY), ["shop"])   # why the helpers exist

    def test_first_visit_and_visited_first(self):
        self.assertIsNone(L.first_visit({}, DAY))
        self.assertFalse(L.visited_first({}, DAY, "shop"))
        state = self._visit("shop", "cafe")
        self.assertEqual(L.first_visit(state, DAY), "shop")
        self.assertTrue(L.visited_first(state, DAY, "shop"))
        self.assertFalse(L.visited_first(state, DAY, "cafe"))
        self.assertFalse(L.visited_first(state, "ch01_d3", "shop"))

    def test_visited_before(self):
        self.assertFalse(L.visited_before({}, DAY, "shop", "cafe"))
        only_shop = self._visit("shop")
        self.assertTrue(L.visited_before(only_shop, DAY, "shop", "cafe"))    # café not yet
        self.assertFalse(L.visited_before(only_shop, DAY, "cafe", "shop"))   # café not visited
        both = self._visit("cafe", "shop")
        self.assertTrue(L.visited_before(both, DAY, "cafe", "shop"))
        self.assertFalse(L.visited_before(both, DAY, "shop", "cafe"))

    def test_reset_day_keeps_every_other_day(self):
        state = self._visit("cafe")
        state = L.record_gain(state, DAY, "c_cafe", [("relationship", "love", 1)])
        state = L.record_gain(state, "dev_leia", "dev_x", [("relationship", "love", 2)])
        state = L.visit(state, self.places, "dev_leia", "shop")
        state = L.mark(L.mark(state, "dev_leia_told"), "ch01_d2_told")
        new = L.reset_day(state, "dev_leia", outcome_prefix="dev_leia_")
        self.assertEqual(L.visits(new, DAY), ("cafe",))
        self.assertEqual(L.gained(new, DAY), 1)
        self.assertEqual(L.visits(new, "dev_leia"), ())
        self.assertEqual(L.gained(new, "dev_leia"), 0)
        self.assertTrue(L.did(new, "ch01_d2_told"))
        self.assertFalse(L.did(new, "dev_leia_told"))
        self.assertEqual(L.visits(state, "dev_leia"), ("shop",))   # input untouched


class RuntimeReviewFixTests(unittest.TestCase):
    """The same production blocks as RuntimeTests, for the helpers added after review."""

    setUp = RuntimeTests.setUp
    call = RuntimeTests.call

    def test_visit_order_helpers(self):
        self.assertEqual(self.call("lc_leia_visits", DAY), ())
        self.assertIsNone(self.call("lc_leia_first", DAY))
        self.call("lc_leia_visit", DAY, "shop")
        self.assertIsInstance(self.call("lc_leia_visits", DAY), tuple)
        self.assertEqual(self.call("lc_leia_first", DAY), "shop")
        self.assertTrue(self.call("lc_leia_visited_first", DAY, "shop"))
        self.assertTrue(self.call("lc_leia_visited_before", DAY, "shop", "cafe"))
        self.call("lc_leia_visit", DAY, "cafe")
        self.assertFalse(self.call("lc_leia_visited_before", DAY, "cafe", "shop"))

    def test_place_helpers_reject_a_typo_in_developer_builds(self):
        self.assertFalse(self.call("lc_leia_visited_first", DAY, "shpo"))   # release: just False
        self.config.developer = True
        with self.assertRaisesRegex(Exception, "'shpo' is not registered"):
            self.call("lc_leia_visited_first", DAY, "shpo")
        with self.assertRaisesRegex(Exception, "not registered"):
            self.call("lc_leia_visited_before", DAY, "cafe", "pier")

    def test_map_takes_a_list_or_tuple_of_ids_or_dicts(self):
        self.screen_result = "shop"
        registered = [dict(e) for e in self.env["LC_LEIA_PLACES"][DAY]]
        as_dicts = [{k: e[k] for k in ("id", "label", "bg", "hint", "locked_reason")} for e in registered]
        for places in (["shop", "cafe"], ("shop", "cafe"), as_dicts, tuple(as_dicts)):
            self.screen_calls.clear()
            self.assertEqual(self.call("lc_leia_map", DAY, places), "shop")
            ids = [c["id"] for c in self.screen_calls[0][1]["cards"]]
            self.assertEqual(ids[:2], [p if isinstance(p, str) else p["id"] for p in places][:2])

    def test_map_with_a_bad_places_argument_is_a_clear_developer_error(self):
        self.screen_result = "shop"
        self.assertEqual(self.call("lc_leia_map", DAY, "cafe"), "shop")   # release: every place
        self.assertEqual([c["id"] for c in self.screen_calls[0][1]["cards"]], ["cafe", "shop", "bar"])
        self.config.developer = True
        with self.assertRaisesRegex(Exception, "list/tuple"):
            self.call("lc_leia_map", DAY, "cafe")
        with self.assertRaisesRegex(Exception, "lc_leia_register_places"):
            self.call("lc_leia_map", DAY, [{"id": "pier", "label": "Pier", "bg": "bg x", "hint": "x"}])

    def test_register_places_from_a_tuple_of_dicts(self):
        self.call("lc_leia_register_places", "ch01_d3", tuple(_dicts()))
        self.assertEqual([e["id"] for e in self.env["LC_LEIA_PLACES"]["ch01_d3"]], ["cafe", "shop", "bar"])
        self.assertEqual([e["id"] for e in self.discoveries["ch01_d3"]],
                         ["leia_ch01_d3_cafe", "leia_ch01_d3_shop"])
        with self.assertRaises(ValueError):
            self.call("lc_leia_register_places", "ch01_d4", _dicts()[0])

    def test_unknown_place_image_is_a_developer_error_naming_the_place(self):
        self.call("lc_leia_place", "ch01_d3", "cafe", "Café", "ch01_d2_cafe", "x")
        self.call("_lc_leia_validate_places")          # release: logged only
        self.assertTrue(any("ch01_d3/cafe" in m for m in self.logged))
        self.config.developer = True
        with self.assertRaisesRegex(Exception, r"ch01_d3/cafe: bg 'ch01_d2_cafe' is not a defined image "
                                               r"\(did you mean \"bg ch01_d2_cafe\"\?\)"):
            self.call("_lc_leia_validate_places")

    def test_validation_passes_for_defined_images_and_loadable_paths(self):
        self.config.developer = True
        self.call("_lc_leia_validate_places")   # setUp: "bg ..." names and an images/ path

    def test_validation_runs_at_init_999(self):
        src = _read("game/systems/leia_side.rpy")
        self.assertRegex(src, r"(?m)^init 999 python:\n    _lc_leia_validate_places\(\)")

    def test_review_clears_a_segment_a_scene_forgot_to_end(self):
        self.store.lc_leia_segment_day = DAY
        self.call("lc_hook_run", "review_finished", DAY)
        self.assertIsNone(self.store.lc_leia_segment_day)
        self.assertTrue(any("lc_leia_segment_end" in m for m in self.logged))
        self.store.lc_leia_segment_day = DAY
        self.config.developer = True
        with self.assertRaises(Exception):
            self.call("lc_hook_run", "review_finished", DAY)
        self.assertIsNone(self.store.lc_leia_segment_day)   # cleared before complaining
        self.store.lc_leia_segment_day = None
        self.call("lc_hook_run", "review_finished", DAY)     # nothing open: silent

    def test_strip_hides_errand_moments_until_she_went(self):
        items = [{"id": "leia_ch01_d2_cafe", "kind": "errand"}, {"id": "d2_door", "kind": "door"}]
        out = self.call("lc_hook_filter", "discovery_strip", items, DAY)
        self.assertEqual(out, [{"id": "d2_door", "kind": "door"}])
        self.call("lc_leia_visit", DAY, "cafe")
        self.assertEqual(self.call("lc_hook_filter", "discovery_strip", items, DAY), items)

    def test_box_matrix_lifts_the_night_paper(self):
        self.env["Matrix"] = lambda values: ("Matrix", tuple(values))
        self.env["TintMatrix"] = lambda colour: ("Tint", colour)
        kind, values = self.call("lc_leia_box_matrix", "night")
        self.assertEqual(kind, "Matrix")
        lift = (values[3], values[7], values[11])
        self.assertEqual(lift, self.env["LC_LEIA_NIGHT_LIFT"])
        self.assertTrue(all(v > 0 for v in lift) and lift[0] > lift[1])   # pink, never darker
        self.assertEqual(values[15], 1.0)
        self.assertEqual(self.call("lc_leia_box_matrix", "day"), ("Tint", "#ffe0ea"))


def _lane_env(ledger_rows, history):
    """Real lc_exhib_gained + ch01_d2_route_lane + the leia_side block, stats/story stubbed."""
    captured = {}
    effects = {
        "ch01_d2_errand_a": [("player", "exhibitionism", 1)],
        "ch01_d2_errand_b": [("player", "exhibitionism", 2)],
        "ch01_d2_confession_ask": [("relationship", "sharing", 1)],
        "ch01_d2_confession_protect": [("relationship", "love", 1), ("relationship", "trust", 1)],
        "ch01_d2_other": [("player", "exhibitionism", 1)],
    }
    state = {}
    for cid, applied in ledger_rows:
        state = L.record_gain(state, DAY, cid, applied)
    store = SimpleNamespace(choice_history=list(history), lc_leia_side_state=state,
                            lc_leia_segment_day=None)

    def d2_route_lane(stats, pressure, gained, focus=None, migrated_lane=None):
        captured.update(stats=stats, gained=gained)
        return "lane"

    env = {
        "renpy": SimpleNamespace(store=store, log=lambda m: None),
        "store": store, "config": SimpleNamespace(developer=True),
        "CHOICE_EFFECTS": effects,
        "get_choice_effects": lambda cid: list(effects[cid]),
        "lc_discovery_register": lambda *a, **kw: None, "lc_discovery_mark": lambda mid: None,
        "has_story_flag": lambda flag: False,
        "get_story_value": lambda key, default=None: default,
        "lc_stats_flat": lambda: {"exhibitionism": 10, "sharing": 5, "love": 50, "trust": 50},
        "lc_route_explorer_for_lane": lambda: None,
        "lc_stat_model": SimpleNamespace(d2_route_lane=d2_route_lane),
    }
    load_blocks(["lc_leia_visit"], env)
    env["lc_leia_register_choices"](DAY, "ch01_d2_errand_a", "ch01_d2_errand_b")
    load(["lc_exhib_gained", "ch01_d2_route_lane"], env)
    env["CH01_D2_LANE_EXEMPT_CHOICES"] = ("ch01_d2_knot_watch", "ch01_d2_errand_a", "ch01_d2_errand_b",
                                          "ch01_d2_confession_ask", "ch01_d2_confession_protect")
    return env, captured


class LaneExemptionTests(unittest.TestCase):
    """I3: the lane exemption and lc_exhib_gained use the same applied values, and Ryan's
    (uncapped) confession reply is still subtracted."""

    LEDGER = [("ch01_d2_errand_a", [("player", "exhibitionism", 1)]),
              ("ch01_d2_errand_b", [("player", "exhibitionism", 1)])]   # b was capped from +2
    HISTORY = ["ch01_d2_errand_a", "ch01_d2_errand_b", "ch01_d2_confession_ask", "ch01_d2_other"]

    def test_applied_effects_ledger_for_leia_registered_for_ryan(self):
        env, _c = _lane_env(self.LEDGER, self.HISTORY)
        f = env["lc_choice_applied_effects"]
        self.assertEqual(f("ch01_d2_errand_b"), [("player", "exhibitionism", 1)])     # capped value
        self.assertEqual(f("ch01_d2_confession_ask"), [("relationship", "sharing", 1)])  # Ryan: registered
        self.assertTrue(env["lc_leia_is_side_choice"]("ch01_d2_errand_a"))
        self.assertFalse(env["lc_leia_is_side_choice"]("ch01_d2_confession_ask"))
        # the trap the docs warned about: her ledger knows nothing of Ryan's reply
        self.assertEqual(env["lc_leia_applied_effects"]("ch01_d2_confession_ask"), [])

    def test_exhib_gained_counts_what_really_landed(self):
        env, _c = _lane_env(self.LEDGER, self.HISTORY)
        self.assertEqual(env["lc_exhib_gained"]("ch01_d2_"), 1 + 1 + 1)   # not 1 + 2 + 1

    def test_a_leia_choice_in_history_twice_counts_once(self):
        env, _c = _lane_env(self.LEDGER, self.HISTORY + ["ch01_d2_errand_a"])
        self.assertEqual(env["lc_exhib_gained"]("ch01_d2_"), 3)

    def test_lane_subtracts_applied_leia_values_and_ryans_reply(self):
        env, captured = _lane_env(self.LEDGER, self.HISTORY)
        env["ch01_d2_route_lane"]()
        # exhibitionism 10 - 1 - 1 (her two applied gains); sharing 5 - 1 (Ryan's reply, uncapped)
        self.assertEqual(captured["stats"]["exhibitionism"], 8)
        self.assertEqual(captured["stats"]["sharing"], 4)
        self.assertEqual(captured["stats"]["love"], 50)   # protect reply not picked: untouched
        # gained today (3) minus her exempt exhibitionism (2): only Ryan's other choice counts
        self.assertEqual(captured["gained"], 1)

    def test_ryan_protect_reply_is_subtracted_in_full(self):
        env, captured = _lane_env(self.LEDGER, ["ch01_d2_confession_protect"])
        env["ch01_d2_route_lane"]()
        self.assertEqual(captured["stats"]["love"], 49)
        self.assertEqual(captured["stats"]["trust"], 49)


def _game_rpy():
    return [p for p in (ROOT / "game").rglob("*.rpy")]


class MisuseGuardTests(unittest.TestCase):
    """Source guards so a story file can't use the API in the ways the review found."""

    def test_segment_labels_are_called_not_run_as_python(self):
        bad = []
        for path in _game_rpy():
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith("#"):
                    continue
                if re.search(r"(?:\$|^\s*python:?).*\blc_leia_segment_(?:begin|end)\s*\(", line) or \
                        re.search(r"^\s*\$\s*lc_leia_segment_(?:begin|end)\b", line):
                    bad.append("%s:%d" % (path.relative_to(ROOT), n))
        self.assertEqual(bad, [], "use `call lc_leia_segment_begin(...) from ...` / `call lc_leia_segment_end`")

    def test_visits_are_never_compared_with_a_list(self):
        bad = []
        for path in _game_rpy():
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if re.search(r"lc_leia_visits\([^)]*\)\s*[!=]=\s*\[", line):
                    bad.append("%s:%d" % (path.relative_to(ROOT), n))
        self.assertEqual(bad, [], "lc_leia_visits returns a tuple: use lc_leia_visited_first/_before")

    def test_every_registered_place_bg_is_a_defined_image(self):
        images = set()
        for path in _game_rpy():
            images |= set(re.findall(r"(?m)^\s*image ([A-Za-z0-9_ ]+?)\s*[=:]", path.read_text(encoding="utf-8")))
        bgs = []
        for path in _game_rpy():
            src = path.read_text(encoding="utf-8")
            bgs += re.findall(r'lc_leia_place\(\s*"[^"]*",\s*"[^"]*",\s*"[^"]*",\s*"([^"]+)"', src)
            if "lc_leia_register_places(" in src:
                bgs += re.findall(r'"bg":\s*"([^"]+)"', src)
        self.assertTrue(bgs)   # the developer demo registers four
        for bg in bgs:
            if L.is_image_name(bg):
                self.assertTrue(bg in images, "lc_leia_place bg %r is not an image defined in game/" % bg)
            else:
                self.assertTrue((ROOT / "game" / bg).exists(), bg)

    def test_map_sits_under_the_quick_menu(self):
        def zorder(src, screen):
            block = src[src.index("\nscreen %s(" % screen):]  # the definition, not a header line
            return int(re.search(r"(?m)^\s+zorder (\d+)", block).group(1))
        self.assertLess(zorder(_read("game/screens/leia_map_screen.rpy"), "lc_leia_map_screen"),
                        zorder(_read("game/screens/quick_menu.rpy"), "quick_menu"))

    def test_day_two_lane_subtracts_applied_effects(self):
        src = _read("game/chapters/ch01/day2/ch01_day2_registrations.rpy")
        lane = src[src.index("def ch01_d2_route_lane():"):]
        lane = lane[:lane.index("return lc_stat_model.d2_route_lane(")]
        self.assertIn("lc_choice_applied_effects(exempt_id)", lane)
        self.assertNotIn("get_choice_effects(", lane)
        stats = _read("game/systems/stats.rpy")
        exhib = stats[stats.index("def lc_exhib_gained(prefix):"):stats.index("def lc_current_lean")]
        self.assertIn("lc_choice_applied_effects(choice_id)", exhib)

    def test_docs_show_the_call_form_and_the_helpers(self):
        doc = _read("docs/LEIA_SIDE.md")
        self.assertIn('call lc_leia_segment_begin("ch01_d2") from d2_errand_begin', doc)
        self.assertIn("call lc_leia_segment_end from d2_errand_end", doc)
        self.assertIn("lc_leia_visited_first(", doc)
        self.assertIn("lc_choice_applied_effects", doc)
        self.assertIn("confession", doc)


if __name__ == "__main__":
    unittest.main()
