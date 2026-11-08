    $ enter_cinematic_mode()
    scene cg ch01_bedroom_window
    with dissolve

    gf "Wait. I'm definitely closing these first."

    $ lc_sfx("curtain")
    "She caught one of the light curtains and pulled it across the window."

    $ exit_cinematic_mode()
    scene bg ch01_master_bedroom_curtains
    with dissolve
    $ cast(ryan="casual", leia="towel", julian="travel")

    gf "...Seriously?"
    mc "What?"
    gf "These barely cover anything."

    "The thin fabric softened the view more than it actually blocked it."
    "I looked at the curtain, then at the towel wrapped around her."

    "{i}That barely covers anything either.{/i}"

    gf "What?"
    mc "Nothing."
    gf "You have that face."
    mc "I was just thinking you look good."
    gf "I'm wearing a towel."
    mc "Exactly."
    $ face("leia", "smile")
    gf "Pervert."

    $ lc_sfx("door_close")
    "She was smiling when she turned back toward the bathroom."
