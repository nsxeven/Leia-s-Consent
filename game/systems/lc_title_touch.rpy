# Title-screen Leia: touch reactions (darryn 2026-11-09).
# Click her for a voice clip, a small motion and a brief expression; she then
# settles back to the face picked in Customize. Chest/private-area clicks escalate
# and only turn lewd (moans, wet sounds, chest jiggle) when 18+ options are shown
# (persistent.lc_title_all_memories, same rule as the Ahegao face). Logic and
# tuning: python-packages/lc_title_touch.py. Rig wiring: lc_title_leia_rig in
# systems/title_customiser.rpy. Click area + bubble: screens/title_screen.rpy.

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
