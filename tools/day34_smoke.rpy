# Copy into game/ in a disposable checkout. Never ship this harness.
# Actual parsed Ren'Py branches/Python; presentation interactions are stubbed.
init 999 python:
    def lc_day34_smoke():
        renpy.arguments.takes_no_arguments()
        renpy.execute_default_statement(True)
        import os, json, traceback, re, copy
        checks = []
        traces = []
        try:
            renpy.restart_interaction = lambda: None
            renpy.notify = lambda *a, **k: None
            store.show_choice_feedback = lambda *a, **k: None
            store.maybe_show_status_choice_tutorial = lambda *a, **k: None
            store.phone_queue_notification = lambda *a, **k: None
            renpy.call_screen = lambda name, **kwargs: kwargs.get('options', [None])[0]
            def check(ok, name):
                assert ok, name
                checks.append(name)
            def fresh(day, route):
                store.phone_messages = {'leia': [], 'julian': [], 'group': []}
                store.phone_photos = []
                store.partner_stats.update({'curiosity':20, 'exhibitionism':10, 'secrecy':5, 'temptation':10, 'boundary_looseness':10})
                chapter_select_apply(day, route)
            def walk(label, prefs=(), stops=('ch01_day5_start',)):
                node = renpy.game.script.lookup(label)
                stack, labels, images, says, menus = [], [], [], [], []
                steps = 0
                while node is not None:
                    steps += 1
                    assert steps < 12000, ('loop', label)
                    if isinstance(node, renpy.ast.Label):
                        if node.name in stops:
                            break
                        labels.append(node.name)
                    if isinstance(node, renpy.ast.Python):
                        renpy.python.py_exec_bytecode(node.code.bytecode)
                    elif isinstance(node, renpy.ast.If):
                        selected = next((b for c,b in node.entries if renpy.python.py_eval(c)), None)
                        if selected:
                            node = selected[0]
                            continue
                    elif isinstance(node, renpy.ast.Menu):
                        items = [(c,b) for c,cond,b in node.items if b and renpy.python.py_eval(cond)]
                        assert items, ('empty menu', node.filename, node.linenumber)
                        selected = next(((c,b) for pref in prefs for c,b in items if pref in c), items[0])
                        menus.append(selected[0])
                        node = selected[1][0]
                        continue
                    elif isinstance(node, renpy.ast.Jump):
                        target = renpy.python.py_eval(node.target) if node.expression else node.target
                        node = renpy.game.script.lookup(target)
                        continue
                    elif isinstance(node, renpy.ast.Call):
                        target = renpy.python.py_eval(node.label) if node.expression else node.label
                        stack.append(node.next)
                        node = renpy.game.script.lookup(target)
                        continue
                    elif isinstance(node, renpy.ast.Return):
                        if not stack:
                            break
                        node = stack.pop()
                        continue
                    elif isinstance(node, renpy.ast.Scene):
                        if node.imspec:
                            images.append(' '.join(node.imspec[0]))
                    elif isinstance(node, renpy.ast.Say):
                        says.append(node.what)
                    # Show/hide, screen calls, transitions and narration are not rendered.
                    node = node.next
                result = dict(labels=labels, images=images, menus=menus, steps=steps)
                traces.append(result)
                return result

            # Complete Days Three/Four AST flows for the three public lanes.
            for route in ('love', 'love_repaired', 'exhibitionism'):
                fresh('day3', route)
                t = walk('ch01_day3_start')
                expected = 'exhibitionism' if route == 'exhibitionism' else 'love'
                check(get_story_value('ch01_d4_end_route') == expected, route + ' complete flow')
                check(not ch01_club_betrayal() and not get_story_value('ch01_d4_monitoring_active', False), route + ' no hidden affair/monitoring')
                check('cg ch01_d4_club_evidence' not in t['images'], route + ' no evidence CG leak')
            fresh('day4', 'exhibitionism')
            walk('ch01_day4_start', ('[d4_r_private]',))
            check(get_story_value('ch01_d4_end_route') == 'love', 'Exhibitionism private opt-out')
            fresh('day4', 'exhibitionism')
            walk('ch01_day4_start', ('[d4_r_watch]',))
            check(get_story_value('ch01_d4_exhib_variant') == 'leia_leads_roleplay', 'Exhibitionism alternate roleplay')

            # All three Day Three effort choices preserve event truth and Ryan ignorance.
            for effort in ("You're right.", 'Can we talk', 'You can enjoy'):
                fresh('day3', 'ntr_confirmed')
                t = walk('ch01_day3_start', (effort,), stops=('ch01_day4_start',))
                check(ch01_club_betrayal(), effort + ' establishes club event')
                check(not get_story_value('ch01_d4_ryan_knows_club_event'), effort + ' Ryan remains unaware on Day Three')
                check(get_story_value('ch01_d3_club_contact_active') and get_story_value('ch01_d3_club_private_photos'), effort + ' ongoing contact/photos')
                messages = [m['text'] for m in phone_messages_for_thread('leia')]
                check(messages[-4:] == ['Where are you?', 'immn the toliet', 'toilet*', 'Are you okay?'], effort + ' exact unanswered phone sequence')
                check(not ch01_evidence_rows('club'), effort + ' evidence inaccessible before discovery')
                # Avoid voluntary disclosure on this run to exercise covert continuation.
                t = walk('ch01_day4_start', ('[d4_wall_times]', '[d4_m_loss]'))
                check(get_story_value('ch01_d4_end_route') == 'ntr_confirmed', effort + ' confirmed ending')
                check(get_story_value('ch01_d4_ryan_knows_second_meeting') and get_story_value('ch01_d4_monitoring_active'), effort + ' second meeting and monitoring')
                check(not get_story_value('ch01_d4_leia_knows_discovery'), effort + ' Leia unaware of discovery')
                check(not ch01_nts_agreed(), effort + ' covert path cannot become NTS')
                check('ch01_day4_ntr_react_resolve' not in t['labels'], effort + ' obsolete repair gate excluded')
                check('cg ch01_d4_meeting_evidence' in t['images'], effort + ' evidence CG reached')

            # Unresolved legacy lane retains its repair / unresolved / deepened choices.
            for prefs, expected in (((), 'love_repaired'), (('[d4_fine2]', '[d4_g_accuse]'), 'ntr_unresolved'), (('[d4_fine2]', '[d4_g_withdraw]'), 'ntr_confirmed')):
                fresh('day4', 'mixed_unresolved')
                walk('ch01_day4_start', prefs)
                check(get_story_value('ch01_d4_end_route') == expected, 'unresolved -> ' + expected)
                check(not ch01_nts_agreed(), 'unresolved ' + expected + ' no automatic NTS')

            # The new chapter preset opens eligibility, not automatic agreement.
            for prefs, expected in ((('[d4_d_exclusive]',), 'love_repaired'), (('[d4_d_curious]', '[d4_nts_talk]'), 'nts_discovery'), (('[d4_d_curious]', '[d4_nts_wait]', '[d4_back_love]'), 'love_repaired'), (('[d4_d_curious]', '[d4_nts_wait]', '[d4_back_exhib]'), 'exhibitionism'), (('[d4_d_no]',), 'ntr_unresolved')):
                fresh('day4', 'disclosure_ready')
                t = walk('ch01_day4_start', prefs)
                check(get_story_value('ch01_d4_betrayal_disclosed'), 'voluntary disclosure ' + str(prefs))
                check(get_story_value('ch01_d4_end_route') == expected, 'disclosed -> ' + expected + str(prefs))
                check(ch01_nts_agreed() == (expected == 'nts_discovery'), 'mutual agreement gating ' + str(prefs))
                check(not get_story_value('ch01_d4_monitoring_active') and not has_story_flag('ch01_d4_phone_access_without_permission'), 'disclosure avoids surveillance ' + str(prefs))
                check(not get_story_value('ch01_d3_club_contact_active'), 'disclosure suspends secret contact ' + str(prefs))
                check(not has_story_flag('ch01_day_05_started'), 'new state stops before unsupported Day Five ' + str(prefs))
            # Deliberately incomplete agreement must not resolve to NTS.
            set_story_value('ch01_d4_end_route_pending', 'nts_discovery')
            set_story_value('ch01_d4_ryan_sharing_curiosity', True)
            set_story_value('ch01_d4_nts_future_agreed', False)
            check(ch01_d4_resolved_ending() == 'ntr_unresolved', 'curiosity alone is not consent')
            set_story_value('ch01_d4_nts_future_agreed', True)
            set_story_value('ch01_d4_leia_future_interest', True)
            set_story_value('ch01_d4_nts_boundaries_discussed', True)
            set_story_value('ch01_d4_monitoring_active', True)
            check(not ch01_nts_agreed(), 'monitoring excludes NTS agreement')
            for pref in ('[d4_ntr_fine]', '[d4_check]'):
                fresh('day4', 'disclosure_ready')
                walk('ch01_day4_start', (pref,))
                check(not get_story_value('ch01_d4_betrayal_disclosed', False), 'missed repair retains covert path ' + pref)
                check(get_story_value('ch01_d4_monitoring_active'), 'covert continuation ' + pref)

            # Day Five's illness begins only after lunch and the relationship tracks stay distinct.
            fresh('day5', 'love')
            walk('ch01_day5_start', stops=('ch01_day5_scene_03_no_bars',))
            check(not get_story_value('ch01_d5_ryan_seasick', False), 'Ryan is well through the morning departure')
            for route, expected in (
                ('love', 'love'), ('exhibitionism', 'exhibitionism'),
                ('love_repaired', 'love_repaired'), ('nts_discovery', 'nts_discovery'),
                ('ntr_unresolved', 'ntr_unresolved'), ('ntr_confirmed', 'ntr_confirmed'),
            ):
                fresh('day5', route)
                prefs = ('[d5_u_space]',) if route == 'ntr_unresolved' else ()
                t = walk('ch01_day5_start', prefs, stops=())
                check(get_story_value('ch01_d5_ryan_seasick') is True, route + ' seasickness follows lunch')
                check(get_story_value('ch01_d5_end_route') == expected, route + ' Day Five ending preserved')
                if route == 'love_repaired':
                    check(get_story_value('ch01_d5_repair_provenance') == 'disclosed_betrayal', 'Love Repaired retains disclosure provenance')
                if route == 'nts_discovery':
                    check(get_story_value('ch01_d5_end_route') == 'nts_discovery' and not get_story_value('ch01_d5_nts_experience_occurred'), 'NTS talk-only stays distinct and optional')
                if route == 'ntr_confirmed':
                    check(get_story_value('ch01_d5_captain_event') == 'secret_kiss', 'confirmed NTR stores objective Day Five event')
                    check(get_story_value('ch01_d5_captain_truth_ryan') == 'unknown' and get_story_value('ch01_d5_captain_truth_player') == 'unknown', 'strict POV preserves separate knowledge')
                    check(get_story_value('ch01_d5_monitoring_active') and not get_story_value('ch01_d5_ntr_confronted'), 'NTR monitoring persists without confrontation')
            fresh('day5', 'nts_discovery')
            walk('ch01_day5_start', ('[d5_nts_first_step]',), stops=())
            check(get_story_value('ch01_d5_nts_ryan_willing') and get_story_value('ch01_d5_nts_leia_willing') and get_story_value('ch01_d5_nts_captain_willing'), 'NTS first step requires all three participants')
            check(get_story_value('ch01_d5_nts_boundaries_discussed') and get_story_value('ch01_d5_nts_experience_occurred'), 'NTS consent and experience are tracked separately')

            # Execute the actual boutique branch, both witnesses, with/without Ryan purchase.
            for absent in (False, True):
                for bought in (False, True):
                    fresh('day2', 'ntr_risk')
                    if bought:
                        grant_story_outfit('boutique_cutout_mini', equip=False)
                    t = walk('ch01_day2_scene_11b_boutique', ('[d2_mall_leave_text]',) if absent else ('[d2_mall_go_text]',), stops=('ch01_day2_scene_12_villa_pool_plan',))
                    witness = 'julian' if absent else 'ryan'
                    check(get_story_value('ch01_d2_boutique_slip_witness') == witness, 'boutique witness ' + str((absent,bought)))
                    check(has_story_flag('ch01_d2_leia_noticed_julian_stare') == absent, 'boutique stare ' + str((absent,bought)))
                    check(get_story_value('ch01_d2_mall_outfit_source') == ('ryan' if bought else 'leia'), 'boutique acquisition ' + str((absent,bought)))
                    check('cg ch01_d2_boutique_slip_' + witness in t['images'], 'boutique matching CG ' + str((absent,bought)))
            check(not gallery_validate(), 'gallery registry and images')
            check(all(renpy.has_image(('cg', n)) for n in ('ch01_d4_hike_private','ch01_d4_club_evidence','ch01_d4_meeting_evidence','ch01_d4_discovery_nightmare')), 'new image references exist')
            for entry, image_id in (('d4_hike_private','ch01_d4_hike_private'), ('d4_club_evidence','ch01_d4_club_evidence'), ('d4_meeting_evidence','ch01_d4_meeting_evidence'), ('d4_discovery_nightmare','ch01_d4_discovery_nightmare')):
                renpy.mark_image_unseen(('cg', image_id))
                check(not is_gallery_unlocked(entry), 'gallery locked before seen ' + entry)
                renpy.mark_image_seen(('cg', image_id))
                check(is_gallery_unlocked(entry), 'gallery unlock helper ' + entry)
            missing = []
            for root, dirs, files in os.walk(config.gamedir + '/chapters/ch01'):
                for filename in files:
                    if filename.endswith('.rpy'):
                        with open(os.path.join(root, filename), encoding='utf-8') as f:
                            for cid in re.findall(r'apply_choice\("([^"\n]+)"\)', f.read()):
                                if cid not in CHOICE_EFFECTS:
                                    missing.append(cid)
            check(not missing, 'all literal Chapter One choice IDs registered: ' + str(missing))
            check(not any('adrian' in tid for tid in store.phone_messages), 'private contact never becomes Ryan phone thread')
            output = dict(status='passed', checks=checks, traces=traces, limits=['AST traversal with presentation stubbed', 'No visual playthrough', 'No interactive rollback or save/load test'])
        except Exception:
            output = dict(status='failed', checks=checks, traces=traces, error=traceback.format_exc())
        with open(os.environ['LC_DAY34_REPORT'], 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        if output['status'] != 'passed':
            raise SystemExit(1)
        return False
    renpy.arguments.register_command('day34_smoke', lc_day34_smoke, uses_display=False)
