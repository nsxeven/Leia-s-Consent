# A clearly labelled opt-in to the mature Julian angle. The caller shows the
# CG as a story image when chosen so its separate gallery page can unlock.
screen lc_breakfast_julian_pov():
    modal True
    zorder 100

    textbutton "View Julian's POV (18+)":
        xalign 0.50
        yalign 0.88
        text_size 32
        action Return("pov")
    textbutton "Continue breakfast":
        xalign 0.92
        yalign 0.94
        action Return("continue")
