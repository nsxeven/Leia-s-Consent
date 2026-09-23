# Leia layered sprite system — current production artwork.
# Render order, bottom -> top: Base -> Chest -> Expression -> Hair.
# Core Leia assets live directly in images/sprites/leia/.
# Expressions live in images/sprites/leia/expressions/.
# Chapter-specific outfit assets live in their chapter/outfit folders.

# Neutral01/Neutral02 form the automatic two-frame blink loop.
# Every non-neutral expression is static, so switching away from neutral pauses blinking.
image leia_expression_neutral_blink:
    "images/sprites/leia/expressions/Neutral01.png"

    block:
        choice:
            pause 1.8
        choice:
            pause 2.4
        choice:
            pause 3.0
        choice:
            pause 3.6
        choice:
            pause 4.2

        "images/sprites/leia/expressions/Neutral02.png"
        pause 0.105
        "images/sprites/leia/expressions/Neutral01.png"

        repeat


# Whole-sprite breathing envelope retained from the approved old artwork.
# Applied at show-time so every layer remains registered to the same canvas.
transform leia_body_idle:
    yanchor 1.0
    yzoom 1.0

    block:
        # Inhale: the assembled sprite rises slightly from the bottom anchor.
        linear 0.65 yzoom 0.985
        pause 0.10
        # Exhale: return to the neutral body state.
        linear 0.65 yzoom 1.0
        pause 0.10
        repeat


# Chest breathing retained as an independent layer animation so it can be tuned
# without changing the base artwork or whole-body breathing.
transform leia_chest_breathe:
    xzoom 1.0
    xoffset 0

    block:
        # Inhale: expand during the same 0.65 s phase as the body's rise.
        parallel:
            linear 0.65 xzoom 1.04
        parallel:
            linear 0.65 xoffset -18
        pause 0.10
        # Exhale: contract while the body returns to neutral.
        parallel:
            linear 0.65 xzoom 1.0
        parallel:
            linear 0.65 xoffset 0
        pause 0.10
        repeat


# Hair keeps the approved subtle secondary follow-through from the old rig.
transform leia_hair_idle:
    yoffset 0

    block:
        linear 0.65 yoffset 5
        pause 0.10
        linear 0.65 yoffset 0
        pause 0.10
        repeat


layeredimage leia_prologue_party_layers:

    always "images/sprites/leia/PRO/Base_PrologueParty.png"
    always "images/sprites/leia/PRO/Chest_PrologueParty.png" at leia_chest_breathe

    group expression:
        attribute neutral default:
            "leia_expression_neutral_blink"
        attribute smile:
            "images/sprites/leia/expressions/Smile.png"
        attribute shy:
            "images/sprites/leia/expressions/Shy.png"
        attribute pout:
            "images/sprites/leia/expressions/Pout.png"
        attribute flustered:
            "images/sprites/leia/expressions/Flustered.png"
        attribute skeptical:
            "images/sprites/leia/expressions/Skeptical.png"
        attribute angry:
            "images/sprites/leia/expressions/Angry.png"
        attribute ahegao:
            "images/sprites/leia/expressions/Ahegao.png"

    always "images/sprites/leia/Hair.png" at leia_hair_idle



# Character silhouette treatment.
# Flatten() first composites Base + Chest + Expression + Hair into one displayable.
# The dark blurred copy is then placed behind the untouched composite, so internal
# layer boundaries never receive their own outline.
init python:
    def lc_sprite_silhouette(displayable):
        composite = Flatten(displayable)
        # Keep the halo crisp rather than GPU-blurring a continuously changing
        # animated texture. The previous blur pass could shimmer/flicker by a
        # pixel as the breathing transforms were re-rendered between frames.
        # Four sub-pixel-offset dark copies produce a stable soft edge instead.
        dark = Transform(
            composite,
            matrixcolor=BrightnessMatrix(-1.0),
            alpha=0.24,
        )
        halo = Fixed(
            Transform(dark, xoffset=-2, yoffset=0),
            Transform(dark, xoffset=2, yoffset=0),
            Transform(dark, xoffset=0, yoffset=-2),
            Transform(dark, xoffset=0, yoffset=2),
            fit_first=True,
        )
        return Fixed(halo, composite, fit_first=True)

