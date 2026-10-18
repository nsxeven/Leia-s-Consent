# Leia's Consent — Chapter 1 Day 3
# First playable dialogue pass. CG insertion points are comments, not missing image references.
# Entry: ch01_day3_start. Day 2's stored ending is authoritative.

label ch01_day3_start:
    $ d3_end = get_story_value("ch01_d2_end_route", "love")
    $ d3_lane = "ntr" if d3_end in ("ntr_confirmed", "mixed_unresolved") else ("exhibitionism" if d3_end == "exhibitionism" else "love")
    $ set_story_value("ch01_d3_lane", d3_lane)
    $ set_story_value("ch01_d3_ntr_repair_effort", "none")
    scene bg ch01_villa_bedroom_night
    with fade
    if d3_lane == "love":
        "Leia woke beside me, still curled against my shoulder."
        gf "Morning. You're not getting up yet, are you?"
        mc "Wasn't planning to."
        "She kissed me and smiled."
    elif d3_lane == "exhibitionism":
        "Leia stood by the window, looking out toward the beach."
        gf "There are people walking past."
        mc "And?"
        gf "Nothing. Just noticing."
        "She waved when someone looked up, then came back to kiss me."
    else:
        "I woke alone. Leia was already downstairs."
        "Today I was going to try again, properly."
    jump ch01_day3_kitchen

label ch01_day3_kitchen:
    # CG TODO: kitchen island, route-specific framing.
    "Leia leaned over the kitchen island to reach the last clean cup."
    if d3_lane == "love":
        mc "Need help?"
        gf "Only if you're making coffee."
    elif d3_lane == "exhibitionism":
        "She caught me watching and gave me an unmistakably pleased smile."
        gf "Coffee first. Distractions later."
    else:
        "Julian was nearby, sorting the breakfast things."
        mc "Leia, can we talk today?"
        gf "Yeah. We should."
        "Maya appeared before either of us could say more."
    maya "Please tell me there's coffee."
    friend "You asked that before you said good morning."
    maya "I have priorities."
    "Julian looked surprisingly functional considering the night before."
    "Maya, a little hungover but slightly smug, had the look of someone who knew exactly how much attention she was getting."
    friend "Don't."
    mc "I haven't said anything."
    friend "Your face did."
    maya "For the record, nobody put me in that room. I picked it."
    gf "Nobody's disputing the record."
    maya "Good. I'd hate to have to remind anyone whose idea it was."
    "Julian stared into his coffee as though it contained legal advice."
    "Nobody volunteered what had or hadn't happened behind that door, and Maya's grin said she would decide when, and whether, anyone heard."
    maya "Beach club today?"
    gf "Definitely."
    jump ch01_day3_beach

label ch01_day3_beach:
    # BG/CG TODO: public beach-facing infinity pool with full glass wall.
    "The beach club's infinity pool ran along a glass wall facing the public beach."
    "Maya and Leia stopped at the edge to look down at the people beyond it."
    if d3_lane == "love":
        gf "That's a view."
        "She came back to stand beside me."
    elif d3_lane == "exhibitionism":
        "Leia leaned against the glass and glanced back to see whether I was watching."
        mc "Enjoying the view?"
        gf "Maybe the other way around."
        "She took my hand before we moved on."
    else:
        "Leia lingered at the glass, absorbed in the attention from below."
        "Maya glanced at me, then at her."
    maya "I have a challenge."
    friend "Those words never end well."
    maya "Swim rings. Everyone gets one attempt."
    "I jumped first and missed. A few beachgoers booed good-naturedly."
    maya "Embarrassing."
    "Maya made it through cleanly."
    "Julian got wedged in the ring until Maya helped him free."
    friend "I was sabotaged."
    maya "By physics?"
    "Leia jumped last, caught the ring awkwardly and couldn't pull herself free."
    gf "A little help?"
    if d3_lane == "ntr":
        "Julian reached her first and helped steady the ring."
        "Leia hugged him in relief just as I arrived."
        "I stopped a step short."
    else:
        "I reached her and steadied the ring until she could slip free."
        if d3_lane == "exhibitionism":
            gf "My hero. Try not to enjoy the applause too much."
        else:
            gf "Never letting Maya invent a game again."
    jump ch01_day3_lunch_walk

