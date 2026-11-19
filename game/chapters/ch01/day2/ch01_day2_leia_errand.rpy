# Chapter One, Day Two: Leia's errand (Leia's side, PR 3), between scenes 19b and 19c.
# Flow: ch01_day2_scene_19b_leia_asks_maya -> ch01_day2_scene_19b2_ryan_dozes (Ryan's bridge)
#       -> ch01_day2_leia_errand (her segment: map, café, resort shop, walk back)
#       -> ch01_day2_scene_19c_back_outside (she wakes him; the told-path confession)
#
# Approved lines: darryn 2026-11-18 (reports/nm-c-script/script.md B01-B14) with the design's
# canon calls K1-K6 (LC-Brain Plans/2026-11-17 Leia's side design.md). System API: docs/LEIA_SIDE.md.
# - Lane: read once from the post-pool record (the value scene 20 reads), stored as
#   ch01_d2_errand_lane. Reason (K1): "dream" only if he told her the dream after the mall.
# - Her choices share the +2/day cap (lc_leia_register_choices); Day Two's paths never reach it.
#   Every id here, Ryan's confession reply and the scene 30 bring-up are left out of tonight's lane
#   and end route (CH01_D2_ERRAND_EXEMPT_CHOICES, ch01_day2_registrations.rpy). Her choice rows and map places
#   are registered there too..
# - Art: bg ch01_shop_day (K2) and cg d2_cafe_stranger are placeholders until darryn renders them
#   (ch01_day2_visuals.rpy). The walks use ch01_d2_island_day (day art; ch01_roadside is night).
# - Old saves already past 19b never see any of this (19c keeps its original line).



# B01: Ryan dozes off on the lounger (his narration), right after 19b.
label ch01_day2_scene_19b2_ryan_dozes:

    scene bg ch01_pool_lounge
    with dissolve

    "[girlfriend_name] was still inside seeing Maya off, and [friend_name] had claimed the one umbrella that actually made shade."
    "I lay down on the lounger next to him and told myself it was only to dry off."

    friend "You're going to fall asleep. I can see it happening. Your whole face is doing the thing."
    mc "I'm not falling asleep. I'm resting my eyes. That's different."
    friend "That's what my grandad says, and then he snores through the entire news, every night, and wakes up and tells us what happened in it."

    if "ch01_d2_postshop_dream" in choice_history:
        "I'd finally told her about the dream at the mall. I'd expected to feel stupid afterwards. Mostly I just felt tired, the good kind."
    elif get_story_value("ch01_dream_response") == "withdrew":
        "I hadn't slept much the night before, and I'd spent all day making a point of not thinking about why."
    else:
        "Last night's dream had mostly worn off. The sun was doing a pretty good job on the rest of it."

    "The water slapped against the edge of the pool. [friend_name] was saying something about the reservation, and whether eight meant eight or eight-ish here."
    "I don't remember him finishing the sentence."

    scene black
    with fade

    jump ch01_day2_leia_errand


