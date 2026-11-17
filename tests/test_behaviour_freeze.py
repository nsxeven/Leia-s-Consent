"""Characterization tests: what wrapped/overridden functions do today.

These pin observable behaviour (not file locations) of functions that the
clean-up folds or moves, so a fold that drops a side effect fails here.
Phone delivery, day review and tag collection are pinned by
test_phone_replies, test_phone_read_state, test_day_review and
test_tag_collection; this file covers what those do not.
"""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lc_rpy_harness import load  # noqa: E402


class StoryFlagHookTests(unittest.TestCase):
    """set_story_flag also unlocks Chapter Select after the first finished Day Two."""

    def setUp(self):
        self.persistent = SimpleNamespace()
        self.store = SimpleNamespace(story_flags={}, story_values={})
        self.env = load(["set_story_flag", "has_story_flag",
                         "_lc_hooks", "lc_hook_add", "lc_hook_run", "chapter_select_unlock_after_day_two"],
                        dict(renpy=SimpleNamespace(store=self.store), persistent=self.persistent))

    def test_value_is_stored_and_returned_as_bool(self):
        self.assertIs(self.env["set_story_flag"]("some_flag", "yes"), True)
        self.assertIs(self.store.story_flags["some_flag"], True)

    def test_day_two_complete_unlocks_chapter_select(self):
        self.assertTrue(self.env["set_story_flag"]("ch01_day_02_complete"))
        self.assertTrue(self.store.story_flags["ch01_day_02_complete"])
        self.assertTrue(self.persistent.ch01_chapter_select_unlocked)

    def test_other_flags_do_not_unlock(self):
        self.env["set_story_flag"]("ch01_day_01_complete")
        self.assertFalse(getattr(self.persistent, "ch01_chapter_select_unlocked", False))

    def test_false_value_stores_false_and_does_not_unlock(self):
        self.assertFalse(self.env["set_story_flag"]("ch01_day_02_complete", False))
        self.assertFalse(self.store.story_flags["ch01_day_02_complete"])
        self.assertFalse(getattr(self.persistent, "ch01_chapter_select_unlocked", False))


class ApplyChoiceTests(unittest.TestCase):
    """The apply_choice the game runs: stats, history, review note, feedback, onboarding."""

    def setUp(self):
        self.calls = []
        self.store = SimpleNamespace(choice_history=[], last_choice_id=None)
        effects = {"c_up": [("relationship", "love", 2), ("partner", "exhibitionism", -1)]}
        env = dict(
            renpy=SimpleNamespace(store=self.store),
            get_choice_effects=lambda cid: effects.get(cid, []),
            # No choice_effects filter registered: the effective effects are the registered ones.
            lc_choice_effective_effects=lambda cid: effects.get(cid, []),
            lc_hook_run=lambda event, *a: self.calls.append(("hook", event) + a),
            change_stat=lambda g, s, a: self.calls.append(("stat", g, s, a)),
            # The snapshot is what has been changed so far: it must be taken BEFORE any stat moves.
            lc_review_stats=lambda: tuple(c for c in self.calls if c[0] == "stat"),
            lc_review_note_choice=lambda cid, before: self.calls.append(("review", cid, before)),
            show_choice_feedback=lambda cid, fx=None: self.calls.append(("feedback", cid)),
            maybe_show_status_choice_tutorial=lambda cid: self.calls.append(("tutorial", cid)),
        )
        # Only apply_choice is loaded; its collaborators are the stubs above.
        self.env = load(["apply_choice"], env)

    def test_effects_history_review_feedback_in_order(self):
        self.assertEqual(self.env["apply_choice"]("c_up"), "c_up")
        self.assertEqual(self.calls, [
            ("stat", "relationship", "love", 2),
            ("stat", "partner", "exhibitionism", -1),
            ("hook", "choice_applied", "c_up", [("relationship", "love", 2), ("partner", "exhibitionism", -1)]),
            ("review", "c_up", ()),
            ("feedback", "c_up"),
            ("tutorial", "c_up"),
        ])
        self.assertEqual(self.store.last_choice_id, "c_up")
        self.assertEqual(self.store.choice_history, ["c_up"])

    def test_choice_without_effects_is_still_recorded(self):
        self.env["apply_choice"]("c_flavour")
        self.assertEqual(self.store.choice_history, ["c_flavour"])
        self.assertIn(("review", "c_flavour", ()), self.calls)


