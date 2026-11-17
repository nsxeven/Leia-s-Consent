"""Discovery registry and Moments strip rules (pure Python, no Ren'Py import).

A *discovery* is an optional moment a player can find during a Day: a Hidden POV opened, a
detail noticed, a door choice taken, a phone moment answered. Each registers once, at init,
under the review day it belongs to. The end-of-day review draws a strip of them: found ones
always, unfound ones (as grey silhouettes with label and mood only) only once the Day has been
cleared on the profile. Immersive ("normal") mode never shows counts or route words.

Ren'Py side: game/systems/discovery.rpy. Tests: tests/test_discovery.py.
"""
import re

KINDS = ("pov", "notice", "door", "phone")

# Neutral stand-in label when an Immersive-mode label would name a route.
KIND_LABELS = {
    "pov": "A hidden view",
    "notice": "Something noticed",
    "door": "A moment",
    "phone": "A message",
}

# Route and lane vocabulary that Immersive mode must not show (whole words, any case).
_ROUTE_WORDS = re.compile(
    r"\b(?:love|ntr|nts|exhib\w*|sharing|shared|temptation|tempted|cuck\w*|hotwife|route|lane)\b",
    re.IGNORECASE,
)


def has_route_words(text):
    """True when text names a route, lane or stat that Immersive mode keeps hidden."""
    return bool(_ROUTE_WORDS.search(text or ""))


def _check_text(name, value, allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ValueError("discovery %s must be a %sstring, got %r"
                         % (name, "" if allow_empty else "non-empty ", value))


def find(registry, moment_id):
    """The registered entry for moment_id on any day, or None."""
    for entries in registry.values():
        for entry in entries:
            if entry["id"] == moment_id:
                return entry
    return None


def register(registry, day_id, moment_id, kind, label, mood, image=None):
    """Add one discovery to registry ({day_id: [entry, ...]}) in registration order.

    kind is one of KINDS; moment ids are unique across every day (duplicate -> ValueError).
    image (optional) is the stable image the strip shows as the thumbnail / silhouette.
    """
    _check_text("day_id", day_id)
    _check_text("moment_id", moment_id)
    _check_text("label", label)
    _check_text("mood", mood, allow_empty=True)
    if kind not in KINDS:
        raise ValueError("discovery kind must be one of %s, got %r" % ("|".join(KINDS), kind))
    if image is not None:
        _check_text("image", image)
    if find(registry, moment_id) is not None:
        raise ValueError("Duplicate discovery: " + moment_id)
    registry.setdefault(day_id, []).append({
        "id": moment_id, "day_id": day_id, "kind": kind,
        "label": label, "mood": mood, "image": image,
    })
    return None


def strip(registry, day_id, found, day_cleared, mode):
    """Items for the day's Moments strip, in registration order.

    Each item is {"id", "kind", "label", "mood", "found", "image"}. Unfound entries are left
    out unless day_cleared. In Immersive mode (mode == "normal") a label that names a route
    becomes the kind's neutral label and such a mood is dropped. found may be None (old saves).
    """
    found = found or ()
    items = []
    for entry in registry.get(day_id, ()):
        is_found = entry["id"] in found
        if not is_found and not day_cleared:
            continue
        label, mood = entry["label"], entry["mood"]
        if mode == "normal":
            if has_route_words(label):
                label = KIND_LABELS[entry["kind"]]
            if has_route_words(mood):
                mood = ""
        items.append({"id": entry["id"], "kind": entry["kind"], "label": label,
                      "mood": mood, "found": is_found, "image": entry["image"]})
    return items


def count_line(items, mode):
    """'n of m' for Insight/Full/Developer; None in Immersive or when there is nothing to count."""
    if mode == "normal" or not items:
        return None
    return "%d of %d" % (sum(1 for item in items if item["found"]), len(items))


def cleared_before(day_id, cleared, first_runs, run_id):
    """True when the profile had finished day_id before this playthrough's review of it.

    cleared: the profile's finished review days; first_runs: {day_id: run id of the playthrough
    that first finished it}. The playthrough that first finished the day keeps reading False, so
    rolling back past its review and replaying stays a first clear. A day finished before run ids
    existed (or carried over from older completion evidence) has no first run: it reads True.
    """
    if day_id not in (cleared or ()):
        return False
    first = (first_runs or {}).get(day_id)
    return not (run_id and first == run_id)


# Moments strip geometry (screens/day_review_screen.rpy): ONE row of fixed height at any count.
# Header line (24) + spacing (4) + the tile row; extra tiles scroll sideways, never wrap.
STRIP_TILE_W = 136
STRIP_TILE_H = 122
STRIP_GAP = 8
STRIP_HEIGHT = 24 + 4 + STRIP_TILE_H


def strip_layout(count, width):
    """{"height", "content_w", "overflow"} for count tiles in a strip width px wide.
    height is constant (STRIP_HEIGHT); overflow is True when the tiles need to scroll."""
    content_w = max(0, count * STRIP_TILE_W + (count - 1) * STRIP_GAP)
    return {"height": STRIP_HEIGHT, "content_w": content_w, "overflow": content_w > width}
