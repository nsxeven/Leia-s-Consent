# Input guard shown underneath the phone overlay.
# It absorbs mouse clicks that would otherwise reach story/menu controls behind the phone.

init python:
    if "phone_input_blocker" not in config.overlay_screens:
        config.overlay_screens.append("phone_input_blocker")


screen phone_input_blocker():

    zorder 309

    if renpy.get_screen("phone_screen"):
        button:
            xfill True
            yfill True
            background Solid("#00000000")
            hover_background Solid("#00000000")
            action NullAction()
