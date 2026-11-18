"""Stat model v2 (darryn, 2026-11-08): pure Python, no Ren'Py imports.

Five player-facing stats, one display name each in every mode and screen:

    Love           how close and cared-for she feels           (Love family)
    Trust          honesty and agreeing things together        (gates NTS steps, NTR repair)
    Exhibitionism  how much they both enjoy her being seen     (Love + Exhibitionism, NTS)
    Sharing        agreed openness to someone else joining in  (NTS; never NTR)
    Temptation     drift, secrets and restlessness             (NTR)

Retired: boredom, curiosity, acceptance, secrecy, boundary_looseness, momentum,
jealousy (folded into the five above, or dropped). The route checks, the Full
"Current lean" readout, the choice route tag, the save migration and the tests
all read this module, so they cannot disagree.
"""

STAT_ORDER = ("love", "trust", "exhibitionism", "sharing", "temptation")

STAT_LABELS = {
    "love": "Love",
    "trust": "Trust",
    "exhibitionism": "Exhibitionism",
    "sharing": "Sharing",
    "temptation": "Temptation",
}

# Save-state dictionary each stat lives in (store.<group>_stats).
STAT_GROUPS = {
    "love": "relationship",
    "trust": "relationship",
    "sharing": "relationship",
    "temptation": "relationship",
    "exhibitionism": "partner",
}

DEFAULTS = {
    "relationship": {"love": 50, "trust": 50, "sharing": 0, "temptation": 10},
    "partner": {"exhibitionism": 10},
    "player": {},
}

# The route each route stat leans toward when it goes up.
ROUTE_STATS = {"exhibitionism": "Love+Exhib", "sharing": "NTS", "temptation": "NTR"}

# Old stat id -> new stat id (None = retired, dropped).
LEGACY_FOLD = {
    "love": "love",
    "trust": "trust",
    "curiosity": "exhibitionism",
    "exhibitionism": "exhibitionism",
    "acceptance": "exhibitionism",
    "boredom": "temptation",
    "temptation": "temptation",
    "secrecy": "temptation",
    "boundary_looseness": "temptation",
    "momentum": None,
    "jealousy": None,
}
RETIRED_STATS = ("boredom", "curiosity", "acceptance", "secrecy", "boundary_looseness", "momentum", "jealousy")

# Route thresholds. Day 1-2 are scaled from the old numbers (Exhibitionism climbs
# about 2.2x faster) and tuned with tests/test_route_simulation.py. Temptation
# thresholds count slips (choice-sense pass, darryn 2026-11-08): an ordinary slip
# is Temptation +1 from the default 10, so one slip never seeds NTR and three do.
# Day 3+ lanes still come from stored values.
THRESHOLDS = {}  # each Day's STAT_THRESHOLDS in lc_days/<day>.py (added at import, in play order)

# Choices that write a route value or are gate-formatted. Used for the derived
# Full route tag and for the scoring rule (gates may move up to 5; hard gates
# may move three stats).
CHOICE_GATES = {}  # each Day's STAT_CHOICE_GATES in lc_days/<day>.py (added at import)

# Route value the branch writes: "locks" (ntr_confirmed), "stays_open"
# (ntr_unresolved), "may_lead" (soft gate or mixed_unresolved). "lean" stamps the plain
# lean even for a one-step slip (Leia's walk-back "keep it" is her NTR-side pick, K4).
CHOICE_ROUTE_FLAGS = {}  # each Day's STAT_ROUTE_FLAGS in lc_days/<day>.py (added at import)

# Repair beats: the only choices allowed to pair Temptation down with Love/Trust up.
REPAIR_CHOICES = frozenset()  # each Day's STAT_REPAIR_CHOICES in lc_days/<day>.py (added at import)

TAGS = ("Love", "Love+Exhib", "NTS", "NTR", "May lead to NTR", "Locks NTR",
        "NTR stays open", "Repair", "Repair, NTR stays open", "Neutral")

LEAN_LABELS = {
    "love": "Love",
    "love_exhib": "Love+Exhib",
    "nts": "NTS",
    "ntr": "NTR",
    "strained": "Love (strained)",
    "undecided": "Undecided",
}


def clamp(value):
    return max(0, min(100, int(round(value))))


# ---------------------------------------------------------------- effects

def effect_deltas(effects):
    """{stat: total} for a list of (group, stat, amount) tuples."""
    out = {}
    for _group, stat, amount in effects:
        out[stat] = out.get(stat, 0) + int(amount)
    return out


