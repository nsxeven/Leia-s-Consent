# Player-facing presentation helpers for Wardrobe and Outfit Shop.
# Mechanical rules stay in wardrobe_logic.rpy; this file only formats UI information.

init python:

    OUTFIT_CATEGORY_LABELS = {
        "casual": "Casual",
        "date": "Date",
        "bold": "Bold",
    }


    def outfit_category_label(outfit_id):
        outfit = get_outfit(outfit_id)
        category = outfit.get("category", "other")
        return OUTFIT_CATEGORY_LABELS.get(category, category.replace("_", " ").title())


    def outfit_context_text(outfit_id):
        contexts = get_outfit(outfit_id).get("contexts", ())
        if not contexts:
            return "General"
        return " • ".join(context.replace("_", " ").title() for context in contexts)


    def outfit_style_rows(outfit_id):
        outfit = get_outfit(outfit_id)
        return (
            ("Boldness", clamp_stat(outfit.get("boldness", 0))),
            ("Comfort", clamp_stat(outfit.get("comfort", 0))),
            ("Playfulness", clamp_stat(outfit.get("playfulness", 0))),
            ("Elegance", clamp_stat(outfit.get("elegance", 0))),
        )


    def outfit_status_short(outfit_id):
        if renpy.store.equipped_outfit == outfit_id:
            return "Wearing now"
        if can_wear(outfit_id):
            return "Ready to wear"
        return "Not comfortable yet"


    def outfit_status_color(outfit_id):
        if renpy.store.equipped_outfit == outfit_id:
            return "#f1a8c8"
        if can_wear(outfit_id):
            return "#b9d7bd"
        return "#d8b9a6"


    def outfit_comfort_note(outfit_id):
        if renpy.store.equipped_outfit == outfit_id:
            return "{} is currently wearing this outfit.".format(renpy.store.girlfriend_name)
        if can_wear(outfit_id):
            return "{} is comfortable wearing this outfit right now.".format(renpy.store.girlfriend_name)
        return "{} owns this outfit, but isn't comfortable wearing it yet.".format(renpy.store.girlfriend_name)


    def shop_item_state(outfit_id):
        if owns_outfit(outfit_id):
            return "owned"
        if not is_shop_unlocked(outfit_id):
            return "locked"
        if not can_afford(get_outfit(outfit_id)["cost"]):
            return "insufficient"
        return "available"


    def shop_item_status_label(outfit_id):
        state = shop_item_state(outfit_id)
        if state == "owned":
            return "OWNED"
        if state == "locked":
            return "LOCKED"
        if state == "insufficient":
            return "NEED MORE FUNDS"
        return "AVAILABLE"


    def shop_item_status_color(outfit_id):
        state = shop_item_state(outfit_id)
        if state == "owned":
            return "#b9d7bd"
        if state == "available":
            return "#f1a8c8"
        return "#b8a8b5"
