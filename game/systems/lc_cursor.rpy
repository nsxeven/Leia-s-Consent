# Themed mouse cursor (darryn 2026-11-08).
#
# Players lost the Windows cursor in fullscreen. Ren'Py now draws the cursor
# itself (config.mouse_displayable), so it is part of the picture and shows in
# fullscreen, windowed and the browser build alike. Pixel art in the scrapbook
# palette: pink arrow; with a little heart while it is over anything clickable.
#
# Art: gui/scrapbook/cursor.png and cursor_button.png (36x38, hotspot at the
# top-left tip). Replace the PNGs to restyle; keep the tip at (0, 0).
# Touch devices (phones, JoiPlay) keep no cursor.

init 5 python:

    class LCCursor(MouseDisplayable):
        """Default arrow; the 'button' cursor while something is focused."""

        def get_cursor_name(self):
            try:
                if renpy.display.focus.get_focused() is not None:
                    return "button"
            except Exception:
                pass
            return MouseDisplayable.get_cursor_name(self)

    if not renpy.variant("touch"):
        config.mouse_displayable = LCCursor("gui/scrapbook/cursor.png", 0, 0).add(
            "button", "gui/scrapbook/cursor_button.png", 0, 0)
