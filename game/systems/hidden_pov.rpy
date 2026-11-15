# Optional POVs are scene-scoped, not story choices. Never show their image on
# the master layer: only an intentional click records it as seen for the Gallery.
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

init python:
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
                        mature=None, center=None, gallery_id=None, sfx=True):
        """Register one optional POV moment.

        position: legacy (x, y) upper-left of a 64x64 slot (sparkle centre = +32).
        center:   (x, y) sparkle centre; preferred for new moments.
        mature:   None derives it from the Gallery row that lists `image`.
        sfx:      play the soft sparkle chime when the cue first appears.
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
        renpy.mark_image_seen(image)  # SDK exports/persistentexports.py.
        renpy.save_persistent()
        renpy.show_screen("lc_pov_viewer", moment_id=moment_id)
        return None

    def lc_pov_close():
        renpy.hide_screen("lc_pov_viewer")
        return None

    # The say behavior's auto-forward timer consults config.afm_callback before
    # advancing (SDK display/behavior.py). Chain the original callback; do not
    # mutate the player's persistent Auto preference, so closing restores it.
    _lc_pov_prior_afm_callback = config.afm_callback
    def lc_pov_afm_callback():
        if renpy.get_screen("lc_pov_viewer"):
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
transform lc_pov_twinkle:
    subpixel True
    alpha 0.72
    ease 1.4 alpha 1.0
    ease 1.4 alpha 0.72
    repeat

transform lc_pov_glow_breathe:
    subpixel True
    alpha 0.55 zoom 0.92
    ease 1.4 alpha 0.85 zoom 1.0
    ease 1.4 alpha 0.55 zoom 0.92
    repeat

transform lc_pov_hover_pop:
    subpixel True
    zoom 0.9 alpha 0.85
    easein_back 0.18 zoom 1.12 alpha 1.0
    block:
        ease 0.7 zoom 1.04
        ease 0.7 zoom 1.12
        repeat

transform lc_pov_static(a=1.0, z=1.0):
    alpha a zoom z

init python:
    _lc_pov_art_cache = {}

    def lc_pov_cue_art(size, hover=False, still=False, bang=False):
        """Centred cue art filling a size x size hit area (cached per state, so a
        screen re-evaluation never restarts the animation).

        Idle: warm glow + twinkling gold sparkle. Hover: brighter pink glow,
        the pink hover sparkle and a small springy pulse. still=True replaces
        every animation with a fixed glow (reduced motion). bang=True draws the
        Full/Developer red "!" instead of the sparkle."""
        key = (size, bool(hover), bool(still), bool(bang))
        if key in _lc_pov_art_cache:
            return _lc_pov_art_cache[key]
        if hover:
            glow = "gui/pov/glow_hover.svg"
            star = Transform("gui/cursor/sparkle_hover.png", zoom=1.0)
            glow_t = lc_pov_static(1.0, 1.08) if still else lc_pov_hover_pop
            star_t = lc_pov_static(1.0, 1.1) if still else lc_pov_hover_pop
        else:
            glow = "gui/pov/glow_idle.svg"
            star = Transform("gui/cursor/sparkle_idle.png", zoom=0.85)
            glow_t = lc_pov_static(0.75) if still else lc_pov_glow_breathe
            star_t = lc_pov_static(1.0) if still else lc_pov_twinkle
        if bang:
            star = Text("!", font="DejaVuSans.ttf", size=(50 if hover else 46),
                        color=("#ff5a60" if hover else "#d93238"), outlines=[(2, "#35121a", 0, 0)])
            star_t = lc_pov_static(1.0)
            glow_t = lc_pov_static(0.9 if hover else 0.5)
        art = Fixed(
            Transform(glow_t(glow), xalign=0.5, yalign=0.5),
            Transform(star_t(star), xalign=0.5, yalign=0.5),
            xysize=(size, size))
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
            hovered Function(lc_ui_sound, "tick", hover=True)
            if mode == "insight":
                text "!":
                    font "DejaVuSans.ttf"
                    size 27
                    color "#efbd55"
                    outlines [(2, "#432823", 0, 0)]
                    xpos (size // 2 + 8)
                    ypos (size // 2 - 34)
        if mode == "developer":
            text "[moment_id]" xpos (px + size + 4) ypos (py + size // 2 - 12) size 20 color "#ffdb82" outlines [(2, "#231019", 0, 0)]

screen lc_pov_viewer(moment_id):
    modal True
    # Above the phone notification banner (620) so a toast never covers the art.
    zorder 630
    $ entry = LC_POV_OPPORTUNITIES.get(moment_id)
    key "K_ESCAPE" action Function(lc_pov_close)
    key "game_menu" action Function(lc_pov_close)
    key "mouseup_3" action Function(lc_pov_close)
    add Solid("#110c12")
    if entry and lc_pov_active == moment_id and lc_pov_in_scope(moment_id):
        add entry["image"]:
            align (0.5, 0.5)
            fit "contain"
            xysize (1920, 1080)
        text gallery_customize_names(entry["title"]):
            xpos 48 ypos 32
            font "fonts/PatrickHand-Regular.ttf"
            size 34 color "#fff2d8" outlines [(2, "#21131c", 0, 0)]
        if entry["mature"]:
            text "18+" xpos 48 ypos 78 size 24 color "#fff2d8"
    # A full-screen input shield consumes dismiss keys/clicks without Return().
    button:
        xfill True
        yfill True
        background None
        action NullAction()
    textbutton "Close view":
        xpos 1620 ypos 32
        xsize 250 ysize 64
        text_size 32
        alt "Close hidden moment"
        action Function(lc_pov_close)