# B02: her segment opens. Lane read once here (continuity note C5); reason per canon call K1.
label ch01_day2_leia_errand:

    call lc_leia_segment_begin("ch01_d2") from d2_errand_begin
    $ d2_errand_lane = get_story_value("ch01_d2_route_lane_post_pool", ch01_d2_route_lane())
    $ set_story_value("ch01_d2_errand_lane", d2_errand_lane)
    $ d2_errand_reason = "dream" if "ch01_d2_postshop_dream" in choice_history else "off"
    $ set_story_value("ch01_d2_errand_reason", d2_errand_reason)
    # Flow: Ryan's mood so far, by the café test (any dismissive/withdrawal pick today). Stored before
    # her own picks can add tags; her thoughts here, the shop, 19c and the sunset read it.
    $ d2_errand_ryan_mood = "detached" if (choice_tag_count("dismissive", ch01_d2_choice_ids()) + choice_tag_count("withdrawal", ch01_d2_choice_ids())) > 0 else "warm"
    $ set_story_value("ch01_d2_errand_ryan_mood", d2_errand_ryan_mood)

    scene bg ch01_villa_entry_day
    with dissolve

    "Maya waved once from the end of the path, and then she was gone, and the villa went quiet behind me."
    "I stayed in the doorway a bit longer than I needed to. From there I could see straight through the house to the pool."
    "[player_name] was flat out on a lounger with one arm over his face. [friend_name] was under the umbrella next to him, scrolling his phone with the sound off, like he was guarding a sleeping baby."

    if d2_errand_reason == "dream":
        leia_think "He told me about that dream at the mall. The drink guy, and him not being able to move, and just having to watch the whole thing."
        leia_think "It's a ridiculous dream. I still spent the whole walk back wondering how long he'd been carrying it around before he said anything."
        leia_think "So he doesn't get a bad dream and a sad afternoon. Pick one. Actually, no, he doesn't get either."
    else:
        if d2_errand_ryan_mood == "warm":
            leia_think "He's been really sweet today. He's also been yawning all afternoon, and half the night he kept doing this thing with his pillow, like he was fighting it."
            leia_think "He says he's just tired. Which, okay, probably. I still want to do something about it."
            if get_story_value("ch01_d2_overheard_talk") == "mild":
                leia_think "I told Maya I wanted to do something nice for him tonight. Okay. This is the something."
        else:
            leia_think "He's been quiet all day. Like, he answers when I talk to him, and he laughs in the right places, but it's like he's always a few seconds behind everyone."
            if "ch01_d2_postshop_sleep" in choice_history:
                leia_think "He says he didn't sleep well. That's probably true. I just don't think it's the whole thing."
        if get_story_value("ch01_d2_pool_response") == "accused":
            leia_think "And whatever that was at the pool. I'm still kind of... I don't know. Maybe I need an hour where I'm not waiting for him to say something, too."
        if d2_errand_ryan_mood == "warm":
            leia_think "I can't make him sleep. I can get him a caramel frappuccino, though. That part I can actually do."
        else:
            leia_think "I can't fix whatever's going on in his head. I can get him a caramel frappuccino, though. That part I can actually do."

    $ face("leia", "smile")
    leia_think "Caramel frappuccino, extra caramel, from the café we had lunch at, because they do it properly. And chocolate muffins from the resort shop, if they've got any left. That's the plan. That's the entire plan."

    "I ran upstairs, pulled my shorts and top back on over my bikini and grabbed my purse, then came back down on tiptoe for no reason at all, since he was outside and asleep."
    "[friend_name] looked up when I slid the door open."

    gf "Hey. I'm popping out for a bit. If he wakes up, I went for a walk."
    friend "Where are you actually going?"
    gf "The café, and the shop. It's a surprise, so you didn't see me. You've got no idea where I went."
    friend "I didn't see anything. I'm not even here, I'm just a guy under an umbrella. I've been under this umbrella since we got back."
    friend "Should I be doing something, though? Like keeping him asleep? I don't really know how you'd do that. I'd probably just sit here and try not to drop anything."
    gf "Yes! Perfect. Just sit there and try really, really hard not to drop anything."
    "He gave me a thumbs-up so serious that I had to leave before I laughed and woke [player_name] up."

    jump ch01_day2_errand_map


# B03: the map. She visits both open places; the player picks the order.
label ch01_day2_errand_map:

    if lc_leia_visits("ch01_d2"):
        $ cast()
        scene bg ch01_d2_island_day
        with dissolve
    if not lc_leia_visits("ch01_d2"):
        "At the bottom of the villa path there was a big painted resort map on a wooden board, with little cartoon palm trees all over it."
        leia_think "Café, shop. Two stops, back before he wakes up. Easy."
    elif lc_leia_visited_first("ch01_d2", "shop"):
        leia_think "Muffins, done. Frappuccino last, so the ice survives the walk home. See? I can plan."
    elif d2_errand_lane == "ntr_risk":
        leia_think "Just get the muffins. Get the muffins and go home."
    else:
        leia_think "Frappuccino first was maybe a mistake. It's already sweating. Shop, quick, then home."

    $ d2_errand_next = lc_leia_map("ch01_d2")
    if d2_errand_next:
        $ lc_leia_visit("ch01_d2", d2_errand_next)
        if d2_errand_next == "cafe":
            call ch01_day2_errand_cafe from d2_errand_call_cafe
        else:
            call ch01_day2_errand_shop from d2_errand_call_shop

    if not lc_leia_errand_done("ch01_d2"):
        jump ch01_day2_errand_map
    jump ch01_day2_errand_walk_back


