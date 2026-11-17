"""Social-feed phone app rules (pure Python, no Ren'Py import).

The feed is a parody photo-sharing app on Ryan's phone (display name LC_FEED_APP_NAME in
game/systems/feed.rpy, placeholder "Instababe"). Posts are init-time data registered once:
id, story day, author, @handle, caption, optional photo, 0-3 comments, likes, an optional
display time, an optional unlock gate and an optional one-time reaction. The story *releases*
posts where they should appear (one call may release a batch); release checks each post's gate
once, then the post stays on the feed (frozen, so a post the player saw never vanishes when a
stat moves later). Opening the feed counts as seeing every released post in it (the list shows
the captions); tapping a card also records it as opened. Reading the feed never changes stats.

All functions take the save state as plain values and return NEW objects instead of mutating
them, so the Ren'Py side can rebind store variables and rollback restores them cleanly.

Ren'Py side: game/systems/feed.rpy, game/screens/phone_feed.rpy. Tests: tests/test_feed.py.
"""
import re

MAX_COMMENTS = 3
BADGE_CAP = 9

# Player-editable names must be written as [player_name] / [girlfriend_name] / [friend_name].
_DEFAULT_NAMES = re.compile(r"\b(?:Ryan|Leia|Julian)\b")
# @handles are lower-case by convention ("leia.official"), so they are checked case-blind.
_DEFAULT_NAMES_ANY_CASE = re.compile(r"\b(?:ryan|leia|julian)\b", re.I)

# Where a photo is drawn: the feed list, the opened post, or the full-screen viewer.
PHOTO_CONTEXTS = ("list", "post", "viewer")

# Unlock-dict keys that are not story values: Leia's recorded choices (lc_leia_did).
UNLOCK_LEIA_DID = "leia_did"
UNLOCK_LEIA_DID_NOT = "leia_did_not"


def _check_text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("feed %s must be a non-empty string, got %r" % (name, value))


def _check_names(name, value, any_case=False):
    if (_DEFAULT_NAMES_ANY_CASE if any_case else _DEFAULT_NAMES).search(value):
        raise ValueError("feed %s types a default name (use [player_name], [girlfriend_name] "
                         "or [friend_name]): %r" % (name, value))


def _as_tuple(value):
    if isinstance(value, (list, tuple, set, frozenset)):
        return tuple(value)
    return (value,)


def _check_unlock(unlock):
    if unlock is None or callable(unlock):
        return
    if not isinstance(unlock, dict) or not unlock:
        raise ValueError("feed unlock must be None, a callable or a non-empty dict, got %r"
                         % (unlock,))
    for key, want in unlock.items():
        _check_text("unlock key", key)
        if key in (UNLOCK_LEIA_DID, UNLOCK_LEIA_DID_NOT):
            for mark in _as_tuple(want):
                _check_text("unlock " + key, mark)


