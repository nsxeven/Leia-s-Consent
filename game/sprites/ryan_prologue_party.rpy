# Ryan layered sprite system — Prologue party outfit.
# Production artwork uses the same fixed 864x1536 source canvas as Leia.
# Render order, bottom -> top: Base -> Chest.
#
# Ryan is intentionally expressionless for now because only the approved Base
# and Chest party layers exist. Additional face/hair layers can be added later
# without changing the Prologue placement contract.

layeredimage ryan_prologue_party_layers:

    always "images/sprites/ryan/PRO/Base_Party.png"
    always "images/sprites/ryan/PRO/Chest_Party.png" at leia_chest_breathe


# Reuse the stable production silhouette treatment and breathing envelope.
image ryan_prologue_party = Fixed(lc_sprite_silhouette("ryan_prologue_party_layers"), xysize=(941, 1672))
