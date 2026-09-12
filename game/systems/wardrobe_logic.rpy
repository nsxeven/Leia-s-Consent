# Wardrobe ownership, purchase validation, and route-based wear acceptance.
# Buying an outfit and Leia agreeing to wear it are deliberately separate states.

init python:

    def get_outfit(outfit_id):
        """Return one static outfit definition."""
        if outfit_id not in OUTFIT_DEFINITIONS:
            raise ValueError("Unknown outfit ID: {}".format(outfit_id))
        return OUTFIT_DEFINITIONS[outfit_id]


    def outfit_name(outfit_id):
        return get_outfit(outfit_id)["name"]


    def shop_outfit_ids():
        """Return shop-visible outfits in a stable display order."""
        return [
            outfit_id for outfit_id in OUTFIT_SHOP_ORDER
            if outfit_id in OUTFIT_DEFINITIONS and OUTFIT_DEFINITIONS[outfit_id].get("shop_visible", False)
        ]


    def valid_owned_outfit_ids():
        """Ignore stale IDs gracefully if definitions change during development."""
        return [outfit_id for outfit_id in renpy.store.owned_outfits if outfit_id in OUTFIT_DEFINITIONS]


    def owns_outfit(outfit_id):
        return outfit_id in renpy.store.owned_outfits


    def _requirement_value(group_name, stat_name):
        return get_stat_group(group_name)[stat_name]


    def _requirements_met(requirements):
        for group_name, stat_name, minimum in requirements:
            if _requirement_value(group_name, stat_name) < minimum:
                return False
        return True


    def is_shop_unlocked(outfit_id):
        """Shop visibility/unlock is separate from wear acceptance."""
        outfit = get_outfit(outfit_id)
        if not outfit.get("shop_visible", False):
            return False
        return _requirements_met(outfit.get("shop_requirements", []))


    def purchase_outfit(outfit_id):
        """Buy an outfit if visible, unlocked, not owned, and affordable."""
        outfit = get_outfit(outfit_id)

        if owns_outfit(outfit_id):
            renpy.store.last_shop_message = "{} is already owned.".format(outfit["name"])
            renpy.restart_interaction()
            return False

        if not is_shop_unlocked(outfit_id):
            renpy.store.last_shop_message = "{} is not available in the shop yet.".format(outfit["name"])
            renpy.restart_interaction()
            return False

        cost = outfit["cost"]
        if not spend_money(cost, "Bought {}".format(outfit["name"])):
            renpy.store.last_shop_message = "Not enough money for {}. Need ${}.".format(outfit["name"], cost)
            renpy.restart_interaction()
            return False

        renpy.store.owned_outfits.append(outfit_id)
        renpy.store.last_shop_message = "Purchased {} for ${}.".format(outfit["name"], cost)
        renpy.restart_interaction()
        return True


    def passing_wear_path(outfit_id):
        """Return the first wear path currently satisfied, or None."""
        outfit = get_outfit(outfit_id)
        for path in outfit.get("wear_paths", []):
            if _requirements_met(path.get("requirements", [])):
                return path
        return None


    def can_wear(outfit_id):
        return owns_outfit(outfit_id) and passing_wear_path(outfit_id) is not None


    def attempt_wear_outfit(outfit_id):
        """Equip an owned outfit only when at least one acceptance path passes."""
        outfit = get_outfit(outfit_id)

        if not owns_outfit(outfit_id):
            renpy.store.last_wardrobe_message = "{} has not been purchased yet.".format(outfit["name"])
            renpy.restart_interaction()
            return False

        path = passing_wear_path(outfit_id)
        if path is None:
            renpy.store.last_wear_route = None
            renpy.store.last_wardrobe_message = "{} isn't comfortable wearing {} yet.".format(
                renpy.store.girlfriend_name,
                outfit["name"],
            )
            renpy.restart_interaction()
            return False

        renpy.store.equipped_outfit = outfit_id
        renpy.store.last_wear_route = path["id"]
        # Keep the visible result message route-neutral. Exact path information is
        # revealed separately by Full Transparency / Developer UI where appropriate.
        renpy.store.last_wardrobe_message = "{} is now wearing {}.".format(
            renpy.store.girlfriend_name,
            outfit["name"],
        )
        refresh_leia_sprite_if_visible()
        renpy.restart_interaction()
        return True


    def current_outfit_name():
        outfit_id = renpy.store.equipped_outfit
        if outfit_id not in OUTFIT_DEFINITIONS:
            return "Unknown"
        return OUTFIT_DEFINITIONS[outfit_id]["name"]


    def outfit_status_text(outfit_id):
        if not owns_outfit(outfit_id):
            return "Not owned"
        if renpy.store.equipped_outfit == outfit_id:
            return "Equipped"
        if can_wear(outfit_id):
            return "Owned — ready to wear"
        return "Owned — not comfortable yet"


    def _wardrobe_stat_label(stat_name):
        labels = {
            "love": "Love",
            "trust": "Trust",
            "boredom": "Boredom",
            "momentum": "Momentum",
            "curiosity": "Curiosity",
            "temptation": "Temptation",
            "exhibitionism": "Exhibitionism",
            "boundary_looseness": "Boundary Looseness",
            "secrecy": "Secrecy",
            "jealousy": "Jealousy",
            "acceptance": "Acceptance",
        }
        return labels.get(stat_name, stat_name.replace("_", " ").title())


    def outfit_requirement_text(outfit_id, mode=None):
        """Format wear requirements according to the current transparency mode."""
        outfit = get_outfit(outfit_id)
        paths = outfit.get("wear_paths", [])
        mode = mode or current_choice_mode()

        # An empty requirement list means the outfit is freely wearable once owned.
        if any(not path.get("requirements", []) for path in paths):
            if mode == "developer":
                path = next(path for path in paths if not path.get("requirements", []))
                return "PASS — no stat gate. Path ID: {}".format(path["id"])
            if mode in ("insight", "full"):
                return "No additional comfort requirements."
            return ""

        if mode == "normal":
            return ""

        if mode == "insight":
            return "Possible comfort paths: {}".format(
                " • ".join(path["label"] for path in paths)
            )

        lines = []
        for path in paths:
            requirement_parts = []
            for group_name, stat_name, minimum in path.get("requirements", []):
                label = _wardrobe_stat_label(stat_name)
                if mode == "developer":
                    current = _requirement_value(group_name, stat_name)
                    marker = "PASS" if current >= minimum else "FAIL"
                    requirement_parts.append("{} {} {}/{}".format(marker, label, current, minimum))
                else:
                    requirement_parts.append("{} {}+".format(label, minimum))

            if mode == "developer":
                path_state = "PASS" if _requirements_met(path.get("requirements", [])) else "FAIL"
                lines.append("{} {} [path: {}] — {}".format(
                    path_state,
                    path["label"],
                    path["id"],
                    ", ".join(requirement_parts),
                ))
            else:
                lines.append("{} — {}".format(path["label"], ", ".join(requirement_parts)))

        return "\n".join(lines)


    def debug_unlock_all_outfits():
        for outfit_id in OUTFIT_DEFINITIONS:
            if outfit_id not in renpy.store.owned_outfits:
                renpy.store.owned_outfits.append(outfit_id)
        renpy.store.modified_save = True
        renpy.store.last_shop_message = "Developer unlock: all current outfits owned."
        renpy.restart_interaction()


    def debug_reset_wardrobe():
        renpy.store.owned_outfits = ["casual_default"]
        renpy.store.equipped_outfit = "casual_default"
        renpy.store.last_wear_route = "default_comfort"
        renpy.store.last_shop_message = "Wardrobe reset to defaults."
        renpy.store.last_wardrobe_message = ""
        renpy.store.modified_save = True
        refresh_leia_sprite_if_visible()
        renpy.restart_interaction()
