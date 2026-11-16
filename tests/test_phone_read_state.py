"""Reading a thread (e.g. opened from a notification) leaves no unread badge (darryn 2026-11-08)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
import lc_rpy_model as m  # noqa: E402

# Found by what they define, so the checks follow the code when files are merged or moved.
_DEFS = m.effective("def")
_SCREENS = m.effective("screen")


class PhoneReadStateTests(unittest.TestCase):

    def test_messages_into_open_thread_are_read(self):
        wrapper = _DEFS["phone_add_message"].body.split("phone_store_message(", 1)[0]
        self.assertIn("if mark_unread and lc_phone_thread_open(thread_id):", wrapper)
        self.assertIn("mark_unread = False", wrapper)

    def test_leaving_thread_marks_read(self):
        screen = _SCREENS["phone_screen"].body
        self.assertIn('on "hide" action [Function(lc_phone_leave_thread, phone_app, phone_thread)', screen)
        self.assertIn('lc_phone_leave_thread(app, thread)', _DEFS["lc_phone_back"].body)
        self.assertIn('action Function(lc_phone_back)', screen)


if __name__ == "__main__":
    unittest.main()
