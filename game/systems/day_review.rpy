# Reusable, save-local daily journal. No persistent gallery unlocks are consulted.
default lc_review_active = None
default lc_review_days = {}
default lc_title_facts = {}
default persistent.lc_recap_animation = True
default persistent.lc_title_style = "story"
default persistent.lc_title_badges = False
default persistent.lc_day1_dream = "ask"

init 20 python:
    import os

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
        for row in lc_review_choice_details(day_id):
            parts = ["{} {:+d}".format(chip["name"], chip["value"]) for chip in row["chips"]]
            if parts:
                rows.append((row["text"], ", ".join(parts)))
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

    # ------------------------------------------------------------------
    # Choice-style tags (darryn). How Ryan played the day sets both review
    # tags, replacing the route-based pair. Confirmed story facts (separated,
    # repair, betrayal known, sharing agreed + happened) still override.
    # Days with no mapped choices keep the route-based titles until mapped.
    LC_CHOICE_STYLE = {
        # Day 1
        "ch01_outfit_conservative": "protective", "ch01_outfit_comfort": "supportive", "ch01_outfit_bolder": "showoff",
        "ch01_photo_exit": "protective", "ch01_photo_support": "supportive", "ch01_photo_more": "showoff",
        "ch01_towel_boundary": "protective", "ch01_towel_laugh": "playful", "ch01_towel_forget": "detached",
        "ch01_towel_reassure": "supportive", "ch01_towel_honest": "honest", "ch01_towel_tease": "playful",
        "ch01_bra_cover": "protective", "ch01_bra_reassure": "supportive", "ch01_bra_playful": "playful",
        "ch01_stranger_territorial": "protective", "ch01_stranger_proud": "showoff", "ch01_stranger_encourage": "showoff",
        "ch01_catch_boundary": "protective", "ch01_catch_check": "supportive", "ch01_catch_ignore": "detached",
        "ch01_catch_joke": "playful",
        "ch01_friend_reassure": "supportive", "ch01_friend_tease": "playful", "ch01_friend_boundary": "honest",
        "ch01_julian_reassure": "supportive", "ch01_julian_honest": "honest", "ch01_julian_joke": "playful",
        "ch01_carry_lookaway": "protective", "ch01_carry_fix": "protective", "ch01_carry_brush": "supportive",
        "ch01_carry_joke": "playful",
        "ch01_movie_stop": "protective", "ch01_movie_subtle": "showoff", "ch01_movie_tease_presence": "playful",
        "ch01_movie_dismiss_concern": "detached",
        "ch01_can_tell_behave": "protective", "ch01_can_tell_tease": "playful", "ch01_can_tell_push": "showoff",
        "ch01_can_tell_dismiss": "detached",
        "ch01_private_apologize": "supportive", "ch01_private_playful": "playful", "ch01_private_curiosity": "honest",
        "ch01_private_dismiss": "detached",
        "ch01_noblanket_behave": "protective", "ch01_noblanket_test": "showoff", "ch01_noblanket_tease": "playful",
        "ch01_noblanket_phone": "detached",
        "ch01_watch_claim": "protective", "ch01_watch_tease": "playful", "ch01_watch_check": "supportive",
        "ch01_watch_ignore": "detached",
        "ch01_micro_warn": "protective", "ch01_micro_silent": "showoff", "ch01_micro_open": "showoff",
        "ch01_micro_dismiss": "detached",
        "ch01_philosophy_couple": "protective", "ch01_philosophy_trust": "honest",
        "ch01_philosophy_jealousy_fun": "showoff", "ch01_philosophy_dont_care": "detached",
        "ch01_julian_change_subject": "protective", "ch01_julian_let_play": "showoff", "ch01_julian_put_spot": "playful",
        "ch01_julian_dont_care": "detached",
        "ch01_compliment_affirm": "supportive", "ch01_compliment_tease": "protective", "ch01_compliment_enjoy": "showoff",
        "ch01_compliment_shrug": "detached",
        "ch01_alone_curiosity": "honest", "ch01_alone_open": "showoff", "ch01_alone_dismiss": "detached",
        "ch01_alone_apologize": "supportive",
        "ch01_private_claim": "protective", "ch01_private_open": "showoff", "ch01_private_jealous": "honest",
        "ch01_private_indifferent": "detached",
        "ch01_dream_curiosity": "honest", "ch01_dream_withdraw": "detached", "ch01_dream_ground": "supportive",
    }
    LC_STYLE_TAGS = {
        "protective": ("Her Bodyguard", "Feeling Safe"),
        "supportive": ("Her Biggest Fan", "Comfortable in Her Skin"),
        "playful": ("Resident Tease", "Blushing Again"),
        "showoff": ("Proud Show-Off", "Enjoying the Spotlight"),
        "honest": ("Open Book", "Heard and Seen"),
        "detached": ("Head in His Phone", "Quietly Drifting"),
    }
    LC_STYLE_MIXED = ("Still Figuring It Out", "Keeping Her Options Open")
    LC_STYLE_ORDER = ("protective", "supportive", "playful", "showoff", "honest", "detached")

    def lc_review_choice_ids(day_id):
        record = store.lc_review_days.get(day_id, {})
        return [c.get("id") for c in record.get("choices", []) if c.get("id")]

    def lc_review_style(day_id):
        """Winning choice style for the day, "mixed" on a near-tie, None if no mapped choices."""
        counts = {}
        for cid in lc_review_choice_ids(day_id):
            style = LC_CHOICE_STYLE.get(cid)
            if style:
                counts[style] = counts.get(style, 0) + 1
        if not counts:
            return None
        ranked = sorted(LC_STYLE_ORDER, key=lambda s: -counts.get(s, 0))
        top, second = counts.get(ranked[0], 0), counts.get(ranked[1], 0)
        if top < 2 or top - second < 1:
            return "mixed"
        return ranked[0]

    def lc_review_fact_override(facts):
        return bool(facts.get("separated") or facts.get("repair_chosen") or facts.get("betrayal_known")
                    or (facts.get("sharing_agreed") and facts.get("sharing_happened")))

    def lc_review_titles(day_id):
        record = store.lc_review_days.get(day_id, {})
        route, facts = record.get("route", "mixed"), record.get("facts", {}) or {}
        if getattr(persistent, "lc_title_style", "story") == "off":
            return ("", "")
        if lc_review_fact_override(facts):
            return lc_character_titles(route, facts)
        style = lc_review_style(day_id)
        if style is None:
            return lc_character_titles(route, facts)
        return LC_STYLE_TAGS.get(style, LC_STYLE_MIXED)

    # Moment stickers: up to two per day, in this priority order.
    # "Asked First": the scene-20 flag set when Ryan promised to ask and did.
    LC_MOMENT_STICKERS = (
        ("Asked First", lambda day_id, ids: day_id == "ch01_d1" and bool(getattr(store, "ch01_grab_promised_to_ask", False))),
        ("Told the Truth", lambda day_id, ids: "ch01_towel_honest" in ids),
        ("Wardrobe Rescue", lambda day_id, ids: "ch01_carry_fix" in ids),
        ("Eyes on Me", lambda day_id, ids: "ch01_watch_claim" in ids),
        ("Let Her Decide", lambda day_id, ids: "ch01_micro_silent" in ids),
        ("Proud of Her", lambda day_id, ids: "ch01_stranger_proud" in ids),
        ("Kept His Cool", lambda day_id, ids: "ch01_julian_reassure" in ids),
        ("Missed It", lambda day_id, ids: sum(1 for c in ("ch01_noblanket_phone", "ch01_watch_ignore", "ch01_compliment_shrug") if c in ids) >= 2),
    )

    def lc_review_stickers(day_id, limit=2):
        if getattr(persistent, "lc_title_style", "story") == "off":
            return []
        ids = set(lc_review_choice_ids(day_id))
        out = []
        for name, test in LC_MOMENT_STICKERS:
            try:
                if test(day_id, ids):
                    out.append(name)
            except Exception:
                pass
            if len(out) >= limit:
                break
        return out

    def lc_review_latest():
        completed = [k for k in LC_REVIEW_DAYS if store.lc_review_days.get(k, {}).get("end") is not None]
        return completed[-1] if completed else None

    def lc_review_reset():
        store.lc_review_active = None
        store.lc_review_days = {}
        store.lc_title_facts = {}

    # Scrapbook presentation. `start` on each day record is the snapshot taken
    # by lc_review_begin, before that day's choices, so bars can grow from
    # yesterday's value to today's. Partial old saves have no start and show
    # no bars rather than an invented baseline.
    LC_REVIEW_SCALE = 3
    # Night title card, 640-space. tools/gen_scrapbook_assets.py paints the same box.
    LC_REVIEW_NIGHT_CARD = (180, 270, 280, 52)
    LC_REVIEW_STAT_ORDER = (
        ("relationship", "love"),
        ("relationship", "trust"),
        ("relationship", "boredom"),
        ("partner", "curiosity"),
        ("partner", "exhibitionism"),
        ("player", "jealousy"),
        ("player", "acceptance"),
        ("relationship", "momentum"),
        ("partner", "temptation"),
        ("partner", "secrecy"),
        ("partner", "boundary_looseness"),
    )
    LC_REVIEW_BAR_STYLE = {
        "love": {"icon": "heart", "ink": "#cc0066"},
        "trust": {"icon": "shield", "ink": "#3f6470"},
        "boredom": {"icon": "zzz", "ink": "#5a4f72"},
        "curiosity": {"icon": "spark", "ink": "#8a4e28"},
        "exhibitionism": {"icon": "eye", "ink": "#8a3058"},
        "jealousy": {"icon": "flame", "ink": "#8a3828"},
        "acceptance": {"icon": "face", "ink": "#8a6420"},
        "momentum": {"icon": "chevron", "ink": "#3e5a28"},
        "temptation": {"icon": "drop", "ink": "#6a3050"},
        "secrecy": {"icon": "lock", "ink": "#5a504a"},
        "boundary_looseness": {"icon": "gate", "ink": "#5a5348"},
    }
    LC_REVIEW_NIGHT = {
        "ch01_d1": ("DAY 1", "ARRIVAL", "night falls over the villa…"),
        "ch01_d2": ("DAY 2", "THE SHORE", "the lights along the water go low…"),
        "ch01_d3": ("DAY 3", "THE CLUB", "night falls over the villa…"),
        "ch01_d4": ("DAY 4", "THE MARKET", "the town folds up its awnings…"),
        "ch01_d5": ("DAY 5", "THE WATER", "the water keeps the last of the light…"),
    }
    LC_REVIEW_TICKET = {
        "ch01_d1": ("VILLA NIGHT", "QUIET HOURS"),
        "ch01_d2": ("SHORE PASS", "DAY TWO"),
        "ch01_d3": ("CLUB NIGHT", "ADMIT ONE"),
        "ch01_d4": ("MARKET DAY", "ONE STUB"),
        "ch01_d5": ("BOAT DAY", "ALL ABOARD"),
    }
    # Two short handwritten lines. Route voice stays second-person, like the summaries.
    LC_REVIEW_DIARY = {
        "love": ("The day ended on a close, private note.", "That is the part worth keeping."),
        "love_repaired": ("You made room for a hard conversation.", "Another chance, not a promise."),
        "exhibitionism": ("Attention became part of the night.", "You were in it together."),
        "nts_seeded": ("You noticed a new possibility.", "Nothing is settled yet."),
        "ntr_seeded": ("Some distance remained.", "The day ended there."),
        "ntr": ("Questions stayed between you.", "The night did not answer them."),
        "ntr_confirmed": ("Questions stayed between you.", "You have not resolved them."),
        "mixed": ("The direction is still taking shape.", "Today did not decide it."),
        "mixed_unresolved": ("The day ended with things unsaid.", "You left them there."),
        "ntr_unresolved": ("The day ended with things unsaid.", "The distance came with you."),
        "ntr_talked": ("You tried to talk it through.", '[girlfriend_name]: "Then let\'s try. Properly."'),
        "ntr_withdrew": ("You stepped away.", "The distance was still there at the end."),
    }
    _lc_review_choice_catalog = None

    def lc_px(value):
        return int(round(value * LC_REVIEW_SCALE))

    def lc_review_chapter_line(day_id):
        label = LC_REVIEW_DAYS.get(day_id, {}).get("label", "")
        head = label.split("·")[0].strip()
        return head.upper() if head else ""

    def lc_review_night_copy(day_id):
        chapter = lc_review_chapter_line(day_id)
        preset = LC_REVIEW_NIGHT.get(day_id)
        if preset:
            return {"kicker": preset[0], "title": preset[1], "line": preset[2], "chapter": chapter}
        label = LC_REVIEW_DAYS.get(day_id, {}).get("label", "The day")
        bits = [part.strip() for part in label.split("·")]
        kicker = bits[-1].upper() if bits else "THE DAY"
        return {"kicker": kicker, "title": "", "line": "the day is over…", "chapter": chapter}

    def lc_review_day_number(day_id):
        tail = str(day_id).rsplit("_d", 1)[-1]
        if tail.isdigit():
            return "{:02d}".format(int(tail))
        return "01"

    def lc_review_ticket(day_id):
        title, detail = LC_REVIEW_TICKET.get(day_id, ("DAY NOTE", "ONE PAGE"))
        return {"title": title, "detail": detail, "number": lc_review_day_number(day_id)}

    def lc_review_diary(day_id):
        record = store.lc_review_days.get(day_id, {})
        route = record.get("route", "mixed")
        lines = LC_REVIEW_DIARY.get((day_id, route)) or LC_REVIEW_DIARY.get(route)
        if not lines:
            summary = (record.get("summary") or "The day has ended.").strip()
            bits = [part.strip() for part in summary.split(". ") if part.strip()]
            first = bits[0] if bits else "The day has ended."
            if not first.endswith("."):
                first += "."
            second = bits[1] if len(bits) > 1 else "That is what I want to remember."
            if not second.endswith("."):
                second += "."
            lines = (first, second)
        return (lines[0], lines[1])

    def lc_review_yesterday(day_id):
        """Copy of the day-start stat snapshot, or None when this save has no baseline."""
        start = store.lc_review_days.get(day_id, {}).get("start")
        if not start:
            return None
        return {group: dict(values) for group, values in start.items()}

    def lc_review_show_stats(day_id, mode):
        if mode == "normal":
            return False
        record = store.lc_review_days.get(day_id, {})
        return bool(record.get("start") and record.get("end") and not record.get("partial"))

    def lc_review_tracked_stats(mode):
        if mode == "normal":
            return []
        if mode == "insight":
            return [pair for pair in LC_REVIEW_STAT_ORDER if pair[1] in LC_REVIEW_INSIGHT_STATS]
        return list(LC_REVIEW_STAT_ORDER)

    def lc_review_bar_rows(day_id, mode):
        """Changed stats the scrapbook animates, yesterday then today.

        Insight is the seven player-facing stats, direction only.
        Full and Developer are all eleven, with exact numbers.
        Immersive and partial saves contribute nothing.
        """
        if not lc_review_show_stats(day_id, mode):
            return []
        record = store.lc_review_days[day_id]
        start, end = record["start"], record["end"]
        rows = []
        for group, stat in lc_review_tracked_stats(mode):
            before = start[group][stat]
            after = end[group][stat]
            if before == after:
                continue
            name = STAT_LABELS.get(stat, stat.replace("_", " ").title())
            rows.append({
                "stat": stat,
                "group": group,
                "label": name.upper(),
                "yesterday": before,
                "today": after,
                "delta": after - before,
            })
        return rows

    def lc_review_unchanged_count(day_id, mode):
        if not lc_review_show_stats(day_id, mode):
            return 0
        changed = len(lc_review_bar_rows(day_id, mode))
        return len(lc_review_tracked_stats(mode)) - changed

    def lc_review_polaroid_slots(count):
        """Landing spots in 640-space. One photo is centered; five still fit the page."""
        if count <= 0:
            return []
        tilts = (-3.2, 2.4, -1.8, 2.8, -1.4)

        def slot(x, y, tilt, tapes):
            return {"x": x, "y": y, "tilt": tilt, "tapes": tapes}

        if count == 1:
            return [slot(124, 72, tilts[0], ("top",))]
        if count == 2:
            return [
                slot(58, 36, tilts[0], ("top",)),
                slot(184, 132, tilts[1], ("corner", "corner_flip")),
            ]
        grid = [
            slot(56, 24, tilts[0], ("top",)),
            slot(186, 32, tilts[1], ("corner", "corner_flip")),
            slot(60, 124, tilts[2], ("top",)),
            slot(190, 132, tilts[3], ("corner",)),
        ]
        if count <= 4:
            return grid[:count]
        return grid + [slot(118, 214, tilts[4], ("corner_flip",))]

    def lc_review_photo_delay(index):
        return 0.25 + index * 0.35

    def lc_review_photo_land(index):
        return lc_review_photo_delay(index) + 0.34

    def lc_review_bars_lead(photo_count):
        if photo_count <= 0:
            return 0.35
        return lc_review_photo_land(photo_count - 1) + 0.20

    # Bars run strictly one after another (darryn): each bar finishes, glows,
    # then the next starts. LC_REVIEW_BAR_GAP is the beat between bars after
    # the glow (the live sequencer uses flash/glow, then advances).
    # Pacing (darryn): about 2x faster than PR #104, ~3.7 s for 3 photos + 3 bars.
    LC_REVIEW_BAR_RUN = 0.45
    LC_REVIEW_BAR_GAP = 0.15
    LC_REVIEW_BAR_GLOW = 0.28

    # Clicks never skip the review (darryn). Holding SPACE for
    # LC_REVIEW_HOLD_SKIP seconds finishes every drop and bar; a fresh SPACE
    # press (or Enter/Esc/Continue) then leaves once everything has landed.
    # All helpers return None: they run as screen actions, and a non-None
    # return would end `call screen`.
    LC_REVIEW_HOLD_SKIP = 0.6
    _lc_review_hold = {"t": None, "fired": False, "armed": False, "skip": False}

    def lc_review_hold_reset():
        _lc_review_hold.update(t=None, fired=False, armed=False, skip=False)

    def lc_review_hold_skipped():
        return _lc_review_hold["skip"]

    def lc_review_hold_down():
        import time
        if _lc_review_hold["t"] is None:
            _lc_review_hold["t"] = time.time()

    def lc_review_hold_up():
        _lc_review_hold.update(t=None, fired=False, armed=False)

    def lc_review_hold_progress():
        import time
        t = _lc_review_hold["t"]
        if t is None:
            return 0.0
        return min(1.0, (time.time() - t) / LC_REVIEW_HOLD_SKIP)

    def lc_review_hold_tick():
        # Runs every 0.05 s while SPACE is held; the restart it triggers
        # re-evaluates the screen so the progress bar and the skip check update.
        if _lc_review_hold["t"] is not None and not _lc_review_hold["fired"] and lc_review_hold_progress() >= 1.0:
            _lc_review_hold["fired"] = True
            _lc_review_hold["skip"] = True   # the screen reads this and sets `skipped`
        return None

    def lc_review_hold_arm():
        # Only a press that starts after the animation finished may leave,
        # so the hold that skipped doesn't also close the review on release.
        if _lc_review_hold["t"] is None:
            _lc_review_hold["armed"] = True

    def lc_review_hold_armed():
        return _lc_review_hold["armed"]

    def lc_review_bar_timing(index, photo_count, bar_count):
        """Legacy (start, duration) for tests. The live screen uses a single
        sequencer (lead → run → flash → next) instead of per-row absolute timers."""
        duration = LC_REVIEW_BAR_RUN
        start = lc_review_bars_lead(photo_count) + index * (duration + LC_REVIEW_BAR_GAP)
        return (start, duration)

    # Wall-clock start per animating bar, keyed by stat. The scrapbook screen
    # rebuilds whenever the sequencer advances; keeping the start time here
    # means a rebuilt LcReviewDelta/Tick carries on instead of restarting.
    lc_review_anim_clock = {}

    def lc_review_anim_start(key):
        import time
        return lc_review_anim_clock.setdefault(key, time.time())

    def lc_review_anim_begin(key):
        """Stamp a fresh wall-clock for the bar that is about to run. Always None
        so it is safe as a screen-timer Function action."""
        import time
        lc_review_anim_clock[key] = time.time()
        return None

    def lc_review_anim_reset():
        lc_review_anim_clock.clear()

    def lc_review_row_phase(index, seq_i, seq_phase, skipped):
        """Derive one row's visual phase from the single screen sequencer.

        Only one bar is ever in run/flash. Earlier bars are done; later bars
        wait. Per-row screen timers used to own their own delays — every
        SetDict rebuild restarted those timers, so bars overlapped or stalled.
        """
        if skipped or seq_phase == "done_all":
            return "done"
        if seq_phase == "lead" or index > seq_i:
            return "wait"
        if index < seq_i:
            return "done"
        if seq_phase in ("run", "flash"):
            return seq_phase
        return "wait"

    def lc_review_quote(text):
        text = (text or "").strip()
        if not text:
            return ""
        if text[0] in ('"', "\u201c"):
            return text
        return "\u201c" + text + "\u201d"

    def lc_review_pack_chips(chips, limit=700):
        """Wrap stat chips onto lines that fit the journal's right page."""
        rows = []
        current = []
        width = 0
        for chip in chips:
            shown = "{} {:+d}".format(chip["label"], chip["value"])
            # Silkscreen at the chip size is about 12px a glyph, plus the tick and padding.
            chip_width = 40 + 12 * len(shown)
            if current and width + chip_width > limit:
                rows.append(current)
                current = []
                width = 0
            current.append(dict(chip, text=shown))
            width += chip_width + 8
        if current:
            rows.append(current)
        return rows

    def _lc_review_content_root():
        gamedir = getattr(config, "gamedir", None)
        if gamedir and os.path.isdir(os.path.join(gamedir, "chapters")):
            return gamedir
        return None

    def _lc_read_expr(text, start):
        i = start
        while i < len(text) and text[i] in " \t\r\n":
            i += 1
        begin = i
        depth = 0
        quote = None
        while i < len(text):
            char = text[i]
            if quote:
                if char == "\\":
                    i += 2
                    continue
                if char == quote:
                    quote = None
                i += 1
                continue
            if char in ("'", '"'):
                quote = char
                i += 1
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    return text[begin:i], i
                depth -= 1
            elif char == "," and depth == 0:
                return text[begin:i], i
            i += 1
        raise ValueError("unclosed choice expression")

    def _lc_eval_choice_expr(expr):
        import ast
        names = {
            "girlfriend_name": "{girlfriend}",
            "friend_name": "{friend}",
            "player_name": "{player}",
        }
        tree = ast.parse(expr, mode="eval")

        def walk(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                return node.value
            if isinstance(node, ast.Name):
                if node.id not in names:
                    raise ValueError(node.id)
                return names[node.id]
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                return walk(node.left) + walk(node.right)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "format":
                base = walk(node.func.value)
                args = [walk(arg) for arg in node.args]
                return base.format(*args)
            raise ValueError("unsupported choice text")

        value = walk(tree.body)
        if not isinstance(value, str) or not value.strip():
            raise ValueError("empty choice text")
        return value.strip()

    def _lc_review_scan_choices(root):
        if not root:
            return {}
        chapters = os.path.join(root, "chapters")
        if not os.path.isdir(chapters):
            return {}
        found = {}
        calls = ("format_choice", "format_day2_risk_choice", "format_day4_gate_choice", "format_day5_gate_choice")
        for dirpath, _dirs, files in os.walk(chapters):
            for name in files:
                if not name.endswith(".rpy"):
                    continue
                path = os.path.join(dirpath, name)
                try:
                    with open(path, "r", encoding="utf-8") as handle:
                        text = handle.read()
                except OSError:
                    continue
                for call in calls:
                    needle = call + "("
                    start = 0
                    while True:
                        at = text.find(needle, start)
                        if at < 0:
                            break
                        cursor = at + len(needle)
                        try:
                            id_expr, cursor = _lc_read_expr(text, cursor)
                            while cursor < len(text) and text[cursor] in " \t\r\n":
                                cursor += 1
                            if cursor >= len(text) or text[cursor] != ",":
                                raise ValueError("missing choice text")
                            text_expr, _end = _lc_read_expr(text, cursor + 1)
                            choice_id = _lc_eval_choice_expr(id_expr.strip())
                            value = _lc_eval_choice_expr(text_expr.strip())
                        except Exception:
                            start = at + len(needle)
                            continue
                        if choice_id and value and choice_id not in found:
                            found[choice_id] = value
                        start = at + len(needle)
        return found

    def lc_review_choice_catalog(root=None):
        """Player-facing choice lines, scanned from the story's format_choice calls."""
        global _lc_review_choice_catalog
        if root is not None:
            return _lc_review_scan_choices(root)
        if _lc_review_choice_catalog is None:
            _lc_review_choice_catalog = _lc_review_scan_choices(_lc_review_content_root())
        return _lc_review_choice_catalog

    def _lc_review_fill_names(text):
        names = {
            "{girlfriend}": getattr(store, "girlfriend_name", None) or "Leia",
            "{friend}": getattr(store, "friend_name", None) or "Julian",
            "{player}": getattr(store, "player_name", None) or "Ryan",
        }
        for token, value in names.items():
            text = text.replace(token, value)
        return text

    def _lc_review_humanize(choice_id):
        text = str(choice_id)
        for prefix in ("ch01_d1_", "ch01_d2_", "ch01_d3_", "ch01_d4_", "ch01_d5_", "ch01_d6_", "ch01_", "dev_"):
            if text.startswith(prefix):
                text = text[len(prefix):]
                break
        text = text.replace("_", " ").strip()
        if not text or text == str(choice_id):
            return "A choice from today."
        if text[-1] not in ".?!":
            text += "."
        return text[0].upper() + text[1:]

    def lc_review_choice_text(choice_id):
        """Readable line for a recorded choice. Never the internal id."""
        raw = lc_review_choice_catalog().get(choice_id)
        if raw:
            return _lc_review_fill_names(raw)
        return _lc_review_humanize(choice_id)

    def lc_review_choice_details(day_id):
        rows = []
        for choice in store.lc_review_days.get(day_id, {}).get("choices", []):
            chips = []
            for _group, key, value in choice.get("deltas") or []:
                if not value:
                    continue
                name = STAT_LABELS.get(key, key.replace("_", " ").title())
                chips.append({"stat": key, "name": name, "label": name.upper(), "value": value})
            if not chips:
                continue
            rows.append({
                "text": lc_review_choice_text(choice["id"]),
                "chips": chips,
                "lines": lc_review_pack_chips(chips),
            })
        return rows

    # Review cue -> shared UI sound (game/audio/ui/) when no review sting exists.
    LC_REVIEW_UI_FALLBACK = {"tick": "bar", "paper": "polaroid"}

    def lc_review_sfx(name):
        """Play audio/sfx/review_<name>.ogg or .wav when it exists.

        Otherwise fall back to the UI sound kit (a bar settling -> ui/bar, a
        polaroid landing -> ui/polaroid). A missing file is silent, so the hook
        is safe to call when a polaroid lands or a bar settles.
        Always returns None: it runs as a screen-timer Function action, and
        any non-None return would end `call screen` and close the review.
        """
        try:
            for ext in (".ogg", ".wav"):
                path = "audio/sfx/review_{}{}".format(name, ext)
                if renpy.loadable(path):
                    renpy.sound.play(path)
                    return None
            lc_ui_sound(LC_REVIEW_UI_FALLBACK.get(name, name))
        except Exception:
            return None
        return None

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
    # Night first, then the journal. A click during the night skips every
    # animation and opens the scrapbook already settled.
    $ lc_review_skipped = False
    $ lc_review_anim_reset()
    if persistent.lc_recap_animation:
        call screen lc_review_night_screen(day_id)
        $ lc_review_skipped = (_return == "skip")
    call screen lc_day_review_screen(day_id, skipped=lc_review_skipped)
    $ phone_hud_enabled = lc_review_saved_hud
    $ quick_menu = lc_review_saved_quick
    window auto
    return
