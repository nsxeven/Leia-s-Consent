# Leia — Prologue Party layered sprite.
# Static reconstruction baseline. ATL animation is added only after this stack is visually verified.
#
# Layer order for this outfit, bottom -> top:
# Base -> Chest -> Hands -> Expression -> Hair

layeredimage leia_prologue_party:

    always "images/sprites/leia/prologue_party/Base.png"
    always "images/sprites/leia/prologue_party/Chest.png"
    always "images/sprites/leia/prologue_party/Hands.png"

    group expression:
        attribute neutral default:
            "images/sprites/leia/prologue_party/Neutral_01.png"

    always "images/sprites/leia/prologue_party/Hair.png"