label ch01_day3_lunch_walk:
    scene bg ch01_d3_cutout_path
    with dissolve
    "We had lunch under the cabana before heading back."
    "Maya and Julian stayed behind to settle a few things at the beach club."
    mc "Want to walk back with me?"
    gf "Okay."
    if d3_lane == "ntr":
        mc "I've been distant. I know that."
        gf "And I've been upset."
        mc "I don't want us to keep missing each other."
        gf "Neither do I."
        "For the first time all day, Leia took my hand."
    "A novelty photo stand stood along the quieter path, with a cutout for posing."
    gf "Wait. We have to try this."
    "She stepped into position and immediately got stuck."
    gf "Ryan. Don't laugh."
    mc "I'm not laughing."
    gf "You're absolutely laughing."
    if d3_lane == "ntr":
        "I tried to free her, but the frame wouldn't budge."
        gf "Go get Maya and Julian. Please."
        mc "I'll be quick."
        "I hurried back toward the beach club."

        "Meanwhile, back at the stand:"

        scene bg ch01_d3_cutout_path
        with dissolve

        "The path was quiet. Somewhere past the palms the beach club was only a low murmur of music and voices."
        "Leia tested the frame again. It did not move."
        gf "Unbelievable."

        "Footsteps slowed on the gravel behind her."

        stranger_d3 "Hey. You okay in there?"
        gf "Define okay."
        stranger_d3 "Stuck?"
        gf "Completely. My boyfriend just went to get our friends."

        "He crouched, checked the edges of the frame for a latch and found none."

        stranger_d3 "Nothing. I'll have to pull."

        "His hands settled at her waist, warm and careful, and he pulled."
        "The frame groaned and did not give an inch."
        "He shifted his grip for better leverage, and his thumb slid against bare skin at her side."

        "A small sound escaped Leia before she could stop it. He froze, hands still at her waist."

        stranger_d3 "You okay?"
        gf "...Don't stop."
        stranger_d3 "You sure?"
        gf "Mm-hm."

        $ set_story_flag("ch01_d3_cutout_consent_established")
        $ set_story_value("ch01_d3_cutout_stranger_choice", "leia_chose")

        $ enter_cinematic_mode()
        scene cg ch01_d3_cutout_stranger
        with dissolve

        # CG TODO (artist): ch01_d3_cutout_stranger. NON-EXPLICIT. Daylight, quiet path,
        # Leia wedged in the novelty cutout board, seen from the front/side so her
        # expression carries the frame. Stranger behind her, adult, face mostly out of
        # frame or turned away. His hands stay at her waist / the edge of the board.
        # Her expression is flushed, eyes half closed, receptive. NOT distressed.
        # One of her hands should reach back toward his wrist or rest over his hand
        # so the consent reads visually. No nudity, no explicit anatomy. Crop or
        # compose so the key beat is implied (hands, faces, board edge, palm trees).
        # Final art replaces the placeholder image declared in the visuals file.

        "After that the painted palm trees, the gravel and the far-off music all went soft at the edges."

        $ exit_cinematic_mode()
        scene bg ch01_d3_cutout_path
        with dissolve

        "Voices carried along the path, close enough now to pick out Maya's laugh."
        "He stepped back, and Leia felt the cooler air where his hands had been."

        stranger_d3 "That's your friends, I think."
        gf "That's them."
        stranger_d3 "Do you want me to stay, or go?"
        gf "Go. Please."
        stranger_d3 "Go it is. Take care of yourself."

        "He was gone before the voices rounded the last bend."
        "The frame still had not moved an inch. Leia stayed exactly where she was, heart racing, practicing a face that gave nothing away."

        "When we got back to the path with Maya and Julian, the only person there was Leia."
        "Leia looked flushed and wouldn't quite meet my eyes."
        maya "How did you manage this?"
        gf "I wish I knew."
        "Between the four of us, we finally freed her."
        "Maya and Julian headed back toward the club while Leia and I walked home."
        mc "Was somebody here while I was gone?"
        gf "Someone tried to help."
        mc "Anything else?"
        gf "Nothing changed."
        mc "We were actually having a good conversation earlier."
        gf "I know."
        "We walked side by side. Neither reached for the other's hand."
        $ set_story_flag("ch01_d3_cutout_secret")
    else:
        "I managed to ease the frame apart until Leia could step free."
        if d3_lane == "love":
            gf "My hero again."
            "She kissed me where nobody else could see."
            # CG TODO: extended private Love sequence, art-first.
        else:
            gf "You know what I was thinking when I couldn't get out?"
            mc "Do I want to know?"
            gf "I'll tell you when we're alone."
            # CG TODO: consensual Exhibitionism scene, art-first.
    jump ch01_day3_villa_evening

