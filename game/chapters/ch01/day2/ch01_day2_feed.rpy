# Day Two feed posts (systems/feed.rpy, docs/FEED.md).
# Registered at init 1, after the feed registry exists (init 0). The story releases each post
# where it should appear; this PR adds only Maya's intro post (scene 09, the photo walk).
# The group photo has no art yet (the four-person selfie is still pending, see
# systems/phone_group_avatar.rpy), so the post is text-only; give it image="cg ..." once it lands.
# No `when`: the post is stamped with the story clock scene 09 sets (14:10).

init 1 python:
    lc_feed_register(
        "d2_maya_group_photo", "ch01_d2", "Maya", "maya.in.frame",
        "Three attempts because somebody blinked twice. Island crew, all eyes open. Somebody frame this.",
        comments=[("[friend_name]", "The sun was very aggressive. I stand by it.")],
        likes=23)
