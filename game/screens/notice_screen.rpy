# Things Ryan noticed screens - the eye cue, the push-in viewer and the Status pins
#
# Purpose: The overlay eye cue on a CG (systems/notice.rpy decides when it may show), the
#   full-screen push-in viewer with Ryan's captions in the dialogue-box spot, and the "Things I
#   noticed" pin row in the phone Status app. Immersive/Insight: a cream eye that blinks now and
#   then over the warm Hidden POV glow; Full/Developer: a honey disc with a white eye (Developer
#   adds the id). Hover and keyboard/gamepad focus share the pink hover state. The push-in eases
#   in, the captions fade up, and a click (or Esc / right click / Space / Enter) eases back
#   before closing; reduced motion makes both instant (opening stops Skip, so the push-in then
#   plays normally). The caption paper sits in the dialogue-box spot, the top spot, or a
#   registration's own caption_box (stretched sideways only).
#
# Public API (call these from scenes/screens):
#   screen lc_notice_hotspot()                overlay with the eye cue (desktop and touch variants)
#   screen lc_notice_hotspot_body(size)       the cue button in a size x size hit square
#   screen lc_notice_viewer(notice_id)        the push-in viewer (shown by lc_notice_open)
#   screen lc_phone_notice_pins(pins)         "Things I noticed": one fixed-height row of pins
#       that scrolls sideways (used by lc_phone_status in screens/phone_sweetheart.rpy)
#   transform lc_notice_push(xa, ya, z, t)    push-in from the full frame to the focus
#   transform lc_notice_pull(xa, ya, z, t)    ease back from the focus to the full frame
#   transform lc_notice_fade_in(delay, t)     captions / close-up fade in after delay
#   transform lc_notice_blink                 the idle eye's occasional blink
#
# Internal (helpers for this file and its screens; do not call from scenes): lc_notice_cue_art,
#   lc_notice_pin_thumb
#
# Example:
#   $ renpy.show_screen("lc_notice_viewer", notice_id="d2_notice_bed_hand")   (lc_notice_open)
#   use lc_phone_notice_pins(lc_notice_pins())                                 (Status app)
#
# Depends on: systems/notice.rpy, systems/hidden_pov.rpy (glow art, lc_pov_hover_pop,
#   lc_pov_glow_breathe, lc_pov_static, lc_pov_reduce_motion), python-packages/lc_notice.py,
#   screens/scrapbook_ui.rpy (lc_say_cg_* boxes), screens/phone_sweetheart.rpy (lc_sw_* styles,
#   LC_PHONE_CONTENT_WIDTH), systems/choice_engine.rpy (current_choice_mode)
# Hooks: none
# Load order: default (screens at init -500; the art helpers at init 0)
# Docs: docs/NOTICES.md   Tests: tests/test_notice.py

transform lc_notice_push(xa, ya, z, t):
    subpixel True
    xalign xa yalign ya zoom 1.0
    ease t zoom z

transform lc_notice_pull(xa, ya, z, t):
    subpixel True
    xalign xa yalign ya zoom z
    ease t zoom 1.0

transform lc_notice_fade_in(delay, t):
    alpha 0.0
    pause delay
    ease t alpha 1.0

transform lc_notice_blink:
    subpixel True
    yzoom 1.0
    pause 2.8
    easein 0.07 yzoom 0.15
    easeout 0.12 yzoom 1.0
    pause 0.4
    repeat

