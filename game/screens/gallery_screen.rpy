# Player-facing gallery.
# Cards and previews draw the real `cg <name>` image by its stable name, so a
# Composite text placeholder and final art both work without changes here.
# Data lives in systems/gallery_data.rpy; unlock rules in systems/gallery.rpy.

screen gallery_card(gallery_id):

    $ entry = get_gallery_entry(gallery_id)
    $ unlocked = is_gallery_unlocked(gallery_id)
    $ title = gallery_display_title(gallery_id)
    $ cover = gallery_cover_image(gallery_id)
    $ masked = gallery_card_masked(gallery_id)
    $ art_state = gallery_art_state(gallery_id)
    $ pages_have, pages_total = gallery_pages_counts(gallery_id)
    $ slot_number = entry["order"]
    $ card_background = Frame("gui/scrapbook/frame_polaroid.png", 12, 12)
    $ preview_background = Solid("#0d0b0f" if (unlocked and cover and not masked) else (entry["accent"] if unlocked else "#242026"))

    button:
        xsize 480
        ysize 305
        padding (14, 14)
        background card_background
        hover_background Frame("gui/scrapbook/frame_paper_hi.png", 9, 9)

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
                padding (0, 0)

                fixed:
                    if unlocked and cover and not masked:
                        add gallery_thumb(cover, 452, 205) xalign 0.5 yalign 0.5
                    elif unlocked:
                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 6
                            text "MATURE" size 34 color "#f3c9cf" xalign 0.5
                            text "18+  /  open to view" size 17 color "#eadde7" xalign 0.5
                    else:
                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 6
                            text "LOCKED" size 34 color "#8f8390" xalign 0.5
                            text "? ? ?" size 22 color "#665d68" xalign 0.5

                    if unlocked and art_state != "final":
                        frame:
                            background Solid("#000000b0")
                            padding (6, 3)
                            xpos 8
                            ypos 8
                            text ("ART PENDING" if art_state == "pending" else "PARTIAL ART") size 13 color "#fff3f7"
                    if unlocked and entry["mature"]:
                        frame:
                            background Solid("#8a2f55d0")
                            padding (6, 3)
                            xalign 1.0
                            xoffset -8
                            ypos 8
                            text "18+" size 13 color "#fff3f7"

            hbox:
                xfill True
                text "[title]" size 20 color ("#ffffff" if unlocked else "#8f8390")
                if unlocked and pages_total > 1:
                    text "[pages_have]/[pages_total] pages" size 14 color "#7a6266" xalign 1.0 yalign 0.5
                elif unlocked:
                    text "#[slot_number]" size 14 color "#7a6266" xalign 1.0 yalign 0.5


screen gallery_screen():

    tag menu
    modal (not lc_ui_shooting)
    zorder 185

    default gallery_selected_tab = GALLERY_TAB_IDS[0]

    key "K_ESCAPE" action Return()

    $ tab_ids = gallery_ids_for_tab(gallery_selected_tab)
    $ rows = gallery_grid_rows(gallery_selected_tab, 3)
    $ tab_unlocked = gallery_unlocked_count(tab_id=gallery_selected_tab)
    $ tab_total = gallery_total_count(tab_id=gallery_selected_tab)
    $ total_unlocked = gallery_unlocked_count()
    $ total_entries = gallery_total_count()
    $ tab_title = gallery_tab_label(gallery_selected_tab)

    add "gui/scrapbook/bg_game_menu.png"
    use lc_journal_tabs(1686)

    frame:
        xpos 70
        ypos 48
        xsize 1580
        ysize 900
        background None
        padding (28, 18)

        vbox:
            spacing 18
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "GALLERY" size 46 color "#3b2a30"
                    text "Scenes you discover in the story are collected here." size 19 color "#7a6266"

                vbox:
                    xalign 1.0
                    spacing 7
                    text "Unlocked: [total_unlocked] / [total_entries]" size 19 color "#7a6266" xalign 1.0
                    textbutton "Close":
                        xalign 1.0
                        action Return()

            frame:
                xfill True
                background Frame("gui/scrapbook/frame_card.png", 9, 9)
                padding (18, 15)

                hbox:
                    spacing 12
                    xfill True

                    for tab_id, tab_label, tab_chapter, tab_day in GALLERY_TABS:
                        $ unlocked_count = gallery_unlocked_count(tab_id=tab_id)
                        $ total_count = gallery_total_count(tab_id=tab_id)

                        textbutton "[tab_label]  [unlocked_count]/[total_count]":
                            action SetScreenVariable("gallery_selected_tab", tab_id)
                            selected (gallery_selected_tab == tab_id)

            hbox:
                xfill True
                text "[tab_title]" size 27 color "#3b2a30"
                text "[tab_unlocked] of [tab_total] unlocked" size 17 color "#7a6266" xalign 1.0

            if not tab_ids:
                frame:
                    xfill True
                    yfill True
                    background Frame("gui/scrapbook/frame_card.png", 9, 9)
                    padding (30, 30)
                    text "No gallery entries have been added for this section yet." size 22 color "#7a6266" xalign 0.5 yalign 0.5

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

                text "Locked entries reveal only that a CG exists. Titles, descriptions, and previews appear after the story unlocks them. Mature scenes (18+) stay hidden in the grid until you open them." size 15 color "#7a6266"


