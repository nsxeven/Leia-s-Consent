# PHONE WALLPAPER (darryn 2026-11-09)
# Any picture sent in a chat (or kept in Photos) can become the phone's
# home-screen background, chosen like on a real phone: open the photo, tap
# "Set as wallpaper", drag to move it, zoom with the mouse wheel or the - / +
# keys (touch / JoiPlay), then Set. Settings > Reset wallpaper goes back to
# the default villa art.
#
# Save data is plain: phone_wallpaper = None or
#   {"image": <image name>, "zoom": 1.0..4.0, "x": 0..1, "y": 0..1}
# (maths and validation: python-packages/lc_wallpaper_crop.py). Old saves
# load with None. No displayable is ever stored in the save.

default phone_wallpaper = None


init 96 python:
    import pygame_sdl2 as _lc_wp_pygame
    import lc_wallpaper_crop as lc_wp

    # Flat handset screen inside the 540x1040 phone (matches the art masks).
    LC_WP_X = 17
    LC_WP_Y = 10
    LC_WP_W = 506
    LC_WP_H = 1020
    LC_WP_MASK = "gui/phone/sprite_match/phone_wall_mask.png"
    LC_WP_SHADE = "gui/phone/sprite_match/phone_wall_shade.png"
    LC_WP_FRAME = "gui/phone/sprite_match/phone_wall_frame.png"
    LC_WP_DOCK = "gui/phone/sprite_match/phone_wall_dock.png"

    def _lc_wp_abs(value):
        # Transform crop treats floats as fractions; absolute() means pixels.
        return renpy.display.position.absolute(value)

    def lc_phone_wallpaper():
        """The saved wallpaper as a valid record, or None (unset/missing art)."""
        data = lc_wp.normalize(getattr(store, "phone_wallpaper", None))
        if data and renpy.has_image(data["image"]):
            return data
        return None

    def lc_phone_wallpaper_active():
        return lc_phone_wallpaper() is not None

    def lc_phone_wallpaper_reset():
        store.phone_wallpaper = None
        lc_ui_play("back")
        renpy.restart_interaction()

    def lc_phone_wallpaper_commit(editor):
        store.phone_wallpaper = lc_wp.make(editor.image, editor.zoom, editor.cx, editor.cy)
        lc_ui_play("pick")
        renpy.restart_interaction()

    class LCWallpaperView(renpy.Displayable):
        """The photo cropped to the phone screen exactly as chosen.

        State is plain attributes only (no revertable containers, no slot
        tricks): the editor changes it per event.
        """

        def __init__(self, image, zoom=1.0, cx=0.5, cy=0.5, **kwargs):
            super(LCWallpaperView, self).__init__(**kwargs)
            self.image = image
            self.zoom = lc_wp.clamp_zoom(zoom)
            self.cx = cx
            self.cy = cy
            self.iw = 0
            self.ih = 0
            self.shown_key = None
            self.shown = None

        def render(self, width, height, st, at):
            rv = renpy.Render(LC_WP_W, LC_WP_H)
            child = renpy.displayable(self.image)
            iw, ih = renpy.render(child, LC_WP_W, LC_WP_H, st, at).get_size()
            if iw <= 0 or ih <= 0:
                return rv
            if (iw, ih) != (self.iw, self.ih):
                self.iw, self.ih = iw, ih
                self.cx, self.cy = lc_wp.clamp_centre(self.cx, self.cy, iw, ih, LC_WP_W, LC_WP_H, self.zoom)
            box = lc_wp.crop_rect(iw, ih, LC_WP_W, LC_WP_H, self.zoom, self.cx, self.cy)
            key = (self.image,) + tuple(round(v, 3) for v in box)
            if key != self.shown_key:
                self.shown_key = key
                photo = Transform(child, crop=tuple(_lc_wp_abs(v) for v in box), xysize=(LC_WP_W, LC_WP_H))
                self.shown = AlphaMask(photo, LC_WP_MASK)
            rv.blit(renpy.render(self.shown, LC_WP_W, LC_WP_H, st, at), (0, 0))
            return rv

        def visit(self):
            return [renpy.displayable(self.image)]

    class LCWallpaperEditor(LCWallpaperView):
        """Drag to pan, wheel to zoom about the pointer, - / + about the centre."""

        def __init__(self, image, **kwargs):
            saved = lc_phone_wallpaper()
            if saved and saved["image"] == image:
                zoom, cx, cy = saved["zoom"], saved["x"], saved["y"]
            else:
                zoom, cx, cy = lc_wp.ZOOM_MIN, 0.5, 0.5
            super(LCWallpaperEditor, self).__init__(image, zoom, cx, cy, **kwargs)
            self.focusable = True
            self.drag_from = None

        def render(self, width, height, st, at):
            rv = super(LCWallpaperEditor, self).render(width, height, st, at)
            # In the focus list (no hover focus) so a drag can grab the mouse
            # and a release over Cancel/Set doesn't press them.
            rv.add_focus(self, renpy.display.render.Render.NO_MOUSE_FOCUS, 0, 0, LC_WP_W, LC_WP_H)
            return rv

        def can_zoom_in(self):
            return self.zoom < lc_wp.ZOOM_MAX - 1e-6

        def can_zoom_out(self):
            return self.zoom > lc_wp.ZOOM_MIN + 1e-6

        def zoom_steps(self, steps, px=None, py=None, factor=None):
            new_zoom = lc_wp.step_zoom(self.zoom, steps, factor or lc_wp.ZOOM_STEP)
            if px is None:
                px, py = LC_WP_W / 2.0, LC_WP_H / 2.0
            if self.iw and self.ih:
                self.cx, self.cy, self.zoom = lc_wp.zoom_at(
                    self.cx, self.cy, self.zoom, new_zoom, px, py, self.iw, self.ih, LC_WP_W, LC_WP_H)
            else:
                self.zoom = new_zoom
            renpy.redraw(self, 0)
            renpy.restart_interaction()
            return None

        def _end_drag(self):
            self.drag_from = None
            if renpy.display.focus.get_grab() is self:
                renpy.display.focus.set_grab(None)

        def event(self, ev, x, y, st):
            pg = _lc_wp_pygame
            if self.drag_from is not None:
                if ev.type == pg.MOUSEMOTION:
                    if not any(getattr(ev, "buttons", (1,))):
                        self._end_drag()
                        return None
                    ox, oy = self.drag_from
                    self.drag_from = (x, y)
                    if self.iw and self.ih:
                        self.cx, self.cy = lc_wp.pan(
                            self.cx, self.cy, x - ox, y - oy, self.iw, self.ih, LC_WP_W, LC_WP_H, self.zoom)
                        renpy.redraw(self, 0)
                    raise renpy.IgnoreEvent()
                if ev.type == pg.MOUSEBUTTONUP and getattr(ev, "button", 1) == 1:
                    self._end_drag()
                    raise renpy.IgnoreEvent()

            if not (0 <= x < LC_WP_W and 0 <= y < LC_WP_H):
                return None

            if renpy.map_event(ev, "viewport_wheelup"):
                self.zoom_steps(1, x, y, lc_wp.WHEEL_STEP)
                raise renpy.IgnoreEvent()
            if renpy.map_event(ev, "viewport_wheeldown"):
                self.zoom_steps(-1, x, y, lc_wp.WHEEL_STEP)
                raise renpy.IgnoreEvent()

            if ev.type == pg.MOUSEBUTTONDOWN and getattr(ev, "button", 0) == 1:
                self.drag_from = (x, y)
                renpy.display.focus.force_focus(self)
                renpy.display.focus.set_grab(self)
                raise renpy.IgnoreEvent()
            return None

    _lc_wp_view_cache = python_dict()

    def lc_phone_wallpaper_view(wall):
        """One cached view per saved crop, so screen updates don't rebuild it."""
        key = (wall["image"], wall["zoom"], wall["x"], wall["y"])
        view = _lc_wp_view_cache.get(key)
        if view is None:
            _lc_wp_view_cache.clear()
            view = LCWallpaperView(wall["image"], wall["zoom"], wall["x"], wall["y"])
            _lc_wp_view_cache[key] = view
        return view


