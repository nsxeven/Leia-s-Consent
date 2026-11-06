"""Tag collection: unlock on finished days, equip per slot, equipped tags shown everywhere."""
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


class TagCollectionTests(unittest.TestCase):
    def setUp(self):
        self.persistent = SimpleNamespace(lc_title_style='story', lc_title_badges=False,
                                          lc_tags_earned=set(), lc_stickers_earned=set(), lc_tag_equipped={})
        self.store = SimpleNamespace(
            relationship_stats=dict(love=50, trust=50, boredom=10, momentum=0),
            partner_stats=dict(curiosity=20, temptation=10, exhibitionism=10, boundary_looseness=10, secrecy=5),
            player_stats=dict(jealousy=20, acceptance=10), lc_review_active=None,
            lc_review_days={}, lc_title_facts={}, modified_save=False, persistent=self.persistent)
        self.env = dict(store=self.store, persistent=self.persistent,
            config=SimpleNamespace(show=lambda *a, **kw: None, gamedir=str(ROOT / 'game')),
            renpy=SimpleNamespace(showing=lambda tag: False, show_screen=lambda *a, **kw: None,
                                  restart_interaction=lambda: None),
            get_stat_group=lambda group: getattr(self.store, group + '_stats'),
            get_story_value=lambda key, default=None: default, GALLERY_ENTRIES={}, STAT_LABELS={})
        review = (ROOT / 'game/systems/day_review.rpy').read_text(encoding='utf-8')
        init = review.split('init 20 python:\n', 1)[1].split('\nlabel lc_day_review', 1)[0]
        exec(compile(textwrap.dedent(init), 'day_review_init', 'exec'), self.env)
        coll = (ROOT / 'game/systems/lc_tag_collection.rpy').read_text(encoding='utf-8')
        exec(compile(textwrap.dedent(coll.split('init 21 python:\n', 1)[1]), 'tags_init', 'exec'), self.env)

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def play(self, *ids):
        self.call('lc_review_begin', 'ch01_d1')
        for cid in ids:
            self.call('lc_review_note_choice', cid, self.call('lc_review_stats'))
        self.call('lc_review_finish', 'ch01_d1')

    def test_finish_unlocks_tags_and_stickers_permanently(self):
        self.play('ch01_outfit_conservative', 'ch01_towel_boundary', 'ch01_towel_honest')
        self.assertIn('ryan:Her Bodyguard', self.persistent.lc_tags_earned)
        self.assertIn('leia:Feeling Safe', self.persistent.lc_tags_earned)
        self.assertIn('Told the Truth', self.persistent.lc_stickers_earned)

    def test_equip_each_slot_separately(self):
        self.play('ch01_outfit_conservative', 'ch01_towel_boundary')
        self.persistent.lc_tags_earned |= {'leia:Blushing Again'}
        self.call('lc_tag_equip', 'leia', 'Blushing Again')
        self.assertEqual(self.call('lc_review_titles', 'ch01_d1'), ('Her Bodyguard', 'Blushing Again'))
        self.assertEqual(self.call('lc_current_titles'), ('Her Bodyguard', 'Blushing Again'))
        self.call('lc_tag_equip', 'leia', None)
        self.assertEqual(self.call('lc_current_titles'), ('Her Bodyguard', 'Feeling Safe'))

    def test_cannot_equip_locked_tag(self):
        self.play('ch01_outfit_conservative', 'ch01_towel_boundary')
        self.call('lc_tag_equip', 'ryan', 'Open Book')
        self.assertIsNone(self.call('lc_tag_equipped', 'ryan'))

    def test_title_style_off_still_hides(self):
        self.play('ch01_outfit_conservative', 'ch01_towel_boundary')
        self.call('lc_tag_equip', 'ryan', 'Her Bodyguard')
        self.persistent.lc_title_style = 'off'
        self.assertEqual(self.call('lc_review_titles', 'ch01_d1'), ('', ''))

    def test_catalog_lists_locked_entries(self):
        rows = self.call('lc_tag_list', 'ryan')
        self.assertIn(('Open Book', False), rows)
        self.assertEqual(len(self.call('lc_sticker_list')), 8)

    def test_menu_has_tags_next_to_status(self):
        ui = (ROOT / 'game/screens/zzzzzzzz_scrapbook_ui.rpy').read_text(encoding='utf-8')
        self.assertIn('rows.append(("STATUS", Show("status_screen"), False))\n            rows.append(("TAGS", Show("lc_tags_screen"), False))', ui)
        self.assertIn('screen lc_tags_screen():', (ROOT / 'game/screens/tag_collection_screen.rpy').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
