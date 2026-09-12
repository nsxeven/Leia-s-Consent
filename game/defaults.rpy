# Save-game state defaults.
# These values belong to an individual playthrough unless marked persistent.

default player_name = "Ryan"
default girlfriend_name = "Leia"
default friend_name = "Julian"

# Economy.
default money = 500
default last_money_change = 0
default last_money_reason = ""

# Wardrobe state. Static outfit definitions live in systems/outfits_data.rpy.
default owned_outfits = ["casual_default"]
default equipped_outfit = "casual_default"
default last_wear_route = "default_comfort"
default last_shop_message = ""
default last_wardrobe_message = ""

# Leia sprite state. Outfit remains controlled by equipped_outfit above.
default leia_pose = "p01"
default leia_expression = "neutral"

# Development-only test flag so the wardrobe allowance is not repeatedly granted.
default dev_wardrobe_reward_claimed = False

default relationship_stats = {
    "love": 50,
    "trust": 50,
    "boredom": 10,
    "momentum": 0,
}

default partner_stats = {
    "curiosity": 20,
    "temptation": 10,
    "exhibitionism": 10,
    "boundary_looseness": 10,
    "secrecy": 5,
}

default player_stats = {
    "jealousy": 20,
    "acceptance": 10,
}

default modified_save = False

# Choice audit trail for debugging and future route logic.
default choice_history = []
default last_choice_id = None

# Player preference: survives across save slots and new games.
default persistent.choice_display_mode = "normal"