# B04: the café, shared by every lane (CG d2_cafe_stranger, before the lanes split).
label ch01_day2_errand_cafe:

    scene bg ch01_d2_island_day
    with dissolve
    "The walk took ten minutes, past the same row of shops we'd wandered through after lunch. It felt different on my own. Quieter. Nobody was arguing about sunglasses."

    scene bg ch01_d2_cafe
    with dissolve
    $ cast(leia="casual")

    "The café from lunch was half empty. A couple were sharing a little fan at the corner table, and the girl behind the counter was wiping down the coffee machine."
    barista "Hi! You were here earlier, right? With the big group?"
    $ face("leia", "shy")
    gf "You remember us? That's a bit embarrassing. Yes, hi. Can I get a caramel frappuccino, a large one, with extra caramel? Like, on top and in it, if that's a thing you can do."
    barista "That's a thing. Give me a few minutes."

    $ face("leia", "smile")
    leia_think "He'll read the whole menu next time too, and ask what's good, and then order exactly this. Four years, and he's never once ordered anything else."

    $ face("leia", "skeptical")
    "I leaned on the counter to wait, and somebody leaned on it right next to me. A lot closer than he needed to be."

    $ cast()
    $ enter_cinematic_mode()
    scene cg d2_cafe_stranger
    with dissolve

    cafe_stranger "That's a big drink for one person."
    gf "It's not for me."
    cafe_stranger "No? So who's the lucky guy? Because I'm not seeing him anywhere."
    "He smiled like we were already in on something together. He smelled like beer and a lot of aftershave, and he'd put his hand flat on the counter, right next to mine."
    gf "He's at the villa. Not that it's any—"
    cafe_stranger "Then he won't mind if I keep you company while you wait."
    "He shifted closer. The counter was at my back, and there was nowhere to step without making a whole scene out of it."

    $ exit_cinematic_mode()
    scene bg ch01_d2_cafe
    with dissolve
    $ cast(leia="casual")

    if d2_errand_lane == "ntr_risk":
        jump ch01_day2_errand_cafe_ntr
    jump ch01_day2_errand_cafe_rescue


# B05: the pool guy steps in (Love and Exhibitionism lanes).
label ch01_day2_errand_cafe_rescue:

    pool_guy "Hey, you made it! We grabbed a table in the back, come on, we've been waiting ages."
    "The stranger turned around. So did I."
    "It was one of the guys from the pool. The one Maya had told me not to look at. The one who had, about two hours ago, watched my bikini top float across the water."
    leia_think "Oh no. It's pool guy."
    cafe_stranger "Who are you?"
    pool_guy "Her friend. We're over there. You good, man? You're kind of standing on her."
    "For a second nobody moved. Then the stranger laughed, like the whole thing had been a joke from the start, picked up his beer and wandered back out onto the terrace."

    $ face("leia", "smile")
    gf "Thank you. Seriously. I didn't really know what to do there. I was just going to stand still until he got bored."
    pool_guy "No problem. Guys like that fold the second somebody else is watching."
    pool_guy "Sorry for pretending to know you, by the way. I mean, I sort of do. From the pool."

    if d2_errand_lane == "exhibitionism":
        $ face("leia", "skeptical")
        gf "Yep. That's me. You were the one doing all the staring."
        # Flow: he only recaps what happened on this save's pool split (ch01_d2_split).
        if get_story_value("ch01_d2_split") == "ryan_leia_julian_maya":
            pool_guy "In my defense, there was a lot going on to stare at. You, your boyfriend, the whole... kiss situation."
            "He waved a hand at nothing in particular and then immediately looked like he regretted it."
        elif get_story_value("ch01_d2_split") == "ryan_maya_leia_julian":
            pool_guy "In my defense, there was a lot going on to stare at. The stretching, and then the bee, and then your..."
            "He made a vague little gesture at his own chest and then immediately looked like he regretted it."
        else:
            pool_guy "In my defense, there was a lot going on to stare at. You and your friend, the strings thing, and then she..."
            "He made a small slapping motion with one hand and then immediately looked like he regretted it."
        $ face("leia", "flustered")
        gf "Okay, we really don't need the whole recap."
        $ face("leia", "smile")
        "I was laughing, though. I didn't totally mind the recap."
        jump ch01_day2_errand_cafe_exhib
    else:
        $ face("leia", "flustered")
        gf "Yeah. Hi. I was really hoping I'd never see any of you again, no offense. It's not about you. It's about the bee."
        pool_guy "None taken. For what it's worth, I looked away really fast. Mostly. My buddy didn't, he's an animal."
        jump ch01_day2_errand_cafe_love


