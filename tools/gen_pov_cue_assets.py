"""Generate the Hidden POV cue glows and the sparkle chime (all project-made).

Run from the repo root: python tools/gen_pov_cue_assets.py
Outputs:
  game/gui/pov/glow_idle.svg, game/gui/pov/glow_hover.svg  (radial-gradient glows)
  game/gui/pov/bang_idle.svg, game/gui/pov/bang_hover.svg, game/gui/pov/bang_ring.svg
      (Full Transparency / Developer red circular "!" button, its hover state
      and the idle pulse ring; the "!" is drawn as shapes so it is exactly centred)
  game/systems/hidden_pov_chime.rpy  (the chime as an embedded OGG, played with
  Ren'Py's AudioData, so the asset stays a reviewable text file)
"""
import base64, subprocess, tempfile, textwrap, wave
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def glow_svg(path, rgb, size=112, peak=0.55, falloff=2.4, steps=12):
    """Same falloff as glow(): opacity = (1 - r) ** falloff * peak."""
    hexcol = "#%02x%02x%02x" % rgb
    stops = "\n".join(
        '    <stop offset="%.3f" stop-color="%s" stop-opacity="%.4f"/>' % (i / steps, hexcol, (1 - i / steps) ** falloff * peak)
        for i in range(steps + 1))
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">\n'
        '  <radialGradient id="g" cx="50%" cy="50%" r="50%">\n{stops}\n  </radialGradient>\n'
        '  <circle cx="{h}" cy="{h}" r="{h}" fill="url(#g)"/>\n</svg>\n'
    ).format(s=size, h=size / 2, stops=stops)
    Path(path).write_text(svg, encoding="utf-8")


BANG_SIZE = 80          # canvas; the button itself is 62 px across
BANG_RED = "#d6334a"
BANG_RED_HOVER = "#ee4b61"
BANG_RIM = "#8a1c2e"


def bang_svg(path, body, hover=False):
    """Red circular button with a darker rim, soft shadow and a white "!"."""
    c = BANG_SIZE / 2
    ring = ('  <circle cx="{c}" cy="{c}" r="35.5" fill="none" stroke="#ffffff" stroke-width="3" stroke-opacity="0.95"/>\n'
            .format(c=c) if hover else "")
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">
  <radialGradient id="shadow" cx="50%" cy="50%" r="50%">
    <stop offset="0.00" stop-color="#1a0a10" stop-opacity="0.45"/>
    <stop offset="0.70" stop-color="#1a0a10" stop-opacity="0.22"/>
    <stop offset="1.00" stop-color="#1a0a10" stop-opacity="0"/>
  </radialGradient>
  <ellipse cx="{c}" cy="{sy}" rx="35" ry="33" fill="url(#shadow)"/>
  <circle cx="{c}" cy="{c}" r="31" fill="{rim}"/>
  <circle cx="{c}" cy="{c}" r="28.5" fill="{body}"/>
  <ellipse cx="{c}" cy="{gy}" rx="19" ry="10" fill="#ffffff" fill-opacity="0.16"/>
{ring}  <rect x="{bx}" y="{by}" width="8" height="24" rx="4" ry="4" fill="#ffffff"/>
  <circle cx="{c}" cy="{dy}" r="4.5" fill="#ffffff"/>
