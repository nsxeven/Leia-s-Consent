# Central choice-effect system.
# Story files provide the visible choice text and a stable choice ID.
# Effects live here so gameplay, Insight mode, Full Transparency mode, and developer tools all read the same data.

init python:

    CHOICE_MODES = ("normal", "insight", "full", "developer")

    CHOICE_MODE_LABELS = {
        "normal": "Normal",
        "insight": "Insight",
        "full": "Full Transparency",
        "developer": "Developer",
    }

    STAT_LABELS = {
        "love": "Love",
        "trust": "Trust",
        "boredom": "Boredom",
        "momentum": "Momentum",
        "curiosity": "Curiosity",
        "temptation": "Temptation",
        "exhibitionism": "Exhibitionism",
        "boundary_looseness": "Boundary Looseness",
        "secrecy": "Secrecy",
        "jealousy": "Jealousy",
        "acceptance": "Acceptance",
    }

    # Static definitions. Add future story choices here with stable IDs.
    CHOICE_EFFECTS = {
        "dev_encourage_curiosity": [
            ("partner", "curiosity", 5),
            ("player", "acceptance", 3),
            ("relationship", "momentum", 1),
        ],
        "dev_be_protective": [
            ("relationship", "trust", 3),
            ("player", "jealousy", 3),
            ("partner", "boundary_looseness", -2),
        ],
        "ch01_outfit_bolder": [
            ("partner", "curiosity", 3),
            ("player", "acceptance", 3),
            ("relationship", "trust", 1),
        ],
        "ch01_outfit_comfort": [
            ("relationship", "trust", 2),
            ("relationship", "love", 1),
        ],
        "ch01_outfit_conservative": [
            ("player", "jealousy", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_photo_support": [
            ("partner", "curiosity", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_photo_more": [
            ("partner", "curiosity", 2),
            ("partner", "exhibitionism", 3),
            ("player", "acceptance", 2),
            ("relationship", "momentum", 1),
        ],
        "ch01_photo_exit": [
            ("relationship", "trust", 2),
        ],
        "ch01_towel_laugh": [
            ("relationship", "love", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_towel_boundary": [
            ("relationship", "trust", 1),
            ("player", "jealousy", 1),
        ],
        "ch01_towel_forget": [
            ("relationship", "trust", 1),
            ("player", "jealousy", 2),
        ],
        "ch01_towel_reassure": [
            ("relationship", "trust", 1),
        ],
        "ch01_towel_honest": [
            ("relationship", "trust", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_towel_tease": [
            ("relationship", "love", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_bra_reassure": [
            ("relationship", "trust", 2),
        ],
        "ch01_bra_playful": [
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 2),
            ("relationship", "momentum", 1),
        ],
        "ch01_bra_cover": [
            ("relationship", "trust", 1),
            ("player", "jealousy", 1),
            ("partner", "boundary_looseness", -1),
        ],
        "ch01_stranger_proud": [
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_stranger_territorial": [
            ("player", "jealousy", 2),
            ("partner", "boundary_looseness", -1),
        ],
        "ch01_stranger_encourage": [
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 2),
            ("relationship", "momentum", 1),
        ],
        "ch01_catch_ignore": [
            ("player", "acceptance", 1),
        ],
        "ch01_catch_check": [
            ("relationship", "trust", 1),
        ],
        "ch01_catch_joke": [
            ("relationship", "love", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_catch_boundary": [
            ("player", "jealousy", 1),
        ],
        "ch01_friend_reassure": [
            ("relationship", "trust", 2),
            ("relationship", "love", 1),
        ],
        "ch01_friend_tease": [
            ("relationship", "love", 1),
        ],
        "ch01_friend_boundary": [
            ("relationship", "trust", 1),
            ("player", "jealousy", -1),
        ],
        "ch01_julian_reassure": [
            ("player", "acceptance", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_julian_honest": [
            ("player", "jealousy", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_julian_joke": [
            ("player", "acceptance", 1),
        ],
        "ch01_carry_brush": [
            ("player", "acceptance", 2),
        ],
        "ch01_carry_lookaway": [
            ("player", "jealousy", 2),
        ],
        "ch01_carry_fix": [
            ("relationship", "trust", 1),
        ],
        "ch01_carry_joke": [
            ("player", "acceptance", 2),
            ("relationship", "momentum", 1),
        ],

        # Movie-night / Day 1 continuation. Open choices can grow NTS while
        # still reinforcing love; dismissive choices intentionally create the
        # boredom / low-love pressure that can later feed the NTR route.
        "ch01_movie_stop": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_movie_subtle": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 2),
            ("relationship", "momentum", 1),
        ],
        "ch01_movie_tease_presence": [
            ("relationship", "love", 1),
            ("partner", "curiosity", 1),
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 1),
            ("relationship", "momentum", 1),
        ],
        "ch01_movie_dismiss_concern": [
            ("relationship", "love", -1),
            ("relationship", "trust", -1),
            ("relationship", "boredom", 2),
            ("player", "acceptance", 1),
        ],
        "ch01_can_tell_behave": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_can_tell_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_can_tell_push": [
            ("partner", "curiosity", 2),
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 2),
            ("relationship", "momentum", 1),
        ],
        "ch01_can_tell_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 2),
            ("partner", "boundary_looseness", 1),
        ],
        "ch01_fidget_cover": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_fidget_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_fidget_push": [
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
            ("relationship", "momentum", 1),
        ],
        "ch01_fidget_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
        ],
        "ch01_private_apologize": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_private_playful": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_private_curiosity": [
            ("relationship", "love", 1),
            ("partner", "curiosity", 2),
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 1),
            ("relationship", "momentum", 1),
        ],
        "ch01_private_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "trust", -1),
            ("relationship", "boredom", 2),
        ],
        "ch01_noblanket_behave": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_noblanket_test": [
            ("partner", "curiosity", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_noblanket_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
            ("relationship", "momentum", 1),
        ],
        "ch01_noblanket_phone": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 2),
        ],
        "ch01_watch_claim": [
            ("relationship", "love", 2),
            ("relationship", "boredom", -1),
            ("player", "jealousy", 1),
        ],
        "ch01_watch_tease": [
            ("relationship", "love", 1),
            ("partner", "curiosity", 1),
            ("partner", "exhibitionism", 1),
        ],
        "ch01_watch_check": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_watch_ignore": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
        ],
        "ch01_micro_warn": [
            ("relationship", "trust", 1),
            ("partner", "boundary_looseness", -1),
        ],
        "ch01_micro_silent": [
            ("partner", "curiosity", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_micro_open": [
            ("partner", "curiosity", 1),
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 1),
            ("relationship", "momentum", 1),
        ],
        "ch01_micro_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
        ],
        "ch01_philosophy_couple": [
            ("relationship", "trust", 1),
            ("relationship", "boredom", -1),
            ("player", "jealousy", 1),
        ],
        "ch01_philosophy_trust": [
            ("relationship", "trust", 2),
            ("player", "acceptance", 1),
        ],
        "ch01_philosophy_jealousy_fun": [
            ("relationship", "love", 1),
            ("partner", "curiosity", 1),
            ("player", "acceptance", 1),
            ("relationship", "momentum", 1),
        ],
        "ch01_philosophy_dont_care": [
            ("relationship", "love", -1),
            ("relationship", "trust", -1),
            ("relationship", "boredom", 2),
            ("partner", "boundary_looseness", 1),
        ],
        "ch01_looking_enjoy": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_looking_harmless": [
            ("relationship", "trust", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_looking_boundary": [
            ("relationship", "trust", 1),
            ("player", "jealousy", 1),
        ],
        "ch01_looking_dont_care": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 2),
        ],
        "ch01_julian_change_subject": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_julian_let_play": [
            ("player", "acceptance", 1),
        ],
        "ch01_julian_put_spot": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_julian_dont_care": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 2),
            ("partner", "temptation", 1),
        ],
        "ch01_compliment_affirm": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
            ("relationship", "boredom", -1),
        ],
        "ch01_compliment_tease": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "jealousy", 1),
        ],
        "ch01_compliment_enjoy": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 2),
            ("relationship", "momentum", 1),
        ],
        "ch01_compliment_shrug": [
            ("relationship", "love", -2),
            ("relationship", "boredom", 2),
            ("partner", "temptation", 1),
        ],
        "ch01_alone_apologize": [
            ("relationship", "love", 1),
            ("relationship", "trust", 2),
        ],
        "ch01_alone_curiosity": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
            ("partner", "curiosity", 1),
        ],
        "ch01_alone_open": [
            ("relationship", "love", 1),
            ("partner", "exhibitionism", 2),
            ("player", "acceptance", 1),
            ("relationship", "momentum", 1),
        ],
        "ch01_alone_dismiss": [
            ("relationship", "love", -1),
            ("relationship", "trust", -1),
            ("relationship", "boredom", 2),
        ],
        "ch01_private_claim": [
            ("relationship", "love", 2),
            ("relationship", "trust", 1),
            ("relationship", "boredom", -1),
            ("player", "jealousy", 1),
        ],
        "ch01_private_open": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_private_jealous": [
            ("relationship", "love", 1),
            ("player", "jealousy", 2),
            ("partner", "boundary_looseness", -1),
        ],
        "ch01_private_indifferent": [
            ("relationship", "love", -2),
            ("relationship", "boredom", 2),
            ("partner", "temptation", 1),
        ],
        "ch01_d2_mall_go_to_leia": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_leave_to_maya": [
            ("relationship", "love", -1),
            ("relationship", "boredom", 1),
            ("partner", "temptation", 1),
        ],
        "ch01_d2_mall_reveal_affection": [
            ("relationship", "love", 1),
            ("relationship", "trust", 1),
        ],
        "ch01_d2_mall_reveal_open": [
            ("partner", "curiosity", 1),
            ("partner", "exhibitionism", 1),
            ("player", "acceptance", 1),
        ],
        "ch01_d2_mall_reveal_tease": [
            ("relationship", "love", 1),
        ],
    }

    # Behavioral metadata is deliberately separate from stat effects. Later scenes
    # can react to patterns such as encouragement/protectiveness/nonchalance without
    # checking a long list of specific choice IDs.
    CHOICE_TAGS = {
        "dev_encourage_curiosity": ("encouraging", "participating", "open"),
        "dev_be_protective": ("protective", "cautious"),
        "ch01_outfit_bolder": ("encouraging", "open", "supportive"),
        "ch01_outfit_comfort": ("neutral", "comfort-first", "supportive"),
        "ch01_outfit_conservative": ("protective", "cautious", "respectful"),
        "ch01_photo_support": ("encouraging", "supportive"),
        "ch01_photo_more": ("encouraging", "participating", "open"),
        "ch01_photo_exit": ("protective", "comfort-first", "supportive"),
        "ch01_towel_laugh": ("encouraging", "lighthearted"),
        "ch01_towel_boundary": ("protective", "respectful"),
        "ch01_towel_forget": ("protective", "honest", "cautious"),
        "ch01_towel_reassure": ("neutral", "supportive", "reassuring"),
        "ch01_towel_honest": ("neutral", "honest", "supportive"),
        "ch01_towel_tease": ("encouraging", "lighthearted", "open"),
        "ch01_bra_reassure": ("neutral", "supportive", "comfort-first"),
        "ch01_bra_playful": ("encouraging", "participating", "open", "playful"),
        "ch01_bra_cover": ("protective", "cautious", "respectful"),
        "ch01_stranger_proud": ("encouraging", "supportive", "open", "attentive"),
        "ch01_stranger_territorial": ("protective", "possessive", "cautious", "attentive"),
        "ch01_stranger_encourage": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_catch_ignore": ("neutral", "trusting"),
        "ch01_catch_check": ("neutral", "supportive", "protective", "attentive"),
        "ch01_catch_joke": ("encouraging", "lighthearted", "open"),
        "ch01_catch_boundary": ("protective", "cautious", "respectful"),
        "ch01_friend_reassure": ("neutral", "honest", "supportive", "attentive"),
        "ch01_friend_tease": ("encouraging", "lighthearted", "playful"),
        "ch01_friend_boundary": ("neutral", "honest", "boundary-setting"),
        "ch01_julian_reassure": ("encouraging", "trusting", "open"),
        "ch01_julian_honest": ("protective", "honest", "respectful"),
        "ch01_julian_joke": ("encouraging", "lighthearted", "trusting"),
        "ch01_carry_brush": ("encouraging", "trusting", "open"),
        "ch01_carry_lookaway": ("protective", "possessive", "cautious"),
        "ch01_carry_fix": ("neutral", "protective", "supportive"),
        "ch01_carry_joke": ("encouraging", "lighthearted", "open", "playful"),

        "ch01_movie_stop": ("protective", "attentive", "supportive", "consent-first"),
        "ch01_movie_subtle": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_movie_tease_presence": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_movie_dismiss_concern": ("neutral", "nonchalant", "dismissive"),
        "ch01_can_tell_behave": ("protective", "attentive", "supportive"),
        "ch01_can_tell_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_can_tell_push": ("encouraging", "participating", "open", "risk-testing"),
        "ch01_can_tell_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_fidget_cover": ("neutral", "supportive", "attentive"),
        "ch01_fidget_tease": ("encouraging", "playful", "open"),
        "ch01_fidget_push": ("encouraging", "open", "risk-testing"),
        "ch01_fidget_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_private_apologize": ("neutral", "supportive", "attentive", "consent-first"),
        "ch01_private_playful": ("encouraging", "open", "playful", "attentive"),
        "ch01_private_curiosity": ("encouraging", "participating", "open", "honest", "attentive"),
        "ch01_private_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_noblanket_behave": ("neutral", "attentive", "supportive"),
        "ch01_noblanket_test": ("encouraging", "open", "risk-testing"),
        "ch01_noblanket_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_noblanket_phone": ("neutral", "nonchalant", "distracted"),
        "ch01_watch_claim": ("protective", "possessive", "attentive", "playful"),
        "ch01_watch_tease": ("encouraging", "open", "playful", "attentive"),
        "ch01_watch_check": ("neutral", "supportive", "attentive"),
        "ch01_watch_ignore": ("neutral", "nonchalant", "distracted"),
        "ch01_micro_warn": ("protective", "attentive", "respectful"),
        "ch01_micro_silent": ("neutral", "trusting", "observant"),
        "ch01_micro_open": ("encouraging", "participating", "open", "risk-testing"),
        "ch01_micro_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_philosophy_couple": ("protective", "possessive", "boundary-setting"),
        "ch01_philosophy_trust": ("neutral", "honest", "trusting", "open"),
        "ch01_philosophy_jealousy_fun": ("encouraging", "open", "playful", "possessive"),
        "ch01_philosophy_dont_care": ("neutral", "nonchalant", "dismissive"),
        "ch01_looking_enjoy": ("encouraging", "open", "playful", "attentive"),
        "ch01_looking_harmless": ("neutral", "trusting", "open"),
        "ch01_looking_boundary": ("protective", "boundary-setting", "attentive"),
        "ch01_looking_dont_care": ("neutral", "nonchalant", "dismissive"),
        "ch01_julian_change_subject": ("protective", "attentive", "boundary-setting"),
        "ch01_julian_let_play": ("neutral", "trusting", "open"),
        "ch01_julian_put_spot": ("encouraging", "open", "playful", "participating"),
        "ch01_julian_dont_care": ("neutral", "nonchalant", "dismissive"),
        "ch01_compliment_affirm": ("neutral", "supportive", "attentive", "possessive"),
        "ch01_compliment_tease": ("encouraging", "playful", "possessive", "attentive"),
        "ch01_compliment_enjoy": ("encouraging", "participating", "open", "attentive"),
        "ch01_compliment_shrug": ("neutral", "nonchalant", "dismissive", "distracted"),
        "ch01_alone_apologize": ("neutral", "supportive", "attentive", "consent-first"),
        "ch01_alone_curiosity": ("neutral", "honest", "attentive", "open"),
        "ch01_alone_open": ("encouraging", "participating", "open", "playful", "attentive"),
        "ch01_alone_dismiss": ("neutral", "nonchalant", "dismissive"),
        "ch01_private_claim": ("protective", "possessive", "attentive", "supportive"),
        "ch01_private_open": ("encouraging", "open", "honest", "attentive"),
        "ch01_private_jealous": ("protective", "possessive", "honest"),
        "ch01_private_indifferent": ("neutral", "nonchalant", "dismissive"),
        "ch01_d2_mall_go_to_leia": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_leave_to_maya": ("neutral", "nonchalant", "dismissive", "withdrawal", "ntr-seed"),
        "ch01_d2_mall_reveal_affection": ("supportive", "attentive", "love-route"),
        "ch01_d2_mall_reveal_open": ("encouraging", "participating", "open", "exhibitionism-seed"),
        "ch01_d2_mall_reveal_tease": ("encouraging", "playful", "attentive"),
    }

    STANCE_TAGS = ("encouraging", "neutral", "protective")


    def current_choice_mode():
        """Return a valid global choice-display mode."""
        mode = getattr(renpy.store.persistent, "choice_display_mode", "normal")
        if mode not in CHOICE_MODES:
            return "normal"
        return mode


    def choice_mode_label():
        return CHOICE_MODE_LABELS[current_choice_mode()]


    def set_choice_display_mode(mode):
        """Set the global display preference used by all future choices."""
        if mode not in CHOICE_MODES:
            raise ValueError("Unknown choice display mode: {}".format(mode))

        renpy.store.persistent.choice_display_mode = mode
        renpy.save_persistent()
        renpy.restart_interaction()


    def get_choice_effects(choice_id):
        """Return a copy of the effects for a stable choice ID."""
        if choice_id not in CHOICE_EFFECTS:
            raise ValueError("Unknown choice ID: {}".format(choice_id))
        return list(CHOICE_EFFECTS[choice_id])


    def get_choice_tags(choice_id):
        """Return immutable behavioral tags for a stable choice ID."""
        return tuple(CHOICE_TAGS.get(choice_id, ()))


    def apply_choice(choice_id):
        """Apply the real effects, record the selection, and surface mode-safe feedback."""
        review_before = lc_review_stats()
        for group_name, stat_name, amount in get_choice_effects(choice_id):
            change_stat(group_name, stat_name, amount)

        renpy.store.last_choice_id = choice_id
        renpy.store.choice_history.append(choice_id)
        lc_review_note_choice(choice_id, review_before)
        show_choice_feedback(choice_id)
        return choice_id


    def choice_ids_with_prefix(prefix, choice_ids=None):
        """Return recorded choices whose stable IDs begin with a chapter/event prefix."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        return [choice_id for choice_id in source if choice_id.startswith(prefix)]


    def choice_tag_count(tag, choice_ids=None):
        """Count how often a behavioral tag appears in the selected choice history."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        return sum(1 for choice_id in source if tag in get_choice_tags(choice_id))


    def choice_tag_counts(choice_ids=None):
        """Return counts for every behavioral tag represented in the selected history."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        counts = {}
        for choice_id in source:
            for tag in get_choice_tags(choice_id):
                counts[tag] = counts.get(tag, 0) + 1
        return counts


    def choice_stance(choice_ids=None):
        """Summarize encouraging/neutral/protective behavior without creating hard routes."""
        source = renpy.store.choice_history if choice_ids is None else choice_ids
        counts = {tag: choice_tag_count(tag, source) for tag in STANCE_TAGS}
        highest = max(counts.values()) if counts else 0

        if highest <= 0:
            return "neutral"

        leaders = [tag for tag, count in counts.items() if count == highest]
        if len(leaders) != 1:
            return "mixed"
        return leaders[0]


    def chapter_choice_ids(chapter_id):
        """Convention: real chapter choice IDs begin with e.g. 'ch01_'."""
        prefix = chapter_id if chapter_id.endswith("_") else chapter_id + "_"
        return choice_ids_with_prefix(prefix)


    def chapter_stance(chapter_id):
        return choice_stance(chapter_choice_ids(chapter_id))


    def chapter_nonchalant_count(chapter_id):
        """Count dismissive/nonchalant choices for route-pressure checks."""
        return choice_tag_count("nonchalant", chapter_choice_ids(chapter_id))


    def _choice_effect_text(choice_id, exact=False):
        parts = []

        for group_name, stat_name, amount in get_choice_effects(choice_id):
            label = STAT_LABELS.get(stat_name, stat_name.replace("_", " ").title())

            if exact:
                parts.append("{} {:+d}".format(label, amount))
            else:
                arrow = "↑" if amount > 0 else "↓" if amount < 0 else "→"
                parts.append("{} {}".format(label, arrow))

        return " • ".join(parts)


    def format_choice(choice_id, base_text):
        """Return the player-facing text for a choice under the active display mode."""
        mode = current_choice_mode()

        if mode == "normal":
            return base_text

        if mode == "insight":
            return "{}\n[{}]".format(base_text, _choice_effect_text(choice_id, exact=False))

        if mode == "full":
            return "{}\n[{}]".format(base_text, _choice_effect_text(choice_id, exact=True))

        tags = get_choice_tags(choice_id)
        tag_text = " • Tags: {}".format(", ".join(tags)) if tags else ""
        return "{}\n[{}]  [ID: {}]{}".format(
            base_text,
            _choice_effect_text(choice_id, exact=True),
            choice_id,
            tag_text,
        )


    def choice_preview_text():
        """Safe live preview used by the choice-mode screen."""
        base_text = "Encourage {}'s curiosity".format(renpy.store.girlfriend_name)
        return format_choice("dev_encourage_curiosity", base_text)

