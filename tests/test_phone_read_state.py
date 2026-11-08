"""Reading a thread (e.g. opened from a notification) leaves no unread badge (darryn 2026-11-08)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGIC = (ROOT / "game/systems/zz_phone_presentation_logic.rpy").read_text(encoding="utf-8")
PHONE = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")


class PhoneReadStateTests(unittest.TestCase):

    def test_messages_into_open_thread_are_read(self):
        wrapper = LOGIC.split("    def phone_add_message(", 1)[1].split("_phone_add_message_base(", 1)[0]
        self.assertIn("if mark_unread and lc_phone_thread_open(thread_id):", wrapper)
        self.assertIn("mark_unread = False", wrapper)

    def test_leaving_thread_marks_read(self):
        self.assertIn('on "hide" action [Function(lc_phone_leave_thread, phone_app, phone_thread)', PHONE)
        self.assertIn('Function(lc_phone_leave_thread, phone_app, phone_thread), Function(lc_ui_play, "back"), SetScreenVariable("phone_app", "messages")', PHONE)


if __name__ == "__main__":
    unittest.main()
