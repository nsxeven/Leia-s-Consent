# Player-facing Wardrobe UI.
# Mechanical ownership and wear acceptance remain in wardrobe_logic.rpy.

screen outfit_style_meter(label, value):

    vbox:
        spacing 5
        xfill True

        hbox:
            xfill True
            text label size 17 color "#7a6266"
            text "[value]" size 16 color "#7a6266" xalign 1.0

        bar:
            value StaticValue(value, 100)
            xfill True
            ysize 12
            left_bar Frame("gui/scrapbook/bar_love.png", 6, 6)
            right_bar Frame("gui/scrapbook/bar_track.png", 6, 6)


screen wardrobe_screen():

    modal True
    zorder 205

    default wardrobe_selected_outfit = equipped_outfit

    key "K_ESCAPE" action Return()

    $ mode = current_choice_mode()
    $ selected_outfit = get_outfit(wardrobe_selected_outfit)
    $ selected_name = selected_outfit["name"]
    $ selected_description = selected_outfit["description"]
    $ selected_category = outfit_category_label(wardrobe_selected_outfit)
    $ selected_contexts = outfit_context_text(wardrobe_selected_outfit)
    $ selected_status = outfit_status_short(wardrobe_selected_outfit)
    $ selected_status_color = outfit_status_color(wardrobe_selected_outfit)
    $ selected_note = outfit_comfort_note(wardrobe_selected_outfit)
    $ selected_requirements = outfit_requirement_text(wardrobe_selected_outfit, mode)
    $ selected_styles = outfit_style_rows(wardrobe_selected_outfit)

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
                    text "WARDROBE" size 46 color "#3b2a30"
                    text "Browse [girlfriend_name]'s owned outfits and choose what to ask her to wear." size 19 color "#7a6266"

                vbox:
                    xalign 1.0
                    spacing 7
                    text "Display: [transparency_mode_label()]" size 18 color "#7a6266" xalign 1.0
                    textbutton "Close":
                        xalign 1.0
                        action Return()

            frame:
                xfill True
                background Frame("gui/scrapbook/frame_card.png", 9, 9)
                padding (22, 15)

                hbox:
                    xfill True
                    text "Currently wearing: [current_outfit_name()]" size 20 color "#3b2a30"
                    text "Owned outfits: [len(valid_owned_outfit_ids())]" size 18 color "#7a6266" xalign 1.0

            if last_wardrobe_message:
                frame:
                    xfill True
                    background Frame("gui/scrapbook/frame_kraft.png", 9, 9)
                    padding (20, 13)
                    text "[last_wardrobe_message]" size 17 color "#3b2a30"

            hbox:
                spacing 20
                xfill True
                yfill True

                frame:
                    xsize 505
                    yfill True
                    background Frame("gui/scrapbook/frame_card.png", 9, 9)
                    padding (18, 18)

                    vbox:
                        spacing 14
                        xfill True
                        yfill True

                        hbox:
                            xfill True
                            text "OWNED" size 24 color "#3b2a30"
                            text "[len(valid_owned_outfit_ids())]" size 17 color "#7a6266" xalign 1.0

                        use lc_scroll_body:
                            vbox:
                                spacing 12
                                xfill True

                                for outfit_id in valid_owned_outfit_ids():
                                    $ card_outfit = get_outfit(outfit_id)
                                    $ card_name = card_outfit["name"]
                                    $ card_category = outfit_category_label(outfit_id)
                                    $ card_status = outfit_status_short(outfit_id)
                                    $ card_status_color = outfit_status_color(outfit_id)
                                    $ card_selected = wardrobe_selected_outfit == outfit_id

                                    button:
                                        xfill True
                                        padding (20, 18)
                                        background (Frame("gui/scrapbook/frame_card_on.png", 9, 9) if card_selected else Frame("gui/scrapbook/frame_card.png", 9, 9))
                                        hover_background Frame("gui/scrapbook/frame_paper_hi.png", 9, 9)
                                        action SetScreenVariable("wardrobe_selected_outfit", outfit_id)

                                        vbox:
                                            spacing 7
                                            xfill True

                                            hbox:
                                                xfill True
                                                text "[card_name]" size 23 color "#3b2a30"
                                                text "[card_category]" size 15 color "#7a6266" xalign 1.0

                                            text "[card_status]" size 16 color card_status_color

                                            if equipped_outfit == outfit_id:
                                                text "CURRENT OUTFIT" size 14 color "#cc0066"

                frame:
                    xfill True
                    yfill True
                    background Frame("gui/scrapbook/frame_card.png", 9, 9)
                    padding (28, 24)

                    use lc_scroll_body:
                        vbox:
                            spacing 18
                            xfill True

                            hbox:
                                xfill True

                                vbox:
                                    spacing 5
                                    text "[selected_name]" size 34 color "#3b2a30"
                                    text "[selected_category]" size 17 color "#cc0066"

                                text "[selected_status]" size 18 color selected_status_color xalign 1.0

                            text "[selected_description]" size 20 color "#3b2a30" line_spacing 4

                            frame:
                                xfill True
                                background Frame("gui/scrapbook/frame_card.png", 9, 9)
                                padding (20, 17)

                                vbox:
                                    spacing 7
                                    text "HOW [girlfriend_name.upper()] FEELS ABOUT IT" size 17 color "#cc0066"
                                    text "[selected_note]" size 18 color "#3b2a30" line_spacing 3

                            vbox:
                                spacing 8
                                text "SUITED FOR" size 18 color "#3b2a30"
                                text "[selected_contexts]" size 17 color "#7a6266"

                            text "STYLE PROFILE" size 22 color "#3b2a30"

                            grid 2 2:
                                spacing 18
                                xfill True

                                for style_label, style_value in selected_styles:
                                    frame:
                                        xfill True
                                        background Frame("gui/scrapbook/frame_card.png", 9, 9)
                                        padding (16, 13)
                                        use outfit_style_meter(style_label, style_value)

                            if selected_requirements:
                                frame:
                                    xfill True
                                    background Frame("gui/scrapbook/frame_card.png", 9, 9)
                                    padding (20, 17)

                                    vbox:
                                        spacing 8
                                        text "COMFORT REQUIREMENTS" size 18 color "#3b2a30"
                                        text "[selected_requirements]" size 16 color "#5a4030" line_spacing 4

                            elif mode == "normal" and not can_wear(wardrobe_selected_outfit):
                                text "Her exact comfort requirements are hidden in Immersive mode." size 16 color "#7a6266"

                            null height 4

                            if equipped_outfit == wardrobe_selected_outfit:
                                frame:
                                    xfill True
                                    background Frame("gui/scrapbook/frame_card_on.png", 9, 9)
                                    padding (20, 15)
                                    text "CURRENTLY EQUIPPED" size 18 color "#cc0066" xalign 0.5
                            else:
                                textbutton "Ask [girlfriend_name] to wear this":
                                    xfill True
                                    action Function(attempt_wear_outfit, wardrobe_selected_outfit)
