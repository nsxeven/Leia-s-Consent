# Phone moments

Three small, optional phone beats: an **incoming call**, a **hesitating reply** (Ryan types,
stops, deletes and rewrites before he sends), and **leaving a message on read**. Each one is
optional and never blocks: a player who ignores them plays exactly as before, nothing has a
timer or a fail state, and none of them moves stats by itself (a later scored choice may read
what happened, like any story value). A reply card can be scored once by the story (Maya's DM:
`ch01_d2_maya_dm_settle`), and then its default must be neutral. All characters are adults.

Files: `game/python-packages/lc_phone_moments.py` (pure rules), `game/systems/phone_moments.rpy`
(calls, read receipts, Moments-strip registration), `game/systems/phone_presentation_logic.rpy`
(the reply-card flags and the typing hold), `game/screens/phone_call.rpy` (call screen, one-to-one
reply delivery), `game/screens/phone_sweetheart.rpy` (composer, Seen receipt, missed-call row).
Demo: `game/dev/dev_phone_moments.rpy` (developer systems menu, "Phone moments demo"). Tests:
`tests/test_phone_moments.py`.

## Incoming call

```renpy
call lc_phone_call("maya", "ch01_d2_call_maya", answer_label="ch01_d2_maya_call_answered", ignore_label="ch01_d2_maya_call_ignored") from ch01_d2_maya_call_ring
if _return == "answered":
    ...
```

- The handset rings over the scene: the player's wallpaper (or the home art) dimmed, the caller's
  avatar with a soft ripple, their name, and two phone buttons, **Let it ring** and **Answer**.
  The ring plays the `phone_notify` buzz once.
- `answer_label` / `ignore_label` are optional labels that are *called* (they `return`), so the
  scene carries on after the call either way. Without them, branch on `_return`, or call
  `phone_call_offer(caller_id, call_id)` from Python; it returns `"answered"` or `"ignored"`.
- The outcome is stored once per save: as the story value `call_id` (so
  `get_story_value("ch01_d2_call_maya")` works for echoes) and in `lc_phone_calls` with the
  caller and the phone time. A call already resolved in this save returns its outcome without
  ringing again (the label still calls the matching branch). Rollback restores both with the store.
- **Let it ring** leaves a centred "☎ Missed call · 23:12" row (unread) in the caller's thread and
  a banner, so Messages shows the badge and the thread list shows "Missed call". The row's message
  id is `lc_call_<call_id>_missed`. Unlike other incoming messages it is **not** a reply deadline:
  a reply card still open in that thread stays open (no default reply is sent above the row); a
  reply the player already picked posts before it.
- The dialogue window is hidden while the phone rings (the last line's box would otherwise show
  under the handset) and comes back with the next line.
- Answer / Let it ring ignore clicks for the first 0.35 s, and show a ring when they have keyboard
  or gamepad focus (Let it ring stays white; Answer turns a lighter blue).
- Calling back is story content: check `lc_phone_missed_calls()` (ignored, not yet returned), play
  the call, then `$ lc_phone_call_mark_returned("ch01_d2_call_maya")`.
- Old saves and Chapter Select starts read `lc_phone_call_outcome(call_id)` as `None` ("no call").
- `caller_id` must be a Messages thread (`PHONE_THREAD_ORDER`); anything else raises.

## Reply-card flags

Reply cards are still `phone_offer_reply(thread_id, prompt_id, options, default_id)` (2-3
options, stat-free unless an option names a `choice_id`: scored in the story, the card shows its
stat line in Insight/Full). Optional keys on an option:

```renpy
$ phone_offer_reply("maya", "ch01_d2_maya_dm", [
    {"id": "reply", "text": "We're fine, go to sleep", "hesitate": True, "draft": "Why are you"},
    {"id": "read", "text": "Leave it on read", "leave_on_read": True},
    {"id": "show", "text": "Show [girlfriend_name]", "send": "it's [girlfriend_name] 🙂",
     "followups": [("maya", "hi!")], "choice_id": "ch01_d2_maya_dm_show"},
], "read")
```

- `"send"`: what the bubble posts (and the hesitation types) when it differs from the card
  label, e.g. the label "Show [girlfriend_name]" sends what she types.
