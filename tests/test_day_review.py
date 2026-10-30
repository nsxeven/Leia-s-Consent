"""Run without Ren'Py: python3 -m unittest discover -s tests -v.
Tests the production init block with engine boundaries stubbed, not a copy of logic.
"""
import copy
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]

class DayReviewTests(unittest.TestCase):
    def setUp(self):
        self.store = SimpleNamespace(
            relationship_stats=dict(love=50, trust=50, boredom=10, momentum=0),
            partner_stats=dict(curiosity=20, temptation=10, exhibitionism=10, boundary_looseness=10, secrecy=5),
            player_stats=dict(jealousy=20, acceptance=10), lc_review_active=None,
            lc_review_days={}, lc_title_facts={}, modified_save=False,
            persistent=SimpleNamespace(lc_title_style='story', lc_title_badges=False))
        self.values = {}
        self.shown = []
        self.config = SimpleNamespace(show=lambda name, *a, **kw: self.shown.append(name))
        self.gallery = {}
        for i in range(8):
            self.gallery[str(i)] = dict(id=str(i), tab='ch01_d1', title='Moment '+str(i),
                dream=i == 7, pages=[{'image': 'test_'+str(i)+'_blue'}, {'image': 'test_'+str(i)+'_white'}])
        self.env = dict(store=self.store, persistent=self.store.persistent, config=self.config,
            renpy=SimpleNamespace(showing=lambda tag: False, show_screen=lambda *a, **kw: None),
            get_stat_group=lambda group: getattr(self.store, group+'_stats'),
            get_story_value=lambda key, default=None: self.values.get(key, default),
            GALLERY_ENTRIES=self.gallery, STAT_LABELS={})
        source = (ROOT/'game/systems/day_review.rpy').read_text()
        init = source.split('init 20 python:\n', 1)[1].split('\nlabel lc_day_review', 1)[0]
        exec(compile(textwrap.dedent(init), 'day_review_init', 'exec'), self.env)

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def begin(self): self.call('lc_review_begin', 'ch01_d1')
    def finish(self): return self.call('lc_review_finish', 'ch01_d1')

    def test_baseline_is_copy_and_reentry_does_not_reset(self):
        self.begin(); self.store.relationship_stats['love'] = 60; self.begin()
        self.assertEqual(self.store.lc_review_days['ch01_d1']['start']['relationship']['love'], 50)

    def test_only_current_day_shown_images_recorded(self):
        self.begin(); self.call('lc_review_record_image', 'bg elsewhere')
        self.call('lc_review_record_image', 'cg unknown')
        self.call('lc_review_record_image', ('cg','test_0_blue'))
        self.assertEqual([c['image'] for c in self.call('lc_review_cards','ch01_d1')], ['test_0_blue'])
        self.call('lc_review_begin', 'ch01_d2'); self.call('lc_review_record_image', 'cg test_1_blue')
        self.assertEqual(self.call('lc_review_cards','ch01_d2'), [])

    def test_latest_actual_variant_one_card_per_moment(self):
        self.begin()
        for x in ('test_0_blue','test_0_white','test_0_white'): self.call('lc_review_record_image', 'cg '+x)
        self.assertEqual([c['image'] for c in self.call('lc_review_cards','ch01_d1')], ['test_0_white'])

    def test_selection_covers_day_and_caps_five(self):
        self.begin()
        for i in range(8): self.call('lc_review_record_image', 'cg test_'+str(i)+'_blue')
        cards = self.call('lc_review_cards','ch01_d1')
        self.assertEqual(len(cards), 5); self.assertEqual(cards[0]['id'],'0'); self.assertEqual(cards[-1]['id'],'7')
        self.assertTrue(cards[-1]['dream'])

    def test_finish_is_idempotent_and_stops_capture(self):
        self.begin(); record=self.finish(); self.store.relationship_stats['love']=99
        self.call('lc_review_record_image', 'cg test_0_blue')
        self.assertEqual(self.finish(), record); self.assertIsNone(self.store.lc_review_active)
        self.assertEqual(record['moments'], [])

    def test_legacy_save_has_no_invented_baseline(self):
        record=self.finish(); self.assertTrue(record['partial']); self.assertIsNone(record['start'])
        self.assertEqual(self.call('lc_review_delta_rows','ch01_d1','full'), [])

    def test_modes_hide_numbers_and_internal_traits(self):
        self.begin(); self.store.relationship_stats['love']+=4; self.store.partner_stats['secrecy']+=7; self.finish()
        self.assertEqual(self.call('lc_review_delta_rows','ch01_d1','normal'), [])
        self.assertEqual(self.call('lc_review_delta_rows','ch01_d1','insight'), [('love','Increased')])
        self.assertIn(('secrecy','5 → 12 (+7)'), self.call('lc_review_delta_rows','ch01_d1','full'))

    def test_choice_deltas_are_actual_not_nominal(self):
        self.store.relationship_stats['trust']=99; self.begin(); before=self.call('lc_review_stats')
        self.store.relationship_stats['trust']=100
        self.call('lc_review_note_choice','ch01_test', before)
        self.assertEqual(self.store.lc_review_days['ch01_d1']['choices'][0]['deltas'], [('relationship','trust',1)])

    def test_direct_changes_in_day_total_not_fabricated_as_choice(self):
        self.begin(); self.store.player_stats['acceptance']=60; self.finish()
        self.assertEqual(self.call('lc_review_choice_rows','ch01_d1'), [])
        self.assertIn(('acceptance','10 → 60 (+50)'), self.call('lc_review_delta_rows','ch01_d1','full'))

    def test_route_label_never_proves_betrayal(self):
        for route in ('ntr_confirmed','ntr','ntr_seeded','ntr_unresolved'):
            self.assertEqual(self.call('lc_character_titles',route=route,style='genre'), ('Uneasy Observer','Growing Distant'))

    def test_explicit_facts_gate_genre_titles(self):
        self.call('lc_title_fact','betrayal_known')
        self.assertEqual(self.call('lc_character_titles',style='genre')[0], 'Cuckold')
        self.call('lc_title_fact','humiliation_agreed')
        self.assertEqual(self.call('lc_character_titles',style='genre')[0], 'Beta Cuck')
        self.call('lc_title_fact','repair_chosen')
        self.assertEqual(self.call('lc_character_titles',style='genre')[0], 'Rebuilding Trust')

    def test_sharing_requires_agreement_and_event(self):
        self.call('lc_title_fact','sharing_happened')
        self.assertNotEqual(self.call('lc_character_titles',style='genre')[0], 'Stag')
        self.call('lc_title_fact','sharing_agreed')
        self.assertEqual(self.call('lc_character_titles',style='genre'), ('Stag','Shared Girlfriend'))
        self.call('lc_title_fact','married')
        self.assertEqual(self.call('lc_character_titles',style='genre')[1], 'Hotwife')

    def test_old_review_titles_do_not_use_future_facts(self):
        self.begin(); self.finish(); self.call('lc_title_fact','betrayal_known'); self.store.persistent.lc_title_style='genre'
        self.assertNotEqual(self.call('lc_review_titles','ch01_d1')[0], 'Cuckold')

    def test_off_and_reset(self):
        self.begin(); self.finish(); self.call('lc_title_fact','betrayal_known')
        self.assertEqual(self.call('lc_character_titles',style='off'), ('',''))
        self.call('lc_review_reset'); self.assertEqual(self.store.lc_review_days,{}); self.assertEqual(self.store.lc_title_facts,{})

    def test_records_can_be_copied_without_mutating_earlier_snapshot(self):
        self.begin(); snapshot=copy.deepcopy(self.store.lc_review_days)
        self.call('lc_review_record_image','cg test_0_blue'); self.finish()
        self.assertEqual(copy.deepcopy(self.store.lc_review_days),self.store.lc_review_days)
        self.store.lc_review_days=snapshot; self.store.lc_review_active='ch01_d1'
        self.assertEqual(self.call('lc_review_cards','ch01_d1'),[])

    def test_show_wrapper_delegates_and_ignores_other_layers(self):
        self.begin(); self.config.show(('cg','test_0_blue'), layer='screens')
        self.assertEqual(len(self.shown),1); self.assertEqual(self.call('lc_review_cards','ch01_d1'),[])
        self.config.show(('cg','test_0_blue'), layer='master')
        self.assertEqual(len(self.call('lc_review_cards','ch01_d1')),1)

    def test_all_five_days_have_entry_and_exit_hooks(self):
        text='\n'.join(p.read_text() for p in (ROOT/'game/chapters/ch01').glob('*.rpy'))
        for day in range(1,6):
            self.assertEqual(text.count('lc_review_begin("ch01_d%d")'%day),1)
            self.assertEqual(text.count('call lc_day_review("ch01_d%d")'%day),1)

    def test_future_day_reuses_engine_with_only_registry_and_gallery_data(self):
        self.env['LC_REVIEW_DAYS']['ch01_d6'] = {'label': 'Day Six', 'route_key': 'ch01_d6_end_route'}
        self.gallery['day6'] = dict(id='day6', tab='ch01_d6', title='Day Six moment', dream=False,
            pages=[{'image': 'day6_photo'}])
        self.call('lc_review_begin', 'ch01_d6')
        self.call('lc_review_record_image', 'cg day6_photo')
        self.values['ch01_d6_end_route'] = 'love'
        self.call('lc_review_finish', 'ch01_d6')
        self.assertEqual(self.call('lc_review_latest'), 'ch01_d6')
        self.assertEqual(self.call('lc_review_cards', 'ch01_d6')[0]['image'], 'day6_photo')
        self.assertEqual(self.store.lc_review_days['ch01_d6']['route'], 'love')

    def test_dream_summary_has_no_effects_and_waking_menu_is_shared(self):
        text=(ROOT/'game/chapters/ch01/ch01_scenes_14_30.rpy').read_text()
        summary=text.split('if lc_dream_presentation == "summary":',1)[1].split('    else:',1)[0]
        self.assertNotIn('apply_choice',summary); self.assertNotIn('scene cg',summary)
        for cid in ('ch01_dream_ground','ch01_dream_curiosity','ch01_dream_withdraw'):
            self.assertEqual(text.count('apply_choice("'+cid+'")'),1)
        self.assertLess(text.index('if lc_dream_presentation == "summary":'),text.index('    "My eyes opened."'))

if __name__ == '__main__': unittest.main()
