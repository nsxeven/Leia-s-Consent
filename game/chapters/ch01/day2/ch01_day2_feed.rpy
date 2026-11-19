# Day Two feed posts (systems/feed.rpy, docs/FEED.md).
# Registered at init 1, after the feed registry exists (init 0). The story releases each post
# where it should appear: Maya's intro post (scene 09, the photo walk) and Leia's errand posts
# (after dinner, scene 24).
# The post carries the new Trip Group selfie (cg ch01_d2_photo_group, GroupSelfie_01).
# No `when`: the post is stamped with the story clock scene 09 sets (14:10).

init 1 python:
    lc_feed_register(
        "d2_maya_group_photo", "ch01_d2", "Maya", "maya.in.frame",
        "Officially in the trip group 🌴 Island crew. Somebody frame this.",
        comments=[("[friend_name]", "Sunglasses stayed on. Nobody can prove I blinked.")],
        image="cg ch01_d2_photo_group", likes=23)


# Leia's errand posts (Leia's side PR 3, script B19, canon call K6 for the names). Scene 24
# releases all six side by side after dinner; each gate holds on one errand lane only, and her café
# pick chooses the variant (leia_did / leia_did_not), so a save gets its lane's posts and nothing
# else. A save that never played the errand (no ch01_d2_errand_lane) gets none. Stamps follow her
# visit order (ch01_d2_errand_stamp). Reading never moves stats; scene 30 reads lc_feed_seen /
# lc_feed_any_seen for one bring-up option. The clip photo is a placeholder (cg d2_feed_cafe_clip,
# ch01_day2_visuals.rpy), 18+ masked like the Gallery.
init 1 python:
    def ch01_d2_errand_stamp(place):
        """Post time for an errand stop: 16:20 for her first stop, 16:45 for her second."""
        return "16:20" if lc_leia_visited_first("ch01_d2", place) else "16:45"

    # Love lane: the pool guy and Margaret.
    lc_feed_register(
        "d2_feed_love_poolguy", "ch01_d2", "Dan", "dan.on.tour",
        "stopped a creep at the resort café. then got shot down by the same girl 💀 her bf is a lucky man",
        comments=[("mikey_k", "\"the same girl\" 😭 brutal"),
                  ("dan.on.tour", "she was really nice about it tbf"),
                  ("sarah.jpg", "good for her. and you. mostly her")],
        likes=48, when=lambda: ch01_d2_errand_stamp("cafe"),
        unlock={"ch01_d2_errand_lane": "love"},
        reaction="ch01_d2_feed_react_love_poolguy")

    lc_feed_register(
        "d2_feed_love_shop", "ch01_d2", "Margaret @ Island Mart", "islandmart_marg",
        "A young lady bought the last chocolate muffins for her sweetheart today. I remember being this in love. 💛",
        comments=[("harold_b", "You still are, Marg."),
                  ("islandmart_marg", "Oh, hush.")],
        likes=12, when=lambda: ch01_d2_errand_stamp("shop"),
        unlock={"ch01_d2_errand_lane": "love"},
        reaction="ch01_d2_feed_react_love_shop")

    # Exhibitionism lane: one post, caption by her café pick (three comments max per post).
    lc_feed_register(
        "d2_feed_exhib_poolguy", "ch01_d2", "Dan", "dan.on.tour",
        "stopped a creep at the café and it was the girl from the pool next door. she's TAKEN, boys 😭",
        comments=[("mikey_k", "THE pool girl?? the bikini top girl??"),
                  ("dan.on.tour", "we don't talk about the pool"),
                  ("mikey_k", "and her bf was at the pool too. he is living my life")],
        likes=96, when=lambda: ch01_d2_errand_stamp("cafe"),
        unlock={"ch01_d2_errand_lane": "exhibitionism", "leia_did_not": "ch01_d2_cafe_exhib_lingered"},
        reaction="ch01_d2_feed_react_exhib")

    lc_feed_register(
        "d2_feed_exhib_poolguy_linger", "ch01_d2", "Dan", "dan.on.tour",
        "stopped a creep at the café, then spent 10 min talking to the girl from the pool next door. she's TAKEN, boys 😭",
        comments=[("mikey_k", "THE pool girl?? the bikini top girl??"),
                  ("dan.on.tour", "we don't talk about the pool"),
                  ("mikey_k", "and her bf was at the pool too. he is living my life")],
        likes=96, when=lambda: ch01_d2_errand_stamp("cafe"),
        unlock={"ch01_d2_errand_lane": "exhibitionism", "leia_did": "ch01_d2_cafe_exhib_lingered"},
        reaction="ch01_d2_feed_react_exhib")

    # NTR-risk lane: Kayla's clip (the last comment follows her café pick).
    lc_feed_register(
        "d2_feed_ntr_clip", "ch01_d2", "Kayla", "kaylax.travels",
        "guy just smacked a girl's ass at the resort café and she... didn't slap him?? 😳",
        image="cg d2_feed_cafe_clip", mature=True,
        comments=[("benny.r", "she's smiling in this??"),
                  ("lou.mf", "ok that guy is a creep though"),
                  ("kaylax.travels", "she told him off after, to be fair. took her a sec though")],
        likes=213, when=lambda: ch01_d2_errand_stamp("cafe"),
        unlock={"ch01_d2_errand_lane": "ntr_risk", "leia_did_not": "ch01_d2_cafe_ntr_lingered"},
        reaction="ch01_d2_feed_react_ntr")

    lc_feed_register(
        "d2_feed_ntr_clip_linger", "ch01_d2", "Kayla", "kaylax.travels",
        "guy just smacked a girl's ass at the resort café and she... didn't slap him?? 😳",
        image="cg d2_feed_cafe_clip", mature=True,
        comments=[("benny.r", "she's smiling in this??"),
                  ("lou.mf", "ok that guy is a creep though"),
                  ("kaylax.travels", "she let him keep talking for ages after too 👀")],
        likes=213, when=lambda: ch01_d2_errand_stamp("cafe"),
        unlock={"ch01_d2_errand_lane": "ntr_risk", "leia_did": "ch01_d2_cafe_ntr_lingered"},
        reaction="ch01_d2_feed_react_ntr")


# Ryan's one-time reactions (docs/FEED.md): each plays once, after he closes the phone, the first
# time he sees the post. One think line, so it fits wherever he reads it (walk home, game night, bed).
label ch01_d2_feed_react_love_poolguy:
    think "I worked out the time, and my stomach went cold. She'd hugged me for ages when she got back. I'd thought she was just in a good mood."
    return

label ch01_d2_feed_react_love_shop:
    think "I'd eaten mine by the pool in about four bites without asking her a single thing about it. I wanted to go find her and say thank you again, properly this time."
    return

label ch01_d2_feed_react_exhib:
    think "I read it twice. So that was why her cheeks were pink when she got back. I kept waiting to feel jealous, and mostly I just wanted her to tell me the whole thing herself."
    return

label ch01_d2_feed_react_ntr:
    if get_story_value("ch01_d2_leia_told") == "told":
        think "She'd already told me all of it herself, on the lounger, before I'd even asked. I still had to put the phone face down for a minute."
    else:
        think "I looked at the photo for a long time. Then I zoomed in, to be sure it was her."
        think "That same afternoon she'd sat on the end of my lounger and watched me drink my frappuccino, and she hadn't said one word."
    return
