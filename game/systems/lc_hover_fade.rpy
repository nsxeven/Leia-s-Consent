## Smooth hover backgrounds, game-wide (darryn 2026-11-08: "no instant snaps").
##
## Ren'Py swaps a button's idle/hover/selected background and foreground art in
## one frame. This hook makes EVERY button cross-fade between its old and new
## background/foreground over LC_HOVER_IN (gaining hover/selection) or
## LC_HOVER_OUT (losing it); imagebuttons cross-fade their idle/hover images
## the same way. So choices, menu tabs, keycaps, phone rows, glass
## cards and title chips all ease the same way. Movement (lift, slide) is done by
## the shared ATL transforms in zzzzzzzz_scrapbook_ui.rpy with the same timings.
##
## Only real state changes between the four interactive states fade; a button's
## first style set-up (screen shown) never does. Set LC_HOVER_FADE = False to
## turn the hook off without touching screens.

define LC_HOVER_FADE = True
define LC_HOVER_IN = 0.18
define LC_HOVER_OUT = 0.22

init -50 python:
    import time as _lc_time

    _LC_FADE_STATES = ("idle_", "hover_", "selected_idle_", "selected_hover_", "insensitive_", "selected_insensitive_")

    class LCHoverBlend(renpy.Displayable):
        """Old art fading out under new art fading in (k = 0..1, eased)."""

        def __init__(self, old, new, k, fit=False, **kwargs):
            super(LCHoverBlend, self).__init__(**kwargs)
            self.old = old
            self.new = new
            self.k = k
            # fit: size to the art (imagebutton images) instead of filling.
            self.fit = fit

        def render(self, width, height, st, at):
            k = self.k
            parts = []
            if self.old is not None:
                # Opaque art stays under the incoming art until the end so the
                # card never dips see-through mid-fade; with no new art it fades.
                keep = (1.0 - k * k) if self.new is not None else (1.0 - k)
                if keep > 0.0:
                    parts.append(renpy.render(Transform(self.old, alpha=keep), width, height, st, at))
            if self.new is not None and k > 0.0:
                parts.append(renpy.render(Transform(self.new, alpha=k), width, height, st, at))
            if self.fit:
                w = max([r.width for r in parts] or [0])
                h = max([r.height for r in parts] or [0])
            else:
                w, h = width, height
            rv = renpy.Render(w, h)
            for r in parts:
                rv.blit(r, (0, 0))
            return rv

        def visit(self):
            return [d for d in (self.old, self.new) if d is not None]


    # python_object: a plain class with __slots__ (no rollback tracking).
    class _LCStyleProxy(python_object):
        """Reads every style property from the real style except the two arts."""

        __slots__ = ("_real", "background", "foreground", "child")

        def __init__(self, real, background, foreground, child):
            object.__setattr__(self, "_real", real)
            object.__setattr__(self, "background", background)
            object.__setattr__(self, "foreground", foreground)
            object.__setattr__(self, "child", child)

        def __getattr__(self, name):
            return getattr(object.__getattribute__(self, "_real"), name)


    def _lc_smooth(k):
        return k * k * (3.0 - 2.0 * k)


    def _lc_install_hover_fade():
        Button = renpy.display.behavior.Button
        if getattr(Button, "_lc_hover_fade_installed", False):
            return
        orig_prefix = Button.set_style_prefix
        orig_render = Button.render

        def set_style_prefix(self, prefix, root):
            if not (root and LC_HOVER_FADE and getattr(self, "_lc_rendered", False)):
                return orig_prefix(self, prefix, root)
            old_prefix = self.style.prefix
            if old_prefix == prefix or old_prefix not in _LC_FADE_STATES or prefix not in _LC_FADE_STATES:
                return orig_prefix(self, prefix, root)
            # Start from whatever is on screen now (mid-fade included).
            fade = getattr(self, "_lc_fade", None)
            if fade is not None:
                old_bg, old_fg, old_ch = fade[4], fade[5], fade[6]
            else:
                old_bg, old_fg, old_ch = self.style.background, self.style.foreground, self.style.child
            rv = orig_prefix(self, prefix, root)
            new_bg, new_fg, new_ch = self.style.background, self.style.foreground, self.style.child
            if old_bg is new_bg and old_fg is new_fg and old_ch is new_ch:
                self._lc_fade = None
                return rv
            gaining = prefix.endswith("hover_") or prefix.startswith("selected_")
            self._lc_fade = [(old_bg, old_fg, old_ch), None, _lc_time.time(),
                             (LC_HOVER_IN if gaining else LC_HOVER_OUT), old_bg, old_fg, old_ch]
            renpy.display.render.redraw(self, 0)
            return rv

        def render(self, width, height, st, at):
            self._lc_rendered = True
            fade = getattr(self, "_lc_fade", None)
            if fade is None:
                return orig_render(self, width, height, st, at)
            (old_bg, old_fg, old_ch), start, duration = fade[0], fade[2], fade[3]
            k = (_lc_time.time() - start) / max(0.01, duration)
            if k >= 1.0:
                self._lc_fade = None
                return orig_render(self, width, height, st, at)
            k = _lc_smooth(max(0.0, k))
            real = self.style
            new_bg, new_fg, new_ch = real.background, real.foreground, real.child
            bg = new_bg if old_bg is new_bg else LCHoverBlend(old_bg, new_bg, k)
            fg = new_fg if old_fg is new_fg else LCHoverBlend(old_fg, new_fg, k)
            ch = new_ch if (old_ch is new_ch or old_ch is None or new_ch is None) else LCHoverBlend(old_ch, new_ch, k, fit=True)
            # What is drawn right now, so a reversal mid-fade starts from here.
            fade[4], fade[5], fade[6] = bg, fg, ch
            self.style = _LCStyleProxy(real, bg, fg, ch)
            try:
                rv = orig_render(self, width, height, st, at)
            except Exception:
                # Never let polish break a screen: drop this fade, draw normally.
                self.style = real
                self._lc_fade = None
                return orig_render(self, width, height, st, at)
            finally:
                self.style = real
            renpy.display.render.redraw(self, 0)
            return rv

        Button.set_style_prefix = set_style_prefix
        Button.render = render
        Button._lc_hover_fade_installed = True

    _lc_install_hover_fade()
