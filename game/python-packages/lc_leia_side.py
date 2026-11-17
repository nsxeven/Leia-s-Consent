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

# Keys a place dict may carry (lc_leia_register_places / lc_leia_map(day, places=[dict, ...])).
PLACE_KEYS = ("id", "label", "bg", "hint", "locked_reason", "locked", "mood", "done")

_ID = re.compile(r"^[A-Za-z0-9_]+$")
# An image name: space-separated words of letters, digits and _ ("bg ch01_d2_cafe").
_IMAGE_NAME = re.compile(r"^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$")


def _check_id(name, value):
    if not isinstance(value, str) or not _ID.match(value):
        raise ValueError("Leia side %s must be a plain id (letters, digits, _), got %r" % (name, value))


def _check_text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Leia side %s must be a non-empty string, got %r" % (name, value))


def is_image_name(bg):
    """'bg ch01_d2_cafe' is an image name; 'images/.../x.webp' is a file path."""
    return "/" not in bg and "." not in bg


# ------------------------------------------------------------------ places

def register_place(registry, day_id, place_id, label, bg, hint=None, locked_reason=None, mood="",
                   done=None):
    """Add one place card to registry ({day_id: [entry, ...]}) in registration order.

    bg is the thumbnail (an image name such as "bg ch01_d2_cafe", or a file path); the Ren'Py side
    checks it names a real image/file once images are defined (init 999). A place with a
    locked_reason is locked: its card shows the reason (Leia's words) and cannot be visited; only
    open places need a hint. done (optional) replaces the hint on the card once she has been there.
    Place ids are unique per day; a map holds at most MAX_PLACES cards (one fixed row).
    """
    _check_id("day_id", day_id)
    _check_id("place_id", place_id)
    _check_text("label", label)
    _check_text("bg", bg)
    if is_image_name(bg) and not _IMAGE_NAME.match(bg):
        raise ValueError("Leia side place %r on %s: bg %r is neither an image name (words of letters, "
                         "digits and _, e.g. \"bg ch01_d2_cafe\") nor a file path" % (place_id, day_id, bg))
    if locked_reason is not None:
        _check_text("locked_reason", locked_reason)
        if hint is not None and not isinstance(hint, str):
            raise ValueError("Leia side hint must be a string, got %r" % (hint,))
    else:
        _check_text("hint", hint)
    if done is not None:
        _check_text("done", done)
    if not isinstance(mood, str):
        raise ValueError("Leia side mood must be a string, got %r" % (mood,))
    entries = registry.setdefault(day_id, [])
    if any(e["id"] == place_id for e in entries):
        raise ValueError("Leia side place %r is already registered for %s" % (place_id, day_id))
    if len(entries) >= MAX_PLACES:
        raise ValueError("Leia side map for %s already holds %d places" % (day_id, MAX_PLACES))
    entry = {"id": place_id, "day_id": day_id, "label": label, "bg": bg, "hint": hint or "",
             "locked_reason": locked_reason, "mood": mood, "done": done}
    entries.append(entry)
    return entry


def place_kwargs(place):
    """register_place keyword arguments from one place dict (PLACE_KEYS). "locked": True needs a
    locked_reason (Leia's words); unknown keys are rejected, so a typo can't vanish silently."""
    if not isinstance(place, dict):
        raise ValueError("Leia side place must be a dict, got %r" % (place,))
    unknown = sorted(k for k in place if k not in PLACE_KEYS)
    if unknown:
        raise ValueError("Leia side place %r: unknown key(s) %s (allowed: %s)"
                         % (place.get("id"), ", ".join(unknown), ", ".join(PLACE_KEYS)))
    for key in ("id", "label", "bg"):
        if key not in place:
            raise ValueError("Leia side place %r is missing %r" % (place.get("id"), key))
    reason = place.get("locked_reason")
    locked = place.get("locked")
    if locked is not None and bool(locked) != (reason is not None):
        raise ValueError("Leia side place %r: \"locked\": %r needs %s locked_reason"
                         % (place["id"], locked, "a" if locked else "no"))
    return {"place_id": place["id"], "label": place["label"], "bg": place["bg"],
            "hint": place.get("hint"), "locked_reason": reason, "mood": place.get("mood", ""),
            "done": place.get("done")}


def register_places(registry, day_id, place_list):
    """Register a list/tuple of place dicts (PLACE_KEYS) in order; returns the entries."""
    if isinstance(place_list, (str, dict)) or not isinstance(place_list, (list, tuple)):
        raise ValueError("Leia side places for %s must be a list or tuple of place dicts, got %r"
                         % (day_id, place_list))
    return [register_place(registry, day_id, **place_kwargs(p)) for p in place_list]


