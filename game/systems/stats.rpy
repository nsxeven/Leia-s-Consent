# Core relationship/stat logic.
# Story code should use these helpers instead of directly changing stat dictionaries.

init python:

    def clamp_stat(value):
        """Clamp a relationship stat to the inclusive 0-100 range."""
        return max(0, min(100, int(round(value))))


    def get_stat_group(group_name):
        """Return one of the mutable save-state stat dictionaries."""
        if group_name == "relationship":
            return renpy.store.relationship_stats
        elif group_name == "partner":
            return renpy.store.partner_stats
        elif group_name == "player":
            return renpy.store.player_stats

        raise ValueError("Unknown stat group: {}".format(group_name))


    def change_stat(group_name, stat_name, amount):
        """Change a stat during normal gameplay and keep it between 0 and 100."""
        group = get_stat_group(group_name)

        if stat_name not in group:
            raise ValueError("Unknown stat '{}' in group '{}'".format(stat_name, group_name))

        group[stat_name] = clamp_stat(group[stat_name] + amount)
        return group[stat_name]


    def debug_change_stat(group_name, stat_name, amount):
        """Developer-only stat editing. Keeps the panel open and shows a small notification."""
        new_value = change_stat(group_name, stat_name, amount)
        renpy.store.modified_save = True
        renpy.notify("{}: {}".format(stat_name.replace("_", " ").title(), new_value))
        renpy.restart_interaction()
        return None


    def debug_add_money(amount):
        """Developer-only currency editing with the same no-negative rule as the economy."""
        old_money = renpy.store.money
        renpy.store.money = max(0, renpy.store.money + int(amount))
        renpy.store.last_money_change = renpy.store.money - old_money
        renpy.store.last_money_reason = "Developer money edit"
        renpy.store.modified_save = True
        renpy.notify("Money: ${}".format(renpy.store.money))
        renpy.restart_interaction()
        return None


    def nts_score():
        """Return the current consensual-sharing/NTS tendency (prototype formula)."""
        relationship = renpy.store.relationship_stats
        partner = renpy.store.partner_stats
        player = renpy.store.player_stats

        score = (
            relationship["love"] * 0.20
            + relationship["trust"] * 0.20
            + partner["curiosity"] * 0.20
            + partner["exhibitionism"] * 0.15
            + player["acceptance"] * 0.15
            + relationship["momentum"] * 0.10
        )

        return clamp_stat(score)


    def ntr_score():
        """Return the current secrecy/betrayal/NTR tendency (prototype formula)."""
        relationship = renpy.store.relationship_stats
        partner = renpy.store.partner_stats

        score = (
            relationship["boredom"] * 0.20
            + partner["temptation"] * 0.25
            + partner["secrecy"] * 0.20
            + partner["boundary_looseness"] * 0.15
            + relationship["momentum"] * 0.10
            + (100 - relationship["trust"]) * 0.10
        )

        return clamp_stat(score)
