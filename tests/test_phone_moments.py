"""Phone moments: incoming calls, hesitation typing, leave on read.

Pure rules: game/python-packages/lc_phone_moments.py. Ren'Py side: game/systems/phone_moments.rpy
(calls, read receipts, discovery registration), the reply-card additions in
game/systems/phone_presentation_logic.rpy (leave_on_read / hesitate options, typing hold) and the
screens in game/screens/phone_call.rpy and game/screens/phone_sweetheart.rpy.
"""
import pickle
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "game" / "python-packages"))
sys.path.insert(0, str(ROOT / "tests"))

import lc_phone_moments as pm  # noqa: E402
from lc_rpy_harness import load_blocks  # noqa: E402


def _prefix_of(frame, *texts):
    return any(t.startswith(frame) for t in texts)


class HesitationFramesTests(unittest.TestCase):
    def test_skip_gives_no_frames(self):
        self.assertEqual(pm.hesitation_frames("I miss", "I'm fine.", skip=True), [])

    def test_empty_final_gives_no_frames(self):
        self.assertEqual(pm.hesitation_frames("draft", ""), [])
        self.assertEqual(pm.hesitation_frames(None, None), [])

    def test_type_pause_delete_retype(self):
        frames = pm.hesitation_frames("I miss you", "I'm fine.")
        self.assertEqual(frames[0], "I")
        self.assertEqual(frames[-1], "I'm fine.")
        # Types the whole draft, one character a frame.
        draft_at = frames.index("I miss you")
        self.assertEqual(frames[:draft_at + 1], ["I miss you"[:n] for n in range(1, 11)])
        # Pauses on it.
        self.assertGreaterEqual(frames.count("I miss you"), pm.PAUSE_FRAMES)
        # Deletes back to the common prefix ("I"), never below it.
        shortest = min(len(f) for f in frames[draft_at:])
        self.assertEqual(shortest, 1)
        after = frames[draft_at:]
        dip = [len(f) for f in after]
        low = dip.index(1)
        self.assertEqual(dip[:low + 1], sorted(dip[:low + 1], reverse=True))
        # Retypes the final text, growing to it.
        tail = after[low:]
        self.assertEqual([len(f) for f in tail], sorted(len(f) for f in tail))
        for frame in frames:
            self.assertTrue(_prefix_of(frame, "I miss you", "I'm fine."), frame)

    def test_draft_that_is_a_prefix_still_hesitates(self):
        final = "Yeah, we're good up here"
        frames = pm.hesitation_frames(final, final)
        self.assertEqual(frames[-1], final)
        lengths = [len(f) for f in frames]
        top = lengths.index(len(final))
        self.assertLess(min(lengths[top:]), len(final), "it never deleted anything")

    def test_missing_draft_uses_the_default_draft(self):
        final = "Yeah, we're good up here"
        self.assertEqual(pm.hesitation_frames(None, final), pm.hesitation_frames(pm.default_draft(final), final))
        self.assertTrue(final.startswith(pm.default_draft(final)))
        self.assertLess(len(pm.default_draft(final)), len(final))
        self.assertEqual(pm.default_draft("Hi"), "H")

    def test_frames_are_plain_strings(self):
        frames = pm.hesitation_frames("ok", "okay then")
        self.assertTrue(all(isinstance(f, str) for f in frames))
        pickle.dumps(frames)

    def test_frame_at_plays_then_ends(self):
        frames = pm.hesitation_frames("hm", "hmm, sure")
        step = pm.frame_step(frames)
        self.assertEqual(pm.frame_at(frames, 0.0, step), frames[0])
        self.assertEqual(pm.frame_at(frames, step * 3 + step / 2, step), frames[3])
        self.assertEqual(pm.frame_at(frames, step * (len(frames) - 0.5), step), frames[-1])
        self.assertIsNone(pm.frame_at(frames, step * len(frames) + 0.01, step))
        self.assertIsNone(pm.frame_at([], 0.0, step))
        self.assertEqual(pm.frame_at(frames, -1.0, step), frames[0])

    def test_long_texts_stay_short_on_screen(self):
        final = "x" * 200
        frames = pm.hesitation_frames("y" * 150, final)
        self.assertLessEqual(pm.frame_step(frames) * len(frames), pm.MAX_SECONDS + 1e-9)
        self.assertLessEqual(pm.frame_step(pm.hesitation_frames("a", "ab")), pm.TYPE_STEP)

    def test_composer_tail_keeps_the_end_of_the_draft(self):
        self.assertEqual(pm.composer_tail("short", 30), "short")
        tail = pm.composer_tail("a" * 10 + "b" * 30, 30)
        self.assertTrue(tail.endswith("b" * 29))
        self.assertTrue(tail.startswith("…"))
        self.assertEqual(len(tail), 30)