# B06: café, Love lane.
label ch01_day2_errand_cafe_love:

    "He laughed, and then he leaned on the counter too, a little closer than the gap the stranger had left."
    pool_guy "So can I buy you a drink? A real one. Since I saved you and everything."
    $ face("leia", "skeptical")
    leia_think "Of course. He didn't even wait for the frappuccino to be ready."

    $ d2_errand_cafe_thank_text = format_choice("ch01_d2_errand_cafe_love_thank", "Thank him properly, then tell him about {}.".format(player_name))
    $ d2_errand_cafe_brush_text = format_choice("ch01_d2_errand_cafe_love_brush", "Brush him off politely.")
    menu:
        "[d2_errand_cafe_thank_text]":
            $ apply_choice("ch01_d2_errand_cafe_love_thank")
            $ lc_leia_mark("ch01_d2_cafe_love_thanked")
            $ face("leia", "smile")
            gf "That's really sweet, and thank you, you didn't have to do any of that. But this drink is for my boyfriend. He's asleep by the pool, and I want it to be there when he wakes up."
            # Flow: no kiss at the pool on the drinks-run split (ch01_d2_split).
            if get_story_value("ch01_d2_split") == "ryan_maya_leia_julian":
                pool_guy "The guy from the pool? The one who went off for drinks with your friend?"
                gf "Yes. That one. He's mine."
                pool_guy "Ha. Okay. Lucky guy. Tell him I said hi. Or, actually, maybe don't."
            else:
                pool_guy "The guy from the pool? The one who..."
                $ face("leia", "shy")
                gf "The one who kissed me right in front of you, yes. That one."
                pool_guy "Ha. Yeah, okay, I can't really compete with that. Tell him I said hi. Or, actually, maybe don't."
            $ face("leia", "smile")
            gf "I'm pretty lucky too. He's really nice. You'd like him, he'd probably thank you for this about five times."
            "He held his hands up, laughing, and went back to his friend at the corner table, who said something that made him shove him."
            leia_think "I just said it out loud to a total stranger, and it felt really nice. I should say it to [player_name] like that more. Not the stranger part."

        "[d2_errand_cafe_brush_text]":
            $ apply_choice("ch01_d2_errand_cafe_love_brush")
            $ lc_leia_mark("ch01_d2_cafe_love_brushed")
            $ face("leia", "neutral")
            gf "That's nice of you, but no, thanks. I'm just here for the coffee."
            pool_guy "No, totally. Worth a shot."
            "He went back to his table without making it weird, which was more than the first guy had managed."
            $ face("leia", "skeptical")
            leia_think "Two guys in five minutes. What is it with this café? I literally just wanted a frappuccino."

    barista "Large caramel frappuccino, extra caramel!"
    $ face("leia", "neutral")
    "My hands were still shaking a little when I took it. Not a lot. Enough that I held it with both of them."
    return


# B07: café, Exhibitionism lane.
label ch01_day2_errand_cafe_exhib:

    pool_guy "Can I at least buy you something? I did a whole rescue."
    $ face("leia", "skeptical")
    gf "I'm literally waiting for a drink. You can't buy me a drink while I'm holding a drink."
    pool_guy "Then I'll wait with you. Bodyguard. In case he comes back."
    $ face("leia", "shy")
    "He leaned on the counter, not as close as the first guy. Close enough that I noticed."

    $ face("leia", "smile")
    leia_think "He's cute. He knows he's cute, which makes it less cute. And he's looking at me the way he did at the pool, except now I'm wearing a lot more clothes and it's still somehow the same look."
    leia_think "I could tell him about [player_name] right now. Or I could just let him talk for a bit. It's only talking."

    $ d2_errand_cafe_linger_text = format_choice("ch01_d2_errand_cafe_exhib_linger", "Let him talk a little longer before you mention {}.".format(player_name))
    $ d2_errand_cafe_mention_text = format_choice("ch01_d2_errand_cafe_exhib_mention", "Mention {} now.".format(player_name))
    menu:
        "[d2_errand_cafe_linger_text]":
            $ apply_choice("ch01_d2_errand_cafe_exhib_linger")
            $ lc_leia_mark("ch01_d2_cafe_exhib_lingered")
            "So I let him talk. He was here with three friends from college, he did something with spreadsheets for work, and the pool at their place was smaller than ours, which he seemed really bitter about."
            $ face("leia", "flustered")
            "He kept finding reasons to look at me, and I kept letting him find them."
            pool_guy "So what are you doing tonight? Because there's a beach thing at the bar later, and if you and your friend wanted to..."
            $ face("leia", "smile")
            "Then the barista called my drink. I picked it up and smiled at him like I'd been waiting for exactly this moment all along."
            if get_story_value("ch01_d2_split") == "ryan_maya_leia_julian":
                gf "That sounds really fun. My boyfriend and I have dinner plans, though. This is his, by the way. He was at the pool too. The one you didn't notice."
                pool_guy "Of course he was. Yeah. Course he was."
            else:
                gf "That sounds really fun. My boyfriend and I have dinner plans, though. This is his, by the way. He's the guy from the pool. The one who kissed me."
                pool_guy "Of course he is. Yeah. Course he is."
            gf "Thank you for the rescue, though. I mean that."
            leia_think "His face. That was a little bit mean. It was also a little bit fun. [player_name] would have loved his face."

        "[d2_errand_cafe_mention_text]":
            $ apply_choice("ch01_d2_errand_cafe_exhib_mention")
            $ lc_leia_mark("ch01_d2_cafe_exhib_mentioned")
            if get_story_value("ch01_d2_split") == "ryan_maya_leia_julian":
                gf "Thank you, really, but you don't need to stay. My boyfriend's back at the villa. He was at the pool too, by the table."
                pool_guy "Ah. Right, yeah. I think I remember him."
                gf "You'd remember him if you met him properly."
            else:
                $ face("leia", "shy")
                gf "Thank you, really, but you don't need to stay. My boyfriend's back at the villa. He was the other guy at the pool, the one who, um. The kiss."
                pool_guy "Ah. Right, yeah. I remember him. Pretty memorable."
                $ face("leia", "smile")
                gf "He is pretty memorable."
            "He took it well. He even laughed, and told me to say hi to the bee for him, which made no sense at all, and I laughed anyway."
            barista "Large caramel frappuccino, extra caramel!"

    $ face("leia", "flustered")
    leia_think "My whole face is hot, like, up to my ears, and I'm still smiling. I should probably feel a lot weirder about that than I do."
    return


