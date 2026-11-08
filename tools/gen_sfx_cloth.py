"""Synthesise a soft clothing-rustle SFX (CC0, made here) for outfit changes.

Writes game/audio/sfx/cloth_change.ogg: ~1.3 s, three fabric "swishes"
(band-passed noise with slow swells + fine crackle), as when someone pulls a
T-shirt over their head. Mono 44.1 kHz, peak about -9 dBFS.

Run: uv run --with numpy --with soundfile python tools/gen_sfx_cloth.py
"""
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100
OUT = Path(__file__).resolve().parents[1] / "game" / "audio" / "sfx" / "cloth_change.ogg"


def bandpass(x, lo, hi):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    # Smooth band edges (raised-cosine) to avoid ringing.
    w = np.clip((f - lo * 0.7) / (lo * 0.3), 0, 1) * np.clip((hi * 1.3 - f) / (hi * 0.3), 0, 1)
    return np.fft.irfft(spec * w, len(x))


def swish(dur, lo, hi, rng, crackle=0.25):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    noise = bandpass(rng.standard_normal(n), lo, hi)
    env = np.sin(np.pi * t) ** 1.6 * (1 + 0.35 * np.sin(2 * np.pi * rng.uniform(2, 4) * t))
    # Fabric crackle: sparse short clicks, also band-limited.
    clicks = np.zeros(n)
    idx = rng.choice(n, size=int(n * 0.0025), replace=False)
    clicks[idx] = rng.uniform(-1, 1, len(idx))
    clicks = bandpass(clicks, 2500, 9000) * 6
    s = (noise + crackle * clicks) * env
    return s / (np.abs(s).max() + 1e-9)


def main():
    rng = np.random.default_rng(1109)
    total = np.zeros(int(1.35 * SR))
    for start, dur, lo, hi, gain in ((0.00, 0.45, 700, 5500, 0.9),
                                     (0.33, 0.55, 500, 4200, 1.0),
                                     (0.80, 0.50, 900, 6500, 0.7)):
        s = swish(dur, lo, hi, rng) * gain
        a = int(start * SR)
        total[a:a + len(s)] += s[: len(total) - a]
    fade = int(0.08 * SR)
    total[-fade:] *= np.linspace(1, 0, fade)
    total = total / np.abs(total).max() * 10 ** (-9 / 20)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(OUT), total.astype(np.float32), SR, format="OGG", subtype="VORBIS")
    print("wrote", OUT, round(len(total) / SR, 2), "s")


if __name__ == "__main__":
    main()