class CallRecordTests(unittest.TestCase):
    def test_record_answered_and_ignored(self):
        calls = pm.record_call({}, "ch01_d2_call_maya", "maya", "answered", "23:10")
        self.assertEqual(pm.call_outcome(calls, "ch01_d2_call_maya"), "answered")
        calls = pm.record_call(calls, "c2", "julian", "ignored", None)
        self.assertEqual(pm.call_outcome(calls, "c2"), "ignored")
        self.assertEqual(calls["c2"], {"caller": "julian", "outcome": "ignored", "time": None,
                                       "returned": False})

    def test_record_never_mutates_and_keeps_the_first_answer(self):
        start = {}
        calls = pm.record_call(start, "c", "maya", "ignored")
        self.assertEqual(start, {})
        again = pm.record_call(calls, "c", "maya", "answered")
        self.assertEqual(pm.call_outcome(again, "c"), "ignored")

    def test_bad_outcome_or_ids_raise(self):
        for args in (("c", "maya", "maybe"), ("", "maya", "answered"), ("c", "", "answered")):
            with self.assertRaises(ValueError, msg=repr(args)):
                pm.record_call({}, *args)

    def test_old_saves_read_no_call(self):
        self.assertIsNone(pm.call_outcome(None, "c"))
        self.assertIsNone(pm.call_outcome({}, "c"))
        self.assertEqual(pm.missed_calls(None), [])

    def test_missed_calls_until_returned(self):
        calls = pm.record_call({}, "a", "maya", "ignored")
        calls = pm.record_call(calls, "b", "leia", "answered")
        calls = pm.record_call(calls, "c", "julian", "ignored")
        self.assertEqual(pm.missed_calls(calls), ["a", "c"])
        returned = pm.mark_returned(calls, "a")
        self.assertEqual(pm.missed_calls(returned), ["c"])
        self.assertFalse(calls["a"]["returned"])
        self.assertIs(pm.mark_returned(returned, "nope"), returned)
        pickle.loads(pickle.dumps(returned))

    def test_missed_call_message_ids_are_stable(self):
        mid = pm.missed_call_message_id("ch01_d2_call_maya")
        self.assertEqual(mid, "lc_call_ch01_d2_call_maya_missed")
        self.assertTrue(pm.is_missed_call_message(mid))
        self.assertFalse(pm.is_missed_call_message("ch01_d2_maya_dm_ryan"))
        self.assertFalse(pm.is_missed_call_message(None))


