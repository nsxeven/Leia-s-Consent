# Chapter One, Day Two: Leia asks Maya about Julian (scenes 19b and 19c).
# Inserted between scene 19 (Maya's goodbye banter) and scene 20 (dinner outfit).
# Flow: ch01_day2_scene_19 -> ch01_day2_scene_19b_leia_asks_maya
#       -> ch01_day2_scene_19c_back_outside -> ch01_day2_scene_20_dinner_outfit
#
# Off-screen Leia/Maya conversation (same convention as scenes 13 and 16); Ryan and
# Julian are out of earshot. Short, flirty, natural. Nothing here changes route lane,
# partner_stats or relationship_stats.
# The state lines and the "came back outside" block formerly at the end of scene 19
# live here (comfort/left_before_sunset in 19b; the rest in 19c).

label ch01_day2_scene_19b_leia_asks_maya:

    scene bg ch01_villa_living
    with dissolve

    "The villa entrance was cool and quiet after the heat of the pool deck."
    "Maya had her bag on one shoulder and her hand on the door when [girlfriend_name] spoke."

    gf "Wait. Can I ask you something?"
    maya "That is a terrifying way to start a sentence."
    gf "It's not bad. I promise."
    maya "That is what people say right before it's bad."
    gf "Maya."
    maya "Fine. Ask."

    gf "Are you into [friend_name]?"

    "Maya did not answer right away."

    maya "Wow. You just walked up and asked."
    gf "You insulted his sunglasses within thirty seconds of meeting him."
    maya "That is basic politeness."
    gf "You also remembered the bee thing."
    maya "That is practical safety information."
    gf "And you keep looking over when he isn't looking back."
    maya "I do not."
    gf "Maya."
    maya "I might. Occasionally. Scientifically."
    gf "So that's a yes."
    maya "That's a 'you're annoying.'"

    "[girlfriend_name] just grinned and waited. Maya held out for about three seconds."

    maya "Okay. Fine. Yes."
    maya "I'm interested. I have been since he moved six inches away from a bee and pretended it never happened."
    gf "I knew it."
    maya "Don't gloat."
    gf "I'm gloating a little."
    maya "And if he offers to share his room tonight, I'd happily end up in there."
    gf "Maya!"
    maya "What? You asked."
    gf "I did. I really did."
    maya "Now go back out there and act normal. I have to go look human."

    "[girlfriend_name] laughed and hugged her goodbye like they had known each other longer than a day."

    $ set_story_flag("ch01_d2_maya_julian_consent_established")
    $ set_story_flag("ch01_d2_maya_julian_talk_complete")
    $ set_story_value("ch01_d2_maya_julian_talk", "interested_room_share_ok")

    # Moved here from the end of scene 19 so the original state is preserved.
    $ set_story_value("ch01_d2_leia_maya_comfort", 4)
    $ set_story_flag("ch01_d2_maya_left_before_sunset")

    $ set_story_flag("ch01_d2_scene_19b_complete")
    jump ch01_day2_scene_19c_back_outside


label ch01_day2_scene_19c_back_outside:

    # Unchanged remainder of the original scene 19, split out so 19b can sit in the middle.
    scene bg ch01_pool_lounge
    with dissolve

    "When [girlfriend_name] came back outside, [friend_name] checked the time and stood."

    friend "I'm going up to get ready."
    mc "Already?"
    friend "Unlike you, I respect reservations."
    gf "That's not what you said this afternoon."
    friend "That was pool time. Different jurisdiction."

    "He headed upstairs, leaving [girlfriend_name] and me alone beside the water."

    $ set_story_flag("ch01_d2_julian_upstairs_before_sunset")
    $ set_story_flag("ch01_d2_scene_19_complete")
    jump ch01_day2_scene_20_dinner_outfit
