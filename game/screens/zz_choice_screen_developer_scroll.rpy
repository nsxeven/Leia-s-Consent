# Choice-screen revision for verbose Developer Mode metadata.
# Normal/Insight/Full retain the existing centered presentation. Developer Mode
# gets a top-anchored scrollable viewport so long stat/ID/tag captions never
# push the first option off-screen.

screen choice(items):
    style_prefix "choice"

    if current_choice_mode() == "developer":
        viewport:
            xalign 0.5
            yalign 0.5
            xsize 1540
            ysize 880
            yinitial 0.0
            mousewheel True
            draggable True
            scrollbars "vertical"

            vbox:
                xalign 0.5
                xfill True
                spacing 8

                for i in items:
                    textbutton i.caption action i.action:
                        xalign 0.5
                        xmaximum 1460
                        text_size 22
                        text_xalign 0.5

    else:
        vbox:
            for i in items:
                textbutton i.caption action i.action