def _same_place(entry, place):
    kw = place_kwargs(place)
    return (entry["label"] == kw["label"] and entry["bg"] == kw["bg"]
            and entry["hint"] == (kw["hint"] or "") and entry["locked_reason"] == kw["locked_reason"]
            and entry["mood"] == kw["mood"] and entry["done"] == kw["done"])


def places(registry, day_id, ids=None):
    """The day's place entries: all in registration order, or the given ones in that order.

    ids: None, or a list/tuple of place ids and/or place dicts. A dict must match the place
    registered under its id (the map always draws the registered entry, which is also the Moments
    strip moment); pass the same list you registered with register_places, or just the ids.
    """
    entries = list(registry.get(day_id, ()))
    if ids is None:
        return entries
    if isinstance(ids, (str, dict)) or not isinstance(ids, (list, tuple)):
        raise ValueError("Leia side places for %s must be None or a list/tuple of place ids or place "
                         "dicts, got %r" % (day_id, ids))
    by_id = {e["id"]: e for e in entries}
    out = []
    for item in ids:
        place = item if isinstance(item, dict) else None
        place_id = place.get("id") if place is not None else item
        if place_id not in by_id:
            raise ValueError("Leia side place %r is not registered for %s: register it at init 1 with "
                             "lc_leia_place or lc_leia_register_places" % (place_id, day_id))
        if place is not None and not _same_place(by_id[place_id], place):
            raise ValueError("Leia side place %r on %s differs from the registered one: register the "
                             "list once with lc_leia_register_places and pass that same list (or ids)"
                             % (place_id, day_id))
        out.append(by_id[place_id])
    return out


def bad_images(registry, has_image, loadable):
    """Problems with the places' bg (one line each, naming day, place and bg): an image name
    must be a defined image (has_image), a path must be loadable."""
    problems = []
    for day_id in sorted(registry):
        for e in registry[day_id]:
            bg = e["bg"]
            if is_image_name(bg):
                if has_image(bg):
                    continue
                hint = ""
                if not bg.startswith("bg ") and has_image("bg " + bg):
                    hint = " (did you mean \"bg %s\"?)" % bg
                problems.append("%s/%s: bg %r is not a defined image%s" % (day_id, e["id"], bg, hint))
            elif not loadable(bg):
                problems.append("%s/%s: bg file %r is not loadable" % (day_id, e["id"], bg))
    return problems


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
    hint: the place's hint (its done line instead once visited, when it has one).
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
        hint = e["hint"]
        if state == "visited" and e.get("done"):
            hint = e["done"]
        out.append({
            "id": e["id"], "label": e["label"], "bg": e["bg"], "hint": hint, "state": state,
            "reason": e["locked_reason"] if locked else None,
            "lock_hint": lock_hint(state, mode),
            "activatable": state == "open",
        })
    return out


# ------------------------------------------------------------------ state

def _state(state):
    return state if state else {}


def visits(state, day_id):
    """Places visited on day_id, in the order she went (always a tuple; () when none / old save).
    Compare with first_visit / visited_first / visited_before, never with a list literal."""
    return tuple(_state(state).get("visits", {}).get(day_id, ()))


def first_visit(state, day_id):
    """The place she went to first on day_id, or None before any visit."""
    done = visits(state, day_id)
    return done[0] if done else None


def visited_first(state, day_id, place_id):
    """True when place_id was the first place she went to on day_id."""
    return first_visit(state, day_id) == place_id


def visited_before(state, day_id, place_a, place_b):
    """True when she has been to place_a and had not been to place_b before it (place_b later, or
    not yet). False when place_a is not visited yet."""
    done = visits(state, day_id)
    if place_a not in done:
        return False
    return place_b not in done or done.index(place_a) < done.index(place_b)


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


def reset_day(state, day_id, outcome_prefix=None):
    """New state without day_id's visits and cap ledger (and, given outcome_prefix, without the
    outcomes whose ids start with it). Other days are kept (the developer demo replays its own)."""
    new = dict(_state(state))
    for key in ("visits", "gains"):
        part = dict(new.get(key, {}))
        part.pop(day_id, None)
        new[key] = part
    if outcome_prefix:
        new["outcomes"] = frozenset(o for o in new.get("outcomes", ()) if not o.startswith(outcome_prefix))
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
    """What a Leia-side choice actually applied (summed over its picks, per stat, first-seen
    order). Callers that subtract a choice's effects again (a Day's lane exemption,
    lc_exhib_gained) use lc_choice_applied_effects, which falls back to the registered effects
    for every other choice (Ryan's choices are never capped)."""
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
