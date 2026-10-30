# Landscape Polaroids are built from existing image references; no new art needed.
transform lc_polaroid_drop(delay=0.0, tilt=0.0):
    alpha 0.0
    yoffset -65
    rotate (tilt - 7)
    pause delay
    parallel:
        linear 0.3 alpha 1.0
    parallel:
        easeout 0.55 yoffset 0 rotate tilt

transform lc_polaroid_still(tilt=0.0):
    rotate tilt

transform lc_title_arrive:
    alpha 0.0
    yoffset -12
    easeout 0.25 alpha 1.0 yoffset 0
    pause 2.1
    linear 0.3 alpha 0.0

screen lc_review_polaroid(card, index, animate):
    frame:
        xsize 400
        ysize 258
        padding (12, 12)
        background Solid("#f4eee4")
        at (lc_polaroid_drop(index * 0.45, (-2.0, 1.5, -1.0, 2.0, -1.5)[index]) if animate else lc_polaroid_still((-2.0, 1.5, -1.0, 2.0, -1.5)[index]))
        vbox:
            spacing 8
            fixed:
                xsize 376
                ysize 210
                add Solid("#29232b")
                if renpy.has_image("cg " + card["image"]):
                    add gallery_thumb(card["image"], 376, 210) xalign 0.5 yalign 0.5
                else:
                    text "Image unavailable" align (0.5, 0.5) size 19 color "#ddd3db"
            text (("DREAM · " if card["dream"] else "") + gallery_customize_names(card["caption"])) size 19 color "#30252f" xmaximum 376 substitute False

