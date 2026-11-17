"""Leia's side: errand map, visit log, named outcomes and the daily gain cap (pure Python).

Once a day the player can play a short stretch as Leia (docs/LEIA_SIDE.md). She picks where to
go on a small map of place cards; every open place gets visited, in the order the player picks.
Locked places show her in-character reason and, in Insight/Full, "Opens on a later day.".
Choices she makes during her segment move her own stats, but only by +2 in total per day: this
module keeps that ledger.

State is one plain dict kept in a save-local store variable. Every function here returns a NEW
dict and never mutates its input, so Ren'Py rollback (which restores the store's reference) puts
visits, outcomes and the cap back exactly as they were. A missing/None state (old saves, Chapter
Select starts) reads as "nothing happened".

    {"visits":   {day_id: (place_id, ...)},          # in the order she went
     "outcomes": frozenset({outcome_id, ...}),       # named results later scenes read
     "gains":    {day_id: ((choice_id, ((group, stat, amount), ...)), ...)}}   # applied effects

Ren'Py side: game/systems/leia_side.rpy. Tests: tests/test_leia_side.py.
"""
import re

DAILY_GAIN_CAP = 2
MAX_PLACES = 4
STATES = ("open", "visited", "locked")
LATER_DAY_HINT = "Opens on a later day."
HINT_MODES = ("insight", "full", "developer")
TITLE_CARD = "Meanwhile \u2014 [girlfriend_name]"
MOMENT_KIND = "errand"
CAPPED_SUFFIX = " (capped)"

_ID = re.compile(r"^[A-Za-z0-9_]+$")


def _check_id(name, value):
    if not isinstance(value, str) or not _ID.match(value):
        raise ValueError("Leia side %s must be a plain id (letters, digits, _), got %r" % (name, value))


def _check_text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Leia side %s must be a non-empty string, got %r" % (name, value))


# ------------------------------------------------------------------ places

def register_place(registry, day_id, place_id, label, bg, hint, locked_reason=None, mood=""):
    """Add one place card to registry ({day_id: [entry, ...]}) in registration order.

    bg is the thumbnail (an image name such as "bg ch01_d2_cafe", or a file path). A place with
    a locked_reason is locked: its card shows the reason (Leia's words) and cannot be visited.
    Place ids are unique per day; a map holds at most MAX_PLACES cards (one fixed row).
    """
    _check_id("day_id", day_id)
    _check_id("place_id", place_id)
    _check_text("label", label)
    _check_text("bg", bg)
    _check_text("hint", hint)
    if locked_reason is not None:
        _check_text("locked_reason", locked_reason)
    if not isinstance(mood, str):
        raise ValueError("Leia side mood must be a string, got %r" % (mood,))
    entries = registry.setdefault(day_id, [])
    if any(e["id"] == place_id for e in entries):
        raise ValueError("Leia side place %r is already registered for %s" % (place_id, day_id))
    if len(entries) >= MAX_PLACES:
        raise ValueError("Leia side map for %s already holds %d places" % (day_id, MAX_PLACES))
    entry = {"id": place_id, "day_id": day_id, "label": label, "bg": bg, "hint": hint,
             "locked_reason": locked_reason, "mood": mood}
    entries.append(entry)
    return entry


def places(registry, day_id, ids=None):
    """The day's place entries: all in registration order, or the given ids in that order."""
    entries = list(registry.get(day_id, ()))
    if ids is None:
        return entries
    by_id = {e["id"]: e for e in entries}
    out = []
    for place_id in ids:
        if place_id not in by_id:
            raise ValueError("Leia side place %r is not registered for %s" % (place_id, day_id))
        out.append(by_id[place_id])
    return out


def moment_id(day_id, place_id):
    """The Moments strip id a visit marks (stable: it is save data)."""
    return "leia_%s_%s" % (day_id, place_id)


def _is_locked(entry):
    return entry.get("locked_reason") is not None


def open_remaining(place_list, visited):
    """Ids of open places not visited yet, in card order."""
    seen = set(visited or ())
    return [e["id"] for e in place_list if not _is_locked(e) and e["id"] not in seen]


def errand_done(place_list, visited):
    """True once every open place has been visited (locked places never count)."""
    return not open_remaining(place_list, visited)


def lock_hint(state, mode):
    """LATER_DAY_HINT for a locked card in Insight/Full/Developer, else None. The map screen
    reads it live, so switching mode while the map is open updates the cards."""
    return LATER_DAY_HINT if (state == "locked" and mode in HINT_MODES) else None