</svg>
""".format(s=BANG_SIZE, c=c, sy=c + 3, gy=c - 15, rim=BANG_RIM, body=body, ring=ring,
           bx=c - 4, by=c - 19, dy=c + 14)
    Path(path).write_text(svg, encoding="utf-8")


def bang_ring_svg(path):
    """Thin ring for the idle pulse (scaled/faded by ATL)."""
    c = BANG_SIZE / 2
    Path(path).write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">\n'
        '  <circle cx="{c}" cy="{c}" r="30" fill="none" stroke="{red}" stroke-width="3"/>\n</svg>\n'
        .format(s=BANG_SIZE, c=c, red=BANG_RED), encoding="utf-8")


def glow(path, rgb, size=112, peak=0.55, falloff=2.4):
    # Rendered at 4x and downsampled: smooth falloff with a clean, round edge.
    s = size * 4
    y, x = np.mgrid[0:s, 0:s] + 0.5
    r = np.hypot(x - s / 2, y - s / 2) / (s / 2)
    a = np.clip(1 - r, 0, 1) ** falloff * peak
    img = np.zeros((s, s, 4), np.uint8)
    img[..., :3] = rgb
    img[..., 3] = (a * 255).round().astype(np.uint8)
    Image.fromarray(img, "RGBA").resize((size, size), Image.LANCZOS).save(path, optimize=True)


def chime(path, sr=44100):
    """Write the chime as OGG Vorbis to `path`."""
    # Two soft bell partials (E6 then B6) with a quick attack and gentle decay.
    t = np.arange(int(sr * 0.75)) / sr
    def bell(f, start, amp):
        tt = np.clip(t - start, 0, None)
        env = np.where(t >= start, (1 - np.exp(-tt * 180)) * np.exp(-tt * 6.5), 0)
        return amp * env * (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 10))
    sig = bell(1318.5, 0.0, 0.5) + bell(1975.5, 0.07, 0.38)
    sig *= 0.22 / np.max(np.abs(sig))
    fade = int(sr * 0.02)
    sig[-fade:] *= np.linspace(1, 0, fade)
    pcm = (sig * 32767).astype(np.int16)
    with tempfile.TemporaryDirectory() as d:
        w = Path(d) / "c.wav"
        with wave.open(str(w), "wb") as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
            f.writeframes(pcm.tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-ar", "32000", "-c:a", "libvorbis", "-q:a", "1", str(path)], check=True)


def chime_rpy(path):
    with tempfile.TemporaryDirectory() as d:
        ogg = Path(d) / "sparkle.ogg"
        chime(ogg)
        data = base64.b64encode(ogg.read_bytes()).decode("ascii")
    lines = "\n".join('    "%s"' % chunk for chunk in textwrap.wrap(data, 96))
    Path(path).write_text(
        "# Hidden POV chime - the sparkle's two-note bell as embedded audio\n"
        "#\n"
        "# Purpose: GENERATED by tools/gen_pov_cue_assets.py; do not edit by hand (re-run the tool). A soft\n"
        "#   two-note bell (E6 then B6) synthesised in-house with numpy (see audio/CREDITS.md), stored as an\n"
        "#   embedded OGG and played through AudioData on the UI channel (SFX slider).\n"
        "#\n"
        "# Public API (call these from scenes/screens):\n"
        "#   LC_POV_CUE_AUDIO                          AudioData the Hidden POV cue plays\n"
        "#\n"
        "# Example:\n"
        "#   renpy.music.play(LC_POV_CUE_AUDIO, channel=\"ui\", relative_volume=...)   (systems/hidden_pov.rpy)\n"
        "#\n"
        "# Depends on: nothing\n"
        "# Hooks: none\n"
        "# Load order: init -1: before systems/hidden_pov.rpy reads it\n"
        "# Docs: docs/HIDDEN_POV.md   Tests: tests/test_hidden_pov.py\n"
        "\n"
        "init -1 python:\n"
        "    import base64 as _lc_pov_b64\n"
        "    LC_POV_CUE_AUDIO = AudioData(_lc_pov_b64.b64decode(\n%s\n    ), \"lc_pov_sparkle.ogg\")\n" % lines,
        encoding="utf-8")


if __name__ == "__main__":
    glow_svg(ROOT / "game/gui/pov/glow_idle.svg", (255, 214, 140))
    glow_svg(ROOT / "game/gui/pov/glow_hover.svg", (255, 170, 210), peak=0.75, falloff=2.0)
    bang_svg(ROOT / "game/gui/pov/bang_idle.svg", BANG_RED)
    bang_svg(ROOT / "game/gui/pov/bang_hover.svg", BANG_RED_HOVER, hover=True)
    bang_ring_svg(ROOT / "game/gui/pov/bang_ring.svg")
    chime_rpy(ROOT / "game/systems/hidden_pov_chime.rpy")