- `"choice_id"`: a registered choice the story scores for this pick. In Insight/Full mode the
  card draws that choice's stat line under the option (`lc_phone_reply_caption`, same text and
  colours as a story choice card; Developer adds the ID); Normal/Immersive shows none. The card
  never applies it: the story does (`apply_choice`), once. Options without it are unchanged.

### Hesitation (`"hesitate": True`, optional `"draft"`)

- After the player picks the option, the composer types the draft, pauses, deletes back and
  types the final text, then the message sends. Without a draft, the first half of the final text
  is typed and partly deleted (`lc_phone_moments.default_draft`). Names are filled in before
  typing, so no frame shows half a `[girlfriend_name]`.
- About 1-3 seconds, never more than 4 (`MAX_SECONDS`; long texts type faster).
- **Skip mode, or reduced motion (screen shake or transitions turned off): no animation, the reply
  sends as it always did.** The choice itself is saved the moment it is picked; the typing is only
  a transient display (`LC_PHONE_TYPING`, never saved). A save holds the state from the start of
  the dialogue line, so loading a save made mid-typing (or rolling back) opens the card again
  with the pick undone; the leftover typing record is dropped because Ryan's message is no longer
  queued. A story deadline (the next incoming message) never waits for it.
- It plays inside the open phone, which is already modal: it never takes the click that advances
  dialogue, and closing the phone mid-typing is fine (the reply posts the next time the chat is
  open, or at the deadline).
- `draft` without `hesitate`, or `hesitate` on a leave-on-read option, raises at the offer.

### Leave it on read (`"leave_on_read": True`)

- A first-class option: Ryan writes nothing. The choice is stored like any reply
  (`get_story_value(prompt_id) == option id`), the thread is marked read, and a **"Seen 23:41"**
  receipt appears under the message he left on read. If he writes in that thread later, the
  receipt goes away. `followups` still play (the other person reacting), with no Ryan bubble.
- Read it back with `lc_phone_left_on_read(prompt_id)`. The receipt lives in
  `lc_phone_read_receipts` (per thread); old saves have none.
- It may be the card's default. When the card runs out at a deadline while the chat is closed
  and still unread (Ryan never opened it; opened and closed counts as read), the choice is still stored (`lc_phone_left_on_read` is True) but Ryan never opened it: the
  thread stays **unread** (badge, unread bubble) and no "Seen" receipt appears.
  `lc_phone_left_unopened(prompt_id)` tells the two cases apart, for a later unread-bubble beat.

## One-to-one chats now post picked replies while open

The Trip Group already played a picked reply (and its follow-ups) while its chat was open, from
the Chapter One overlay. One-to-one chats had no timer, so a picked reply waited for the next
story message. `lc_phone_moments_overlay` (`game/screens/phone_call.rpy`) now posts staged steps
in any open one-to-one chat at the same cadence (Ryan 0.45 s, replies 0.9 s), and posts a
hesitating reply in any chat once its typing ends. This also changes Day Two's Maya lunch reply:
the picked answer now appears while the chat is open instead of at the next Maya message.

## On the Moments strip

```renpy
init 1 python:
    lc_phone_moment_register("ch01_d2_maya_dm", "ch01_d2", "Maya, late text", "unread",
                             found_on=("show",))
    lc_phone_moment_register("ch01_d2_call_maya", "ch01_d2", "Maya, a late call", "ringing")
```

`moment_id` is the call id or the reply card's prompt id. The moment is a `phone` discovery
(`game/systems/discovery.rpy`) and counts as found when the call's outcome or the picked option
id is in `found_on` (default `("answered",)`). Label and mood follow the Moments strip rules in
`docs/HIDDEN_POV.md` (no route words in Immersive).

## Hooks

`phone_choose_reply` emits `phone_reply_chosen (thread_id, prompt_id, option)`;
`game/systems/phone_moments.rpy` listens (read receipt, discovery mark).

## Checking it

- Unit tests: `PYTHONPATH=game/python-packages python -m unittest tests.test_phone_moments`.
- In game: developer systems menu, "Phone moments demo" (Maya's chat; ids start `dev_pm_`).
