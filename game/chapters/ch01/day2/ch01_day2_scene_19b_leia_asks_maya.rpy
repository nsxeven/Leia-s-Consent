# Chapter One, Day Two: Leia asks Maya about Julian (scenes 19b and 19c).
# Inserted between scene 19 (Maya's goodbye banter) and scene 20 (dinner outfit).
# Flow: ch01_day2_scene_19 -> ch01_day2_scene_19b_leia_asks_maya
#       -> ch01_day2_scene_19b2_ryan_dozes -> Leia's errand (ch01_day2_leia_errand.rpy)
#       -> ch01_day2_scene_19c_back_outside -> ch01_day2_scene_20_dinner_outfit
#
# Off-screen Leia/Maya conversation (same convention as scenes 13 and 16); Ryan and
# Julian are out of earshot. Short, flirty, natural. Nothing here changes route lane,
# partner_stats or relationship_stats.
# The state lines and the "came back outside" block formerly at the end of scene 19
# live here (comfort/left_before_sunset in 19b; the rest in 19c).

label ch01_day2_scene_19b_leia_asks_maya:

    scene bg ch01_villa_entry_day  # front door, afternoon: Maya leaving (day art, darryn)
    with dissolve

    "The villa entrance was cool and quiet after the heat of the pool deck."
    "Maya had her bag on one shoulder and her hand on the door when [girlfriend_name] spoke."

    gf "Wait. Can I ask you something?"
    maya "Oh no. That's the scariest way anyone's ever started a sentence."
    gf "It's not bad. I promise."
    maya "That is what people say right before it's bad."
    gf "Maya."
    maya "Fine. Fine, ask. I'm braced."

    gf "So it's not— you're going to laugh at me. Are you into [friend_name]?"

    "Maya did not answer right away."

    maya "Wow. You just walked right up and asked."
    gf "You insulted his sunglasses within thirty seconds of meeting him."
    maya "Somebody had to! They cover half his face. I was being, like, a good citizen about it."
    gf "You also remembered the bee thing."
    maya "Okay, that was funny, though. And it's useful! If a bee shows up, we all need to know he's leaving first."
    gf "And you keep looking over when he isn't looking back."
    maya "I do not."
    gf "Maya. You do. I've seen you do it, like, four times."
    maya "I might. Occasionally. Scientifically."
    gf "So that's a yes."
    maya "That's a— no. That's a you're-annoying. Stop smiling at me like that."

    "[girlfriend_name] just grinned and waited. Maya held out for about three seconds."

    maya "Okay. Fine. Yes."
    maya "I'm interested. I have been since he moved six inches away from a bee and pretended it never happened."
    gf "I knew it! I called it."
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
    jump ch01_day2_scene_19b2_ryan_dozes


