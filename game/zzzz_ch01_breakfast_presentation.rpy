# Day Two breakfast CG sequence and optional Julian POV (darryn-approved A).

screen lc_breakfast_julian_pov():
    modal True
    zorder 100
    default pov = False

    if pov:
        add "ch01_d2_breakfast_julian_pov"
        textbutton "Back to breakfast":
            xalign 0.5
            yalign 0.93
            action SetScreenVariable("pov", False)
    else:
        textbutton "✦":
            xpos 0.86
            ypos 0.14
            xsize 100
            ysize 100
            text_size 52
            text_color "#fff7df"
            text_hover_color "#ffd18a"
            action SetScreenVariable("pov", True)
        textbutton "Continue":
            xalign 0.94
            yalign 0.94
            action Return()