class LeaveOnReadTests(unittest.TestCase):
    def test_option_kinds(self):
        self.assertTrue(pm.is_leave_on_read({"id": "read", "text": "Leave it on read", "leave_on_read": True}))
        self.assertFalse(pm.is_leave_on_read({"id": "a", "text": "Sure"}))
        self.assertFalse(pm.is_leave_on_read(None))

    def test_validate_options(self):
        pm.validate_options([{"id": "a", "text": "Hey", "hesitate": True, "draft": "I"},
                             {"id": "r", "text": "Leave it on read", "leave_on_read": True}])
        with self.assertRaises(ValueError):
            pm.validate_options([{"id": "r", "text": "x", "leave_on_read": True, "hesitate": True}])
        with self.assertRaises(ValueError):
            pm.validate_options([{"id": "a", "text": "x", "draft": "y"}])

    def test_record_and_receipt_row(self):
        receipts = pm.record_left_on_read({}, "maya", "ch01_d2_maya_dm", "m2", "23:41")
        self.assertEqual(receipts["maya"], {"prompt": "ch01_d2_maya_dm", "message_id": "m2", "time": "23:41"})
        messages = [{"id": "m1", "sender": "maya"}, {"id": "m2", "sender": "maya"}]
        self.assertEqual(pm.receipt_row(messages, receipts.get("maya")), 1)
        # A later message from Ryan replaces the receipt; a later incoming one keeps it.
        self.assertIsNone(pm.receipt_row(messages + [{"id": "m3", "sender": "player"}], receipts["maya"]))
        self.assertEqual(pm.receipt_row(messages + [{"id": "m3", "sender": "maya"}], receipts["maya"]), 1)

    def test_receipt_row_old_save_and_missing_message(self):
        self.assertIsNone(pm.receipt_row([{"id": "m1", "sender": "maya"}], None))
        self.assertIsNone(pm.receipt_row([], {"message_id": "m1"}))
        self.assertIsNone(pm.receipt_row([{"id": "m1", "sender": "maya"}], {"message_id": None}))

    def test_record_never_mutates(self):
        start = {}
        pm.record_left_on_read(start, "maya", "p", None, None)
        self.assertEqual(start, {})

    def test_unopened_record_has_no_seen_row(self):
        receipts = pm.record_left_on_read({}, "maya", "p", "m1", "23:41", unopened=True)
        self.assertEqual(receipts["maya"], {"prompt": "p", "message_id": None, "time": None,
                                            "unopened": True})
        self.assertIsNone(pm.receipt_row([{"id": "m1", "sender": "maya"}], receipts["maya"]))
        self.assertNotIn("unopened", pm.record_left_on_read({}, "maya", "p", "m1")["maya"])

    def test_last_incoming_id(self):
        messages = [{"id": "a", "sender": "maya"}, {"id": "b", "sender": "player"},
                    {"id": "c", "sender": "system"}]
        self.assertEqual(pm.last_incoming_id(messages), "a")
        self.assertIsNone(pm.last_incoming_id([]))


class MomentFoundTests(unittest.TestCase):
    def test_found_on(self):
        self.assertTrue(pm.moment_found(("answered",), "answered"))
        self.assertFalse(pm.moment_found(("answered",), "ignored"))
        self.assertTrue(pm.moment_found(("show", "read"), "read"))
        self.assertFalse(pm.moment_found((), "read"))
        self.assertEqual(pm.normalise_found_on(None), ("answered",))
        self.assertEqual(pm.normalise_found_on("read"), ("read",))
        with self.assertRaises(ValueError):
            pm.normalise_found_on(())


# ---------------------------------------------------------------- Ren'Py side (harness)

def load_phone(screen_result="ignored", skipping=False, transitions=True, developer=False):
    """Phone writer + reply cards + phone moments, executed as Ren'Py runs them."""
    story = {}
    marked = []
    shown = []
    store = SimpleNamespace(
        phone_messages={"leia": [], "julian": [], "maya": [], "group": []},
        phone_photos=[], phone_reply_prompts={}, phone_reply_delivery={},
        phone_last_open_thread=None, phone_notification_queue=[], phone_notification_current=None,
        player_name="Ryan", girlfriend_name="Leia", friend_name="Julian",
        lc_phone_story_time="23:41",
    )

    def call_screen(name, **kw):
        shown.append((name, kw))
        return screen_result

    renpy = SimpleNamespace(
        store=store, get_screen=lambda *a, **kw: None, restart_interaction=lambda: None,
        call_screen=call_screen, is_skipping=lambda: skipping, show_screen=lambda *a, **kw: None,
        hide_screen=lambda *a, **kw: None, log=lambda *a: None,
    )
    env = {
        "renpy": renpy,
        "store": store,
        "config": SimpleNamespace(developer=developer),
        "persistent": SimpleNamespace(lc_screen_shake=True),
        "_preferences": SimpleNamespace(transitions=2 if transitions else 0),
        "has_story_value": lambda key: key in story,
        "get_story_value": lambda key, default=None: story.get(key, default),
        "set_story_value": lambda key, value: story.__setitem__(key, value),
        "lc_discovery_register": lambda *a, **kw: None,
        "lc_discovery_mark": lambda moment_id: marked.append(moment_id),
        "lc_ui_sound": lambda *a, **kw: None,
        "lc_sfx": lambda *a, **kw: None,
        "lc_phone_close": lambda: None,
    }
    load_blocks(["phone_add_message", "phone_store_message", "phone_call_offer"], env)
    env["PHONE_THREAD_ORDER"] = ("leia", "julian", "maya", "group")
    return env, story, store, marked, shown


