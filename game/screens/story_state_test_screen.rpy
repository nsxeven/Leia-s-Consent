# Development harness for story-state, choice-tag, and story-outfit mechanics.

screen dev_story_state_screen():
    use dev_menu_shell("STORY STATE FOUNDATION", "Test flags, one-time outcomes, behavioral choice tags, and story-granted outfits."):
        textbutton "Set demo story flag" action Return("set_flag") xfill True
        textbutton "Clear demo story flag" action Return("clear_flag") xfill True
        textbutton "Resolve pool outfit once (60/40)" action Return("resolve_pool") xfill True
        textbutton "Show story state summary" action Return("show_state") xfill True
        textbutton "Record encouraging tagged choice" action Return("choice_encourage") xfill True
        textbutton "Record protective tagged choice" action Return("choice_protective") xfill True
        textbutton "Show behavioral tag / stance summary" action Return("show_tags") xfill True
        textbutton "Grant + equip conservative pool outfit" action Return("grant_conservative") xfill True
        textbutton "Grant + equip bolder pool outfit" action Return("grant_bolder") xfill True
        textbutton "Open Wardrobe" action Return("wardrobe") xfill True
        textbutton "Reset story state" action Return("reset") xfill True
        textbutton "Back to systems menu" action Return("back") xfill True
