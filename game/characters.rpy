# Character definitions.
# Display names are player-customizable; internal character IDs stay fixed.

define mc = Character("player_name", dynamic=True)
define gf = Character("girlfriend_name", dynamic=True)
define friend = Character("friend_name", dynamic=True)

# Chapter 1 supporting roles.
define stranger = Character("Stranger")
define maya = Character("Maya")
# Day One used the temporary phone_friend role before Maya was introduced in person.
define phone_friend = maya