init python:
    _lc_notice_art_cache = {}
    # The eye art is 72 px; drawn a little larger so it reads on busy CGs (playtest frame).
    LC_NOTICE_EYE_ZOOM = 1.3

    def lc_notice_cue_art(size, hover=False, still=False, disc=False):
        """Centred eye cue art filling a size x size hit area (cached per state, so a screen
        refresh never restarts the blink). still=True: no blink or pulse (reduced motion)."""
        key = (size, bool(hover), bool(still), bool(disc))
        if key in _lc_notice_art_cache:
            return _lc_notice_art_cache[key]
        layers = []
        if disc:
            face = "gui/notice/eye_disc_hover.svg" if hover else "gui/notice/eye_disc_idle.svg"
        else:
            glow = "gui/pov/glow_hover.svg" if hover else "gui/pov/glow_idle.svg"
            glow_t = (lc_pov_static(1.0, 1.0) if still else lc_pov_hover_pop) if hover else \
                (lc_pov_static(0.95, 1.0) if still else lc_pov_glow_breathe)
            layers.append(Transform(glow_t(Transform(glow, zoom=1.15)), xalign=0.5, yalign=0.5))
            face = "gui/notice/eye_hover.svg" if hover else "gui/notice/eye_idle.svg"
        face = Transform(face, zoom=LC_NOTICE_EYE_ZOOM)
        if hover:
            face_d = lc_pov_static(1.0, 1.1)(face) if still else lc_pov_hover_pop(face)
        else:
            face_d = face if still else lc_notice_blink(face)
        layers.append(Transform(face_d, xalign=0.5, yalign=0.5))
        art = Fixed(*layers, xysize=(size, size))
        _lc_notice_art_cache[key] = art
        return art

    def lc_notice_pin_thumb(pin, width, height):
        """The noticed detail, cropped from the CG (or the whole close-up render)."""
        if pin.get("closeup"):
            return Transform(pin["closeup"], xysize=(width, height), fit="cover")
        crop = lc_notice.thumb_crop(pin["focus_rect"], width, height)
        art = Transform(pin["source"], xysize=(1920, 1080))
        return Transform(art, crop=crop, xysize=(width, height))

screen lc_notice_hotspot():
    zorder 105
    use lc_notice_hotspot_body(LC_NOTICE_HITBOX)

screen lc_notice_hotspot():
    variant "touch"
    zorder 105
    use lc_notice_hotspot_body(LC_NOTICE_HITBOX_TOUCH)