class PhoneAddMessageTests(unittest.TestCase):
    """The effective phone_add_message (base writer + presentation wrapper)."""

    def setUp(self):
        self.open_thread = None
        self.events = []
        self.store = SimpleNamespace(phone_messages={"group": [], "leia": []}, phone_photos=[])
        stubs = dict(
            renpy=SimpleNamespace(store=self.store),
            lc_phone_thread_open=lambda t: t == self.open_thread,
            phone_default_reply=lambda t: self.events.append(("default_reply", t)),
            phone_flush_reply_delivery=lambda t: self.events.append(("flush", t)),
            lc_phone_message_pop=lambda t: self.events.append(("pop", t)),
            phone_queue_notification=lambda *a, **kw: self.events.append(("notify", a[1], a[2])),
            phone_show_notification=lambda *a, **kw: self.events.append(("toast",) + a),
            phone_thread_label=lambda t: t.title(),
            phone_sender_label=lambda s: s.title(),
            phone_add_photo=lambda *a, **kw: self.events.append(("photo", a[1])),
        )
        self.env = load(["_phone_ensure_thread", "phone_has_message", "phone_add_message",
                         "phone_store_message"], stubs)

    def thread(self, t):
        return self.store.phone_messages[t]

    def test_incoming_to_closed_thread_is_unread_and_notifies_once(self):
        self.assertTrue(self.env["phone_add_message"]("leia", "leia", text="hi", message_id="m1", notify=True))
        self.assertFalse(self.thread("leia")[0]["read"])
        self.assertEqual([e for e in self.events if e[0] in ("notify", "toast")], [("notify", "Leia", "hi")])
        self.assertEqual(self.events[:2], [("default_reply", "leia"), ("flush", "leia")])

    def test_incoming_to_open_thread_is_read(self):
        self.open_thread = "group"
        self.env["phone_add_message"]("group", "julian", text="pic", message_id="m2")
        self.assertTrue(self.thread("group")[0]["read"])
        self.assertIn(("pop", "group"), self.events)

    def test_stable_id_replay_is_ignored(self):
        self.env["phone_add_message"]("leia", "leia", text="hi", message_id="m3", notify=True)
        self.events.clear()
        self.assertFalse(self.env["phone_add_message"]("leia", "leia", text="hi", message_id="m3", notify=True))
        self.assertEqual(len(self.thread("leia")), 1)
        self.assertEqual(self.events, [])

    def test_player_message_does_not_trigger_deadline_or_notification(self):
        self.env["phone_add_message"]("leia", "player", text="ok", message_id="m4", notify=True)
        self.assertEqual(self.events, [])
        self.assertTrue(self.thread("leia")[0]["read"])

    def test_attachment_goes_to_photos(self):
        self.env["phone_add_message"]("group", "julian", attachment_id="pool_1", message_id="m5")
        self.assertIn(("photo", "pool_1"), self.events)


class PhoneReplyStepTests(unittest.TestCase):
    """One staged reply beat: stored as read, no notification, pop only for incoming."""

    def setUp(self):
        self.events = []
        self.store = SimpleNamespace(phone_reply_delivery={
            "group": [("player", "ok", "r1"), ("julian", "nice", "r2")]})
        stubs = dict(
            renpy=SimpleNamespace(store=self.store, restart_interaction=lambda: None),
            phone_store_message=lambda *a, **kw: self.events.append(("store", a[0], a[1], kw)) or True,
            lc_phone_message_pop=lambda t: self.events.append(("pop", t)),
            # Phone moments: no hesitation typing in progress.
            phone_reply_typing_text=lambda t: None,
            phone_reply_typing_clear=lambda t=None: None,
        )
        self.env = load(["phone_deliver_reply_step"], stubs)

    def test_player_beat_then_incoming_beat(self):
        step = self.env["phone_deliver_reply_step"]
        step("group")
        self.assertEqual([e[0] for e in self.events], ["store"])
        self.assertEqual(self.events[0][3], {"text": "ok", "message_id": "r1",
                                             "mark_unread": False, "notify": False})
        step("group")
        self.assertEqual(self.events[-1], ("pop", "group"))
        self.assertNotIn("group", self.store.phone_reply_delivery)


if __name__ == "__main__":
    unittest.main()
