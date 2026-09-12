# Leia's Consent — Prologue
# Narrative beats favor full-screen CGs. Player decisions deliberately return to
# reusable backgrounds + sprites so choice moments remain readable and modular.

label prologue_name_setup:

    scene black
    with fade

    centered "{size=48}LEIA'S CONSENT{/size}\n\nBefore we begin..."

    $ entered_player_name = renpy.input("Your name", default=player_name, exclude="{}[]", length=20).strip()
    $ player_name = entered_player_name if entered_player_name else "Ryan"

    $ entered_girlfriend_name = renpy.input("Your girlfriend's name", default=girlfriend_name, exclude="{}[]", length=20).strip()
    $ girlfriend_name = entered_girlfriend_name if entered_girlfriend_name else "Leia"

    $ entered_friend_name = renpy.input("Your best friend's name", default=friend_name, exclude="{}[]", length=20).strip()
    $ friend_name = entered_friend_name if entered_friend_name else "Julian"

    jump prologue_start


label prologue_start:

    $ set_story_flag("prologue_started")

    scene black
    with fade
    centered "{size=54}FOUR YEARS AGO{/size}\n{size=34}End of First Year{/size}"

    # ---------------------------------------------------------------------
    # Scene 1 — College party arrival.
    # Full-screen CG: establish Leia as visually intimidating from Ryan's POV,
    # but keep the overall atmosphere ordinary, warm, and college-social.
    # ---------------------------------------------------------------------

    scene cg prologue_party_arrival
    with dissolve

    "I noticed [girlfriend_name] before I ever spoke to her."
    "That wasn't difficult. Half the room probably had."
    "She was standing with people I vaguely knew, looking like the kind of girl who already had better things to do than talk to me."

    mc "She's terrifying."

    friend "Who?"

    mc "Nobody."

    friend "You are literally looking at her."

    mc "I'm observing the room."

    friend "Very academically."

    "The groups merged eventually. Not because of fate. Not because [friend_name] had a plan."
    "Mostly because somebody dragged two chairs over and suddenly everyone was talking over everyone else."

    # ---------------------------------------------------------------------
    # Scene 2 — Leia speaks / Ryan discovers the dork beneath the first
    # impression. Narrative beat remains a full image.
    # ---------------------------------------------------------------------

    scene cg prologue_leia_nerdy
    with dissolve

    gf "Technically, you're both wrong."

    "She said it quietly enough that the conversation almost rolled straight over her."

    gf "...Never mind."

    mc "No, no. You can't say that and then retreat."

    gf "I can absolutely retreat."

    mc "Too late. Explain."

    "She did."
    "Not for ten seconds, either."
    "There were examples. There was context. At one point she used her drink to demonstrate something nobody had asked to see demonstrated."

    "And somewhere in the middle of it, the version of her I had invented from across the room disappeared."

    mc "Oh."

    gf "What?"

    mc "Nothing. Keep going."

    "She narrowed her eyes at me and continued anyway."

    # ---------------------------------------------------------------------
    # Decision 1 — flavor only. Switch away from CG to background + sprite.
    # This shapes Ryan's narrative voice, not relationship stats.
    # ---------------------------------------------------------------------

    scene bg prologue_party
    $ set_leia_sprite("p03", "smile")
    show leia at prologue_leia_left
    with dissolve

    "What was I actually thinking?"

    menu:
        "She's a complete dork.":
            $ set_story_value("prologue_ryan_first_impression", "dork")
            mc "You're a complete dork, aren't you?"
            gf "You made me explain it!"
            mc "And I'm glad I did."

        "She's way easier to talk to than I expected.":
            $ set_story_value("prologue_ryan_first_impression", "comfortable")
            mc "You're not what I expected."
            gf "That sounded dangerously close to an insult."
            mc "It wasn't."
            gf "Good recovery."

        "I am definitely in trouble.":
            $ set_story_value("prologue_ryan_first_impression", "smitten")
            "Right."
            "So the problem wasn't that she was intimidating anymore."
            "The problem was that now I actually liked talking to her."

    hide leia

    # ---------------------------------------------------------------------
    # Scene 3 — Group chemistry. Full-screen CG again after decision.
    # Ryan repeatedly makes conversational space for Leia.
    # ---------------------------------------------------------------------

    scene cg prologue_group_warmup
    with dissolve

    "The longer the night went on, the easier it became to notice something else about her."
    "[girlfriend_name] wasn't shy exactly. She could talk to anyone."
    "She just waited for openings that louder people never seemed interested in giving her."

    "So I started giving them back."

    mc "Wait, [girlfriend_name] was saying something."

    "A few minutes later—"

    mc "What do you think?"

    "Then again."

    mc "No, let her finish."

    "I didn't think much of it."
    "Apparently, she did."

    # ---------------------------------------------------------------------
    # Scene 4 — Truth or Dare / Leia's first admission.
    # ---------------------------------------------------------------------

    scene cg prologue_truth_reveal
    with dissolve

    "By the time somebody suggested Truth or Dare, the room had reached that specific stage of a college party where terrible ideas started sounding organized."

    "Most of the dares were harmless."
    "Somebody had to send an embarrassing text. Someone else drank something that should never have been mixed."
    "[girlfriend_name], meanwhile, had discovered an extremely advanced strategy."

    gf "Truth."

    friend "Again?"

    gf "Yes. Again."

    friend "Coward."

    gf "Alive coward."

    "The next question came from somewhere across the circle."

    "Who in this room do you like the most?"

    "[girlfriend_name] looked around once."
    "Then she pointed at me."

    mc "Me?"

    gf "You asked."

    "Nobody had asked me."
    "That did not seem important at the time."

    # ---------------------------------------------------------------------
    # Scene 5 — Julian pushes Dare, but Leia keeps agency over the kiss.
    # ---------------------------------------------------------------------

    scene cg prologue_before_kiss
    with dissolve

    friend "Okay. Next round, you are not choosing Truth again."

    gf "Watch me."

    friend "Chicken."

    gf "I'm not a chicken."

    friend "Then pick Dare."

    "Three people immediately joined in."
    "[girlfriend_name] looked around the circle, realized the room had turned against her, and sighed."

    gf "Fine. Dare."

    friend "Kiss [player_name]."

    "The room changed temperature."
    "Or maybe that was just me."

    "She looked at [friend_name]. Then at me."

    mc "You don't actually have to."

    gf "I know."

    "And then she moved closer anyway."

    # ---------------------------------------------------------------------
    # Scene 6 — First kiss. Full image, cinematic, no player decision.
    # ---------------------------------------------------------------------

    scene cg prologue_first_kiss
    with dissolve

    "It was not smooth."
    "Our noses nearly collided. Somebody laughed before we'd even figured out the angle."

    friend "Oh my God, just kiss already."

    "[girlfriend_name] laughed."
    "Then she kissed me."

    "Brief. Warm. Just awkward enough to be real."

    "The room cheered like we'd accomplished something."

    mc "...Does that mean I win Truth or Dare?"

    gf "No."

    mc "Worth asking."

    scene black
    with fade

    "And somehow... that was the beginning."

    $ set_story_flag("prologue_first_kiss_complete")

    # ---------------------------------------------------------------------
    # Scene 7 — Present day hard cut.
    # ---------------------------------------------------------------------

    scene cg prologue_present_stare
    with hpunch

    gf "[player_name]?"

    gf "You're staring again."

    mc "It never gets old."

    gf "Four years and you still haven't learned to be subtle."

    mc "Wasn't trying to be."

    "She tried not to smile and failed."

    # ---------------------------------------------------------------------
    # Scene 8 — Packing for their first overseas trip together.
    # ---------------------------------------------------------------------

    scene cg prologue_packing_banter
    with dissolve

    "Our first trip together had somehow taken four years."
    "College. Exams. Money. Work. The usual collection of reasons that always sounded temporary until another year disappeared."

    "Now there were two open suitcases on the floor and enough clothes on the bed to suggest [girlfriend_name] had misunderstood the length of the holiday."

    mc "You packed fourteen outfits."

    gf "Options."

    mc "That's two [girlfriend_name]s a day."

    gf "Exactly."

    mc "That did not explain anything."

    gf "It explained everything."

    "The trip wasn't just ours."
    "[friend_name] was coming too."
    "My best friend since before [girlfriend_name] and I were even a thing. The same idiot who had, technically, started the whole thing."

    $ phone_add_message(
        "group",
        "julian",
        text="I'm downstairs.",
        message_id="prologue_julian_downstairs_01",
        mark_unread=True,
    )
    $ phone_add_message(
        "group",
        "julian",
        text="If either of you makes us miss this flight I am leaving without you.",
        message_id="prologue_julian_downstairs_02",
        mark_unread=True,
    )

    "My phone buzzed twice."

    "[friend_name]: I'm downstairs."
    "[friend_name]: If either of you makes us miss this flight I am leaving without you."

    gf "He's been downstairs for two minutes."

    mc "He's rich. His time is worth more."

    gf "You say that every time he rushes you."

    mc "Because it's true."

    # ---------------------------------------------------------------------
    # Decision 2 — approved departure flavor choice. Background + sprite only.
    # ---------------------------------------------------------------------

    scene bg prologue_packing
    $ set_leia_sprite("p02", "smile")
    show leia at prologue_leia_left
    with dissolve

    gf "Ready?"

    menu:
        "Been ready.":
            $ set_story_value("prologue_departure_reply", "ready")
            mc "Been ready."
            gf "You were still packing ten minutes ago."
            mc "Emotionally ready."

        "I still think we're forgetting something.":
            $ set_story_value("prologue_departure_reply", "forgetting")
            mc "I still think we're forgetting something."
            gf "If we are, we're buying it there."
            mc "That is an expensive philosophy."

        "Ask me when [friend_name] starts snoring on the plane.":
            $ set_story_value("prologue_departure_reply", "snoring")
            mc "Ask me when [friend_name] starts snoring on the plane."
            gf "I'm recording it this time."

    hide leia

    # ---------------------------------------------------------------------
    # Scene 9 — Departure / prologue ending.
    # ---------------------------------------------------------------------

    scene cg prologue_departure
    with dissolve

    "Our first trip together."
    "Four years after [friend_name] dared her to kiss me."
    "The three of us, heading somewhere none of us had ever been."

    gf "[player_name]!"

    mc "Coming!"

    $ set_story_flag("prologue_complete")

    scene black
    with fade

    centered "{size=72}LEIA'S CONSENT{/size}\n{size=34}Every boundary starts somewhere.{/size}"

    scene black
    with fade

    centered "{size=58}CHAPTER ONE{/size}\n{size=40}SOMETHING DIFFERENT{/size}"

    return