# Public displayables retain the established fixed envelope. Neutral alone uses
# the blink ATL; named expressions remain static until neutral is shown again.
image leia_prologue_party neutral = Fixed(lc_sprite_silhouette("leia_prologue_party_layers neutral"), xysize=(941, 1672))
image leia_prologue_party smile = Fixed(lc_sprite_silhouette("leia_prologue_party_layers smile"), xysize=(941, 1672))
image leia_prologue_party shy = Fixed(lc_sprite_silhouette("leia_prologue_party_layers shy"), xysize=(941, 1672))
image leia_prologue_party pout = Fixed(lc_sprite_silhouette("leia_prologue_party_layers pout"), xysize=(941, 1672))
image leia_prologue_party flustered = Fixed(lc_sprite_silhouette("leia_prologue_party_layers flustered"), xysize=(941, 1672))
image leia_prologue_party skeptical = Fixed(lc_sprite_silhouette("leia_prologue_party_layers skeptical"), xysize=(941, 1672))
image leia_prologue_party angry = Fixed(lc_sprite_silhouette("leia_prologue_party_layers angry"), xysize=(941, 1672))
image leia_prologue_party ahegao = Fixed(lc_sprite_silhouette("leia_prologue_party_layers ahegao"), xysize=(941, 1672))


# Leia — Casual outfit used for the present-day Prologue and early Chapter One.
# Uses the same production rig: Base -> Chest -> Expression -> Hair.
layeredimage leia_casual_layers:

    always "images/sprites/leia/PRO/Base_Casual.png"
    always "images/sprites/leia/PRO/Chest_Casual.png" at leia_chest_breathe

    group expression:
        attribute neutral default:
            "leia_expression_neutral_blink"
        attribute smile:
            "images/sprites/leia/expressions/Smile.png"
        attribute shy:
            "images/sprites/leia/expressions/Shy.png"
        attribute pout:
            "images/sprites/leia/expressions/Pout.png"
        attribute flustered:
            "images/sprites/leia/expressions/Flustered.png"
        attribute skeptical:
            "images/sprites/leia/expressions/Skeptical.png"
        attribute angry:
            "images/sprites/leia/expressions/Angry.png"
        attribute ahegao:
            "images/sprites/leia/expressions/Ahegao.png"

    always "images/sprites/leia/Hair.png" at leia_hair_idle

image leia_casual neutral = Fixed(lc_sprite_silhouette("leia_casual_layers neutral"), xysize=(941, 1672))
image leia_casual smile = Fixed(lc_sprite_silhouette("leia_casual_layers smile"), xysize=(941, 1672))
image leia_casual shy = Fixed(lc_sprite_silhouette("leia_casual_layers shy"), xysize=(941, 1672))
image leia_casual pout = Fixed(lc_sprite_silhouette("leia_casual_layers pout"), xysize=(941, 1672))
image leia_casual flustered = Fixed(lc_sprite_silhouette("leia_casual_layers flustered"), xysize=(941, 1672))
image leia_casual skeptical = Fixed(lc_sprite_silhouette("leia_casual_layers skeptical"), xysize=(941, 1672))
image leia_casual angry = Fixed(lc_sprite_silhouette("leia_casual_layers angry"), xysize=(941, 1672))
image leia_casual ahegao = Fixed(lc_sprite_silhouette("leia_casual_layers ahegao"), xysize=(941, 1672))


# Leia — Chapter One pool outfits.
# Story mapping:
#   pool_conservative -> BlueBikini
#   pool_bolder       -> WhiteRuffle
# Both retain the production Base -> Chest -> Expression -> Hair rig.
layeredimage leia_blue_bikini_layers:

    always "images/sprites/leia/CH1/Base_BlueBikini.png"
    always "images/sprites/leia/CH1/Chest_BlueBikini.png" at leia_chest_breathe

    group expression:
        attribute neutral default:
            "leia_expression_neutral_blink"
        attribute smile:
            "images/sprites/leia/expressions/Smile.png"
        attribute shy:
            "images/sprites/leia/expressions/Shy.png"
        attribute pout:
            "images/sprites/leia/expressions/Pout.png"
        attribute flustered:
            "images/sprites/leia/expressions/Flustered.png"
        attribute skeptical:
            "images/sprites/leia/expressions/Skeptical.png"
        attribute angry:
            "images/sprites/leia/expressions/Angry.png"
        attribute ahegao:
            "images/sprites/leia/expressions/Ahegao.png"

    always "images/sprites/leia/Hair.png" at leia_hair_idle

