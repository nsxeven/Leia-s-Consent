# Hidden POV - optional, scene-scoped alternate views behind a sparkle
#
# Purpose: A registered moment shows a non-modal sparkle while its source CG is on screen between
#   lc_pov_begin/lc_pov_end; clicking opens the alternate view and only that click marks it seen for
#   the Gallery. Never shown on the master layer, never a story choice. Registrations are validated
#   at init 999 (developer builds fail loudly).
#
# Public API (call these from scenes/screens):
#   lc_pov_register(moment_id, image, source, position=None, title="Optional view", mature=None, center=None, gallery_id=None, sfx=True, day_id=None, label=None, mood=None) -> None
#       register one moment (stable image/source/position) at init; day_id also registers it
#       as a `pov` discovery on that day's Moments strip (label defaults to title)
#   lc_pov_begin(moment_id) -> None           open the moment's scope (its sparkle may show)
#   lc_pov_end() -> None                      close the current scope
#   lc_pov_in_scope(moment_id)                True while the moment's source image is showing
#   lc_pov_available()                        True when a cue may show now
#   lc_pov_open(moment_id) -> None            open the viewer (the sparkle's action); also marks the
#       moment found in this save (lc_discovery_mark, read back with lc_pov_seen_in_save)
#   lc_pov_close() -> None                    close the viewer (the viewer's ease back calls it)
#   lc_pov_instant()                          True when the viewer opens/closes without animation
#   lc_pov_focus(moment_id)                   (xalign, yalign) of the push toward the sparkle
#   LC_POV_IN, LC_POV_OUT, LC_POV_PUSH_ZOOM   viewer transition seconds and push-in zoom
#   lc_pov_validate(moment_id)                problems with one registration
#   lc_pov_validate_all()                     {moment_id: problems} for every registration
#   LC_POV_OPPORTUNITIES                      the registry {moment_id: entry}
#   screen lc_pov_viewer(moment_id)           the full-screen alternate view: the source CG
#       pushes in toward the sparkle and the POV CG fades up over it; closing reverses it. Every
#       registered moment gets this transition; nothing to add per moment.
#   transform lc_pov_push_in(xa, ya, z, t) / lc_pov_push_out(xa, ya, z, t)   source CG legs
#   transform lc_pov_reveal(t) / lc_pov_unreveal(t)                          POV CG legs
#   transform lc_pov_fade(a0, a1, delay, t)                                  backdrop / labels
#   screen lc_pov_hotspot()                   overlay with the sparkle cue (desktop and touch
#       variants)
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_pov_warn,
#   lc_pov_hitbox_size, lc_pov_hit_rect, lc_pov_reduce_motion, lc_pov_announce_cue,
#   lc_pov_hover_sound, lc_pov_afm_grace, lc_pov_afm_callback, lc_pov_scope_cleanup,
#   _lc_pov_gallery_rows_for, _lc_pov_rects_overlap, lc_pov_static, lc_pov_cue_art
#
# Example:
#   init 1 python:
#       lc_pov_register("d2_breakfast_julian", image="cg ch01_d2_breakfast_julian_pov",
#                       source="cg ch01_d2_breakfast_02", center=(1785, 255), title="Julian's POV", mature=True)
#   $ lc_pov_begin("d2_breakfast_julian")   ...   $ lc_pov_end()
#
# Depends on: systems/hidden_pov_chime.rpy (LC_POV_CUE_AUDIO), systems/gallery.rpy,
#   systems/lc_fx.rpy, screens/scrapbook_ui.rpy (lc_phone_covers_scene, lc_journal_menu_open),
#   systems/discovery.rpy (lc_discovery_register, lc_discovery_mark)
# Hooks: none (installs config.afm_callback, a start_interact callback and the lc_pov_hotspot
#   overlay)
# Load order: init -1 constants; init 0 registry and API (moments register at init 1); init 999
#   validation, after every registration file and the gallery tables
# Docs: docs/HIDDEN_POV.md   Tests: tests/test_hidden_pov.py, tests/test_d2_breakfast_cgs.py,
#   tests/test_discovery.py

