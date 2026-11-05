# Shared audio channels, cue routing, and consent-safe visual effects.
# Audio files are intentionally optional: missing files remain silent.

init python:
    import math

    renpy.music.register_channel("ambience", mixer="ambience", loop=True)
    renpy.music.register_channel("ui", mixer="ui", loop=False)

    def cue(name, kind="sound", loop=False):
        """Play an optional audio cue on its logical channel.

        `name` may be a complete game-relative path or a bare audio stem.
        Missing assets are a deliberate no-op so the foundation can ship first.
        """
        if not name:
            return None
        path = name
        if "." not in path.rsplit("/", 1)[-1]:
            path = "audio/%s.ogg" % path
        if not renpy.loadable(path):
            return None
        channel = kind if kind in ("music", "sound", "ambience", "ui") else "sound"
        if channel == "music":
            renpy.music.play(path, channel="music", loop=loop)
        elif channel == "ambience":
            renpy.music.play(path, channel="ambience", loop=loop)
        else:
            renpy.sound.play(path, channel=channel, loop=loop)
        return path

    def _lc_shake(trans, st, duration, amplitude, cycles):
        if not getattr(persistent, "lc_screen_shake", True):
            trans.xoffset = 0
            trans.yoffset = 0
            return None
        if st >= duration:
            trans.xoffset = 0
            trans.yoffset = 0
            return None
        progress = st / duration
        envelope = (1.0 - progress) ** 2
        wave = math.sin(progress * math.pi * 2.0 * cycles)
        trans.xoffset = int(round(wave * amplitude * envelope))
        trans.yoffset = int(round(math.sin(progress * math.pi * cycles) * amplitude * 0.35 * envelope))
        return 0

    def lc_shake_s_function(trans, st, at):
        return _lc_shake(trans, st, 0.25, 5.0, 2.0)

    def lc_shake_m_function(trans, st, at):
        return _lc_shake(trans, st, 0.40, 13.0, 2.5)

    def lc_flash_function(trans, st, at):
        if not getattr(persistent, "lc_camera_flash", True):
            trans.alpha = 0.0
            return None
        if st >= 0.18:
            trans.alpha = 0.0
            return None
        trans.alpha = max(0.0, 0.82 * (1.0 - st / 0.18))
        return 0

transform lc_shake_s:
    function lc_shake_s_function

transform lc_shake_m:
    function lc_shake_m_function

transform lc_flash:
    function lc_flash_function

transform lc_warm_bloom:
    matrixcolor TintMatrix("#ffd9a8")
    alpha 0.0
    ease 0.12 alpha 1.0
    ease 0.45 alpha 0.82
    ease 0.35 alpha 1.0

transform lc_punch_zoom:
    zoom 1.0
    ease 0.07 zoom 1.075
    ease 0.18 zoom 1.0

transform lc_push_in(duration=6.0, start_zoom=1.0, end_zoom=1.06):
    zoom start_zoom
    linear duration zoom end_zoom

transform lc_dream_sway:
    matrixcolor SaturationMatrix(0.68) * BrightnessMatrix(-0.16)
    rotate 0
    xoffset 0
    yoffset 0
    parallel:
        easein 2.4 rotate 0.8
        easeout 2.4 rotate -0.8
        repeat
    parallel:
        easein 2.4 xoffset 4
        easeout 2.4 xoffset -4
        repeat
    parallel:
        easein 2.4 yoffset -2
        easeout 2.4 yoffset 2
        repeat

image lc_effect_flash_white = Solid("#ffffff")
