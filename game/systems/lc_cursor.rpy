# Themed mouse cursor: the Sparkle glint (darryn 2026-11-08, draft E).
#
# Ren'Py draws the cursor itself (config.mouse_displayable), so it shows in
# fullscreen, windowed and the browser build alike. Touch devices (phones,
# JoiPlay) keep no cursor.
#
# The sparkle is alive:
#   * idle: a slow twinkle (gentle rock + breathing pulse);
#   * moving: it leaves a short trail of fading glints;
#   * over anything clickable it eases (same timing as button hovers,
#     LC_HOVER_IN / LC_HOVER_OUT) from honey to pink, tilts, grows a touch, and
#     a small twin sparkle orbits it.
# The hotspot is the sparkle's centre. Art: gui/cursor/ (tools/gen_cursor_sparkle.py).
# Knob: LC_CURSOR_TRAIL (glints on/off).

define LC_CURSOR_TRAIL = True

init 5 python:
    import math as _lc_cm
    import time as _lc_ct

    LC_CURSOR_DIR = "gui/cursor/"
    LC_CURSOR_TRAIL_LIFE = 0.45     # seconds a glint lingers
    LC_CURSOR_TRAIL_STEP = 18       # px of movement between glints

    class LCCursor(MouseDisplayable):
        """Animated sparkle; everything is computed from wall-clock time each frame.

        Per-frame state lives in a plain python_list / floats on this displayable,
        never in rollback-tracked store objects (see lc_hover_fade.rpy, #168).
        """

        def __init__(self):
            super(LCCursor, self).__init__(LC_CURSOR_DIR + "sparkle_idle.png", 22, 22)
            self.idle_art = renpy.displayable(LC_CURSOR_DIR + "sparkle_idle.png")
            self.hover_art = renpy.displayable(LC_CURSOR_DIR + "sparkle_hover.png")
            self.twin_art = renpy.displayable(LC_CURSOR_DIR + "sparkle_twin.png")
            self.mote_art = renpy.displayable(LC_CURSOR_DIR + "sparkle_mote.png")
            self.h = 0.0
            self.last_t = None
            self.last_xy = None
            self.trail = python_list()

        def _focused(self):
            try:
                return renpy.display.focus.get_focused() is not None
            except Exception:
                return False

        def _blit_centred(self, rv, d, x, y, width, height, st, at):
            cr = renpy.render(d, width, height, st, at)
            rv.subpixel_blit(cr, (x - cr.width / 2.0, y - cr.height / 2.0))

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            now = _lc_ct.time()
            dt = 0.0 if self.last_t is None else min(0.1, now - self.last_t)
            self.last_t = now

            # Ease toward the hover state with the button-hover timings.
            target = 1.0 if self._focused() else 0.0
            if target > self.h:
                self.h = min(1.0, self.h + dt / max(0.01, LC_HOVER_IN))
            elif target < self.h:
                self.h = max(0.0, self.h - dt / max(0.01, LC_HOVER_OUT))
            s = self.h * self.h * (3.0 - 2.0 * self.h)

            x, y = renpy.get_mouse_pos()
            if not ((0 <= x < width) and (0 <= y < height) and renpy.is_mouse_visible()):
                del self.trail[:]
                self.last_xy = None
                renpy.redraw(self, 0.2)
                return rv

            # Trail of glints behind a moving cursor.
            if LC_CURSOR_TRAIL:
                if self.last_xy is None:
                    self.last_xy = (x, y)
                elif _lc_cm.hypot(x - self.last_xy[0], y - self.last_xy[1]) >= LC_CURSOR_TRAIL_STEP:
                    self.trail.append((self.last_xy[0], self.last_xy[1], now, renpy.random.uniform(0, 90)))
                    self.last_xy = (x, y)
                self.trail[:] = [p for p in self.trail if now - p[2] < LC_CURSOR_TRAIL_LIFE]
                for px, py, pt, pr in self.trail:
                    a = 1.0 - (now - pt) / LC_CURSOR_TRAIL_LIFE
                    mote = Transform(self.mote_art, alpha=0.85 * a, zoom=0.45 + 0.55 * a, rotate=pr + 120 * (1 - a))
                    self._blit_centred(rv, mote, px, py, width, height, st, at)
            elif self.trail:
                del self.trail[:]

            # Twinkle: slow rock and breathing pulse; on hover it tilts, grows and quickens.
            rock = _lc_cm.sin(now * 2 * _lc_cm.pi / (2.6 - 0.8 * s)) * (6 + 6 * s)
            pulse = 1.0 + (0.045 + 0.03 * s) * _lc_cm.sin(now * 2 * _lc_cm.pi / (1.7 - 0.5 * s))
            rot = rock + 22 * s
            zoom = pulse * (1.0 + 0.1 * s)

            if s < 1.0:
                self._blit_centred(rv, Transform(self.idle_art, rotate=rot, zoom=zoom, alpha=1.0 - s),
                                   x, y, width, height, st, at)
            if s > 0.0:
                self._blit_centred(rv, Transform(self.hover_art, rotate=rot, zoom=zoom, alpha=s),
                                   x, y, width, height, st, at)
                # Twin sparkle orbiting the cursor, twinkling.
                ang = now * 2 * _lc_cm.pi / 2.2
                tx = x + _lc_cm.cos(ang) * 15 * (0.6 + 0.4 * s)
                ty = y + _lc_cm.sin(ang) * 11 * (0.6 + 0.4 * s) - 3
                tz = (0.75 + 0.25 * _lc_cm.sin(now * 9.0)) * s
                self._blit_centred(rv, Transform(self.twin_art, rotate=-rot * 2, zoom=max(0.05, tz), alpha=s),
                                   tx, ty, width, height, st, at)

            renpy.redraw(self, 0)
            return rv

        def visit(self):
            return [self.idle_art, self.hover_art, self.twin_art, self.mote_art]

    if not renpy.variant("touch"):
        config.mouse_displayable = LCCursor()
