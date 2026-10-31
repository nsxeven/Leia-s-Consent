# Shared developer-menu layout and reusable sandbox menu screens.
# Development menus use a consistent titled, scrollable frame so they remain
# usable as more tools are added.

screen dev_menu_shell(title, subtitle=None):

    modal True
    zorder 260

    key "K_ESCAPE" action Return("back")

    add "gui/scrapbook/bg_table.png"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1220
        ysize 920
        background Frame("gui/scrapbook/frame_paper.png", 9, 9)
        padding (36, 30)

        vbox:
            spacing 18
            xfill True
            yfill True

            text title size 42 color "#3b2a30" xalign 0.5

            if subtitle:
                text subtitle size 19 color "#aaa0aa" xalign 0.5 text_align 0.5

            use lc_scroll_body:
                vbox:
                    spacing 14
                    xfill True
                    transclude


screen dev_gallery_lab_screen():
    use dev_menu_shell("GALLERY TEST", "Persistent Gallery unlocks and placeholder CG previews."):
        textbutton "Open Gallery" action Return("open") xfill True
        textbutton "Unlock \"Villa arrival\" (d1_arrival)" action Return("unlock_one") xfill True
        textbutton "Unlock all Gallery entries" action Return("unlock_all") xfill True
        textbutton "Reset Gallery unlocks and seen CGs" action Return("reset") xfill True
        textbutton "Show Gallery unlock state" action Function(dev_notify_gallery_state) xfill True
        textbutton "How do I test persistence?" action Return("persistence_help") xfill True
        textbutton "Back to systems menu" action Return("back") xfill True


screen dev_sprite_lab_screen():
    use dev_menu_shell("SPRITE SYSTEM TEST", "Pose, expression, and wardrobe state share one sprite controller."):
        textbutton "Open pose + expression controls" action Return("controls") xfill True
        textbutton "Open Wardrobe to change the visible outfit" action Return("wardrobe") xfill True
        textbutton "Unlock all current outfits for sprite testing" action Function(debug_unlock_all_outfits) xfill True
        textbutton "Open Developer Panel" action Return("developer") xfill True
        textbutton "Show exact sprite state" action Function(dev_notify_sprite_state) xfill True
        textbutton "How do I test outfit switching?" action Return("outfit_help") xfill True
        textbutton "Continue to save/load verification" action Return("verify") xfill True
        textbutton "Back to systems menu" action Return("back") xfill True


screen dev_wardrobe_lab_screen():
    use dev_menu_shell("ECONOMY + WARDROBE TEST", "Buying and wearing remain separate mechanics."):
        textbutton "Open Outfit Shop" action Return("shop") xfill True
        textbutton "Open Wardrobe" action Return("wardrobe") xfill True
        textbutton "Open Player Transparency Settings" action Return("settings") xfill True
        textbutton "Open Developer Panel" action Return("developer") xfill True
        textbutton "Show current economy + wardrobe state" action Function(dev_notify_economy_state) xfill True
        textbutton "How do I test the gated outfit?" action Return("gated_help") xfill True
        textbutton "Continue to save/load verification" action Return("verify") xfill True
        textbutton "Back to systems menu" action Return("back") xfill True


screen dev_verify_state_screen():
    use dev_menu_shell("VERIFICATION / SAVE-STATE", "Quick access to current state and persistence checks."):
        textbutton "Open Integrated systems slice" action Return("vertical_slice") xfill True
        textbutton "Open Gallery" action Return("gallery") xfill True
        textbutton "Open Player Settings / Transparency" action Return("settings") xfill True
        textbutton "Open Player Status screen" action Return("status") xfill True
        textbutton "Show current character names" action Function(dev_notify_character_names) xfill True
        textbutton "Open Sprite System test" action Return("sprite") xfill True
        textbutton "Show sprite state" action Function(dev_notify_sprite_state) xfill True
        textbutton "Open Developer Panel" action Return("developer") xfill True
        textbutton "Open Developer Choice Display controls" action Return("choice_controls") xfill True
        textbutton "Show recorded choice state" action Function(dev_notify_choice_state) xfill True
        textbutton "Open Outfit Shop" action Return("shop") xfill True
        textbutton "Open Wardrobe" action Return("wardrobe") xfill True
        textbutton "Show economy + wardrobe state" action Function(dev_notify_economy_state) xfill True
        textbutton "Repeat save/load instructions" action Return("save_help") xfill True
        textbutton "Back to systems menu" action Return("back") xfill True
        textbutton "Finish systems test and return to the main menu" action Return("finish") xfill True


screen dev_vertical_slice_checkpoint_screen():
    use dev_menu_shell("INTEGRATION CHECKPOINT", "Use the buttons below without advancing the underlying story interaction."):
        textbutton "Show current checkpoint state" action Function(dev_notify_checkpoint_state) xfill True
        textbutton "Open Status" action Return("status") xfill True
        textbutton "Open Wardrobe" action Return("wardrobe") xfill True
        textbutton "Open Shop" action Return("shop") xfill True
        textbutton "Open Gallery" action Return("gallery") xfill True
        textbutton "Open Transparency Settings" action Return("settings") xfill True
        textbutton "Open Developer Panel" action Return("developer") xfill True
        textbutton "Save/load checkpoint instructions" action Return("save_help") xfill True
        textbutton "Restart the integrated slice" action Return("restart") xfill True
        textbutton "Back to systems menu" action Return("back") xfill True
