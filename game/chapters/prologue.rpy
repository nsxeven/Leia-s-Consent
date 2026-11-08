# Leia's Consent — Prologue
# Narrative beats favor full-screen CGs. Player decisions deliberately return to
# reusable backgrounds + sprites so choice moments remain readable and modular.

label prologue_name_setup:

    $ set_phone_unlocked(False)
    $ set_phone_hud_enabled(False)

    scene black
    with fade

    centered "{size=48}LEIA'S CONSENT{/size}\n\nBefore we begin..."

    # Ease from the title card onto the paper table before the name cards
    # appear (the cut straight into the first input felt abrupt).
    scene expression "gui/scrapbook/bg_table.png"
    with Dissolve(0.8)

    $ entered_player_name = renpy.input("Your name", default=player_name, exclude="{}[]", length=20).strip()
    $ player_name = entered_player_name if entered_player_name else "Ryan"

    $ entered_girlfriend_name = renpy.input("Your girlfriend's name", default=girlfriend_name, exclude="{}[]", length=20).strip()
    $ girlfriend_name = entered_girlfriend_name if entered_girlfriend_name else "Leia"

    $ entered_friend_name = renpy.input("Your best friend's name", default=friend_name, exclude="{}[]", length=20).strip()
    $ friend_name = entered_friend_name if entered_friend_name else "Julian"

    jump prologue_start


