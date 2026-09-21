# Scrollable developer verification menu.
# Kept separate from story labels so long test menus remain usable on smaller screens.

screen dev_verify_menu():

    modal True
    zorder 260

    key "K_ESCAPE" action Return("systems")

    add Solid("#17151a")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1450
        ysize 850
        background Solid("#1d1920")
        padding (34, 30)

        vbox:
            spacing 18
            xfill True
            yfill True

            hbox:
                xfill True

                vbox:
                    spacing 4
                    text "DEVELOPMENT VERIFICATION" size 38 color "#ffffff"
                    text "Scroll to access every system and save-state check." size 17 color "#aa9dab"

                textbutton "Back to Systems":
                    xalign 1.0
                    action Return("systems")

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                pagekeys True
                scrollbars "vertical"
                side_yfill True

                vbox:
                    spacing 12
                    xfill True

                    textbutton "Open Player Settings / Transparency":
                        xfill True
                        action Return("settings")

                    textbutton "Open Player Status screen":
                        xfill True
                        action Return("status")

                    textbutton "Show current character names":
                        xfill True
                        action Return("names")


                    textbutton "Open Developer Panel":
                        xfill True
                        action Return("dev_panel")

                    textbutton "Open Developer Choice Display controls":
                        xfill True
                        action Return("choice_display")

                    textbutton "Show recorded choice state":
                        xfill True
                        action Return("choice_state")

                    textbutton "Open Outfit Shop":
                        xfill True
                        action Return("shop")

                    textbutton "Open Wardrobe":
                        xfill True
                        action Return("wardrobe")

                    textbutton "Show economy + wardrobe state":
                        xfill True
                        action Return("economy_state")

                    textbutton "Repeat save/load instructions":
                        xfill True
                        action Return("save_load")

                    null height 8

                    textbutton "Finish systems test and return to the main menu":
                        xfill True
                        action Return("finish")
