# Effects + audio foundation (darryn 2026-11-06; plan: Kanban t_d30bd492).
#
# Story scripts call these helpers instead of raw `play`/`hpunch`, so every
# effect respects the player's settings and a missing audio file is silent.
#
#   Visual
#     "line" with lc_shake("s")        small shake (impacts, comedic shouts)
#     "line" with lc_shake("m")        medium shake (falls, collisions, waking)
#     "line" with lc_punch()           quick zoom pop on the whole scene
#     $ lc_flash()                     one soft white blink (photo); colour/strength optional
#     $ lc_photo()                     camera shutter sound + flash
#     scene cg x at lc_push_in         slow push-in on a CG (about 9 s)
#     scene cg x at lc_dream_sway      nightmare warp (slow drift + blur pulse)
#
#   Audio (files are optional: missing = silent)
#     $ lc_sfx("splash_big")           game/audio/sfx/<name>.ogg on the "audio" channel (overlaps)
#     $ lc_amb("party_chatter")        game/audio/amb/<name>.ogg, looping, crossfades
#     $ lc_amb_stop()
#     $ lc_music("dinner_lounge")      game/audio/music/<name>.ogg, looping
#     $ lc_music_stop()
#     $ lc_duck() / lc_unduck()        dip / restore the music and ambience
#     lc_ui_sound("tap")               game/audio/ui/<name>.ogg on the "ui" channel
#
# Settings: Preferences gets SCREEN SHAKE and CAMERA FLASH toggles and
# AMBIENCE / UI SOUNDS sliders (mixers "ambience" and "ui").

default persistent.lc_screen_shake = True
default persistent.lc_camera_flash = True

init -10 python:
    renpy.music.register_channel("ambience", mixer="ambience", loop=True, stop_on_mute=True, tight=True)
    renpy.music.register_channel("ui", mixer="ui", loop=False, stop_on_mute=True)
    # Looping story sound under a beat (e.g. sunscreen being rubbed in); Sound slider.
    renpy.music.register_channel("sfx_loop", mixer="sfx", loop=True, stop_on_mute=True)