label prologue_start:

    $ set_story_flag("prologue_started")
    # Sprites come from the cast (systems/cast_staging.rpy).
    # Party outfit = black shirt stand-in until party art exists.

    scene black
    with fade
    centered "{size=54}FOUR YEARS AGO{/size}\n{size=34}End of First Year{/size}"

    scene cg prologue_party_arrival at lc_push_in
    with dissolve
    $ lc_amb("crowd")
    $ lc_bgm("party")  # muffled party pop under the chatter (darryn)

    "I noticed [girlfriend_name] before I ever spoke to her."
    "That wasn't difficult. Half the room probably had."
    "She was standing with people I vaguely knew, looking like the kind of girl who already had better things to do than talk to me."

    mc "I mean... she's kind of terrifying."
    friend "Who is? Wait, who are we talking about?"
    mc "Nobody. No one. Forget I said anything."
    friend "Dude, you're literally looking right at her. You haven't stopped looking at her since we walked in."
    mc "I'm not— I'm just looking at the room. In general."
    friend "Well, the room can see you looking, man. You couldn't make it more obvious if you waved."

    "The groups merged eventually, and it wasn't fate, and it definitely wasn't one of [friend_name]'s plans."
    "Mostly because somebody dragged two chairs over and suddenly everyone was talking over everyone else."

    scene cg prologue_party_couch
    with dissolve

    "For a while, we all ended up squeezed around the same couch, talking over drinks and whoever happened to be loudest."

    scene bg prologue_party
    with dissolve
    $ cast(leia="prologue_party")

    gf "Um, technically... I think you're both kind of wrong?"
    "She said it quietly enough that the conversation almost rolled straight over her."
    $ face("leia", "shy")
    gf "...Never mind."
    $ cast_add(ryan="prologue_party")
    mc "No, wait— you can't say that and then just retreat."
    $ face("leia", "smile")
    gf "I can, actually. Retreating is, like, my main skill."
    mc "Too late. Come on, I want to know why we're wrong."
    "She did."
    "Not for ten seconds, either."
    "There were examples. There was context. At one point she used her drink to demonstrate something nobody had asked to see demonstrated."
    "And somewhere in the middle of it, the version of her I had invented from across the room disappeared."

    mc "Oh."
    $ face("leia", "neutral")
    gf "What? Did I lose you? I lost you. Sorry, I do this."
    mc "No, nothing. You didn't lose me. Keep going."
    $ face("leia", "skeptical")
    "She narrowed her eyes at me and continued anyway."

    "What was I actually thinking?"

    menu:
        "She's a complete dork.":
            $ set_story_value("prologue_ryan_first_impression", "dork")
            mc "You're a complete dork, aren't you?"
            $ face("leia", "pout")
            gf "Hey! You made me explain it! You literally asked!"
            mc "I know. I mean it in a good way. Mostly."

        "She's way easier to talk to than I expected.":
            $ set_story_value("prologue_ryan_first_impression", "comfortable")
            mc "You're, um... not really what I expected."
            $ face("leia", "skeptical")
            gf "That sounded kind of like an insult? Like, dangerously close to one."
            mc "No, it's not— I mean, it's a good thing. You're easy to talk to."
            $ face("leia", "smile")
            gf "Hm. Okay. That's a pretty good recovery, I'll give you that."

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

    # Pacing Revision v2 — give Ryan and Leia one quiet pocket of time together
    # before Truth or Dare turns their chemistry into a public event.
    scene bg prologue_party_kitchen
    with dissolve
    $ lc_duck(0.25)
    $ cast(ryan="prologue_party", leia="prologue_party", julian="party")

    "A while later I escaped to the kitchen in search of another drink."
    "She was already there, studying the bottles on the counter like one of them had personally offended her."

    mc "Hey. Are you... hiding in here?"
    gf "Recharging."
    mc "Isn't that just another word for hiding?"
    $ face("leia", "skeptical")
    gf "No, I came in here to get a drink. Like a normal person."
    mc "You've been holding the same one for twenty minutes."
    $ face("leia", "shy")
    gf "...You noticed that?"
    mc "I mean... yeah. I noticed. Sorry, that sounds kind of creepy."

    "Without the rest of the room talking over us, the silence between sentences felt easy instead of awkward."

    gf "Honestly? I almost didn't come tonight. I was this close to staying in."
    mc "Wait, seriously? Why?"
    gf "Big groups are just... exhausting? Like, everyone's waiting for their turn to talk, and I never know when it's my turn."
    mc "You seemed fine, though. Out there, I mean."
    gf "I spent the first hour pretending to check my phone. I read the same text, like, nine times."
    mc "Well, it worked. I actually thought you were terrifying."
    $ face("leia", "skeptical")
    gf "Wait, terrifying? Me?"
    mc "Yeah. A little. In a good way?"
    gf "I was literally just standing there holding a red cup. What about that is scary?"
    mc "Menacingly."
    $ face("leia", "smile")
    gf "Oh my God. You're such an idiot."

    "She was laughing when she said it, though."
    "Someone shouted our names from the other room."

    gf "Oh no. I think that means we've been missed."
    mc "We could just... stay in here. Hide a bit longer."
    gf "Recharging. It's called recharging."
    mc "Right. Sorry."
    $ face("leia", "smile")
    gf "Come on. If I have to go back out there, so do you."

    # Both leave with the location change itself (one dissolve), then Leia enters.
    scene bg prologue_truthordare
    with dissolve
    $ lc_amb("crowd")
    $ lc_unduck()
    $ cast(ryan="prologue_party", leia="prologue_party", julian="party")

    "By the time somebody suggested Truth or Dare, the room had reached that specific stage of a college party where terrible ideas started sounding organized."
    "Most of the dares were harmless."
    "Somebody had to send an embarrassing text. Someone else drank something that should never have been mixed."
    "[girlfriend_name], meanwhile, had discovered an extremely advanced strategy."

    $ face("leia", "neutral")
    gf "Truth."
    friend "Again? That's, what, four in a row? You know you're allowed to pick the other one, right?"
    $ face("leia", "skeptical")
    gf "Yes, again. It's a perfectly good option."
    friend "It's a coward's option and you know it."
    $ face("leia", "smile")
    gf "Yeah, but I'm a coward who's still alive, so..."

    "The next question came from somewhere across the circle."
    "Who in this room do you like the most?"
    "[girlfriend_name] looked around once."
    "Then she pointed at me."

    $ lc_sfx("crowd_ooh")
    mc "Me?" with lc_punch()
    $ face("leia", "shy")
    gf "You asked."
    "Nobody had asked me."
    "That did not seem important at the time."
    friend "No. Nope. Next round you're not allowed to pick Truth again. I'm making that a rule."
    $ face("leia", "skeptical")
    gf "You can't just make up rules. Watch me."
    friend "Chicken. You're a total chicken, and everyone here knows it."
    $ face("leia", "pout")
    gf "I'm not a chicken! I just like knowing what's going to happen."
    friend "Then prove it. Pick Dare, just once."

    $ lc_sfx("cheer_small")
    "Three people immediately joined in."
    $ lc_sfx("leia_sigh")
    "[girlfriend_name] looked around the circle, realized the room had turned against her, and sighed."
    $ face("leia", "skeptical")
    gf "Fine. Fine! Dare. Ugh."
    # Dare lands: small screen shake (lc_shake respects the SCREEN SHAKE setting).
    $ lc_duck()
    $ lc_bgm_cut()  # comic beat: music stops dead on the scratch
    $ lc_sfx("record_scratch")
    friend "Kiss [player_name]." with lc_shake("s")
    $ face("leia", "flustered")
    "The room changed temperature."
    "Or maybe that was just me."
    "She looked at [friend_name]. Then at me."

    mc "Hey, you don't actually have to. Seriously."
    $ face("leia", "shy")
    gf "I know."
    "And then she moved closer anyway."
    scene cg prologue_first_kiss_01
    with dissolve

    "She leaned toward me, cheeks burning, like she was still deciding whether this was actually happening."

    scene cg prologue_first_kiss_02
    with dissolve
    $ lc_breath_once()  # soft inhale on Leia's CG (darryn: less static)

    "It was not smooth."
    "Our noses nearly collided. Somebody laughed before we'd even figured out the angle." with lc_shake("s")
    friend "You guys, it's not that complicated. Just kiss already."
    $ lc_sfx("leia_laugh")
    "[girlfriend_name] laughed."

    scene cg prologue_first_kiss_03
    with dissolve

    $ lc_flash("#ffe2cf", 0.4, 0.9)
    $ lc_sfx("leia_kiss")  # darryn's kiss sound (VOICE slider)
    "Then she kissed me."
    "Brief. Warm. Just awkward enough to be real."
    $ lc_bgm_resume()
    $ lc_unduck()
    $ lc_sfx("cheer_small")
    "The room cheered like we'd accomplished something."

    scene bg prologue_truthordare
    with dissolve
    $ cast(ryan="prologue_party", leia="prologue_party", julian="party")
    $ face("leia", "smile")

    mc "So, um... does that mean I win Truth or Dare?"
    gf "No. That's— no. That's not how it works."
    mc "Worth asking, though."
    scene black
    with fade
    $ lc_amb_stop()
    $ lc_bgm_stop()
    "And somehow... that was the beginning."

    $ set_story_flag("prologue_first_kiss_complete")

    scene cg prologue_present_stare
    with dissolve
    $ lc_breath_once()  # Leia's soft inhale on each packing CG (darryn)
    $ lc_amb("room_tone")
    $ lc_bgm("cozy_home")

    gf "[player_name]?"
    gf "You're staring again. You're doing the thing."
    mc "Sorry. I mean... not really sorry. It never gets old."
    gf "Four years, and you still haven't learned how to be subtle about it. Like, at all."
    mc "I wasn't really trying to be."
    "She tried not to smile and failed."
    $ lc_sfx("suitcase_zip")
    "She reached for my hand, gave it a quick squeeze, and went back to packing as though it were the most ordinary thing in the world."

    scene cg prologue_packing_banter
    with dissolve
    $ lc_breath_once()  # Leia's soft inhale on each packing CG (darryn)

    "Our first trip together had somehow taken four years."
    "College. Exams. Money. Work. The usual collection of reasons that always sounded temporary until another year disappeared."
    "Now there were two open suitcases on the floor and enough clothes on the bed to suggest [girlfriend_name] had misunderstood the length of the holiday."

    mc "You know you packed fourteen outfits, right? I counted."
    gf "They're options. You need options on holiday, it's like, a whole thing."
    mc "That's two [girlfriend_name]s a day."
    gf "Yeah, that's— yes. Beach me and dinner me. That's the plan."
    mc "That doesn't really explain anything."
    gf "It explains everything, you're just not listening."

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

    $ lc_sfx("car_horn")
    gf "He's been downstairs for two minutes. Two! Why is he already honking?"
    mc "He's rich, though. His minutes cost more than ours."
    gf "You say that every time he rushes you. He hates it when you say that."
    mc "Yeah, that's kind of why I say it."
    gf "Tell him we'll be down in two minutes."
    mc "You said two minutes before he even got here. So that's four. Five, probably."
    "She didn't even look up."

    scene bg prologue_packing
    with dissolve
    $ lc_amb("room_tone")
    $ cast(ryan="casual", leia="casual")
    $ face("leia", "smile")

    gf "Okay! Ready? Do you have everything?"

    menu:
        "Been ready.":
            $ set_story_value("prologue_departure_reply", "ready")
            mc "Been ready."
            $ face("leia", "skeptical")
            gf "You were literally still packing ten minutes ago. I watched you."
            mc "Emotionally ready."
            $ face("leia", "smile")

        "I still think we're forgetting something.":
            $ set_story_value("prologue_departure_reply", "forgetting")
            mc "I still think we're forgetting something."
            $ face("leia", "neutral")
            gf "If we are, we'll just buy it there. That's what shops are for."
            mc "That's... kind of an expensive way to live."
            $ face("leia", "smile")

        "Ask me when [friend_name] starts snoring on the plane.":
            $ set_story_value("prologue_departure_reply", "snoring")
            mc "Ask me when [friend_name] starts snoring on the plane."
            $ face("leia", "smile")
            gf "Oh my God, yes. I'm recording it this time, he can't keep saying he doesn't snore."


    $ enter_cinematic_mode()

    scene cg prologue_departure at lc_push_in
    with dissolve
    $ lc_breath_once()  # Leia's soft inhale on each packing CG (darryn)
    $ lc_sfx("suitcase_wheels")

    "Our first trip together."
    "Four years after [friend_name] dared her to kiss me."
    "The three of us, heading somewhere none of us had ever been."

    gf "[player_name]!"
    mc "Coming!"
    $ lc_sfx("door_close")

    $ set_story_flag("prologue_complete")
    $ set_story_flag("prologue_story_locked")

    scene black
    with fade
    $ lc_amb_stop()
    $ lc_bgm_stop(3.0)
    centered "{size=72}LEIA'S CONSENT{/size}\n{size=34}Every boundary starts somewhere.{/size}"

    scene black
    with fade
    centered "{size=58}CHAPTER ONE{/size}\n{size=40}SOMETHING DIFFERENT{/size}"

    $ exit_cinematic_mode()

    jump chapter_one_start
