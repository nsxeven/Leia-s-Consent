# Phone moments - incoming calls, leave-on-read receipts, phone moments on the Moments strip
#
# Purpose: Small optional phone beats. An incoming call rings over the scene (screen phone_call
#   in screens/phone_call.rpy) with Answer / Let it ring; the outcome is stored once per save,
#   and an ignored call leaves an unread "Missed call" row in the caller's thread (the Messages
#   badge) that the story can return later. Reply cards (systems/phone_presentation_logic.rpy)
#   gain a first-class "leave it on read" option, recorded here as a read receipt, and a
#   hesitate flag (typed-draft animation). A phone moment can register on a day's Moments strip
#   (kind 'phone'). Rules live in python-packages/lc_phone_moments.py; this file binds them to
#   the store. Ignoring every phone moment plays exactly as before; old saves read "no call".
#
# Public API (call these from scenes/screens):
#   phone_call_offer(caller_id, call_id) -> str
#       ring now and return 'answered' / 'ignored'; stored once per save (story value call_id
#       and lc_phone_calls); a call already resolved in this save returns its outcome without
#       ringing again. caller_id is a Messages thread id (PHONE_THREAD_ORDER)
#   label lc_phone_call(caller_id, call_id, answer_label=None, ignore_label=None)
#       the Ren'Py entry: rings, then calls answer_label or ignore_label (when given) and
#       returns the outcome in _return
#   lc_phone_call_outcome(call_id)            'answered' / 'ignored', or None (no call, old save)
#   lc_phone_missed_calls()                   ignored calls not yet returned, oldest first
#   lc_phone_call_mark_returned(call_id) -> None
#       Ryan called back (the story plays the call itself); drops it from lc_phone_missed_calls
#   lc_phone_call_ring() -> None              the ring cue (screen action; never raises)
#   lc_phone_left_on_read(prompt_id)          True when that reply card was answered by leaving
#       the message on read
#   lc_phone_read_receipt_row(thread_id)      index of the message the 'Seen' receipt sits under
#       in phone_messages_for_thread(thread_id), or None
#   lc_phone_receipt_time(thread_id)          the receipt's clock text ('' when none)
#   lc_phone_moment_register(moment_id, day_id, label, mood, found_on=None, image=None) -> None
#       init 1+: put a call (moment_id = call_id) or reply card (moment_id = prompt_id) on the
#       day's Moments strip; found when the outcome / option id is in found_on (default:
#       'answered')
#   lc_phone_on_reply_chosen(thread_id, prompt_id, option) -> None
#       phone_reply_chosen hook: records the read receipt and marks a registered moment
#   LC_PHONE_MOMENTS                          {moment_id: found_on} (init-time, never saved)
#   default lc_phone_calls                    save state: {call_id: {caller, outcome, time,
#       returned}}
#   default lc_phone_read_receipts            save state: {thread_id: {prompt, message_id, time}}
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_phone_now_text,
#   _lc_phone_moment_mark, _lc_phone_call_record
#
# Example:
#   call lc_phone_call("maya", "ch01_d2_call_maya", answer_label="ch01_d2_maya_call_answered") from ch01_d2_maya_call
#   $ phone_offer_reply("maya", "ch01_d2_maya_dm", [
#       {"id": "reply", "text": "We're fine, go to sleep", "hesitate": True, "draft": "Why are you"},
#       {"id": "read", "text": "Leave it on read", "leave_on_read": True},
#       {"id": "show", "text": "Show [girlfriend_name]"}], "read")
#   if lc_phone_left_on_read("ch01_d2_maya_dm"):
#
# Depends on: python-packages/lc_phone_moments.py, systems/phone_state.rpy,
#   systems/phone_presentation_logic.rpy, systems/story_state.rpy, systems/discovery.rpy,
#   systems/lc_hooks.rpy, systems/lc_fx.rpy (lc_sfx), screens/phone_call.rpy
# Hooks: listens to phone_reply_chosen (systems/phone_presentation_logic.rpy, phone_choose_reply)
# Load order: default (init 0), so moment registrations at init 1 find LC_PHONE_MOMENTS and the
#   discovery registry; everything else is looked up at call time
# Docs: docs/PHONE_MOMENTS.md, docs/ARCHITECTURE.md   Tests: tests/test_phone_moments.py

default lc_phone_calls = {}
default lc_phone_read_receipts = {}

