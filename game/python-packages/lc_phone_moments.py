"""Phone moments: pure rules for incoming calls, hesitation typing and leave on read.

No Ren'Py import: tests/test_phone_moments.py runs these directly. The Ren'Py side is
game/systems/phone_moments.rpy (calls, read receipts, discovery) and the reply-card additions in
game/systems/phone_presentation_logic.rpy. Every value these functions return or store is plain
data (str, dict, list), so it pickles into saves and rolls back with the store.
"""

CALL_OUTCOMES = ("answered", "ignored")

# Hesitation typing: one frame per TYPE_STEP seconds, the whole run capped at MAX_SECONDS.
TYPE_STEP = 0.055
MAX_SECONDS = 4.0
PAUSE_FRAMES = 12        # hold on the finished draft (about 0.65 s)
RETYPE_PAUSE_FRAMES = 4  # short beat after deleting
END_FRAMES = 3           # the final text sits in the composer a moment before it sends
DELETE_CHARS_PER_FRAME = 2

MISSED_CALL_PREFIX = "lc_call_"
MISSED_CALL_SUFFIX = "_missed"


# ---------------------------------------------------------------- hesitation typing

def _common_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def default_draft(final):
    """The first half of the final text (whole words when it has several): typed, then
    partly deleted and finished, which reads as second thoughts."""
    final = final or ""
    words = final.split(" ")
    if len(words) > 1:
        draft = " ".join(words[:(len(words) + 1) // 2])
        if draft != final:
            return draft
    return final[:max(1, len(final) // 2)] if len(final) > 1 else final


def _rewind_point(draft, final):
    """Where the delete stops: the shared prefix, or (when the draft is already a prefix of the
    final text) the start of the draft's second half, so a hesitation always deletes something."""
    shared = _common_prefix(draft, final)
    if shared < len(draft):
        return shared
    if len(draft) <= 1:
        return 0
    words = draft.split(" ")
    if len(words) > 1:
        keep = " ".join(words[:len(words) // 2])
        return len(keep) + 1 if keep else 0
    return len(draft) // 2


def hesitation_frames(draft, final, skip=False):
    """Composer texts for a hesitating reply: type the draft, pause, delete, retype the final
    text. `skip` (skip mode, reduced motion) or an empty final text gives [] = send at once.
    A missing draft uses default_draft(final)."""
    final = final or ""
    if skip or not final:
        return []
    draft = draft or default_draft(final)
    frames = [draft[:n] for n in range(1, len(draft) + 1)]
    frames.extend([draft] * PAUSE_FRAMES)
    stop = _rewind_point(draft, final)
    length = len(draft)
    while length > stop:
        length = max(stop, length - DELETE_CHARS_PER_FRAME)
        frames.append(draft[:length])
    frames.extend([draft[:stop]] * RETYPE_PAUSE_FRAMES)
    frames.extend(final[:n] for n in range(stop + 1, len(final) + 1))
    frames.extend([final] * END_FRAMES)
    return frames


def frame_step(frames):
    """Seconds per frame: TYPE_STEP, faster for long texts so a run never passes MAX_SECONDS."""
    if not frames:
        return TYPE_STEP
    return min(TYPE_STEP, MAX_SECONDS / float(len(frames)))


def frame_at(frames, elapsed, step=TYPE_STEP):
    """The composer text `elapsed` seconds into the run, or None once it is over."""
    if not frames:
        return None
    index = int(max(0.0, elapsed) / step)
    if index >= len(frames):
        return None
    return frames[index]


def composer_tail(text, limit=30):
    """The end of a long draft for the one-line composer ('…' + the last limit-1 characters)."""
    text = text or ""
    if len(text) <= limit:
        return text
    return "…" + text[-(limit - 1):]


# ---------------------------------------------------------------- calls

def record_call(calls, call_id, caller_id, outcome, time=None):
    """A new calls dict with this call's outcome. The first answer stands: recording a call that
    is already stored returns the dict unchanged. Never mutates `calls`."""
    if not call_id or not caller_id:
        raise ValueError("A call needs a call id and a caller")
    if outcome not in CALL_OUTCOMES:
        raise ValueError("Call outcome must be one of %r, not %r" % (CALL_OUTCOMES, outcome))
    calls = dict(calls or {})
    if call_id in calls:
        return calls
    calls[call_id] = {"caller": caller_id, "outcome": outcome, "time": time, "returned": False}
    return calls


def call_outcome(calls, call_id):
    """'answered' / 'ignored', or None when this save never got the call (old saves too)."""
    entry = (calls or {}).get(call_id)
    return entry.get("outcome") if entry else None


def missed_calls(calls):
    """Ignored calls not yet returned, in the order they rang."""
    return [cid for cid, entry in (calls or {}).items()
            if entry.get("outcome") == "ignored" and not entry.get("returned")]


def mark_returned(calls, call_id):
    """A new dict with the call marked returned (unchanged when the id is unknown)."""
    if call_id not in (calls or {}):
        return calls
    calls = dict(calls)
    entry = dict(calls[call_id])
    entry["returned"] = True
    calls[call_id] = entry
    return calls


def missed_call_message_id(call_id):
    return MISSED_CALL_PREFIX + call_id + MISSED_CALL_SUFFIX


def is_missed_call_message(message_id):
    return bool(message_id) and message_id.startswith(MISSED_CALL_PREFIX) and \
        message_id.endswith(MISSED_CALL_SUFFIX)


# ---------------------------------------------------------------- reply options, leave on read

def is_leave_on_read(option):
    return bool(option) and bool(option.get("leave_on_read"))


def validate_options(options):
    """Reply-card flags: `leave_on_read` sends nothing, so it can't also `hesitate`; a `draft`
    only means something on a hesitating option."""
    for option in options:
        if is_leave_on_read(option) and option.get("hesitate"):
            raise ValueError("Option %r: leave_on_read and hesitate exclude each other" % option.get("id"))
        if option.get("draft") and not option.get("hesitate"):
            raise ValueError("Option %r: a draft needs hesitate=True" % option.get("id"))
    return None


def record_left_on_read(receipts, thread_id, prompt_id, message_id, time=None):
    """A new receipts dict: thread_id's latest left-on-read message. Never mutates `receipts`."""
    receipts = dict(receipts or {})
    receipts[thread_id] = {"prompt": prompt_id, "message_id": message_id, "time": time}
    return receipts


def last_incoming_id(messages):
    """Id of the newest message someone else sent (system rows excluded), or None."""
    for message in reversed(messages or ()):
        if message.get("sender") not in ("player", "system", None):
            return message.get("id")
    return None


def receipt_row(messages, receipt):
    """Index of the message the 'Seen' receipt sits under, or None: no receipt (old saves),
    message gone, or Ryan has written in the thread since."""
    if not receipt or not receipt.get("message_id"):
        return None
    index = None
    for i, message in enumerate(messages or ()):
        if message.get("id") == receipt["message_id"]:
            index = i
        elif index is not None and message.get("sender") == "player":
            return None
    return index


# ---------------------------------------------------------------- discovery

def normalise_found_on(found_on):
    """Outcomes / option ids that count as finding a phone moment (default: an answered call)."""
    if found_on is None:
        return ("answered",)
    if isinstance(found_on, str):
        found_on = (found_on,)
    found_on = tuple(found_on)
    if not found_on:
        raise ValueError("found_on needs at least one outcome or option id")
    return found_on


def moment_found(found_on, outcome):
    return outcome in (found_on or ())
