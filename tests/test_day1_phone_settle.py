"""Day One's waiting group replies land before Day Two's first text (darryn 2026-11-19)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D2 = (ROOT / "game/chapters/ch01/day2/ch01_day2_scenes_01_15.rpy").read_text(encoding="utf-8")
D1 = (ROOT / "game/chapters/ch01/day1/ch01_phone_moments.rpy").read_text(encoding="utf-8")


class Day1PhoneSettle(unittest.TestCase):
    def test_settle_runs_before_bro_wake_up(self):
        settle = D2.index("$ ch01_day1_settle_pending_phone()")
        self.assertLess(settle, D2.index('lc_phone_set_story_time("11:00")'))
        self.assertLess(settle, D2.index('message_id="ch01_d2_julian_wake_up"'))

    def test_settle_lands_both_pending_chains_silently(self):
        body = D1.split("def ch01_day1_settle_pending_phone():", 1)[1].split("    def ", 1)[0]
        for key in ("ch01_late_photo_followup_pending", "ch01_breakfast_reply_pending",
                    'message_id="ch01_trip_group_breakfast_leia_reply"', "notify=False",
                    "lc_phone_story_time = None", "lc_phone_story_time = prev_time"):
            self.assertIn(key, body)


if __name__ == "__main__":
    unittest.main()
