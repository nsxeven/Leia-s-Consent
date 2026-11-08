# Optional player-facing route exploration for Full Transparency.
# Applies to future route checks; already-played scenes remain unchanged.
# The release demo supports Day 1 steering and the Day 2 lane resolver.
# Later day/state-specific route gates require explicit adaptation before release.

default lc_route_explorer_focus = "auto"
default lc_route_explorer_used = False

init 200 python:

    LC_ROUTE_EXPLORER_OPTIONS = (
        ("auto", "Story-driven", "Let choices determine the route."),
        ("love", "Love", "Favor Love and Trust; keep it between the two of you."),
        ("exhibitionism", "Love+Exhib", "Favor Exhibitionism, with both of you in on it."),
        ("ntr_risk", "NTR", "Favor rising Temptation and a strained relationship."),
    )

    # Stat model v2 baselines (Love / Trust / Exhibitionism / Temptation).
    LC_ROUTE_EXPLORER_BASELINES = {
        "love": {
            "relationship": {"love": 72, "trust": 72, "temptation": 5},
            "partner": {"exhibitionism": 12},
            "player": {},
            "pressure": "mixed",
        },
        "exhibitionism": {
            "relationship": {"love": 68, "trust": 65, "temptation": 5},
            "partner": {"exhibitionism": 71},
            "player": {},
            "pressure": "nts_seeded",
        },
        "ntr_risk": {
            "relationship": {"love": 38, "trust": 36, "temptation": 43},
            "partner": {"exhibitionism": 12},
            "player": {},
            "pressure": "ntr_seeded",
        },
    }

    def lc_route_explorer_allowed():
        if getattr(store, "LC_IS_RELEASE", False) and not config.developer:
            return False
        mode = current_choice_mode()
        return mode == "full" or (mode == "developer" and config.developer)

    def lc_route_explorer_current():
        value = getattr(store, "lc_route_explorer_focus", "auto")
        return value if value in ("auto", "love", "exhibitionism", "ntr_risk") else "auto"

    def lc_route_explorer_current_label():
        route = lc_route_explorer_current()
        return next((label for key, label, _ in LC_ROUTE_EXPLORER_OPTIONS if key == route), "Story-driven")

    def lc_route_explorer_for_lane():
        """Optional override for dynamic Day 1 / Day 2 route selection."""
        route = lc_route_explorer_current()
        return None if route == "auto" else route

    def lc_route_explorer_set_focus(route):
        """Menu-safe route switch. Does not rewrite previous player history."""
        if not lc_route_explorer_allowed() or route not in [x[0] for x in LC_ROUTE_EXPLORER_OPTIONS]:
            return None
        if not has_story_flag("ch01_started"):
            renpy.notify("Route Explorer becomes available during Chapter One.")
            return None
        if has_story_flag("ch01_day_02_complete"):
            renpy.notify("This story has committed later route states. Use a new chapter checkpoint to replay a different path.")
            return None

        store.lc_route_explorer_focus = route
        store.lc_route_explorer_used = True
        set_story_value("ch01_route_explorer_focus", route)

        if route != "auto":
            preset = LC_ROUTE_EXPLORER_BASELINES[route]
            # These are deliberate exploration presets, not an edit to the actual
            # choice effects. Switching back to Story-driven stops future overrides
            # but does not undo previously seeded stats.
            for key, value in preset["relationship"].items():
                store.relationship_stats[key] = value
            for key, value in preset["partner"].items():
                store.partner_stats[key] = value
            for key, value in preset["player"].items():
                store.player_stats[key] = value
            set_story_value("ch01_day1_route_pressure", preset["pressure"])
            renpy.notify("Route focus: {}. Future checks will follow this direction.".format(lc_route_explorer_current_label()))
        else:
            renpy.notify("Route focus: Story-driven. Future choices control progression.")

        store.modified_save = True
        renpy.restart_interaction()
        return None
