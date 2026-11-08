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


# Chapter One Ryan — deliberately plain visual treatment.
# Dressed state: basic white T-shirt + black shorts.
layeredimage ryan_casual_layers:
    always "images/sprites/ryan/Base_Casual.png"
    always "images/sprites/ryan/Chest_Casual.png" at leia_chest_breathe

image ryan_casual = Fixed(lc_sprite_silhouette("ryan_casual_layers"), xysize=(941, 1672))


# Pool / beach state: same black shorts, shirt removed.
layeredimage ryan_pool_layers:
    always "images/sprites/ryan/Base_BlackShorts.png"
    always "images/sprites/ryan/Chest_Nude.png" at leia_chest_breathe

image ryan_pool = Fixed(lc_sprite_silhouette("ryan_pool_layers"), xysize=(941, 1672))


# Home clothes (darryn 2026-11-09): what Ryan changes into upstairs after the
# restaurant on Day 1 (scene 14a) and wears for movie night to the end of the day.
layeredimage ryan_home_layers:
    always "images/sprites/ryan/Base_HomeClothes.png"
    always "images/sprites/ryan/Chest_HomeClothes.png" at leia_chest_breathe

image ryan_home = Fixed(lc_sprite_silhouette("ryan_home_layers"), xysize=(941, 1672))
