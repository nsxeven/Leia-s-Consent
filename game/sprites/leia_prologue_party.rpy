# Leia — Prologue Party layered sprite.
# Layer order for this outfit, bottom -> top:
# Base -> Chest -> Hands -> Expression -> Hair
#
# Shared Leia expressions live one level above outfit-specific assets:
# images/sprites/leia/expressions/
#
# Neutral_01/02/03 form the automatic blink loop.
# All other expressions are static and therefore pause blinking until neutral
# is shown again.

image leia_expression_neutral_blink:
    "images/sprites/leia/expressions/Neutral_01.png"

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

        "images/sprites/leia/expressions/Neutral_02.png"
        pause 0.075
        "images/sprites/leia/expressions/Neutral_03.png"
        pause 0.105
        "images/sprites/leia/expressions/Neutral_02.png"
        pause 0.075
        "images/sprites/leia/expressions/Neutral_01.png"

        repeat


# Primary idle motion for the complete assembled sprite.
# 1.5% bottom-anchored breathing with a brief pause at each end of the breath.
transform leia_body_idle:
    yanchor 1.0
    yzoom 1.0

    block:
        linear 0.65 yzoom 0.985
        pause 0.10
        linear 0.65 yzoom 1.0
        pause 0.10
        repeat


# Chest breathing. Expansion is synchronized with the body's upward/inhalation
# phase. Compensation keeps the manually registered chest layer aligned.
transform leia_chest_breathe:
    xzoom 1.04
    xoffset -18

    block:
        parallel:
            linear 0.65 xzoom 1.0
        parallel:
            linear 0.65 xoffset 0
        pause 0.10
        parallel:
            linear 0.65 xzoom 1.04
        parallel:
            linear 0.65 xoffset -18
        pause 0.10
        repeat


# Hands secondary motion. Keep the approved registered canvas position and
# vertical follow-through values unchanged.
transform leia_hands_idle:
    yoffset -4
    pause 0.08

    block:
        linear 0.65 yoffset 1
        pause 0.10
        linear 0.65 yoffset -4
        pause 0.10
        repeat


# Hair secondary motion. Keep the approved 5 px vertical motion unchanged.
transform leia_hair_idle:
    yoffset 0

    block:
        linear 0.65 yoffset 5
        pause 0.10
        linear 0.65 yoffset 0
        pause 0.10
        repeat


layeredimage leia_prologue_party_layers:

    always "images/sprites/leia/prologue_party/Base.png"
    always "images/sprites/leia/prologue_party/Chest.png" at leia_chest_breathe
    always "images/sprites/leia/prologue_party/Hands.png" at leia_hands_idle

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

    always "images/sprites/leia/prologue_party/Hair.png" at leia_hair_idle


# Public Leia displayables. Each expression keeps invariant 941x1672 bounds,
# so expression swaps cannot disturb screen placement. Only neutral references
# the blinking ATL image; every named expression is static.
image leia_prologue_party neutral = Fixed(
    "leia_prologue_party_layers neutral",
    xysize=(941, 1672),
)

image leia_prologue_party smile = Fixed(
    "leia_prologue_party_layers smile",
    xysize=(941, 1672),
)

image leia_prologue_party shy = Fixed(
    "leia_prologue_party_layers shy",
    xysize=(941, 1672),
)

image leia_prologue_party pout = Fixed(
    "leia_prologue_party_layers pout",
    xysize=(941, 1672),
)

image leia_prologue_party flustered = Fixed(
    "leia_prologue_party_layers flustered",
    xysize=(941, 1672),
)

image leia_prologue_party skeptical = Fixed(
    "leia_prologue_party_layers skeptical",
    xysize=(941, 1672),
)


# Leia — Outfit 02 layered sprite.
# Reuses the approved shared expression, hand, and hair layers. Body motion
# follows the same timing as the Prologue Party outfit, while the chest layer
# has its own transform so registration can be tuned independently.

transform leia_outfit02_chest_breathe:
    xzoom 1.04
    xoffset -18

    block:
        parallel:
            linear 0.65 xzoom 1.0
        parallel:
            linear 0.65 xoffset 0
        pause 0.10
        parallel:
            linear 0.65 xzoom 1.04
        parallel:
            linear 0.65 xoffset -18
        pause 0.10
        repeat


layeredimage leia_outfit02_layers:

    always "images/sprites/leia/prologue_party/Base_02.png"
    always "images/sprites/leia/prologue_party/Chest_02.png" at leia_outfit02_chest_breathe
    always "images/sprites/leia/prologue_party/Hands.png" at leia_hands_idle

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

    always "images/sprites/leia/prologue_party/Hair.png" at leia_hair_idle


image leia_outfit02 neutral = Fixed(
    "leia_outfit02_layers neutral",
    xysize=(941, 1672),
)

image leia_outfit02 smile = Fixed(
    "leia_outfit02_layers smile",
    xysize=(941, 1672),
)

image leia_outfit02 shy = Fixed(
    "leia_outfit02_layers shy",
    xysize=(941, 1672),
)

image leia_outfit02 pout = Fixed(
    "leia_outfit02_layers pout",
    xysize=(941, 1672),
)

image leia_outfit02 flustered = Fixed(
    "leia_outfit02_layers flustered",
    xysize=(941, 1672),
)

image leia_outfit02 skeptical = Fixed(
    "leia_outfit02_layers skeptical",
    xysize=(941, 1672),
)
