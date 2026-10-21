# Prologue / Day One — Continuity and immersion polish
Date: 2026-10-21
Target: `main` (unrestricted full development build)
Status: **Code changes committed; requires live Ren'Py testing before release.**
Scope: Prologue and Day 1 only; no Day 2–5 plot rewrites.

## Locked creative intentions
- Leia remains an affectionate, silly, and clumsy character; retain **all** approved towel, restaurant, street-fall, carry, and movie-night incidents.
- Preserve the deliberate gradual shyness/curiosity in movie-night dialogue; do not convert her behavior into an already-established route.
- Ryan POV and wardrobe continuity are mandatory. No incorrect casual/purple-dress sprite should substitute for a yet-unproduced loungewear/seated sprite.
- The main branch must remain **unrestricted**, with Chapter Select accessible and the Day 1 demo gate disabled. Do not merge demo-only gate changes back to main.

## Fixed
1. **Arrival scene:** The car BG now matches a transfer-car arrival at the villa; jetty travel occurs before the scene. Master-bedroom balcony connection is established in the narration and reused by the towel incident.
2. **Pool photo-stop continuity:** When Leia decides to stop and Julian says her solo capture was deleted, `ch01_pool_capture_count` is now **0**. The delivery helper correctly returns no solo photographs; it does not resurrect the capture through a default of 1. The **already-established group selfie**, outfit-correct, is delivered as the optional late photo on this path.
3. **Late favourite outfit variants:** Added `ch01_photo_late_favourite_white` and `ch01_photo_late_favourite_blue` image IDs, both temporarily pointing to the same placeholder, for distinct final assets. Retained legacy `ch01_photo_late_favourite` for existing saved attachment references.
4. **Street fall:** Both existing `CH1D1_CG_StreetWalkFall_01.webp` and `_02.webp` are now registered and played in chronological 01 → 02 order. Removed the erroneous Leia dialogue sprite overlay from the active fall CG.
5. **Maya call and relationship:** Ryan hangs up after Leia's fall before speaking to Leia and Julian. He explicitly tells Leia he and Maya have always been friends, resolving the unanswered dating question. This should be treated as an affirmative *editorial canon decision* and checked against any future intended backstory.
6. **Scene 13:** The previously redirected “Leia sleeps / Julian carries her” revision was made the *authoritative* Scene 13. The obsolete developer-end card and fragile `config.label_callback` override are gone. The old revised-label entry survives as a compatibility jump for development saves. Day 1 continues to night pool.
7. **Movie-night visuals:** Existing seated compositions stay visible during interactive dialogue rather than repeatedly displaying a blank living-room background; the group CG is removed when Julian actually walks to the kitchen. After Leia fixes or adjusts her top, the image returns to the ordinary seated composition. Production-quality loungewear or seated variants would allow even better expression staging later.
8. **Responsive dialogue:** A Ryan who stops and lightly teases can still receive Leia's acknowledgment of respecting her discomfort. The private aftermath checks the actual high-pressure choices, rather than treating all non-default choices as provocation.
9. **Day 1 ending:** Affectionate Love-path bedtime dialogue is shown on the bedroom scene, *then* the screen fades to the dream. The shared dream remains intact.
10. **Customization:** Fixed the remaining hardcoded name in the street-fall joke choice and the dream grounding choice.
11. **Prose:** Removed redundant narrator commentary about Leia and Julian “becoming friends” and one overly explanatory pool-gaze ending, while retaining all dialogue and incidents.

## Still required
- Replace the remaining **14** referenced Day 1 placeholders (3 night/movie CGs, carry/drive assets, closing dream sequence, etc.); register the final white/blue late pool favourite appropriately.
- Review fall CG 01 and 02 visually for intended beat order, composition, camera and adjacent scene continuity. Files were checked by name and source registration, not opened visually.
- Run **Ren'Py 8.5.3 lint** on the exact current `main` commit. No Ren'Py runtime/compiler is exposed through the GitHub connector in this task.
- Conduct real playthroughs through **Prologue, Love, Exhibitionism and NTR-risk** branches, including both swimsuits, all photo-stop outcomes, Day 1 Scene 13 direct flow, Phone attachment indexing, custom names, save/load/rollback, and Day 1 → Day 2 progression.
- Verify every in-story character has the correct sprite/CG outfit, position, layer ordering, and line timing.
- Sound/music are deliberately deferred by the owner. Avoid claiming audio validation.
- Release branch `release/prologue-day1-demo-v0.1.0` is a snapshot and has **not** automatically received the main-branch corrections. Create a fresh release candidate or cherry-pick reviewed changes when ready.

## QA guidance for photo delivery
- Capture paths: 0 deleted, 2 supportive, 3 photo-more, 2 chose-to-continue. Do not deliver more solos than actually earned.
- Early stop: no deleted solo arrives in Trip Group/Photos; only initial group selfie may be delivered later.
- Other paths: earned Capture IDs continue to arrive after the towel follow-up; a separately staged late favourite remains a narrative reveal.
- Check rolling back before photo delivery and reopening the Phone after delayed notifications.

## Source/verification scope
Reviewed current `main` story files, overrides, relevant image definitions, Phone attachment logic, and chapter release settings. Static checks and GitHub content reads only. No playable build has been generated or uploaded.
