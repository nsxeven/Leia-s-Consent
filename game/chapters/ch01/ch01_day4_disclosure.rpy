# Optional, voluntary truth; never reached from covert monitoring.
label ch01_day4_voluntary_disclosure:
    "I put my phone away and turned toward her."
    mc "I miss you. Not how we looked yesterday, or whether dinner was nice. You."
    mc "I keep trying to protect myself by making you speak first. I'm sorry. I'm here now."
    "Her eyes filled before she answered."
    gf "Please don't be kind to me because you think nothing happened. I can't let you do that."
    gf "I went upstairs with Adrian. We slept together."
    "For a moment I could hear a loose rope tapping against a mast below us. Nothing else."
    mc "While I was looking for you."
    gf "Yes."
    mc "And you let me stand there apologizing for asking."
    gf "I did. I'm sorry."
    "I moved my hand away from hers. She left it where it was."
    gf "We've been messaging. He has photos we took. I haven't told him to stop."
    mc "You were going to keep seeing him?"
    gf "I hadn't let myself finish that thought. That's not an excuse."
    mc "Don't make this something I caused by going to the bar."
    gf "You didn't. I was angry with you, and I liked being with someone who didn't know any of it. I still chose what I did."
    "She wasn't asking whether we were okay anymore. I was glad of that. I couldn't have answered."
    mc "I need time. Not another version of what happened. Just time."
    gf "I'll stop the conversation with him. You can watch me send it if you want."
    mc "Tell him because you mean it."
    "She wrote that she wouldn't meet him again and needed space. Then she put the phone away."
    $ set_story_value("ch01_d4_betrayal_disclosed", True)
    $ set_story_value("ch01_d4_discovery_source", "voluntary_disclosure")
    $ set_story_value("ch01_d4_ryan_knows_club_event", True)
    $ set_story_value("ch01_d4_ryan_knows_contact", True)
    $ set_story_value("ch01_d4_ryan_knows_private_photos", True)
    $ set_story_value("ch01_d4_leia_knows_discovery", True)
    $ set_story_value("ch01_d3_club_contact_active", False)
    $ set_story_value("ch01_d4_end_route_pending", "ntr_unresolved")
    $ set_story_value("ch01_d4_ntr_outcome", "ntr_unresolved")
    $ set_story_flag("ch01_d4_scene_08_complete")
    "We stayed at the harbor until Maya and Julian came back. I asked them for a minute, and they gave us one."
    jump ch01_day4_scene_09_getting_ready