init -2 python:
    import time as _lc_fx_time

    LC_AUDIO_EXTS = (".ogg", ".opus", ".wav", ".mp3")

    # ONE place to tune levels after playtesting: "kind/name": multiplier
    # (1.0 = as mastered, 0.5 = about -6 dB, 0.0 = muted). Credits and
    # sources for every file: game/audio/CREDITS.md.
    LC_AUDIO_GAIN = {
        "amb/room_tone": 0.6,   # quiet indoor A/C hum under every villa/bedroom scene
        "amb/restaurant": 0.75, # darryn: restaurant recording slightly lower than the other ambience
        # "sfx/splash_big": 0.8,
        # "amb/party": 1.0,
        # "music/lounge_piano": 0.7,
        # "ui/tick": 0.6,
    }

    def lc_audio_gain(kind, name, volume=1.0):
        return max(0.0, float(volume) * LC_AUDIO_GAIN.get("%s/%s" % (kind, name), 1.0))

    def lc_audio_path(kind, name):
        """game/audio/<kind>/<name>.<ext> if it exists, else None."""
        if not name:
            return None
        if "/" in name or "." in name:
            return name if renpy.loadable(name) else None
        for ext in LC_AUDIO_EXTS:
            path = "audio/%s/%s%s" % (kind, name, ext)
            if renpy.loadable(path):
                return path
        return None

    # ---------------------------------------------------------------- shakes

    _LC_SHAKES = {
        # (x px, y px, period s, total s)
        "s": (5, 3, 0.055, 0.24),
        "m": (11, 7, 0.065, 0.40),
    }

    def lc_shake(size="s"):
        """A screen-shake transition, or None when the player turned shakes off."""
        if not persistent.lc_screen_shake:
            return None
        x, y, period, total = _LC_SHAKES.get(size, _LC_SHAKES["s"])
        return Move((x, y), (-x, -y), period, bounce=True, repeat=True, delay=total)

    def lc_punch():
        """Quick zoom-pop transition for a say line: `"line" with lc_punch()`.

        Respects the SCREEN SHAKE setting (returns None when it's off).
        """
        if not persistent.lc_screen_shake:
            return None
        return lc_punch_trans

    # --------------------------------------------------------------- flashes

    def lc_flash(colour="#ffffff", strength=0.55, duration=0.42):
        """One soft blink over the scene; skipped when camera flashes are off."""
        if not persistent.lc_camera_flash:
            return
        renpy.show_screen("lc_flash_overlay", colour=colour, strength=strength, duration=duration)

    def lc_photo(flash=True):
        """In-story photo: shutter sound plus a soft white blink."""
        lc_sfx("camera_shutter", 0.8)
        if flash:
            lc_flash()

    # ----------------------------------------------------------------- audio

    def lc_sfx(name, volume=1.0):
        path = lc_audio_path("sfx", name)
        if path:
            renpy.music.play(path, channel="audio", relative_volume=lc_audio_gain("sfx", name, volume))
        return path

    def lc_amb(name, volume=1.0, fadein=1.5, fadeout=1.5):
        path = lc_audio_path("amb", name)
        if path:
            renpy.music.play(path, channel="ambience", loop=True, fadein=fadein, fadeout=fadeout,
                             if_changed=True, relative_volume=lc_audio_gain("amb", name, volume))
        else:
            renpy.music.stop(channel="ambience", fadeout=fadeout)
        return path

    def lc_amb_stop(fadeout=1.5):
        renpy.music.stop(channel="ambience", fadeout=fadeout)

    def lc_sfx_loop(name, volume=1.0, fadein=0.3):
        """Loop audio/sfx/<name> until lc_sfx_loop_stop(); a missing file is silent."""
        path = lc_audio_path("sfx", name)
        if path:
            renpy.music.play(path, channel="sfx_loop", loop=True, fadein=fadein,
                             relative_volume=lc_audio_gain("sfx", name, volume))
        return path

    def lc_sfx_loop_stop(fadeout=0.8):
        renpy.music.stop(channel="sfx_loop", fadeout=fadeout)

    def lc_music(name, volume=1.0, fadein=2.0, fadeout=2.0):
        path = lc_audio_path("music", name)
        if path:
            renpy.music.play(path, channel="music", loop=True, fadein=fadein, fadeout=fadeout,
                             if_changed=True, relative_volume=lc_audio_gain("music", name, volume))
        return path

    def lc_music_stop(fadeout=2.0):
        renpy.music.stop(channel="music", fadeout=fadeout)

    def lc_duck(level=0.3, delay=0.6):
        """Dip music + ambience for a tense or quiet beat."""
        renpy.music.set_volume(level, delay=delay, channel="music")
        renpy.music.set_volume(min(1.0, level + 0.2), delay=delay, channel="ambience")

    def lc_unduck(delay=1.2):
        renpy.music.set_volume(1.0, delay=delay, channel="music")
        renpy.music.set_volume(1.0, delay=delay, channel="ambience")

    def lc_audio_quiet(fadeout=1.0):
        """Stop music and ambience (scene ends, hard cuts)."""
        lc_music_stop(fadeout)
        lc_amb_stop(fadeout)

    # -------------------------------------------------------------- UI sound

    LC_UI_HOVER_COOLDOWN = 0.06
    _lc_ui_last = {"t": 0.0}

    def lc_ui_sound(name, volume=1.0, hover=False):
        """Short UI sound on its own channel/mixer. Hovers are rate-limited."""
        if hover:
            now = _lc_fx_time.time()
            if now - _lc_ui_last["t"] < LC_UI_HOVER_COOLDOWN:
                return None
            _lc_ui_last["t"] = now
        path = lc_audio_path("ui", name)
        if path:
            renpy.music.play(path, channel="ui", relative_volume=lc_audio_gain("ui", name, volume))
        return path


transform lc_punch_trans(old_widget=None, new_widget=None):
    delay 0.36
    contains:
        new_widget
        subpixel True
        xanchor 0.5 yanchor 0.5 xpos 0.5 ypos 0.5
        zoom 1.0
        easein 0.07 zoom 1.03
        easeout 0.28 zoom 1.0

transform lc_push_in(z=1.05, t=9.0):
    subpixel True
    xanchor 0.5 yanchor 0.5 xpos 0.5 ypos 0.5
    zoom 1.0
    easeout t zoom z

transform lc_dream_sway:
    subpixel True
    xanchor 0.5 yanchor 0.5 xpos 0.5 ypos 0.5
    zoom 1.04
    parallel:
        ease 3.2 xoffset 9 yoffset -4
        ease 3.2 xoffset -9 yoffset 4
        repeat
    parallel:
        ease 2.6 blur 2.5
        ease 2.6 blur 0.0
        repeat

transform lc_flash_tf(strength, duration):
    alpha 0.0
    linear 0.05 alpha strength
    easeout duration alpha 0.0

screen lc_flash_overlay(colour="#ffffff", strength=0.55, duration=0.42):
    zorder 60
    add Solid(colour) at lc_flash_tf(strength, duration)
    timer (duration + 0.1) action Hide("lc_flash_overlay")
