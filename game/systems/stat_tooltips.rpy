# Hover / focus explanations for every stat row (Status screen, phone Status
# app, end-of-day review bars).
#
# Owner decision (darryn): no numbers yet. The stats do not translate into
# fixed thresholds while the story is still being built, so these texts only
# say what a stat represents and, in broad strokes, what tends to happen as
# its bar fills. Keep digits, thresholds and exact effects OUT of
# LC_STAT_TOOLTIPS (tests/test_stat_tooltips.py enforces this).
#
# Wording per display mode (internal keys from CHOICE_MODES):
#   "normal"  = Immersive: vague, in-world, feeling-based, no spoilers.
#   "insight" = Insight: direction of travel (what raises / lowers it, what a
#               high bar leans toward).
#   "full"    = Full Transparency: what the stat tracks and what a full bar
#               means for the story. Developer mode reuses this text.
#
# Names: write [girlfriend_name], [player_name], [friend_name], never the
# default names. lc_stat_tooltip() swaps them for the player's typed names.

init python:

    LC_STAT_TOOLTIP_MODES = ("normal", "insight", "full")

    # Modes without their own text borrow another mode's wording.
    LC_STAT_TOOLTIP_MODE_FALLBACK = {"developer": "full"}

    # stat id -> mode -> text. Stat ids match _status_row(group, stat_id, ...)
    # in status_display.rpy, LC_REVIEW_STAT_ORDER in day_review.rpy and the
    # route rows ("nts_score", "ntr_score").
    LC_STAT_TOOLTIPS = {
        "love": {
            "normal": "How warm things feel between you two: the easy smiles, the little touches, the way [girlfriend_name] lights up when you walk in.",
            "insight": "How loved [girlfriend_name] feels. Being present, kind and on her side tends to raise it; brushing her off or putting her second lowers it. A high bar leans toward a closer, more playful couple.",
            "full": "Tracks how emotionally close [girlfriend_name] feels to [player_name]. A full bar means the relationship is the anchor, so new adventures stay something you share. It feeds the shared (NTS) tendency, and letting it slip feeds the NTR tendency.",
        },
        "trust": {
            "normal": "Whether [girlfriend_name] feels safe being honest with you, even about the things that make her blush.",
            "insight": "How safe [girlfriend_name] feels being open with you. Keeping your word, checking in and respecting a no raise it; waving off her worries lowers it. High trust makes bolder conversations feel safe.",
            "full": "Tracks how sure [girlfriend_name] is that she can tell [player_name] anything and be heard. A full bar means new ideas get talked through openly, together, before anything happens. It supports the shared (NTS) tendency; as it drains, the NTR tendency gains ground.",
        },
        "boredom": {
            "normal": "A sense of whether things feel fresh lately, or whether [girlfriend_name] seems a little restless and in need of something new.",
            "insight": "How restless [girlfriend_name] feels in the relationship. Dismissing her, tuning out or playing it safe for too long tends to raise it; real attention and shared fun bring it down. A high bar leans toward her looking for excitement elsewhere.",
            "full": "Tracks how overlooked and under-stimulated [girlfriend_name] feels with [player_name]. A full bar means she is ready to chase excitement on her own, without you. It is one of the strongest drivers of the NTR tendency, so keeping it low keeps the story centered on the two of you.",
        },
        "momentum": {
            "normal": "That feeling that this trip is carrying you both somewhere new, a little faster than you expected.",
            "insight": "How far and how fast things have been moving. Playful, bolder choices nudge it forward; holding back lets it settle. A high bar means the next step feels closer than it did.",
            "full": "Tracks overall escalation: how far the two of you have already stepped beyond your old routine. A full bar means bolder story beats arrive sooner and feel more natural. It adds to both route tendencies, so it measures speed, not direction.",
        },
        "curiosity": {
            "normal": "The spark in [girlfriend_name]'s eyes when something new, or a little daring, comes up.",
            "insight": "How open [girlfriend_name] is to new ideas and experiences. Encouraging her questions and teasing gently tend to raise it; shutting ideas down cools it. A high bar leans toward her suggesting things herself.",
            "full": "Tracks [girlfriend_name]'s appetite for exploring new experiences. A full bar means she starts asking for new things herself instead of just going along. It is a core part of the shared (NTS) tendency.",
        },
        "temptation": {
            "normal": "Every so often her attention seems to drift somewhere you can't quite follow.",
            "insight": "How strongly outside attention pulls at [girlfriend_name]. Restlessness and moments without you nearby tend to raise it; feeling close and included keeps it in check. A high bar leans toward choices she makes on her own.",
            "full": "Tracks how strongly attention from other people pulls at [girlfriend_name] when [player_name] isn't part of it. A full bar means she is more likely to act on that pull, with or without you. It feeds the NTR tendency.",
        },
        "exhibitionism": {
            "normal": "How at ease [girlfriend_name] seems when eyes turn her way: shy, amused, or quietly enjoying it.",
            "insight": "How comfortable [girlfriend_name] is being noticed and admired. Playful moments with you there, cheering her on, tend to raise it; making her feel exposed or judged lowers it. A high bar leans toward bolder outfits and moments in public.",
            "full": "Tracks how much [girlfriend_name] enjoys being seen and admired by others. A full bar means she is genuinely comfortable being the center of attention, which opens the door to bolder outfits and public moments. It feeds the shared (NTS) tendency, especially when you are part of it.",
        },
        "boundary_looseness": {
            "normal": "Whether [girlfriend_name] seems happy where her comfort zone sits, or curious about stretching it a little.",
            "insight": "How far [girlfriend_name]'s comfort zone has stretched. Feeling left to her own devices tends to loosen it; protective, possessive moments pull it back in. A high bar means ideas that once felt too far may be up for discussion.",
            "full": "Tracks how far [girlfriend_name]'s limits have moved from where the trip started. A full bar means she will consider things she would once have refused outright. It is about where her lines sit, not who she is with, and it adds weight to the NTR tendency.",
        },
        "secrecy": {
            "normal": "Little things she might be keeping to herself. Hard to tell from where you're standing.",
            "insight": "How much [girlfriend_name] keeps to herself. Moments she handles alone, or doesn't feel she can share, tend to raise it; honest talks and coming clean bring it down. A high bar leans toward a story you only hear part of.",
            "full": "Tracks how much of what happens [girlfriend_name] is keeping from [player_name]. A full bar means important moments happen out of your sight and stay there. It is one of the clearest signs of the NTR tendency.",
        },
        "jealousy": {
            "normal": "That tight little feeling in your chest when someone else gets her smile.",
            "insight": "How possessive [player_name] feels. Watching her get attention you weren't part of tends to raise it; laughing it off or joining in eases it. A high bar leans toward reining her in rather than letting her explore.",
            "full": "Tracks [player_name]'s possessive streak. A full bar means you are more likely to step in and pull [girlfriend_name] back, which keeps her limits closer to home but can cost warmth if it turns controlling.",
        },
        "acceptance": {
            "normal": "How easy it feels for you to let her shine, even when other eyes are on her.",
            "insight": "How comfortable [player_name] is with [girlfriend_name] being admired and exploring. Joking along, encouraging her and staying relaxed raise it. A high bar leans toward shared adventures you are both in on.",
            "full": "Tracks how genuinely okay [player_name] is with [girlfriend_name] being noticed, admired and trying new things. A full bar means you can be part of her adventures instead of the obstacle. It is a core part of the shared (NTS) tendency.",
        },
        "nts_score": {
            "normal": "Where this trip seems to be taking the two of you, together. Only time will tell.",
            "insight": "How much the story is leaning toward adventures you share. Closeness, trust, her curiosity and your openness all push it up.",
            "full": "A combined read of how strongly the story leans toward shared, consensual adventures that [player_name] and [girlfriend_name] explore together. Affection, Trust, Curiosity, Exhibitionism, Acceptance and Momentum feed it. A full bar means upcoming branches lean toward the shared route.",
        },
        "ntr_score": {
            "normal": "Whether you two still feel like you're heading the same way. Hard to say.",
            "insight": "How much the story is leaning toward [girlfriend_name] drifting away from you. Restlessness, temptation and secrets push it up; closeness and trust pull it down.",
            "full": "A combined read of how strongly the story leans toward [girlfriend_name] following outside attention without [player_name]. Boredom, Temptation, Secrecy, Boundary Flexibility and Momentum feed it, and so do low Affection and Trust. A full bar means upcoming branches lean toward the NTR route.",
        },
    }

    # FUTURE NUMBERS GO HERE (keep LC_STAT_TOOLTIPS number-free).
    # Once darryn decides what the values mean, add exact thresholds / effects
    # per stat and mode, e.g.
    #     "boredom": {"full": "...", "developer": "..."},
    # lc_stat_tooltip() appends the sentence after the base text. Mostly for
    # "full" / "developer"; Immersive should stay number-free. Update
    # tests/test_stat_tooltips.py (it asserts this is empty) when you do.
    LC_STAT_TOOLTIP_NUMBERS = {}

    LC_STAT_TOOLTIP_NAME_TOKENS = (
        ("[girlfriend_name]", "girlfriend_name"),
        ("[player_name]", "player_name"),
        ("[friend_name]", "friend_name"),
    )


    def lc_stat_tooltip(stat_id, mode=None):
        """Player-facing explanation for one stat row, or None if unknown.

        The result already holds the player's typed names, so display it with
        `substitute False`.
        """
        mode = mode or current_choice_mode()
        entry = LC_STAT_TOOLTIPS.get(stat_id)
        if not entry:
            return None
        text_mode = LC_STAT_TOOLTIP_MODE_FALLBACK.get(mode, mode)
        text = entry.get(text_mode) or entry["normal"]
        numbers = LC_STAT_TOOLTIP_NUMBERS.get(stat_id, {})
        extra = numbers.get(mode) or numbers.get(text_mode)
        if extra:
            text = text + " " + extra
        # Typed default names (none today) follow the player's names first;
        # then the bracket tokens are filled in, so a renamed character can't
        # be rewritten a second time.
        text = gallery_customize_names(text)
        for token, field in LC_STAT_TOOLTIP_NAME_TOKENS:
            text = text.replace(token, str(getattr(store, field, "")))
        return text
