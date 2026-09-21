# Leia — Prologue Party layered sprite.
# Layer order for this outfit, bottom -> top:
# Base -> Chest -> Hands -> Expression -> Hair
#
# Neutral blink sequence:
# Neutral_01 = open
# Neutral_02 = half blink
# Neutral_03 = closed
#
# Only the expression layer animates at this stage. All body layers remain static.

transform leia_prologue_party_neutral_blink:
    "images/sprites/leia/prologue_party/Neutral_01.png"

    block:
        choice:
            pause 2.8
        choice:
            pause 3.6
        choice:
            pause 4.4
        choice:
            pause 5.2
        choice:
            pause 6.0

        "images/sprites/leia/prologue_party/Neutral_02.png"
        pause 0.045
        "images/sprites/leia/prologue_party/Neutral_03.png"
        pause 0.065
        "images/sprites/leia/prologue_party/Neutral_02.png"
        pause 0.045
        "images/sprites/leia/prologue_party/Neutral_01.png"

        repeat


layeredimage leia_prologue_party:

    always "images/sprites/leia/prologue_party/Base.png"
    always "images/sprites/leia/prologue_party/Chest.png"
    always "images/sprites/leia/prologue_party/Hands.png"

    group expression:
        attribute neutral default:
            "leia_prologue_party_neutral_blink"

    always "images/sprites/leia/prologue_party/Hair.png"
