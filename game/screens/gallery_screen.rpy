# Player-facing gallery shell.
# Uses placeholder tiles until final CG thumbnails/art are produced.

screen gallery_card(gallery_id):

    $ entry = get_gallery_entry(gallery_id)
    $ unlocked = is_gallery_unlocked(gallery_id)
    $ title = gallery_display_title(gallery_id)
    $ chapter_label = gallery_chapter_label(entry["chapter"])
    $ slot_number = entry["order"]
    $ card_background = Solid("#241f27")
    $ preview_background = Solid(entry["accent"] if unlocked else "#242026")

    button:
        xsize 480
        ysize 305
        padding (14, 14)
        background card_background
        hover_background Solid("#302831")

        if unlocked:
            action Show("gallery_preview_screen", gallery_id=gallery_id)
        else:
            action Function(renpy.notify, "This gallery entry is still locked.")

        vbox:
            spacing 11
            xfill True
            yfill True

            frame:
                xfill True
                ysize 205
                background preview_background
                padding (14, 14)

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 6

                    if unlocked:
                        text "CG [slot_number:02d]" size 38 color "#ffffff" xalign 0.5
                        text "PLACEHOLDER PREVIEW" size 15 color "#eadde7" xalign 0.5
                    else:
                        text "LOCKED" size 34 color "#8f8390" xalign 0.5
                        text "? ? ?" size 22 color "#665d68" xalign 0.5

            hbox:
                xfill True
                text "[title]" size 20 color ("#ffffff" if unlocked else "#8f8390")
                text "[chapter_label]" size 14 color "#a99ba8" xalign 1.0


screen gallery_screen():

    modal True
    zorder 185

    default gallery_selected_chapter = GALLERY_CHAPTERS[0]

    key "K_ESCAPE" action Return()

    $ chapter_ids = gallery_ids_for_chapter(gallery_selected_chapter)
    $ rows = gallery_grid_rows(gallery_selected_chapter, 3)
    $ chapter_unlocked = gallery_unlocked_count(gallery_selected_chapter)
    $ chapter_total = gallery_total_count(gallery_selected_chapter)
    $ total_unlocked = gallery_unlocked_count()
    $ total_entries = gallery_total_count()

    add Solid("#141117")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1740
        ysize 980
        background Solid("#19151d")
        padding (42, 34)

        vbox:
            spacing 18
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "GALLERY" size 46 color "#ffffff"
                    text "Scenes you discover in the story are collected here." size 19 color "#aa9dab"

                vbox:
                    xalign 1.0
                    spacing 7
                    text "Unlocked: [total_unlocked] / [total_entries]" size 19 color "#d8cad5" xalign 1.0
                    textbutton "Close":
                        xalign 1.0
                        action Return()

            frame:
                xfill True
                background Solid("#211c25")
                padding (18, 15)

                hbox:
                    spacing 12
                    xfill True

                    for chapter_id in GALLERY_CHAPTERS:
                        $ chapter_label = gallery_chapter_label(chapter_id)
                        $ selected = gallery_selected_chapter == chapter_id
                        $ unlocked_count = gallery_unlocked_count(chapter_id)
                        $ total_count = gallery_total_count(chapter_id)

                        textbutton "[chapter_label]  [unlocked_count]/[total_count]":
                            action SetScreenVariable("gallery_selected_chapter", chapter_id)
                            selected selected

            hbox:
                xfill True
                text "[gallery_chapter_label(gallery_selected_chapter)]" size 27 color "#ffffff"
                text "[chapter_unlocked] of [chapter_total] unlocked" size 17 color "#a99ba8" xalign 1.0

            if not chapter_ids:
                frame:
                    xfill True
                    yfill True
                    background Solid("#211c25")
                    padding (30, 30)
                    text "No gallery entries have been added for this chapter yet." size 22 color "#b9aabb" xalign 0.5 yalign 0.5

            else:
                use lc_scroll_body:
                    vbox:
                        spacing 18
                        xfill True

                        for row_ids in rows:
                            hbox:
                                spacing 20
                                xfill True

                                for gallery_id in row_ids:
                                    use gallery_card(gallery_id)

                                if len(row_ids) < 3:
                                    for missing_index in range(3 - len(row_ids)):
                                        null width 480 height 1

                        null height 8

                text "Locked entries reveal only that a CG exists. Titles, descriptions, and previews appear after the story unlocks them." size 15 color "#817582"


screen gallery_preview_screen(gallery_id):

    modal True
    zorder 220

    key "K_ESCAPE" action Hide("gallery_preview_screen")

    $ entry = get_gallery_entry(gallery_id)
    $ title = gallery_display_title(gallery_id)
    $ description = gallery_display_description(gallery_id)
    $ chapter_label = gallery_chapter_label(entry["chapter"])
    $ slot_number = entry["order"]

    add Solid("#000000dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1500
        ysize 930
        background Solid("#19151d")
        padding (34, 30)

        vbox:
            spacing 18
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "[title]" size 38 color "#ffffff"
                    text "[chapter_label]" size 17 color "#f1a8c8"

                textbutton "Close":
                    xalign 1.0
                    action Hide("gallery_preview_screen")

            frame:
                xalign 0.5
                xsize 1320
                ysize 700
                background Solid(entry["accent"])
                padding (20, 20)

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 10

                    text "CG [slot_number:02d]" size 72 color "#ffffff" xalign 0.5
                    text "FINAL CG ART WILL REPLACE THIS PLACEHOLDER" size 19 color "#f4eaf1" xalign 0.5
                    text "Asset ID: [entry['asset_id']]" size 15 color "#e1d4de" xalign 0.5

            hbox:
                spacing 18
                xfill True

                vbox:
                    spacing 5
                    xfill True
                    text "[description]" size 19 color "#ddd2db"
                    text "Scene replay is scaffolded in the data model and will be enabled when real replay labels exist." size 15 color "#918493"

                if gallery_has_replay(gallery_id):
                    textbutton "Replay Scene":
                        sensitive False
                else:
                    text "REPLAY NOT YET AVAILABLE" size 15 color "#817582" xalign 1.0
