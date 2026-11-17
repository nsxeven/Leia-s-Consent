"""Things Ryan noticed: push-in notice rules (pure Python, no Ren'Py import).

A *notice* is a detail already in a CG that Ryan can stop on: a small eye cue sits on the CG
while it is on screen; clicking it pushes the camera in on `focus_rect` (zoom <= 1.4, because
the CGs are 1920x1080 and more would blur) and shows Ryan's one or two thought captions. The
captions may change by lane (Love captions are about Leia); the spot never does. Opening one
writes a save-local record {notice_id: lane seen}, and the phone Status app pins it under
"Things I noticed". Noticing never changes stats; a later talk may offer an extra option.

Ren'Py side: game/systems/notice.rpy, game/screens/notice_screen.rpy. Tests: tests/test_notice.py.
"""
import re

FRAME = (1920, 1080)
MIN_ZOOM = 1.0
MAX_ZOOM = 1.4
DEFAULT_ZOOM = 1.35

# Caption lanes, from the stats-model lean (systems/stats.rpy lc_current_lean), coloured on the
# Love lean by Leia's Day Two tint (lc_leia_tint): see lane_from_lean.
LANES = ("love", "exhib", "ntr")
_LEAN_TO_LANE = {"love": "love", "love_exhib": "exhib", "ntr": "ntr"}

MAX_LINES = 2
MAX_LINE_CHARS = 150
# The Status pin shows the first caption in a fixed-height card: 4 lines at most.
MAX_PIN_CHARS = 125
DEFAULT_LABEL = "Something I noticed"

# Player-editable names must be written as [player_name] / [girlfriend_name] / [friend_name].
_DEFAULT_NAMES = re.compile(r"\b(?:Ryan|Leia|Julian)\b")
_NAME_DEFAULTS = {"player_name": "Ryan", "girlfriend_name": "Leia", "friend_name": "Julian"}


# ---------------------------------------------------------------- geometry

def _is_rect(rect):
    return (isinstance(rect, (tuple, list)) and len(rect) == 4
            and all(isinstance(v, (int, float)) for v in rect))


def rect_in_frame(rect, frame=FRAME):
    """True when rect (x, y, w, h) has a size and sits wholly inside the frame."""
    if not _is_rect(rect):
        return False
    x, y, w, h = rect
    return w > 0 and h > 0 and x >= 0 and y >= 0 and x + w <= frame[0] and y + h <= frame[1]


