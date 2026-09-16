# Love-route outfit control.
#
# Design rule:
# Once the story has resolved into a Love lane, outfit-prompt scenes can offer
# Ryan a dedicated "let me choose" option. Love gives Ryan meaningful outfit
# control, but Leia's current sexual confidence still matters. At ordinary
# outdoor outfit prompts she will accept outdoor clothes he owns. Swimwear stays
# visible in the picker but is locked until Exhibitionism is high enough.
#
# This is deliberately NOT a global Wardrobe bypass. The perk only applies when
# the script explicitly opens the Love-route outfit picker.

init 10 python:

    LOVE_OUTFIT_END_STATES = ("love", "love_repaired")
    LOVE_SWIMWEAR_EXHIBITIONISM_MIN = 22

    # Day Two needs a distinct narrative outfit even though final art is still
    # pending. Until final layers are generated it reuses the current bold
    # placeholder layer.
    if "d2_loose_low_cut" not in OUTFIT_DEFINITIONS:
        OUTFIT_DEFINITIONS["d2_loose_low_cut"] = {
            "name": "Loose Low-Cut Top + Fitted Skirt",
            "category": "bold",
            "description": "A loose low-cut evening top with a fitted skirt. The neckline shifts noticeably when Leia leans forward.",
            "cost": 0,
            "shop_visible": False,
            "story_grant": True,
            "shop_requirements": [],
            "boldness": 70,
            "exposure": 65,
            "public_risk": 55,
            "comfort": 45,
            "playfulness": 65,
            "elegance": 55,
            "contexts": ("date", "restaurant", "nightlife", "evening"),
            "asset_id": "leia_outfit_d2_loose_low_cut",
            "wear_paths": [
                {
                    "id": "story_d2_evening",
                    "label": "Day Two evening outfit",
                    "requirements": [],
                },
            ],
        }

    # Keep the layered sprite system testable before the final outfit layer is
    # generated. Final art can replace this mapping without changing story IDs.
    LEIA_OUTFIT_ATTRIBUTES["d2_loose_low_cut"] = "outfit_after_hours"
    LEIA_CONTROLLED_ATTRIBUTES.add("outfit_after_hours")


    def love_outfit_control_active(route_lane=None):
        """Return True when the current story state has earned Love outfit control."""
        if route_lane == "love":
            return True

        end_route = get_story_value("ch01_d2_end_route", None)
        return end_route in LOVE_OUTFIT_END_STATES


    def love_outfit_is_outdoor(outfit_id):
        """Whether an outfit belongs in an ordinary public/outdoor story picker."""
        outfit = get_outfit(outfit_id)
        contexts = set(outfit.get("contexts", ()))
        outdoor_contexts = {
            "casual", "day", "date", "restaurant", "resort",
            "evening", "nightlife", "party",
        }
        return bool(contexts.intersection(outdoor_contexts))


    def love_outfit_is_swimwear(outfit_id):
        return get_outfit(outfit_id).get("category") == "swimwear"


    def love_outfit_swimwear_unlocked():
        return renpy.store.partner_stats.get("exhibitionism", 0) >= LOVE_SWIMWEAR_EXHIBITIONISM_MIN


    def love_outfit_available(outfit_id):
        """Availability inside the Love story picker, separate from visibility."""
        if love_outfit_is_swimwear(outfit_id):
            return love_outfit_swimwear_unlocked()
        return love_outfit_is_outdoor(outfit_id)


    def love_outfit_lock_text(outfit_id):
        """Mode-sensitive explanation for a visible but unavailable outfit."""
        if not love_outfit_is_swimwear(outfit_id):
            return "Not suitable for this outing."

        mode = getattr(persistent, "choice_display_mode", "normal") or "normal"
        current = renpy.store.partner_stats.get("exhibitionism", 0)

        if mode == "normal":
            return "Leia isn't comfortable wearing this here yet."
        elif mode == "insight":
            return "Requires higher Exhibitionism."
        elif mode == "full":
            return "Requires Exhibitionism {}. Current: {}.".format(
                LOVE_SWIMWEAR_EXHIBITIONISM_MIN, current
            )
        else:
            return "LOCKED — Exhibitionism {}/{} | category: swimwear | id: {}".format(
                current, LOVE_SWIMWEAR_EXHIBITIONISM_MIN, outfit_id
            )


    def love_outfit_candidates(story_ids=()):
        """Build the Love-route picker in a stable order.

        Scene-specific outdoor story outfits are first. Owned outdoor outfits
        follow. Owned swimwear is deliberately included even while locked so the
        player can see that higher Exhibitionism expands Love-route outfit control.
        Home/lounge/sleep-only clothing is omitted from outdoor prompts.
        """
        result = []

        for outfit_id in story_ids:
            if outfit_id not in OUTFIT_DEFINITIONS or outfit_id in result:
                continue
            if love_outfit_is_outdoor(outfit_id) or love_outfit_is_swimwear(outfit_id):
                result.append(outfit_id)

        for outfit_id in valid_owned_outfit_ids():
            if outfit_id in result:
                continue
            if love_outfit_is_outdoor(outfit_id) or love_outfit_is_swimwear(outfit_id):
                result.append(outfit_id)

        return result


    def love_route_wear_request(outfit_id, route_lane=None):
        """Equip an outfit because Ryan explicitly requested it on the Love route.

        Outdoor clothes bypass ordinary wear-path gates at explicit Love outfit
        prompts. Swimwear additionally requires the Love exhibitionism threshold.
        Non-owned shop outfits remain unavailable. Scene-specific story-grantable
        outfits are obtained automatically when chosen.
        """
        if not love_outfit_control_active(route_lane=route_lane):
            return False

        if not love_outfit_available(outfit_id):
            return False

        outfit = get_outfit(outfit_id)

        if not owns_outfit(outfit_id):
            if outfit.get("story_grant", False):
                renpy.store.owned_outfits.append(outfit_id)
            else:
                return False

        renpy.store.equipped_outfit = outfit_id
        renpy.store.last_wear_route = "love_route_request"
        renpy.store.last_wardrobe_message = "{} is wearing {} because you asked.".format(
            renpy.store.girlfriend_name,
            outfit["name"],
        )

        set_story_flag("love_outfit_request_used")
        set_story_value("love_outfit_last_request", outfit_id)
        set_story_value(
            "love_outfit_request_count",
            int(get_story_value("love_outfit_request_count", 0) or 0) + 1,
        )

        refresh_leia_sprite_if_visible()
        return True


    def love_outfit_is_daring(outfit_id):
        """Narrative helper for scenes that need secure-vs-daring behavior."""
        outfit = get_outfit(outfit_id)
        return (
            outfit.get("exposure", 0) >= 50
            or outfit.get("boldness", 0) >= 60
        )


