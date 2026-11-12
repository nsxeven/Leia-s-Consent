"""Day Two story-local phone time must not leak into unrelated scenes."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHONE_STATE = (ROOT / "game/systems/phone_state.rpy").read_text(encoding="utf-8")
PHONE_LOGIC = (ROOT / "game/systems/zz_phone_presentation_logic.rpy").read_text(encoding="utf-8")
PHONE_UI = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
SCENE = (ROOT / "game/chapters/ch01/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")


class DayTwoPhoneTimeTests(unittest.TestCase):
    def test_message_time_is_optional_and_save_safe(self):
        self.assertIn('"display_time": display_time or getattr(renpy.store, "lc_phone_story_time", None)', PHONE_STATE)
        self.assertIn("display_time=None", PHONE_STATE)
        self.assertIn("display_time=display_time", PHONE_LOGIC)
        self.assertIn('lc_phone_set_story_time("11:00")', SCENE)
        self.assertIn("lc_phone_clear_story_time()", SCENE)

    def test_thread_surfaces_use_delivered_time(self):
        self.assertIn("def lc_phone_thread_clock_text(thread_id):", PHONE_UI)
        self.assertIn('text "[lc_phone_thread_clock_text(phone_thread)]"', PHONE_UI)
        self.assertIn('text "Today · [lc_phone_thread_clock_text(phone_thread)]"', PHONE_UI)
        self.assertIn('text "Read [lc_phone_thread_clock_text(phone_thread)]"', PHONE_UI)


if __name__ == "__main__":
    unittest.main()
