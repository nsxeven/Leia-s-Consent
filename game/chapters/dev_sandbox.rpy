# Temporary systems sandbox.
# This will be removed/replaced once the core mechanics are proven.

image bg dev = Solid("#17151a")

label dev_name_setup:

    scene bg dev

    centered "Personalize your development playthrough"

    $ entered_player_name = renpy.input("Your name", default=player_name, exclude="{}[]", length=20).strip()
    $ player_name = entered_player_name if entered_player_name else "Ryan"

    $ entered_girlfriend_name = renpy.input("Your girlfriend's name", default=girlfriend_name, exclude="{}[]", length=20).strip()
    $ girlfriend_name = entered_girlfriend_name if entered_girlfriend_name else "Leia"

    $ entered_friend_name = renpy.input("Your friend's name", default=friend_name, exclude="{}[]", length=20).strip()
    $ friend_name = entered_friend_name if entered_friend_name else "Julian"

    "You: [player_name]\nGirlfriend: [girlfriend_name]\nFriend: [friend_name]"

    menu:
        "Use these names":
            jump dev_sandbox

        "Change them again":
            jump dev_name_setup


label dev_sandbox:

    scene bg dev

    gf "The Leia's Consent development sandbox is running."

    mc "This isn't Chapter 1 yet. We're testing the systems underneath it."

    friend "Apparently I'm here to make things complicated later."

    "First, open the Developer Panel and change a few values."

    call screen dev_panel

    "Current NTS tendency: [nts_score()]."
    "Current NTR tendency: [ntr_score()]."

    "Next we'll test the choice engine. You can switch between all four display modes and watch the live preview change."

    call screen choice_mode_screen

    jump dev_choice_test


label dev_choice_test:

    $ encourage_choice_text = format_choice("dev_encourage_curiosity", "Encourage {}'s curiosity".format(girlfriend_name))
    $ protective_choice_text = format_choice("dev_be_protective", "Be more protective")

    menu:
        "[encourage_choice_text]":
            $ apply_choice("dev_encourage_curiosity")
            gf "You're surprisingly open-minded about this."

        "[protective_choice_text]":
            $ apply_choice("dev_be_protective")
            gf "You're being a little protective today."

    "The choice was applied using the central choice-effect table rather than hard-coded stat changes in this scene."

    "Open the Developer Panel once more to see the new values."

    call screen dev_panel

    gf "That's enough for the current systems test."

    "Save the game now, quit completely, reopen Leia's Consent, and load this save. After loading, use the verification menu to confirm the names, stats, and choice state survived."

    jump dev_verify_state


label dev_verify_state:

    menu:
        "Show current character names":
            "You: [player_name]\nGirlfriend: [girlfriend_name]\nFriend: [friend_name]"
            jump dev_verify_state

        "Open Developer Panel to check stats":
            call screen dev_panel
            jump dev_verify_state

        "Open Choice Display Mode settings":
            call screen choice_mode_screen
            jump dev_verify_state

        "Show recorded choice state":
            "Last choice ID: [last_choice_id]\nChoices recorded this playthrough: [len(choice_history)]"
            jump dev_verify_state

        "Repeat save/load instructions":
            "While this verification menu is active, open Save from the quick menu. Save to a slot, quit the game completely, reopen it, choose Load, and load that slot."
            "If you return to this same verification menu, your save position persisted. Then check the names, Developer Panel, and recorded choice state above."
            jump dev_verify_state

        "Test another choice":
            "This will apply another set of stat effects and add another choice ID to the history."
            call screen choice_mode_screen
            jump dev_choice_test

        "Finish systems test and return to the main menu":
            return