def register(registry, post_id, day, author, handle, caption, image=None, comments=(), likes=0,
             when=None, unlock=None, mature=False, reaction=None):
    """Add one post to registry ({post_id: entry}). Bad fields or a duplicate id -> ValueError.

    comments: up to MAX_COMMENTS (handle, text) pairs. image: a Ren'Py image name (mature=True
    hides it behind an 18+ card outside the viewer). when: None (stamped from the story clock at
    release), a fixed time string, or a zero-argument callable evaluated once at release.
    unlock: None, a zero-argument callable, or a dict checked once at release (see unlock_ok).
    reaction: None, a label name, or a zero-argument callable run once, after the phone closes,
    the first time Ryan sees the post.
    """
    for field, value in (("post_id", post_id), ("day", day), ("author", author),
                         ("handle", handle), ("caption", caption)):
        _check_text(field, value)
    _check_names("author", author)
    _check_names("handle", handle, any_case=True)
    _check_names("caption", caption)
    if image is not None:
        _check_text("image", image)
    if when is not None and not callable(when):
        _check_text("when", when)
    if isinstance(likes, bool) or not isinstance(likes, int) or likes < 0:
        raise ValueError("feed likes must be a whole number >= 0, got %r" % (likes,))
    _check_unlock(unlock)
    if reaction is not None and not callable(reaction):
        _check_text("reaction", reaction)
    rows = tuple(comments or ())
    if len(rows) > MAX_COMMENTS:
        raise ValueError("feed post %s has %d comments (max %d)" % (post_id, len(rows), MAX_COMMENTS))
    clean = []
    for row in rows:
        if not isinstance(row, (tuple, list)) or len(row) != 2:
            raise ValueError("feed comment must be a (handle, text) pair, got %r" % (row,))
        _check_text("comment handle", row[0])
        _check_text("comment text", row[1])
        _check_names("comment handle", row[0], any_case=True)
        _check_names("comment text", row[1])
        clean.append((row[0], row[1]))
    if post_id in registry:
        raise ValueError("Duplicate feed post: " + post_id)
    registry[post_id] = {
        "id": post_id, "day": day, "author": author, "handle": handle, "caption": caption,
        "image": image, "comments": tuple(clean), "likes": likes, "when": when,
        "unlock": unlock, "mature": bool(mature), "reaction": reaction,
    }
    return None


def unlock_ok(entry, get_value=None, leia_did=None):
    """True when entry's gate holds now.

    unlock None -> True. A callable -> bool(unlock()). A dict -> every row must hold:
      story key -> value: get_value(key) == value; a list/tuple/set value means "any of these";
                  True means "set to anything truthy".
      "leia_did": id or ids -> leia_did(id) for each (all must hold).
      "leia_did_not": id or ids -> not leia_did(id) for each.
    A dict row whose lookup the caller cannot supply (get_value/leia_did None) is False, so a
    post never releases on a save that cannot answer its gate.
    """
    gate = entry.get("unlock")
    if gate is None:
        return True
    if callable(gate):
        return bool(gate())
    for key, want in gate.items():
        if key in (UNLOCK_LEIA_DID, UNLOCK_LEIA_DID_NOT):
            if leia_did is None:
                return False
            marks = _as_tuple(want)
            if key == UNLOCK_LEIA_DID and not all(leia_did(m) for m in marks):
                return False
            if key == UNLOCK_LEIA_DID_NOT and any(leia_did(m) for m in marks):
                return False
            continue
        if get_value is None:
            return False
        have = get_value(key)
        if want is True:
            if not have:
                return False
        elif isinstance(want, (list, tuple, set, frozenset)):
            if have not in want:
                return False
        elif have != want:
            return False
    return True


def release(registry, released, post_ids, is_unlocked=None):
    """Release a batch of posts. Returns (released, newly): newly lists the ids that came out
    now, in call order.

    released: post ids in release order (never mutated). An unknown id raises ValueError before
    anything changes. A post that is already out, or whose gate is_unlocked(entry) says False
    now, is skipped. Nothing new -> the same released object comes back with newly == [].
    """
    if isinstance(post_ids, str):
        post_ids = (post_ids,)
    post_ids = tuple(post_ids)
    for pid in post_ids:
        if pid not in registry:
            raise ValueError("Unknown feed post: %r" % (pid,))
    current = released if released is not None else []
    have = set(current)
    newly = []
    for pid in post_ids:
        if pid in have or pid in newly:
            continue
        if is_unlocked is not None and not is_unlocked(registry[pid]):
            continue
        newly.append(pid)
    if not newly:
        return current, []
    return list(current) + newly, newly


def banner_text(entries):
    """(title, body) for ONE banner covering a release batch, or None when nothing came out.
    One post: its author and caption. Several: "N new posts" and who posted."""
    entries = list(entries or ())
    if not entries:
        return None
    if len(entries) == 1:
        return entries[0]["author"], entries[0]["caption"]
    authors = []
    for entry in entries:
        if entry["author"] not in authors:
            authors.append(entry["author"])
    if len(authors) > 2:
        body = "%s, %s and more posted." % (authors[0], authors[1])
    else:
        body = " and ".join(authors) + " posted."
    return "%d new posts" % len(entries), body