def fold_legacy_effects(effects):
    """Runtime safety net: map old-stat tuples onto the five stats.

    Folded parts move by max(part) (+1 when two or more parts move the same way);
    retired stats are dropped. New-style tuples pass through unchanged.
    tests/test_choice_scoring.py still fails on any legacy tuple in the data.
    """
    if all(stat in STAT_GROUPS and STAT_GROUPS[stat] == group for group, stat, _ in effects):
        return list(effects)
    parts = {}
    for _group, stat, amount in effects:
        target = LEGACY_FOLD.get(stat, stat if stat in STAT_GROUPS else None)
        if target:
            parts.setdefault(target, []).append(int(amount))
    out = []
    for stat in STAT_ORDER:
        values = parts.get(stat)
        if not values:
            continue
        if stat in ("love", "trust"):
            total = sum(values)
        else:
            pos = [v for v in values if v > 0]
            neg = [v for v in values if v < 0]
            total = 0
            if pos:
                total += max(pos) + (1 if len(pos) > 1 else 0)
            if neg:
                total += min(neg) - (1 if len(neg) > 1 else 0)
        if total:
            out.append((STAT_GROUPS[stat], stat, total))
    return out


def lean_of(deltas):
    """Route direction of one choice from its stat deltas."""
    if deltas.get("temptation", 0) > 0:
        return "NTR"
    if deltas.get("sharing", 0) > 0:
        return "NTS"
    if deltas.get("exhibitionism", 0) > 0:
        return "Love+Exhib"
    if deltas.get("temptation", 0) < 0 and (deltas.get("love", 0) > 0 or deltas.get("trust", 0) > 0):
        return "Repair"
    if deltas.get("love", 0) > 0 or deltas.get("trust", 0) > 0:
        return "Love"
    if not any(deltas.values()):
        return "Neutral"
    if deltas.get("temptation", 0) < 0 and not any(v for k, v in deltas.items() if k != "temptation"):
        return "Love"
    return None


def route_tag(effects, route_flag=None):
    """Full Transparency tag for a choice, derived from its effects (never hand-typed)."""
    lean = lean_of(effect_deltas(effects))
    if lean is None:
        return None
    if route_flag == "locks":
        return "Locks NTR"
    if route_flag == "stays_open":
        return "NTR stays open" if lean == "NTR" else "Repair, NTR stays open"
    if route_flag == "may_lead":
        return "May lead to NTR"
    if route_flag == "lean":
        return lean
    if lean == "NTR" and effect_deltas(effects).get("temptation", 0) == 1:
        # A one-step slip (Temptation +1) only leans toward NTR; several of them
        # are what open it (darryn's slow burn, choice-sense pass).
        return "May lead to NTR"
    return lean


def choice_route_tag(choice_id, effects):
    return route_tag(effects, CHOICE_ROUTE_FLAGS.get(choice_id))


# Full Transparency path stamp on the choice card: the derived tag above, written
# small, plus the colour meaning it shares with the stat deltas (delta_kind):
# good = Love family (green), bad = toward NTR (red), exhibitionism = pink,
# sharing = purple. Neutral choices get no stamp. "->" is drawn as an arrow glyph
# by the screen (in a font that has one).
PATH_STAMPS = {
    "Love": ("-> Love", "good"),
    "Love+Exhib": ("-> Love+Exhib", "exhibitionism"),
    "NTS": ("-> NTS", "sharing"),
    "NTR": ("-> NTR", "bad"),
    "May lead to NTR": ("may lead to NTR", "bad"),
    "Locks NTR": ("locks NTR", "bad"),
    "NTR stays open": ("NTR stays open", "bad"),
    "Repair": ("Repair", "good"),
    "Repair, NTR stays open": ("Repair, NTR stays open", "good"),
    "Neutral": None,
}

# Tags that pull toward NTR. Gate formatters keep their warning diamond only for these.
NTR_TAGS = frozenset(("NTR", "May lead to NTR", "Locks NTR", "NTR stays open"))


def path_stamp(tag):
    """(text, colour kind) for a route tag, or None (Neutral / no tag)."""
    return PATH_STAMPS.get(tag)


def choice_path_stamp(choice_id, effects):
    return path_stamp(choice_route_tag(choice_id, effects))


def effects_from_chips(chips):
    """Rebuild (group, stat, amount) effects from exact stat-line chips.

    Only for captions that carry no choice id (literal test captions); real story
    captions carry the id and use the registered effects.
    """
    out = []
    for name, amount, exact in chips:
        stat = stat_id_for_label(name)
        if not exact or stat not in STAT_GROUPS or not amount:
            return None
        out.append((STAT_GROUPS[stat], stat, int(amount)))
    return out