# B08: café, NTR-risk lane (no rescue). Same ending either way; she never mentions him.
label ch01_day2_errand_cafe_ntr:

    "I looked around the café. The couple in the corner were still busy with their fan. The girl behind the counter had her back to us, fighting the blender."
    "Nobody was coming over."
    $ face("leia", "skeptical")
    gf "I'm fine, thanks. I'm just waiting for my drink."
    cafe_stranger "Sure you are."

    "I turned back to the counter, and he smacked my ass."
    "Not a tap. A proper, loud smack, right through my shorts, loud enough to hear over the blender."
    $ face("leia", "angry")
    gf "Hey!"
    "It came out squeakier than I wanted. I spun around, and he was grinning at me, completely unbothered, like he'd told a joke and was waiting for me to laugh at it."
    cafe_stranger "Sorry. Couldn't help it. You can't lean on a counter like that in those shorts and expect nobody to notice."

    "In my head I was already telling him off. I had all of it, every word, exactly how I'd say it."
    $ face("leia", "flustered")
    "What I did instead was stand there with my face burning and say none of it."
    leia_think "Why aren't you saying anything? Say something. Say anything at all."
    "The worst part was the half a second right after, before I got angry, when something low in my stomach went warm and fluttery and I didn't know what to do with it."
    cafe_stranger "See? You're smiling."
    $ face("leia", "pout")
    gf "I'm not smiling."
    $ face("leia", "shy")
    "I was, a little. I could feel it on my face, and I hated it."
    cafe_stranger "So what's your name? You staying around here? Because I'm in one of the beach bungalows, and they're way nicer than wherever you're..."

    $ d2_errand_cafe_linger_text = format_choice("ch01_d2_errand_cafe_ntr_linger", "Let it linger a moment before you shut it down.")
    $ d2_errand_cafe_shut_text = format_choice("ch01_d2_errand_cafe_ntr_shut", "Shut it down. Right now.")
    menu:
        "[d2_errand_cafe_linger_text]":
            $ apply_choice("ch01_d2_errand_cafe_ntr_linger")
            $ lc_leia_mark("ch01_d2_cafe_ntr_lingered")
            $ face("leia", "flustered")
            "I didn't say no straight away. I let him finish that sentence, and the one after it, about the bungalow and the hot tub and the view of the water."
            "He was standing very close again. I didn't step away. I didn't step closer either. I just stood there and let him talk, and felt my face getting hotter."
            leia_think "What are you doing? You're here to buy his frappuccino. You're standing here waiting for his frappuccino."
            "Then the blender stopped, the café went very quiet, and whatever that was broke."
            $ face("leia", "skeptical")
            gf "No. I'm good. Thanks."
            cafe_stranger "You sure? You don't look sure."
            gf "I'm sure."
            "He shrugged and went back out to the terrace, like he had all the time in the world."

        "[d2_errand_cafe_shut_text]":
            $ apply_choice("ch01_d2_errand_cafe_ntr_shut")
            $ lc_leia_mark("ch01_d2_cafe_ntr_shut")
            $ face("leia", "angry")
            gf "No. Don't. I'm not interested, and you can't just do that to people."
            "My voice shook, but it came out, which was something."
            cafe_stranger "Wow. Relax, it was a joke."
            gf "It wasn't funny."
            "He rolled his eyes, said something about uptight tourists and went back out to the terrace."

    $ face("leia", "pout")
    "I didn't tell him who the drink was for. I didn't say anything else at all."
    barista "Large caramel frappuccino, extra caramel! Have a good one!"
    "The couple in the corner had a phone out now, held up sideways. I didn't think anything of it."
    "I took the drink in both hands and got out of there."
    return


