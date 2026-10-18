# Chapter Select screen: pick a day and a route preset, then start a new game there.
# Shown from the main menu only when chapter_select_unlocked() (see systems/chapter_select.rpy).

screen chapter_select():

    tag menu

    default cs_day = "day3"
    default cs_route = "love"

    use game_menu(_("Chapter Select"), scroll="viewport"):

        vbox:
            spacing 22
            xfill True

            text _("Developer / QA shortcut. This starts a new game with a preset of the earlier story state; it does not play the skipped scenes.") size 22

            text _("Day") size 30
            hbox:
                spacing 16
                for day_id, day_label, day_note in CH01_SELECT_DAYS:
                    textbutton day_label:
                        action [SetScreenVariable("cs_day", day_id), SetScreenVariable("cs_route", "love")]
                        selected (cs_day == day_id)

            $ cs_routes = CH01_SELECT_DAY2_ROUTES if cs_day == "day2" else (CH01_SELECT_DAY5_ROUTES if cs_day == "day5" else CH01_SELECT_END_ROUTES)
            text (_("Day Two lane preset") if cs_day == "day2" else (_("Stored Day Four ending") if cs_day == "day5" else _("Stored Day Two ending"))) size 30
            vbox:
                spacing 8
                for route_id, route_label in cs_routes:
                    textbutton route_label:
                        action SetScreenVariable("cs_route", route_id)
                        selected (cs_route == route_id)

            textbutton _("Begin"):
                action [SetField(persistent, "ch01_chapter_select_pending", (cs_day, cs_route)), Start("ch01_chapter_select_entry")]
                text_size 36

            if gallery_qa_tools_enabled():
                text _("QA (developer only)") size 30
                hbox:
                    spacing 16
                    textbutton _("Unlock all Gallery entries") action Function(debug_unlock_all_gallery)
                    textbutton _("Reset Gallery unlocks and seen CGs") action Function(debug_reset_gallery)
