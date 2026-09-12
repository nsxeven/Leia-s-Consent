# Player-facing Wardrobe UI.
# Mechanical ownership and wear acceptance remain in wardrobe_logic.rpy.

screen outfit_style_meter(label, value):

    vbox:
        spacing 5
        xfill True

        hbox:
            xfill True
            text label size 17 color "#d8cad5"
            text "[value]" size 16 color "#a99ba8" xalign 1.0

        bar:
            value StaticValue(value, 100)
            xfill True
            ysize 12
            left_bar Solid("#cc5d91")
            right_bar Solid("#3a303d")


screen wardrobe_outfit_card(outfit_id, selected_outfit_id):

    $ outfit = get_outfit(outfit_id)
    $ outfit_name_value = outfit["name"]
    $ category_value = outfit_category_label(outfit_id)
    $ status_value = outfit_status_short(outfit_id)
    $ status_color_value = outfit_status_color(outfit_id)
    $ is_selected = selected_outfit_id == outfit_id

    button:
        xfill True
        padding (20, 18)
        background (Solid("#3b2a38") if is_selected else Solid("#211c25"))
        hover_background Solid("#30242f")
        action SetScreenVariable("wardrobe_selected_outfit", outfit_id)

        vbox:
            spacing 7
            xfill True

            hbox:
                xfill True
                text "[outfit_name_value]" size 23 color "#ffffff"
                text "[category_value]" size 15 color "#a99ba8" xalign 1.0

            text "[status_value]" size 16 color status_color_value

            if equipped_outfit == outfit_id:
                text "CURRENT OUTFIT" size 14 color "#f1a8c8"


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
                    text "WARDROBE" size 46 color "#ffffff"
                    text "Browse [girlfriend_name]'s owned outfits and choose what to ask her to wear." size 19 color "#aa9dab"

                vbox:
                    xalign 1.0
                    spacing 7
                    text "Display: [transparency_mode_label()]" size 18 color "#d8cad5" xalign 1.0
                    textbutton "Close":
                        xalign 1.0
                        action Return()

            frame:
                xfill True
                background Solid("#2a222c")
                padding (22, 15)

                hbox:
                    xfill True
                    text "Currently wearing: [current_outfit_name()]" size 20 color "#ffffff"
                    text "Owned outfits: [len(valid_owned_outfit_ids())]" size 18 color "#b9aabb" xalign 1.0

            if last_wardrobe_message:
                frame:
                    xfill True
                    background Solid("#30242e")
                    padding (20, 13)
                    text "[last_wardrobe_message]" size 17 color "#e6d9e3"

            hbox:
                spacing 20
                xfill True
                yfill True

                frame:
                    xsize 505
                    yfill True
                    background Solid("#1d1920")
                    padding (18, 18)

                    vbox:
                        spacing 14
                        xfill True
                        yfill True

                        hbox:
                            xfill True
                            text "OWNED" size 24 color "#ffffff"
                            text "[len(valid_owned_outfit_ids())]" size 17 color "#a99ba8" xalign 1.0

                        use lc_scroll_body:
                            vbox:
                                spacing 12
                                xfill True

                                for outfit_id in valid_owned_outfit_ids():
                                    use wardrobe_outfit_card(outfit_id, wardrobe_selected_outfit)

                frame:
                    xfill True
                    yfill True
                    background Solid("#211c25")
                    padding (28, 24)

                    use lc_scroll_body:
                        vbox:
                            spacing 18
                            xfill True

                            hbox:
                                xfill True

                                vbox:
                                    spacing 5
                                    text "[selected_name]" size 34 color "#ffffff"
                                    text "[selected_category]" size 17 color "#f1a8c8"

                                text "[selected_status]" size 18 color selected_status_color xalign 1.0

                            text "[selected_description]" size 20 color "#ddd2db" line_spacing 4

                            frame:
                                xfill True
                                background Solid("#2a242d")
                                padding (20, 17)

                                vbox:
                                    spacing 7
                                    text "HOW [girlfriend_name.upper()] FEELS ABOUT IT" size 17 color "#f1a8c8"
                                    text "[selected_note]" size 18 color "#eee7ed" line_spacing 3

                            vbox:
                                spacing 8
                                text "SUITED FOR" size 18 color "#ffffff"
                                text "[selected_contexts]" size 17 color "#b9aabb"

                            text "STYLE PROFILE" size 22 color "#ffffff"

                            grid 2 2:
                                spacing 18
                                xfill True

                                for style_label, style_value in selected_styles:
                                    frame:
                                        xfill True
                                        background Solid("#272129")
                                        padding (16, 13)
                                        use outfit_style_meter(style_label, style_value)

                            if selected_requirements:
                                frame:
                                    xfill True
                                    background Solid("#2a242d")
                                    padding (20, 17)

                                    vbox:
                                        spacing 8
                                        text "COMFORT REQUIREMENTS" size 18 color "#ffffff"
                                        text "[selected_requirements]" size 16 color "#cdbfca" line_spacing 4

                            elif mode == "normal" and not can_wear(wardrobe_selected_outfit):
                                text "Her exact comfort requirements are hidden in Immersive mode." size 16 color "#918493"

                            null height 4

                            if equipped_outfit == wardrobe_selected_outfit:
                                frame:
                                    xfill True
                                    background Solid("#3b2a38")
                                    padding (20, 15)
                                    text "CURRENTLY EQUIPPED" size 18 color "#f1a8c8" xalign 0.5
                            else:
                                textbutton "Ask [girlfriend_name] to wear this":
                                    xfill True
                                    action Function(attempt_wear_outfit, wardrobe_selected_outfit)