# B09: the resort shop, shared opening. bg ch01_shop_day: darryn's daytime shop (K2), placeholder.
label ch01_day2_errand_shop:

    scene bg ch01_d2_island_day
    with dissolve
    if lc_leia_visited_first("ch01_d2", "shop"):
        "The resort shop was at the other end of the same row, past the ice cream place and a stand selling hats nobody needed."
    else:
        "The resort shop was a couple of minutes further along, past the ice cream place. I walked faster than I needed to."

    scene bg ch01_shop_day
    with dissolve
    $ cast(leia="casual")

    "Inside, it was one long room of snacks, sunscreen and inflatable things, with a fridge humming along the back wall."
    "There was exactly one box of chocolate muffins left, on the bottom shelf, behind a whole tower of banana bread."
    # Flow: straight after the café on the NTR-risk lane (the smack), the shop opens subdued.
    if d2_errand_lane == "ntr_risk" and not lc_leia_visited_first("ch01_d2", "shop"):
        "I pulled it out from behind the banana bread and didn't let myself think about anything else."
        "The woman at the till had reading glasses on a chain, a name badge that said MARGARET, and a radio playing something old and quiet."
        shop_owner "Last box. You must really want those."
        gf "They're for my boyfriend. They're his favorite."
    else:
        $ face("leia", "smile")
        leia_think "Yes. Mine. Sorry, banana bread."
        "The woman at the till had reading glasses on a chain, a name badge that said MARGARET, and a radio playing something old and quiet. She watched me carry the box over like I'd won it at a fair."
        shop_owner "Last box. You must really want those."
        gf "They're not for me. I mean, I'm going to steal one. But they're for my boyfriend. They're his favorite."

    if lc_leia_visited_first("ch01_d2", "shop"):
        jump ch01_day2_errand_shop_first
    elif d2_errand_lane == "love":
        jump ch01_day2_errand_shop_after_love
    elif d2_errand_lane == "exhibitionism":
        jump ch01_day2_errand_shop_after_exhib
    jump ch01_day2_errand_shop_after_ntr


# B10: shop first (any lane). NTR-risk lane: no menu (canon call K3), the walk back stays her
# second scored pick.
label ch01_day2_errand_shop_first:

    shop_owner "And what's he done to earn the last box?"
    if d2_errand_reason == "dream":
        $ face("leia", "neutral")
        gf "Nothing, really. He had a bad dream last night and he finally told me about it today, and I keep thinking about how long he sat on it first. He's asleep by the pool now, and I want him to wake up to his favorite things."
    elif get_story_value("ch01_d2_errand_ryan_mood") == "warm":
        $ face("leia", "smile")
        gf "Nothing, really. He barely slept last night, and he's been lovely all day anyway. He's asleep by the pool now, and I want him to wake up to his favorite things."
    else:
        $ face("leia", "neutral")
        gf "Nothing, really. That's kind of the point. He's been a bit quiet today, and he's asleep by the pool, and I want him to wake up to his favorite things."
    $ face("leia", "smile")
    gf "A caramel frappuccino and these. That's it, that's all it takes. He's very easy to please. It's one of the best things about him."
    shop_owner "How long have you two been together?"
    gf "Four years."
    shop_owner "Four years, and you're still running out for his muffins while he naps."
    "She rang them up slowly, smiling at the box like it reminded her of something."
    $ face("leia", "shy")
    shop_owner "I remember being this in love. Forty-one years with my Harold, and I'd still have done this for him. I still do, some days, when he's being nice."

    if d2_errand_lane == "ntr_risk":
        $ face("leia", "smile")
        gf "I'm also trying to get him on his own before dinner. Our friend has to go upstairs to get ready eventually, and the second he does, I'm stealing him."
        shop_owner "Good. Steal him. They never know they need stealing until it's done."
        return

    $ d2_errand_shop_tell_text = format_choice("ch01_d2_errand_shop_tell", "Tell her what you're planning for him.")
    $ d2_errand_shop_keep_text = format_choice("ch01_d2_errand_shop_keep", "Keep it to yourself.")
    menu:
        "[d2_errand_shop_tell_text]":
            $ apply_choice("ch01_d2_errand_shop_tell")
            $ lc_leia_mark("ch01_d2_shop_told_owner")
            $ face("leia", "smile")
            gf "And I'm going to get him on his own before dinner. Our friend has to go upstairs to get ready eventually, and the second he does, I'm stealing him. My friend Maya says everybody leaves eventually, you just have to wait."
            shop_owner "Your friend's right. Steal him. They never know they need stealing until it's done."
            "She tucked two paper napkins into the bag, and a little plastic knife, in case I wanted to cut one in half and share it, she said."
            $ face("leia", "flustered")
            leia_think "Great. Now Margaret knows my whole plan, so now I actually have to go through with it."

        "[d2_errand_shop_keep_text]":
            $ apply_choice("ch01_d2_errand_shop_keep")
            $ lc_leia_mark("ch01_d2_shop_kept_plan")
            $ face("leia", "smile")
            gf "Oh, I'm just going to be nice to him. That's the plan."
            shop_owner "Well. Enjoy being nice to him."
            "She didn't push. She just tucked a couple of napkins into the bag."
            $ face("leia", "shy")
            leia_think "Some of it I want to keep just for us. It's not a secret plan if I tell the muffin lady."
    return


