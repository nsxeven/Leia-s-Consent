# Scrollable development systems menu.
# Uses the same titled/scrollable developer template as the other sandbox menus.

screen dev_systems_menu_screen():
    use dev_menu_shell("SYSTEMS TEST MENU", "Choose which system you want to test."):
        textbutton "Integrated systems slice (Phase 9)" action Return("vertical_slice") xfill True
        textbutton "Story State foundation test" action Jump("dev_story_state_test") xfill True
        textbutton "Gallery shell test" action Return("gallery") xfill True
        textbutton "Player Settings / Transparency test" action Return("settings") xfill True
        textbutton "Player Status screen test" action Return("status") xfill True
        textbutton "Economy + Wardrobe test" action Return("economy") xfill True
        textbutton "Choice Engine test" action Return("choice") xfill True
        textbutton "Reset Phone tutorial (persistent)" action Function(debug_reset_phone_tutorial) xfill True
        textbutton "Open Developer Panel" action Return("developer") xfill True
        textbutton "Open verification / save-state menu" action Return("verify") xfill True
        textbutton "Finish systems test and return to the main menu" action Return("finish") xfill True
