"""Social-feed phone app rules (pure Python, no Ren'Py import).

The feed is a parody photo-sharing app on Ryan's phone (display name LC_FEED_APP_NAME in
game/systems/feed.rpy, placeholder "Instababe"). Posts are init-time data registered once:
id, story day, author, @handle, caption, optional photo, 0-3 comments, likes, a display time
and an optional unlock condition. The story *releases* a post at the point it should appear;
release checks the unlock condition once, then the post stays on the feed (frozen, so a post
the player saw never vanishes when a stat moves later). Opening a post writes a save-local
seen record that later scenes may read. Reading the feed never changes stats.

All functions take the save state as plain values and return NEW objects instead of mutating
them, so the Ren'Py side can rebind store variables and rollback restores them cleanly.

Ren'Py side: game/systems/feed.rpy, game/screens/phone_feed.rpy. Tests: tests/test_feed.py.
"""
import re

MAX_COMMENTS = 3
BADGE_CAP = 9

# Player-editable names must be written as [player_name] / [girlfriend_name] / [friend_name].
_DEFAULT_NAMES = re.compile(r"\b(?:Ryan|Leia|Julian)\b")

# Where a photo is drawn: the feed list, the opened post, or the full-screen viewer.
PHOTO_CONTEXTS = ("list", "post", "viewer")


def _check_text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("feed %s must be a non-empty string, got %r" % (name, value))


def _check_names(name, value):
    if _DEFAULT_NAMES.search(value):
        raise ValueError("feed %s types a default name (use [player_name], [girlfriend_name] "
                         "or [friend_name]): %r" % (name, value))


def register(registry, post_id, day, author, handle, caption, image=None, comments=(), likes=0,
             when=None, unlock=None, mature=False):
    """Add one post to registry ({post_id: entry}). Bad fields or a duplicate id -> ValueError.

    comments: up to MAX_COMMENTS (handle, text) pairs. unlock: None or a zero-argument callable
    checked at release. image: a Ren'Py image name (mature=True masks it outside the viewer).
    """
    for field, value in (("post_id", post_id), ("day", day), ("author", author),
                         ("handle", handle), ("caption", caption)):
        _check_text(field, value)
    _check_names("caption", caption)
    if image is not None:
        _check_text("image", image)
    if when is not None:
        _check_text("when", when)
    if isinstance(likes, bool) or not isinstance(likes, int) or likes < 0:
        raise ValueError("feed likes must be a whole number >= 0, got %r" % (likes,))
    if unlock is not None and not callable(unlock):
        raise ValueError("feed unlock must be None or a callable, got %r" % (unlock,))
    rows = tuple(comments or ())
    if len(rows) > MAX_COMMENTS:
        raise ValueError("feed post %s has %d comments (max %d)" % (post_id, len(rows), MAX_COMMENTS))
    clean = []
    for row in rows:
        if not isinstance(row, (tuple, list)) or len(row) != 2:
            raise ValueError("feed comment must be a (handle, text) pair, got %r" % (row,))
        _check_text("comment handle", row[0])
        _check_text("comment text", row[1])
        _check_names("comment handle", row[0])
        _check_names("comment text", row[1])
        clean.append((row[0], row[1]))
    if post_id in registry:
        raise ValueError("Duplicate feed post: " + post_id)
    registry[post_id] = {
        "id": post_id, "day": day, "author": author, "handle": handle, "caption": caption,
        "image": image, "comments": tuple(clean), "likes": likes, "when": when,
        "unlock": unlock, "mature": bool(mature),
    }
    return None


def release(registry, released, banner_days, post_id):
    """Make post_id appear. Returns (released, banner_days, banner).

    released: post ids in release order; banner_days: days that already showed a banner (one
    banner per day). An unknown id raises ValueError. A post whose unlock condition is False
    now, or that is already out, changes nothing (the same objects come back, banner False).
    """
    entry = registry.get(post_id)
    if entry is None:
        raise ValueError("Unknown feed post: %r" % (post_id,))
    released = released if released is not None else []
    banner_days = banner_days if banner_days is not None else set()
    if post_id in released or (entry["unlock"] is not None and not entry["unlock"]()):
        return released, banner_days, False
    banner = entry["day"] not in banner_days
    return list(released) + [post_id], set(banner_days) | {entry["day"]}, banner


def visible(registry, released):
    """Released posts that are still registered, newest release first."""
    return [registry[pid] for pid in reversed(list(released or ())) if pid in registry]


def mark_seen(seen, post_id):
    """seen plus post_id as a new set; the same set back when it was already there."""
    if seen is not None and post_id in seen:
        return seen
    return set(seen or ()) | {post_id}


def any_seen(seen, post_ids):
    return any(pid in (seen or ()) for pid in post_ids)


def unseen_count(registry, released, seen):
    return sum(1 for entry in visible(registry, released) if entry["id"] not in (seen or ()))


def badge_label(count):
    """None for no badge, else '1'..'9' or '9+'."""
    if not count:
        return None
    return "%d+" % BADGE_CAP if count > BADGE_CAP else str(count)


def app_visible(installed, released):
    """The app sits on the home grid once installed (the story intro) or a post is out."""
    return bool(installed) or bool(released)


def photo_masked(entry, context):
    """True when a mature photo must be blurred with an 18+ mark (feed list and opened post);
    the full-screen viewer, which the player opens on purpose, shows it as the Gallery does."""
    return bool(entry.get("image") and entry.get("mature")) and context != "viewer"
