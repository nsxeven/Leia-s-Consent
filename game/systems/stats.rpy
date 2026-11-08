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


    # ------------------------------------------------------------------
    # Stat model v2. The rules live in python-packages/lc_stat_model.py so
    # the route checks, the Full "Current lean" line, the choice route tag
    # and the unit tests all run the same code.
    import lc_stat_model

    # Route and her-own-call thresholds (lc_stat_model.THRESHOLDS), e.g. LC_T["d2_exhib_lane"].
    LC_T = lc_stat_model.THRESHOLDS

    def lc_stats_flat():
        """{stat: value} for the five stats, read from the save-state groups."""
        out = {}
        for stat in lc_stat_model.STAT_ORDER:
            group = get_stat_group(lc_stat_model.STAT_GROUPS[stat])
            default = lc_stat_model.DEFAULTS[lc_stat_model.STAT_GROUPS[stat]][stat]
            out[stat] = int(group.get(stat, default))
        return out

    def lc_stat(stat):
        return lc_stats_flat()[stat]

    def lc_exhib_gained(prefix):
        """Exhibitionism gained from choices whose ids start with `prefix` (e.g. today's)."""
        total = 0
        for choice_id in renpy.store.choice_history:
            if not choice_id.startswith(prefix) or choice_id not in CHOICE_EFFECTS:
                continue
            for _group, stat, amount in get_choice_effects(choice_id):
                if stat == "exhibitionism":
                    total += amount
        return total

    def lc_d1_route_pressure():
        """Day 1 end state ('ntr_seeded' / 'nts_seeded' / 'mixed'). Story and Full readout share it."""
        return lc_stat_model.d1_route_pressure(lc_stats_flat(), lc_route_explorer_for_lane())

    def lc_d1_love_bedtime(pressure):
        return lc_stat_model.d1_love_bedtime(pressure, lc_stats_flat())

    def lc_current_lean():
        """Lean key for the Full 'Current lean' line, from the same resolvers the routes use."""
        flat = lc_stats_flat()
        for key in ("ch01_d5_end_route", "ch01_d4_end_route"):
            value = get_story_value(key, None)
            if value:
                return lc_stat_model.lean_from_route_value(value)
        if has_story_flag("ch01_day_03_started"):
            lane = get_story_value("ch01_d4_lane", None) or get_story_value("ch01_d3_lane", None)
            if (lane == "love" and get_story_value("ch01_d3_strained_love", False)
                    and not has_story_flag("ch01_day_03_complete")):
                return "strained"
            if lane:
                return lc_stat_model.lean_from_route_value(lane)
        if has_story_flag("ch01_day_02_complete"):
            return lc_stat_model.lean_from_route_value(get_story_value("ch01_d2_end_route", "love"))
        if has_story_flag("ch01_day_02_started"):
            lane = ch01_d2_route_lane()
            if lc_stat_model.d2_love_exhib_blend(lane, flat, lc_exhib_gained("ch01_d2_")):
                return "love_exhib"
            return lc_stat_model.lean_from_route_value(lane)
        if has_story_flag("ch01_started"):
            pressure = get_story_value("ch01_day1_route_pressure", None) or lc_d1_route_pressure()
            if pressure == "mixed":
                return "love" if lc_stat_model.d1_love_bedtime(pressure, flat) else "undecided"
            return lc_stat_model.lean_from_route_value(pressure)
        return "undecided"

    def lc_current_lean_label():
        return lc_stat_model.LEAN_LABELS.get(lc_current_lean(), "Undecided")

    def lc_migrate_stats_v2():
        """after_load: convert a pre-v2 save once (formulas in lc_stat_model.migrate_stats).

        Story values, choice history, lanes and end states are never touched.
        A save made mid-Day-2 keeps the lane the old rules gave it for the rest
        of that day (ch01_d2_lane_migrated), so loading can't flip it.
        """
        store_ = renpy.store
        rel = getattr(store_, "relationship_stats", None) or {}
        par = getattr(store_, "partner_stats", None) or {}
        ply = getattr(store_, "player_stats", None) or {}
        if lc_stat_model.is_legacy_stats(rel, par, ply):
            if (has_story_flag("ch01_day_02_started") and not has_story_flag("ch01_day_02_complete")
                    and get_story_value("ch01_d2_lane_migrated", None) is None):
                d2_ids = choice_ids_with_prefix("ch01_d2_")
                lane = lc_stat_model.legacy_d2_lane(
                    rel, par, ply,
                    get_story_value("ch01_day1_route_pressure", "mixed"),
                    chapter_nonchalant_count("ch01"),
                    choice_tag_count("nonchalant", d2_ids),
                    choice_tag_count("open", d2_ids),
                    choice_tag_count("attentive", d2_ids),
                )
                set_story_value("ch01_d2_lane_migrated", lane)
            new_rel, new_par, new_ply, legacy = lc_stat_model.migrate_stats(rel, par, ply)
            store_.relationship_stats = new_rel
            store_.partner_stats = new_par
            store_.player_stats = new_ply
            store_.lc_legacy_stats = legacy
            days = {}
            for day_id, record in dict(getattr(store_, "lc_review_days", {}) or {}).items():
                record = dict(record)
                record["start"] = lc_stat_model.migrate_snapshot(record.get("start"))
                record["end"] = lc_stat_model.migrate_snapshot(record.get("end"))
                record["choices"] = [dict(c, deltas=lc_stat_model.migrate_deltas(c.get("deltas")))
                                     for c in record.get("choices", [])]
                days[day_id] = record
            store_.lc_review_days = days
        else:
            # A v2 save from before a stat existed: add the missing key at its default.
            for group_name, defaults in lc_stat_model.DEFAULTS.items():
                group = get_stat_group(group_name)
                for stat, value in defaults.items():
                    if stat not in group:
                        group[stat] = value
        store_.lc_stat_model_version = 2

    if lc_migrate_stats_v2 not in config.after_load_callbacks:
        config.after_load_callbacks.append(lc_migrate_stats_v2)
