# Prototype wardrobe / wear-acceptance screen.

screen wardrobe_screen():

    modal True
    zorder 205

    key "K_ESCAPE" action Return()

    add Solid("#000000bb")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1280
        ysize 960
        padding (38, 32)

        vbox:
            spacing 16
            xfill True

            hbox:
                xfill True
                text "WARDROBE" size 40
                textbutton "Close":
                    xalign 1.0
                    action Return()

            text "Equipped: [current_outfit_name()]" size 27
            text "Transparency mode: [choice_mode_label()]" size 20

            if current_choice_mode() == "normal":
                text "Normal mode hides outfit requirement details." size 19
            elif current_choice_mode() == "insight":
                text "Insight mode shows the types of progression paths that could make an outfit comfortable." size 19
            elif current_choice_mode() == "full":
                text "Full Cheat mode shows exact stat thresholds." size 19
            else:
                text "Developer mode shows exact thresholds, current values, pass/fail state, and internal path IDs." size 19

            if last_wardrobe_message:
                text "[last_wardrobe_message]" size 21

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 18
                    xfill True

                    for outfit_id in valid_owned_outfit_ids():
                        $ outfit = get_outfit(outfit_id)
                        $ outfit_name_value = outfit["name"]
                        $ outfit_description = outfit["description"]
                        $ status_value = outfit_status_text(outfit_id)
                        $ requirement_info = outfit_requirement_text(outfit_id)

                        frame:
                            xfill True
                            padding (24, 20)

                            vbox:
                                spacing 9
                                xfill True

                                hbox:
                                    xfill True
                                    text "[outfit_name_value]" size 28
                                    text "[status_value]" size 22 xalign 1.0

                                text "[outfit_description]" size 20

                                if requirement_info:
                                    text "[requirement_info]" size 18

                                if equipped_outfit != outfit_id:
                                    textbutton "Ask [girlfriend_name] to wear this":
                                        action Function(attempt_wear_outfit, outfit_id)
                                else:
                                    text "CURRENTLY EQUIPPED" size 20