default lc_pov_active = None
default lc_pov_viewed = False
# The cue chime plays once per encounter (reset by lc_pov_begin).
default lc_pov_cue_announced = False

init -1 python:
    # Hit targets (px, square, centred on the sparkle). The art stays the same
    # size; only the invisible click/tap area grows. Touch builds get more room.
    LC_POV_HITBOX = 120
    LC_POV_HITBOX_TOUCH = 160
    # Legacy registrations give `position` as the upper-left of a 64x64 slot;
    # the sparkle centre is that corner + 32 px.
    LC_POV_LEGACY_SLOT = 64
    # Screen areas a cue must never overlap (x, y, w, h at 1920x1080): the
    # dialogue box and everything under it (phone HUD at 1785,858; quick menu at
    # y 1020-1040) and the phone notification banner at the top centre.
    LC_POV_RESERVED_RECTS = (
        ("dialogue box / phone HUD / quick menu", (0, 792, 1920, 288)),
        ("phone notification banner", (610, 0, 700, 116)),
    )
    # Soft chime when a cue appears: LC_POV_CUE_AUDIO (systems/hidden_pov_chime.rpy).
    LC_POV_CUE_VOLUME = 0.7
    # Viewer transition (darryn 2026-11-18: no instant snap, match the push-in of Things Ryan
    # noticed). Open: the source CG pushes in toward the sparkle while the POV fades up over it.
    # Close: the POV fades out while the source eases back to the full frame.
    LC_POV_IN = 0.8
    LC_POV_OUT = 0.6
    LC_POV_PUSH_ZOOM = 1.3

