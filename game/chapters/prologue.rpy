# Leia's Consent — Prologue
# Narrative beats favor full-screen CGs. Player decisions deliberately return to
# reusable backgrounds + sprites so choice moments remain readable and modular.

label prologue_name_setup:

    $ set_phone_unlocked(False)
    $ set_phone_hud_enabled(False)

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
    friend "You can't make it any more obvious."

    "The groups merged eventually. Not because of fate. Not because [friend_name] had a plan."
    "Mostly because somebody dragged two chairs over and suddenly everyone was talking over everyone else."

    scene cg prologue_party_couch
    with dissolve

    "For a while, we all ended up squeezed around the same couch, talking over drinks and whoever happened to be loudest."

    scene bg prologue_party
    show leia_prologue_party neutral at prologue_sprite_enter_left, leia_body_idle
    with sprite_enter_exit

    gf "Technically, you're both wrong."
    "She said it quietly enough that the conversation almost rolled straight over her."
    show leia_prologue_party shy
    with sprite_change
    gf "...Never mind."
    mc "No, no. You can't say that and then retreat."
    show leia_prologue_party smile
    with sprite_change
    gf "I can absolutely retreat."
    mc "Too late. Explain."
    "She did."
    "Not for ten seconds, either."
    "There were examples. There was context. At one point she used her drink to demonstrate something nobody had asked to see demonstrated."
    "And somewhere in the middle of it, the version of her I had invented from across the room disappeared."

    mc "Oh."
    show leia_prologue_party neutral
    with sprite_change
    gf "What?"
    mc "Nothing. Keep going."
    show leia_prologue_party skeptical
    with sprite_change
    "She narrowed her eyes at me and continued anyway."

    "What was I actually thinking?"

    menu:
        "She's a complete dork.":
            $ set_story_value("prologue_ryan_first_impression", "dork")
            mc "You're a complete dork, aren't you?"
            show leia_prologue_party pout
            with sprite_change
            gf "You made me explain it!"
            mc "And I'm glad I did."

        "She's way easier to talk to than I expected.":
            $ set_story_value("prologue_ryan_first_impression", "comfortable")
            mc "You're not what I expected."
            show leia_prologue_party skeptical
            with sprite_change
            gf "That sounded dangerously close to an insult."
            mc "It wasn't."
            show leia_prologue_party smile
            with sprite_change
            gf "Good recovery."

        "I am definitely in trouble.":
            $ set_story_value("prologue_ryan_first_impression", "smitten")
            "Right."
            "So the problem wasn't that she was intimidating anymore."
            "The problem was that now I actually liked talking to her."

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

    scene bg prologue_truthordare
    show leia_prologue_party neutral at prologue_sprite_enter_left, leia_body_idle
    with dissolve

    "By the time somebody suggested Truth or Dare, the room had reached that specific stage of a college party where terrible ideas started sounding organized."
    "Most of the dares were harmless."
    "Somebody had to send an embarrassing text. Someone else drank something that should never have been mixed."
    "[girlfriend_name], meanwhile, had discovered an extremely advanced strategy."

    show leia_prologue_party neutral
    with sprite_change
    gf "Truth."
    friend "Again?"
    show leia_prologue_party skeptical
    with sprite_change
    gf "Yes. Again."
    friend "Coward."
    show leia_prologue_party smile
    with sprite_change
    gf "Alive coward."

    "The next question came from somewhere across the circle."
    "Who in this room do you like the most?"
    "[girlfriend_name] looked around once."
    "Then she pointed at me."

    show ryan_prologue_party at prologue_ryan_enter_right, leia_body_idle
    with sprite_enter_exit
    mc "Me?"
    show leia_prologue_party shy
    with sprite_change
    gf "You asked."
    "Nobody had asked me."
    "That did not seem important at the time."
    hide ryan_prologue_party
    with sprite_enter_exit
    friend "Okay. Next round, you are not choosing Truth again."
    show leia_prologue_party skeptical
    with sprite_change
    gf "Watch me."
    friend "Chicken."
    show leia_prologue_party pout
    with sprite_change
    gf "I'm not a chicken."
    friend "Then pick Dare."

    "Three people immediately joined in."
    "[girlfriend_name] looked around the circle, realized the room had turned against her, and sighed."
    show leia_prologue_party skeptical
    with sprite_change
    gf "Fine. Dare."
    friend "Kiss [player_name]."
    show leia_prologue_party flustered
    with sprite_change
    "The room changed temperature."
    "Or maybe that was just me."
    "She looked at [friend_name]. Then at me."

    mc "You don't actually have to."
    show leia_prologue_party shy
    with sprite_change
    gf "I know."
    "And then she moved closer anyway."
    hide leia_prologue_party
    hide ryan_prologue_party
    scene cg prologue_first_kiss_01
    with dissolve

    "She leaned toward me, cheeks burning, like she was still deciding whether this was actually happening."

    scene cg prologue_first_kiss_02
    with dissolve

    "It was not smooth."
    "Our noses nearly collided. Somebody laughed before we'd even figured out the angle."
    friend "Oh my God, just kiss already."
    "[girlfriend_name] laughed."

    scene cg prologue_first_kiss_03
    with dissolve

    "Then she kissed me."
    "Brief. Warm. Just awkward enough to be real."
    "The room cheered like we'd accomplished something."

    scene bg prologue_truthordare
    show leia_prologue_party smile at prologue_sprite_enter_left, leia_body_idle
    show ryan_prologue_party at prologue_ryan_enter_right, leia_body_idle
    with sprite_enter_exit

    mc "...Does that mean I win Truth or Dare?"
    gf "No."
    mc "Worth asking."
    hide leia_prologue_party
    hide ryan_prologue_party
    scene black
    with fade
    "And somehow... that was the beginning."

    $ set_story_flag("prologue_first_kiss_complete")

    scene cg prologue_present_stare

    gf "[player_name]?"
    gf "You're staring again."
    mc "It never gets old."
    gf "Four years and you still haven't learned to be subtle."
    mc "Wasn't trying to be."
    "She tried not to smile and failed."

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
        notify=True,
        notification_title="Trip Group",
    )

    # The Phone notification already presents Julian's message; do not
    # duplicate its contents through the VN textbox.

    $ phone_add_message(
        "group",
        "julian",
        text="If either of you makes us miss this flight I am leaving without you.",
        message_id="prologue_julian_downstairs_02",
        mark_unread=True,
        notify=True,
        notification_title="Trip Group",
    )

    # Second notification is likewise left to the Phone UI.

    $ phone_unlock_with_tutorial()
    $ set_phone_hud_enabled(True)

    gf "He's been downstairs for two minutes."
    mc "He's rich. His time is worth more."
    gf "You say that every time he rushes you."
    mc "Because it's true."

    scene bg prologue_packing
    show leia_casual smile at prologue_sprite_enter_left, leia_body_idle
    with sprite_enter_exit

    gf "Ready?"

    menu:
        "Been ready.":
            $ set_story_value("prologue_departure_reply", "ready")
            mc "Been ready."
            show leia_casual skeptical
            with sprite_change
            gf "You were still packing ten minutes ago."
            mc "Emotionally ready."
            show leia_casual smile
            with sprite_change

        "I still think we're forgetting something.":
            $ set_story_value("prologue_departure_reply", "forgetting")
            mc "I still think we're forgetting something."
            show leia_casual neutral
            with sprite_change
            gf "If we are, we're buying it there."
            mc "That is an expensive philosophy."
            show leia_casual smile
            with sprite_change

        "Ask me when [friend_name] starts snoring on the plane.":
            $ set_story_value("prologue_departure_reply", "snoring")
            mc "Ask me when [friend_name] starts snoring on the plane."
            show leia_casual smile
            with sprite_change
            gf "I'm recording it this time."


    hide leia_casual
    $ enter_cinematic_mode()

    scene cg prologue_departure
    with dissolve

    "Our first trip together."
    "Four years after [friend_name] dared her to kiss me."
    "The three of us, heading somewhere none of us had ever been."

    gf "[player_name]!"
    mc "Coming!"

    $ set_story_flag("prologue_complete")
    $ set_story_flag("prologue_story_locked")

    scene black
    with fade
    centered "{size=72}LEIA'S CONSENT{/size}\n{size=34}Every boundary starts somewhere.{/size}"

    scene black
    with fade
    centered "{size=58}CHAPTER ONE{/size}\n{size=40}SOMETHING DIFFERENT{/size}"

    $ exit_cinematic_mode()

    jump chapter_one_start
