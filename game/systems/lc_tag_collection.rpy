## Tag collection (darryn): every tag and moment sticker shown on an end-of-day
## review is unlocked permanently (across all saves, like title-screen unlocks).
## The TAGS page in the in-game menu lets the player equip one of Ryan's tags and
## one of Leia's tags separately, or leave either slot on Automatic. The equipped
## tag replaces the automatic one on the Status screen, the day review card and
## the sprite title badges. Stickers are collectible only (view, not equip).
##
## Equipping never changes the story: route, facts and stats are untouched.

default persistent.lc_tags_earned = set()        # {"ryan:Her Bodyguard", "leia:Feeling Safe", ...}
default persistent.lc_stickers_earned = set()    # {"Asked First", ...}
default persistent.lc_tag_equipped = {}          # {"ryan": "Her Bodyguard", "leia": None}

init 21 python:

    # Display order on the TAGS page. Story-style titles first, then the
    # route/story-event titles. Anything earned that isn't listed (e.g. a Genre
    # title) is appended so it still shows.
    LC_TAG_CATALOG = {
        "ryan": [LC_STYLE_TAGS[s][0] for s in LC_STYLE_ORDER] + [LC_STYLE_MIXED[0],
                 "Curious Partner", "Devoted Boyfriend", "Knowing Accomplice", "Uneasy Observer",
                 "Giving Her Another Chance", "Rebuilding Trust", "Sharing Partner",
                 "Betrayed Boyfriend", "Walking Away"],
        "leia": [LC_STYLE_TAGS[s][1] for s in LC_STYLE_ORDER] + [LC_STYLE_MIXED[1],
                 "Affectionate Partner", "Enjoying the Attention", "Testing the Waters", "Growing Distant",
                 "Rebuilding Trust", "Making Amends", "Adventurous Partner",
                 "Unfaithful Lover", "Estranged Partner"],
    }

    def lc_tags_earned_set():
        earned = persistent.lc_tags_earned
        return set(earned) if earned else set()

    def lc_tag_is_earned(who, tag):
        return (who + ":" + tag) in lc_tags_earned_set()

    def lc_tag_list(who):
        """[(tag, earned)] in catalog order plus any extra earned tags."""
        earned = lc_tags_earned_set()
        seen, rows = set(), []
        for tag in LC_TAG_CATALOG.get(who, []):
            if tag not in seen:
                seen.add(tag)
                rows.append((tag, (who + ":" + tag) in earned))
        for key in sorted(earned):
            w, _, tag = key.partition(":")
            if w == who and tag not in seen:
                seen.add(tag)
                rows.append((tag, True))
        return rows

    def lc_sticker_list():
        earned = set(persistent.lc_stickers_earned or ())
        return [(name, name in earned) for name, _test in LC_MOMENT_STICKERS]

    def lc_tags_unlock_pair(titles, stickers=()):
        earned = lc_tags_earned_set()
        for who, tag in zip(("ryan", "leia"), titles):
            if tag:
                earned.add(who + ":" + tag)
        persistent.lc_tags_earned = earned
        if stickers:
            persistent.lc_stickers_earned = set(persistent.lc_stickers_earned or ()) | set(stickers)

    def lc_tag_equipped(who):
        eq = persistent.lc_tag_equipped or {}
        tag = eq.get(who)
        return tag if tag and lc_tag_is_earned(who, tag) else None

    def lc_tag_equip(who, tag=None):
        """Equip an earned tag for one slot; None returns it to Automatic. Returns None."""
        eq = dict(persistent.lc_tag_equipped or {})
        eq[who] = tag if (tag is None or lc_tag_is_earned(who, tag)) else eq.get(who)
        persistent.lc_tag_equipped = eq
        renpy.restart_interaction()

    def lc_tags_apply(auto):
        """Swap in the equipped tags. Title style Off still hides everything."""
        if not (auto and (auto[0] or auto[1])):
            return auto
        return (lc_tag_equipped("ryan") or auto[0], lc_tag_equipped("leia") or auto[1])

    # Hooks into the day review (systems/lc_hooks.rpy).
    # Unlock on every finished day: whatever the card shows automatically.
    def lc_tags_unlock_finished_day(day_id):
        """review_finished hook: unlock the day's automatic tags and moment stickers."""
        try:
            lc_tags_unlock_pair(lc_review_auto_titles(day_id), lc_review_stickers(day_id))
        except Exception:
            pass

    lc_hook_add("review_finished", lc_tags_unlock_finished_day)
    # The review card shows the equipped tags instead of the automatic ones.
    lc_hook_add("review_titles", lc_tags_apply)

    def lc_current_titles():
        """Status screen / title badges: latest finished day's tags, equipped ones applied."""
        latest = lc_review_latest()
        auto = lc_review_auto_titles(latest) if latest else lc_character_titles()
        return lc_tags_apply(auto)