label ch01_day3_villa_evening:
    # Reset the background for all lanes: the lunch walk leaves the cutout-path
    # placeholder showing, which must not carry over into the villa evening.
    scene bg ch01_villa_entry_evening
    with dissolve
    "Back at the villa, we rested before getting ready for the club."
    if d3_lane == "ntr":
        "Maya noticed the silence between us but didn't push."
        "When I next saw Leia, she was already wearing the Black Cutout Mini from yesterday's shopping trip."
        mc "You look nice."
        gf "Thanks."
        "Neither of us seemed to know what to say next."
    elif d3_lane == "exhibitionism":
        "Leia appeared in her Black Cutout Mini and gave me a little turn."
        gf "Well?"
        mc "You're going to get noticed."
        gf "Good thing you're coming with me."
    else:
        "Leia came out in the Black Cutout Mini she'd bought yesterday."
        gf "What do you think?"
        mc "I think I'm lucky."
        gf "Correct answer."
    "We met Maya and Julian for drinks and group photographs before leaving."
    maya "One proper photo. Nobody blink."
    friend "That's aimed at me, isn't it?"
    jump ch01_day3_club

label ch01_day3_club:
    # BG TODO: nightclub dance floor.
    "Music filled the nightclub. We found a place near the dance floor."
    "Maya dragged Julian toward the music, laughing at his protests."
    if d3_lane == "ntr":
        gf "Can we just enjoy tonight?"
        menu:
            "You're right. Let's just enjoy tonight.":
                $ set_story_value("ch01_d3_ntr_repair_effort", "enjoy")
                mc "You're right. Let's just enjoy tonight."
                "We danced together. For a little while, it felt easy."
            "Can we talk somewhere quieter?":
                $ set_story_value("ch01_d3_ntr_repair_effort", "talk")
                mc "Can we talk somewhere quieter?"
                "We stepped away from the music."
                mc "I'm sorry I've been distant."
                gf "I don't want to lose you."
                mc "I don't want to lose you either."
                gf "Then let's try. Properly."
                "We held each other for a moment before returning."
            "You can enjoy yourself. I'll get a drink.":
                $ set_story_value("ch01_d3_ntr_repair_effort", "withdraw")
                mc "You can enjoy yourself. I'll get a drink."
                "Leia watched me leave, frustrated."
    else:
        "Leia and I danced until she noticed the VIP seating nearby."
    jump ch01_day3_hairclip

label ch01_day3_hairclip:
    # CG TODO: hairclip drop; shared bent-forward composition for Exhib/NTR.
    "Leia's hairclip slipped free near a long VIP sofa occupied by several men."
    if d3_lane == "love":
        "I retrieved it and handed it back."
        mc "Here."
        gf "Thank you."
        "One of the men complimented her dress; Leia smiled politely."
    else:
        "Leia bent forward with straight legs to retrieve it, and her short dress shifted."
        "The men noticed."
        if d3_lane == "exhibitionism":
            "Leia looked back at me with a mischievous smile."
            "She exchanged a few playful remarks before they invited her to sit."
            gf "That's sweet, but I should probably get back to my boyfriend."
            "She came straight back to me, delighted by our shared joke."
        else:
            $ d3_effort = get_story_value("ch01_d3_ntr_repair_effort", "enjoy")
            if d3_effort == "withdraw":
                "Leia accepted their invitation and sat between two of the men."
                "From the bar, I could see her laughing, but couldn't hear a word."
            elif d3_effort == "talk":
                "I approached as she was chatting."
                gf "Can I have another minute?"
                mc "Sure."
                "She returned to me shortly afterward."
            else:
                "I brought our drinks over. Leia introduced me as her boyfriend."
                "We rejoined the music together."
    jump ch01_day3_vip

