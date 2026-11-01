# Developer capture for the scrapbook review. Not linked from any menu.
# Launch with LC_SHOT set (insight, full, one, zero, night, anim) and the
# game opens on the review instead of the main menu. Unset, before_main_menu
# returns immediately.

init -999 python:
    import os
    if os.environ.get("LC_SHOT"):
        config.gl_vsync = False
        config.performance_test = False
        config.predict_statements = 0

    # Opt in when GL cannot start. Ren'Py ignores RENPY_RENDERER=sw on its own.
    if os.environ.get("LC_FORCE_SOFTWARE"):
        import renpy.pygame as _pygame
        _set_mode = _pygame.display.set_mode

        def _borderless(size, flags=0, depth=0, *args, **kwargs):
            # Keep the 1920x1080 window from being shrunk by decorations, which
            # clips the right side of the scrapbook before the screenshot.
            return _set_mode(size, flags | _pygame.NOFRAME, depth)

        _pygame.display.set_mode = _borderless

        import renpy.display.core as _core
        _orig_draws = _core.Interface.get_draw_constructors

        def _software_draws(self):
            draws = _orig_draws(self)
            software = [item for item in draws if item[0] == "sw"]
            return software or draws

        _core.Interface.get_draw_constructors = _software_draws

init python:
    import os

    def lc_scrapbook_save_surface(surf, path):
        """Dump the pygame window as RGBX plus a size header.

        This software renderer stores R,G,B,pad. pygame.image.save treats the
        pad as a color channel and the saved picture slides off the right edge.
        The capture script turns the dump into a PNG.
        """
        import ctypes
        width, height = surf.get_size()
        pitch = surf.get_pitch()
        raw = ctypes.string_at(surf._pixels_address, pitch * height)
        with open(path + ".rgbx", "wb") as handle:
            handle.write(raw)
        with open(path + ".meta", "w") as handle:
            handle.write("{} {} {}\n".format(width, height, pitch))

    def lc_scrapbook_preview_build(photos=4):
        start = {
            "relationship": {"love": 50, "trust": 50, "boredom": 20, "momentum": 0},
            "partner": {"curiosity": 20, "temptation": 10, "exhibitionism": 10, "boundary_looseness": 10, "secrecy": 5},
            "player": {"jealousy": 20, "acceptance": 10},
        }
        end = {
            "relationship": dict(start["relationship"], love=52, trust=52, boredom=18),
            "partner": dict(start["partner"], secrecy=4),
            "player": dict(start["player"], acceptance=11),
        }
        choices = [
            {"id": "ch01_d3_ntr_talk", "deltas": [
                ("relationship", "love", 2),
                ("relationship", "trust", 2),
                ("relationship", "boredom", -2),
                ("partner", "secrecy", -1),
            ]},
            {"id": "ch01_d3_dessert_recommended", "deltas": [
                ("player", "acceptance", 1),
            ]},
        ]
        if photos < 0:
            # Worst case: every stat moved, and several long choice lines.
            end = {
                "relationship": {"love": 61, "trust": 44, "boredom": 28, "momentum": 6},
                "partner": {"curiosity": 27, "temptation": 16, "exhibitionism": 18, "boundary_looseness": 14, "secrecy": 9},
                "player": {"jealousy": 26, "acceptance": 17},
            }
            choices = [
                {"id": "ch01_d3_ntr_talk", "deltas": [
                    ("relationship", "love", 4), ("relationship", "trust", -3),
                    ("relationship", "boredom", 2), ("relationship", "momentum", 1),
                ]},
                {"id": "ch01_d3_dessert_recommended", "deltas": [
                    ("partner", "curiosity", 3), ("partner", "temptation", 2),
                    ("partner", "exhibitionism", 4), ("player", "acceptance", 2),
                ]},
                {"id": "ch01_d4_ntr_ask_gently", "deltas": [
                    ("partner", "secrecy", -2), ("partner", "boundary_looseness", 1),
                    ("player", "jealousy", 3),
                ]},
                {"id": "ch01_d5_ntr_u_press_hard", "deltas": [
                    ("relationship", "love", -2), ("partner", "secrecy", 2),
                ]},
            ]
            photos = 4
        gallery = [
            {"id": "arrival", "image": "ch01_villa_arrival", "caption": "Arrival", "dream": False},
            {"id": "window", "image": "ch01_bedroom_window", "caption": "The window", "dream": False},
            {"id": "pool", "image": "ch01_photo_group_white", "caption": "The pool", "dream": False},
            {"id": "dinner", "image": "ch01_dinner_arrival", "caption": "Dinner", "dream": False},
        ]
        store.lc_review_active = None
        store.lc_review_days = {
            "ch01_d3": {
                "start": start,
                "end": end,
                "moments": gallery[:photos],
                "choices": choices,
                "route": "ntr_talked",
                "facts": {},
                "titles_before": ("Curious Partner", "Affectionate Partner"),
                "titles_after": ("Uneasy Observer", "Growing Distant"),
                "partial": False,
                "summary": LC_REVIEW_ROUTES["ntr_talked"][1],
                "modified": False,
            },
        }
        store.persistent.lc_recap_animation = True
        store.persistent.lc_title_style = "story"


