# Day 3–4 implementation plan

Baseline: main `41913f32e216e9b7cfb96ee7fc5a330468857786`. The user's 20 October specification supersedes the old ambiguous-club/Day Five disclosure plan on the confirmed trajectory only. PR #22 is separate and is not part of main.

1. Preserve Days 1–2 byte-for-byte, including boutique witnesses, purchase source, CG timing and overrides. Audit effective labels rather than removing late patches.
2. Keep the Day 3 lane mapping. Only stored Day 2 `ntr_confirmed` establishes the new nightclub event. The three existing repair-effort options affect dialogue but cannot undo an event by changing a stat. `mixed_unresolved` retains ambiguity and later repair.
3. Name the nightclub man Adrian Vale, 29, a visiting sound technician with dry humor. He is distinct from both existing strangers. He knows Leia has a boyfriend, chooses a concealed affair, and neither coerces nor blackmails her. Keep the private encounter off-screen; establish its facts through stored history and the later non-graphic conversation evidence.
4. Add save-specific story values for event truth, contact, private-photo possession, Ryan's knowledge, Leia's knowledge of his discovery, and Ryan's fictional monitoring choice. Never use cross-save `persistent` for story truth. Never put Leia's private conversations in Ryan's normal phone before discovery.
5. Confirmed Day 4 bypasses obsolete disclosure/repair gates at the harbor and evening. Preserve the existing unresolved repair branch. Preserve Maya/Julian's independent hike; explicitly allow time for photos before Scene 11's receipt.
6. Implement a static fictional evidence screen with scripted messages and placeholder cards. No networking, device access, executable surveillance, installation process or real instructions. Keep private-photo evidence non-graphic. Ordinary messages continue using the established phone API.
7. Keep early romance in Scene 13; move final romantic fade to Scene 16. Preserve private opt-out and existing route IDs. Confirmed ending remains `ntr_confirmed`, with separate knowledge flags and Julian uncertainty.
8. Update Day Four chapter-select setup only. Legacy saves without new event history are not retroactively declared to contain the affair; replay Day Three or select Day Four confirmed. Day Five story and presets remain unchanged, with incompatibilities documented for follow-up.
9. Validate actual Ren'Py parsing/lint and execute headless branch/state tests. Report visual, rollback and save/load coverage separately. Publish a review branch/PR and update existing Notion pages with Implemented, Pending Approval and Planned status.

Known dependencies: the phone presentation patch wraps `phone_add_message` and automatically indexes attachments; private evidence therefore needs separate storage. Gallery unlocks derive from seen CG images, not phone attachments. No duplicate Day 3/4 labels or overrides were found in the initial label scan; Day 1/2 and phone-screen overrides remain untouched.

## Approved amendments during implementation

The subsequent user directions add an optional guilt-driven voluntary disclosure branch. Day Three `talk`, Day Four `joined`, the harbor fear response and listening instead of cross-checking open it. Ryan explicitly makes a genuine repair attempt; Leia confesses and apologizes. The event remains a betrayal.

After time to process, evening choices are exclusive repair, exploring unexpected sharing curiosity, or inability to reconcile. Curiosity opens a separate mutual discussion. Only both agreeing to explore the question, without acting yet, produces `nts_discovery`. Declining NTS offers `love_repaired` or `exhibitionism`; rejecting reconciliation itself still allows `ntr_unresolved`. Covert monitoring can never set this mutual-agreement state.

All new nightclub-event branches end safely after Day Four because the unchanged Day Five script assumes either deferred confession or ignorance, and silently maps an unknown NTS ending to Love. Existing Love, Exhibitionism and legacy unresolved paths retain their Day Five link. The new Day Four Chapter Select option seeds eligibility, not forced consent. Day Five presets and story remain unchanged pending their separate overhaul.
