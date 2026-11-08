## Audio stays with its scene (darryn 2026-11-08).
##
## 1. Skipping: one-shot sounds (gasps, moans, SFX, lewd foley) are not played at
##    all while Ren'Py is skipping, so nothing from a skipped CG or conversation
##    sounds over what comes after. Looping beds (ambience, breath loops) still
##    start, so the scene you land on sounds right.
## 2. Scene changes: every `scene` statement (new background or CG) cuts one-shot
##    clips that were started on an EARLIER line and are still ringing, with a
##    short fade. Clips started in the same beat as the scene change (a door
##    slam right before `scene ... with dissolve`) keep playing, and loops
##    (ambience, Leia's breath loop, lewd loops) are never cut here: scenes that
##    keep breathing across CG changes stay continuous.
##
## lc_sfx and Leia's voice helpers call lc_audio_mark(channel) when they start a
## clip; lc_audio_scene_cut() runs from config.scene.

define config.skip_sounds = True

init -40 python:
    import time as _lc_at

    # Channels whose one-shot clips belong to the scene they were started in.
    LC_SCENE_LOCKED_CHANNELS = ("audio", "lc_voice", "lc_lewd", "lc_breath")
    LC_SCENE_CUT_GRACE = 0.05     # s: same-beat clips (no click in between) survive
    LC_SCENE_CUT_FADE = 0.15

    # Plain dict (not rollback-tracked, never saved): channel -> wall-clock start.
    _lc_audio_started = python_dict()

    def lc_audio_mark(channel):
        _lc_audio_started[channel] = _lc_at.time()

    def lc_audio_scene_cut():
        now = _lc_at.time()
        for ch in LC_SCENE_LOCKED_CHANNELS:
            started = _lc_audio_started.get(ch)
            if started is None or now - started < LC_SCENE_CUT_GRACE:
                continue
            # Leia's breath channel carries a running loop: leave it alone.
            if ch == "lc_breath" and getattr(store, "lc_breath_loop", None):
                continue
            try:
                if renpy.music.get_playing(channel=ch):
                    renpy.music.stop(channel=ch, fadeout=LC_SCENE_CUT_FADE)
            except Exception:
                pass
            _lc_audio_started.pop(ch, None)

init 999 python:
    # Wrap whatever scene function is installed (Ren'Py's own by default).
    if not getattr(config.scene, "_lc_audio_lock", False):
        _lc_scene_inner = config.scene

        def _lc_scene_with_audio_lock(layer=None):
            if layer in (None, "master"):
                lc_audio_scene_cut()
            return _lc_scene_inner(layer)

        _lc_scene_with_audio_lock._lc_audio_lock = True
        config.scene = _lc_scene_with_audio_lock