screen gallery_preview_screen(gallery_id):

    modal True
    zorder 220

    default gp_page = gallery_first_page(gallery_id)

    key "K_ESCAPE" action Hide("gallery_preview_screen")
    key "K_LEFT" action SetScreenVariable("gp_page", gallery_neighbor_page(gallery_id, gp_page, -1))
    key "K_RIGHT" action SetScreenVariable("gp_page", gallery_neighbor_page(gallery_id, gp_page, 1))

    $ entry = get_gallery_entry(gallery_id)
    $ title = gallery_display_title(gallery_id)
    $ description = gallery_display_description(gallery_id)
    $ tab_label = gallery_tab_label(entry["tab"])
    $ chapter_label = gallery_chapter_label(entry["chapter"])
    $ page_info = entry["pages"][gp_page]
    $ page_image = page_info["image"]
    $ page_label = page_info["label"]
    $ page_is_placeholder = gallery_is_placeholder(page_image)
    $ pages_have, pages_total = gallery_pages_counts(gallery_id)
    $ route_text = gallery_customize_names(entry["route"])
    $ page_number = gp_page + 1

    add Solid("#0e0912aa")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1500
        ysize 930
        background Frame("gui/scrapbook/frame_paper.png", 9, 9)
        padding (34, 30)

        vbox:
            spacing 14
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 3
                    text "[title]" size 38 color "#3b2a30"
                    text "[chapter_label]  /  [tab_label]" size 17 color "#cc0066"

                textbutton "Close":
                    xalign 1.0
                    action Hide("gallery_preview_screen")

            frame:
                xalign 0.5
                xsize 1320
                ysize 580
                background Solid("#000000")
                padding (0, 0)

                add gallery_thumb(page_image, 1320, 580) xalign 0.5 yalign 0.5

                if page_is_placeholder:
                    frame:
                        background Solid("#000000b0")
                        padding (7, 4)
                        xpos 10
                        ypos 10
                        text "ART PENDING" size 15 color "#fff3f7"

            hbox:
                xalign 0.5
                spacing 10

                for page_index, page_entry in enumerate(entry["pages"]):
                    $ page_ok = gallery_page_available(gallery_id, page_index)
                    textbutton (str(page_index + 1) if page_ok else "?"):
                        action SetScreenVariable("gp_page", page_index)
                        sensitive page_ok
                        selected (page_index == gp_page)

            hbox:
                spacing 18
                xfill True

                vbox:
                    spacing 4
                    xsize 1050
                    text "[page_label]  ([page_number] of [pages_total], [pages_have] seen)" size 19 color "#3b2a30"
                    text "[description]" size 18 color "#3b2a30"
                    if entry["mature"]:
                        text "Mature scene (18+). Adults only." size 15 color "#cc0066"
                    if entry["dream"]:
                        text "Dream sequence: a dream is not evidence of what happened." size 15 color "#7a6266"
                    text "[route_text]" size 15 color "#7a6266"
                    if page_is_placeholder:
                        text "Final CG art will replace this placeholder." size 15 color "#7a6266"

                if gallery_has_replay(gallery_id):
                    textbutton "Replay Scene":
                        sensitive False
                else:
                    text "REPLAY NOT YET AVAILABLE" size 15 color "#7a6266" xalign 1.0 xsize 360 text_align 1.0
