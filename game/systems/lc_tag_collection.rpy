# Tag collection - earned review tags and stickers, and equipping tags
#
# Purpose: Every tag and moment sticker shown on an end-of-day review is unlocked permanently
#   (across saves). The TAGS page lets the player equip one of Ryan's and one of Leia's tags, or
#   leave them Automatic; the equipped tag replaces the automatic one on Status, the review card and
#   sprite badges. Equipping never changes route, facts or stats.
#
# Public API (call these from scenes/screens):
#   lc_current_titles()                       latest finished day's (ryan, leia) titles, equipped
#       ones applied
#   lc_tag_list(who)                          [(tag, earned)] for 'ryan' or 'leia' in catalog order
#   lc_sticker_list()                         [(sticker, earned)]
#   lc_tag_equipped(who)                      equipped tag for who, or None (Automatic)
#   lc_tag_equip(who, tag=None) -> None       equip an earned tag; None returns to Automatic
#   lc_tag_is_earned(who, tag)                True once who:tag is earned
#   lc_tags_earned_set()                      set of 'who:tag' strings
#   lc_tags_apply(auto)                       swap equipped tags into an automatic (ryan, leia) pair
#   lc_tags_unlock_pair(titles, stickers=()) -> None
#       mark titles and stickers earned
#   lc_tags_unlock_finished_day(day_id) -> None
#       review_finished hook: unlock a day's tags/stickers
#   LC_TAG_CATALOG                            {who: [tag, ...]} display order
#   default persistent.lc_tags_earned         earned 'who:tag' strings
#   default persistent.lc_stickers_earned     earned sticker names
#   default persistent.lc_tag_equipped        {who: tag or None}
#
# Example:
#   action Function(lc_tag_equip, who, tag)      (screens/tag_collection_screen.rpy)
#
# Depends on: systems/day_review.rpy (titles, stickers, LC_STYLE_TAGS), systems/lc_hooks.rpy
# Hooks: listens to review_finished (unlock) and filters review_titles (equipped tags)
# Load order: init 21: right after systems/day_review.rpy (init 20), whose tables it reads
# Docs: docs/DAY_REVIEW.md   Tests: tests/test_tag_collection.py, tests/test_review_tags.py

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