label ch01_day3_vip:
    if d3_lane == "love":
        "The men invited both of us to sit. We spent a while trading holiday stories."
        gf "Want to get some air?"
        mc "With you? Always."
        jump ch01_day3_balcony
    elif d3_lane == "exhibitionism":
        "The men invited us both onto the sofa."
        "Leia settled beside me, enjoying their teasing about the hairclip."
        gf "You're awfully confident tonight."
        mc "Should I be worried?"
        gf "Maybe I should give you something to worry about."
        "She kissed me, then climbed onto my lap for another long kiss."
        "The group laughed and cheered. I held her close."
        gf "I think we're causing a scene."
        mc "You started it."
        gf "And you didn't stop me."
        "She stood, straightened her dress and took my hand."
        gf "Come with me."
        jump ch01_day3_balcony
    else:
        $ d3_effort = get_story_value("ch01_d3_ntr_repair_effort", "enjoy")
        if d3_effort != "withdraw":
            "The men invited us to sit together. Conversation was easy at first."
            if d3_effort == "talk":
                "Leia squeezed my hand, remembering what we'd promised each other."
            else:
                "I was glad we'd decided to have a good night."
            "My phone buzzed. Julian wanted help with a surprise for Maya."
            friend "Bro, come to the bar for a sec. Need your opinion. Don't bring the girls."
            mc "Julian needs me. I'll be right back."
            gf "Okay. Don't take too long."
        else:
            "Leia stayed between the men while I watched from the bar."
            "One suggested inviting me over. She declined, saying I wasn't in the mood."
            "Julian approached me with his phone."
            friend "Bro, need your opinion on something."
        jump ch01_day3_dessert

label ch01_day3_balcony:
    "We found a quiet balcony away from the music."
    if d3_lane == "love":
        gf "My favourite part of tonight is being here with you."
        mc "Mine too."
        "We kissed and stayed together until the music inside changed."
    else:
        gf "That was different."
        mc "Different good?"
        gf "Very. I liked that we were doing it together."
        "We talked about our boundaries and what we both wanted."
    "We rejoined Maya and Julian for the rest of the night."
    jump ch01_day3_group_return

label ch01_day3_dessert:
    friend "Maya's been complaining about her hangover. I wanted to get her something."
    mc "You dragged me here to choose dessert?"
    friend "Don't make it weird."
    menu:
        "Get her something chocolate.":
            mc "Chocolate. Easy."
            $ set_story_value("ch01_d3_maya_dessert", "chocolate")
        "Ask the bartender what they recommend.":
            mc "Ask the bartender."
            $ set_story_value("ch01_d3_maya_dessert", "recommended")
        "Just admit you're trying to impress her.":
            mc "You like her."
            friend "Just help me order."
            $ set_story_value("ch01_d3_maya_dessert", "surprise")
    "The bartender took a few minutes to prepare the dessert."
    "We carried it to Maya near the dance floor."
    friend "For you."
    maya "I said I wanted something sweet hours ago!"
    friend "I remembered."
    "She hugged him."
    maya "Where's Leia?"
    "I glanced toward the VIP sofa. Leia wasn't there."
    $ d3_effort = get_story_value("ch01_d3_ntr_repair_effort", "enjoy")
    if d3_effort == "withdraw":
        "She'd been sitting with those guys. Now they were gone too."
    elif d3_effort == "talk":
        "She'd asked me not to take long."
    else:
        "She'd been right there when I left."
    jump ch01_day3_search

label ch01_day3_search:
    "I searched the dance floor, the VIP sofa and the corridor near the restrooms."
    "Maya and Julian hadn't seen her."
    # Phone UI TODO: use existing in-game Messages framework; preserve exact typo and timing.
    "I sent Leia a message: Where are you?"
    "A typing indicator appeared, then vanished."
    "After a pause it appeared again."
    "Leia: immn the toliet"
    "Leia: toilet*"
    "I typed: Are you okay?"
    "The typing indicator appeared again, then disappeared without a reply."
    "I waited by the restroom corridor."
    jump ch01_day3_leia_returns

