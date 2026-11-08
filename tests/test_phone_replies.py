"""Phone reply cards: executable Ren'Py Python blocks with a small store stub."""
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def load_logic():
    values = {}
    store = SimpleNamespace(
        phone_messages={"leia": [], "julian": [], "group": []},
        phone_photos=[], phone_reply_prompts={}, phone_last_open_thread=None,
        player_name="Ryan", girlfriend_name="Leia", friend_name="Julian",
    )
    renpy = SimpleNamespace(store=store, get_screen=lambda *a, **kw: None,
                            restart_interaction=lambda: None)
    story = {}
    env = {
        "renpy": renpy,
        "has_story_value": lambda key: key in story,
        "set_story_value": lambda key, value: story.__setitem__(key, value),
        "phone_queue_notification": lambda *a, **kw: None,
    }
    for relative in ("game/systems/phone_state.rpy", "game/systems/zz_phone_presentation_logic.rpy"):
        source = (ROOT / relative).read_text(encoding="utf-8")
        block = textwrap.dedent(source.split("init python:\n", 1)[1])
        exec(compile(block, relative, "exec"), env)
    return env, story, store


class PhoneRepliesTest(unittest.TestCase):
    def setUp(self):
        self.api, self.story, self.store = load_logic()
        self.options = [
            {"id": "yes", "text": "Yeah bro", "followups": [("julian", "Cheers")]},
            {"id": "other", "text": "The last one"},
        ]
        self.offer = self.api["phone_offer_reply"]
        self.add = self.api["phone_add_message"]

    def test_selected_reply_waits_for_staged_delivery(self):
        self.add("group", "julian", "Photos", message_id="first")
        self.offer("group", "pool_pick", self.options, "yes")
        self.assertIsNone(self.api["phone_select_reply"]("group", "yes"))
        self.assertEqual([m["id"] for m in self.store.phone_messages["group"]], ["first"])
        self.assertEqual(len(self.store.phone_reply_delivery["group"]), 2)
        self.api["phone_deliver_reply_step"]("group")
        self.assertEqual([m["id"] for m in self.store.phone_messages["group"]],
                         ["first", "pool_pick_ryan"])
        self.api["phone_deliver_reply_step"]("group")
        self.assertEqual([m["id"] for m in self.store.phone_messages["group"]],
                         ["first", "pool_pick_ryan", "pool_pick_followup_01"])
        self.assertFalse(self.store.phone_reply_delivery.get("group"))

    def test_deadline_flushes_pending_steps_before_next_incoming(self):
        self.add("group", "julian", "Photos", message_id="first")
        self.offer("group", "pool_pick", self.options, "yes")
        self.api["phone_select_reply"]("group", "yes")
        self.add("group", "leia", "Next", message_id="next")
        self.assertEqual([m["id"] for m in self.store.phone_messages["group"]],
                         ["first", "pool_pick_ryan", "pool_pick_followup_01", "next"])

    def test_reply_choices_live_in_a_distinct_tray_not_outgoing_bubbles(self):
        source = (ROOT / "game/screens/zzzzzz_phone_ios_presentation.rpy").read_text(encoding="utf-8")
        tray = source.split('            if reply_prompt:\n                frame:', 1)[1].split('            text "+":', 1)[0]
        self.assertIn('reply_choice.png', tray)
        self.assertIn('row_hover.png', tray)
        self.assertNotIn('bubble_out.png', tray)
        self.assertIn('Choose a reply', source)

    def test_reply_delivery_is_timed_only_while_thread_open(self):
        source = (ROOT / "game/chapters/ch01/zz_ch01_phone_sequence_revision.rpy").read_text(encoding="utf-8")
        self.assertIn('phone_reply_delivery', source)
        self.assertIn('timer 0.55 action Function(phone_deliver_reply_step, "group")', source)
        self.assertIn('if _ch01_group_thread_open:', source)

    def test_all_six_photo_followups_react_to_already_shared_photos(self):
        import re
        files = ("game/chapters/ch01/ch01_photo_route_phone_patch.rpy",
                 "game/chapters/ch01/zzzz_ch01_scene27_staged_phone.rpy")
        followups = []
        for name in files:
            source = (ROOT / name).read_text(encoding="utf-8")
            followups.extend(re.findall(r'"followups": \[\("(?:julian|leia)", "([^"]+)"\)\]', source))
        self.assertEqual(len(followups), 6)
        self.assertFalse(any(re.search(r'\bsend\b', text, re.I) for text in followups))

    def test_open_thread_does_not_pick_and_manual_reply_posts_followup(self):
        self.add("group", "julian", "Photos", message_id="first")
        self.offer("group", "pool_pick", self.options, "yes")
        self.api["phone_mark_thread_read"]("group")
        self.assertNotIn("pool_pick", self.story)
        self.assertIsNone(self.api["phone_select_reply"]("group", "other"))
        self.assertEqual(self.story["pool_pick"], "other")
        self.assertEqual([m["sender"] for m in self.store.phone_messages["group"]], ["julian"])
        self.api["phone_deliver_reply_step"]("group")
        self.assertEqual([m["sender"] for m in self.store.phone_messages["group"]],
                         ["julian", "player"])
        self.assertFalse(self.api["phone_choose_reply"]("group", "yes"))
        self.assertFalse(self.offer("group", "pool_pick", self.options, "yes"))

    def test_default_precedes_next_incoming_and_followup(self):
        self.add("group", "julian", "Photos", message_id="first")
        self.offer("group", "pool_pick", self.options, "yes")
        self.add("leia", "leia", "Different thread", message_id="leia_1")
        self.assertIsNotNone(self.api["phone_pending_reply"]("group"))
        self.add("group", "julian", "Late photo", message_id="next")
        self.assertEqual(self.story["pool_pick"], "yes")
        self.assertEqual([(m["id"], m["sender"]) for m in self.store.phone_messages["group"]],
                         [("first", "julian"), ("pool_pick_ryan", "player"),
                          ("pool_pick_followup_01", "julian"), ("next", "julian")])
        self.assertEqual(self.api["phone_thread_unread_count"]("group"), 2)

    def test_replayed_message_does_not_consume_and_invalid_choice_is_safe(self):
        self.add("group", "julian", "Photos", message_id="first")
        self.offer("group", "pool_pick", self.options, "yes")
        self.assertFalse(self.add("group", "julian", "Photos", message_id="first"))
        self.assertFalse(self.api["phone_choose_reply"]("group", "missing"))
        self.assertNotIn("pool_pick", self.story)
        self.assertTrue(self.api["phone_default_reply"]("group"))
        self.assertFalse(self.api["phone_default_reply"]("group"))

    def test_old_save_without_prompt_field(self):
        del self.store.phone_reply_prompts
        self.assertIsNone(self.api["phone_pending_reply"]("group"))
        self.assertTrue(self.add("group", "julian", "Hello", message_id="old"))

    def test_reject_invalid_prompt(self):
        with self.assertRaises(ValueError):
            self.offer("group", "bad", self.options, "unknown")


if __name__ == "__main__":
    unittest.main()