def rects_overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def hit_rect(center, size):
    """Square hit area of `size` px centred on center (same rule as Hidden POV)."""
    cx, cy = center
    return (int(cx - size // 2), int(cy - size // 2), size, size)


def clamp_zoom(zoom):
    return max(MIN_ZOOM, min(MAX_ZOOM, float(zoom)))


def focus_transform(focus_rect, zoom=DEFAULT_ZOOM, frame=FRAME):
    """(xalign, yalign, zoom) that pushes a full-frame CG in on focus_rect.

    zoom is clamped to MIN_ZOOM..MAX_ZOOM and lowered further when the rect would not fit the
    visible window. The window is centred on the rect and kept inside the frame. A full-frame
    image shown with Transform(xalign=a, zoom=z) sits at x = a * W * (1 - z), so the visible
    source window starts at a * (W - W / z).
    """
    w, h = frame
    fx, fy, fw, fh = focus_rect
    z = clamp_zoom(zoom)
    z = max(MIN_ZOOM, min(z, w / float(fw), h / float(fh)))
    if z <= MIN_ZOOM + 1e-9:
        return (0.5, 0.5, 1.0)
    vw, vh = w / z, h / z
    left = min(max(fx + fw / 2.0 - vw / 2.0, 0.0), w - vw)
    top = min(max(fy + fh / 2.0 - vh / 2.0, 0.0), h - vh)
    return (round(left / (w - vw), 4), round(top / (h - vh), 4), round(z, 4))


# Caption box bands on screen (y, height): the dialogue-box spot, and a top spot below the Back
# button for a detail that the push-in leaves in the lower part of the screen. The box is the
# dialogue paper (222 px tall); it only ever stretches sideways.
CAPTION_BOTTOM = (792, 222)
CAPTION_TOP = (110, 222)
CAPTION_X = 132
CAPTION_W = 1656
CAPTION_MIN_W = 900


def focus_on_screen(focus_rect, zoom=DEFAULT_ZOOM, frame=FRAME):
    """Where focus_rect lands on screen after focus_transform (x, y, w, h)."""
    w, h = frame
    xa, ya, z = focus_transform(focus_rect, zoom, frame)
    off_x, off_y = xa * w * (1 - z), ya * h * (1 - z)
    fx, fy, fw, fh = focus_rect
    return (off_x + fx * z, off_y + fy * z, fw * z, fh * z)


def caption_slot(focus_rect, zoom=DEFAULT_ZOOM, frame=FRAME):
    """'bottom' (the dialogue-box spot) unless the pushed-in detail sits under it; then 'top'."""
    _x, y, _w, fh = focus_on_screen(focus_rect, zoom, frame)

    def cover(band):
        by, bh = band
        return max(0.0, min(y + fh, by + bh) - max(y, by))

    return "top" if cover(CAPTION_BOTTOM) > cover(CAPTION_TOP) else "bottom"


def caption_box(entry, frame=FRAME):
    """Caption paper on screen (x, y, w, h): the registration's caption_box (x, y, w) when given,
    else the full-width bottom spot, or the top spot when the detail sits under it."""
    if entry.get("caption_box"):
        x, y, w = entry["caption_box"]
        return (x, y, w, CAPTION_BOTTOM[1])
    slot = caption_slot(entry["focus_rect"], entry["zoom"], frame)
    y, h = CAPTION_TOP if slot == "top" else CAPTION_BOTTOM
    return (CAPTION_X, y, CAPTION_W, h)


# ---------------------------------------------------------------- registry

def lane_from_lean(lean, tint=None):
    """Caption lane for a stats-model lean ('love' / 'love_exhib' / 'ntr'); None otherwise.

    tint is Leia's Love-lane tint (lc_stat_model.leia_tint with lane 'love', which never returns
    temptation). On the Love lean, an Exhibitionism tint picks the exhib captions: early in a day
    (Day Two scene 1, before any Day Two choice) the lane can't be Love + Exhib yet, so this is
    how a save that leans that way still sees them. Nothing ever moves a lean toward NTR.
    """
    if lean == "love" and tint == "exhibitionism":
        return "exhib"
    return _LEAN_TO_LANE.get(lean)


def _lines(name, value):
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError("notice %s must be a list of 1-%d strings, got %r" % (name, MAX_LINES, value))
    if not 1 <= len(value) <= MAX_LINES:
        raise ValueError("notice %s needs 1-%d lines, got %d" % (name, MAX_LINES, len(value)))
    for line in value:
        if not isinstance(line, str) or not line.strip():
            raise ValueError("notice %s has an empty or non-text line: %r" % (name, line))
    return tuple(value)


def _text(name, value, optional=False):
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError("notice %s must be a non-empty string, got %r" % (name, value))
    return value


def register(registry, notice_id, source, center, focus_rect, zoom=DEFAULT_ZOOM, lines=None,
             lane_lines=None, closeup=None, day_id=None, label=None, mood=None, caption_box=None):
    """Add one notice to registry ({notice_id: entry}) and return the entry.

    Shape errors (duplicate id, missing captions, unknown lane, malformed points) raise
    ValueError at once; placement problems are reported by validate() after every
    registration has loaded.
    """
    _text("notice_id", notice_id)
    if notice_id in registry:
        raise ValueError("Duplicate notice: " + notice_id)
    _text("source", source)
    if not (isinstance(center, (tuple, list)) and len(center) == 2):
        raise ValueError("notice center must be an (x, y) pixel pair, got %r" % (center,))
    if not _is_rect(focus_rect):
        raise ValueError("notice focus_rect must be (x, y, w, h), got %r" % (focus_rect,))
    if caption_box is not None and not (isinstance(caption_box, (tuple, list)) and len(caption_box) == 3
                                        and all(isinstance(v, (int, float)) for v in caption_box)):
        raise ValueError("notice caption_box must be (x, y, width), got %r" % (caption_box,))
    base = _lines("lines", lines)
    lanes = {}
    for lane, value in (lane_lines or {}).items():
        if lane not in LANES:
            raise ValueError("notice lane must be one of %s, got %r" % ("|".join(LANES), lane))
        lanes[lane] = _lines("lane_lines[%r]" % lane, value)
    entry = {
        "id": notice_id, "source": source, "center": tuple(center),
        "focus_rect": tuple(focus_rect), "zoom": float(zoom), "lines": base,
        "lane_lines": lanes, "closeup": _text("closeup", closeup, optional=True),
        "day_id": _text("day_id", day_id, optional=True),
        "label": _text("label", label, optional=True),
        "mood": mood if isinstance(mood, str) else "",
        "caption_box": tuple(caption_box) if caption_box is not None else None,
    }
    registry[notice_id] = entry
    return entry


def caption_lines(entry, lane):
    """The captions for lane (its lane_lines when given, else the base lines)."""
    return entry["lane_lines"].get(lane) or entry["lines"]


def fill_names(text, names):
    """Fill [player_name] / [girlfriend_name] / [friend_name]; missing names use the defaults."""
    names = names or {}
    for key, default in _NAME_DEFAULTS.items():
        text = text.replace("[%s]" % key, names.get(key) or default)
    return text


def validate(entry, hitbox, reserved_rects, pov_rects=(), others=(), frame=FRAME):
    """Problems with one registration (empty list when it is sound).

    hitbox: the largest cue hit square (touch builds); reserved_rects: ((label, rect), ...) the
    cue must avoid; pov_rects: ((moment_id, source, hit rect), ...) Hidden POV cues; others:
    other notice entries. Only cues on the same source CG can collide.
    """
    problems = []
    rect = hit_rect(entry["center"], hitbox)
    if not rect_in_frame(rect, frame):
        problems.append("cue hit area %r leaves the %dx%d frame" % (rect, frame[0], frame[1]))
    for label, reserved in reserved_rects:
        if rects_overlap(rect, reserved):
            problems.append("cue hit area %r overlaps the %s %r" % (rect, label, reserved))
    for moment_id, source, pov_rect in pov_rects:
        if source == entry["source"] and rects_overlap(rect, pov_rect):
            problems.append("cue hit area %r overlaps Hidden POV %s %r" % (rect, moment_id, pov_rect))
    for other in others:
        if other["id"] != entry["id"] and other["source"] == entry["source"]:
            if rects_overlap(rect, hit_rect(other["center"], hitbox)):
                problems.append("cue hit area %r overlaps notice %s" % (rect, other["id"]))
    if not rect_in_frame(entry["focus_rect"], frame):
        problems.append("focus_rect %r is not inside the %dx%d frame"
                        % ((entry["focus_rect"],) + tuple(frame)))
    if not MIN_ZOOM < entry["zoom"] <= MAX_ZOOM:
        problems.append("zoom %r is outside %.1f-%.1f (CGs are %dx%d)" % (entry["zoom"], MIN_ZOOM, MAX_ZOOM,
                                                                         frame[0], frame[1]))
    box = entry.get("caption_box")
    if box is not None:
        x, y, bw = box
        if not rect_in_frame((x, y, bw, CAPTION_BOTTOM[1]), frame) or not CAPTION_MIN_W <= bw <= CAPTION_W:
            problems.append("caption_box %r must sit inside the frame and be %d-%d px wide"
                            % (box, CAPTION_MIN_W, CAPTION_W))
    for first in [entry["lines"][0]] + [lines[0] for lines in entry["lane_lines"].values()]:
        if len(first) > MAX_PIN_CHARS:
            problems.append("first caption %r is too long for the Status pin (max %d characters)"
                            % (first[:40], MAX_PIN_CHARS))
    texts = list(entry["lines"]) + [line for lines in entry["lane_lines"].values() for line in lines]
    texts += [entry["label"] or "", entry["mood"] or ""]
    for text in texts:
        if _DEFAULT_NAMES.search(text):
            problems.append("caption %r types a default name; use [player_name] / [girlfriend_name] / "
                            "[friend_name]" % text)
        if len(text) > MAX_LINE_CHARS:
            problems.append("caption %r is too long (max %d characters)" % (text[:40], MAX_LINE_CHARS))
    return problems


# ---------------------------------------------------------------- found record

def noticed(found, notice_id):
    return notice_id in (found or {})


def noticed_any(found, notice_ids):
    return any(noticed(found, notice_id) for notice_id in notice_ids)


def record(found, notice_id, lane):
    """The save record with notice_id added (lane = the caption lane seen then).

    Returns a NEW dict, so Ren'Py's rollback and saves see the change; the first answer stands,
    so a repeat open returns `found` itself (no new rollback entry, no double count).
    """
    found = found or {}
    if notice_id in found:
        return found
    updated = dict(found)
    updated[notice_id] = lane
    return updated


def pins(registry, found):
    """Status pins for every noticed entry, in registration order, with the captions seen."""
    found = found or {}
    items = []
    for notice_id, entry in registry.items():
        if notice_id not in found:
            continue
        lane = found[notice_id]
        items.append({"id": notice_id, "label": entry["label"] or DEFAULT_LABEL, "lane": lane,
                      "lines": caption_lines(entry, lane), "source": entry["source"],
                      "closeup": entry["closeup"], "focus_rect": entry["focus_rect"]})
    return items


# Status pin row geometry (screens/notice_screen.rpy): ONE row of fixed height at any count;
# extra pins scroll sideways, never wrap. A pin is wide enough for its first caption line,
# so the phone card shows one pin and the edge of the next.
PIN_W = 300
PIN_H = 268
PIN_GAP = 12
PIN_THUMB_H = 120


def pin_layout(count, width):
    """{"height", "content_w", "overflow"} for count pins in a row width px wide."""
    content_w = max(0, count * PIN_W + (count - 1) * PIN_GAP)
    return {"height": PIN_H, "content_w": content_w, "overflow": content_w > width}


def thumb_crop(focus_rect, width, height, frame=FRAME):
    """Source crop (x, y, w, h) with the thumbnail's aspect that covers the focus rect's centre
    and stays inside the frame, so a pin shows the noticed detail without stretching."""
    fx, fy, fw, fh = focus_rect
    aspect = float(width) / height
    cw = max(fw, fh * aspect)
    ch = cw / aspect
    if ch > frame[1]:
        ch = float(frame[1])
        cw = ch * aspect
    if cw > frame[0]:
        cw = float(frame[0])
        ch = cw / aspect
    x = min(max(fx + fw / 2.0 - cw / 2.0, 0.0), frame[0] - cw)
    y = min(max(fy + fh / 2.0 - ch / 2.0, 0.0), frame[1] - ch)
    return (int(round(x)), int(round(y)), int(round(cw)), int(round(ch)))
