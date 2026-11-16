# Dialogue staging - sprite height and the LEFT/RIGHT placement transforms
#
# Purpose: Source of truth for where dialogue sprites stand: one height for the whole game
#   (lc_sprite_yoffset) and the enter/stay transforms for the right (Leia) and left (other speaker)
#   slots, plus the prologue variants. Who goes in which slot is decided by
#   systems/cast_staging.rpy.
#
# Public API (call these from scenes/screens):
#   define lc_sprite_yoffset                  y offset of every dialogue sprite (feet hidden behind
#       the box)
#   define lc_sprite_enter_yoffset            start offset of an entering sprite
#   transform leia_enter_right                RIGHT slot entrance
#   transform leia_right                      RIGHT slot
#   transform other_enter_left                LEFT slot entrance
#   transform other_left                      LEFT slot
#   transform prologue_leia_enter_right       prologue RIGHT entrance
#   transform prologue_leia_right             prologue RIGHT
#   transform prologue_other_enter_left       prologue LEFT entrance
#   transform prologue_other_left             prologue LEFT
#
# Example:
#   $ cast(ryan="pool", julian="pool")   (cast_staging picks these transforms; scenes do not name them)
#
# Depends on: nothing
# Hooks: none
# Load order: default (define/transform at init 0)
# Docs: docs/SPRITE_STAGING.md   Tests: tests/test_cast_staging.py

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
