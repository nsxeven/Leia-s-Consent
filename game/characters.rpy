# Character definitions.
# Display names are player-customizable; internal character IDs stay fixed.

define mc = Character("player_name", dynamic=True)
# Ryan's direct inner voice (present-tense words in his head): italic, no name
# tag. Plain past-tense narration stays on the narrator (darryn 2026-11-08).
#     think "What the hell was that?"
define think = Character(None, show_think=True)
# Leia's inner voice during her own segment (systems/leia_side.rpy, docs/LEIA_SIDE.md): the
# same italic, no-name look as Ryan's think; the tinted text box says whose head it is.
#     leia_think "He'd never ask for this. That's why I'm doing it."
define leia_think = Character(None, show_think=True)
define gf = Character("girlfriend_name", dynamic=True)
define friend = Character("friend_name", dynamic=True)

# Chapter 1 supporting roles.
define stranger = Character("Stranger")
# The later corridor/table compliment man is a separate person from the dinner
# collision stranger. Keep his speaker (and any future sprite) registered apart.
define passerby = Character("Stranger")
# Day 3 cutout-stand stranger: a separate person from the Day 2 dinner collision
# stranger (and from the passerby). Same on-screen name, separate speaker object.
define stranger_d3 = Character("Stranger")
# Day 2 boutique: the man by the racks who compliments Maya (and the Hidden POV there).
# A separate person again; no sprite, so he is not in LC_CAST_SPEAKERS.
define boutique_stranger = Character("Stranger")
define maya = Character("Maya")
# Day One used the temporary phone_friend role before Maya was introduced in person.
define phone_friend = maya