init python:
    import time as _lc_pov_time
    # Registry is init-time data; each new moment needs only a row and begin/end.
    LC_POV_OPPORTUNITIES = {}

    def _lc_pov_warn(message, fatal=False):
        """Developer builds fail loudly; release builds only log."""
        text = "[hidden_pov] " + message
        if fatal and config.developer:
            raise Exception(text)
        print(text)
        try:
            renpy.log(text)
        except Exception:
            pass
        if config.developer and not renpy.is_init_phase():
            renpy.notify(text)
        return None

    def lc_pov_register(moment_id, image, source, position=None, title="Optional view",
                        mature=None, center=None, gallery_id=None, sfx=True,
                        day_id=None, label=None, mood=None):
        """Register one optional POV moment.

        position: legacy (x, y) upper-left of a 64x64 slot (sparkle centre = +32).
        center:   (x, y) sparkle centre; preferred for new moments.
        mature:   None derives it from the Gallery row that lists `image`.
        sfx:      play the soft sparkle chime when the cue first appears.
        day_id:   review day (e.g. "ch01_d2"); when given the moment is also a `pov`
                  discovery on that day's Moments strip (systems/discovery.rpy), shown with
                  `label` (default: title) and `mood` (default: "").
        """
        if moment_id in LC_POV_OPPORTUNITIES:
            raise ValueError("Duplicate optional POV: " + moment_id)
        if (position is None) == (center is None):
            raise ValueError("POV %s needs exactly one of position=(x, y) or center=(x, y)" % moment_id)
        pair = center if center is not None else position
        if not (isinstance(pair, tuple) and len(pair) == 2):
            raise ValueError("POV position/center must be an (x, y) pixel pair")
        if center is None:
            half = LC_POV_LEGACY_SLOT // 2
            center = (position[0] + half, position[1] + half)
        LC_POV_OPPORTUNITIES[moment_id] = {
            "image": image, "source": source, "center": tuple(center),
            "position": position, "title": title,
            "mature": None if mature is None else bool(mature),
            "gallery_id": gallery_id, "sfx": bool(sfx),
        }
        if day_id is not None:
            lc_discovery_register(day_id, moment_id, "pov", label or title, mood or "", image=image)

    def lc_pov_hitbox_size():
        return LC_POV_HITBOX_TOUCH if renpy.variant("touch") else LC_POV_HITBOX

    def lc_pov_hit_rect(entry, size=None):
        size = size or lc_pov_hitbox_size()
        cx, cy = entry["center"]
        return (int(cx - size // 2), int(cy - size // 2), size, size)

    def lc_pov_reduce_motion():
        """Static cue when the player turned off screen shake or transitions."""
        return (not getattr(persistent, "lc_screen_shake", True)
                or not _preferences.transitions)

    def lc_pov_begin(moment_id):
        if moment_id not in LC_POV_OPPORTUNITIES:
            raise ValueError("Unknown optional POV: " + moment_id)
        previous = renpy.store.lc_pov_active
        if previous is not None:
            _lc_pov_warn("lc_pov_begin(%r) while %r is still active; ending %r first. "
                         "Add $ lc_pov_end() before the next begin." % (moment_id, previous, previous))
            lc_pov_end()
        renpy.store.lc_pov_active = moment_id
        renpy.store.lc_pov_viewed = False
        renpy.store.lc_pov_cue_announced = False
        return None

    def lc_pov_end():
        renpy.store.lc_pov_active = None
        renpy.store.lc_pov_viewed = False
        renpy.store.lc_pov_cue_announced = False
        renpy.hide_screen("lc_pov_viewer")
        return None

    def lc_pov_in_scope(moment_id):
        entry = LC_POV_OPPORTUNITIES.get(moment_id)
        return bool(entry and renpy.showing(entry["source"], layer="master"))

    def lc_pov_available():
        moment_id = renpy.store.lc_pov_active
        return bool(
            moment_id and not renpy.store.lc_pov_viewed
            and lc_pov_in_scope(moment_id)
            and renpy.get_screen("say")
            and not renpy.get_screen("lc_pov_viewer")
            and not renpy.get_screen("main_menu")
            and not renpy.get_screen("game_menu")
            and not lc_phone_covers_scene()
            and renpy.store.quick_menu
            and not renpy.store._windows_hidden
            and not lc_journal_menu_open()
        )

    def lc_pov_announce_cue(moment_id):
        """Soft chime the first time a cue appears in an encounter (no story effect)."""
        if renpy.store.lc_pov_cue_announced or renpy.store.lc_pov_active != moment_id:
            return None
        renpy.store.lc_pov_cue_announced = True
        entry = LC_POV_OPPORTUNITIES.get(moment_id)
        if entry and entry["sfx"] and not renpy.is_skipping():
            renpy.music.play(LC_POV_CUE_AUDIO, channel="ui",
                             relative_volume=lc_audio_gain("ui", "sparkle", LC_POV_CUE_VOLUME))
        return None

    def lc_pov_open(moment_id):
        # Called only by the hotspot's click action, never by screen evaluation,
        # hover, image prediction or the viewer's own render.
        if renpy.store.lc_pov_active != moment_id or not lc_pov_available():
            return None
        image = LC_POV_OPPORTUNITIES[moment_id]["image"]
        renpy.stop_skipping()  # SDK exports/contextexports.py; do not resume Skip.
        renpy.store.lc_pov_viewed = True
        # Save-local "seen" record (systems/discovery.rpy): rollback restores it with the
        # store; retain_after_load keeps it in a save made on this same line.
        lc_discovery_mark(moment_id)
        renpy.retain_after_load()
        renpy.mark_image_seen(image)  # SDK exports/persistentexports.py.
        renpy.save_persistent()
        renpy.show_screen("lc_pov_viewer", moment_id=moment_id)
        return None

    def lc_pov_hover_sound():
        # Must return None: a `hovered` action that returns a value ends the
        # interaction, and lc_ui_sound returns the sound path, so hovering the
        # cue used to advance the dialogue line.
        lc_ui_sound("tick", hover=True)
        return None

    # Auto-forward grace after the viewer closes. The say line's Auto timer keeps
    # running while the viewer is up (only lc_pov_afm_callback holds it), so
    # without this the line advanced the instant the player closed the view.
    # Closing restarts the line's Auto countdown instead. Plain list, not
    # rollback-tracked store state.
    _lc_pov_afm_hold = python_list([0.0])

    def lc_pov_afm_grace():
        """Seconds of Auto-forward the current line would normally get."""
        try:
            what = renpy.filter_text_tags(getattr(renpy.store, "_last_say_what", "") or "", allow=[])
            return (1.0 * (config.afm_bonus + max(len(what), 1)) / config.afm_characters) * _preferences.afm_time
        except Exception:
            return 2.0

    def lc_pov_instant():
        """No viewer transition with reduced motion (or while skipping, which opening stops)."""
        return bool(renpy.is_skipping() or lc_pov_reduce_motion())

    def lc_pov_focus(moment_id):
        """(xalign, yalign) that keeps the sparkle point fixed while the source CG zooms."""
        cx, cy = LC_POV_OPPORTUNITIES[moment_id]["center"]
        w, h = float(config.screen_width), float(config.screen_height)
        return (min(max(cx / w, 0.0), 1.0), min(max(cy / h, 0.0), 1.0))

    def lc_pov_close():
        renpy.hide_screen("lc_pov_viewer")
        _lc_pov_afm_hold[0] = _lc_pov_time.time() + lc_pov_afm_grace()
        return None

    # The say behavior's auto-forward timer consults config.afm_callback before
    # advancing (SDK display/behavior.py). Chain the original callback; do not
    # mutate the player's persistent Auto preference, so closing restores it.
    _lc_pov_prior_afm_callback = config.afm_callback
    def lc_pov_afm_callback():
        if renpy.get_screen("lc_pov_viewer"):
            return False
        if _lc_pov_time.time() < _lc_pov_afm_hold[0]:
            return False
        if _lc_pov_prior_afm_callback is not None:
            return _lc_pov_prior_afm_callback()
        return True
    config.afm_callback = lc_pov_afm_callback

    def lc_pov_scope_cleanup():
        moment_id = renpy.store.lc_pov_active
        if moment_id and not lc_pov_in_scope(moment_id):
            lc_pov_end()
        return None

    config.start_interact_callbacks.append(lc_pov_scope_cleanup)
    if "lc_pov_hotspot" not in config.overlay_screens:
        config.overlay_screens.append("lc_pov_hotspot")

    # ------------------------------------------------------- registration checks
    def _lc_pov_gallery_rows_for(image):
        name = image[3:] if image.startswith("cg ") else image
        rows = []
        for gid, entry in GALLERY_ENTRIES.items():
            if any(page["image"] == name for page in entry["pages"]):
                rows.append(gid)
        return sorted(rows)

    def _lc_pov_rects_overlap(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

    def lc_pov_validate(moment_id):
        """Problems with one registration (empty list when it is sound).

        Also resolves `mature` and `gallery_id` from the Gallery row when omitted."""
        entry = LC_POV_OPPORTUNITIES[moment_id]
        problems = []
        for key in ("image", "source"):
            if not renpy.has_image(entry[key], exact=True):
                problems.append("%s=%r is not a defined image" % (key, entry[key]))
        # Check the largest (touch) hit area so every build variant fits.
        rect = lc_pov_hit_rect(entry, LC_POV_HITBOX_TOUCH)
        x, y, w, h = rect
        if x < 0 or y < 0 or x + w > config.screen_width or y + h > config.screen_height:
            problems.append("cue hit area %r leaves the %dx%d screen" % (rect, config.screen_width, config.screen_height))
        for label, reserved in LC_POV_RESERVED_RECTS:
            if _lc_pov_rects_overlap(rect, reserved):
                problems.append("cue hit area %r overlaps the %s %r" % (rect, label, reserved))
        rows = _lc_pov_gallery_rows_for(entry["image"])
        if entry["gallery_id"] is None and len(rows) == 1:
            entry["gallery_id"] = rows[0]
        gid = entry["gallery_id"]
        if gid is not None and gid not in GALLERY_ENTRIES:
            problems.append("gallery_id %r is not a Gallery row" % gid)
            gid = None
        if gid is None:
            if len(rows) > 1:
                problems.append("image is in several Gallery rows %r; pass gallery_id=" % (rows,))
            if entry["mature"] is None:
                entry["mature"] = False
        else:
            row_mature = GALLERY_ENTRIES[gid]["mature"]
            if entry["mature"] is None:
                entry["mature"] = row_mature
            elif entry["mature"] != row_mature:
                problems.append("mature=%r disagrees with Gallery row %r (mature=%r)" % (entry["mature"], gid, row_mature))
        return problems

    def lc_pov_validate_all():
        report = {}
        for moment_id in sorted(LC_POV_OPPORTUNITIES):
            problems = lc_pov_validate(moment_id)
            if problems:
                report[moment_id] = problems
        return report

# Runs after every registration file (init 1+) and the Gallery tables.
init 999 python:
    _lc_pov_report = lc_pov_validate_all()
    if _lc_pov_report:
        _lc_pov_warn("Hidden POV registration problems:\n" + "\n".join(
            "  %s: %s" % (mid, problem)
            for mid in sorted(_lc_pov_report) for problem in _lc_pov_report[mid]), fatal=True)


# ------------------------------------------------------------------ cue art
# Idle: a gentle twinkle with a warm glow. Hover/focus: the pink hover sparkle,
# a brighter glow and a small scale pulse. The art is centred in the hit area,
# so scaling never moves the button or reflows dialogue.
# Immersive idle is kept clearly visible on bright CGs (playtest: the old
# 0.72-alpha, 0.85-zoom sparkle was easy to miss): a larger star whose alpha
# never drops below 0.88 and a fuller glow.
transform lc_pov_twinkle:
    subpixel True
    alpha 0.88
    ease 1.4 alpha 1.0
    ease 1.4 alpha 0.88
    repeat

transform lc_pov_glow_breathe:
    subpixel True
    alpha 0.8 zoom 1.0
    ease 1.4 alpha 1.0 zoom 1.12
    ease 1.4 alpha 0.8 zoom 1.0
    repeat

# Full/Developer red button: an expanding, fading ring behind it while idle,
# a springy scale-up on hover.
transform lc_pov_bang_ring:
    subpixel True
    zoom 1.0 alpha 0.55
    linear 1.3 zoom 1.45 alpha 0.0
    pause 0.5
    repeat

transform lc_pov_bang_breathe:
    subpixel True
    zoom 1.0
    ease 0.9 zoom 1.03
    ease 0.9 zoom 1.0
    repeat

transform lc_pov_bang_hover:
    subpixel True
    zoom 0.94
    easein_back 0.2 zoom 1.1

transform lc_pov_hover_pop:
    subpixel True
    zoom 0.9 alpha 0.85
    easein_back 0.18 zoom 1.12 alpha 1.0
    block:
        ease 0.7 zoom 1.04
        ease 0.7 zoom 1.12
        repeat

init python:
    def lc_pov_static(a=1.0, z=1.0):
        """Fixed alpha/zoom wrapper with the same call shape as the ATL cue
        transforms: lc_pov_static(a, z)(child). A plain function, because a
        parameterised ATL transform would bind `child` to its next positional
        parameter (z) and crash with "must be real number, not str"."""
        def apply(child):
            return Transform(child, alpha=a, zoom=z)
        return apply

    _lc_pov_art_cache = {}
    # Sparkle sizes (the 44px cursor art). Hover stays larger than idle.
    LC_POV_STAR_ZOOM_IDLE = 1.6
    LC_POV_STAR_ZOOM_HOVER = 1.8

    def lc_pov_cue_art(size, hover=False, still=False, bang=False):
        """Centred cue art filling a size x size hit area (cached per state, so a
        screen re-evaluation never restarts the animation).

        Idle: warm glow + twinkling gold sparkle. Hover: brighter pink glow,
        the pink hover sparkle and a small springy pulse. still=True replaces
        every animation with a fixed glow (reduced motion). bang=True draws the
        Full/Developer red circular "!" button instead of the sparkle."""
        key = (size, bool(hover), bool(still), bool(bang))
        if key in _lc_pov_art_cache:
            return _lc_pov_art_cache[key]
        if hover:
            glow = "gui/pov/glow_hover.svg"
            star = Transform("gui/cursor/sparkle_hover.png", zoom=LC_POV_STAR_ZOOM_HOVER)
            glow_t = lc_pov_static(1.0, 1.08) if still else lc_pov_hover_pop
            star_t = lc_pov_static(1.0, 1.1) if still else lc_pov_hover_pop
        else:
            glow = "gui/pov/glow_idle.svg"
            star = Transform("gui/cursor/sparkle_idle.png", zoom=LC_POV_STAR_ZOOM_IDLE)
            glow_t = lc_pov_static(0.95, 1.06) if still else lc_pov_glow_breathe
            star_t = lc_pov_static(1.0) if still else lc_pov_twinkle
        if bang:
            # Red circular "!" button (gui/pov/bang_*.svg, tools/gen_pov_cue_assets.py).
            layers = []
            if not hover and not still:
                layers.append(Transform(lc_pov_bang_ring("gui/pov/bang_ring.svg"), xalign=0.5, yalign=0.5))
            if hover:
                face = lc_pov_static(1.0, 1.08)("gui/pov/bang_hover.svg") if still else lc_pov_bang_hover("gui/pov/bang_hover.svg")
            else:
                face = lc_pov_static(1.0)("gui/pov/bang_idle.svg") if still else lc_pov_bang_breathe("gui/pov/bang_idle.svg")
            layers.append(Transform(face, xalign=0.5, yalign=0.5))
            art = Fixed(*layers, xysize=(size, size))
            _lc_pov_art_cache[key] = art
            return art
        layers = [Transform(glow_t(glow), xalign=0.5, yalign=0.5)]
        if not hover:
            # Brighter warm core so the idle (Immersive) sparkle reads on dark hair.
            layers.append(Transform(glow_t(glow), zoom=0.55, xalign=0.5, yalign=0.5))
        layers.append(Transform(star_t(star), xalign=0.5, yalign=0.5))
        art = Fixed(*layers, xysize=(size, size))
        _lc_pov_art_cache[key] = art
        return art

screen lc_pov_hotspot():
    zorder 105
    use lc_pov_hotspot_body(LC_POV_HITBOX)

screen lc_pov_hotspot():
    variant "touch"
    zorder 105
    use lc_pov_hotspot_body(LC_POV_HITBOX_TOUCH)

screen lc_pov_hotspot_body(size):
    if lc_pov_available():
        $ moment_id = lc_pov_active
        $ entry = LC_POV_OPPORTUNITIES[moment_id]
        $ mode = current_choice_mode()
        $ px, py, _w, _h = lc_pov_hit_rect(entry, size)
        $ still = lc_pov_reduce_motion()
        $ cue_title = gallery_customize_names(entry["title"])
        $ bang = mode in ("full", "developer")
        timer 0.05 action Function(lc_pov_announce_cue, moment_id)
        button:
            xpos px
            ypos py
            xysize (size, size)
            background lc_pov_cue_art(size, False, still, bang)
            hover_background lc_pov_cue_art(size, True, still, bang)
            focus_mask None
            alt "Hidden moment: [cue_title]"
            action Function(lc_pov_open, moment_id)
            hovered Function(lc_pov_hover_sound)
            if mode == "insight":
                # Gold "!" beside the sparkle; on hover/focus it turns white
                # with the pink hover rim so it reads as part of the button.
                text "!":
                    font "DejaVuSans-Bold.ttf"
                    size 32
                    color "#f4c65c"
                    hover_color "#ffffff"
                    outlines [(3, "#432823", 0, 0)]
                    hover_outlines [(3, "#c2185b", 0, 0), (5, "#43282399", 0, 0)]
                    xpos (size // 2 + 14)
                    ypos (size // 2 - 44)
        if mode == "developer":
            # Id label beside the hit area; flips to the left near the right edge.
            $ label_right = px + size + 4 + 240 <= config.screen_width
            text "[moment_id]":
                xpos ((px + size + 4) if label_right else (px - 4))
                xanchor (0.0 if label_right else 1.0)
                ypos (py + size // 2 - 12)
                size 20 color "#ffdb82" outlines [(2, "#231019", 0, 0)]

# ------------------------------------------------------------- viewer transition
# The viewer opens on a copy of the source CG that matches the master layer, so fading it in only
# fades the dialogue box away; then it pushes toward the sparkle and the POV fades up over it.
transform lc_pov_push_in(xa, ya, z, t):
    subpixel True
    xalign xa yalign ya
    zoom 1.0 alpha 0.0
    parallel:
        ease (t * 0.25) alpha 1.0
    parallel:
        easein t zoom z
    # Hidden behind the opaque POV from here on (and out of any letterbox bars).
    alpha 0.0

transform lc_pov_push_out(xa, ya, z, t):
    subpixel True
    xalign xa yalign ya
    zoom z alpha 1.0
    parallel:
        ease (t * 0.8) zoom 1.0
    parallel:
        pause (t * 0.75)
        ease (t * 0.25) alpha 0.0

transform lc_pov_reveal(t):
    subpixel True
    xalign 0.5 yalign 0.5
    alpha 0.0 zoom 1.08
    pause (t * 0.4)
    ease (t * 0.6) alpha 1.0 zoom 1.0

transform lc_pov_unreveal(t):
    subpixel True
    xalign 0.5 yalign 0.5
    alpha 1.0 zoom 1.0
    ease (t * 0.45) alpha 0.0 zoom 1.06

transform lc_pov_fade(a0, a1, delay, t):
    alpha a0
    pause delay
    ease t alpha a1

screen lc_pov_viewer(moment_id):
    modal True
    # Above the phone notification banner (620) so a toast never covers the art.
    zorder 630
    default closing = False
    $ entry = LC_POV_OPPORTUNITIES.get(moment_id)
    $ instant = lc_pov_instant()
    $ dismiss = Function(lc_pov_close) if instant else SetScreenVariable("closing", True)
    key "K_ESCAPE" action dismiss
    key "game_menu" action dismiss
    key "mouseup_3" action dismiss
    if closing:
        timer LC_POV_OUT action Function(lc_pov_close)
    if instant:
        add Solid("#110c12")
    elif closing:
        add Solid("#110c12") at lc_pov_fade(1.0, 0.0, LC_POV_OUT * 0.75, LC_POV_OUT * 0.25)
    else:
        add Solid("#110c12") at lc_pov_fade(0.0, 1.0, 0.0, LC_POV_IN * 0.25)
    if entry and lc_pov_active == moment_id and lc_pov_in_scope(moment_id):
        $ xa, ya = lc_pov_focus(moment_id)
        $ source = Transform(entry["source"], xysize=(1920, 1080))
        $ art = Transform(entry["image"], fit="contain", xysize=(1920, 1080))
        if instant:
            add art align (0.5, 0.5)
        elif closing:
            add source at lc_pov_push_out(xa, ya, LC_POV_PUSH_ZOOM, LC_POV_OUT)
            add art at lc_pov_unreveal(LC_POV_OUT)
        else:
            add source at lc_pov_push_in(xa, ya, LC_POV_PUSH_ZOOM, LC_POV_IN)
            add art at lc_pov_reveal(LC_POV_IN)
        if not closing:
            frame:
                background None
                padding (0, 0)
                at (Transform() if instant else lc_pov_fade(0.0, 1.0, LC_POV_IN * 0.7, 0.3))
                xpos 48 ypos 32
                vbox:
                    spacing 12
                    text gallery_customize_names(entry["title"]):
                        font "fonts/PatrickHand-Regular.ttf"
                        size 34 color "#fff2d8" outlines [(2, "#21131c", 0, 0)]
                    if entry["mature"]:
                        text "18+" size 24 color "#fff2d8"
    # A full-screen input shield consumes dismiss keys/clicks without Return().
    button:
        xfill True
        yfill True
        background None
        keyboard_focus False
        action NullAction()
    if not closing:
        textbutton "Close view":
            at (Transform() if instant else lc_pov_fade(0.0, 1.0, LC_POV_IN * 0.7, 0.3))
            xpos 1620 ypos 32
            xsize 250 ysize 64
            text_size 32
            alt "Close hidden moment"
            action dismiss
