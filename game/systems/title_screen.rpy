# Title screen ("Golden Hour + Memory Reel", darryn 2026-11-06).
# Logic for screens/title_screen.rpy: the Continue card and the scrolling
# polaroid reel of unlocked gallery memories.
#
# Content rule: by default the reel only shows entries listed in
# LC_TITLE_SAFE_GALLERY (non-explicit moments). Players can switch to every
# unlocked memory with the chip above the reel (persistent.lc_title_all_memories).
# New gallery entries stay OFF the default reel until they are added here.

default persistent.lc_title_all_memories = False

init python:

    import time as _lc_time

    LC_TITLE_SAFE_GALLERY = (
        "pro_party_meet", "pro_first_kiss", "pro_four_years_on", "pro_departure",
        "d1_arrival", "d1_swimsuit_choice", "d1_pool_sunscreen", "d1_pool_photos",
        "d1_dress_reveal", "d1_drive_to_dinner", "d1_dinner_arrival", "d1_walk_back",
        "d1_trip_catch", "d1_drive_back", "d1_julian_carry", "d1_night_pool",
        "d1_julian_drink", "d1_movie_night", "d1_wake_up",
        "d2_photo_leia_maya", "d2_boutique",
        "d4_market_photo", "d4_photo_hunt",
        "d5_snorkel", "d5_cove_lunch", "d5_sunset_deck", "d5_invitation",
    )

    LC_TITLE_REEL_MIN = 9      # pad with "not yet..." cards up to this many
    LC_TITLE_REEL_MAX = 14     # cap (each card holds a full CG texture)
    LC_TITLE_REEL_STEP = 248   # card pitch in px (card art width incl. shadow)
    LC_TITLE_REEL_SPEED = 34.0 # px per second
    LC_TITLE_TILTS = (-5, 4, -3, 6, -4, 3, -6, 5, -2, 4, -5, 3, -3, 6)

    _lc_title_reel_cache = {}

    def lc_title_reel_cards(show_all=False):
        """One card per unlocked entry (a random viewable page), shuffled, padded with locked cards.

        Cached per (filter, seen-image count) so redraws don't reshuffle, but new
        unlocks show up the next time the title screen is built."""
        seen = len(getattr(persistent, "_seen_images", None) or ())
        key = (bool(show_all), seen, len(persistent.gallery_unlocked or ()))
        if key in _lc_title_reel_cache:
            return _lc_title_reel_cache[key]

        rng = renpy.random.Random()
        cards = []
        for gallery_id in sorted(GALLERY_ENTRIES):
            if not show_all and gallery_id not in LC_TITLE_SAFE_GALLERY:
                continue
            entry = GALLERY_ENTRIES[gallery_id]
            pages = [i for i in gallery_available_pages(gallery_id)
                     if entry["pages"][i]["image"] not in GALLERY_PLACEHOLDER_IMAGES
                     and renpy.has_image(("cg", entry["pages"][i]["image"]))]
            if not pages:
                continue
            page = entry["pages"][rng.choice(pages)]
            cards.append({
                "id": gallery_id,
                "image": page["image"],
                "title": gallery_customize_names(entry["title"]),
                "locked": False,
            })
        rng.shuffle(cards)
        cards = cards[:LC_TITLE_REEL_MAX]
        while len(cards) < LC_TITLE_REEL_MIN:
            cards.append({"id": None, "image": None, "title": "not yet...", "locked": True})
        for index, card in enumerate(cards):
            card["tilt"] = LC_TITLE_TILTS[index % len(LC_TITLE_TILTS)]
            card["lift"] = 14 if index % 2 else 0
        _lc_title_reel_cache.clear()
        _lc_title_reel_cache[key] = cards
        return cards

    def lc_title_reel_seconds(count):
        return max(10.0, count * LC_TITLE_REEL_STEP / LC_TITLE_REEL_SPEED)

    def lc_title_photo(image_name):
        return Transform(ImageReference(("cg", image_name)), fit="cover", xysize=(188, 150))

    def lc_title_continue_slot():
        """Newest real save (manual, auto or quick), or None on a fresh install."""
        try:
            return renpy.newest_slot(r"(\d+|auto|quick)-\d+$")
        except Exception:
            return None

    def lc_title_ago(slot):
        try:
            mtime = renpy.slot_mtime(slot)
        except Exception:
            mtime = None
        if not mtime:
            return ""
        minutes = int(max(0, _lc_time.time() - mtime) // 60)
        if minutes < 1:
            return "just now"
        if minutes < 60:
            return "{} min ago".format(minutes)
        hours = minutes // 60
        if hours < 24:
            return "{} h ago".format(hours)
        days = hours // 24
        return "{} day{} ago".format(days, "" if days == 1 else "s")

    def lc_title_continue_label(slot):
        name = ""
        try:
            name = (renpy.slot_json(slot) or {}).get("_save_name") or ""
        except Exception:
            name = ""
        kind = "Autosave" if slot.startswith("auto") else ("Quick save" if slot.startswith("quick") else "Save")
        parts = [p for p in (name or kind, lc_title_ago(slot)) if p]
        return "  \u00b7  ".join(parts)

    def lc_title_version():
        version = config.version or ""
        if version.startswith("dev") and not config.developer:
            return ""
        return version if version.startswith("dev") else "v" + version