class CallOfferHarnessTests(unittest.TestCase):
    def test_ignored_call_stores_outcome_and_leaves_a_missed_call(self):
        env, story, store, marked, shown = load_phone("ignored")
        self.assertEqual(env["phone_call_offer"]("maya", "ch01_test_call"), "ignored")
        self.assertEqual(shown[0][0], "phone_call")
        self.assertEqual(story["ch01_test_call"], "ignored")
        self.assertEqual(env["lc_phone_call_outcome"]("ch01_test_call"), "ignored")
        missed = store.phone_messages["maya"]
        self.assertEqual([m["id"] for m in missed], ["lc_call_ch01_test_call_missed"])
        self.assertEqual(missed[0]["sender"], "system")
        self.assertFalse(missed[0]["read"])
        self.assertEqual(env["phone_thread_unread_count"]("maya"), 1)
        self.assertEqual(env["lc_phone_missed_calls"](), ["ch01_test_call"])
        env["lc_phone_call_mark_returned"]("ch01_test_call")
        self.assertEqual(env["lc_phone_missed_calls"](), [])

    def test_answered_call_leaves_no_badge(self):
        env, story, store, marked, shown = load_phone("answered")
        self.assertEqual(env["phone_call_offer"]("maya", "c1"), "answered")
        self.assertEqual(store.phone_messages["maya"], [])
        self.assertEqual(env["lc_phone_missed_calls"](), [])

    def test_a_resolved_call_never_rings_again(self):
        env, story, store, marked, shown = load_phone("answered")
        env["phone_call_offer"]("maya", "c1")
        self.assertEqual(env["phone_call_offer"]("maya", "c1"), "answered")
        self.assertEqual(len(shown), 1)

    def test_old_save_reads_no_call(self):
        env, story, store, marked, shown = load_phone()
        if hasattr(store, "lc_phone_calls"):
            del store.lc_phone_calls
        self.assertIsNone(env["lc_phone_call_outcome"]("c1"))
        self.assertEqual(env["lc_phone_missed_calls"](), [])
        self.assertIsNone(env["lc_phone_read_receipt_row"]("maya"))

    def test_unknown_caller_raises(self):
        env, *_ = load_phone()
        with self.assertRaises(ValueError):
            env["phone_call_offer"]("stranger", "c1")

    def test_registered_call_marks_its_discovery_when_answered(self):
        env, story, store, marked, shown = load_phone("answered")
        env["lc_phone_moment_register"]("c1", "ch01_d2", "Maya, late call", "she called")
        env["phone_call_offer"]("maya", "c1")
        self.assertEqual(marked, ["c1"])

    def test_unregistered_or_ignored_call_marks_nothing(self):
        env, story, store, marked, shown = load_phone("ignored")
        env["lc_phone_moment_register"]("c1", "ch01_d2", "Maya, late call", "she called")
        env["phone_call_offer"]("maya", "c1")
        env["phone_call_offer"]("maya", "c2")
        self.assertEqual(marked, [])