init python:
    import datetime as _lc_phone_moment_dt
    import lc_phone_moments

    LC_PHONE_MOMENTS = {}

    def _lc_phone_now_text():
        return (getattr(renpy.store, "lc_phone_story_time", None)
                or _lc_phone_moment_dt.datetime.now().strftime("%H:%M"))

    def lc_phone_moment_register(moment_id, day_id, label, mood, found_on=None, image=None):
        found_on = lc_phone_moments.normalise_found_on(found_on)
        lc_discovery_register(day_id, moment_id, "phone", label, mood, image=image)
        LC_PHONE_MOMENTS[moment_id] = found_on
        return None

    def _lc_phone_moment_mark(moment_id, outcome):
        found_on = LC_PHONE_MOMENTS.get(moment_id)
        if found_on and lc_phone_moments.moment_found(found_on, outcome):
            lc_discovery_mark(moment_id)
        return None

    def lc_phone_call_outcome(call_id):
        return lc_phone_moments.call_outcome(getattr(renpy.store, "lc_phone_calls", None), call_id)

    def lc_phone_missed_calls():
        return lc_phone_moments.missed_calls(getattr(renpy.store, "lc_phone_calls", None))

    def lc_phone_call_mark_returned(call_id):
        calls = getattr(renpy.store, "lc_phone_calls", None) or {}
        renpy.store.lc_phone_calls = lc_phone_moments.mark_returned(calls, call_id)
        return None

    def lc_phone_call_ring():
        try:
            lc_sfx("phone_notify")
        except Exception:
            pass
        return None

    def _lc_phone_call_record(caller_id, call_id, outcome):
        renpy.store.lc_phone_calls = lc_phone_moments.record_call(
            getattr(renpy.store, "lc_phone_calls", None), call_id, caller_id, outcome,
            _lc_phone_now_text())
        set_story_value(call_id, outcome)
        if outcome == "ignored":
            phone_add_message(caller_id, "system", text="Missed call",
                              message_id=lc_phone_moments.missed_call_message_id(call_id),
                              mark_unread=True, notify=True, notification_app="Phone",
                              notification_title=phone_thread_label(caller_id))
        _lc_phone_moment_mark(call_id, outcome)
        return None

    def phone_call_offer(caller_id, call_id):
        """Ring over the scene. Rollback-safe: the outcome lives in the store (story value and
        lc_phone_calls), written after the screen returns."""
        if caller_id not in PHONE_THREAD_ORDER or not call_id:
            raise ValueError("Unknown caller thread or missing call id")
        done = lc_phone_call_outcome(call_id)
        if done:
            return done
        lc_phone_close()
        outcome = renpy.call_screen("phone_call", caller_id=caller_id)
        if outcome not in lc_phone_moments.CALL_OUTCOMES:
            outcome = "ignored"
        _lc_phone_call_record(caller_id, call_id, outcome)
        return outcome

    def lc_phone_left_on_read(prompt_id):
        receipts = getattr(renpy.store, "lc_phone_read_receipts", None) or {}
        return any(r.get("prompt") == prompt_id for r in receipts.values())

    def lc_phone_read_receipt_row(thread_id):
        receipt = (getattr(renpy.store, "lc_phone_read_receipts", None) or {}).get(thread_id)
        if not receipt:
            return None
        return lc_phone_moments.receipt_row(phone_messages_for_thread(thread_id), receipt)

    def lc_phone_receipt_time(thread_id):
        receipt = (getattr(renpy.store, "lc_phone_read_receipts", None) or {}).get(thread_id) or {}
        return receipt.get("time") or ""

    def lc_phone_on_reply_chosen(thread_id, prompt_id, option):
        if lc_phone_moments.is_leave_on_read(option):
            renpy.store.lc_phone_read_receipts = lc_phone_moments.record_left_on_read(
                getattr(renpy.store, "lc_phone_read_receipts", None), thread_id, prompt_id,
                lc_phone_moments.last_incoming_id(phone_messages_for_thread(thread_id)),
                _lc_phone_now_text())
        _lc_phone_moment_mark(prompt_id, option.get("id"))
        return None

    lc_hook_add("phone_reply_chosen", lc_phone_on_reply_chosen)


# The Ren'Py entry for a call. `from` clauses on the caller's `call` keep saves stable.
label lc_phone_call(caller_id, call_id, answer_label=None, ignore_label=None):
    $ _lc_phone_call_outcome = phone_call_offer(caller_id, call_id)
    if _lc_phone_call_outcome == "answered" and answer_label:
        call expression answer_label
    elif _lc_phone_call_outcome == "ignored" and ignore_label:
        call expression ignore_label
    return lc_phone_call_outcome(call_id)