image leia_blue_bikini neutral = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers neutral"), xysize=(941, 1672))
image leia_blue_bikini smile = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers smile"), xysize=(941, 1672))
image leia_blue_bikini shy = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers shy"), xysize=(941, 1672))
image leia_blue_bikini pout = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers pout"), xysize=(941, 1672))
image leia_blue_bikini flustered = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers flustered"), xysize=(941, 1672))
image leia_blue_bikini skeptical = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers skeptical"), xysize=(941, 1672))
image leia_blue_bikini angry = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers angry"), xysize=(941, 1672))
image leia_blue_bikini ahegao = Fixed(lc_sprite_silhouette("leia_blue_bikini_layers ahegao"), xysize=(941, 1672))

layeredimage leia_white_ruffle_layers:

    always "images/sprites/leia/CH1/Base_WhiteRuffle.png"
    always "images/sprites/leia/CH1/Chest_WhiteRuffle.png" at leia_chest_breathe

    group expression:
        attribute neutral default:
            "leia_expression_neutral_blink"
        attribute smile:
            "images/sprites/leia/expressions/Smile.png"
        attribute shy:
            "images/sprites/leia/expressions/Shy.png"
        attribute pout:
            "images/sprites/leia/expressions/Pout.png"
        attribute flustered:
            "images/sprites/leia/expressions/Flustered.png"
        attribute skeptical:
            "images/sprites/leia/expressions/Skeptical.png"
        attribute angry:
            "images/sprites/leia/expressions/Angry.png"
        attribute ahegao:
            "images/sprites/leia/expressions/Ahegao.png"

    always "images/sprites/leia/Hair.png" at leia_hair_idle

image leia_white_ruffle neutral = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers neutral"), xysize=(941, 1672))
image leia_white_ruffle smile = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers smile"), xysize=(941, 1672))
image leia_white_ruffle shy = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers shy"), xysize=(941, 1672))
image leia_white_ruffle pout = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers pout"), xysize=(941, 1672))
image leia_white_ruffle flustered = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers flustered"), xysize=(941, 1672))
image leia_white_ruffle skeptical = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers skeptical"), xysize=(941, 1672))
image leia_white_ruffle angry = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers angry"), xysize=(941, 1672))
image leia_white_ruffle ahegao = Fixed(lc_sprite_silhouette("leia_white_ruffle_layers ahegao"), xysize=(941, 1672))


# Leia — Chapter One towel outfit.
# The towel/holding-hand artwork is a single animated chest layer over the nude
# base, so it uses the same breathing, expression, hair, silhouette, and fixed
# 941x1672 envelope as the other production outfits.
layeredimage leia_towel_layers:

    always "images/sprites/leia/CH1/Base_Towel.png"
    always "images/sprites/leia/CH1/Chest_Towel.png" at leia_chest_breathe

    group expression:
        attribute neutral default:
            "leia_expression_neutral_blink"
        attribute smile:
            "images/sprites/leia/expressions/Smile.png"
        attribute shy:
            "images/sprites/leia/expressions/Shy.png"
        attribute pout:
            "images/sprites/leia/expressions/Pout.png"
        attribute flustered:
            "images/sprites/leia/expressions/Flustered.png"
        attribute skeptical:
            "images/sprites/leia/expressions/Skeptical.png"
        attribute angry:
            "images/sprites/leia/expressions/Angry.png"
        attribute ahegao:
            "images/sprites/leia/expressions/Ahegao.png"

    always "images/sprites/leia/Hair.png" at leia_hair_idle

image leia_towel neutral = Fixed(lc_sprite_silhouette("leia_towel_layers neutral"), xysize=(941, 1672))
image leia_towel smile = Fixed(lc_sprite_silhouette("leia_towel_layers smile"), xysize=(941, 1672))
image leia_towel shy = Fixed(lc_sprite_silhouette("leia_towel_layers shy"), xysize=(941, 1672))
image leia_towel pout = Fixed(lc_sprite_silhouette("leia_towel_layers pout"), xysize=(941, 1672))
image leia_towel flustered = Fixed(lc_sprite_silhouette("leia_towel_layers flustered"), xysize=(941, 1672))
image leia_towel skeptical = Fixed(lc_sprite_silhouette("leia_towel_layers skeptical"), xysize=(941, 1672))
image leia_towel angry = Fixed(lc_sprite_silhouette("leia_towel_layers angry"), xysize=(941, 1672))
image leia_towel ahegao = Fixed(lc_sprite_silhouette("leia_towel_layers ahegao"), xysize=(941, 1672))