class ReplyCardHarnessTests(unittest.TestCase):
    def options(self):
        return [
            {"id": "reply", "text": "We're good up here", "hesitate": True, "draft": "Why are you"},
            {"id": "read", "text": "Leave it on read", "leave_on_read": True,
             "followups": [("maya", "wow ok")]},
            {"id": "plain", "text": "Night"},
        ]

    def setup_thread(self, **kw):
        env, story, store, marked, shown = load_phone(**kw)
        env["phone_add_message"]("maya", "maya", "you two okay up there?", message_id="m1")
        env["phone_offer_reply"]("maya", "ch01_test_dm", self.options(), "plain")
        return env, story, store, marked

    def test_leave_on_read_records_the_choice_and_sends_nothing(self):
        env, story, store, marked = self.setup_thread()
        self.assertTrue(env["phone_choose_reply"]("maya", "read"))
        self.assertEqual(story["ch01_test_dm"], "read")
        ids = [m["id"] for m in store.phone_messages["maya"]]
        self.assertNotIn("ch01_test_dm_ryan", ids)
        self.assertEqual(ids, ["m1", "ch01_test_dm_followup_01"])
        self.assertTrue(store.phone_messages["maya"][0]["read"])
        self.assertEqual(store.lc_phone_read_receipts["maya"]["message_id"], "m1")
        self.assertEqual(env["lc_phone_read_receipt_row"]("maya"), 0)
        self.assertTrue(env["lc_phone_left_on_read"]("ch01_test_dm"))

    def test_leave_on_read_staged_queues_only_followups(self):
        env, story, store, marked = self.setup_thread()
        env["phone_select_reply"]("maya", "read")
        self.assertEqual([s[0] for s in store.phone_reply_delivery["maya"]], ["maya"])
        self.assertEqual(env["lc_phone_read_receipt_row"]("maya"), 0)

    def test_leave_on_read_without_followups_queues_nothing(self):
        env, story, store, marked = self.setup_thread()
        store.phone_reply_prompts["maya"]["options"][1].pop("followups")
        env["phone_select_reply"]("maya", "read")
        self.assertNotIn("maya", store.phone_reply_delivery)

    def test_a_sent_reply_is_not_left_on_read(self):
        env, story, store, marked = self.setup_thread()
        env["phone_choose_reply"]("maya", "plain")
        self.assertFalse(env["lc_phone_left_on_read"]("ch01_test_dm"))
        self.assertIsNone(env["lc_phone_read_receipt_row"]("maya"))

    def test_registered_reply_moment_marks_found_on_its_option(self):
        env, story, store, marked = self.setup_thread()
        env["lc_phone_moment_register"]("ch01_test_dm", "ch01_d2", "Maya, late text", "unread",
                                        found_on=("read",))
        env["phone_choose_reply"]("maya", "read")
        self.assertEqual(marked, ["ch01_test_dm"])

    def test_hesitate_holds_the_send_until_the_typing_ends(self):
        env, story, store, marked = self.setup_thread()
        env["phone_select_reply"]("maya", "reply")
        self.assertIsNotNone(env["phone_reply_typing_text"]("maya"))
        env["phone_deliver_reply_step"]("maya")
        self.assertEqual([m["id"] for m in store.phone_messages["maya"]], ["m1"])
        # When the frames are over, the send goes through and the typing record is cleared.
        env["LC_PHONE_TYPING"]["maya"]["start"] -= 60
        self.assertIsNone(env["phone_reply_typing_text"]("maya"))
        env["phone_deliver_reply_step"]("maya")
        self.assertEqual([m["id"] for m in store.phone_messages["maya"]], ["m1", "ch01_test_dm_ryan"])
        self.assertNotIn("maya", env["LC_PHONE_TYPING"])

    def test_a_story_deadline_never_waits_for_the_typing(self):
        env, story, store, marked = self.setup_thread()
        env["phone_select_reply"]("maya", "reply")
        env["phone_add_message"]("maya", "maya", "hello?", message_id="m2")
        self.assertEqual([m["id"] for m in store.phone_messages["maya"]], ["m1", "ch01_test_dm_ryan", "m2"])
        self.assertNotIn("maya", env["LC_PHONE_TYPING"])

    def test_skip_mode_and_reduced_motion_send_at_once(self):
        for kw in ({"skipping": True}, {"transitions": False}):
            env, story, store, marked = self.setup_thread(**kw)
            env["phone_select_reply"]("maya", "reply")
            self.assertIsNone(env["phone_reply_typing_text"]("maya"), kw)
            self.assertNotIn("maya", env["LC_PHONE_TYPING"])
            env["phone_deliver_reply_step"]("maya")
            self.assertEqual(store.phone_messages["maya"][-1]["id"], "ch01_test_dm_ryan")

    def test_options_without_hesitate_never_type(self):
        env, story, store, marked = self.setup_thread()
        env["phone_select_reply"]("maya", "plain")
        self.assertNotIn("maya", env["LC_PHONE_TYPING"])

    def test_the_typing_record_is_never_saved_state(self):
        env, story, store, marked = self.setup_thread()
        env["phone_select_reply"]("maya", "reply")
        self.assertFalse(any("typing" in name.lower() for name in vars(store)))

    def test_send_posts_its_own_text_under_a_label(self):
        # "send": the card shows a label ("Show Leia"), the bubble posts what is typed.
        env, story, store, marked = self.setup_thread()
        store.phone_reply_prompts["maya"]["options"][2].update(
            {"text": "Show [girlfriend_name]", "send": "it's [girlfriend_name] 🙂", "hesitate": True})
        env["phone_select_reply"]("maya", "plain")
        frames = env["LC_PHONE_TYPING"]["maya"]["frames"]
        self.assertTrue(frames[-1].startswith("it's "), frames[-1])  # types the send, not the label
        env["phone_flush_reply_delivery"]("maya")
        self.assertEqual(store.phone_messages["maya"][-1]["text"], "it's [girlfriend_name] 🙂")

    def test_options_without_send_post_their_text(self):
        env, story, store, marked = self.setup_thread()
        env["phone_choose_reply"]("maya", "plain")
        self.assertEqual(store.phone_messages["maya"][-1]["text"], "Night")

    def test_bad_option_flags_raise_at_offer(self):
        env, *_ = load_phone()
        with self.assertRaises(ValueError):
            env["phone_offer_reply"]("maya", "p", [{"id": "a", "text": "x", "leave_on_read": True,
                                                   "hesitate": True}, {"id": "b", "text": "y"}], "b")


