# Static outfit definitions.
# These are game rules/content metadata, not save-state values.

init python:

    OUTFIT_SHOP_ORDER = (
        "date_night_dress",
        "after_hours_dress",
    )

    OUTFIT_DEFINITIONS = {
        "casual_default": {
            "name": "Everyday Casual",
            "category": "casual",
            "description": "Leia's default everyday outfit.",
            "cost": 0,
            "shop_visible": False,
            "shop_requirements": [],
            "boldness": 10,
            "exposure": 10,
            "public_risk": 5,
            "comfort": 90,
            "playfulness": 20,
            "elegance": 25,
            "contexts": ("home", "casual", "day"),
            "asset_id": "leia_outfit_casual_default",
            "wear_paths": [
                {
                    "id": "default_comfort",
                    "label": "Default comfort",
                    "requirements": [],
                },
            ],
        },

        "date_night_dress": {
            "name": "Date Night Dress",
            "category": "date",
            "description": "A polished date outfit that Leia is already comfortable wearing.",
            "cost": 180,
            "shop_visible": True,
            "shop_requirements": [],
            "boldness": 30,
            "exposure": 25,
            "public_risk": 15,
            "comfort": 70,
            "playfulness": 35,
            "elegance": 80,
            "contexts": ("date", "restaurant", "evening"),
            "asset_id": "leia_outfit_date_night_dress",
            "wear_paths": [
                {
                    "id": "normal_comfort",
                    "label": "Normal comfort",
                    "requirements": [],
                },
            ],
        },

        "after_hours_dress": {
            "name": "After Hours Dress",
            "category": "bold",
            "description": "A noticeably bolder outfit. Buying it does not mean Leia is ready to wear it.",
            "cost": 350,
            "shop_visible": True,
            "shop_requirements": [],
            "boldness": 80,
            "exposure": 70,
            "public_risk": 65,
            "comfort": 25,
            "playfulness": 75,
            "elegance": 65,
            "contexts": ("nightlife", "party", "evening"),
            "asset_id": "leia_outfit_after_hours_dress",
            "wear_paths": [
                {
                    "id": "confident_exhibitionist",
                    "label": "Confidence / exhibitionism",
                    "requirements": [
                        ("partner", "curiosity", 30),
                        ("partner", "exhibitionism", 20),
                    ],
                },
                {
                    "id": "romantic_trust",
                    "label": "Trust / consensual encouragement",
                    "requirements": [
                        ("relationship", "love", 60),
                        ("relationship", "trust", 60),
                        ("player", "acceptance", 20),
                        ("partner", "curiosity", 25),
                    ],
                },
                {
                    "id": "risky_temptation",
                    "label": "Risk / temptation",
                    "requirements": [
                        ("relationship", "boredom", 25),
                        ("partner", "temptation", 25),
                        ("partner", "boundary_looseness", 20),
                    ],
                },
            ],
        },
    }
