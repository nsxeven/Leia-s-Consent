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

# --- Sprite height (whole game) ---------------------------------------------
# One place for how high every dialogue sprite stands. The dialogue box spans
# y=792..1014. At -80 the 900px envelope's bottom (feet) sits at y=1000, tucked
# behind the box, while the knees (~72% down) land at about y=750, above it.
# Entering sprites start 14px lower (feet still hidden) and ease up.
define lc_sprite_yoffset = -80
define lc_sprite_enter_yoffset = -66

# --- Leia (always RIGHT) --------------------------------------------------
transform leia_enter_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_enter_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset lc_sprite_yoffset

transform leia_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    # Full opacity, always: a sprite re-shown mid-entrance (fast clicks,
    # skip, expression change) must not keep the half-faded alpha.
    alpha 1.0

# --- Other speakers (always LEFT) -----------------------------------------
transform other_enter_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_enter_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset lc_sprite_yoffset

transform other_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    # Full opacity, always: a sprite re-shown mid-entrance (fast clicks,
    # skip, expression change) must not keep the half-faded alpha.
    alpha 1.0

# Backward-compatible aliases (existing scripts use the prologue_ names).
# Prefer the short names above in new code.
# Ren'Py does not support transform alias = other_transform, so these are full copies.
transform prologue_leia_enter_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_enter_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset lc_sprite_yoffset

transform prologue_leia_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom -1.0
    # Full opacity, always: a sprite re-shown mid-entrance (fast clicks,
    # skip, expression change) must not keep the half-faded alpha.
    alpha 1.0

transform prologue_other_enter_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_enter_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    alpha 0.0
    parallel:
        linear 0.30 alpha 1.0
    parallel:
        easeout 0.30 yoffset lc_sprite_yoffset

transform prologue_other_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    yoffset lc_sprite_yoffset
    xysize (760, 900)
    fit "contain"
    xzoom 1.0
    # Full opacity, always: a sprite re-shown mid-entrance (fast clicks,
    # skip, expression change) must not keep the half-faded alpha.
    alpha 1.0