class DeadlineHarnessTests(unittest.TestCase):
    """I1: a missed call is not a reply deadline. I2: leave-on-read chosen by default at a
    deadline keeps the chat unread with no 'Seen' receipt."""

    def setup_card(self, default="plain", **kw):
        env, story, store, marked, shown = load_phone(**kw)
        env["phone_add_message"]("maya", "maya", "you two okay up there?", message_id="m1")
        env["phone_offer_reply"]("maya", "ch01_test_dm", [
            {"id": "plain", "text": "On my way, two minutes."},
            {"id": "read", "text": "Leave it on read", "leave_on_read": True},
        ], default)
        return env, story, store

    def ids(self, store):
        return [m["id"] for m in store.phone_messages["maya"]]

    def test_a_missed_call_leaves_an_open_reply_card_open(self):
        env, story, store = self.setup_card(screen_result="ignored")
        self.assertEqual(env["phone_call_offer"]("maya", "c1"), "ignored")
        self.assertEqual(self.ids(store), ["m1", "lc_call_c1_missed"])
        self.assertNotIn("ch01_test_dm", story)
        self.assertIsNotNone(env["phone_pending_reply"]("maya"))
        # The next real message is still the deadline.
        env["phone_add_message"]("maya", "maya", "hello??", message_id="m2")
        self.assertEqual(self.ids(store), ["m1", "lc_call_c1_missed", "ch01_test_dm_ryan", "m2"])
        self.assertEqual(story["ch01_test_dm"], "plain")

    def test_a_picked_reply_still_posts_before_the_missed_call(self):
        env, story, store = self.setup_card(screen_result="ignored")
        env["phone_select_reply"]("maya", "plain")
        env["phone_call_offer"]("maya", "c1")
        self.assertEqual(self.ids(store), ["m1", "ch01_test_dm_ryan", "lc_call_c1_missed"])

    def test_default_leave_on_read_at_a_deadline_stays_unread(self):
        env, story, store = self.setup_card("read")
        env["phone_add_message"]("maya", "maya", "hello??", message_id="m2")
        self.assertEqual(story["ch01_test_dm"], "read")
        self.assertTrue(env["lc_phone_left_on_read"]("ch01_test_dm"))
        self.assertTrue(env["lc_phone_left_unopened"]("ch01_test_dm"))
        self.assertIsNone(env["lc_phone_read_receipt_row"]("maya"))
        self.assertEqual(env["lc_phone_receipt_time"]("maya"), "")
        self.assertEqual([m["read"] for m in store.phone_messages["maya"]], [False, False])
        self.assertEqual(env["phone_thread_unread_count"]("maya"), 2)

    def test_a_chat_opened_then_closed_is_seen_not_unopened(self):
        # Opened and closed unanswered (leaving a chat marks it read): the default at the
        # deadline is a 'Seen', not an unread bubble for a later lock-screen beat.
        env, story, store = self.setup_card("read")
        env["phone_mark_thread_read"]("maya")
        env["phone_default_reply"]("maya")
        self.assertEqual(story["ch01_test_dm"], "read")
        self.assertFalse(env["lc_phone_left_unopened"]("ch01_test_dm"))
        self.assertEqual(env["lc_phone_read_receipt_row"]("maya"), 0)

    def test_a_picked_leave_on_read_is_seen_not_unopened(self):
        env, story, store = self.setup_card("plain")
        env["phone_choose_reply"]("maya", "read")
        self.assertFalse(env["lc_phone_left_unopened"]("ch01_test_dm"))
        self.assertEqual(env["lc_phone_read_receipt_row"]("maya"), 0)


