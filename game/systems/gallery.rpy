# Gallery metadata and persistent unlock helpers.
# Unlocks are player-wide and intentionally survive across save slots/new games.

init python:

    GALLERY_CHAPTERS = ("ch01", "ch02")

    GALLERY_CHAPTER_LABELS = {
        "ch01": "Chapter 1",
        "ch02": "Chapter 2",
    }

    # Placeholder entries prove the gallery architecture before final CGs exist.
    # Titles/descriptions can be replaced later without changing unlock IDs.
    GALLERY_ENTRIES = {
        "ch01_cg01": {
            "chapter": "ch01",
            "order": 1,
            "title": "Chapter 1 — CG 01",
            "description": "Placeholder gallery entry for a future Chapter 1 scene.",
            "asset_id": "gallery_ch01_cg01",
            "replay_label": None,
            "accent": "#8f5d75",
        },
        "ch01_cg02": {
            "chapter": "ch01",
            "order": 2,
            "title": "Chapter 1 — CG 02",
            "description": "Placeholder gallery entry for a future Chapter 1 scene.",
            "asset_id": "gallery_ch01_cg02",
            "replay_label": None,
            "accent": "#6f617f",
        },
        "ch01_cg03": {
            "chapter": "ch01",
            "order": 3,
            "title": "Chapter 1 — CG 03",
            "description": "Placeholder gallery entry for a future Chapter 1 scene.",
            "asset_id": "gallery_ch01_cg03",
            "replay_label": None,
            "accent": "#70566f",
        },
        "ch01_cg04": {
            "chapter": "ch01",
            "order": 4,
            "title": "Chapter 1 — CG 04",
            "description": "Placeholder gallery entry for a future Chapter 1 scene.",
            "asset_id": "gallery_ch01_cg04",
            "replay_label": None,
            "accent": "#7c6258",
        },
        "ch02_cg01": {
            "chapter": "ch02",
            "order": 1,
            "title": "Chapter 2 — CG 01",
            "description": "Placeholder gallery entry for a future Chapter 2 scene.",
            "asset_id": "gallery_ch02_cg01",
            "replay_label": None,
            "accent": "#556b78",
        },
        "ch02_cg02": {
            "chapter": "ch02",
            "order": 2,
            "title": "Chapter 2 — CG 02",
            "description": "Placeholder gallery entry for a future Chapter 2 scene.",
            "asset_id": "gallery_ch02_cg02",
            "replay_label": None,
            "accent": "#716054",
        },
    }


    def get_gallery_entry(gallery_id):
        if gallery_id not in GALLERY_ENTRIES:
            raise ValueError("Unknown gallery ID: {}".format(gallery_id))
        return GALLERY_ENTRIES[gallery_id]


    def gallery_chapter_label(chapter_id):
        return GALLERY_CHAPTER_LABELS.get(chapter_id, chapter_id.upper())


    def gallery_ids_for_chapter(chapter_id):
        ids = [
            gallery_id for gallery_id, entry in GALLERY_ENTRIES.items()
            if entry["chapter"] == chapter_id
        ]
        return sorted(ids, key=lambda gallery_id: get_gallery_entry(gallery_id)["order"])


    def gallery_all_ids():
        ids = []
        for chapter_id in GALLERY_CHAPTERS:
            ids.extend(gallery_ids_for_chapter(chapter_id))
        return ids


    def _gallery_unlock_list():
        unlocked = getattr(renpy.store.persistent, "gallery_unlocked", None)
        if unlocked is None:
            unlocked = []
            renpy.store.persistent.gallery_unlocked = unlocked
        return unlocked


    def is_gallery_unlocked(gallery_id):
        return gallery_id in _gallery_unlock_list()


    def unlock_gallery(gallery_id):
        """Unlock one gallery entry permanently for this player profile."""
        get_gallery_entry(gallery_id)
        unlocked = _gallery_unlock_list()
        if gallery_id not in unlocked:
            unlocked.append(gallery_id)
            renpy.save_persistent()
        renpy.restart_interaction()
        return True


    def gallery_unlocked_count(chapter_id=None):
        if chapter_id is None:
            ids = gallery_all_ids()
        else:
            ids = gallery_ids_for_chapter(chapter_id)
        return sum(1 for gallery_id in ids if is_gallery_unlocked(gallery_id))


    def gallery_total_count(chapter_id=None):
        if chapter_id is None:
            return len(gallery_all_ids())
        return len(gallery_ids_for_chapter(chapter_id))


    def gallery_display_title(gallery_id):
        if not is_gallery_unlocked(gallery_id):
            return "Locked CG"
        return get_gallery_entry(gallery_id)["title"]


    def gallery_display_description(gallery_id):
        if not is_gallery_unlocked(gallery_id):
            return "Discover this scene in the story to unlock it here."
        return get_gallery_entry(gallery_id)["description"]


    def gallery_has_replay(gallery_id):
        return bool(get_gallery_entry(gallery_id).get("replay_label"))


    def gallery_grid_rows(chapter_id, columns=3):
        ids = gallery_ids_for_chapter(chapter_id)
        return [ids[index:index + columns] for index in range(0, len(ids), columns)]


    def debug_unlock_gallery_entry(gallery_id):
        unlock_gallery(gallery_id)
        renpy.notify("Gallery entry unlocked for testing.")


    def debug_unlock_all_gallery():
        renpy.store.persistent.gallery_unlocked = list(gallery_all_ids())
        renpy.save_persistent()
        renpy.notify("All placeholder gallery entries unlocked.")
        renpy.restart_interaction()


    def debug_reset_gallery():
        renpy.store.persistent.gallery_unlocked = []
        renpy.save_persistent()
        renpy.notify("Gallery unlocks reset.")
        renpy.restart_interaction()