def scoring_violations(choice_id, effects):
    """Every way a choice breaks the scoring rule (empty list = OK).

    1. Only the five stats, each in its own group, each listed once.
    2. At most 2 stats (hard gates: 3). Deltas within +-3 (gates: +-5).
    3. At most one route stat (Exhibitionism, Sharing, Temptation).
    4. Temptation up never sits with any stat going up.
    5. Allowed shapes only: Love (Love/Trust up), Love+Exhib (Exhibitionism up,
       optional Love/Trust up), NTS (Sharing up, optional Trust up), NTR
       (Temptation up, optional Love or Trust down; hard gates both), Repair
       (Temptation down + Love or Trust up, repair beats only), Temptation down
       alone, or Neutral (no stats).
    6. A route tag can be derived.
    """
    bad = []
    gate = CHOICE_GATES.get(choice_id)
    seen = set()
    for item in effects:
        if len(item) != 3:
            bad.append("malformed effect {!r}".format(item))
            continue
        group, stat, amount = item
        if stat not in STAT_GROUPS:
            bad.append("unknown or retired stat '{}'".format(stat))
            continue
        if STAT_GROUPS[stat] != group:
            bad.append("'{}' belongs to group '{}', not '{}'".format(stat, STAT_GROUPS[stat], group))
        if stat in seen:
            bad.append("'{}' listed twice".format(stat))
        seen.add(stat)
        if not isinstance(amount, int) or amount == 0:
            bad.append("'{}' needs a non-zero whole number".format(stat))
        cap = 5 if gate else 3
        if isinstance(amount, int) and abs(amount) > cap:
            bad.append("'{}' {:+d} is over the cap of {}".format(stat, amount, cap))
    if bad:
        return bad
    d = effect_deltas(effects)
    limit = 3 if gate == "hard" else 2
    if len(d) > limit:
        bad.append("{} stats (max {})".format(len(d), limit))
    routes = [s for s in ("exhibitionism", "sharing", "temptation") if s in d]
    if len(routes) > 1:
        bad.append("more than one route stat: {}".format(", ".join(routes)))
    ups = [s for s, v in d.items() if v > 0]
    if d.get("temptation", 0) > 0 and len(ups) > 1:
        bad.append("Temptation up together with another stat going up")
    shape_ok = False
    lt = {k: v for k, v in d.items() if k in ("love", "trust")}
    if not d:
        shape_ok = True
    elif not routes:
        shape_ok = all(v > 0 for v in lt.values())
    elif routes == ["exhibitionism"]:
        shape_ok = d["exhibitionism"] > 0 and all(v > 0 for v in lt.values())
    elif routes == ["sharing"]:
        shape_ok = d["sharing"] > 0 and "love" not in d and all(v > 0 for v in lt.values())
    elif routes == ["temptation"]:
        if d["temptation"] > 0:
            shape_ok = all(v < 0 for v in lt.values()) and (len(lt) <= 1 or gate == "hard")
        else:
            shape_ok = (not lt) or (choice_id in REPAIR_CHOICES and len(lt) == 1 and all(v > 0 for v in lt.values()))
    if not shape_ok:
        bad.append("shape not allowed: {}".format(", ".join("{} {:+d}".format(STAT_LABELS[k], v) for k, v in sorted(d.items()))))
    if choice_route_tag(choice_id, effects) is None:
        bad.append("no route tag can be derived")
    return bad


def delta_kind(stat, amount):
    """Colour meaning of a stat change: 'good', 'bad', or the route stat id.

    Love/Trust up = good, down = bad. Temptation up = bad (toward NTR), down = good.
    Exhibitionism and Sharing are directions, not good or bad: they keep their
    own route colour either way.
    """
    if not amount:
        return None
    if stat in ("exhibitionism", "sharing"):
        return stat
    if stat == "temptation":
        return "bad" if amount > 0 else "good"
    return "good" if amount > 0 else "bad"


# Suffix on a stat label whose gain Leia's daily cap cut ("Love (capped)"; docs/LEIA_SIDE.md).
CAPPED_SUFFIX = " (capped)"


def stat_id_for_label(label):
    # "Love (capped)" (a Leia-side gain cut by her daily cap) keeps Love's colour.
    key = (label or "").strip().lower()
    suffix = CAPPED_SUFFIX.strip()
    if key.endswith(suffix):
        key = key[:-len(suffix)].strip()
    for stat, name in STAT_LABELS.items():
        if name.lower() == key:
            return stat
    return key.replace(" ", "_")