# Home-screen wallpaper layers: photo, readability shade, handset, dock.
# Drawn by phone_screen instead of phone_home.png when a wallpaper is set.
screen lc_phone_wallpaper_layers(wall):
    add lc_phone_wallpaper_view(wall) xpos LC_WP_X ypos LC_WP_Y
    add LC_WP_SHADE xpos LC_WP_X ypos LC_WP_Y
    add LC_WP_FRAME
    add LC_WP_DOCK


# Full-phone crop editor, opened from the photo viewer. Esc / right-click /
# Cancel go back one tier (to the photo); Set saves and returns to the chat.
screen lc_phone_wallpaper_editor(photo_asset):
    modal True
    zorder 390

    default wp_editor = LCWallpaperEditor(photo_asset)
    $ _wp_cancel = Function(lc_phone_back)  # one tier: editor -> photo viewer
    $ _wp_set = [Function(lc_phone_wallpaper_commit, wp_editor), Hide("lc_phone_wallpaper_editor"), Hide("lc_phone_photo_viewer")]
    $ _wp_in = Function(wp_editor.zoom_steps, 1) if wp_editor.can_zoom_in() else None
    $ _wp_out = Function(wp_editor.zoom_steps, -1) if wp_editor.can_zoom_out() else None

    key "K_ESCAPE" action _wp_cancel
    key "game_menu" action _wp_cancel
    key "mouseup_3" action _wp_cancel
    key "K_EQUALS" action _wp_in
    key "K_PLUS" action _wp_in
    key "K_KP_PLUS" action _wp_in
    key "K_MINUS" action _wp_out
    key "K_KP_MINUS" action _wp_out

    add Solid("#12080e")

    fixed:
        xalign 0.5
        yalign 0.5
        xysize (540, 1040)

        add wp_editor xpos LC_WP_X ypos LC_WP_Y
        add LC_WP_SHADE xpos LC_WP_X ypos LC_WP_Y
        add LC_WP_FRAME

        # Faded home-screen preview (clock and apps) so the crop can be
        # judged the way it will look. Not interactive.
        fixed:
            at Transform(alpha=0.5)
            xysize (540, 1040)
            text "[lc_phone_home_caption()]":
                style "lc_sw_hand"
                size 26
                color "#FFFFFF"
                xalign 0.5
                ypos 96
                xmaximum 440
                outlines [(2, "#102033", 0, 1)]
            text "[lc_phone_clock_text()]":
                style "lc_sw_pixel_bold"
                size 70
                color "#FFFFFF"
                xalign 0.5
                ypos 132
                outlines [(2, "#102033", 0, 1)]
            for i, row in enumerate(LC_SM_HOME):
                fixed:
                    xpos 56 + (i % 4) * 114
                    ypos 280 + (i // 4) * 150
                    xysize (80, 118)
                    add Transform("gui/phone/sprite_match/" + row[0] + ".png", nearest=True)
                    text row[1]:
                        style "lc_sw_hand"
                        size 22
                        color "#FFFFFF"
                        outlines [(2, "#14243D", 0, 1)]
                        xalign 0.5
                        ypos 84
                        xsize 108
                        text_align 0.5

        frame:
            style "lc_sw_frame"
            xalign 0.5
            ypos 846
            background Frame("gui/phone/sprite_match/key.png", 18, 18)
            padding (18, 8)
            text "Drag to move  ·  scroll or - / + to zoom":
                style "lc_sw_hand"
                size 22
                color "#FFFFFF"
                text_align 0.5

        hbox:
            xalign 0.5
            ypos 916
            spacing 10
            textbutton "Cancel":
                style "lc_phone_btn"
                xfill False
                xsize 132
                action _wp_cancel
            textbutton "{font=DejaVuSans.ttf}−{/font}":
                style "lc_phone_btn"
                xfill False
                xsize 64
                action _wp_out
            textbutton "{font=DejaVuSans.ttf}+{/font}":
                style "lc_phone_btn"
                xfill False
                xsize 64
                action _wp_in
            textbutton "Set":
                style "lc_phone_btn_primary"
                xfill False
                xsize 132
                action _wp_set