class TypingRecordTests(unittest.TestCase):
    def test_a_rolled_back_pick_drops_its_typing_record(self):
        env, story, store, marked, shown = load_phone()
        env["phone_add_message"]("maya", "maya", "hey", message_id="m1")
        env["phone_offer_reply"]("maya", "p", [
            {"id": "a", "text": "We're fine. Go to sleep", "hesitate": True},
            {"id": "b", "text": "Night"}], "b")
        env["phone_select_reply"]("maya", "a")
        self.assertTrue(env["phone_reply_typing_active"]("maya"))
        # Rollback/load restores the store from before the pick: nothing queued any more.
        store.phone_reply_delivery = {}
        self.assertFalse(env["phone_reply_typing_active"]("maya"))
        self.assertIsNone(env["phone_reply_typing_text"]("maya"))
        self.assertNotIn("maya", env["LC_PHONE_TYPING"])


class CallLabelSourceTests(unittest.TestCase):
    def test_answer_and_ignore_calls_have_stable_from_names(self):
        src = (ROOT / "game/systems/phone_moments.rpy").read_text(encoding="utf-8")
        self.assertIn("call expression answer_label from lc_phone_call_answer_return", src)
        self.assertIn("call expression ignore_label from lc_phone_call_ignore_return", src)

    def test_the_call_hides_the_dialogue_window(self):
        src = (ROOT / "game/systems/phone_moments.rpy").read_text(encoding="utf-8")
        self.assertIn("_window_hide(None)", src)
        self.assertIn("_window_show(None)", src)


def load_caption(mode):
    """lc_phone_reply_caption with the real choice engine and stat colours."""
    import lc_stat_model
    import lc_ui_logic
    from lc_rpy_harness import load
    env = {
        "renpy": SimpleNamespace(store=SimpleNamespace(persistent=SimpleNamespace(
            choice_display_mode=mode))),
        "lc_stat_model": lc_stat_model, "lc_ui_logic": lc_ui_logic,
        "LC_DELTA_UP": "#5aa874", "LC_DELTA_DOWN": "#d4636e",
        "LC_DELTA_EXHIBITIONISM": "#c2568c", "LC_DELTA_SHARING": "#8a62b8",
        "LC_REVIEW_DELTA_INK": {},
        "CHOICE_EFFECTS": {"t_love": [("relationship", "love", 1)], "t_none": []},
        "lc_choice_route_tag": lambda cid: "Love",
        "get_choice_tags": lambda cid: (),
    }
    load(["CHOICE_MODES", "STAT_LABELS", "current_choice_mode", "get_choice_effects",
          "_lc_hooks", "lc_hook_filter", "lc_choice_effective_effects", "_choice_effect_text", "format_choice", "lc_delta_colour", "lc_delta_colour_for_label",
          "lc_choice_effect_markup", "lc_phone_reply_caption"], env)
    env["CHOICE_EFFECTS"] = {"t_love": [("relationship", "love", 1)], "t_none": []}
    return env["lc_phone_reply_caption"], env


