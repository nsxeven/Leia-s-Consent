# Keep Ren'Py confirmation dialogs above the in-game phone overlay.
# The stock confirm screen uses zorder 200, while the phone uses zorder 310.
# This override preserves the stock layout/styles but raises its display priority.

screen confirm(message, yes_action, no_action):

    modal True
    zorder 500
    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    key "game_menu" action no_action