label ch01_day4_disclosed_evening:
    scene bg ch01_d4_terrace_night
    with fade
    "We'd made it through dinner. I'd even laughed at something Julian said. Then the four of us had become two again."
    gf "Do you want to talk?"
    mc "I don't think I can keep doing small talk."
    "She sat at the other end of the bench and waited."
    mc "I keep thinking of things I want to ask. Then I don't know if the answer will help."
    gf "You don't have to decide everything tonight."
    mc "I know. I need to decide something."
    $ d4_d_exclusive = format_choice("ch01_d4_disclosed_exclusive", "I want us to rebuild, just the two of us.")
    $ d4_d_curious = format_choice("ch01_d4_disclosed_curious", "I'm hurt. But some of what I'm feeling is curiosity, and I don't understand it yet.")
    $ d4_d_no = format_choice("ch01_d4_disclosed_unresolved", "I can't promise we can come back from this.")
    menu:
        "[d4_d_exclusive]":
            $ apply_choice("ch01_d4_disclosed_exclusive")
            mc "I want us to rebuild, just the two of us. I can't do another secret."
            gf "Neither can I. I want to try."
            mc "That doesn't mean tomorrow will be normal."
            gf "I know. I'll answer what you ask. Even when the answer makes me look worse."
            $ set_story_value("ch01_d4_end_route_pending", "love_repaired")
        "[d4_d_curious]":
            $ apply_choice("ch01_d4_disclosed_curious")
            $ set_story_value("ch01_d4_ryan_sharing_curiosity", True)
            mc "I'm hurt. But some of what I'm feeling is curiosity, and I don't understand it yet."
            gf "Curiosity about what happened?"
            mc "At first. Then I wondered whether I'd feel differently if we'd talked first. If we both wanted someone else involved."
            "Leia looked at me for a long moment."
            gf "Are you saying that because you think it's how you keep me?"
            mc "I'm scared of losing you. I can't pretend I'm not. But that's not the whole feeling."
            mc "I don't want to turn what happened into something I secretly agreed to. I didn't."
            gf "I know you didn't."
            mc "But I think part of me wants to explore the idea. That's why this is so hard to say."
            "She drew her knees up onto the bench."
            gf "I might want to talk about it. I don't know whether I'd want to do it. Those are different things."
            mc "They are for me too."
            $ set_story_value("ch01_d4_leia_future_interest", True)
            $ d4_nts_talk = format_choice("ch01_d4_nts_talk_only", "Agree to explore the question together, without acting on it yet.")
            $ d4_nts_wait = format_choice("ch01_d4_nts_not_ready", "I don't want to involve anyone else. Let's find our way back to us.")
            menu:
                "[d4_nts_talk]":
                    $ apply_choice("ch01_d4_nts_talk_only")
                    mc "Could we keep talking about it, without arranging anything?"
                    gf "Yes. Just talking. And if one of us changes our mind, we say so."
                    mc "No private plans while the other person thinks we're still deciding."
                    gf "Agreed. Adrian stays out of it. I'm not asking you to make room for him."
                    mc "And this isn't a way around rebuilding trust."
                    gf "I know. We still have that to do."
                    $ set_story_value("ch01_d4_nts_boundaries_discussed", True)
                    $ set_story_value("ch01_d4_nts_future_agreed", True)
                    $ set_story_value("ch01_d4_nts_discovery", True)
                    $ set_story_value("ch01_d4_end_route_pending", "nts_discovery")
                "[d4_nts_wait]":
                    $ apply_choice("ch01_d4_nts_not_ready")
                    mc "I needed you to hear it. But I don't want to involve anyone else."
                    gf "Okay. We leave that idea here."
                    $ set_story_value("ch01_d4_nts_future_agreed", False)
                    $ d4_back_love = format_choice("ch01_d4_back_love", "Rebuild privately, just the two of us.")
                    $ d4_back_exhib = format_choice("ch01_d4_back_exhibition", "Keep the playful attention we share together. Nothing with another person.")
                    menu:
                        "[d4_back_love]":
                            $ apply_choice("ch01_d4_back_love")
                            mc "I want to feel close to you again. Just us."
                            gf "I want that too. We'll take our time."
                            $ set_story_value("ch01_d4_end_route_pending", "love_repaired")
                        "[d4_back_exhib]":
                            $ apply_choice("ch01_d4_back_exhibition")
                            mc "I still like flirting with you, being out together. Feeling like we're in on the same joke."
                            mc "That doesn't mean I want anyone else involved."
                            gf "Then that's where we stop. And if it doesn't feel good, we go home."
                            $ set_story_value("ch01_d4_shared_attention_agreed", True)
                            $ set_story_value("ch01_d4_end_route_pending", "exhibitionism")
        "[d4_d_no]":
            $ apply_choice("ch01_d4_disclosed_unresolved")
            mc "I can't promise we can come back from this."
            gf "I want us to. But I heard you."
            "She didn't reach across the bench. I was grateful she hadn't made me move away again."
            $ set_story_value("ch01_d4_end_route_pending", "ntr_unresolved")
    $ set_story_value("ch01_d4_ntr_outcome", get_story_value("ch01_d4_end_route_pending"))
    $ set_story_value("ch01_d4_ntr_repaired", get_story_value("ch01_d4_end_route_pending") == "love_repaired")
    $ set_story_flag("ch01_d4_scene_13_complete")
    jump ch01_day4_scene_14_night_after