# B11: shop after the café, Love lane. Same tell/keep menu and ids as B10.
label ch01_day2_errand_shop_after_love:

    $ face("leia", "shy")
    "I put the frappuccino down on the counter to get my purse out, and my hand still wasn't totally steady."
    shop_owner "You alright, sweetheart? You look a bit shaken."
    $ face("leia", "pout")
    gf "Some guy at the café was being gross. It's fine. Someone stepped in."
    "It came out wobblier than I meant it to."
    shop_owner "Then tell me about this boyfriend instead. Go on. What's he like?"
    $ face("leia", "smile")
    gf "He's really nice. That sounds boring, I know. He's quiet, and he reads the whole menu every time and then orders the same thing, and he counts out loud when I'm getting ready, which is so annoying, and he notices everything. Like, the stuff I don't even know I'm doing."
    "By the time I ran out of things to say, my hands had stopped shaking."
    shop_owner "I remember being this in love."
    shop_owner "Forty-one years with my Harold. He still counts, too. Out loud, in the hallway."

    $ d2_errand_shop_tell_text = format_choice("ch01_d2_errand_shop_tell", "Tell her what you're planning for him.")
    $ d2_errand_shop_keep_text = format_choice("ch01_d2_errand_shop_keep", "Keep it to yourself.")
    menu:
        "[d2_errand_shop_tell_text]":
            $ apply_choice("ch01_d2_errand_shop_tell")
            $ lc_leia_mark("ch01_d2_shop_told_owner")
            gf "I'm going to get him on his own before dinner. Our friend has to go upstairs to get ready eventually, and the second he does, I'm stealing him."
            shop_owner "Good. Steal him. They never know they need stealing until it's done."
            "She tucked two napkins into the bag, and a little plastic knife, in case we wanted to share one."
            leia_think "I can barely even picture the café guy's face anymore. Harold counting in the hallway, though. I'm keeping that one."

        "[d2_errand_shop_keep_text]":
            $ apply_choice("ch01_d2_errand_shop_keep")
            $ lc_leia_mark("ch01_d2_shop_kept_plan")
            gf "Just being nice to him. That's the whole plan."
            shop_owner "Well. Enjoy being nice to him."
            $ face("leia", "shy")
            leia_think "Some of it's just for us. Even the muffin lady doesn't get all of it."
    return


# B12: shop after the café, Exhibitionism lane (her reflection in the drinks fridge door).
label ch01_day2_errand_shop_after_exhib:

    "I was still buzzing from the café. My face was warm, and I'd caught myself smiling twice on the walk over for no reason."
    shop_owner "And what's he done to earn the last box?"
    gf "Nothing. He's just mine."
    "She laughed at that, and started ringing them up."
    "While she did, I caught my reflection in the glass door of the drinks fridge."
    $ face("leia", "flustered")
    "My top had slid further off my shoulder than it was supposed to. My hair was a mess from the walk, and my cheeks were still pink."
    $ face("leia", "smile")
    leia_think "Huh. I look kind of good, actually. Like somebody who just got hit on twice in one café. Which, to be fair, I did."
    $ face("leia", "flustered")
    leia_think "Pool guy definitely saw this shoulder. He saw a lot more than this shoulder two hours ago, so what's a shoulder."

    $ d2_errand_mirror_leave_text = format_choice("ch01_d2_errand_shop_mirror_leave", "Leave your top as it is.")
    $ d2_errand_mirror_fix_text = format_choice("ch01_d2_errand_shop_mirror_fix", "Fix it.")
    menu:
        "[d2_errand_mirror_leave_text]":
            $ apply_choice("ch01_d2_errand_shop_mirror_leave")
            $ lc_leia_mark("ch01_d2_shop_top_left")
            $ face("leia", "smile")
            "I left it. I picked up the muffins and the frappuccino and walked out with my shoulder bare, and the guy stacking water bottles by the door looked, and I let him."
            leia_think "[player_name] is going to notice the second he opens his eyes. Good."

        "[d2_errand_mirror_fix_text]":
            $ apply_choice("ch01_d2_errand_shop_mirror_fix")
            $ lc_leia_mark("ch01_d2_shop_top_fixed")
            $ face("leia", "shy")
            "I tugged the top back up where it belonged and pushed my hair into something a bit more decent."
            leia_think "Calm down. You bought muffins. You're not in a music video."
    return


