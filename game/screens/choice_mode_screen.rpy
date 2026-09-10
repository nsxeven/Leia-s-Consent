# Choice transparency settings / development preview.

screen choice_mode_screen():

    modal True
    zorder 210

    key "K_ESCAPE" action Return()

    add Solid("#000000aa")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1100
        padding (40, 35)

        vbox:
            spacing 22

            text "CHOICE DISPLAY MODE" size 40
            text "Current mode: [choice_mode_label()]" size 26

            text "This controls how much information the player sees before choosing. The underlying consequences are unchanged." size 21

            grid 2 2:
                spacing 18

                vbox:
                    spacing 8
                    textbutton "Normal":
                        action Function(set_choice_display_mode, "normal")
                    text "No stat consequences are shown." size 19

                vbox:
                    spacing 8
                    textbutton "Insight":
                        action Function(set_choice_display_mode, "insight")
                    text "Shows direction only, such as Curiosity ↑." size 19

                vbox:
                    spacing 8
                    textbutton "Full Cheat":
                        action Function(set_choice_display_mode, "full")
                    text "Shows exact numerical stat changes." size 19

                vbox:
                    spacing 8
                    textbutton "Developer":
                        action Function(set_choice_display_mode, "developer")
                    text "Shows exact changes plus the internal choice ID." size 19

            null height 10

            text "LIVE PREVIEW" size 28
            text "[choice_preview_text()]" size 23

            null height 10

            textbutton "Close":
                action Return()
