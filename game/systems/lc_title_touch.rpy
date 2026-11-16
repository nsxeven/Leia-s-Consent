# Title-screen touch - click Leia on the title screen for a reaction
#
# Purpose: A click on Leia plays a voice clip, a small motion and a brief expression, then she
#   settles back to the Customize face. Chest/private-area clicks escalate and only turn lewd when
#   18+ title options are shown (persistent.lc_title_all_memories). Logic and tuning:
#   python-packages/lc_title_touch.py. Rig: systems/title_customiser.rpy.
#
# Public API (call these from scenes/screens):
#   lc_title_touch(region=None) -> None       button action: react to a click (returns None)
#   screen lc_title_touch_area()              the invisible click area over Leia
#   lc_title_touch_mask()                     her outline at title size (clicks outside pass
#       through)
#   lc_title_face_disp(default_face)          the rig's face layer with reaction swaps
#   lc_title_touch_body(d)                    wrap the body layer in the reaction motion
#   lc_title_touch_chest(d)                   wrap the chest layer in the reaction motion
#   define LC_TITLE_TOUCH_POS                 area position
#   define LC_TITLE_TOUCH_SIZE                area size
#
# Internal (helpers for this file and its screens; do not call from scenes): _lc_tt_face_displayable,
#   _lc_tt_body_fn, _lc_tt_chest_fn, _lc_tt_bubble_fn, _lc_tt_bubble_text
#
# Example:
#   use lc_title_touch_area()      (screens/title_screen.rpy)
#
# Depends on: python-packages/lc_title_touch.py, systems/title_customiser.rpy,
#   systems/lc_breath.rpy, systems/lc_fx.rpy
# Hooks: none
# Load order: default (init 0)
# Docs: docs/TITLE_SCREEN.md   Tests: tests/test_title_leia_touch.py

init python:
    import time as _lc_tt_time
    import random as _lc_tt_random
    import lc_title_touch as _lc_tt

    # Plain (non-rollback) dicts: title-screen only, never saved.
    lc_title_touch_state = _lc_tt.new_state()
    lc_title_touch_live = _lc_tt.new_live()
    _lc_tt_faces = {}

    def _lc_tt_face_displayable(face_id):
        d = _lc_tt_faces.get(face_id)
        if d is None:
            path = next((e[2] for e in LC_TITLE_EXPRESSIONS if e[0] == face_id), None)
            if path is None:
                return None
            d = _lc_tt_faces[face_id] = renpy.displayable(path)
        return d

    def lc_title_face_disp(default_face):
        """The rig's face layer: the Customize face, swapped briefly during a reaction.
        Built once per rig so the breathing and the blink never restart."""
        base = renpy.displayable(default_face)

        def show(st, at):
            face = _lc_tt.current_face(lc_title_touch_live, _lc_tt_time.time())
            d = _lc_tt_face_displayable(face) if face else None
            return (d or base), 0.05
        return DynamicDisplayable(show)

    def _lc_tt_body_fn(trans, st, at):
        live = lc_title_touch_live
        x, y = _lc_tt.body_offset(live["kind"], _lc_tt_time.time() - live["start"])
        trans.xoffset = x
        trans.yoffset = y
        return 0

    def _lc_tt_chest_fn(trans, st, at):
        live = lc_title_touch_live
        trans.yoffset = _lc_tt.chest_offset(live["jiggle"], _lc_tt_time.time() - live["start"])
        return 0

    def lc_title_touch_body(d):
        return Transform(d, function=_lc_tt_body_fn)

    def lc_title_touch_chest(d):
        return Transform(d, function=_lc_tt_chest_fn)

    def _lc_tt_bubble_fn(trans, st, at):
        trans.alpha = _lc_tt.bubble_alpha(lc_title_touch_live, _lc_tt_time.time())
        return 0

    def _lc_tt_bubble_text(st, at):
        return Text(lc_title_touch_live["bubble"] or "", font="fonts/Fredoka-SemiBold.ttf",
                    size=30, color="#ffffff"), 0.1

    def lc_title_touch_mask():
        """Her outline (body, chest, hair) at title size: clicks outside it pass through."""
        o = lc_title_current_outfit()

        def make():
            return Transform(Fixed(o["base"], o["chest"], o["hair"], xysize=_lc_tt.CANVAS),
                             zoom=_lc_tt.TITLE_ZOOM)
        return lc_title_cached(("leia_mask", o["id"]), make)

    def lc_title_touch(region=None):
        """Button action: react to a click on Leia. Returns None (screen actions must)."""
        if region is None:
            mx, my = renpy.get_mouse_pos()
            region = _lc_tt.region_at(*_lc_tt.screen_to_canvas(mx, my))
        now = _lc_tt_time.time()
        reaction = _lc_tt.plan(lc_title_touch_state, region, now, lc_title_show_mature(), _lc_tt_random)
        if not reaction:
            return None
        _lc_tt.apply(lc_title_touch_live, reaction, now)
        # Audio is best-effort here: a missing clip or channel must never pop a
        # traceback on the title screen.
        try:
            voice = reaction["voice"]
            if voice and voice[0] == "sfx":
                lc_sfx(voice[1])
            elif voice and voice[0] == "moan":
                lc_moan_once(voice[1])
            if reaction["lewd"]:
                lc_sfx(reaction["lewd"], reaction["lewd_vol"])
        except Exception as e:
            renpy.log("lc_title_touch audio: %r" % (e,))
        renpy.restart_interaction()
        return None

define LC_TITLE_TOUCH_POS = (int(_lc_tt.TITLE_LEFT), int(_lc_tt.TITLE_TOP))
define LC_TITLE_TOUCH_SIZE = (int(_lc_tt.CANVAS[0] * _lc_tt.TITLE_ZOOM), int(_lc_tt.CANVAS[1] * _lc_tt.TITLE_ZOOM))

transform lc_title_touch_bubble_fade:
    function _lc_tt_bubble_fn

# Click area over Leia (title screen only), plus the "Hey~ hands off!" bubble.
screen lc_title_touch_area():
    button:
        pos LC_TITLE_TOUCH_POS
        xysize LC_TITLE_TOUCH_SIZE
        background None
        hover_background None
        padding (0, 0)
        focus_mask lc_title_touch_mask()
        keyboard_focus False
        alt "Leia"
        action Function(lc_title_touch)
        add Null()
    frame at lc_title_touch_bubble_fade:
        background Frame("gui/title/chip_hover.png", 20, 20)
        padding (26, 14)
        xanchor 1.0
        xpos 1420
        ypos 150
        add DynamicDisplayable(_lc_tt_bubble_text)