def cards(place_list, visited, mode):
    """What the map screen draws, one dict per place in card order.

    state: open / visited / locked. reason: Leia's in-character reason, on locked cards in every
    mode. lock_hint: LATER_DAY_HINT on locked cards in Insight/Full/Developer, else None.
    activatable: only open cards can be picked (locked and visited cards still take focus).
    """
    seen = set(visited or ())
    out = []
    for e in place_list:
        if _is_locked(e):
            state = "locked"
        elif e["id"] in seen:
            state = "visited"
        else:
            state = "open"
        locked = state == "locked"
        out.append({
            "id": e["id"], "label": e["label"], "bg": e["bg"], "hint": e["hint"], "state": state,
            "reason": e["locked_reason"] if locked else None,
            "lock_hint": lock_hint(state, mode),
            "activatable": state == "open",
        })
    return out


# ------------------------------------------------------------------ state

def _state(state):
    return state if state else {}


def visits(state, day_id):
    """Places visited on day_id, in the order she went (a tuple; () when none / old save)."""
    return tuple(_state(state).get("visits", {}).get(day_id, ()))


def visit(state, place_list, day_id, place_id):
    """New state with place_id appended to the day's visit log.

    Raises ValueError for a place that is not on the map or is locked. A repeat visit returns
    the same state object (nothing to record).
    """
    entry = next((e for e in place_list if e["id"] == place_id), None)
    if entry is None:
        raise ValueError("Leia side place %r is not on the %s map" % (place_id, day_id))
    if _is_locked(entry):
        raise ValueError("Leia side place %r is locked on %s" % (place_id, day_id))
    done = visits(state, day_id)
    if place_id in done:
        return state
    new = dict(_state(state))
    log = dict(new.get("visits", {}))
    log[day_id] = done + (place_id,)
    new["visits"] = log
    return new


def did(state, outcome_id):
    """True once the named outcome was marked in this save."""
    return outcome_id in _state(state).get("outcomes", ())


def mark(state, outcome_id):
    """New state with outcome_id recorded (the same state when it already was)."""
    _check_id("outcome_id", outcome_id)
    if did(state, outcome_id):
        return state
    new = dict(_state(state))
    new["outcomes"] = frozenset(new.get("outcomes", ())) | {outcome_id}
    return new


# ------------------------------------------------------------------ gain cap

def gained(state, day_id):
    """Total positive stat change Leia-side choices have applied on day_id."""
    total = 0
    for _choice_id, effects in _state(state).get("gains", {}).get(day_id, ()):
        total += sum(amount for _g, _s, amount in effects if amount > 0)
    return total


def cap_effects(state, day_id, effects):
    """The effects a Leia-side choice would apply now: each gain is cut to what is left of the
    day's DAILY_GAIN_CAP (spent in effect order); losses pass unchanged and never refund the
    allowance. Same length and order as effects; the input is not changed."""
    left = max(0, DAILY_GAIN_CAP - gained(state, day_id))
    out = []
    for group, stat, amount in effects:
        if amount > 0:
            allowed = min(amount, left)
            left -= allowed
            amount = allowed
        out.append((group, stat, amount))
    return out


def record_gain(state, day_id, choice_id, applied):
    """New state with one applied Leia-side choice in the day's ledger. Record the effects that
    were actually applied (cap_effects output), so the ledger never passes the cap."""
    _check_id("choice_id", choice_id)
    new = dict(_state(state))
    ledger = dict(new.get("gains", {}))
    row = (choice_id, tuple((g, s, int(a)) for g, s, a in applied))
    ledger[day_id] = tuple(ledger.get(day_id, ())) + (row,)
    new["gains"] = ledger
    return new


def applied_effects(state, choice_id):
    """What a Leia-side choice actually applied (summed per stat, first-seen order), for
    callers that subtract a choice's effects again (e.g. a Day's lane exemption)."""
    totals, order = {}, []
    for rows in _state(state).get("gains", {}).values():
        for cid, effects in rows:
            if cid != choice_id:
                continue
            for group, stat, amount in effects:
                key = (group, stat)
                if key not in totals:
                    totals[key] = 0
                    order.append(key)
                totals[key] += amount
    return [(g, s, totals[(g, s)]) for g, s in order]


def capped_label(stat_label):
    """Choice-card label of a gain the cap cut ("Love (capped)"): the amount after it stays the
    number that will really apply, so Insight/Full never promise a gain that won't land."""
    return stat_label + CAPPED_SUFFIX
