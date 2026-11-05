## Typing sounds for the name cards (and any other renpy.input() prompt).
##
## The `input` screen's Input gets `changed lc_input_typed`: a longer text
## plays one of four soft key clicks, a shorter one plays key_back. In Ren'Py an
## Input with a `changed` callback no longer returns its text on Enter by
## itself, so the screen also gives it `action Function(lc_input_submit)`,
## which returns the typed text (plus any IME text still being composed),
## exactly what renpy.input() returned before.
## Sounds are self-made (game/audio/ui/key_*.ogg) and follow the UI volume slider.

init python:
    LC_TYPING_KEYS = ("key_1", "key_2", "key_3", "key_4")
    _lc_typing = {"last": None, "n": 0}

    def lc_input_reset():
        _lc_typing["last"] = None

    def lc_input_typed(new_text):
        last = _lc_typing["last"]
        if last is None:
            widget = renpy.get_widget("input", "input")
            last = getattr(widget, "default", "") or ""
        _lc_typing["last"] = new_text
        if len(new_text) > len(last):
            # Random click, never the same one twice in a row.
            choices = [k for k in LC_TYPING_KEYS if k != _lc_typing.get("key")]
            _lc_typing["key"] = renpy.random.choice(choices)
            lc_ui_sound(_lc_typing["key"])
        elif len(new_text) < len(last):
            lc_ui_sound("key_back")

    def lc_input_submit():
        widget = renpy.get_widget("input", "input")
        if widget is None:
            return None
        text = widget.content
        if widget.edit_text:
            text = text[:widget.caret_pos] + widget.edit_text + text[widget.caret_pos:]
        lc_ui_sound("key_enter")
        _lc_typing["last"] = None
        return text