# ---------------------------------------------------------------- routes

def lean_from_route_value(value):
    """Lean key for a stored lane / end state (Day 2 onward)."""
    if value in ("love", "love_repaired", "mixed", "love_private"):
        return "love"
    if value in ("exhibitionism", "nts_seeded"):
        return "love_exhib"
    if value == "mixed_unresolved":
        return "strained"
    if value in ("ntr", "ntr_risk", "ntr_seeded", "ntr_confirmed", "ntr_unresolved", "ntr_repaired"):
        return "ntr"
    return "undecided"


# ---------------------------------------------------------------- migration

def is_legacy_stats(relationship, partner, player=None):
    return any(k in (relationship or {}) for k in ("boredom", "momentum")) or any(
        k in (partner or {}) for k in ("curiosity", "secrecy", "boundary_looseness")
    ) or any(k in (player or {}) for k in ("jealousy", "acceptance"))


def migrate_stats(relationship, partner, player):
    """Old stat dicts -> (relationship, partner, player, legacy) under the v2 model.

    Love = love; Trust = trust;
    Exhibitionism = 10 + (exhibitionism - 10) + ((curiosity - 20) + (acceptance - 10)) / 2;
    Temptation = boredom + max(0, temptation - 10) + max(0, secrecy - 5)
                 + max(0, boundary_looseness - 10);
    Sharing = 0. Every value is clamped to 0-100.
    """
    rel = dict(relationship or {})
    par = dict(partner or {})
    ply = dict(player or {})
    legacy = {"relationship": dict(rel), "partner": dict(par), "player": dict(ply)}

    def g(d, k, default):
        try:
            return int(d.get(k, default))
        except (TypeError, ValueError):
            return default

    love = g(rel, "love", 50)
    trust = g(rel, "trust", 50)
    exhib = 10 + (g(par, "exhibitionism", 10) - 10) + ((g(par, "curiosity", 20) - 20) + (g(ply, "acceptance", 10) - 10)) / 2.0
    temptation = (
        g(rel, "boredom", 10)
        + max(0, g(par, "temptation", 10) - 10)
        + max(0, g(par, "secrecy", 5) - 5)
        + max(0, g(par, "boundary_looseness", 10) - 10)
    )
    new_rel = {"love": clamp(love), "trust": clamp(trust), "sharing": clamp(g(rel, "sharing", 0)), "temptation": clamp(temptation)}
    new_par = {"exhibitionism": clamp(exhib)}
    return new_rel, new_par, {}, legacy


def migrate_snapshot(snapshot):
    """Migrate a {group: {stat: value}} snapshot (e.g. a day-review start/end)."""
    if not snapshot or not is_legacy_stats(snapshot.get("relationship"), snapshot.get("partner"), snapshot.get("player")):
        return snapshot
    rel, par, ply, _legacy = migrate_stats(snapshot.get("relationship"), snapshot.get("partner"), snapshot.get("player"))
    return {"relationship": rel, "partner": par, "player": ply}


def migrate_deltas(deltas):
    """Old (group, stat, delta) review deltas -> v2 deltas (folded, retired dropped)."""
    if not deltas:
        return deltas
    if all(stat in STAT_GROUPS for _g, stat, _v in deltas) and not any(stat in RETIRED_STATS for _g, stat, _v in deltas):
        return list(deltas)
    return fold_legacy_effects([(g, s, v) for g, s, v in deltas if v])


# ---------------------------------------------------------------- Day packs
def _install_day_packs():
    """Add every Day's thresholds, gate and route-flag rows, repair choices and route resolvers
    (game/python-packages/lc_days/<day>.py), in play order. Runs once, at import."""
    global REPAIR_CHOICES
    import lc_days
    rest = dict(THRESHOLDS)  # thresholds not owned by a Day: after the Days', in play order
    THRESHOLDS.clear()
    for day in lc_days.modules():
        THRESHOLDS.update(getattr(day, "STAT_THRESHOLDS", {}))
        CHOICE_GATES.update(getattr(day, "STAT_CHOICE_GATES", {}))
        CHOICE_ROUTE_FLAGS.update(getattr(day, "STAT_ROUTE_FLAGS", {}))
        REPAIR_CHOICES = REPAIR_CHOICES | frozenset(getattr(day, "STAT_REPAIR_CHOICES", ()))
        for name in getattr(day, "STAT_MODEL_EXPORTS", ()):
            globals()[name] = getattr(day, name)
    THRESHOLDS.update(rest)


_install_day_packs()