class ReplyCaptionTests(unittest.TestCase):
    """A scored reply option (`choice_id`) shows the same stat line as a story choice card."""

    def test_normal_mode_and_unscored_options_show_nothing(self):
        caption, _ = load_caption("normal")
        self.assertEqual(caption({"id": "a", "text": "x", "choice_id": "t_love"}), "")
        for mode in ("insight", "full", "developer"):
            caption, _ = load_caption(mode)
            self.assertEqual(caption({"id": "a", "text": "x"}), "", mode)

    def test_insight_and_full_match_the_choice_card_markup(self):
        for mode in ("insight", "full"):
            caption, env = load_caption(mode)
            _line, chips = env["lc_ui_logic"].parse_choice_caption(env["format_choice"]("t_love", "x"))
            self.assertTrue(chips)
            expected = env["lc_choice_effect_markup"](chips)
            self.assertEqual(caption({"id": "a", "text": "x", "choice_id": "t_love"}), expected)
            self.assertIn("Love", expected)
        self.assertIn("+1", load_caption("full")[0]({"choice_id": "t_love"}))
        self.assertIn("\u2191", load_caption("insight")[0]({"choice_id": "t_love"}))

    def test_a_no_stat_choice_has_no_label_except_in_developer_mode(self):
        self.assertEqual(load_caption("full")[0]({"choice_id": "t_none"}), "")
        dev = load_caption("developer")[0]({"choice_id": "t_none"})
        self.assertIn("no stats", dev)
        self.assertIn("t_none", dev)


class ScreenSourceTests(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_call_screen_uses_the_phone_look(self):
        src = self.read("game/screens/phone_call.rpy")
        self.assertIn("screen phone_call(caller_id):", src)
        self.assertIn('style "lc_phone_call_btn_primary"', src)
        self.assertIn('style "lc_phone_call_btn"', src)
        # A visible focus ring (keyboard/gamepad), and "Let it ring" stays white when focused.
        self.assertIn("style lc_phone_call_btn is lc_phone_btn:", src)
        self.assertIn("style lc_phone_call_btn_primary is lc_phone_btn_primary:", src)
        self.assertEqual(src.count("hover_background lc_phone_call_focus("), 2)
        self.assertIn('Return("answered")', src)
        self.assertIn('Return("ignored")', src)
        self.assertIn("lc_phone_motion_instant()", src)

    def test_thread_view_draws_typing_receipt_and_missed_call(self):
        src = self.read("game/screens/phone_sweetheart.rpy")
        self.assertIn("phone_reply_typing_text(phone_thread)", src)
        self.assertIn("lc_phone_read_receipt_row(phone_thread)", src)
        self.assertIn("lc_phone_moments.is_missed_call_message", src)
        self.assertIn('reply_option.get("leave_on_read")', src)

    def test_reply_card_draws_the_stat_label_unsubstituted(self):
        src = self.read("game/screens/phone_sweetheart.rpy")
        block = src.split("for reply_option in reply_view_prompt[\"options\"]:", 1)[1].split('text "+":', 1)[0]
        self.assertIn("lc_phone_reply_caption(reply_option)", block)
        self.assertIn("substitute False", block)

    def test_demo_label_is_dev_only(self):
        src = self.read("game/dev/dev_phone_moments.rpy")
        self.assertIn("label lc_dev_phone_moments:", src)
        self.assertIn("call lc_phone_call(", src)
        self.assertIn('"hesitate": True', src)
        self.assertIn('"leave_on_read": True', src)


if __name__ == "__main__":
    unittest.main()
