# Character definitions.
# Display names are player-customizable; internal character IDs stay fixed.

define mc = Character("player_name", dynamic=True)
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
define maya = Character("Maya")
# Day One used the temporary phone_friend role before Maya was introduced in person.
define phone_friend = maya
