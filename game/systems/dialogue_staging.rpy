# Leia's Consent — Canonical Dialogue Staging
# Source of truth for sprite positions. Reuse these transforms everywhere.
# Rule (from Asset Production Blueprint):
#   - Leia always RIGHT.
#   - Other active speakers LEFT.
#   - Face inward.
#   - Do not pop characters in/out unnecessarily during immediate exchanges.
#
# Envelope: 760x900 dialogue sprites, explicit xpos/xanchor so placement
# is independent of source canvas size.

# --- Leia (always RIGHT) --------------------------------------------------
transform leia_enter_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset 198
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 180

transform leia_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset 180
    xysize (760, 900)
    fit "contain"
    xzoom -1.0

# --- Other speakers (always LEFT) -----------------------------------------
transform other_enter_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset 198
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 180

transform other_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset 180
    xysize (760, 900)
    fit "contain"
    xzoom 1.0

# Backward-compatible aliases (existing scripts use the prologue_ names).
# Prefer the short names above in new code.
# Ren'Py does not support transform alias = other_transform, so these are full copies.
transform prologue_leia_enter_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset 198
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 180

transform prologue_leia_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset 180
    xysize (760, 900)
    fit "contain"
    xzoom -1.0

transform prologue_other_enter_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset 198
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset 180

transform prologue_other_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset 180
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