# B13: shop after the café, NTR-risk lane. No stat choice (keeps her side at +2).
label ch01_day2_errand_shop_after_ntr:

    $ face("leia", "flustered")
    "My face was still hot. I could feel exactly where his hand had been, which was stupid. It had been one second."
    shop_owner "You alright, love? You're all red."
    $ face("leia", "shy")
    gf "Just the heat."
    "She looked at me over her glasses a moment longer than I liked. Then she rang them up and didn't ask anything else."
    $ face("leia", "pout")
    leia_think "Just the heat. Sure. It's the heat."
    return


# B14: walk back. NTR-risk lane: tell (Sharing +1, NTS) or keep (Temptation +1, NTR, K4).
label ch01_day2_errand_walk_back:

    scene bg ch01_d2_island_day
    with dissolve
    $ cast(leia="casual")

    "Frappuccino in one hand, muffins in the other, and maybe ten minutes before the ice gave up."

    if d2_errand_lane == "love":
        leia_think "He's going to be so smug that I remembered the extra caramel. Fine. He can be smug."
        leia_think "I'll tell him about the café guy later. Or not. I don't want his frappuccino story to be about some creep. It's supposed to be about him."
    elif d2_errand_lane == "exhibitionism":
        leia_think "I'm telling him about pool guy. Obviously. I just want to see his face when I do."
        if lc_leia_did("ch01_d2_cafe_exhib_lingered"):
            leia_think "Maybe I'll leave out how long I let him talk. Or maybe that's the bit I put in first. I can't tell yet which one would be more fun."
    else:
        "The walk back was the same ten minutes as the walk there. It felt a lot longer."
        leia_think "Okay. I'm okay. It was one stupid second, and it's over."
        leia_think "Some guy I'll never see again did something gross, and I stood there like an idiot, and that's the whole story. That's all it was."
        if lc_leia_did("ch01_d2_cafe_ntr_lingered"):
            leia_think "Except I didn't just stand there. I let him keep talking. Part of me wanted to hear what he'd say next."
        else:
            leia_think "Except for that one second, right before I got angry. The part where I didn't hate it."
        leia_think "[player_name] is going to wake up and smile at his frappuccino, and I'm going to hand it to him with the same hand that... no. Don't finish that sentence."
        leia_think "Do I tell him?"

        $ d2_errand_walk_tell_text = format_choice("ch01_d2_errand_walk_tell", "\"I'm telling him. Tonight.\"")
        $ d2_errand_walk_keep_text = format_choice("ch01_d2_errand_walk_keep", "\"It was nothing. He doesn't need to know.\"")
        menu:
            "[d2_errand_walk_tell_text]":
                $ apply_choice("ch01_d2_errand_walk_tell")
                $ set_story_value("ch01_d2_leia_told", "told")
                leia_think "I'm telling him. Tonight, before I lose my nerve. Before dinner, even, if [friend_name] ever goes upstairs."
                if get_story_value("ch01_d2_errand_ryan_mood") == "warm":
                    leia_think "He's been so sweet all day, and he still feels half somewhere else. Maybe if I give him something real, he'll give me something real back."
                else:
                    leia_think "He's been so far away all day. Maybe if I give him something real, he'll give me something real back."

            "[d2_errand_walk_keep_text]":
                $ apply_choice("ch01_d2_errand_walk_keep")
                $ set_story_value("ch01_d2_leia_told", "kept")
                if get_story_value("ch01_d2_errand_ryan_mood") == "warm":
                    leia_think "It was nothing. A stranger, a stupid joke, one second. He barely slept last night. He doesn't need this in his head too."
                else:
                    leia_think "It was nothing. A stranger, a stupid joke, one second. He's already stuck in his own head about something. He doesn't need this in there too."
                leia_think "And if a tiny part of me wants to keep it, just for me, nobody has to know about that part either."

    scene bg ch01_villa_entry_day
    with dissolve
    "The villa door was still unlocked, exactly how I'd left it. I could hear [friend_name] laughing at something on his phone out by the pool."
    leia_think "Okay. Big smile. Cold drink. Go."

    $ cast()
    call lc_leia_segment_end from d2_errand_end
    jump ch01_day2_scene_19c_back_outside