label ch01_day3_leia_returns:
    "Leia finally appeared, looking flustered and adjusting her dress."
    gf "Ryan?"
    mc "I've been looking everywhere."
    gf "Sorry. I was in the bathroom."
    mc "For that long?"
    gf "There was a queue."
    mc "Did you go upstairs with those guys?"
    "She hesitated."
    gf "We were just hanging out."
    mc "So you did?"
    gf "For a little while."
    mc "Why didn't you tell me?"
    gf "I didn't think it was a big deal. Can we not argue here?"
    $ d3_effort = get_story_value("ch01_d3_ntr_repair_effort", "enjoy")
    if d3_effort == "enjoy":
        mc "I thought we were having a good night."
        gf "We were."
        mc "I trusted you."
        gf "You still can."
        mc "Can I?"
    elif d3_effort == "talk":
        mc "You remember what we talked about earlier?"
        gf "Of course."
        mc "Then help me understand."
        gf "I don't know what you want me to say."
        mc "The truth would be a start."
        "Leia looked away."
    else:
        mc "You seemed comfortable with those guys."
        gf "They were being nice to me. You walked away."
        mc "Have you done something wrong?"
        gf "I can't believe you're asking me that."
    "Maya found us near the corridor."
    maya "Everything okay?"
    gf "We're fine."
    maya "Right. Maybe we should head back."
    "While Julian arranged our ride, Maya spoke quietly to Leia."
    maya "Is there something you're not telling him?"
    gf "Can we talk tomorrow?"
    jump ch01_day3_group_return

label ch01_day3_group_return:
    "The four of us headed back to the villa."
    if d3_lane == "ntr":
        "Maya and Julian sat together, quieter than usual."
        $ d3_effort = get_story_value("ch01_d3_ntr_repair_effort", "enjoy")
        if d3_effort == "enjoy":
            "Leia leaned toward me. I didn't know whether to lean back."
        elif d3_effort == "talk":
            "Our hands rested inches apart. Neither of us reached across."
        else:
            "Leia watched the lights pass outside the window. I looked at my phone."
    else:
        "Maya teased Julian about the surprise. Leia rested against me."
    "At the villa, Maya and Julian wished us goodnight and went upstairs."
    jump ch01_day3_bedroom

label ch01_day3_bedroom:
    scene bg ch01_villa_bedroom_night
    with fade
    if d3_lane == "love":
        gf "The balcony was my favourite part."
        mc "Really?"
        gf "Just being there with you."
        "She kissed me and pulled me closer."
        # CG TODO: Love bedroom sequence; insert CGs when approved.
        "We spent the rest of the night together, with the curtains drawn."
        "Afterward she curled against me."
        gf "We should have more nights like this."
        mc "I'm not complaining."
        $ set_story_value("ch01_d3_end_variant", "love_private")
    elif d3_lane == "exhibitionism":
        "Leia looked toward the uncovered bedroom window."
        gf "Remember the sofa?"
        mc "Hard to forget."
        gf "What if we left the curtains open again?"
        mc "Are you sure?"
        gf "With you? Yes."
        "We stayed close by the window, sharing another private moment with the curtains open."
        # CG TODO: exhibition bedroom/window payoff, art-first.
        "Later Leia closed the curtains and came back to bed."
        gf "I think we're getting braver."
        mc "Together."
        gf "Together."
        $ set_story_value("ch01_d3_end_variant", "exhibition_window")
    else:
        mc "Do you still want this?"
        gf "Want what?"
        mc "Us."
        gf "Of course I do."
        mc "Then why does it feel like I'm losing you?"
        gf "I don't know."
        "We turned out the light without resolving anything."
        scene black
        with fade
        # CG TODO: dream-only restroom imagery, never treated as evidence.
        "The nightclub corridor returned in my sleep, distorted and impossibly quiet."
        "Behind the restroom door I imagined Leia kissing one of the men from the sofa."
        mc "Leia?"
        "Dream-Leia turned toward me."
        gf "You weren't supposed to see."
        "The door slammed. My phone showed the same messages again."
        "Leia: immn the toliet"
        "Leia: toilet*"
        "Typing..."
        "The indicator never stopped."
        scene bg ch01_villa_bedroom_night
        with fade
        "I woke sharply. Leia was asleep beside me."
        gf "Ryan...? What's wrong?"
        mc "Just a bad dream."
        gf "Come here."
        "I lay back down. It was only a dream, not proof of anything."
        $ set_story_value("ch01_d3_end_variant", "ntr_restroom_nightmare")
    $ set_story_flag("ch01_d3_complete")
    return
