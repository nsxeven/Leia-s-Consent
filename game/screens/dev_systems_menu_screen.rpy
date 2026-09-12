# Scrollable development systems menu.
# Keeps the sandbox launcher usable as more test entries are added.

screen dev_systems_menu_screen():

    modal True
    zorder 220

    add Solid("#17151a")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1220
        ysize 920
        background Solid("#1d1a20")
        padding (36, 30)

        vbox:
            spacing 22
            xfill True
            yfill True

            text "SYSTEMS TEST MENU" size 42 color "#ffffff" xalign 0.5
            text "Choose which system you want to test." size 20 color "#aaa0aa" xalign 0.5

            use lc_scroll_body:
                vbox:
                    spacing 14
                    xfill True

                    textbutton "Integrated systems slice (Phase 9)":
                        xfill True
                        action Return("vertical_slice")

                    textbutton "Gallery shell test":
                        xfill True
                        action Return("gallery")

                    textbutton "Player Settings / Transparency test":
                        xfill True
                        action Return("settings")

                    textbutton "Player Status screen test":
                        xfill True
                        action Return("status")

                    textbutton "Sprite System test":
                        xfill True
                        action Return("sprite")

                    textbutton "Economy + Wardrobe test":
                        xfill True
                        action Return("economy")

                    textbutton "Choice Engine test":
                        xfill True
                        action Return("choice")

                    textbutton "Open Developer Panel":
                        xfill True
                        action Return("developer")

                    textbutton "Open verification / save-state menu":
                        xfill True
                        action Return("verify")

                    textbutton "Finish systems test and return to the main menu":
                        xfill True
                        action Return("finish")
