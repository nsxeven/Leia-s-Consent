## Leia's breaths and moans for intimate / lewd beats.
##
##   $ lc_breath_start(1)                 # soft: mostly breaths, rare small moan
##   $ lc_breath_start(1, moans=False)    # holding it in: breaths only
##   $ lc_breath_start(3)                 # louder, quicker, more moans
##   $ lc_breath_stop()                   # fade out (call when the beat ends)
##
## Each start builds a fresh random string of inhales, moans and pauses from
## game/audio/voice/leia/<inhale|moan>-iNN-MM.ogg (any number of files; new
## ones are picked up automatically) and loops it on its own channel under
## the Voice volume slider. Higher intensity = louder files, more moans,
## shorter pauses. Never more than two moans without a breath in between, and
## the same clip is never played twice in a row.
## Sounds: MoanBox by Selenyhr (Unlicense / public domain).

# The loop that is running (its settings), so single moans can resume it; saved with the game.
default lc_breath_loop = None

init -5 python:
    renpy.music.register_channel("lc_breath", mixer="voice", loop=True, stop_on_mute=True, tight=False)

init python:
    import re as _lc_re

    LC_BREATH_DIR = "audio/voice/leia/"
    LC_BREATH_GAIN = 1.0      # one knob for the whole system
    # Pacing (darryn 2026-11-08: moans/inhales came too often). Every pause in a
    # loop, including per-scene pause=(lo, hi) overrides, is stretched by
    # LC_BREATH_PACE, and every moan chance is scaled by LC_BREATH_MOAN_SCALE.
    LC_BREATH_PACE = 1.7
    LC_BREATH_MOAN_SCALE = 0.75
    _lc_breath_files = None

    def _lc_breath_index():
        """{'inhale': {1: [...], 2: [...]}, 'moan': {...}} from the folder."""
        global _lc_breath_files
        if _lc_breath_files is None:
            pat = _lc_re.compile(r"^" + _lc_re.escape(LC_BREATH_DIR) + r"(inhale|exhale|moan)-i(\d+)-(\d+)\.(ogg|opus|mp3|wav)$")
            idx = {"inhale": {}, "exhale": {}, "moan": {}}
            for f in renpy.list_files():
                m = pat.match(f)
                if m:
                    idx[m.group(1)].setdefault(int(m.group(2)), []).append(f)
            _lc_breath_files = idx
        return _lc_breath_files

    def _lc_breath_pick(kind, intensity, last):
        levels = _lc_breath_index().get(kind) or {}
        if not levels:
            return None
        avail = sorted(levels)
        # Mostly the requested level, sometimes one either side.
        roll = renpy.random.random()
        want = intensity + (-1 if roll < 0.2 else (1 if roll > 0.85 else 0))
        level = min(avail, key=lambda a: (abs(a - want), a))
        pool = [f for f in levels[level] if f != last] or levels[level]
        return renpy.random.choice(pool)

    def lc_breath_sequence(intensity=1, moans=True, length=28, moan_chance=None, pause=None):
        intensity = max(1, int(intensity))
        if moan_chance is None:
            moan_chance = 0.0 if not moans else min(0.65, 0.12 + 0.17 * (intensity - 1))
            if intensity == 1 and moans:
                moan_chance = 0.12
        elif not moans:
            moan_chance = 0.0
        moan_chance *= LC_BREATH_MOAN_SCALE
        pause_lo, pause_hi = pause or {1: (1.2, 2.6), 2: (0.7, 1.8), 3: (0.35, 1.1)}.get(intensity, (0.2, 0.7))
        pause_lo, pause_hi = pause_lo * LC_BREATH_PACE, pause_hi * LC_BREATH_PACE
        out, last, moans_in_row = [], None, 0
        for _ in range(length):
            if moans_in_row < 2 and renpy.random.random() < moan_chance:
                kind = "moan"
                moans_in_row += 1
            else:
                kind = "inhale"
                moans_in_row = 0
            f = _lc_breath_pick(kind, intensity, last)
            if f:
                out.append(f)
                last = f
            out.append("<silence %.2f>" % renpy.random.uniform(pause_lo, pause_hi))
        return out

    def _lc_breath_loop_seq():
        """A fresh random string for the loop that is running (None if no loop)."""
        p = store.lc_breath_loop
        if not p:
            return None
        seq = lc_breath_sequence(p["intensity"], p["moans"], moan_chance=p["moan_chance"], pause=p["pause"])
        return seq if any(not s.startswith("<") for s in seq) else None

    def lc_breath_start(intensity=1, moans=True, fadein=0.6, volume=1.0, moan_chance=None, pause=None):
        """moan_chance / pause=(lo, hi) override the intensity defaults (e.g. a dense, moan-heavy beat).

        Only one of Leia's sounds plays at a time: if a single moan/inhale is still
        sounding on the channel, the loop is queued to start right after it.
        """
        seq = lc_breath_sequence(intensity, moans, moan_chance=moan_chance, pause=pause)
        if not any(not s.startswith("<") for s in seq):
            return None
        single_still_playing = store.lc_breath_loop is None and renpy.music.get_playing(channel="lc_breath")
        store.lc_breath_loop = {"intensity": intensity, "moans": moans, "moan_chance": moan_chance,
                                "pause": tuple(pause) if pause else None, "volume": volume}
        if single_still_playing:
            renpy.music.queue(seq, channel="lc_breath", loop=True, clear_queue=True,
                              relative_volume=LC_BREATH_GAIN * volume)
        else:
            renpy.music.play(seq, channel="lc_breath", loop=True, fadein=fadein,
                             relative_volume=LC_BREATH_GAIN * volume)
        return seq

    def lc_breath_once(intensity=1, volume=1.0):
        """One random soft inhale (a single breath on a Leia CG); never loops (ends a running loop)."""
        f = _lc_breath_pick("inhale", max(1, int(intensity)), None)
        if f:
            store.lc_breath_loop = None
            renpy.music.play(f, channel="lc_breath", loop=False, relative_volume=LC_BREATH_GAIN * volume)
        return f

    def _lc_breath_single(kind, intensity, volume):
        """Play one clip on Leia's channel without ever stacking two voices.

        Inside a running loop the current clip fades out, this one plays, and the
        loop carries on afterwards with a fresh random string (darryn: the dream
        moans used to overlap and sound like two people).
        """
        f = _lc_breath_pick(kind, max(1, int(intensity)), None)
        if not f:
            return None
        loop = _lc_breath_loop_seq()
        renpy.music.play(f, channel="lc_breath", loop=False, fadeout=0.15,
                         relative_volume=LC_BREATH_GAIN * volume)
        if loop:
            renpy.music.queue(loop, channel="lc_breath", loop=True, clear_queue=False,
                              relative_volume=LC_BREATH_GAIN * store.lc_breath_loop.get("volume", 1.0))
        return f

    def lc_leia_voice_clip(path, volume=1.0):
        """Leia's one-shot vocal clips (gasp, giggle, sigh... from lc_sfx) share her
        breath channel, so a new cue always cuts the one still sounding (darryn
        2026-11-08: clicking on fast stacked two Leias). A running breath loop
        carries on right after the clip."""
        loop = _lc_breath_loop_seq()
        renpy.music.play(path, channel="lc_breath", loop=False, fadeout=0.12, relative_volume=volume)
        if loop:
            renpy.music.queue(loop, channel="lc_breath", loop=True, clear_queue=False,
                              relative_volume=LC_BREATH_GAIN * store.lc_breath_loop.get("volume", 1.0))
        return path

    def lc_moan_once(intensity=2, volume=1.0):
        """One random moan; inside a running loop it replaces the loop's next sound instead of layering."""
        return _lc_breath_single("moan", intensity, volume)

    def lc_inhale_over(intensity=1, volume=1.0):
        """One random inhale; inside a running loop it replaces the loop's next sound instead of layering."""
        return _lc_breath_single("inhale", intensity, volume)

    def lc_breath_stop(fadeout=1.2):
        store.lc_breath_loop = None
        renpy.music.stop(channel="lc_voice", fadeout=min(fadeout, 0.3))
        renpy.music.stop(channel="lc_breath", fadeout=fadeout)