screen leia_love_outfit_picker(options, title_text="What should Leia wear?"):
    modal True
    zorder 240

    add Solid("#000000B8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        ysize 760
        padding (42, 36)

        vbox:
            spacing 16

            text "LOVE ROUTE — OUTFIT CHOICE" size 34
            text "[title_text]" size 28
            text "Choose from Leia's outdoor wardrobe. More daring categories open as her confidence grows." size 22

            viewport:
                xfill True
                ysize 560
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 14
                    xfill True

                    for outfit_id in options:
                        $ outfit = get_outfit(outfit_id)
                        $ display_name = outfit.get("name", outfit_id)
                        $ display_description = outfit.get("description", "")
                        $ display_context = outfit_context_text(outfit_id)
                        $ outfit_available = love_outfit_available(outfit_id)
                        $ lock_text = love_outfit_lock_text(outfit_id) if not outfit_available else ""

                        button:
                            xfill True
                            padding (22, 18)
                            sensitive outfit_available
                            action Return(outfit_id)

                            if not outfit_available:
                                at transform:
                                    alpha 0.38

                            vbox:
                                spacing 5
                                text "[display_name]" size 29
                                text "[display_description]" size 21
                                text "Usual context: [display_context]" size 18
                                if not outfit_available:
                                    text "[lock_text]" size 19