label before_main_menu:
    python:
        import os
        store.lc_scrapbook_shot = os.environ.get("LC_SHOT") or ""
        store.lc_scrapbook_shot_path = os.environ.get("LC_SHOT_PATH") or "/tmp/scrapbook.png"
        store.lc_scrapbook_frame = 0
        store.lc_scrapbook_frame_dir = os.environ.get("LC_FRAME_DIR") or "/tmp/scrapbook_frames"
    if lc_scrapbook_shot:
        jump lc_scrapbook_preview
    return


label lc_scrapbook_preview:
    python:
        import os
        store.lc_scrapbook_shot = os.environ.get("LC_SHOT") or "full"
        store.lc_scrapbook_shot_path = os.environ.get("LC_SHOT_PATH") or "/tmp/scrapbook.png"
        store.lc_scrapbook_frame = 0
        store.lc_scrapbook_frame_dir = os.environ.get("LC_FRAME_DIR") or "/tmp/scrapbook_frames"
    window hide
    $ quick_menu = False
    $ phone_hud_enabled = False
    scene black
    $ lc_scrapbook_preview_build(-1 if lc_scrapbook_shot == "worst" else (1 if lc_scrapbook_shot == "one" else (0 if lc_scrapbook_shot == "zero" else 4)))
    $ persistent.choice_display_mode = "insight" if lc_scrapbook_shot in ("insight", "one", "zero", "night") else "full"
    if lc_scrapbook_shot == "night":
        show screen lc_review_night_screen("ch01_d3")
        call screen lc_scrapbook_grabber(1.3, 1)
    elif lc_scrapbook_shot == "anim":
        $ lc_scrapbook_frame = 0
        $ lc_scrapbook_frame_limit = 36
        show screen lc_day_review_screen("ch01_d3", skipped=False)
        call screen lc_scrapbook_anim_grabber
    else:
        show screen lc_day_review_screen("ch01_d3", skipped=True)
        call screen lc_scrapbook_grabber(0.4, 1)
    return


init python:
    def lc_scrapbook_grab():
        import os
        os.makedirs(os.path.dirname(store.lc_scrapbook_shot_path) or ".", exist_ok=True)
        draw = renpy.display.draw
        info = renpy.display.get_info()
        with open("/tmp/scrapbook_geom.txt", "w") as handle:
            handle.write("screen %s x %s scale %s\n" % (info.current_w, info.current_h, getattr(draw, "scale_factor", None)))
            screen = getattr(draw, "screen", None)
            window = getattr(draw, "window", None)
            handle.write("surf %s window %s\n" % (
                screen.get_size() if screen is not None else None,
                window.get_size() if window is not None else None,
            ))
        window = getattr(draw, "window", None)
        if window is not None:
            lc_scrapbook_save_surface(window, store.lc_scrapbook_shot_path)
        else:
            renpy.screenshot(store.lc_scrapbook_shot_path)
        if store.lc_scrapbook_shot == "anim":
            return
        renpy.quit()


screen lc_scrapbook_grabber(delay=0.4, frames=1):
    modal True
    zorder 400
    timer delay action [Function(lc_scrapbook_grab), Return()]


init python:
    def lc_scrapbook_grab_frame():
        import os
        os.makedirs(store.lc_scrapbook_frame_dir, exist_ok=True)
        path = os.path.join(store.lc_scrapbook_frame_dir, "f%03d.png" % store.lc_scrapbook_frame)
        window = getattr(renpy.display.draw, "window", None)
        if window is not None:
            lc_scrapbook_save_surface(window, path)
        else:
            renpy.screenshot(path)
        store.lc_scrapbook_frame += 1

    class LcScrapbookFrameGrab(renpy.Displayable):
        """Save frames from render time, without restarting the interaction.

        A timer action restarts the interaction every frame. That resets the
        clock the stat-bar timers read, so the bars never leave yesterday.
        Render time keeps moving for the whole call, and so do the bars.
        """

        def __init__(self, interval, limit, **kwargs):
            super(LcScrapbookFrameGrab, self).__init__(**kwargs)
            self.interval = float(interval)
            self.limit = int(limit)
            self.saved = 0

        def render(self, width, height, st, at):
            while self.saved < self.limit and st + 0.001 >= self.saved * self.interval:
                lc_scrapbook_grab_frame()
                self.saved += 1
            if self.saved < self.limit:
                renpy.redraw(self, max(0.01, self.saved * self.interval - st))
            return renpy.Render(1, 1)

        def event(self, ev, x, y, st):
            if self.saved >= self.limit:
                renpy.quit()
            return None


screen lc_scrapbook_anim_grabber():
    # Not modal: time events have to reach the journal so its bars can run.
    zorder 400
    add LcScrapbookFrameGrab(0.18, lc_scrapbook_frame_limit)
