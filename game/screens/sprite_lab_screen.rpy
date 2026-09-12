# Development-only controls for testing Leia's layered sprite state.

screen sprite_lab_controls():

    modal True
    zorder 210

    key "K_ESCAPE" action Return()

    frame:
        xalign 0.98
        yalign 0.5
        xsize 620
        ysize 930
        padding (32, 28)

        vbox:
            spacing 16
            xfill True

            hbox:
                xfill True
                text "SPRITE LAB" size 38
                textbutton "Close":
                    xalign 1.0
                    action Return()

            text "Placeholder art only — this screen proves state + layering before final assets." size 19

            text "Current pose: [leia_pose_label()]" size 23
            text "Expression: [leia_expression_label()]" size 23
            text "Outfit: [current_outfit_name()]" size 23

            null height 8
            text "POSE" size 28

            for pose_id, pose_label in LEIA_POSES:
                textbutton "[pose_label]":
                    action Function(set_leia_pose, pose_id)
                    selected leia_pose == pose_id

            null height 8
            text "EXPRESSION" size 28

            for expression_id, expression_label in LEIA_EXPRESSIONS:
                textbutton "[expression_label]":
                    action Function(set_leia_expression, expression_id)
                    selected leia_expression == expression_id

            null height 8
            text "OUTFIT" size 28
            text "Outfit is intentionally controlled by the Wardrobe system, not this sprite panel." size 19
            text "Equip an owned outfit in Wardrobe and Leia should refresh automatically." size 19

            null height 8
            textbutton "Reset pose + expression":
                action Function(debug_reset_leia_sprite)

            textbutton "Close controls":
                action Return()
