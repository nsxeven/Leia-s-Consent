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

    always "images/sprites/leia/prologue_party/Base_PrologueParty.png"
    always "images/sprites/leia/prologue_party/Chest_PrologueParty.png" at leia_chest_breathe

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


# Public displayables retain the established fixed envelope. Neutral alone uses
# the blink ATL; named expressions remain static until neutral is shown again.
image leia_prologue_party neutral = Fixed("leia_prologue_party_layers neutral", xysize=(941, 1672))
image leia_prologue_party smile = Fixed("leia_prologue_party_layers smile", xysize=(941, 1672))
image leia_prologue_party shy = Fixed("leia_prologue_party_layers shy", xysize=(941, 1672))
image leia_prologue_party pout = Fixed("leia_prologue_party_layers pout", xysize=(941, 1672))
image leia_prologue_party flustered = Fixed("leia_prologue_party_layers flustered", xysize=(941, 1672))
image leia_prologue_party skeptical = Fixed("leia_prologue_party_layers skeptical", xysize=(941, 1672))
image leia_prologue_party angry = Fixed("leia_prologue_party_layers angry", xysize=(941, 1672))
image leia_prologue_party ahegao = Fixed("leia_prologue_party_layers ahegao", xysize=(941, 1672))


# Leia — Casual outfit used for the present-day Prologue and early Chapter One.
# Uses the same production rig: Base -> Chest -> Expression -> Hair.
layeredimage leia_casual_layers:

    always "images/sprites/leia/prologue_party/Base_Casual.png"
    always "images/sprites/leia/prologue_party/Chest_Casual.png" at leia_chest_breathe

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

image leia_casual neutral = Fixed("leia_casual_layers neutral", xysize=(941, 1672))
image leia_casual smile = Fixed("leia_casual_layers smile", xysize=(941, 1672))
image leia_casual shy = Fixed("leia_casual_layers shy", xysize=(941, 1672))
image leia_casual pout = Fixed("leia_casual_layers pout", xysize=(941, 1672))
image leia_casual flustered = Fixed("leia_casual_layers flustered", xysize=(941, 1672))
image leia_casual skeptical = Fixed("leia_casual_layers skeptical", xysize=(941, 1672))
image leia_casual angry = Fixed("leia_casual_layers angry", xysize=(941, 1672))
image leia_casual ahegao = Fixed("leia_casual_layers ahegao", xysize=(941, 1672))
