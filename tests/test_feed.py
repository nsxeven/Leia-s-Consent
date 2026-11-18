"""The social-feed phone app (placeholder name LC_FEED_APP_NAME = "Instababe").

Pure rules: game/python-packages/lc_feed.py (registry checks, release batches and unlock gates,
ordering, the save-local seen/opened records, badge, stamps, reactions, scroll-to-focus maths).
Ren'Py side: game/systems/feed.rpy (store state, API, reaction runner) and
game/screens/phone_feed.rpy (feed list inside phone_screen, opened post). Day Two content:
game/chapters/ch01/day2/ch01_day2_feed.rpy (Maya's intro post) and scene 09 of
game/chapters/ch01/day2/ch01_day2_scenes_01_15.rpy.
"""
import pickle
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
sys.path.insert(0, str(GAME / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_feed  # noqa: E402
from lc_rpy_harness import load_blocks  # noqa: E402

FEED_RPY = GAME / "systems" / "feed.rpy"
FEED_SCREEN = GAME / "screens" / "phone_feed.rpy"
PHONE_SRC = GAME / "screens" / "phone_sweetheart.rpy"
HUD_SRC = GAME / "screens" / "phone_hud.rpy"
DAY2_FEED = GAME / "chapters" / "ch01" / "day2" / "ch01_day2_feed.rpy"
DAY2_SCENES = GAME / "chapters" / "ch01" / "day2" / "ch01_day2_scenes_01_15.rpy"


def _read(path):
    return path.read_text(encoding="utf-8")


def _registry(*posts):
    reg = {}
    for kwargs in posts:
        lc_feed.register(reg, **kwargs)
    return reg


def _post(post_id, day="ch01_d2", **kw):
    row = dict(post_id=post_id, day=day, author="Maya", handle="maya.in.frame",
               caption="Caption for " + post_id)
    row.update(kw)
    return row


class RegisterTests(unittest.TestCase):
    def test_register_keeps_every_field(self):
        react = lambda: None  # noqa: E731
        reg = _registry(_post("a", image="cg x", comments=[("[friend_name]", "Hi.")], likes=12,
                              when="Day Two, 14:20", mature=True, reaction=react))
        entry = reg["a"]
        self.assertEqual(entry["id"], "a")
        self.assertEqual(entry["day"], "ch01_d2")
        self.assertEqual(entry["author"], "Maya")
        self.assertEqual(entry["handle"], "maya.in.frame")
        self.assertEqual(entry["image"], "cg x")
        self.assertEqual(entry["comments"], (("[friend_name]", "Hi."),))
        self.assertEqual(entry["likes"], 12)
        self.assertEqual(entry["when"], "Day Two, 14:20")
        self.assertTrue(entry["mature"])
        self.assertIsNone(entry["unlock"])
        self.assertIs(entry["reaction"], react)

    def test_gates_reactions_and_times_accept_their_forms(self):
        reg = _registry(_post("a", unlock={"ch01_d2_errand_lane": "love"}, reaction="some_label"),
                        _post("b", unlock={"leia_did": ["x", "y"], "leia_did_not": "z"}),
                        _post("c", unlock=lambda: True, when=lambda: "16:20"))
        self.assertEqual(reg["a"]["reaction"], "some_label")
        self.assertTrue(callable(reg["c"]["when"]))

    def test_duplicate_id_is_rejected(self):
        reg = _registry(_post("a"))
        with self.assertRaises(ValueError):
            lc_feed.register(reg, **_post("a", day="ch01_d3"))

    def test_bad_fields_are_rejected_and_nothing_is_registered(self):
        bad = (
            _post(""), _post("a", day=""), _post("a", author=""), _post("a", handle=""),
            _post("a", caption=""), _post("a", likes=-1), _post("a", likes="12"),
            _post("a", image=""), _post("a", unlock="not callable"), _post("a", unlock={}),
            _post("a", unlock={"leia_did": ""}), _post("a", when=""), _post("a", reaction=""),
            _post("a", reaction=3),
            _post("a", comments=[("x", "1"), ("x", "2"), ("x", "3"), ("x", "4")]),
            _post("a", comments=[("x",)]), _post("a", comments=[("", "text")]),
        )
        for row in bad:
            reg = {}
            with self.assertRaises(ValueError, msg=repr(row)):
                lc_feed.register(reg, **row)
            self.assertEqual(reg, {})

    def test_typed_default_names_are_rejected(self):
        for row in (_post("a", caption="Ryan blinked."),
                    _post("a", author="Julian"),
                    _post("a", handle="leia.official"),
                    _post("a", handle="Leia"),
                    _post("a", comments=[("Julian", "Hi.")]),
                    _post("a", comments=[("x", "Leia, send it.")])):
            with self.assertRaises(ValueError, msg=repr(row)):
                lc_feed.register({}, **row)
        # Bracketed name variables are the right way to write them.
        lc_feed.register({}, **_post("ok", author="[friend_name]", handle="[friend_name]",
                                    caption="[player_name] blinked.",
                                    comments=[("[friend_name]", "[girlfriend_name], send it.")]))


class UnlockTests(unittest.TestCase):
    def gate(self, unlock, values=None, did=None, use_did=True):
        entry = _registry(_post("p", unlock=unlock))["p"]
        values = values or {}
        did = did or set()
        return lc_feed.unlock_ok(entry, get_value=values.get,
                                 leia_did=(lambda m: m in did) if use_did else None)

    def test_none_and_callables(self):
        self.assertTrue(self.gate(None))
        self.assertTrue(self.gate(lambda: True))
        self.assertFalse(self.gate(lambda: 0))

    def test_story_value_rows(self):
        lane = {"ch01_d2_errand_lane": "love"}
        self.assertTrue(self.gate(lane, {"ch01_d2_errand_lane": "love"}))
        self.assertFalse(self.gate(lane, {"ch01_d2_errand_lane": "ntr_risk"}))
        # An old save that never ran the errand has no value: the post stays out.
        self.assertFalse(self.gate(lane, {}))
        either = {"ch01_d2_errand_lane": ("love", "exhibitionism")}
        self.assertTrue(self.gate(either, {"ch01_d2_errand_lane": "exhibitionism"}))
        self.assertFalse(self.gate(either, {"ch01_d2_errand_lane": "ntr_risk"}))
        self.assertTrue(self.gate({"ch01_d2_leia_told": True}, {"ch01_d2_leia_told": "told"}))
        self.assertFalse(self.gate({"ch01_d2_leia_told": True}, {}))

    def test_leia_did_rows(self):
        lingered = {"ch01_d2_errand_lane": "ntr_risk", "leia_did": "ch01_d2_cafe_ntr_lingered"}
        values = {"ch01_d2_errand_lane": "ntr_risk"}
        self.assertTrue(self.gate(lingered, values, {"ch01_d2_cafe_ntr_lingered"}))
        self.assertFalse(self.gate(lingered, values, set()))
        default = {"ch01_d2_errand_lane": "ntr_risk", "leia_did_not": "ch01_d2_cafe_ntr_lingered"}
        self.assertTrue(self.gate(default, values, set()))
        self.assertFalse(self.gate(default, values, {"ch01_d2_cafe_ntr_lingered"}))
        # A build without lc_leia_did cannot answer: never release.
        self.assertFalse(self.gate(default, values, set(), use_did=False))


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.reg = _registry(_post("a"), _post("b"), _post("c", day="ch01_d3"))

    def test_release_appends_without_mutating_its_inputs(self):
        released = []
        new_released, newly = lc_feed.release(self.reg, released, ["a"])
        self.assertEqual(new_released, ["a"])
        self.assertEqual(newly, ["a"])
        self.assertEqual(released, [])

    def test_a_batch_comes_out_in_call_order(self):
        released, newly = lc_feed.release(self.reg, ["a"], ["c", "a", "b", "c"])
        self.assertEqual(released, ["a", "c", "b"])
        self.assertEqual(newly, ["c", "b"])
        self.assertEqual(lc_feed.release(self.reg, None, "b"), (["b"], ["b"]))

    def test_releasing_twice_changes_nothing(self):
        released, _ = lc_feed.release(self.reg, [], ["a"])
        again, newly = lc_feed.release(self.reg, released, ["a"])
        self.assertIs(again, released)
        self.assertEqual(newly, [])

    def test_unknown_post_raises_before_anything_changes(self):
        with self.assertRaises(ValueError):
            lc_feed.release(self.reg, [], ["a", "zzz"])

    def test_a_locked_post_is_not_released_until_its_condition_holds(self):
        gate = {"open": False}
        reg = _registry(_post("lane", unlock=lambda: gate["open"]), _post("free"))
        check = lambda entry: lc_feed.unlock_ok(entry)  # noqa: E731
        released, newly = lc_feed.release(reg, [], ["lane", "free"], check)
        self.assertEqual((released, newly), (["free"], ["free"]))
        gate["open"] = True
        released, newly = lc_feed.release(reg, released, ["lane"], check)
        self.assertEqual((released, newly), (["free", "lane"], ["lane"]))
        # Frozen once released: the condition changing later does not hide it.
        gate["open"] = False
        self.assertEqual([e["id"] for e in lc_feed.visible(reg, released)], ["lane", "free"])

    def test_one_banner_text_per_batch(self):
        reg = _registry(_post("a", caption="First."), _post("b", author="Dan"),
                        _post("c", author="Kayla"))
        self.assertIsNone(lc_feed.banner_text([]))
        self.assertEqual(lc_feed.banner_text([reg["a"]]), ("Maya", "First."))
        self.assertEqual(lc_feed.banner_text([reg["a"], reg["b"]]), ("2 new posts", "Maya and Dan posted."))
        self.assertEqual(lc_feed.banner_text([reg["a"], reg["b"], reg["c"]]),
                         ("3 new posts", "Maya, Dan and more posted."))


class VisibleAndSeenTests(unittest.TestCase):
    def setUp(self):
        self.reg = _registry(_post("a"), _post("b"), _post("c"))

    def test_newest_release_first(self):
        self.assertEqual([e["id"] for e in lc_feed.visible(self.reg, ["b", "a", "c"])], ["c", "a", "b"])

    def test_nothing_visible_for_old_saves_and_retired_ids_are_skipped(self):
        self.assertEqual(lc_feed.visible(self.reg, None), [])
        self.assertEqual([e["id"] for e in lc_feed.visible(self.reg, ["a", "gone"])], ["a"])

    def test_mark_seen_and_many_return_a_new_set_once(self):
        seen = set()
        new = lc_feed.mark_seen(seen, "a")
        self.assertEqual(new, {"a"})
        self.assertEqual(seen, set())
        self.assertIs(lc_feed.mark_seen(new, "a"), new)
        self.assertEqual(lc_feed.mark_seen(None, "b"), {"b"})
        both = lc_feed.mark_many(new, ["a", "b"])
        self.assertEqual(both, {"a", "b"})
        self.assertIs(lc_feed.mark_many(both, ["b"]), both)

    def test_any_seen(self):
        self.assertTrue(lc_feed.any_seen({"a"}, ("b", "a")))
        self.assertFalse(lc_feed.any_seen({"a"}, ("b",)))
        self.assertFalse(lc_feed.any_seen(None, ("a",)))

    def test_unseen_ids_count_and_badge(self):
        self.assertEqual(lc_feed.unseen_ids(self.reg, ["a", "b", "c"], {"b"}), ["c", "a"])
        self.assertEqual(lc_feed.unseen_count(self.reg, ["a", "b"], {"a"}), 1)
        self.assertEqual(lc_feed.unseen_count(self.reg, None, None), 0)
        self.assertIsNone(lc_feed.badge_label(0))
        self.assertEqual(lc_feed.badge_label(3), "3")
        self.assertEqual(lc_feed.badge_label(12), "9+")

    def test_likes_label_is_singular_for_one(self):
        self.assertEqual(lc_feed.likes_label(1), "1 like")
        self.assertEqual(lc_feed.likes_label(0), "0 likes")
        self.assertEqual(lc_feed.likes_label(23), "23 likes")

    def test_app_shows_once_installed_or_any_post_is_released(self):
        self.assertFalse(lc_feed.app_visible(False, []))
        self.assertFalse(lc_feed.app_visible(None, None))
        self.assertTrue(lc_feed.app_visible(True, []))
        self.assertTrue(lc_feed.app_visible(False, ["a"]))

    def test_mature_photos_follow_the_gallery_switch(self):
        reg = _registry(_post("m", image="cg m", mature=True), _post("p", image="cg p"))
        self.assertTrue(lc_feed.photo_masked(reg["m"], "list"))
        self.assertTrue(lc_feed.photo_masked(reg["m"], "post", True))
        self.assertFalse(lc_feed.photo_masked(reg["m"], "viewer"))
        self.assertFalse(lc_feed.photo_masked(reg["p"], "list"))
        # GALLERY_MASK_MATURE_COVERS off: the gallery shows mature covers, so does the feed.
        self.assertFalse(lc_feed.photo_masked(reg["m"], "list", False))

    def test_stamp_never_uses_the_device_clock(self):
        reg = _registry(_post("fixed", when="14:10"), _post("fn", when=lambda: "16:45"),
                        _post("clock"), _post("empty_fn", when=lambda: None))
        self.assertEqual(lc_feed.stamp(reg["fixed"], "09:00"), "14:10")
        self.assertEqual(lc_feed.stamp(reg["fn"], None), "16:45")
        self.assertEqual(lc_feed.stamp(reg["clock"], "21:30"), "21:30")
        self.assertIsNone(lc_feed.stamp(reg["clock"], None))
        self.assertIsNone(lc_feed.stamp(reg["empty_fn"], "21:30"))

    def test_reactions_due_once_per_post(self):
        reg = _registry(_post("r", reaction="lbl"), _post("q"), _post("s", reaction=lambda: None))
        self.assertEqual(lc_feed.reactions_due(reg, ["q", "r", "s", "r"], set()), ["r", "s"])
        self.assertEqual(lc_feed.reactions_due(reg, ["r", "s"], {"r"}), ["s"])
        self.assertEqual(lc_feed.reactions_due(reg, ["gone"], None), [])

    def test_reveal_delta_scrolls_a_cut_off_card_fully_into_view(self):
        # View 184..1004 (the phone viewport), margin 48. Focus rects are clipped to the view.
        self.assertEqual(lc_feed.reveal_delta(300, 200, 184, 1004, 48), 0)
        # Cut off at the bottom (only 598..1004 visible): its top goes to 184 + 48.
        self.assertEqual(lc_feed.reveal_delta(598, 406, 184, 1004, 48), 598 - 232)
        # Fully visible but inside the bottom margin: just enough to clear the margin.
        self.assertEqual(lc_feed.reveal_delta(700, 280, 184, 1004, 48), 980 - 956)
        # Cut off at the top (184..400 visible): its visible bottom goes to 1004 - 48.
        self.assertEqual(lc_feed.reveal_delta(184, 216, 184, 1004, 48), 400 - 956)
        # Fully visible inside the top margin.
        self.assertEqual(lc_feed.reveal_delta(200, 200, 184, 1004, 48), 200 - 232)
        # A card filling the whole view: page by page.
        self.assertEqual(lc_feed.reveal_delta(184, 820, 184, 1004, 48), 48)
        self.assertEqual(lc_feed.reveal_delta(220, 784, 184, 1004, 20), 0 + (220 - 204))
        self.assertEqual(lc_feed.reveal_delta(190, 814, 184, 1004, 48), 820 - 96)


class _Disp(object):
    """Records how a displayable was built (stands in for Solid/Text/Fixed/...)."""

    def __init__(self, kind, *args, **kw):
        self.kind, self.args, self.kw = kind, args, kw

    def walk(self):
        yield self
        for arg in self.args:
            if isinstance(arg, _Disp):
                for d in arg.walk():
                    yield d


class FeedRuntimeTests(unittest.TestCase):
    """The production init blocks of systems/feed.rpy with engine stubs."""

    def setUp(self):
        self.calls = []
        self.values = {}
        self.store = SimpleNamespace(lc_feed_installed=False, lc_feed_released=[],
                                     lc_feed_seen_posts=set(), lc_feed_opened_posts=set(),
                                     lc_feed_stamps={}, lc_feed_reacted=set(),
                                     lc_feed_reaction_queue=[], lc_phone_story_time=None,
                                     LC_FEED_APP_NAME="Instababe", main_menu=False)
        self.ctx = SimpleNamespace(interacting=True, current="node")
        self.node = None

        class Say(object):
            pass

        class Menu(object):
            pass

        self.Say = Say

        def call(label, **kw):
            self.calls.append(("call", label, kw))

        renpy = SimpleNamespace(
            store=self.store,
            retain_after_load=lambda: self.calls.append("retain_after_load"),
            show_screen=lambda name, **kw: self.calls.append(("show", name, kw)),
            hide_screen=lambda name: self.calls.append(("hide", name)),
            get_screen=lambda name: None,
            restart_interaction=lambda: None,
            has_image=lambda name, exact=True: True,
            has_label=lambda name: name in ("react_label",),
            loadable=lambda path: False,
            log=lambda *a: None,
            call=call,
            context_nesting_level=lambda: 0,
            game=SimpleNamespace(context=lambda: self.ctx,
                                 script=SimpleNamespace(lookup=lambda name: self.node)),
            ast=SimpleNamespace(Say=Say, Menu=Menu),
            focus_coordinates=lambda: self.focus,
            display=SimpleNamespace(focus=SimpleNamespace(focus_type="keyboard")),
        )
        self.renpy = renpy
        self.focus = (None, None, None, None)
        config = SimpleNamespace(developer=True, screen_height=1080)

        def stat_guard(name):
            return lambda *a, **k: self.calls.append(("STAT", name))

        def disp(kind):
            return lambda *a, **kw: _Disp(kind, *a, **kw)

        self.env = dict(store=self.store, renpy=renpy, config=config, LC_FEED_APP_NAME="Instababe",
                        LC_FEED_VIEW_Y=164, LC_FEED_VIEW_H=820, LC_FEED_REVEAL_MARGIN=48,
                        GALLERY_MASK_MATURE_COVERS=True,
                        get_story_value=lambda key, default=None: self.values.get(key, default),
                        phone_queue_notification=lambda *a, **k: self.calls.append(("banner", a, k)),
                        lc_ui_play=lambda *a, **k: None,
                        lc_phone_rounded_photo=lambda image, w, h: _Disp("photo", image),
                        Solid=disp("Solid"), Text=disp("Text"), Fixed=disp("Fixed"),
                        Transform=disp("Transform"), AlphaMask=disp("AlphaMask"),
                        change_stat=stat_guard("change_stat"), apply_choice=stat_guard("apply_choice"),
                        set_story_value=stat_guard("set_story_value"),
                        set_story_flag=stat_guard("set_story_flag"))
        load_blocks(["lc_feed_register"], self.env)
        self.call("lc_feed_register", "p1", "ch01_d2", "Maya", "maya.in.frame", "First.", likes=3)
        self.call("lc_feed_register", "p2", "ch01_d2", "Maya", "maya.in.frame", "Second.")

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def banners(self):
        return [c for c in self.calls if c[0] == "banner"]

    def test_app_hidden_until_the_intro(self):
        self.assertFalse(self.call("lc_feed_app_visible"))
        self.assertEqual(self.call("lc_feed_visible"), [])
        self.assertIsNone(self.call("lc_feed_badge"))

    def test_every_release_call_shows_one_banner(self):
        self.call("lc_feed_install")
        self.assertTrue(self.call("lc_feed_app_visible"))
        self.call("lc_feed_release", "p1")
        self.call("lc_feed_release", "p2")
        self.assertEqual([e["id"] for e in self.call("lc_feed_visible")], ["p2", "p1"])
        self.assertEqual(self.call("lc_feed_badge"), "2")
        banners = self.banners()
        # Same day, two release calls: two banners (the after-dinner drop is not swallowed).
        self.assertEqual(len(banners), 2)
        self.assertEqual(banners[0][1], ("Instababe", "Maya", "First."))
        self.assertEqual(banners[0][2].get("kind"), "feed")
        # Releasing again shows nothing.
        self.call("lc_feed_release", "p1", "p2")
        self.assertEqual(len(self.banners()), 2)

    def test_a_batch_shows_one_banner(self):
        self.call("lc_feed_release", "p1", "p2")
        self.assertEqual([b[1] for b in self.banners()], [("Instababe", "2 new posts", "Maya posted.")])
        self.call("lc_feed_register", "p3", "ch01_d2", "Dan", "dan.on.tour", "Third.")
        self.call("lc_feed_release", ["p3"])
        self.assertEqual(len(self.banners()), 2)

    def test_release_with_notify_false_shows_no_banner(self):
        self.call("lc_feed_release", "p1", notify=False)
        self.assertEqual(self.banners(), [])
        self.assertTrue(self.call("lc_feed_app_visible"))

    def test_gated_posts_release_only_when_their_condition_holds(self):
        self.call("lc_feed_register", "love", "ch01_d2", "Dan", "dan.on.tour", "Love post.",
                  unlock={"ch01_d2_errand_lane": "love"})
        self.call("lc_feed_register", "ntr", "ch01_d2", "Kayla", "kaylax", "Clip.",
                  unlock={"ch01_d2_errand_lane": "ntr_risk", "leia_did": "ch01_d2_cafe_ntr_lingered"})
        # An old save that skipped the errand: nothing comes out, no banner, no app.
        self.call("lc_feed_release", "love", "ntr")
        self.assertEqual(self.store.lc_feed_released, [])
        self.assertEqual(self.banners(), [])
        self.assertFalse(self.call("lc_feed_app_visible"))
        # NTR lane, but no lc_leia_did in this build: the leia_did row cannot hold.
        self.values["ch01_d2_errand_lane"] = "ntr_risk"
        self.call("lc_feed_release", "love", "ntr")
        self.assertEqual(self.store.lc_feed_released, [])
        self.store.lc_leia_did = lambda mark: mark == "ch01_d2_cafe_ntr_lingered"
        self.call("lc_feed_release", "love", "ntr")
        self.assertEqual(self.store.lc_feed_released, ["ntr"])
        self.assertEqual(len(self.banners()), 1)

    def test_listing_the_feed_counts_as_seeing_every_post(self):
        self.call("lc_feed_release", "p1", "p2")
        self.assertEqual(self.call("lc_feed_unseen_count"), 2)
        self.call("lc_feed_visit_start")
        self.assertTrue(self.call("lc_feed_is_fresh", "p1"))
        self.assertIsNone(self.call("lc_feed_catch_up"))
        self.assertTrue(self.call("lc_feed_seen", "p1"))
        self.assertTrue(self.call("lc_feed_any_seen", "p2"))
        self.assertFalse(self.call("lc_feed_opened", "p1"))
        self.assertEqual(self.call("lc_feed_unseen_count"), 0)
        self.assertIsNone(self.call("lc_feed_badge"))
        self.assertIn("retain_after_load", self.calls)
        # The blue dots stay for this visit, and clear on the next one.
        self.assertTrue(self.call("lc_feed_is_fresh", "p2"))
        self.call("lc_feed_visit_start")
        self.assertFalse(self.call("lc_feed_is_fresh", "p2"))
        self.assertEqual([c for c in self.calls if c[0] == "STAT"], [])

    def test_opening_a_post_marks_it_opened_and_seen_and_moves_no_stats(self):
        self.call("lc_feed_release", "p1")
        self.assertFalse(self.call("lc_feed_seen", "p1"))
        self.assertIsNone(self.call("lc_feed_open_post", "p1"))
        self.assertTrue(self.call("lc_feed_seen", "p1"))
        self.assertTrue(self.call("lc_feed_opened", "p1"))
        self.assertIn(("show", "lc_feed_post", {"post_id": "p1"}), self.calls)
        self.assertIn("retain_after_load", self.calls)
        self.assertIsNone(self.call("lc_feed_badge"))
        self.assertEqual([c for c in self.calls if c[0] == "STAT"], [])

    def test_posts_are_stamped_with_the_story_clock_at_release(self):
        self.store.lc_phone_story_time = "14:10"
        self.call("lc_feed_release", "p1")
        self.store.lc_phone_story_time = None          # the next time skip clears the clock
        self.call("lc_feed_release", "p2")
        self.assertEqual(self.call("lc_feed_when", self.call("lc_feed_entry", "p1")), "14:10")
        # No story clock and no `when`: no time at all, never the device clock.
        self.assertEqual(self.call("lc_feed_when", self.call("lc_feed_entry", "p2")), "")
        self.call("lc_feed_register", "p3", "ch01_d2", "Dan", "dan", "Third.", when=lambda: "16:45")
        self.store.lc_phone_story_time = "21:00"
        self.call("lc_feed_release", "p3")
        self.assertEqual(self.store.lc_feed_stamps, {"p1": "14:10", "p3": "16:45"})

    def test_first_sight_reaction_is_queued_once_and_runs_after_the_phone_closes(self):
        ran = []
        self.call("lc_feed_register", "r1", "ch01_d2", "Kayla", "kaylax", "Clip.", reaction="react_label")
        self.call("lc_feed_register", "r2", "ch01_d2", "Dan", "dan", "Pool.", reaction=lambda: ran.append("r2"))
        self.call("lc_feed_release", "r1", "r2", "p1")
        self.assertEqual(self.store.lc_feed_reaction_queue, [])
        self.call("lc_feed_catch_up")
        self.assertEqual(self.store.lc_feed_reaction_queue, ["r2", "r1"])
        # Seeing them again never re-queues.
        self.call("lc_feed_open_post", "r1")
        self.assertEqual(self.store.lc_feed_reaction_queue, ["r2", "r1"])
        # The phone closes from a player action during a dialogue line: the runner is called and
        # returns to that line.
        self.node = self.Say()
        self.env["_lc_feed_on_phone_closed"]()
        self.assertIn(("call", "lc_feed_reaction_runner", {"from_current": True}), self.calls)
        # The runner's steps: the callable runs in place, the label comes back to be called.
        self.assertIsNone(self.call("lc_feed_reaction_next"))
        self.assertEqual(ran, ["r2"])
        self.assertEqual(self.call("lc_feed_reaction_next"), "react_label")
        self.assertEqual(self.store.lc_feed_reaction_queue, [])
        self.assertIsNone(self.call("lc_feed_reaction_next"))

    def test_reactions_never_start_from_story_python_menus_contexts_or_replays(self):
        self.call("lc_feed_register", "r1", "ch01_d2", "Kayla", "kaylax", "Clip.", reaction="react_label")
        self.call("lc_feed_release", "r1")
        self.call("lc_feed_catch_up")
        hook = self.env["_lc_feed_on_phone_closed"]
        self.node = object()                   # a python statement (phone_call_offer closes it)
        hook()
        self.node = self.Say()
        self.ctx.interacting = False           # story code closing the phone, not the player
        hook()
        self.ctx.interacting = True
        self.store.main_menu = True
        hook()
        self.store.main_menu = False
        self.store._in_replay = "some_label"
        hook()
        self.assertEqual([c for c in self.calls if c[0] == "call"], [])
        self.assertEqual(self.store.lc_feed_reaction_queue, ["r1"])

    def test_the_hook_is_registered_on_phone_closed(self):
        self.assertIn(self.env["_lc_feed_on_phone_closed"], self.env["_lc_hooks"]["phone_closed"])

    def test_missing_reaction_label_fails_loudly_in_developer_builds(self):
        self.call("lc_feed_register", "r1", "ch01_d2", "Kayla", "kaylax", "Clip.", reaction="no_such_label")
        self.store.lc_feed_reaction_queue = ["r1"]
        with self.assertRaises(Exception):
            self.call("lc_feed_reaction_next")
        self.env["config"].developer = False
        self.store.lc_feed_reaction_queue = ["r1"]
        self.assertIsNone(self.call("lc_feed_reaction_next"))
        self.assertEqual(self.store.lc_feed_reaction_queue, [])

    def test_keyboard_focus_scrolls_the_card_into_view_but_the_mouse_never_does(self):
        adj = SimpleNamespace(value=0.0)
        adj.change = lambda v: setattr(adj, "value", v)
        # A card cut off at the bottom of the 184..1004 viewport.
        self.focus = (732, 892, 456, 112)
        self.assertIsNone(self.call("lc_feed_reveal_focus", adj))
        self.assertEqual(adj.value, 892 - (184 + 48))
        adj.value = 0.0
        self.renpy.display.focus.focus_type = "mouse"
        self.call("lc_feed_reveal_focus", adj)
        self.assertEqual(adj.value, 0.0)
        self.renpy.display.focus.focus_type = "keyboard"
        self.focus = (732, 300, 456, 330)      # already inside
        self.call("lc_feed_reveal_focus", adj)
        self.assertEqual(adj.value, 0.0)
        self.assertIsNone(self.call("lc_feed_reveal_focus", None))

    def test_mature_photo_is_a_gallery_style_card_with_no_image(self):
        self.call("lc_feed_register", "m", "ch01_d2", "Kayla", "kaylax", "Clip.", image="cg clip", mature=True)
        entry = self.call("lc_feed_entry", "m")
        card = self.call("lc_feed_photo", entry, 456, 240, "list")
        kinds = [d.kind for d in card.walk()]
        self.assertNotIn("photo", kinds)
        self.assertIn("MATURE", [d.args[0] for d in card.walk() if d.kind == "Text"])
        self.assertEqual(self.call("lc_feed_photo", entry, 456, 456, "viewer").kind, "photo")
        # Gallery switch off: the photo shows, as gallery covers do.
        self.env["GALLERY_MASK_MATURE_COVERS"] = False
        self.assertEqual(self.call("lc_feed_photo", entry, 456, 240, "list").kind, "photo")

    def test_likes_text(self):
        self.assertEqual(self.call("lc_feed_likes", self.call("lc_feed_entry", "p1")), "3 likes")
        self.call("lc_feed_register", "one", "ch01_d2", "Dan", "dan", "One.", likes=1)
        self.assertEqual(self.call("lc_feed_likes", self.call("lc_feed_entry", "one")), "1 like")

    def test_save_and_rollback_carry_the_feed_state(self):
        before = dict(vars(self.store))
        self.store.lc_phone_story_time = "14:10"
        self.call("lc_feed_install")
        self.call("lc_feed_release", "p1")
        self.call("lc_feed_open_post", "p1")
        saved = pickle.loads(pickle.dumps({k: v for k, v in vars(self.store).items()
                                           if k.startswith("lc_feed_")}))
        self.assertEqual(saved["lc_feed_released"], ["p1"])
        self.assertEqual(saved["lc_feed_seen_posts"], {"p1"})
        self.assertEqual(saved["lc_feed_opened_posts"], {"p1"})
        self.assertEqual(saved["lc_feed_stamps"], {"p1": "14:10"})
        self.assertTrue(saved["lc_feed_installed"])
        # Rollback restores the store variables; nothing was mutated in place.
        for key, value in before.items():
            setattr(self.store, key, value)
        self.assertEqual(before["lc_feed_released"], [])
        self.assertEqual(before["lc_feed_seen_posts"], set())
        self.assertEqual(before["lc_feed_stamps"], {})
        self.assertFalse(self.call("lc_feed_app_visible"))
        self.assertFalse(self.call("lc_feed_seen", "p1"))

    def test_old_saves_without_feed_state_read_as_nothing_happened(self):
        for key in ("lc_feed_installed", "lc_feed_released", "lc_feed_seen_posts",
                    "lc_feed_opened_posts", "lc_feed_stamps", "lc_feed_reacted",
                    "lc_feed_reaction_queue"):
            delattr(self.store, key)
        self.assertFalse(self.call("lc_feed_app_visible"))
        self.assertEqual(self.call("lc_feed_visible"), [])
        self.assertFalse(self.call("lc_feed_seen", "p1"))
        self.assertIsNone(self.call("lc_feed_badge"))
        self.assertEqual(self.call("lc_feed_when", self.call("lc_feed_entry", "p1")), "")
        self.call("lc_feed_release", "p1")
        self.assertEqual([e["id"] for e in self.call("lc_feed_visible")], ["p1"])
        self.call("lc_feed_catch_up")
        self.assertIsNone(self.call("lc_feed_reaction_next"))

    def test_unknown_post_open_raises_in_developer_builds_and_is_ignored_in_release(self):
        with self.assertRaises(Exception):
            self.call("lc_feed_open_post", "nope")
        with self.assertRaises(Exception):
            self.call("lc_feed_release", "nope")
        self.env["config"].developer = False
        self.assertIsNone(self.call("lc_feed_open_post", "nope"))
        self.assertIsNone(self.call("lc_feed_release", "nope", "p1"))
        self.assertFalse(self.call("lc_feed_seen", "nope"))
        self.assertEqual(self.store.lc_feed_released, ["p1"])


class WiringTests(unittest.TestCase):
    def test_app_name_is_one_define(self):
        self.assertIn('define LC_FEED_APP_NAME = "Instababe"', _read(FEED_RPY))

    def test_viewing_code_never_touches_stats_or_story_state(self):
        banned = re.compile(r"\b(change_stat|apply_choice|set_story_value|set_story_flag|add_stat)\s*\(")
        for path in (FEED_RPY, FEED_SCREEN):
            code = "\n".join(l for l in _read(path).splitlines() if not l.lstrip().startswith("#"))
            self.assertIsNone(banned.search(code), path.name)

    def test_home_grid_draws_the_app_only_when_visible(self):
        src = _read(PHONE_SRC)
        self.assertIn("for i, row in enumerate(lc_sm_home_apps()):", src)
        self.assertIn("lc_feed_app_visible()", src)
        self.assertIn('if app_id == "feed":', src)
        self.assertIn('[Function(lc_feed_visit_start), SetScreenVariable("phone_app", "feed")]', src)

    def test_hud_badge_counts_unseen_posts_too(self):
        src = _read(HUD_SRC)
        self.assertIn("$ _hud_count = phone_total_unread() + lc_feed_unseen_count()", src)
        self.assertIn("phone_unread_badge_label(_hud_count)", src)
        self.assertIn("unread messages and new posts", src)

    def test_feed_list_is_marked_seen_and_scrolls_to_the_focused_card(self):
        src = _read(PHONE_SRC)
        self.assertIn("default feed_yadj = ui.adjustment()", src)
        self.assertIn('yadjustment (feed_yadj if phone_app == "feed" else None)', src)
        self.assertIn("use lc_feed_list(feed_yadj)", src)
        self.assertIn("timer 0.2 repeat True action Function(lc_feed_catch_up, _update_screens=False)", src)
        screen = _read(FEED_SCREEN)
        self.assertIn("hovered Function(lc_feed_reveal_focus, yadj)", screen)
        post = screen.split("screen lc_feed_post(post_id):", 1)[1]
        self.assertIn("arrowkeys True", post)
        self.assertIn("pagekeys True", post)

    def test_phone_back_and_close_know_the_opened_post(self):
        src = _read(PHONE_SRC)
        back = src.split("def lc_phone_back():", 1)[1].split("\n    def ", 1)[0]
        close = src.split("def lc_phone_close():", 1)[1].split("\n    def ", 1)[0]
        self.assertIn('"lc_feed_post"', back)
        self.assertIn('"lc_feed_post"', close)
        self.assertIn('lc_hook_run("phone_closed")', close)
        # The photo viewer a post opens sits on top (zorder 380 > 340): Back closes it first.
        self.assertLess(back.index("lc_phone_photo_viewer"), back.index("lc_feed_post"))

    def test_feed_screen_uses_the_phone_lane_and_masks_mature_photos(self):
        src = _read(FEED_SCREEN)
        self.assertIn("screen lc_feed_list(yadj=None):", src)
        self.assertIn("screen lc_feed_post(post_id):", src)
        self.assertIn("LC_PHONE_CONTENT_WIDTH", src)
        self.assertIn('lc_feed_photo(', src)
        self.assertIn("use lc_phone_backdrop(", src)
        self.assertIn("GALLERY_MASK_MATURE_COVERS", _read(FEED_RPY))

    def test_banner_deep_links_into_the_feed(self):
        logic = _read(GAME / "systems" / "phone_presentation_logic.rpy")
        self.assertIn('item.get("kind") == "feed"', logic)
        self.assertIn("lc_feed_visit_start()", logic)

    def test_reaction_runner_label_exists(self):
        src = _read(FEED_RPY)
        self.assertIn("label lc_feed_reaction_runner:", src)
        self.assertIn('lc_hook_add("phone_closed", _lc_feed_on_phone_closed)', src)

    def test_chapter_select_later_days_have_the_app(self):
        src = _read(GAME / "chapters" / "ch01" / "day2" / "ch01_day2_chapter.rpy")
        apply = src.split("def ch01_d2_select_finished(", 1)[1]
        self.assertIn("lc_feed_install()", apply)

    def test_icon_comes_from_the_sprite_match_generator(self):
        self.assertTrue((GAME / "gui" / "phone" / "sprite_match" / "feed.png").is_file())
        self.assertIn('"feed"', _read(ROOT / "tools" / "gen_sprite_match_ui.py"))

    def test_app_label_fits_under_the_icon(self):
        try:
            from PIL import ImageFont
        except ImportError:
            self.skipTest("Pillow is not installed")
        name = re.search(r'define LC_FEED_APP_NAME = "([^"]+)"', _read(FEED_RPY)).group(1)
        hand = ImageFont.truetype(str(GAME / "fonts" / "PatrickHand-Regular.ttf"), 22)
        self.assertLess(hand.getlength(name), 108)


class DayTwoIntroTests(unittest.TestCase):
    def test_maya_intro_post_is_registered_text_only_and_stamped_by_the_story_clock(self):
        src = _read(DAY2_FEED)
        call = re.search(r'lc_feed_register\(\s*"d2_maya_group_photo".*?\)\n', src, re.S)
        self.assertIsNotNone(call)
        self.assertNotIn("image=", call.group(0))
        self.assertNotIn("mature=", call.group(0))
        self.assertNotIn("when=", call.group(0))

    def test_photo_walk_installs_the_app_and_releases_only_mayas_post(self):
        scene = _read(DAY2_SCENES).split("label ch01_day2_scene_09_photo_walk:", 1)[1]
        scene = scene.split("\nlabel ", 1)[0]
        self.assertIn("[LC_FEED_APP_NAME]", scene)
        self.assertIn("$ lc_feed_install()", scene)
        self.assertIn('$ lc_feed_release("d2_maya_group_photo")', scene)
        whole = _read(DAY2_SCENES)
        self.assertEqual(len(re.findall(r"lc_feed_release\(", whole)), 1)
        self.assertLess(scene.index("$ lc_feed_install()"), scene.index("lc_feed_release("))

    def test_photo_walk_sets_the_story_clock_before_the_post_and_clears_it_after(self):
        scene = _read(DAY2_SCENES).split("label ch01_day2_scene_09_photo_walk:", 1)[1]
        scene = scene.split("\nlabel ", 1)[0]
        set_at = scene.index('$ lc_phone_set_story_time("14:10")')
        self.assertLess(set_at, scene.index("lc_feed_release("))
        self.assertLess(scene.index("lc_feed_release("), scene.index("$ lc_phone_clear_story_time()"))
        self.assertLess(scene.index("$ lc_phone_clear_story_time()"),
                        scene.index("jump ch01_day2_scene_10_leia_maya_photo"))


if __name__ == "__main__":
    unittest.main()
