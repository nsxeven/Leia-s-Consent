"""Crop maths for the phone wallpaper editor (pure Python, no Ren'Py).

A wallpaper is saved as plain data:

    {"image": "<ren'py image name>", "zoom": 1.0..4.0, "x": 0..1, "y": 0..1}

``zoom`` is relative to the "cover" scale: 1.0 means the photo just covers
the phone screen with no empty edge (the smallest allowed), 4.0 is 4x that.
``x``/``y`` are the centre of the visible screen in normalised image
coordinates (0..1), so a crop stays the same if the photo is re-exported at
another resolution. Every helper clamps so the screen is always covered.
"""

ZOOM_MIN = 1.0
ZOOM_MAX = 4.0
ZOOM_STEP = 1.25  # one +/- button press
WHEEL_STEP = 1.1  # one mouse-wheel notch (finer, like a trackpad pinch)


def _num(value, default):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return default
    if value != value or value in (float("inf"), float("-inf")):
        return default
    return value


def cover_scale(iw, ih, sw, sh):
    """Scale at which an iw x ih image just covers an sw x sh screen."""
    if iw <= 0 or ih <= 0:
        return 1.0
    return max(float(sw) / iw, float(sh) / ih)


def clamp_zoom(zoom):
    return min(ZOOM_MAX, max(ZOOM_MIN, _num(zoom, ZOOM_MIN)))


def half_view(iw, ih, sw, sh, zoom):
    """Half the visible width/height, as a fraction of the image (<= 0.5)."""
    scale = cover_scale(iw, ih, sw, sh) * clamp_zoom(zoom)
    hx = float(sw) / (iw * scale) / 2.0 if iw > 0 else 0.5
    hy = float(sh) / (ih * scale) / 2.0 if ih > 0 else 0.5
    return min(0.5, hx), min(0.5, hy)


def clamp_centre(cx, cy, iw, ih, sw, sh, zoom):
    """Keep the visible window inside the image (no empty screen edge)."""
    hx, hy = half_view(iw, ih, sw, sh, zoom)
    cx = min(1.0 - hx, max(hx, _num(cx, 0.5)))
    cy = min(1.0 - hy, max(hy, _num(cy, 0.5)))
    return cx, cy


def pan(cx, cy, dx, dy, iw, ih, sw, sh, zoom):
    """Drag by (dx, dy) screen pixels: the photo follows the finger."""
    scale = cover_scale(iw, ih, sw, sh) * clamp_zoom(zoom)
    cx = _num(cx, 0.5) - float(dx) / (iw * scale)
    cy = _num(cy, 0.5) - float(dy) / (ih * scale)
    return clamp_centre(cx, cy, iw, ih, sw, sh, zoom)


def zoom_at(cx, cy, zoom, new_zoom, px, py, iw, ih, sw, sh):
    """Zoom to new_zoom keeping the photo point under (px, py) still.

    (px, py) is the pointer in screen pixels from the screen's top-left.
    Returns (cx, cy, zoom), clamped.
    """
    zoom = clamp_zoom(zoom)
    new_zoom = clamp_zoom(new_zoom)
    base = cover_scale(iw, ih, sw, sh)
    ox = float(px) - sw / 2.0
    oy = float(py) - sh / 2.0
    ux = _num(cx, 0.5) + ox / (iw * base * zoom)
    uy = _num(cy, 0.5) + oy / (ih * base * zoom)
    cx = ux - ox / (iw * base * new_zoom)
    cy = uy - oy / (ih * base * new_zoom)
    cx, cy = clamp_centre(cx, cy, iw, ih, sw, sh, new_zoom)
    return cx, cy, new_zoom


def step_zoom(zoom, steps, factor=ZOOM_STEP):
    """Zoom after `steps` button presses / wheel notches (negative = out)."""
    zoom = clamp_zoom(zoom) * (float(factor) ** steps)
    # Snap tiny float drift so repeated in/out lands back on 1.0 exactly.
    if abs(zoom - round(zoom, 3)) < 1e-6:
        zoom = round(zoom, 3)
    return clamp_zoom(zoom)


def crop_rect(iw, ih, sw, sh, zoom, cx, cy):
    """(x, y, w, h) in image pixels that fills the screen, same aspect."""
    zoom = clamp_zoom(zoom)
    cx, cy = clamp_centre(cx, cy, iw, ih, sw, sh, zoom)
    scale = cover_scale(iw, ih, sw, sh) * zoom
    w = min(float(iw), sw / scale)
    h = min(float(ih), sh / scale)
    x = min(max(0.0, cx * iw - w / 2.0), iw - w)
    y = min(max(0.0, cy * ih - h / 2.0), ih - h)
    return x, y, w, h


def make(image, zoom=ZOOM_MIN, cx=0.5, cy=0.5):
    """Plain, save-safe wallpaper record (str + floats only)."""
    return {
        "image": str(image),
        "zoom": round(clamp_zoom(zoom), 4),
        "x": round(min(1.0, max(0.0, _num(cx, 0.5))), 5),
        "y": round(min(1.0, max(0.0, _num(cy, 0.5))), 5),
    }


def normalize(data):
    """A valid wallpaper record from saved data, or None (old/broken saves)."""
    if not isinstance(data, dict):
        return None
    image = data.get("image")
    if not isinstance(image, str) or not image.strip():
        return None
    return make(image.strip(), data.get("zoom", ZOOM_MIN), data.get("x", 0.5), data.get("y", 0.5))
