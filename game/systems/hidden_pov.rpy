# Optional POVs are scene-scoped, not story choices. Never show their image on
# the master layer: only an intentional click records it as seen for the Gallery.
default lc_pov_active = None
default lc_pov_viewed = False

init python:
    # Registry is init-time data; each new moment needs only a row and begin/end.
    LC_POV_OPPORTUNITIES = {}

    def lc_pov_register(moment_id, image, source, position, title, mature=False):
        if moment_id in LC_POV_OPPORTUNITIES:
            raise ValueError("Duplicate optional POV: " + moment_id)
        if not (isinstance(position, tuple) and len(position) == 2):
            raise ValueError("POV position must be a (x, y) pixel pair")
        LC_POV_OPPORTUNITIES[moment_id] = {
            "image": image, "source": source, "position": position,
            "title": title, "mature": bool(mature),
        }

    def lc_pov_begin(moment_id):
        if moment_id not in LC_POV_OPPORTUNITIES:
            raise ValueError("Unknown optional POV: " + moment_id)
        renpy.store.lc_pov_active = moment_id
        renpy.store.lc_pov_viewed = False
        return None

    def lc_pov_end():
        renpy.store.lc_pov_active = None
        renpy.store.lc_pov_viewed = False
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

# Keep the artwork inside its fixed 64x64 hit area. Scaling never moves the
# button or reflows dialogue; the normal-mode cue uses the existing cursor art.
transform lc_pov_twinkle:
    subpixel True
    alpha 0.72
    ease 1.4 alpha 1.0
    ease 1.4 alpha 0.72
    repeat

screen lc_pov_hotspot():
    zorder 105
    if lc_pov_available():
        $ moment_id = lc_pov_active
        $ entry = LC_POV_OPPORTUNITIES[moment_id]
        $ mode = current_choice_mode()
        $ px, py = entry["position"]
        button:
            xpos px
            ypos py
            xysize (64, 64)
            background None
            hover_background None
            focus_mask None
            action Function(lc_pov_open, moment_id)
            if mode in ("full", "developer"):
                text "!":
                    font "DejaVuSans.ttf"
                    size 46
                    color "#d93238"
                    outlines [(2, "#35121a", 0, 0)]
                    align (0.5, 0.5)
            else:
                add "gui/cursor/sparkle_idle.png" at lc_pov_twinkle:
                    align (0.5, 0.5)
                    zoom 0.85
                if mode == "insight":
                    text "!":
                        font "DejaVuSans.ttf"
                        size 27
                        color "#efbd55"
                        outlines [(2, "#432823", 0, 0)]
                        xpos 40
                        ypos 2
        if mode == "developer":
            text "[moment_id]" xpos (px + 68) ypos py size 20 color "#ffdb82" outlines [(2, "#231019", 0, 0)]

screen lc_pov_viewer(moment_id):
    modal True
    zorder 400
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
        action Function(lc_pov_close)
