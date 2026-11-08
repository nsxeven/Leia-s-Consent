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
    renpy = SimpleNamespace(store=store, get_screen=lambda *a, **kw: None)
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

    def test_open_thread_does_not_pick_and_manual_reply_posts_followup(self):
        self.add("group", "julian", "Photos", message_id="first")
        self.offer("group", "pool_pick", self.options, "yes")
        self.api["phone_mark_thread_read"]("group")
        self.assertNotIn("pool_pick", self.story)
        self.assertIsNone(self.api["phone_select_reply"]("group", "other"))
        self.assertEqual(self.story["pool_pick"], "other")
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
