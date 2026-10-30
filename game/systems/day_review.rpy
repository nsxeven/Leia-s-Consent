# Reusable, save-local daily journal. No persistent gallery unlocks are consulted.
default lc_review_active = None
default lc_review_days = {}
default lc_title_facts = {}
default persistent.lc_recap_animation = True
default persistent.lc_title_style = "story"
default persistent.lc_title_badges = False
default persistent.lc_day1_dream = "ask"

init 20 python:
    LC_REVIEW_GROUPS = ("relationship", "partner", "player")
    LC_REVIEW_DAYS = {
        "ch01_d1": {"label": "Chapter One · Day One", "route_key": "ch01_day1_route_pressure"},
        "ch01_d2": {"label": "Chapter One · Day Two", "route_key": "ch01_d2_end_route"},
        "ch01_d3": {"label": "Chapter One · Day Three", "route_key": "ch01_d3_lane"},
        "ch01_d4": {"label": "Chapter One · Day Four", "route_key": "ch01_d4_end_route"},
        "ch01_d5": {"label": "Chapter One · Day Five", "route_key": "ch01_d5_end_route"},
    }
    LC_REVIEW_ROUTES = {
        "mixed": ("Mixed / undecided", "The direction is still taking shape."),
        "love": ("Love", "Your time together ended on a close, private note."),
        "love_repaired": ("Repair", "You made room for a difficult conversation and another chance."),
        "exhibitionism": ("Shared attention", "Attention from others became part of an experience you shared."),
        "nts_seeded": ("Shared curiosity", "You noticed a new possibility together. Nothing is settled yet."),
        "ntr_seeded": ("NTR pressure", "Some distance between you remained at the end of the day."),
        "ntr": ("NTR pressure", "There are questions you have not resolved together."),
        "ntr_confirmed": ("NTR direction", "There are questions you have not resolved together."),
        "mixed_unresolved": ("Mixed / unresolved", "The day ended with things left unsaid."),
        "ntr_unresolved": ("NTR / unresolved", "The day ended with things left unsaid."),
        # Day Three's NTR night is still one scene. The club choice only changes
        # how that night is described in the recap; Day Four keeps reading the lane.
        "ntr_talked": ("NTR pressure", "You tried to talk it through. The night still ended with questions between you."),
        "ntr_withdrew": ("NTR pressure", "You stepped away, and the distance was still there at the end of the night."),
    }
    # Internal trait changes are deliberately hidden in Insight; Full exposes them.
    LC_REVIEW_INSIGHT_STATS = {"love", "trust", "boredom", "curiosity", "exhibitionism", "jealousy", "acceptance"}

    def lc_review_stats():
        return {group: dict(get_stat_group(group)) for group in LC_REVIEW_GROUPS}

    def lc_review_begin(day_id):
        if day_id not in LC_REVIEW_DAYS:
            raise ValueError("Register the day in LC_REVIEW_DAYS first: " + day_id)
        old = store.lc_review_days.get(day_id)
        if store.lc_review_active == day_id and old and old.get("end") is None:
            return  # Do not reset a day's baseline on repeated entry.
        record = {"start": lc_review_stats(), "end": None, "moments": [], "choices": [],
                  "route": "mixed", "facts": {}, "titles_before": lc_character_titles(),
                  "partial": False, "summary": None}
        store.lc_review_days = dict(store.lc_review_days, **{day_id: record})
        store.lc_review_active = day_id

    def lc_review_replace(day_id, **changes):
        record = dict(store.lc_review_days[day_id])
        record.update(changes)
        store.lc_review_days = dict(store.lc_review_days, **{day_id: record})

    def lc_review_record_image(name):
        day_id = getattr(store, "lc_review_active", None)
        if not day_id or day_id not in store.lc_review_days:
            return
        record = store.lc_review_days[day_id]
        if record.get("end") is not None:
            return
        image = " ".join(name) if isinstance(name, (tuple, list)) else str(name)
        if not image.startswith("cg "):
            return
        image = image[3:]
        for entry in GALLERY_ENTRIES.values():
            if entry["tab"] != day_id:
                continue
            if any(page["image"] == image for page in entry["pages"]):
                # One card per moment, retaining the actual latest variant shown.
                moments = [m for m in record["moments"] if m["id"] != entry["id"]]
                moments.append({"id": entry["id"], "image": image,
                                "caption": entry["title"], "dream": entry["dream"]})
                lc_review_replace(day_id, moments=moments)
                return

    def lc_review_note_choice(choice_id, before):
        day_id = store.lc_review_active
        if not day_id or day_id not in store.lc_review_days:
            return
        after = lc_review_stats()
        deltas = [(g, key, after[g][key] - value) for g in LC_REVIEW_GROUPS
                  for key, value in before[g].items() if after[g][key] != value]
        record = store.lc_review_days[day_id]
        if record.get("end") is None:
            lc_review_replace(day_id, choices=record["choices"] + [{"id": choice_id, "deltas": deltas}])

    def lc_review_route(day_id):
        value = get_story_value(LC_REVIEW_DAYS[day_id]["route_key"], "mixed")
        if day_id == "ch01_d1" and getattr(store, "ch01_day1_love_ending", False):
            return "love"
        # Day Three's lane is fixed by Day Two. The two NTR choices still change
        # how the recap describes the night, without relabeling the lane Day Four reads.
        if day_id == "ch01_d3" and value == "ntr":
            effort = get_story_value("ch01_d3_ntr_repair_effort", "none")
            if effort == "talk":
                return "ntr_talked"
            if effort == "withdraw":
                return "ntr_withdrew"
        return value if value in LC_REVIEW_ROUTES else "mixed"

    def lc_review_finish(day_id):
        if day_id not in LC_REVIEW_DAYS:
            raise ValueError("Unknown review day: " + day_id)
        if day_id not in store.lc_review_days:
            # An old save loaded mid-day has no reliable day-start state.
            store.lc_review_days = dict(store.lc_review_days, **{day_id: {
                "start": None, "end": None, "moments": [], "choices": [],
                "titles_before": None, "partial": True}})
        if store.lc_review_days[day_id].get("end") is None:
            route = lc_review_route(day_id)
            lc_review_replace(day_id, end=lc_review_stats(), route=route,
                              facts=dict(store.lc_title_facts), summary=LC_REVIEW_ROUTES[route][1],
                              modified=bool(store.modified_save),
                              titles_after=lc_character_titles(route=route))
        if store.lc_review_active == day_id:
            store.lc_review_active = None
        return store.lc_review_days[day_id]

    def lc_review_cards(day_id):
        record = store.lc_review_days.get(day_id, {})
        moments = record.get("moments", [])
        # Evenly cover the day, instead of filling the recap with one late scene.
        if len(moments) > 5:
            moments = [moments[int(round(i * (len(moments) - 1) / 4.0))] for i in range(5)]
        return moments

    def lc_review_delta_rows(day_id, mode):
        record = store.lc_review_days.get(day_id, {})
        if mode == "normal" or not record.get("start") or not record.get("end"):
            return []
        rows = []
        for group in LC_REVIEW_GROUPS:
            for stat, before in record["start"][group].items():
                after = record["end"][group][stat]
                if before == after or (mode == "insight" and stat not in LC_REVIEW_INSIGHT_STATS):
                    continue
                detail = "Increased" if after > before else "Decreased"
                if mode in ("full", "developer"):
                    detail = "{} → {} ({:+d})".format(before, after, after - before)
                rows.append((STAT_LABELS.get(stat, stat), detail))
        return rows

    def lc_review_choice_rows(day_id):
        rows = []
        for choice in store.lc_review_days.get(day_id, {}).get("choices", []):
            parts = ["{} {:+d}".format(STAT_LABELS.get(k, k), v) for g, k, v in choice["deltas"]]
            if parts:
                rows.append((choice["id"].replace("ch01_", "").replace("_", " ").title(), ", ".join(parts)))
        return rows

    def lc_title_fact(fact, value=True):
        """Author only at a confirmed story event, never from a stat threshold.
        Facts are in-world facts known to Ryan; do not call for dreams/suspicions.
        """
        allowed = {"sharing_agreed", "sharing_happened", "betrayal_known", "humiliation_agreed",
                   "married", "repair_chosen", "separated"}
        if fact not in allowed:
            raise ValueError("Unknown title fact: " + fact)
        store.lc_title_facts = dict(store.lc_title_facts, **{fact: bool(value)})

    def lc_current_review_route():
        for day_id in reversed(tuple(LC_REVIEW_DAYS)):
            record = store.lc_review_days.get(day_id, {})
            if record.get("end") is not None:
                return record.get("route", "mixed")
        return "mixed"

    def lc_character_titles(route=None, facts=None, style=None):
        style = style or getattr(persistent, "lc_title_style", "story")
        if style == "off":
            return ("", "")
        facts = store.lc_title_facts if facts is None else facts
        route = route or lc_current_review_route()
        if facts.get("separated"):
            return ("Walking Away", "Estranged Partner")
        if facts.get("repair_chosen"):
            return ("Rebuilding Trust", "Making Amends")
        if facts.get("betrayal_known"):
            ryan = "Betrayed Boyfriend"
            if style == "genre":
                ryan = "Beta Cuck" if facts.get("humiliation_agreed") else "Cuckold"
            return (ryan, "Unfaithful Lover" if style == "story" else "Cheating Girlfriend")
        if facts.get("sharing_agreed") and facts.get("sharing_happened"):
            if style == "genre":
                return ("Stag", "Hotwife" if facts.get("married") else "Shared Girlfriend")
            return ("Sharing Partner", "Adventurous Partner")
        if route == "love_repaired":
            return ("Giving Her Another Chance", "Rebuilding Trust")
        if route == "love":
            return ("Devoted Boyfriend", "Affectionate Partner")
        if route == "exhibitionism":
            return ("Knowing Accomplice", "Enjoying the Attention")
        if route == "nts_seeded":
            return ("Curious Partner", "Testing the Waters")
        if route in ("ntr", "ntr_seeded", "ntr_confirmed", "ntr_unresolved", "mixed_unresolved", "ntr_talked", "ntr_withdrew"):
            # These legacy route labels do not establish infidelity or Ryan's knowledge.
            return ("Uneasy Observer", "Growing Distant")
        return ("Curious Partner", "Affectionate Partner")

    def lc_review_titles(day_id):
        record = store.lc_review_days.get(day_id, {})
        return lc_character_titles(record.get("route", "mixed"), record.get("facts", {}))

    def lc_review_latest():
        completed = [k for k in LC_REVIEW_DAYS if store.lc_review_days.get(k, {}).get("end") is not None]
        return completed[-1] if completed else None

    def lc_review_reset():
        store.lc_review_active = None
        store.lc_review_days = {}
        store.lc_title_facts = {}

    # Capture show/scene statements, not image prediction or gallery browsing.
    # Preserve the project's configured show callable and all its arguments.
    _lc_review_original_show = config.show
    def lc_review_show(name, *args, **kwargs):
        tag = name.split()[0] if isinstance(name, str) else name[0]
        character_id = "leia" if tag.startswith("leia_") else ("ryan" if tag.startswith("ryan_") else None)
        entering = character_id and not renpy.showing(tag)
        result = _lc_review_original_show(name, *args, **kwargs)
        if kwargs.get("layer", "master") == "master" and not getattr(store, "_main_menu", False):
            lc_review_record_image(name)
            if entering and getattr(persistent, "lc_title_badges", False):
                titles = lc_character_titles()
                title = titles[1 if character_id == "leia" else 0]
                if title:
                    renpy.show_screen("lc_title_badge", character_id, title)
        return result
    config.show = lc_review_show

label lc_day_review(day_id):
    $ lc_review_finish(day_id)
    $ lc_review_saved_hud = phone_hud_enabled
    $ lc_review_saved_quick = quick_menu
    $ phone_hud_enabled = False
    $ quick_menu = False
    window hide
    call screen lc_day_review_screen(day_id)
    $ phone_hud_enabled = lc_review_saved_hud
    $ quick_menu = lc_review_saved_quick
    window auto
    return
