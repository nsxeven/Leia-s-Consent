# Phone moments demo - developer/QA only (game/dev/ is left out of release builds).
#
# Plays the three phone moments in Maya's chat, with no story content: an incoming call
# (Answer / Let it ring; letting it ring leaves a missed call and the Messages badge), then a
# reply card with a hesitating reply, "Leave it on read" and a plain reply. Reach it from the
# developer systems menu ("Phone moments demo") or `jump lc_dev_phone_moments`. Its ids start
# with dev_pm_ and are not story values any Day reads. Docs: docs/PHONE_MOMENTS.md.

label lc_dev_phone_moments:
    scene black
    with dissolve
    $ set_phone_unlocked(True)
    $ set_phone_hud_enabled(True)
    $ lc_phone_set_story_time("23:12")
    "Phone moments demo. Maya is about to call."
    call lc_phone_call("maya", "dev_pm_call", answer_label="lc_dev_phone_moments_answered", ignore_label="lc_dev_phone_moments_ignored") from lc_dev_phone_moments_ring
    $ lc_dev_pm_outcome = _return
    "The call came back as \"[lc_dev_pm_outcome]\". Missed calls not returned: [len(lc_phone_missed_calls())]"
    $ lc_phone_set_story_time("23:41")
    call lc_dev_phone_moments_offer from lc_dev_phone_moments_offer_1
    $ lc_dev_pm_choice = get_story_value("dev_pm_dm", "none")
    $ lc_dev_pm_on_read = lc_phone_left_on_read("dev_pm_dm")
    "Reply card answered with \"[lc_dev_pm_choice]\". Left on read: [lc_dev_pm_on_read]."
    $ lc_phone_clear_story_time()
    return

label lc_dev_phone_moments_answered:
    "(Answered. A scene would play the call here, then carry on.)"
    return

label lc_dev_phone_moments_ignored:
    "(Let it ring. Maya's chat now shows a missed call, and Messages has a badge.)"
    return

# The reply card: open the phone (the chat is already showing) and pick an option.
label lc_dev_phone_moments_offer:
    python:
        phone_add_message("maya", "maya", text="you two okay up there? 👀", message_id="dev_pm_dm_01",
                          mark_unread=True, notify=True, notification_title="Maya")
        phone_offer_reply("maya", "dev_pm_dm", [
            {"id": "reply", "text": "We're fine. Go to sleep, Maya.", "hesitate": True,
             "draft": "Why are you still"},
            {"id": "read", "text": "Leave it on read", "leave_on_read": True},
            {"id": "show", "text": "Show [girlfriend_name]",
             "followups": [("maya", "hi [girlfriend_name] 😇")]},
        ], "read")
        lc_phone_deep_link = ("thread", "maya")
        renpy.show_screen("phone_screen")
    "Pick a reply in Maya's chat, then close the phone."
    return
