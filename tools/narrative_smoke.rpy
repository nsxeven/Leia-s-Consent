# Developer-only harness. Copy into game/ ONLY in a disposable test checkout.
# Registers a no-display CLI command using the Ren'Py 8.5.3 command API.
# This is a state smoke test, not a visual playthrough or rollback test.
init 999 python:
    def lc_narrative_smoke():
        renpy.arguments.takes_no_arguments()
        renpy.execute_default_statement(True)
        import json
        import os
        import traceback
        import copy
        results = []
        try:
            keys = ('story_flags', 'story_values', 'relationship_stats', 'partner_stats', 'player_stats', 'choice_history', 'owned_outfits', 'equipped_outfit', 'money')
            initial = {k: copy.deepcopy(getattr(store, k)) for k in keys}
            def reset_test_state():
                for k, v in initial.items():
                    setattr(store, k, copy.deepcopy(v))
            def run_top_level_python(label_name):
                # Execute only top-level Python statements, not scene/interaction nodes.
                for node in renpy.game.script.lookup(label_name).block:
                    if isinstance(node, renpy.ast.Python):
                        renpy.python.py_exec_bytecode(node.code.bytecode)
            for day, presets in (('day2', CH01_SELECT_DAY2_PRESETS), ('day3', CH01_SELECT_END_PRESETS), ('day4', CH01_SELECT_END_PRESETS), ('day5', CH01_SELECT_DAY5_PRESETS)):
                for route in presets:
                    reset_test_state()
                    entry = chapter_select_apply(day, route)
                    assert renpy.has_label(entry), entry
                    if day == 'day2':
                        assert ch01_d2_route_lane() == route, (route, ch01_d2_route_lane())
                    elif day in ('day3', 'day4'):
                        assert get_story_value('ch01_d2_end_route') == route
                    else:
                        assert get_story_value('ch01_d4_end_route') == route
                        run_top_level_python('ch01_day5_start')
                        expected = 'ntr_repaired' if route == 'love_repaired' else route
                        assert get_story_value('ch01_d5_track') == expected
                        assert get_story_value('ch01_d5_end_route_pending') == route
                    results.append('PASS preset {}:{}'.format(day, route))
            for route in ('love', 'exhibitionism', 'love_repaired', 'ntr_unresolved', 'ntr_confirmed'):
                reset_test_state()
                chapter_select_apply('day5', route)
                run_top_level_python('ch01_day5_start')
                run_top_level_python('ch01_day5_scene_16_finish')
                assert get_story_value('ch01_d5_end_route') == route
                assert has_story_flag('ch01_day_05_complete')
                results.append('PASS Day Five stored ending ' + route)
            # Inspect the actual dinner menu AST; evaluate its existing branch expressions.
            dinner = renpy.game.script.lookup('ch01_day5_scene_10_dinner')
            brave_block = next(block for node in dinner.block if isinstance(node, renpy.ast.Menu) for caption, cond, block in node.items if caption == '[d5_as_brave]')
            branch = next(node for node in brave_block if isinstance(node, renpy.ast.If))
            cases = [
                ('ntr_unresolved', 'love_repaired', 'Telling you. Obviously.'),
                ('ntr_confirmed', 'love_repaired', 'Telling you. Obviously.'),
                ('ntr_repaired', 'ntr_unresolved', 'Telling you. Obviously.'),
                ('ntr_repaired', 'love_repaired', 'Telling you. Obviously.'),
                ('ntr_unresolved', 'ntr_unresolved', 'Showing up at the pier. And not running.'),
                ('ntr_confirmed', 'ntr_confirmed', 'Showing up at the pier. And not running.'),
                ('love', 'love', 'Telling you about the hallway. The ten minutes.'),
            ]
            for track, pending, expected in cases:
                store.d5_track, store.d5_pending = track, pending
                selected = next(block for condition, block in branch.entries if renpy.python.py_eval(condition))
                actual = next(n.what for n in selected if isinstance(n, renpy.ast.Say))
                assert actual == expected, (track, pending, actual)
                results.append('PASS dinner callback {} -> {}'.format(track, pending))
            missing = []
            import re
            for root, dirs, files in os.walk(config.gamedir + '/chapters/ch01'):
                for filename in files:
                    if filename.endswith('.rpy'):
                        with open(os.path.join(root, filename), encoding='utf-8') as source:
                            for choice in re.findall(r'apply_choice\("([^"\n]+)"\)', source.read()):
                                if choice not in CHOICE_EFFECTS:
                                    missing.append(choice)
            assert not missing, sorted(set(missing))
            results.append('PASS all literal Chapter One apply_choice IDs registered')
            errors = gallery_validate()
            assert not errors, errors
            results.append('PASS gallery_validate')
            output = {'status': 'passed', 'checks': results, 'limits': ['No visual playthrough', 'No save/load or rollback interaction', 'Top-level state execution does not explore every branch']}
        except Exception:
            output = {'status': 'failed', 'checks': results, 'error': traceback.format_exc()}
        with open(os.environ['LC_NARRATIVE_TEST_REPORT'], 'w', encoding='utf-8') as report:
            json.dump(output, report, indent=2)
        if output['status'] != 'passed':
            raise SystemExit(1)
        return False

    renpy.arguments.register_command('narrative_smoke', lc_narrative_smoke, uses_display=False)
