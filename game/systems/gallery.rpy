# Gallery logic: entry registry (built from systems/gallery_data.rpy), unlock rules,
# counts and QA helpers. Unlocks are player-wide and survive across save slots/new games.
#
# UNLOCK RULE (seen-image based, no story-script edits):
#   * a page is viewable when its CG has ever been shown on this profile
#     (renpy.seen_image(("cg", name)); Ren'Py records every show/scene of an image
#     in persistent._seen_images), OR when the whole entry was unlocked explicitly
#     (unlock_gallery(id), QA unlock-all);
#   * an entry is unlocked when any one of its pages is viewable. Later pages of a
#     partly seen sequence stay locked until they are seen.
# Unknown ids (old dev profiles, entries from a newer build) are ignored, never raised.

init python:

    GALLERY_CHAPTERS = ("prologue", "ch01")

    GALLERY_CHAPTER_LABELS = {
        "prologue": "Prologue",
        "ch01": "Chapter 1",
    }

    GALLERY_TAB_IDS = tuple(t[0] for t in GALLERY_TABS)

    # Card/preview tint per tab (used behind locked tiles and as the fallback fill).
    GALLERY_TAB_ACCENTS = {
        "prologue": "#6f617f",
        "ch01_d1": "#8f5d75",
        "ch01_d2": "#70566f",
        "ch01_d3": "#7c6258",
        "ch01_d4": "#556b78",
        "ch01_d5": "#5f7a6a",
    }

    def _gallery_build_entries():
        entries = {}
        tabs = dict((t[0], t) for t in GALLERY_TABS)
        orders = {}
        for row in GALLERY_TABLE:
            entry_id = row["id"]
            if entry_id in entries:
                raise Exception("Duplicate gallery id in GALLERY_TABLE: {}".format(entry_id))
            tab = row["tab"]
            if tab not in tabs:
                raise Exception("Gallery entry {} uses unknown tab {}".format(entry_id, tab))
            orders[tab] = orders.get(tab, 0) + 1
            pages = []
            for page in row["pages"]:
                if isinstance(page, str):
                    image, label = page, None
                else:
                    image, label = page
                pages.append({"image": image, "label": label or image})
            entries[entry_id] = {
                "id": entry_id,
                "tab": tab,
                "chapter": tabs[tab][2],
                "day": tabs[tab][3],
                "order": orders[tab],
                "title": row["title"],
                "description": row["description"],
                "pages": pages,
                "mature": bool(row.get("mature")),
                "dream": bool(row.get("dream")),
                "route": row.get("route") or "All routes",
                "asset_id": "cg " + pages[0]["image"],
                "replay_label": None,
                "accent": GALLERY_TAB_ACCENTS.get(tab, "#6f617f"),
            }
        return entries

    GALLERY_ENTRIES = _gallery_build_entries()

    # Grid shows a masked cover (no image) for mature entries until they are opened.
    GALLERY_MASK_MATURE_COVERS = True

    # ---------------------------------------------------------------- lookups
    def get_gallery_entry(gallery_id):
        """The entry dict, or None for an unknown id. Never raises."""
        return GALLERY_ENTRIES.get(gallery_id)

    def gallery_has_entry(gallery_id):
        return gallery_id in GALLERY_ENTRIES

    def gallery_chapter_label(chapter_id):
        return GALLERY_CHAPTER_LABELS.get(chapter_id, str(chapter_id).upper())

    def gallery_tab_label(tab_id):
        for t in GALLERY_TABS:
            if t[0] == tab_id:
                return t[1]
        return str(tab_id)

    def gallery_ids_for_tab(tab_id):
        ids = [i for i, e in GALLERY_ENTRIES.items() if e["tab"] == tab_id]
        return sorted(ids, key=lambda i: GALLERY_ENTRIES[i]["order"])

    def gallery_ids_for_chapter(chapter_id):
        ids = []
        for t in GALLERY_TABS:
            if t[2] == chapter_id:
                ids.extend(gallery_ids_for_tab(t[0]))
        return ids

    def gallery_all_ids():
        ids = []
        for t in GALLERY_TABS:
            ids.extend(gallery_ids_for_tab(t[0]))
        return ids

    # ------------------------------------------------------------- unlock state
    def _gallery_unlock_list():
        unlocked = getattr(renpy.store.persistent, "gallery_unlocked", None)
        if unlocked is None:
            unlocked = []
            renpy.store.persistent.gallery_unlocked = unlocked
        return unlocked

    def gallery_explicitly_unlocked(gallery_id):
        return gallery_id in _gallery_unlock_list()

    def gallery_image_seen(image_name):
        return bool(renpy.seen_image(("cg", image_name)))

    def gallery_page_available(gallery_id, page_index):
        entry = get_gallery_entry(gallery_id)
        if entry is None or page_index < 0 or page_index >= len(entry["pages"]):
            return False
        if gallery_explicitly_unlocked(gallery_id):
            return True
        return gallery_image_seen(entry["pages"][page_index]["image"])

    def gallery_available_pages(gallery_id):
        entry = get_gallery_entry(gallery_id)
        if entry is None:
            return []
        return [i for i in range(len(entry["pages"])) if gallery_page_available(gallery_id, i)]

    def is_gallery_unlocked(gallery_id):
        """True when the entry is known and at least one page is viewable."""
        if not gallery_has_entry(gallery_id):
            return False
        return bool(gallery_available_pages(gallery_id))

    def unlock_gallery(gallery_id):
        """Explicitly unlock one whole entry (manual/dev use; the story does not call this).

        Unknown ids are ignored and return False instead of raising."""
        if not gallery_has_entry(gallery_id):
            return False
        unlocked = _gallery_unlock_list()
        if gallery_id not in unlocked:
            unlocked.append(gallery_id)
            renpy.save_persistent()
        renpy.restart_interaction()
        return True

    def gallery_unlocked_count(chapter_id=None, tab_id=None):
        if tab_id is not None:
            ids = gallery_ids_for_tab(tab_id)
        elif chapter_id is not None:
            ids = gallery_ids_for_chapter(chapter_id)
        else:
            ids = gallery_all_ids()
        return sum(1 for i in ids if is_gallery_unlocked(i))

    def gallery_total_count(chapter_id=None, tab_id=None):
        if tab_id is not None:
            return len(gallery_ids_for_tab(tab_id))
        if chapter_id is not None:
            return len(gallery_ids_for_chapter(chapter_id))
        return len(gallery_all_ids())

    def gallery_pages_counts(gallery_id):
        """(viewable pages, total pages)."""
        entry = get_gallery_entry(gallery_id)
        if entry is None:
            return (0, 0)
        return (len(gallery_available_pages(gallery_id)), len(entry["pages"]))

    # ----------------------------------------------------------------- display
    def gallery_customize_names(text):
        """Substitute customized cast names in static gallery descriptions."""
        for original, replacement in (("Ryan", store.player_name), ("Leia", store.girlfriend_name), ("Julian", store.friend_name)):
            text = text.replace(original, replacement)
        return text

    def gallery_display_title(gallery_id):
        entry = get_gallery_entry(gallery_id)
        if entry is None or not is_gallery_unlocked(gallery_id):
            return "Locked CG"
        return gallery_customize_names(entry["title"])

    def gallery_display_description(gallery_id):
        entry = get_gallery_entry(gallery_id)
        if entry is None or not is_gallery_unlocked(gallery_id):
            return "Discover this scene in the story to unlock it here."
        return gallery_customize_names(entry["description"])

    def gallery_has_replay(gallery_id):
        entry = get_gallery_entry(gallery_id)
        return bool(entry and entry.get("replay_label"))

    def gallery_is_placeholder(image_name):
        return image_name in GALLERY_PLACEHOLDER_IMAGES

    def gallery_art_state(gallery_id):
        """'final', 'partial' or 'pending' (all pages are still placeholder art)."""
        entry = get_gallery_entry(gallery_id)
        if entry is None:
            return "final"
        flags = [gallery_is_placeholder(p["image"]) for p in entry["pages"]]
        if all(flags):
            return "pending"
        if any(flags):
            return "partial"
        return "final"

    def gallery_first_page(gallery_id):
        pages = gallery_available_pages(gallery_id)
        return pages[0] if pages else 0

    def gallery_cover_image(gallery_id):
        """Stable image name of the first viewable page, or None while locked."""
        entry = get_gallery_entry(gallery_id)
        pages = gallery_available_pages(gallery_id)
        if entry is None or not pages:
            return None
        return entry["pages"][pages[0]]["image"]

    def gallery_card_masked(gallery_id):
        entry = get_gallery_entry(gallery_id)
        return bool(entry and entry["mature"] and GALLERY_MASK_MATURE_COVERS)

    def gallery_neighbor_page(gallery_id, current, step):
        """Next/previous viewable page index, wrapping; stays put when there is only one."""
        pages = gallery_available_pages(gallery_id)
        if not pages:
            return current
        if current not in pages:
            return pages[0]
        return pages[(pages.index(current) + step) % len(pages)]

    def gallery_thumb(image_name, width, height):
        """Fit the stable `cg <name>` image inside a box (placeholder or final art alike)."""
        return Transform(ImageReference(("cg", image_name)), fit="contain", xysize=(width, height))

    def gallery_grid_rows(tab_id, columns=3):
        ids = gallery_ids_for_tab(tab_id)
        return [ids[index:index + columns] for index in range(0, len(ids), columns)]

    # --------------------------------------------------------------- validation
    def gallery_validate():
        """Return a list of problems (empty = OK): missing images, shared images, bad placeholders."""
        problems = []
        seen_in = {}
        for gallery_id, entry in GALLERY_ENTRIES.items():
            for page in entry["pages"]:
                image = page["image"]
                if not renpy.has_image("cg " + image):
                    problems.append("{}: image 'cg {}' is not defined".format(gallery_id, image))
                if image in seen_in:
                    problems.append("{}: image {} also used by {}".format(gallery_id, image, seen_in[image]))
                seen_in[image] = gallery_id
        for image in GALLERY_PLACEHOLDER_IMAGES:
            if image not in seen_in:
                problems.append("placeholder list names {} which no entry uses".format(image))
        return problems

    # ------------------------------------------------------------------ QA tools
    def gallery_qa_tools_enabled():
        """QA-only gallery tools (unlock all / reset) follow the Chapter Select rule.

        They appear only in developer mode, and never when CHAPTER_SELECT_RULE is "never";
        a distribution build (config.developer False) never shows them, even with rule "always"."""
        return bool(config.developer) and store.CHAPTER_SELECT_RULE != "never"

    def debug_unlock_gallery_entry(gallery_id):
        unlock_gallery(gallery_id)
        renpy.notify("Gallery entry unlocked for testing.")

    def debug_unlock_all_gallery():
        renpy.store.persistent.gallery_unlocked = list(gallery_all_ids())
        renpy.save_persistent()
        renpy.notify("All gallery entries unlocked (QA).")
        renpy.restart_interaction()

    def debug_reset_seen_cgs():
        """Mark every gallery CG as not seen (they count as seen from any earlier play on this profile)."""
        for entry in GALLERY_ENTRIES.values():
            for page in entry["pages"]:
                renpy.mark_image_unseen(("cg", page["image"]))
        renpy.save_persistent()

    def debug_reset_gallery():
        renpy.store.persistent.gallery_unlocked = []
        debug_reset_seen_cgs()
        renpy.notify("Gallery unlocks and seen CGs reset.")
        renpy.restart_interaction()