screen lc_notice_hotspot_body(size):
    if lc_notice_available():
        $ notice_id = lc_notice_active
        $ entry = LC_NOTICES[notice_id]
        $ mode = current_choice_mode()
        $ px, py, _w, _h = lc_notice.hit_rect(entry["center"], size)
        $ still = lc_pov_reduce_motion()
        $ disc = mode in ("full", "developer")
        $ cue_label = lc_notice.fill_names(entry["label"] or lc_notice.DEFAULT_LABEL, _lc_notice_names())
        button:
            xpos px
            ypos py
            xysize (size, size)
            background lc_notice_cue_art(size, False, still, disc)
            hover_background lc_notice_cue_art(size, True, still, disc)
            focus_mask None
            alt ("Something you noticed: " + cue_label.replace("[", "[["))  # plain string: self-voicing reads alt outside the screen scope
            action Function(lc_notice_open, notice_id)
            hovered Function(lc_notice_hover_sound)
        if mode == "developer":
            $ label_right = px + size + 4 + 260 <= config.screen_width
            text "[notice_id]":
                xpos ((px + size + 4) if label_right else (px - 4))
                xanchor (0.0 if label_right else 1.0)
                ypos (py + size // 2 - 12)
                size 20 color "#ffdb82" outlines [(2, "#231019", 0, 0)]

screen lc_notice_viewer(notice_id):
    modal True
    # Above the phone notification banner (620), like the Hidden POV viewer.
    zorder 630
    default closing = False
    $ entry = LC_NOTICES.get(notice_id)
    $ instant = lc_notice_instant()
    $ dismiss = Function(lc_notice_close) if instant else SetScreenVariable("closing", True)
    key "K_ESCAPE" action dismiss
    key "game_menu" action dismiss
    key "mouseup_3" action dismiss
    key "dismiss" action dismiss
    if closing:
        timer LC_NOTICE_OUT action Function(lc_notice_close)
    add Solid("#110c12")
    if entry and lc_notice_active == notice_id and lc_notice_in_scope(notice_id):
        $ xa, ya, z = lc_notice_focus(notice_id)
        $ art = Transform(entry["source"], xysize=(1920, 1080))
        if instant:
            add art at Transform(xalign=xa, yalign=ya, zoom=z)
        elif closing:
            add art at lc_notice_pull(xa, ya, z, LC_NOTICE_OUT)
        else:
            add art at lc_notice_push(xa, ya, z, LC_NOTICE_IN)
        if entry["closeup"] and not closing:
            if instant:
                add Transform(entry["closeup"], xysize=(1920, 1080))
            else:
                add Transform(entry["closeup"], xysize=(1920, 1080)) at lc_notice_fade_in(0.15, 0.35)
    # The full-screen click target eases back. keyboard_focus False, so keyboard/gamepad focus
    # stays on the Back button instead of landing on an invisible button.
    button:
        xfill True
        yfill True
        background None
        keyboard_focus False
        action dismiss
    if entry and not closing:
        $ theme = store.lc_dialogue_theme if store.lc_dialogue_theme in ("day", "night") else "day"
        $ ink = "#ece2f2" if theme == "night" else "#34242c"
        $ halo = "#1e1628c0" if theme == "night" else "#efe4cdc0"
        $ caption = "\n".join(lc_notice_captions(notice_id, lc_noticed_record.get(notice_id) if notice_id in lc_noticed_record else "current"))
        $ box_x, box_y, box_w, box_h = lc_notice_caption_box(notice_id)
        frame:
            at (Transform() if instant else lc_notice_fade_in(LC_NOTICE_IN * 0.7, 0.3))
            xpos box_x
            ypos box_y
            xsize box_w
            ysize box_h
            # The dialogue paper, stretched sideways only (left border keeps the margin line).
            background Frame(("lc_say_cg_%s" % theme), 96, 0, 24, 0)
            padding ((84, 28, 72, 18) if box_w >= lc_notice.CAPTION_W else (84, 20, 48, 12))
            text caption:
                substitute False
                font "fonts/PatrickHand-Regular.ttf"
                # A narrower caption_box keeps two captions to 4 lines with a smaller hand.
                size (40 if box_w >= lc_notice.CAPTION_W else 34)
                italic True
                color ink
                line_spacing 6
                outlines [(2, halo, 0, 0)]
                yalign 0.4
        textbutton "Back":
            xpos 1640 ypos 32
            xsize 230 ysize 64
            text_size 32
            alt "Back to the scene"
            action dismiss

screen lc_phone_notice_pins(pins):
    $ _row_w = LC_PHONE_CONTENT_WIDTH - 28
    $ _layout = lc_notice.pin_layout(len(pins), _row_w)
    frame:
        style "lc_sw_frame"
        xfill True
        background Frame("gui/phone/sprite_match/card.png", 18, 18)
        padding (14, 12)
        vbox:
            spacing 10
            xfill True
            text "Things I noticed":
                style "lc_sw_hand"
                size 20
                color "#6E8399"
            # ONE row of fixed height at any count (lc_notice.pin_layout); extra pins scroll
            # sideways (wheel when the row can move, or drag), never wrap.
            viewport:
                xsize _row_w
                ysize lc_notice.PIN_H
                mousewheel ("horizontal-change" if _layout["overflow"] else False)
                draggable _layout["overflow"]
                hbox:
                    spacing lc_notice.PIN_GAP
                    for pin in pins:
                        frame:
                            xsize lc_notice.PIN_W
                            ysize lc_notice.PIN_H
                            background Frame("gui/phone/sprite_match/card.png", 18, 18)
                            padding (8, 8)
                            vbox:
                                spacing 6
                                add lc_notice_pin_thumb(pin, lc_notice.PIN_W - 16, lc_notice.PIN_THUMB_H)
                                text pin["label"]:
                                    substitute False
                                    style "lc_sw_hand"
                                    size 22
                                    color "#293C53"
                                text pin["lines"][0]:
                                    substitute False
                                    style "lc_sw_hand"
                                    size 18
                                    italic True
                                    color "#6E8399"
                                    xmaximum (lc_notice.PIN_W - 16)
