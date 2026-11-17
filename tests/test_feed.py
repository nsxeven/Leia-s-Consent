"""The social-feed phone app (placeholder name LC_FEED_APP_NAME = "Instababe").

Pure rules: game/python-packages/lc_feed.py (registry checks, release/unlock, ordering, the
save-local seen record, badge). Ren'Py side: game/systems/feed.rpy (store state, API) and
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
        reg = _registry(_post("a", image="cg x", comments=[("[friend_name]", "Hi.")], likes=12,
                              when="Day Two, 14:20", mature=True))
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

    def test_duplicate_id_is_rejected(self):
        reg = _registry(_post("a"))
        with self.assertRaises(ValueError):
            lc_feed.register(reg, **_post("a", day="ch01_d3"))

    def test_bad_fields_are_rejected_and_nothing_is_registered(self):
        bad = (
            _post(""), _post("a", day=""), _post("a", author=""), _post("a", handle=""),
            _post("a", caption=""), _post("a", likes=-1), _post("a", likes="12"),
            _post("a", image=""), _post("a", unlock="not callable"),
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
                    _post("a", comments=[("Julian", "Hi.")]),
                    _post("a", comments=[("x", "Leia, send it.")])):
            with self.assertRaises(ValueError, msg=repr(row)):
                lc_feed.register({}, **row)
        # Bracketed name variables are the right way to write them.
        lc_feed.register({}, **_post("ok", caption="[player_name] blinked.",
                                    comments=[("[friend_name]", "[girlfriend_name], send it.")]))


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.reg = _registry(_post("a"), _post("b"), _post("c", day="ch01_d3"))

    def test_release_appends_without_mutating_its_inputs(self):
        released, days = [], set()
        new_released, new_days, banner = lc_feed.release(self.reg, released, days, "a")
        self.assertEqual(new_released, ["a"])
        self.assertEqual(new_days, {"ch01_d2"})
        self.assertTrue(banner)
        self.assertEqual(released, [])
        self.assertEqual(days, set())

    def test_one_banner_per_day(self):
        released, days, first = lc_feed.release(self.reg, [], set(), "a")
        released, days, second = lc_feed.release(self.reg, released, days, "b")
        released, days, third = lc_feed.release(self.reg, released, days, "c")
        self.assertEqual((first, second, third), (True, False, True))

    def test_releasing_twice_changes_nothing(self):
        released, days, _ = lc_feed.release(self.reg, [], set(), "a")
        again, again_days, banner = lc_feed.release(self.reg, released, days, "a")
        self.assertIs(again, released)
        self.assertIs(again_days, days)
        self.assertFalse(banner)

    def test_unknown_post_raises(self):
        with self.assertRaises(ValueError):
            lc_feed.release(self.reg, [], set(), "zzz")

    def test_a_locked_post_is_not_released_until_its_condition_holds(self):
        gate = {"open": False}
        reg = _registry(_post("lane", unlock=lambda: gate["open"]))
        released, days, banner = lc_feed.release(reg, [], set(), "lane")
        self.assertEqual((released, days, banner), ([], set(), False))
        gate["open"] = True
        released, days, banner = lc_feed.release(reg, released, days, "lane")
        self.assertEqual((released, banner), (["lane"], True))
        # Frozen once released: the condition changing later does not hide it.
        gate["open"] = False
        self.assertEqual([e["id"] for e in lc_feed.visible(reg, released)], ["lane"])

    def test_old_saves_with_no_state_release_cleanly(self):
        released, days, banner = lc_feed.release(self.reg, None, None, "a")
        self.assertEqual((released, days, banner), (["a"], {"ch01_d2"}, True))


class VisibleAndSeenTests(unittest.TestCase):
    def setUp(self):
        self.reg = _registry(_post("a"), _post("b"), _post("c"))

    def test_newest_release_first(self):
        self.assertEqual([e["id"] for e in lc_feed.visible(self.reg, ["b", "a", "c"])], ["c", "a", "b"])

    def test_nothing_visible_for_old_saves_and_retired_ids_are_skipped(self):
        self.assertEqual(lc_feed.visible(self.reg, None), [])
        self.assertEqual([e["id"] for e in lc_feed.visible(self.reg, ["a", "gone"])], ["a"])

    def test_mark_seen_returns_a_new_set_once(self):
        seen = set()
        new = lc_feed.mark_seen(seen, "a")
        self.assertEqual(new, {"a"})
        self.assertEqual(seen, set())
        self.assertIs(lc_feed.mark_seen(new, "a"), new)
        self.assertEqual(lc_feed.mark_seen(None, "b"), {"b"})

    def test_any_seen(self):
        self.assertTrue(lc_feed.any_seen({"a"}, ("b", "a")))
        self.assertFalse(lc_feed.any_seen({"a"}, ("b",)))
        self.assertFalse(lc_feed.any_seen(None, ("a",)))

    def test_unseen_count_and_badge(self):
        self.assertEqual(lc_feed.unseen_count(self.reg, ["a", "b"], {"a"}), 1)
        self.assertEqual(lc_feed.unseen_count(self.reg, None, None), 0)
        self.assertIsNone(lc_feed.badge_label(0))
        self.assertEqual(lc_feed.badge_label(3), "3")
        self.assertEqual(lc_feed.badge_label(12), "9+")

    def test_app_shows_once_installed_or_any_post_is_released(self):
        self.assertFalse(lc_feed.app_visible(False, []))
        self.assertFalse(lc_feed.app_visible(None, None))
        self.assertTrue(lc_feed.app_visible(True, []))
        self.assertTrue(lc_feed.app_visible(False, ["a"]))

    def test_mature_photos_are_masked_in_the_feed_and_post_but_not_the_viewer(self):
        reg = _registry(_post("m", image="cg m", mature=True), _post("p", image="cg p"))
        self.assertTrue(lc_feed.photo_masked(reg["m"], "list"))
        self.assertTrue(lc_feed.photo_masked(reg["m"], "post"))
        self.assertFalse(lc_feed.photo_masked(reg["m"], "viewer"))
        self.assertFalse(lc_feed.photo_masked(reg["p"], "list"))


class FeedRuntimeTests(unittest.TestCase):
    """The production init blocks of systems/feed.rpy with engine stubs."""

    def setUp(self):
        self.calls = []
        self.store = SimpleNamespace(lc_feed_installed=False, lc_feed_released=[],
                                     lc_feed_seen_posts=set(), lc_feed_banner_days=set(),
                                     LC_FEED_APP_NAME="Instababe")
        renpy = SimpleNamespace(
            store=self.store,
            retain_after_load=lambda: self.calls.append("retain_after_load"),
            show_screen=lambda name, **kw: self.calls.append(("show", name, kw)),
            hide_screen=lambda name: self.calls.append(("hide", name)),
            get_screen=lambda name: None,
            restart_interaction=lambda: None,
            has_image=lambda name, exact=True: True,
            log=lambda *a: None,
        )
        config = SimpleNamespace(developer=True)

        def stat_guard(name):
            return lambda *a, **k: self.calls.append(("STAT", name))

        self.env = dict(store=self.store, renpy=renpy, config=config, LC_FEED_APP_NAME="Instababe",
                        phone_queue_notification=lambda *a, **k: self.calls.append(("banner", a, k)),
                        lc_ui_play=lambda *a, **k: None,
                        change_stat=stat_guard("change_stat"), apply_choice=stat_guard("apply_choice"),
                        set_story_value=stat_guard("set_story_value"),
                        set_story_flag=stat_guard("set_story_flag"))
        load_blocks(["lc_feed_register"], self.env)
        self.call("lc_feed_register", "p1", "ch01_d2", "Maya", "maya.in.frame", "First.", likes=3)
        self.call("lc_feed_register", "p2", "ch01_d2", "Maya", "maya.in.frame", "Second.")

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def test_app_hidden_until_the_intro(self):
        self.assertFalse(self.call("lc_feed_app_visible"))
        self.assertEqual(self.call("lc_feed_visible"), [])
        self.assertIsNone(self.call("lc_feed_badge"))

    def test_install_then_release_shows_the_post_badge_and_one_banner(self):
        self.call("lc_feed_install")
        self.assertTrue(self.call("lc_feed_app_visible"))
        self.call("lc_feed_release", "p1")
        self.call("lc_feed_release", "p2")
        self.assertEqual([e["id"] for e in self.call("lc_feed_visible")], ["p2", "p1"])
        self.assertEqual(self.call("lc_feed_badge"), "2")
        banners = [c for c in self.calls if c[0] == "banner"]
        self.assertEqual(len(banners), 1)
        self.assertEqual(banners[0][1][0], "Instababe")
        self.assertEqual(banners[0][2].get("kind"), "feed")

    def test_release_with_notify_false_shows_no_banner(self):
        self.call("lc_feed_release", "p1", notify=False)
        self.assertEqual([c for c in self.calls if c[0] == "banner"], [])
        self.assertTrue(self.call("lc_feed_app_visible"))

    def test_opening_a_post_marks_it_seen_shows_it_and_moves_no_stats(self):
        self.call("lc_feed_release", "p1")
        self.assertFalse(self.call("lc_feed_seen", "p1"))
        self.assertIsNone(self.call("lc_feed_open_post", "p1"))
        self.assertTrue(self.call("lc_feed_seen", "p1"))
        self.assertTrue(self.call("lc_feed_any_seen", "p2", "p1"))
        self.assertIn(("show", "lc_feed_post", {"post_id": "p1"}), self.calls)
        self.assertIn("retain_after_load", self.calls)
        self.assertIsNone(self.call("lc_feed_badge"))
        self.assertEqual([c for c in self.calls if c[0] == "STAT"], [])

    def test_save_and_rollback_carry_the_feed_state(self):
        before = dict(vars(self.store))
        self.call("lc_feed_install")
        self.call("lc_feed_release", "p1")
        self.call("lc_feed_open_post", "p1")
        saved = pickle.loads(pickle.dumps({k: v for k, v in vars(self.store).items()
                                           if k.startswith("lc_feed_")}))
        self.assertEqual(saved["lc_feed_released"], ["p1"])
        self.assertEqual(saved["lc_feed_seen_posts"], {"p1"})
        self.assertTrue(saved["lc_feed_installed"])
        # Rollback restores the store variables; nothing was mutated in place.
        for key, value in before.items():
            setattr(self.store, key, value)
        self.assertEqual(before["lc_feed_released"], [])
        self.assertEqual(before["lc_feed_seen_posts"], set())
        self.assertFalse(self.call("lc_feed_app_visible"))
        self.assertFalse(self.call("lc_feed_seen", "p1"))

    def test_old_saves_without_feed_state_read_as_nothing_happened(self):
        for key in ("lc_feed_installed", "lc_feed_released", "lc_feed_seen_posts", "lc_feed_banner_days"):
            delattr(self.store, key)
        self.assertFalse(self.call("lc_feed_app_visible"))
        self.assertEqual(self.call("lc_feed_visible"), [])
        self.assertFalse(self.call("lc_feed_seen", "p1"))
        self.assertIsNone(self.call("lc_feed_badge"))
        self.call("lc_feed_release", "p1")
        self.assertEqual([e["id"] for e in self.call("lc_feed_visible")], ["p1"])

    def test_unknown_post_open_raises_in_developer_builds_and_is_ignored_in_release(self):
        with self.assertRaises(Exception):
            self.call("lc_feed_open_post", "nope")
        self.env["config"].developer = False
        self.assertIsNone(self.call("lc_feed_open_post", "nope"))
        self.assertFalse(self.call("lc_feed_seen", "nope"))


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

    def test_phone_back_and_close_know_the_opened_post(self):
        src = _read(PHONE_SRC)
        back = src.split("def lc_phone_back():", 1)[1].split("\n    def ", 1)[0]
        close = src.split("def lc_phone_close():", 1)[1].split("\n    def ", 1)[0]
        self.assertIn('"lc_feed_post"', back)
        self.assertIn('"lc_feed_post"', close)
        # The photo viewer a post opens sits on top (zorder 380 > 340): Back closes it first.
        self.assertLess(back.index("lc_phone_photo_viewer"), back.index("lc_feed_post"))

    def test_feed_screen_uses_the_phone_lane_and_masks_mature_photos(self):
        src = _read(FEED_SCREEN)
        self.assertIn("screen lc_feed_list():", src)
        self.assertIn("screen lc_feed_post(post_id):", src)
        self.assertIn("LC_PHONE_CONTENT_WIDTH", src)
        self.assertIn('lc_feed_photo(', src)
        self.assertIn("use lc_phone_backdrop(", src)

    def test_banner_deep_links_into_the_feed(self):
        logic = _read(GAME / "systems" / "phone_presentation_logic.rpy")
        self.assertIn('item.get("kind") == "feed"', logic)

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
    def test_maya_intro_post_is_registered_text_only(self):
        src = _read(DAY2_FEED)
        call = re.search(r'lc_feed_register\(\s*"d2_maya_group_photo".*?\)\n', src, re.S)
        self.assertIsNotNone(call)
        self.assertNotIn("image=", call.group(0))
        self.assertNotIn("mature=", call.group(0))

    def test_photo_walk_installs_the_app_and_releases_only_mayas_post(self):
        scene = _read(DAY2_SCENES).split("label ch01_day2_scene_09_photo_walk:", 1)[1]
        scene = scene.split("\nlabel ", 1)[0]
        self.assertIn("[LC_FEED_APP_NAME]", scene)
        self.assertIn("$ lc_feed_install()", scene)
        self.assertIn('$ lc_feed_release("d2_maya_group_photo")', scene)
        whole = _read(DAY2_SCENES)
        self.assertEqual(len(re.findall(r"lc_feed_release\(", whole)), 1)
        self.assertLess(scene.index("$ lc_feed_install()"), scene.index("lc_feed_release("))


if __name__ == "__main__":
    unittest.main()
