# Runtime override for Scene 30.
# Extends the existing Day One ending directly into the new Day Two build.
# Uses the same callback-redirect pattern as the existing Scene 13 revision so
# the original label remains intact and Ren'Py does not see a duplicate label.

init 999 python:
    _ch01_scene30_previous_label_callback = config.label_callback

    def _ch01_scene30_label_callback(name, abnormal):
        if _ch01_scene30_previous_label_callback is not None:
            _ch01_scene30_previous_label_callback(name, abnormal)

        if name == "ch01_scene_30_end_day_one":
            renpy.jump("ch01_scene_30_end_day_one_day2_bridge")

    config.label_callback = _ch01_scene30_label_callback


label ch01_scene_30_end_day_one_day2_bridge:

    scene bg ch01_villa_bedroom_night
    show leia at ch01_leia_left
    $ set_leia_sprite("p01", "neutral")
    with fade

    "We switched off the downstairs lights and finally headed upstairs."
    "Leia plugged her phone in beside the bed and climbed under the covers."

    "Before either of us could settle, my phone lit up one last time."

    python:
        phone_add_message(
            "group",
            "julian",
            text="Breakfast after 11 or I'm calling the police.",
            message_id="ch01_trip_group_breakfast_warning",
            mark_unread=True,
            notify=True,
            notification_title="Trip Group",
        )
        set_story_flag("ch01_breakfast_reply_pending")
        clear_story_flag("ch01_breakfast_phone_session_active")

    "Leia checked the same message on her phone and laughed quietly."

    gf "He's dramatic."
    mc "He's correct."
    gf "Eleven-thirty."
    mc "Eleven-fifteen."
    gf "Eleven-thirty."
    mc "Fine."

    $ set_story_value("ch01_day1_nonchalant_count", chapter_nonchalant_count("ch01"))

    if chapter_nonchalant_count("ch01") >= 3 and (relationship_stats["boredom"] >= 15 or relationship_stats["love"] <= 48):
        $ set_story_value("ch01_day1_route_pressure", "ntr_seeded")
        "Leia put her phone down, but the small distance between us felt more noticeable than it had that morning."
        "Julian had not done anything wrong. If anything changed from here, it would begin with the spaces I kept leaving open."
    elif nts_score() >= ntr_score() + 5 and partner_stats["curiosity"] >= 24:
        $ set_story_value("ch01_day1_route_pressure", "nts_seeded")
        "Somewhere during the day, a private joke between Leia and me had started acquiring a third point of reference."
        "Nothing had happened. The fact that nothing had happened was part of what made the possibility feel new."
    else:
        $ set_story_value("ch01_day1_route_pressure", "mixed")
        "Yesterday, Julian had simply been my friend."
        "By the end of the day, he'd started becoming Leia's friend too, and none of us had decided yet what that would mean."

    $ set_story_flag("ch01_scene_30_complete")
    $ set_story_flag("ch01_day_01_complete")
    $ set_story_flag("ch01_scenes_14_30_complete")

    scene black
    with fade

    centered "{size=46}CHAPTER ONE — DAY ONE COMPLETE{/size}"

    jump ch01_day2_start
