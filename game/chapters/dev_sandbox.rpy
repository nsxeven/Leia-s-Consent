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

    menu:
        "Encourage [girlfriend_name]'s curiosity":
            $ change_stat("partner", "curiosity", 5)
            $ change_stat("player", "acceptance", 3)
            $ change_stat("relationship", "momentum", 1)

            gf "You're surprisingly open-minded about this."

        "Be more protective":
            $ change_stat("relationship", "trust", 3)
            $ change_stat("player", "jealousy", 3)
            $ change_stat("partner", "boundary_looseness", -2)

            gf "You're being a little protective today."

    "Open the panel once more to see how the choice changed the state."

    call screen dev_panel

    gf "That's enough for the first systems test."

    "Try saving here, quitting the game, and loading the save again. The names and stat values should still be intact."

    return