def visible(registry, released):
    """Released posts that are still registered, newest release first."""
    return [registry[pid] for pid in reversed(list(released or ())) if pid in registry]


def mark_many(seen, post_ids):
    """seen plus post_ids as a new set; the same object back when nothing is new."""
    new = [pid for pid in post_ids if pid not in (seen or ())]
    if not new and seen is not None:
        return seen
    return set(seen or ()) | set(new)


def mark_seen(seen, post_id):
    """seen plus post_id as a new set; the same set back when it was already there."""
    return mark_many(seen, (post_id,))


def any_seen(seen, post_ids):
    return any(pid in (seen or ()) for pid in post_ids)


def unseen_ids(registry, released, seen):
    """Released, registered posts not seen yet, newest first."""
    return [entry["id"] for entry in visible(registry, released) if entry["id"] not in (seen or ())]


def unseen_count(registry, released, seen):
    return len(unseen_ids(registry, released, seen))


def badge_label(count):
    """None for no badge, else '1'..'9' or '9+'."""
    if not count:
        return None
    return "%d+" % BADGE_CAP if count > BADGE_CAP else str(count)


def likes_label(count):
    return "%d like%s" % (count, "" if count == 1 else "s")


def app_visible(installed, released):
    """The app sits on the home grid once installed (the story intro) or a post is out."""
    return bool(installed) or bool(released)


def photo_masked(entry, context, mask_mature=True):
    """True when a mature photo must be replaced by the 18+ card (feed list and opened post),
    following the Gallery switch (GALLERY_MASK_MATURE_COVERS); the full-screen viewer, which the
    player opens on purpose, shows it as the Gallery does."""
    return (bool(mask_mature) and bool(entry.get("image") and entry.get("mature"))
            and context != "viewer")


def stamp(entry, story_time):
    """The time to freeze on a post at release: a fixed `when` string, a callable `when`'s
    result, else the story clock (story_time) when one is set, else None (no time is shown:
    the device clock never leaks onto a post)."""
    when = entry.get("when")
    if callable(when):
        value = when()
        return value if isinstance(value, str) and value.strip() else None
    if when:
        return when
    return story_time or None


def reactions_due(registry, newly_seen, reacted):
    """Ids among newly_seen whose post has a reaction that has not run yet (in order)."""
    out = []
    for pid in newly_seen:
        entry = registry.get(pid)
        if entry and entry.get("reaction") is not None and pid not in (reacted or ()) and pid not in out:
            out.append(pid)
    return out


def reveal_delta(top, height, view_top, view_bottom, margin=0):
    """How far to scroll a viewport so a focused card shows fully, with margin to spare (a peek
    of the next card, so focus can keep moving). Positive scrolls down, 0 when it already fits.

    [top, top+height) is the card's FOCUS rect, which Ren'Py clips to the viewport: a card cut off
    at an edge reports only its visible part, so its real size is unknown. A card touching the
    bottom edge scrolls until its top sits margin below the view's top; one touching the top edge
    scrolls until its visible bottom sits margin above the view's bottom. When that would not
    move at all (a card taller than the view), it scrolls by a page instead.
    """
    bottom = top + height
    page = max(1, (view_bottom - view_top) - 2 * margin)
    if bottom >= view_bottom - 1 and top > view_top + 1:
        delta = top - (view_top + margin)
        return delta if delta > 0 else page
    if top <= view_top + 1 and bottom < view_bottom - 1:
        delta = bottom - (view_bottom - margin)
        return delta if delta < 0 else -page
    if bottom > view_bottom - margin:
        return bottom - (view_bottom - margin)
    if top < view_top + margin:
        return top - (view_top + margin)
    return 0
