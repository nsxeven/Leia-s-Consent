# Leia's side demo - developer/QA only (game/dev/ is left out of release builds).
#
# A click-through of the errand system with no story content: the "Meanwhile" card, the tinted
# text box and leia_think, then the map with two open places (cafe, resort shop) and two locked
# ones (bar, boutique). Visit both open places in either order; each has one Leia-side choice.
# Picking the warm option at both shows the +2/day cap: the second one reads "Love (capped) +0"
# in Insight/Full. Reach it from the developer systems menu ("Leia's side demo") or
# `call lc_dev_leia_side`. Its ids start with dev_leia and are not story values any Day reads.
# The label refuses to run unless config.developer is on. Docs: docs/LEIA_SIDE.md.

define lc_dev_leia_barista = Character("Barista")
define lc_dev_leia_cashier = Character("Cashier")
default lc_dev_leia_place = None

init 1 python:
    lc_leia_place("dev_leia", "cafe", "Café", "bg ch01_d2_cafe",
                  "Something cold and sweet for him.", mood="his drink", done="Frappuccino: got it.")
    lc_leia_place("dev_leia", "shop", "Resort shop", "bg ch01_shop_night",
                  "His favorite snack, if they have any left.", mood="his snack", done="Muffins: got them.")
    lc_leia_place("dev_leia", "bar", "Resort bar", "bg ch01_restaurant_bar",
                  "Cocktails and loud music.",
                  locked_reason="A bar, on my own, at four in the afternoon? Not on day two. Maybe if Maya comes next time.")
    lc_leia_place("dev_leia", "boutique", "Boutique", "bg ch01_d2_boutique",
                  "Dresses, swimsuits, Maya's favorite rack.",
                  locked_reason="I've had enough of that boutique for one day, thank you.")
    CHOICE_EFFECTS.update({
        "dev_leia_cafe_warm": [("relationship", "love", 1), ("relationship", "trust", 1)],
        "dev_leia_cafe_plain": [],
        "dev_leia_shop_warm": [("relationship", "love", 1)],
        "dev_leia_shop_plain": [],
    })
    CHOICE_TAGS.update({
        "dev_leia_cafe_warm": ("supportive", "love-route"),
        "dev_leia_cafe_plain": ("neutral",),
        "dev_leia_shop_warm": ("supportive", "love-route"),
        "dev_leia_shop_plain": ("neutral",),
    })
    lc_leia_register_choices("dev_leia", "dev_leia_cafe_warm", "dev_leia_cafe_plain",
                             "dev_leia_shop_warm", "dev_leia_shop_plain")

label lc_dev_leia_side:
    if not config.developer:
        return
    # Sandbox only: forget the demo's own visits, cap ledger and outcomes so it can be replayed;
    # every story day's Leia-side record in this save is kept.
    $ lc_leia_side_state = lc_leia_side.reset_day(lc_leia_side_state, "dev_leia", outcome_prefix="dev_leia_")
    call lc_leia_segment_begin("dev_leia") from lc_dev_leia_side_begin
    scene bg ch01_villa_entry_day
    with dissolve
    "I left [player_name] dozing on the lounger with his sunglasses on crooked, and slipped out the front door before I could talk myself out of it."
    leia_think "He'd never ask for any of this. That's exactly why I'm going."
    while not lc_leia_errand_done("dev_leia"):
        $ lc_dev_leia_place = lc_leia_map("dev_leia")
        if lc_dev_leia_place:
            $ lc_leia_visit("dev_leia", lc_dev_leia_place)
            call expression "lc_dev_leia_" + lc_dev_leia_place from lc_dev_leia_side_stop
    $ lc_dev_leia_order = " then ".join(lc_leia_visits("dev_leia"))
    if lc_leia_visited_first("dev_leia", "shop"):
        leia_think "Muffins first, so the ice survives the walk home. See? I can plan."
    "Both bags in one hand, I headed back. (Visited: [lc_dev_leia_order].)"
    call lc_leia_segment_end from lc_dev_leia_side_end
    scene bg dev
    with fade
    $ lc_dev_leia_told = lc_leia_did("dev_leia_told_barista")
    "Back to [player_name]. Told the barista: [lc_dev_leia_told]. Moments strip ids marked: leia_dev_leia_cafe / leia_dev_leia_shop."
    return

label lc_dev_leia_cafe:
    scene bg ch01_d2_cafe
    with dissolve
    "The café was cold enough to raise goosebumps after the walk. I got in line behind a couple arguing about oat milk."
    lc_dev_leia_barista "What can I get you?"
    $ lc_dev_leia_warm_text = format_choice("dev_leia_cafe_warm", "Tell him it's for {} and why".format(player_name))
    $ lc_dev_leia_plain_text = format_choice("dev_leia_cafe_plain", "Just order the drink")
    menu:
        "[lc_dev_leia_warm_text]":
            $ apply_choice("dev_leia_cafe_warm")
            $ lc_leia_mark("dev_leia_told_barista")
            gf "A large caramel frappuccino, extra whipped cream. It's for my boyfriend, he's had a rough couple of days and he doesn't know I'm doing this."
            lc_dev_leia_barista "Then I'm putting extra caramel on it. Don't tell my manager."
        "[lc_dev_leia_plain_text]":
            $ apply_choice("dev_leia_cafe_plain")
            gf "A large caramel frappuccino, please."
    leia_think "He's going to pretend he doesn't care and then drink the whole thing in two minutes."
    return

label lc_dev_leia_shop:
    scene bg ch01_shop_night
    with dissolve
    "The resort shop had one box of chocolate muffins left, squashed behind the sunscreen. I took it like it was the last lifeboat."
    lc_dev_leia_cashier "Treating yourself?"
    $ lc_dev_leia_warm_text = format_choice("dev_leia_shop_warm", "Tell her what you're planning for {}".format(player_name))
    $ lc_dev_leia_plain_text = format_choice("dev_leia_shop_plain", "Keep it to yourself")
    menu:
        "[lc_dev_leia_warm_text]":
            $ apply_choice("dev_leia_shop_warm")
            gf "They're for my boyfriend. He's asleep by the pool, and I want him to wake up to his favorite things for once."
            lc_dev_leia_cashier "Oh, I remember being this in love."
        "[lc_dev_leia_plain_text]":
            $ apply_choice("dev_leia_shop_plain")
            gf "Something like that."
    return
