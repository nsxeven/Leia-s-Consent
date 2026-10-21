# Prologue + Day One Demo — Release handoff

Branch: `release/prologue-day1-demo-polish` (based on main `41913f32e216e9b7cfb96ee7fc5a330468857786`)
Status: IMPLEMENTED IN BRANCH / NOT YET VERIFIED IN LIVE REN'PY / NOT RELEASED.
Scope: Prologue and Day One launch. Day 2–5 working branches are deliberately not merged.

## Approved creative rules preserved
- Leia remains the same clumsy, silly, affectionate character. No exposure/collision/carry/movie incidents were removed.
- The deliberately shy/ambiguous progression during movie night is preserved on its original choices.
- Ryan/Leia begin as a genuinely affectionate long-term couple; Julian remains the loyal long-term friend.
- No production image placeholders or audio files were replaced; artist will supply them.
- A few dialogue consequences now acknowledge Ryan's actual earlier choices, especially respecting Leia's discomfort and whether Ryan pressed Julian.

## Editorial/code edits implemented
- Dynamic `player_name`, `girlfriend_name`, and `friend_name` interpolation replaces hardcoded visible names in Prologue/Day One story narration, the sleeping/carry override, and staged-photo dialogue.
- Names are resolved dynamically in Phone header/tutorial/status text, pool-photo attachment labels, and Gallery descriptions/titles/routes.
- Corrected outdated “known each other longer than a day” reference.
- Tightened several towel/photo lines and added a small present-day affection beat to the Prologue.
- Added choice-conditional Scene 18 and Scene 28 dialogue so a respectful Ryan is not treated as if he provoked Leia or Julian.
- Added a short warm bedtime callback for attentive Love playthroughs. Full nightmare remains available.
- Five photo-shutter flashes now use a registered white image instead of undefined `scene white`.
- Legacy photo aliases reference defined visual assets rather than `ImageReference()` strings that generated lint warnings.
- Replaced out-of-range init priorities 1000–1003 with supported 998 in affected scripts; removed undeclared `hide julian` statement.
- Added Full Transparency `Route Explorer` (Status/Settings and Phone Settings). Player can select Story-driven, Love, Exhibitionism or NTR risk during the early story. This deliberately seeds related stats and changes future Day One / Day Two route checks. It does not replay earlier scenes or automatically modify fixed route history.
- Normal/Insight modes cannot change routes; the Developer-mode entry in the phone settings is now reserved for developer builds. Route switching is intentionally an optional **Full Transparency** exploration/cheat feature; it is not a canonical in-world character decision.
- Added 18+ maturity acknowledgment, standalone Day One completion card, persistent completion flag, Day Two entry gate, and Chapter Select gate.
- Demo identity changed to `Leia's Consent — Day One Demo`, `0.1.0-demo.1`.

## Route Explorer constraints
Currently the supported dynamic branch steering is Day One and Day Two. Later fixed end states are intentionally not rewritten; switching stops being available after Day Two completes. For future Day 3–5 releases, extend the route adapter with explicit saved knowledge/consent and scene-state contracts before promising arbitrary late-game route switching. In this Day One demo all three early focuses are selectable from the Full Transparency screen.

## Outstanding artwork (currently literal placeholder CGs)
1. `ch01_trip_catch`
2. `ch01_drive_back_seating`
3. `ch01_julian_carry`
4. `ch01_carry_dress_shift`
5. `ch01_night_pool_attention`
6. `ch01_movie_cuddle_blanket`
7. `ch01_movie_no_blanket`
8. `ch01_lounge_micro_test`
9. `ch01_photo_late_favourite` (phone-sized attachment)
10. `ch01_dream_towel_replay`
11. `ch01_dream_towel_shift`
12. `ch01_dream_towel_curtain`
13. `ch01_dream_stranger_behind`
14. `ch01_dream_stranger_look`
15. `ch01_dream_stranger_reach`

Use existing stable image IDs. Match established art specs, camera/POV, character clothes, and adjacent compositions; update placeholder registry definitions only after the source images exist. Two other defined placeholder BGs are not referenced by the Day One script and are not Day One release blockers.

## Mandatory before release
1. Replace every *referenced* placeholder asset; visual-check scaling and phone gallery full-screen image views.
2. Run Ren'Py 8.5.3 lint on the exact release branch AFTER art replacement. Earlier lint had 17 diagnostics; patches target the known issues, but fresh lint has NOT been executed in this session.
3. Complete beginning-to-end playthroughs for normal Love-leaning, Exhibitionism-leaning and NTR-risk states, plus Full Transparency route switching mid-run and switching back to Story-driven.
4. Test name customization: different names for all three characters, including swapped canonical names; inspect story, Phone and Gallery.
5. Test both swimsuit variants and pool photo capture counts, towel-did-he-see timing, restaurant bra continuity, sleeping/carry override, and staged late phone photo with early/late handset closing.
6. Test age notice acceptance/exit, Day One end card and main-menu return; verify Day Two and Chapter Select are inaccessible.
7. Test save/load and rollback before and after route switching and across the Day One finish.
8. Run packaged Windows build, verify menu/thumbnail/metadata, music/SFX plan, adult-platform policy, and visibility of no debug/placeholder text.
9. Verify installed release has expected assets, and that any future-day scripts bundled but gated do not create unwanted size or content exposure.
10. Merge only after approval and tested release handoff; review conflicts with separate dialogue-polish PR #22.

## Verification accomplished
- GitHub source compare and static text/assertion checks against updated branch.
- Checked that dialogue/narration in the reviewed Prologue and Day One story/override files no longer hardcodes the customizable names.
- Checked source for declared photo-flash image, image aliases, route focus hooks, and demo gate.
- **No actual Ren'Py lint, visual playthrough, package build, screenshot review, or release upload was executed in this chat.**
