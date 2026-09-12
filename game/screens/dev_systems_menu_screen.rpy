# Scrollable development systems menu.
# This overlays the original Ren'Py menu while the sandbox launcher label is active,
# preventing the growing list of test entries from being cropped at 1080p.

init python:
    if "dev_systems_menu_screen" not in config.overlay_screens:
        config.overlay_screens.append("dev_systems_menu_screen")


screen dev_systems_menu_screen():

    if renpy.get_label() == "dev_systems_menu":

        modal True
        zorder 260

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
                            action Jump("dev_vertical_slice")

                        textbutton "Gallery shell test":
                            xfill True
                            action Jump("dev_gallery_test")

                        textbutton "Player Settings / Transparency test":
                            xfill True
                            action Jump("dev_systems_settings_helper")

                        textbutton "Player Status screen test":
                            xfill True
                            action Jump("dev_systems_status_helper")

                        textbutton "Sprite System test":
                            xfill True
                            action Jump("dev_sprite_test")

                        textbutton "Economy + Wardrobe test":
                            xfill True
                            action Jump("dev_economy_wardrobe_test")

                        textbutton "Choice Engine test":
                            xfill True
                            action Jump("dev_choice_intro")

                        textbutton "Open Developer Panel":
                            xfill True
                            action Jump("dev_systems_panel_helper")

                        textbutton "Open verification / save-state menu":
                            xfill True
                            action Jump("dev_verify_state")

                        textbutton "Finish systems test and return to the main menu":
                            xfill True
                            action MainMenu(confirm=False)


label dev_systems_settings_helper:
    call screen player_settings_screen
    jump dev_systems_menu


label dev_systems_status_helper:
    call screen status_screen
    jump dev_systems_menu


label dev_systems_panel_helper:
    call screen dev_panel
    jump dev_systems_menu