label ch01_day2_scene_19c_back_outside:

    # Unchanged remainder of the original scene 19, split out so 19b can sit in the middle.
    scene bg ch01_pool_lounge
    with dissolve

    # Leia's errand (ch01_day2_leia_errand.rpy) ends here with her waking him. A save from before
    # the errand existed (no ch01_d2_errand_lane) keeps the original line.
    $ d2_errand_lane = get_story_value("ch01_d2_errand_lane")
    if d2_errand_lane is None:
        "When [girlfriend_name] came back outside, [friend_name] checked the time and stood."
    else:
        "Something very cold pressed against the side of my neck."
        mc "Ah! What? What is that?"
        gf "Hi. You were snoring."
        "I opened my eyes. [girlfriend_name] was crouched beside the lounger, holding a caramel frappuccino against my neck and looking extremely pleased with herself."
        mc "Is that... wait, is that a caramel frappuccino?"
        gf "Large. Extra caramel, on top and in it. I asked. I ran the last bit so it wouldn't melt, in flip-flops, so you have to appreciate it."
        "She put a paper bag on my stomach next."
        gf "And these. Last box. I had to fight a tower of banana bread for them."
        mc "Chocolate muffins? When did you even go?"
        gf "While you were asleep. [friend_name] was my lookout."
        friend "I didn't see anything, for the record. I was just a guy under an umbrella. I didn't even drop anything, which I think was the main part of the job."

        if get_story_value("ch01_d2_errand_reason") == "dream":
            gf "You had a bad night, and you actually told me about it, so you get your favorite things. That's the rule now."
            think "I'd told her about the dream mostly to get it out of my head. I hadn't expected her to do anything with it."
        else:
            gf "You've been quiet all day. I can't fix that, but I can do frappuccinos. So."
            think "I'd thought I was hiding it pretty well. Apparently I'd been hiding it from nobody."

        mc "This is... thank you. Really. You didn't have to."
        gf "I know. I wanted to, though. Now drink it before it melts all over you."

        if d2_errand_lane == "love":
            "She hugged me before I could sit all the way up. Longer than usual, with her face against my shoulder, like she'd had a longer walk than ten minutes. I didn't ask. I just let her."
        elif d2_errand_lane == "exhibitionism":
            "She was pink across the cheeks, like she'd spent a lot longer in the sun than a coffee run takes."
            if lc_leia_did("ch01_d2_shop_top_left"):
                "Her top had slid halfway off one shoulder. She saw me notice and didn't fix it."
        elif get_story_value("ch01_d2_leia_told") == "told":
            "She sat down on the end of the lounger and watched me take the first sip, like she was waiting for something."
        else:
            "She sat down on the end of the lounger and watched me take the first sip. Then she watched the pool for a while."

        gf "[friend_name], do you want one? Lookout tax."
        friend "Oh. No, I'm good, they're his. ...Okay, maybe one. A small one. Is there a small one?"
        "There wasn't a small one. He took one anyway, ate it in about three bites, then checked the time and stood up."

    friend "I'm going to go up and get ready."
    mc "Already? We've got ages."
    friend "Unlike some people, I like being on time for a reservation. I've been late with you before. Many, many times."
    gf "Since when do you care about being on time?"
    friend "Since he made us forty minutes late to my own birthday dinner in college. I still think about it."

    "He headed upstairs, leaving [girlfriend_name] and me alone beside the water."

    # v0.2.0 flavor: pays off the scene 15 "very boring sunscreen stuff" whisper.
    gf "Finally. That was the very boring sunscreen stuff, by the way."
    mc "[friend_name] going to get ready was the secret?"
    gf "Getting you on your own before dinner was the secret. I asked Maya how you get one person alone in a house full of people, and she said just wait, everybody leaves eventually."
    gf "I was ready to be really disappointed in that advice, and then it worked. Don't tell her it worked."

    # Leia's confession (told path, NTR-risk errand only). Ryan's reply is his own scored choice:
    # never capped, and left out of tonight's lane and end route (CH01_D2_ERRAND_EXEMPT_CHOICES).
    if get_story_value("ch01_d2_leia_told") == "told":
        "Then she stopped smiling. It didn't happen all at once. It sort of drained out of her face, and she turned on the lounger so she was facing me properly."
        gf "Okay. I need to tell you something before I chicken out."
        mc "That sounds bad."
        gf "It's not bad bad. I don't think. Just let me get it all out, and then you can say stuff."
        gf "At the café, some guy... he spanked me. Like, a real smack, right on my butt, really loud."
        "I just looked at her."
        gf "He was gross. He was this sweaty guy with way too much aftershave, and he just did it while I was waiting for your drink, and I didn't even say anything. I just stood there."
        if lc_leia_did("ch01_d2_cafe_ntr_lingered"):
            gf "And then he kept talking, and I let him, for way longer than I should have. I didn't say yes to anything. I just didn't say no fast enough."
        gf "And for one second right after, before I got angry, I didn't hate it. That freaked me out way more than he did."
        gf "I didn't want to sit on it all night and smile at you like nothing happened. So. That's all of it. That's everything."

        $ d2_confession_ask_text = format_choice("ch01_d2_confession_ask", "Ask her how it felt.")
        $ d2_confession_protect_text = format_choice("ch01_d2_confession_protect", "Make sure she's okay.")
        $ d2_confession_brush_text = format_choice("ch01_d2_confession_brush", "\"Weird guy. Glad you're okay.\"")
        menu:
            "[d2_confession_ask_text]":
                $ apply_choice("ch01_d2_confession_ask")
                $ set_story_value("ch01_d2_confession_reply", "asked")
                mc "When you say you didn't hate it... what did it actually feel like?"
                "[girlfriend_name] stared at me. Whatever she'd been bracing for, it wasn't that."
                gf "You're not mad?"
                mc "Not at you. I'd kind of like to go throw his drink at him. But I'm asking."
                gf "It felt... I don't know. Warm? Embarrassing. Like everybody in the café could see my face doing something, and I couldn't make it stop."
                "She laughed, a short surprised laugh, and covered her mouth with her hand."
                gf "Why is that easier to say to you than it was to think it?"
                "Her shoulders came down. For the first time since she'd sat down, she looked like herself again."
                think "I didn't know what I was feeling either. Jealousy was part of it. I didn't have a word yet for the rest."

            "[d2_confession_protect_text]":
                $ apply_choice("ch01_d2_confession_protect")
                $ set_story_value("ch01_d2_confession_reply", "protective")
                mc "Hey. Are you okay? Did he do anything else? He didn't follow you out?"
                gf "No. No, he just went back outside. I'm okay."
                mc "You don't have to be okay about it. I mean, he's the one who did something wrong here. Some guy did that to you while you were buying me a coffee."
                gf "But the part where I didn't hate it..."
                mc "I'm not— I'm not going to be weird about that part. I promise. I'm just really glad you told me."
                "[girlfriend_name] let out a long breath and leaned her forehead against my shoulder."
                gf "Me too. I was so scared you'd be weird about it."

            "[d2_confession_brush_text]":
                $ apply_choice("ch01_d2_confession_brush")
                $ set_story_value("ch01_d2_confession_reply", "brushed")
                mc "Weird guy. Glad you're okay."
                "[girlfriend_name] waited, like there might be more. There wasn't."
                gf "...Yeah. Me too."
                "She took one of the muffins out of the bag and picked at it without eating any."
                think "She'd just told me the hardest thing she'd said all day, and I'd answered like she'd told me they were out of whipped cream."

    $ set_story_flag("ch01_d2_julian_upstairs_before_sunset")
    $ set_story_flag("ch01_d2_scene_19_complete")
    jump ch01_day2_scene_20_dinner_outfit