screen lc_day_review_screen(day_id, replay=False):
    modal True
    zorder 220
    default reveal_all = replay or not persistent.lc_recap_animation
    default show_choices = False
    $ record = lc_review_days[day_id]
    $ cards = lc_review_cards(day_id)
    $ mode = current_choice_mode()
    $ titles = lc_review_titles(day_id)
    $ rows = lc_review_delta_rows(day_id, mode)

    add Solid("#100d16f5")
    key "K_ESCAPE" action (Hide("lc_review_history_screen") if replay else Return())
    key "K_SPACE" action SetScreenVariable("reveal_all", True)
    frame:
        align (0.5, 0.5)
        xsize 1800
        ysize 1010
        padding (40, 30)
        background Solid("#211a28")
        vbox:
            spacing 18
            hbox:
                xfill True
                vbox:
                    text LC_REVIEW_DAYS[day_id]["label"].upper() size 36 color "#fff4e8"
                    text "A few moments to take with you." size 20 color "#c4b3c6"
                textbutton ("Close" if replay else "Continue"):
                    xalign 1.0
                    action (Hide("lc_review_history_screen") if replay else Return())
            hbox:
                spacing 35
                fixed:
                    xsize 850
                    ysize 830
                    if cards:
                        for index, card in enumerate(cards):
                            fixed:
                                xpos ((index % 2) * 430 + 12)
                                ypos ((index // 2) * 275 + 10)
                                xsize 400
                                ysize 258
                                use lc_review_polaroid(card, index, not reveal_all)
                    else:
                        text "No recorded photographs for this day.\nYour story recap is still available." align (0.5, 0.4) textalign 0.5 size 23 color "#c4b3c6"
                viewport:
                    xsize 820
                    ysize 830
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vbox:
                        xsize 780
                        spacing 18
                        text record.get("summary", "The day has ended.") size 26 color "#f5e8ef"
                        if record.get("partial"):
                            text "This save predates daily tracking. Earlier moments and day-start changes are unavailable; tracking begins fully on the next day." size 18 color "#ddbd9a"
                        if mode != "normal":
                            text "CURRENT DIRECTION" size 18 color "#e3a8c4"
                            text LC_REVIEW_ROUTES.get(record.get("route"), LC_REVIEW_ROUTES["mixed"])[0] size 26 color "#fff4e8"
                            text "A current tendency, not a guaranteed ending. Route labels are not proof of an affair." size 17 color "#b7a5ba"
                        if rows:
                            text "WHAT CHANGED" size 18 color "#e3a8c4"
                            for label, detail in rows:
                                hbox:
                                    text label size 21 color "#e9dce7" xsize 340
                                    text detail size 21 color "#d7c2a7"
                        elif mode != "normal" and not record.get("partial"):
                            text "No stat changes are shown in this mode." size 19 color "#b7a5ba"
                        if mode in ("full", "developer"):
                            if record.get("modified"):
                                text "This playthrough includes developer or Route Explorer adjustments." size 17 color "#ddbd9a"
                            textbutton ("Hide choice details" if show_choices else "Show choice details"):
                                action ToggleScreenVariable("show_choices")
                            if show_choices:
                                text "Actual clamped changes from recorded choices. Direct story or Route Explorer changes may also affect the day's totals." size 16 color "#b7a5ba"
                                for choice_label, detail in lc_review_choice_rows(day_id):
                                    text choice_label size 18 color "#e9dce7" substitute False
                                    text detail size 17 color "#b7a5ba" substitute False
                        if titles[0]:
                            text "CHARACTER TITLES" size 18 color "#e3a8c4"
                            text (player_name + " · " + titles[0]) size 23 color "#fff4e8" substitute False
                            text (girlfriend_name + " · " + titles[1]) size 23 color "#fff4e8" substitute False
                            if record.get("titles_before") and tuple(record["titles_before"]) != tuple(record.get("titles_after", record["titles_before"])):
                                text "Your story titles changed today." size 17 color "#d7c2a7"
                        if any(card["dream"] for card in cards):
                            text "Dream cards depict imagined events, not evidence of what happened." size 17 color "#ddbd9a"
                        textbutton "Reveal all photos now" action SetScreenVariable("reveal_all", True)
                        textbutton ("Photo animation: On" if persistent.lc_recap_animation else "Photo animation: Off"):
                            action [ToggleField(persistent, "lc_recap_animation"), SetScreenVariable("reveal_all", True)]
                        null height 20

screen lc_review_settings():
    frame:
        xfill True
        background Solid("#211c25")
        padding (26, 22)
        vbox:
            spacing 14
            text "DAY REVIEW & CHARACTER TITLES" size 27 color "#ffffff"
            text "Recap detail follows your Information Transparency mode. Photos only use moments shown in this playthrough." size 18 color "#c8b8c5"
            textbutton ("Falling photos: On" if persistent.lc_recap_animation else "Falling photos: Off"):
                action ToggleField(persistent, "lc_recap_animation")
            hbox:
                spacing 25
                text "Titles:" size 21
                textbutton "Off" action SetField(persistent, "lc_title_style", "off")
                textbutton "Story" action SetField(persistent, "lc_title_style", "story")
                textbutton "Genre" action SetField(persistent, "lc_title_style", "genre")
            text ("Selected: " + persistent.lc_title_style.title()) size 17 color "#c8b8c5"
            text "Genre titles can include provocative labels after explicit story milestones. They never change your route." size 17 color "#c8b8c5"
            textbutton ("Brief sprite title badges: On" if persistent.lc_title_badges else "Brief sprite title badges: Off"):
                action ToggleField(persistent, "lc_title_badges")
            text "DAY ONE DREAM" size 23 color "#ffffff"
            hbox:
                spacing 25
                textbutton "Ask each time" action SetField(persistent, "lc_day1_dream", "ask")
                textbutton "Full scene" action SetField(persistent, "lc_day1_dream", "show")
                textbutton "Brief summary" action SetField(persistent, "lc_day1_dream", "summary")
            text ("Selected: " + persistent.lc_day1_dream.title() + ". The waking choice and its consequences remain unchanged. This does not disable NTR elsewhere.") size 17 color "#c8b8c5"

screen lc_title_badge(character_id, title):
    zorder 90
    timer 2.8 action Hide("lc_title_badge")
    if persistent.lc_title_badges and persistent.lc_title_style != "off" and phone_hud_enabled and quick_menu and not renpy.get_screen("lc_day_review_screen") and any(tag.startswith(character_id + "_") for tag in renpy.get_showing_tags()):
        frame:
            xpos (0.78 if character_id == "leia" else 0.22)
            xanchor 0.5
            ypos 0.14
            padding (18, 10)
            background Solid("#211a28df")
            at lc_title_arrive
            text title size 23 color "#f0c4da" substitute False


screen lc_review_history_screen(day_id):
    modal True
    zorder 230
    use lc_day_review_screen(day_id, replay=True)
    # Override Return actions inherited by the reused screen with a local close.
    key "K_ESCAPE" action Hide("lc_review_history_screen")
