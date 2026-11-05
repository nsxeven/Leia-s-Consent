# Shared audio channels, cue routing, and consent-safe visual effects.
# Audio files are intentionally optional: missing files remain silent.

init -10 python:
    import math

    renpy.music.register_channel("ambience", mixer="ambience", loop=True, stop_on_mute=True, tight=True)
    renpy.music.register_channel("ui", mixer="ui", loop=False, stop_on_mute=True)

    def cue(name, kind="sound", loop=False):
        """Play an optional cue on its logical channel, or silently do nothing."""
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

    def lc_shake(size="s"):
        """Shake the visible master camera, respecting the accessibility toggle."""
        if not getattr(persistent, "lc_screen_shake", True):
            return False
        transform = lc_shake_m if size == "m" else lc_shake_s
        renpy.show_layer_at([transform], layer="master", reset=True, camera=True)
        return True

    def lc_punch():
        """Apply a quick camera pop to the visible scene."""
        if not getattr(persistent, "lc_screen_shake", True):
            return False
        renpy.show_layer_at([lc_punch_zoom], layer="master", reset=True, camera=True)
        return True

    def lc_reset_camera():
        renpy.show_layer_at([], layer="master", reset=True, camera=True)

    def _lc_shake(trans, st, duration, amplitude, cycles):
        if not getattr(persistent, "lc_screen_shake", True) or st >= duration:
            trans.xoffset = 0
            trans.yoffset = 0
            return None
        progress = st / duration
        envelope = (1.0 - progress) ** 2
        trans.xoffset = int(round(math.sin(progress * math.pi * 2.0 * cycles) * amplitude * envelope))
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
        trans.alpha = 0.92 * (1.0 - st / 0.18) ** 1.6
        return 0

transform lc_shake_s:
    function lc_shake_s_function

transform lc_shake_m:
    function lc_shake_m_function

transform lc_flash:
    function lc_flash_function

transform lc_warm_bloom:
    alpha 0.0
    easein 0.08 alpha 0.42
    easeout 0.30 alpha 0.0

transform lc_punch_zoom:
    zoom 1.0
    easein 0.07 zoom 1.075
    easeout 0.18 zoom 1.0

transform lc_push_in(duration=6.0, start_zoom=1.0, end_zoom=1.06):
    zoom start_zoom
    linear duration zoom end_zoom

transform lc_dream_sway:
    # Overscan prevents drift/blur from cropping the CG edges.
    zoom 1.05
    matrixcolor SaturationMatrix(0.68) * BrightnessMatrix(-0.16)
    parallel:
        easein 2.4 xoffset 7
        easeout 2.4 xoffset -7
        repeat
    parallel:
        easein 2.4 yoffset -3
        easeout 2.4 yoffset 3
        repeat
    parallel:
        easein 2.4 blur 1.8
        easeout 2.4 blur 0.0
        repeat

image lc_effect_flash_white = Solid("#ffffff")
image lc_effect_flash_blue = Solid("#dff7ff")
image lc_effect_warm_bloom = Solid("#ffd9a8")
image lc_effect_dream_vignette = "gui/title/vignette.png"

transform lc_dream_vignette:
    alpha 0.0
    easein 0.8 alpha 0.22
