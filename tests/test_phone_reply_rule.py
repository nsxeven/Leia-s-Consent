"""Phone replies are picked inside the phone (darryn 2026-11-19).

A reply meant for Messages (or the feed) is never a dialogue menu: scenes offer a reply card
(phone_offer_reply, scored options carry "choice_id") and wait with lc_phone_await_reply.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
MOMENTS = (GAME / "systems/phone_moments.rpy").read_text(encoding="utf-8")
LOGIC = (GAME / "systems/phone_presentation_logic.rpy").read_text(encoding="utf-8")
HIDDEN = (GAME / "systems/hidden_pov.rpy").read_text(encoding="utf-8")


def scene_files():
    return sorted((GAME / "chapters").rglob("*.rpy"))


class PhoneReplyRuleTests(unittest.TestCase):
    def test_no_menu_option_sends_a_phone_message(self):
        offenders = []
        for path in scene_files():
            lines = path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                if "phone_send_player_message" not in line:
                    continue
                indent = len(line) - len(line.lstrip())
                for j in range(i - 1, max(-1, i - 12), -1):
                    prev = lines[j]
                    if not prev.strip():
                        continue
                    prev_indent = len(prev) - len(prev.lstrip())
                    if prev_indent < indent:
                        if re.match(r'\s*".*"\s*(if .*)?:\s*$', prev):
                            offenders.append("%s:%d" % (path.relative_to(ROOT), i + 1))
                        break
        self.assertEqual(offenders, [], "phone replies belong on a reply card, not a menu")

    def test_await_label_scores_once(self):
        self.assertIn("label lc_phone_await_reply(thread_id):", MOMENTS)
        self.assertIn("call screen lc_phone_await(thread_id)", MOMENTS)
        self.assertIn("lc_phone_scored_replies", MOMENTS)
        self.assertIn("apply_choice(choice_id)", MOMENTS)

    def test_reply_cards_keep_save_ids(self):
        self.assertIn('option.get("message_id") or prompt["id"] + "_ryan"', LOGIC)
        self.assertIn("2 <= len(ids) <= 4", LOGIC)

    def test_scored_cards_are_awaited(self):
        for path in scene_files():
            src = path.read_text(encoding="utf-8")
            for m in re.finditer(r'phone_offer_reply\("(\w+)", "(\w+)", \[(.*?)\], "\w+"\)', src, re.S):
                if '"choice_id"' in m.group(3) and "ch01_d2_maya_dm" != m.group(2):
                    rest = src[m.end():m.end() + 400]
                    self.assertIn('call lc_phone_await_reply("%s")' % m.group(1), rest, m.group(2))


class HiddenPovPlacementTests(unittest.TestCase):
    def test_eye_and_temple_placement(self):
        self.assertIn("def lc_pov_temple_center(eye, temple):", HIDDEN)
        self.assertIn("eye=None, temple=None", HIDDEN)
        visuals = (GAME / "chapters/ch01/day2/ch01_day2_visuals.rpy").read_text(encoding="utf-8")
        block = visuals.split('"d2_boutique_stranger"', 1)[1].split(")", 3)
        self.assertIn('temple="left"', visuals.split('"d2_boutique_stranger"', 1)[1][:600])


if __name__ == "__main__":
    unittest.main()
