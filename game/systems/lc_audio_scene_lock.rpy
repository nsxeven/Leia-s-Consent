# Audio scene lock - one-shot sounds stay with the scene that started them
#
# Purpose: While skipping, one-shot sounds are not played at all (config.skip_sounds); looping beds
#   still start. Every `scene` statement on the master layer cuts one-shot clips started on an
#   earlier line (short fade); same-beat clips and loops are kept. lc_sfx and Leia's voice helpers
#   call lc_audio_mark(channel) when they start a clip.
#
# Public API (call these from scenes/screens):
#   lc_audio_mark(channel) -> None            note that a one-shot clip started on channel now
#   lc_audio_scene_cut() -> None              fade out stale one-shots (the scene wrapper calls it)
#   define config.skip_sounds                 True: no one-shot sounds while skipping
#   LC_SCENE_LOCKED_CHANNELS                  channels whose one-shots belong to their scene
#
# Example:
#   $ lc_sfx("crowd_ooh")   (lc_fx marks the clip; the next `scene` cuts it if still ringing)
#
# Depends on: systems/lc_fx.rpy and systems/lc_breath.rpy (callers)
# Hooks: none (wraps config.scene once at init 999)
# Load order: init -40 (helpers, before lc_fx/lc_breath at -10/-5 use them); init 999 wraps whatever
#   config.scene is installed last
# Docs: docs/ARCHITECTURE.md   Tests: tests/test_audio_scene_lock.py

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
