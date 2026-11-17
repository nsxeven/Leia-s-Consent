"""Things Ryan noticed: push-in notices on a CG, their save-local record and the Status pins.

Pure rules: game/python-packages/lc_notice.py. Ren'Py side: game/systems/notice.rpy (registry,
scope, open/close, found record, validation at init 999), game/screens/notice_screen.rpy (cue,
push-in viewer, Status pins). Day Two instances: game/chapters/ch01/day2/.
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
import lc_notice  # noqa: E402
from lc_rpy_harness import load_blocks  # noqa: E402

GAME = ROOT / "game"
SYSTEM = GAME / "systems/notice.rpy"
SCREEN = GAME / "screens/notice_screen.rpy"
VISUALS = GAME / "chapters/ch01/day2/ch01_day2_visuals.rpy"
SC_01_15 = GAME / "chapters/ch01/day2/ch01_day2_scenes_01_15.rpy"
SC_16_30 = GAME / "chapters/ch01/day2/ch01_day2_scenes_16_30.rpy"
PHONE = GAME / "screens/phone_sweetheart.rpy"

RESERVED = (("dialogue box", (0, 792, 1920, 288)), ("banner", (610, 0, 700, 116)))


def _entry(**kw):
    reg = {}
    args = dict(source="cg a", center=(400, 300), focus_rect=(200, 100, 600, 400),
                lines=["I noticed it."])
    args.update(kw)
    return lc_notice.register(reg, "n1", **args), reg


def _window(xa, ya, z, frame=lc_notice.FRAME):
    """Visible source rect for a full-frame image shown with Transform(xalign, yalign, zoom)."""
    w, h = frame
    vw, vh = w / z, h / z
    return (xa * (w - vw), ya * (h - vh), vw, vh)


class FocusTransformTests(unittest.TestCase):
    def test_zoom_is_clamped_to_the_cg_safe_range(self):
        self.assertEqual(lc_notice.clamp_zoom(1.6), 1.4)
        self.assertEqual(lc_notice.clamp_zoom(0.7), 1.0)
        self.assertEqual(lc_notice.clamp_zoom(1.35), 1.35)
        self.assertEqual(lc_notice.focus_transform((800, 400, 200, 200), 3.0)[2], 1.4)

    def test_centred_rect_aligns_to_the_middle(self):
        xa, ya, z = lc_notice.focus_transform((860, 440, 200, 200), 1.35)
        self.assertAlmostEqual(xa, 0.5, places=3)
        self.assertAlmostEqual(ya, 0.5, places=3)
        self.assertEqual(z, 1.35)

    def test_corner_rects_pin_to_the_frame_edges(self):
        self.assertEqual(lc_notice.focus_transform((0, 0, 100, 100), 1.35)[:2], (0.0, 0.0))
        self.assertEqual(lc_notice.focus_transform((1820, 980, 100, 100), 1.35)[:2], (1.0, 1.0))

    def test_visible_window_always_contains_the_focus_rect(self):
        for rect in ((200, 300, 600, 400), (0, 0, 300, 200), (1500, 700, 400, 300),
                     (620, 120, 560, 420), (330, 400, 520, 560)):
            xa, ya, z = lc_notice.focus_transform(rect, 1.35)
            wx, wy, ww, wh = _window(xa, ya, z)
            x, y, w, h = rect
            self.assertLessEqual(wx, x + 0.5, rect)
            self.assertLessEqual(wy, y + 0.5, rect)
            self.assertGreaterEqual(wx + ww, x + w - 0.5, rect)
            self.assertGreaterEqual(wy + wh, y + h - 0.5, rect)
            self.assertTrue(0.0 <= xa <= 1.0 and 0.0 <= ya <= 1.0)

    def test_caption_moves_to_the_top_when_the_detail_sits_under_the_dialogue_box(self):
        # A detail low in the CG (a hand under the dialogue box) gets the top caption spot.
        self.assertEqual(lc_notice.caption_slot((330, 560, 520, 500), 1.35), "top")
        self.assertEqual(lc_notice.caption_slot((640, 100, 520, 480), 1.35), "bottom")
        x, y, w, h = lc_notice.focus_on_screen((860, 440, 200, 200), 1.35)
        self.assertAlmostEqual(x + w / 2, 960, delta=1)
        self.assertAlmostEqual(y + h / 2, 540, delta=1)

    def test_a_rect_too_big_for_the_zoom_lowers_the_zoom(self):
        xa, ya, z = lc_notice.focus_transform((100, 100, 1600, 900), 1.4)
        self.assertLessEqual(z, 1920 / 1600)
        self.assertGreaterEqual(z, 1.0)
        full = lc_notice.focus_transform((0, 0, 1920, 1080), 1.4)
        self.assertEqual(full, (0.5, 0.5, 1.0))

    def test_rect_in_frame(self):
        self.assertTrue(lc_notice.rect_in_frame((0, 0, 1920, 1080)))
        self.assertTrue(lc_notice.rect_in_frame((10, 10, 100, 100)))
        for bad in ((-1, 0, 10, 10), (1900, 0, 30, 10), (0, 1000, 10, 100), (0, 0, 0, 10), (5, 5, 10)):
            self.assertFalse(lc_notice.rect_in_frame(bad), bad)


class RegisterTests(unittest.TestCase):
    def test_entry_keeps_every_field(self):
        entry, reg = _entry(zoom=1.3, lane_lines={"love": ["About her."]}, closeup="cg b",
                            day_id="ch01_d2", label="Morning", mood="noticed")
        self.assertIs(reg["n1"], entry)
        self.assertEqual(entry["lines"], ("I noticed it.",))
        self.assertEqual(entry["lane_lines"], {"love": ("About her.",)})
        self.assertEqual((entry["source"], entry["center"], entry["focus_rect"], entry["zoom"]),
                         ("cg a", (400, 300), (200, 100, 600, 400), 1.3))
        self.assertEqual((entry["closeup"], entry["day_id"], entry["label"], entry["mood"]),
                         ("cg b", "ch01_d2", "Morning", "noticed"))

    def test_duplicate_and_malformed_registrations_raise(self):
        _entry_, reg = _entry()
        with self.assertRaises(ValueError):
            lc_notice.register(reg, "n1", "cg a", (1, 1), (0, 0, 10, 10), lines=["x"])
        bad = (
            dict(lines=None),                                   # no caption at all
            dict(lines=[]),
            dict(lines=["one", "two", "three"]),                # 1-2 lines only
            dict(lines=[""]),
            dict(lines=["ok"], lane_lines={"nts_lane": ["x"]}),  # unknown lane key
            dict(lines=["ok"], lane_lines={"love": []}),
            dict(center=(1, 2, 3)),
            dict(focus_rect=(0, 0, 10)),
            dict(source=""),
        )
        for kw in bad:
            with self.assertRaises(ValueError, msg=repr(kw)):
                _entry(**kw)

    def test_lane_lines_alone_are_not_enough(self):
        with self.assertRaises(ValueError):
            _entry(lines=None, lane_lines={"love": ["x"]})

    def test_lanes_follow_the_stat_model_leans(self):
        self.assertEqual(lc_notice.LANES, ("love", "exhib", "ntr"))
        self.assertEqual(lc_notice.lane_from_lean("love"), "love")
        self.assertEqual(lc_notice.lane_from_lean("love_exhib"), "exhib")
        self.assertEqual(lc_notice.lane_from_lean("ntr"), "ntr")
        for lean in ("undecided", "strained", None, ""):
            self.assertIsNone(lc_notice.lane_from_lean(lean))

    def test_love_lean_with_an_exhibitionism_tint_takes_the_exhib_captions(self):
        # Day Two scene 1 comes before any Day Two choice, so the lean can't be love_exhib yet.
        self.assertEqual(lc_notice.lane_from_lean("love", "exhibitionism"), "exhib")
        for tint in ("shy", "love", "trust", "sharing", None):
            self.assertEqual(lc_notice.lane_from_lean("love", tint), "love", tint)
        # The tint never moves another lean (and never toward NTR).
        self.assertEqual(lc_notice.lane_from_lean("ntr", "exhibitionism"), "ntr")
        self.assertIsNone(lc_notice.lane_from_lean("undecided", "exhibitionism"))

    def test_every_bed_caption_lane_is_reachable_at_day_two_start(self):
        """Monte Carlo over Day One choice paths: at Day Two scene 1 (no Day Two choice yet) the
        bed notice can show its love, exhib and ntr captions, and the Love lane never gets ntr."""
        import random
        sys.path.insert(0, str(ROOT / "tests"))
        import lc_stat_model as m
        import test_route_simulation as rs
        rng = random.Random(228)
        seen = set()
        for _ in range(4000):
            stats = {s: m.DEFAULTS[m.STAT_GROUPS[s]][s] for s in m.STAT_ORDER}
            lean_exhib = rng.random()
            for menu in rs.D1 + [rs.DREAM]:
                if rng.random() < lean_exhib:
                    choice = max(menu, key=lambda c: sum(a for _g, s, a in rs.EFF[c] if s == "exhibitionism"))
                else:
                    choice = rng.choice(menu)
                for _g, stat, amount in rs.EFF[choice]:
                    stats[stat] = m.clamp(stats[stat] + amount)
            lane = m.d2_route_lane(stats, m.d1_route_pressure(stats), 0)
            self.assertIn(lane, ("love", "ntr_risk"))          # never Love + Exhib this early
            lean = m.lean_from_route_value(lane)
            caption_lane = lc_notice.lane_from_lean(lean, m.leia_tint(stats, "love") if lean == "love" else None)
            if lane == "love":
                self.assertNotEqual(caption_lane, "ntr")
            seen.add(caption_lane)
        self.assertEqual(seen, {"love", "exhib", "ntr"})

    def test_captions_pick_the_lane_then_fall_back(self):
        entry, _reg = _entry(lines=["Base."], lane_lines={"love": ["Love one.", "Love two."]})
        self.assertEqual(lc_notice.caption_lines(entry, "love"), ("Love one.", "Love two."))
        self.assertEqual(lc_notice.caption_lines(entry, "ntr"), ("Base.",))
        self.assertEqual(lc_notice.caption_lines(entry, None), ("Base.",))

    def test_fill_names(self):
        text = lc_notice.fill_names("[girlfriend_name] and [friend_name] and [player_name].",
                                    {"girlfriend_name": "Mia", "friend_name": None})
        self.assertEqual(text, "Mia and Julian and Ryan.")


class ValidateTests(unittest.TestCase):
    def problems(self, entry, pov=(), others=()):
        return lc_notice.validate(entry, 160, RESERVED, pov, others)

    def test_a_sound_entry_has_no_problems(self):
        entry, _ = _entry()
        self.assertEqual(self.problems(entry), [])

    def test_cue_must_stay_on_screen_and_clear_of_reserved_ui(self):
        for center in ((40, 300), (400, 760), (960, 60), (1900, 300)):
            entry, _ = _entry(center=center)
            self.assertTrue(self.problems(entry), center)

    def test_focus_rect_must_sit_inside_the_frame(self):
        entry, _ = _entry(focus_rect=(1800, 900, 300, 300))
        self.assertTrue(any("focus_rect" in p for p in self.problems(entry)))

    def test_zoom_outside_the_safe_range_is_reported(self):
        entry, _ = _entry(zoom=1.6)
        self.assertTrue(any("zoom" in p for p in self.problems(entry)))
        entry, _ = _entry(zoom=1.4)
        self.assertEqual(self.problems(entry), [])

    def test_overlap_with_a_hidden_pov_cue_on_the_same_cg_is_reported(self):
        entry, _ = _entry(center=(400, 300))
        pov = [("pov1", "cg a", (380, 280, 160, 160))]
        self.assertTrue(any("pov1" in p for p in self.problems(entry, pov)))
        # A POV on another CG never collides.
        self.assertEqual(self.problems(entry, [("pov1", "cg other", (380, 280, 160, 160))]), [])

    def test_overlap_with_another_notice_on_the_same_cg_is_reported(self):
        entry, _ = _entry(center=(400, 300))
        other, _ = _entry(center=(450, 320))
        other["id"] = "n2"
        self.assertTrue(any("n2" in p for p in self.problems(entry, others=[other])))

    def test_typed_default_names_in_captions_are_reported(self):
        entry, _ = _entry(lines=["Leia smiled."])
        self.assertTrue(any("name" in p for p in self.problems(entry)))
        entry, _ = _entry(lines=["Fine."], lane_lines={"ntr": ["Julian looked."]})
        self.assertTrue(any("name" in p for p in self.problems(entry)))

    def test_overlong_captions_are_reported(self):
        entry, _ = _entry(lines=["x" * (lc_notice.MAX_LINE_CHARS + 1)])
        self.assertTrue(any("long" in p for p in self.problems(entry)))

    def test_first_captions_fit_the_status_pin(self):
        ok = "x" * lc_notice.MAX_PIN_CHARS
        entry, _ = _entry(lines=[ok, "y" * lc_notice.MAX_LINE_CHARS])
        self.assertEqual(self.problems(entry), [])
        entry, _ = _entry(lines=[ok], lane_lines={"love": [ok + "x"]})
        self.assertTrue(any("Status pin" in p for p in self.problems(entry)))

    def test_caption_box_override_is_checked(self):
        entry, _ = _entry(caption_box=(790, 792, 998))
        self.assertEqual(self.problems(entry), [])
        self.assertEqual(lc_notice.caption_box(entry), (790, 792, 998, 222))
        for bad in ((1000, 792, 998), (790, 900, 998), (790, 792, 400)):
            entry, _ = _entry(caption_box=bad)
            self.assertTrue(any("caption_box" in p for p in self.problems(entry)), bad)
        with self.assertRaises(ValueError):
            _entry(caption_box=(1, 2))

    def test_default_caption_box_follows_the_slot(self):
        entry, _ = _entry(focus_rect=(330, 560, 520, 500))
        self.assertEqual(lc_notice.caption_box(entry), (132, 110, 1656, 222))
        entry, _ = _entry(focus_rect=(560, 40, 1300, 620), zoom=1.2)
        self.assertEqual(lc_notice.caption_box(entry), (132, 792, 1656, 222))


class FoundRecordTests(unittest.TestCase):
    def test_record_is_new_dict_and_idempotent(self):
        found = {}
        first = lc_notice.record(found, "n1", "love")
        self.assertEqual(first, {"n1": "love"})
        self.assertEqual(found, {})                     # never mutated in place (rollback)
        again = lc_notice.record(first, "n1", "ntr")
        self.assertIs(again, first)                     # the first answer stands
        self.assertTrue(lc_notice.noticed(first, "n1"))
        self.assertFalse(lc_notice.noticed(first, "n2"))
        self.assertTrue(lc_notice.noticed_any(first, ["n2", "n1"]))
        self.assertFalse(lc_notice.noticed_any(None, ["n1"]))      # old save
        self.assertFalse(lc_notice.noticed(None, "n1"))

    def test_pins_follow_registration_order_with_the_seen_lane(self):
        reg = {}
        lc_notice.register(reg, "b", "cg b", (400, 300), (100, 100, 500, 400), lines=["B base."],
                           lane_lines={"love": ["B love."]}, label="Breakfast")
        lc_notice.register(reg, "a", "cg a", (400, 300), (100, 100, 500, 400), lines=["A base."])
        pins = lc_notice.pins(reg, {"a": None, "b": "love"})
        self.assertEqual([p["id"] for p in pins], ["b", "a"])
        self.assertEqual(pins[0]["lines"], ("B love.",))
        self.assertEqual(pins[0]["label"], "Breakfast")
        self.assertEqual(pins[1]["label"], lc_notice.DEFAULT_LABEL)
        self.assertEqual(lc_notice.pins(reg, None), [])
        self.assertEqual(lc_notice.pins(reg, {"zzz": None}), [])

    def test_pin_row_has_one_fixed_height_at_any_count(self):
        heights = {lc_notice.pin_layout(n, 428)["height"] for n in range(0, 12)}
        self.assertEqual(len(heights), 1)
        self.assertFalse(lc_notice.pin_layout(1, 428)["overflow"])
        self.assertTrue(lc_notice.pin_layout(2, 428)["overflow"])

    def test_thumb_crop_keeps_the_pin_aspect_inside_the_frame(self):
        w, h = lc_notice.PIN_W - 16, lc_notice.PIN_THUMB_H
        for rect in ((300, 380, 600, 640), (620, 120, 560, 420), (0, 0, 100, 100),
                     (1800, 1000, 120, 80), (0, 0, 1920, 1080)):
            x, y, cw, ch = lc_notice.thumb_crop(rect, w, h)
            self.assertAlmostEqual(cw / ch, w / h, delta=0.02, msg=rect)
            self.assertTrue(lc_notice.rect_in_frame((x, y, cw, ch)), (rect, (x, y, cw, ch)))
            fx, fy, fw, fh = rect
            self.assertTrue(x <= fx + fw / 2 <= x + cw and y <= fy + fh / 2 <= y + ch, rect)


class NoticeRuntimeTests(unittest.TestCase):
    """The production init blocks of systems/notice.rpy (+ discovery) with engine stubs."""

    def setUp(self):
        self.calls = []
        self.store = SimpleNamespace(lc_notice_active=None, lc_notice_viewed=False,
                                     lc_noticed_record={}, lc_discoveries_found=set(),
                                     lc_discovery_review_cleared={}, lc_discovery_run_id="r",
                                     quick_menu=True, _windows_hidden=False,
                                     LC_POV_OPPORTUNITIES={}, lc_pov_active=None)
        self.showing = {"cg a"}
        renpy = SimpleNamespace(
            store=self.store,
            showing=lambda name, layer=None: name in self.showing,
            get_screen=lambda name: name == "say",
            stop_skipping=lambda: self.calls.append("stop_skipping"),
            retain_after_load=lambda: self.calls.append("retain_after_load"),
            show_screen=lambda name, **kw: self.calls.append(("show", name, kw)),
            hide_screen=lambda name: self.calls.append(("hide", name)),
            is_skipping=lambda: False,
            is_init_phase=lambda: True,
            has_image=lambda name, exact=True: True,
            log=lambda *a: None,
            notify=lambda *a: None,
            variant=lambda name: False,
        )
        self.lean = "love"
        self.tint = "shy"
        config = SimpleNamespace(developer=True, afm_callback=None, start_interact_callbacks=[],
                                 overlay_screens=[], screen_width=1920, screen_height=1080)
        self.env = dict(store=self.store, renpy=renpy, config=config,
                        persistent=SimpleNamespace(lc_days_cleared=set()),
                        current_choice_mode=lambda: "normal",
                        lc_phone_covers_scene=lambda: False, lc_journal_menu_open=lambda: False,
                        lc_current_lean=lambda: self.lean, _preferences=SimpleNamespace(transitions=1),
                        lc_leia_tint=lambda lane=None, lane_scene=False: self.tint,
                        LC_POV_RESERVED_RECTS=RESERVED, LC_POV_HITBOX=120, LC_POV_HITBOX_TOUCH=160,
                        lc_pov_reduce_motion=lambda: False, lc_ui_sound=lambda *a, **k: "x")
        load_blocks(["lc_discovery_register", "lc_notice_register"], self.env)
        self.store.LC_POV_OPPORTUNITIES = {}
        self.call("lc_notice_register", "n1", "cg a", (400, 300), (200, 100, 600, 400),
                  lines=["Base [girlfriend_name]."], lane_lines={"love": ["Love [girlfriend_name]."]},
                  day_id="ch01_d2", label="Morning", mood="noticed")
        self.store.girlfriend_name = "Mia"

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def test_registration_also_registers_a_notice_discovery(self):
        entry = lc_discovery.find(self.env["LC_DISCOVERIES"], "n1")
        self.assertEqual((entry["kind"], entry["day_id"], entry["label"], entry["image"]),
                         ("notice", "ch01_d2", "Morning", "cg a"))

    def test_open_outside_scope_or_when_inactive_records_nothing(self):
        self.assertIsNone(self.call("lc_notice_open", "n1"))
        self.assertFalse(self.call("lc_noticed", "n1"))
        self.call("lc_notice_begin", "n1")
        self.showing.clear()                                   # source CG gone
        self.assertIsNone(self.call("lc_notice_open", "n1"))
        self.assertFalse(self.call("lc_noticed", "n1"))

    def test_open_marks_the_record_and_discovery_once_and_survives_a_save(self):
        self.call("lc_notice_begin", "n1")
        self.assertTrue(self.call("lc_notice_available"))
        self.assertIsNone(self.call("lc_notice_open", "n1"))
        self.assertTrue(self.call("lc_noticed", "n1"))
        self.assertTrue(self.call("lc_discovery_found", "n1"))
        self.assertFalse(self.call("lc_pov_seen_in_save", "n1"))
        self.assertIn("retain_after_load", self.calls)
        self.assertIn(("show", "lc_notice_viewer", {"notice_id": "n1"}), self.calls)
        self.assertEqual(self.store.lc_noticed_record, {"n1": "love"})
        self.assertFalse(self.call("lc_notice_available"))      # viewed this encounter
        record = self.store.lc_noticed_record
        self.lean = "ntr"
        self.store.lc_notice_viewed = False
        self.call("lc_notice_open", "n1")
        self.assertIs(self.store.lc_noticed_record, record)     # no double count
        saved = pickle.loads(pickle.dumps(vars(self.store)))
        self.assertEqual(saved["lc_noticed_record"], {"n1": "love"})
        self.assertEqual(saved["lc_discoveries_found"], {"n1"})

    def test_rollback_restores_the_record_with_the_store(self):
        self.call("lc_notice_begin", "n1")
        before = dict(vars(self.store))
        self.call("lc_notice_open", "n1")
        for key, value in before.items():
            setattr(self.store, key, value)
        self.assertFalse(self.call("lc_noticed", "n1"))
        self.assertTrue(self.call("lc_notice_available"))

    def test_old_saves_read_as_nothing_noticed(self):
        del self.store.lc_noticed_record
        self.assertFalse(self.call("lc_noticed", "n1"))
        self.assertFalse(self.call("lc_noticed_any", "n1", "n2"))
        self.assertEqual(self.call("lc_notice_pins"), [])

    def test_captions_follow_the_lane_and_fill_names(self):
        self.assertEqual(self.call("lc_notice_captions", "n1"), ["Love Mia."])
        self.lean = "undecided"
        self.assertEqual(self.call("lc_notice_captions", "n1"), ["Base Mia."])
        self.assertEqual(self.call("lc_notice_captions", "n1", "love"), ["Love Mia."])

    def test_love_lean_with_an_exhibitionism_tint_uses_the_exhib_lane(self):
        self.tint = "exhibitionism"
        self.assertEqual(self.call("lc_notice_lane"), "exhib")
        self.assertEqual(self.call("lc_notice_captions", "n1"), ["Base Mia."])   # n1 has no exhib lines
        self.lean = "ntr"
        self.assertEqual(self.call("lc_notice_lane"), "ntr")

    def test_pins_show_the_caption_seen_at_the_time(self):
        self.call("lc_notice_begin", "n1")
        self.call("lc_notice_open", "n1")
        self.lean = "ntr"
        pins = self.call("lc_notice_pins")
        self.assertEqual([(p["id"], p["lines"]) for p in pins], [("n1", ["Love Mia."])])

    def test_scope_ends_cleanly(self):
        self.call("lc_notice_begin", "n1")
        self.call("lc_notice_end")
        self.assertIsNone(self.store.lc_notice_active)
        self.assertFalse(self.call("lc_notice_available"))
        with self.assertRaises(ValueError):
            self.call("lc_notice_begin", "nope")

    def test_screen_actions_return_none(self):
        self.call("lc_notice_begin", "n1")
        for name in ("lc_notice_open", "lc_notice_close", "lc_notice_hover_sound"):
            args = ("n1",) if name == "lc_notice_open" else ()
            self.assertIsNone(self.call(name, *args), name)

    def test_validation_reports_a_cue_on_a_pov_spot(self):
        self.store.LC_POV_OPPORTUNITIES = {"pov1": {"source": "cg a", "center": (420, 310)}}
        report = self.call("lc_notice_validate_all")
        self.assertIn("n1", report)
        self.store.LC_POV_OPPORTUNITIES = {}
        self.assertEqual(self.call("lc_notice_validate_all"), {})


class SourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = SYSTEM.read_text(encoding="utf-8")
        cls.screen = SCREEN.read_text(encoding="utf-8")

    def test_viewer_is_modal_above_the_banner_and_never_returns(self):
        viewer = self.screen[self.screen.index("\nscreen lc_notice_viewer("):]
        viewer = viewer[:viewer.index("\nscreen ", 1)] if "\nscreen " in viewer[1:] else viewer
        self.assertIn("modal True", viewer)
        self.assertGreater(int(viewer.split("zorder", 1)[1].split()[0]), 620)
        self.assertIn("keyboard_focus False", viewer)          # the full-screen click target
        for key in ('key "K_ESCAPE"', 'key "game_menu"', 'key "mouseup_3"'):
            self.assertIn(key, viewer)
        self.assertNotIn("Return(", self.screen)
        self.assertNotIn("call screen", self.system + self.screen)

    def test_push_in_and_ease_back_with_an_instant_path(self):
        self.assertIn("transform lc_notice_push(", self.screen)
        self.assertIn("transform lc_notice_pull(", self.screen)
        self.assertIn("lc_notice_instant()", self.screen)
        self.assertIn("def lc_notice_instant", self.system)
        self.assertIn("renpy.is_skipping()", self.system)
        self.assertIn("lc_pov_reduce_motion()", self.system)

    def test_cue_is_a_focusable_button_with_alt_text_and_eye_art(self):
        hotspot = self.screen[self.screen.index("\nscreen lc_notice_hotspot_body("):]
        self.assertIn("button:", hotspot)
        self.assertIn("hover_background lc_notice_cue_art(size, True", hotspot)
        self.assertIn('alt ("Something you noticed: " + cue_label', hotspot)
        self.assertNotIn("keyboard_focus False", hotspot.split("screen lc_notice_viewer")[0])
        for name in ("eye_idle", "eye_hover", "eye_disc_idle", "eye_disc_hover"):
            svg = (GAME / "gui/notice" / (name + ".svg")).read_text(encoding="utf-8")
            self.assertIn("<svg", svg)
        gen = (ROOT / "tools/gen_pov_cue_assets.py").read_text(encoding="utf-8")
        self.assertIn("def eye_svg(", gen)

    def test_open_is_the_only_writer_of_the_record(self):
        self.assertEqual(self.system.count("lc_notice.record("), 1)
        self.assertEqual(self.system.count("lc_discovery_mark(notice_id)"), 1)
        opener = self.system[self.system.index("def lc_notice_open"):self.system.index("def lc_notice_close")]
        self.assertIn("lc_notice.record(", opener)
        self.assertIn("renpy.retain_after_load()", opener)
        self.assertIn("renpy.stop_skipping()", opener)

    def test_validation_runs_after_every_registration(self):
        self.assertIn("init 999 python:", self.system)
        self.assertIn("lc_notice_validate_all()", self.system)

    def test_status_app_draws_the_pins_in_one_fixed_row(self):
        phone = PHONE.read_text(encoding="utf-8")
        status = phone[phone.index("screen lc_phone_status():"):]
        self.assertIn("lc_notice_pins()", status)
        self.assertIn("use lc_phone_notice_pins(", status)
        pins = self.screen[self.screen.index("\nscreen lc_phone_notice_pins("):]
        self.assertIn('"Things I noticed"', pins)
        self.assertIn("lc_notice.pin_layout(", pins)
        self.assertIn("viewport", pins)
        self.assertIn("ysize lc_notice.PIN_H", pins)


class DayTwoNoticeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visuals = VISUALS.read_text(encoding="utf-8")
        cls.early = SC_01_15.read_text(encoding="utf-8")
        cls.late = SC_16_30.read_text(encoding="utf-8")

    def registrations(self):
        return re.findall(r'lc_notice_register\(\s*"(\w+)",\s*source="([^"]+)"', self.visuals)

    def test_two_notices_on_finished_day_two_cgs(self):
        regs = self.registrations()
        self.assertEqual(len(regs), 2, regs)
        for notice_id, source in regs:
            name = source.split(" ", 1)[1]
            m = re.search(r"^image cg %s = At\(\"(images/cg/[^\"]+)\"" % re.escape(name), self.visuals, re.M)
            self.assertIsNotNone(m, "%s must be real (file-backed) art" % source)
            self.assertTrue((GAME / m.group(1)).is_file(), m.group(1))

    def test_each_notice_is_scoped_in_the_story_and_every_lane_gets_a_love_caption(self):
        for notice_id, source in self.registrations():
            self.assertEqual(self.early.count('$ lc_notice_begin("%s")' % notice_id), 1, notice_id)
            start = self.early.index('$ lc_notice_begin("%s")' % notice_id)
            self.assertIn("scene " + source, self.early[max(0, start - 200):start])
            self.assertIn("$ lc_notice_end()", self.early[start:start + 4000])
            block = self.visuals[self.visuals.index('"%s"' % notice_id):]
            block = block[:block.index("\n    )")]
            self.assertIn("day_id=\"ch01_d2\"", block)
            for lane in ("love", "exhib", "ntr"):
                self.assertIn('"%s": [' % lane, block, (notice_id, lane))
            self.assertIn("[girlfriend_name]", block[block.index('"love": ['):])
            self.assertNotRegex(block, r"\b(Ryan|Leia|Julian)\b")

    def test_sunset_option_only_after_a_named_notice_on_the_shared_tail(self):
        start = self.late.index("label ch01_day2_scene_20_dinner_outfit:")
        end = self.late.index("label ch01_day2_scene_21_pre_sunset:")
        scene = self.late[start:end]
        tail = scene[scene.index("    else:\n        \"[girlfriend_name] stood beside me"):]
        tail = tail[tail.index("\n    if lc_noticed_any("):]
        self.assertLess(tail.index("lc_noticed_any("), tail.index("A few minutes later"))
        self.assertIn('format_choice("ch01_d2_sunset_noticed"', tail)
        self.assertIn('$ apply_choice("ch01_d2_sunset_noticed")', tail)
        self.assertIn('not get_story_value("ch01_d2_ntr_soft_gate", False)', tail.split("\n")[1])
        for notice_id, _src in self.registrations():
            self.assertIn('"%s"' % notice_id, tail.split("\n")[1])

    def test_sunset_option_is_scored_as_a_love_choice(self):
        sys.path.insert(0, str(ROOT / "tests"))
        from lc_effective_effects import effective_effects
        import lc_stat_model as m
        effects = effective_effects()["ch01_d2_sunset_noticed"]
        self.assertEqual(m.scoring_violations("ch01_d2_sunset_noticed", effects), [])
        self.assertEqual(m.choice_route_tag("ch01_d2_sunset_noticed", effects), "Love")


if __name__ == "__main__":
    unittest.main()


class AltTextInterpolationTests(unittest.TestCase):
    """Self-voicing reads a button's alt text outside the screen's scope, so a screen-local
    [variable] in a quoted alt string raises NameError on hover (crash seen 2026-11-18)."""

    def test_no_alt_string_interpolates_a_variable(self):
        import pathlib, re
        game = pathlib.Path(__file__).resolve().parents[1] / "game"
        bad = []
        for path in game.rglob("*.rpy"):
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if re.match(r'\s*alt\s+"[^"]*\[[^\[]', line):
                    bad.append(f"{path.relative_to(game)}:{n}")
        self.assertEqual(bad, [])
