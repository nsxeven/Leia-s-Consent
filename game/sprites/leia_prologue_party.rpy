# Leia — Prologue Party layered sprite.
# Layer order for this outfit, bottom -> top:
# Base -> Chest -> Hands -> Expression -> Hair
#
# Expression source files keep their reusable asset names:
# Neutral_01 = open
# Neutral_02 = half blink
# Neutral_03 = closed
#
# The assembled sprite uses a bottom-anchored whole-body idle.
# Individual body-layer secondary motion is added only after this parent motion passes QA.

image leia_expression_neutral_blink:
    "images/sprites/leia/prologue_party/Neutral_01.png"

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

        "images/sprites/leia/prologue_party/Neutral_02.png"
        pause 0.075
        "images/sprites/leia/prologue_party/Neutral_03.png"
        pause 0.105
        "images/sprites/leia/prologue_party/Neutral_02.png"
        pause 0.075
        "images/sprites/leia/prologue_party/Neutral_01.png"

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


layeredimage leia_prologue_party:

    always "images/sprites/leia/prologue_party/Base.png"
    always "images/sprites/leia/prologue_party/Chest.png"
    always "images/sprites/leia/prologue_party/Hands.png"

    group expression:
        attribute neutral default:
            "leia_expression_neutral_blink"

    always "images/sprites/leia/prologue_party/Hair.png"
