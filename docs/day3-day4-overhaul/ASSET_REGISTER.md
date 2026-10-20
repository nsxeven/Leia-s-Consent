# CG, phone and UI requirements

No final artwork was generated or replaced. Existing approved binaries are unchanged. All new displayables below are 1920×1080 text cards. Production images need individual review against current GitHub/Notion canon before creation.

| Requirement | Runtime / reuse | Status and final-art dependency |
|---|---|---|
| Nightclub entry / VIP | New `bg ch01_d3_club_revision`; neutral dark placeholder. Existing Day 3 scripts lacked a club BG transition. | **Implemented placeholder.** Final club BG needs the dance floor, VIP sofa, bar, upstairs access and restroom corridor to share consistent geography. |
| Day 2 boutique | Existing `cg ch01_d2_boutique_slip_ryan` / `...julian` and reveal variants. | **Reused unchanged.** Witness and acquisition tests executed. No new artwork. |
| Harbor confrontation / confession | Existing `bg ch01_d4_harbor_wall`; dialogue supports both paths. | **Reused.** No mandatory new CG; preserve player choice on BG. |
| Rooftop dinner | Existing `bg ch01_d4_dinner_terrace`. | **Reused.** Ordinary notification first, discreet later reply. No readable secret screen before discovery. |
| Maya hike photographs | New `cg ch01_d4_hike_private`, one gallery entry `d4_hike_private`. | **Implemented placeholder; final composition pending approval.** A private candid kiss, adults clothed, at the cliff lookout. The image is a photograph being viewed by Ryan, not a live omniscient shot. A second hand-over-lens variant is described but not separately implemented. |
| Club evidence | New `cg ch01_d4_club_evidence`, gallery `d4_club_evidence`. | **Implemented placeholder; final art pending approval.** Kiss in upstairs lounge, Day 3 dress/hairclip state. No explicit photography. Show only after covert discovery. Dialogue states the affair; image need not depict it. |
| Second meeting evidence | New `cg ch01_d4_meeting_evidence`, gallery `d4_meeting_evidence`. | **Implemented placeholder; final art pending approval.** Ferry kiosk light, Day 4 jacket, Adrian and Leia together/kissing. Preserve outfit continuity; final jacket design not approved. |
| Discovery nightmare | New `cg ch01_d4_discovery_nightmare`, gallery `d4_discovery_nightmare`, marked dream. | **Implemented placeholder; final art pending approval.** Distorted corridor/message composition. Never add Julian involvement or new facts through a dream. |
| Love ending | Existing `cg ch01_d4_love_night_01` for early closeness, `...02` private fade now at Scene 16. | **Reused placeholders.** Final art remains pending as before. |
| Shared roleplay | Existing terrace BG, dialogue and kiss. Existing exposure CG declarations retained but not displayed by the replacement roleplay. | **Implemented without new art.** No third-party involvement is implied by this route. Optional close-up would need approval. |
| NTS Discovery ending | Existing bedroom BG, dialogue and tentative hand-holding. | **Implemented without new CG.** Optional emotional close-up is a proposal, not a production requirement. No Day 4 third-party payoff. |

## Phone and UI register

| Sequence | Implementation | Limits / pending work |
|---|---|---|
| Day 3 search | Existing `phone_send_player_message` and `phone_add_message`, IDs `ch01_d3_search_where`, `...typo`, `...correction`, `...okay`. | Exact typo and correction retained; final question remains unanswered. Typing overlay is presentation only; it does not create a message. Visual timing not playtested. |
| Maya → Leia | `ch01_evidence("hike")`; permission and receipt staged in dialogue; private records live outside Ryan's ordinary phone. | Static view, not a full second-character phone OS. Photograph placeholder follows it. No private material automatically saved to Ryan's Photos. |
| Adrian → Leia | `ch01_evidence("club")`, gated by Ryan's factual knowledge; scripted messages identify affair, contact, possession of photographs and possible meeting. | No new Adrian thread in Ryan's phone. Existing phone API untouched. |
| Fictional monitoring | `ch01_evidence("meeting")`, Echo heading, static scripted records and explicit fictional-interface subtitle. | No real surveillance functionality, device permissions, installation workflow or executable payload. |
| Disclosure | Spoken confession and apology; ending contact is described in dialogue and stored as inactive. | No forced photo viewing; knowledge source is voluntary disclosure. Future photo-deletion and privacy discussion remains open story work. |
| Evidence navigation | Modal dark screen, scrollable records, close button and game-menu key returning to scene. | Ren'Py parses it; rendering, touch scrolling and small-screen readability require visual QA. |

Gallery registry grows from 47 to **51 entries** through four new seen-image pages. Existing IDs and placeholder declarations remain stable. Helper unlock tests mark images seen explicitly in an isolated test profile; they do not claim that a rendered scene or phone tap was tested.

Sprite masters, placement transforms, dimensions and layer system are unchanged. These new scenes use BG/text placeholders; no Adrian sprite is claimed. A final Adrian design and sprite family remain **Pending Approval**. Do not substitute the existing cutout or dinner-stranger rig.

Day Five's boat scenes, captain redesign and possible future NTS/NTR encounters are **Planned / Pending Approval**, with no artwork or story implemented here.
