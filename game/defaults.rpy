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


# Generic story state. Flags are booleans; values hold resolved outcomes or other story data.
default story_flags = {}
default story_values = {}

# Development-only test flags so sandbox allowances are not repeatedly granted.
default dev_wardrobe_reward_claimed = False
default dev_vertical_slice_reward_claimed = False

# Stat model v2 (python-packages/lc_stat_model.py): Love, Trust, Sharing and
# Temptation live in relationship_stats, Exhibitionism in partner_stats.
# player_stats stays as an empty group so old code paths and saves keep loading.
# Older saves are converted once on load (lc_migrate_stats_v2 in systems/stats.rpy).
default relationship_stats = {
    "love": 50,
    "trust": 50,
    "sharing": 0,
    "temptation": 10,
}

default partner_stats = {
    "exhibitionism": 10,
}

default player_stats = {}

default lc_stat_model_version = 2
default lc_legacy_stats = None

default modified_save = False

# Choice audit trail for debugging and future route logic.
default choice_history = []
default last_choice_id = None

# Player preferences/unlocks: survive across save slots and new games.
default persistent.choice_display_mode = "normal"
default persistent.full_transparency_notice_seen = False
default persistent.gallery_unlocked = []

# Chapter Select (see systems/chapter_select.rpy).
default persistent.ch01_chapter_select_unlocked = False
default persistent.ch01_chapter_select_pending = None
