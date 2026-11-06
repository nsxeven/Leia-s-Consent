"""Choice-style review tags and moment stickers (production init, engine stubbed)."""
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


class ReviewTagTests(unittest.TestCase):
    def setUp(self):
        self.store = SimpleNamespace(
            relationship_stats=dict(love=50, trust=50, boredom=10, momentum=0),
            partner_stats=dict(curiosity=20, temptation=10, exhibitionism=10, boundary_looseness=10, secrecy=5),
            player_stats=dict(jealousy=20, acceptance=10), lc_review_active=None,
            lc_review_days={}, lc_title_facts={}, modified_save=False,
            persistent=SimpleNamespace(lc_title_style='story', lc_title_badges=False))
        self.config = SimpleNamespace(show=lambda *a, **kw: None, gamedir=str(ROOT / 'game'))
        self.env = dict(store=self.store, persistent=self.store.persistent, config=self.config,
            renpy=SimpleNamespace(showing=lambda tag: False, show_screen=lambda *a, **kw: None),
            get_stat_group=lambda group: getattr(self.store, group + '_stats'),
            get_story_value=lambda key, default=None: default,
            GALLERY_ENTRIES={}, STAT_LABELS={})
        source = (ROOT / 'game/systems/day_review.rpy').read_text()
        init = source.split('init 20 python:\n', 1)[1].split('\nlabel lc_day_review', 1)[0]
        exec(compile(textwrap.dedent(init), 'day_review_init', 'exec'), self.env)

    def call(self, name, *a, **kw):
        return self.env[name](*a, **kw)

    def play(self, *ids):
        self.call('lc_review_begin', 'ch01_d1')
        for cid in ids:
            self.call('lc_review_note_choice', cid, self.call('lc_review_stats'))
        self.call('lc_review_finish', 'ch01_d1')

    def test_every_day1_choice_is_mapped(self):
        import re
        src = ''.join((ROOT / 'game' / 'chapters' / 'ch01' / f).read_text(encoding='utf-8')
                      for f in ('ch01_main.rpy', 'ch01_scenes_04_06.rpy', 'ch01_scenes_07_13.rpy', 'ch01_scenes_14_30.rpy'))
        ids = set(re.findall(r'format_choice\("(ch01_[a-z0-9_]+)"', src))
        missing = sorted(i for i in ids if i not in self.env['LC_CHOICE_STYLE'])
        self.assertEqual(missing, [])

    def test_protective_run_gets_bodyguard(self):
        self.play('ch01_outfit_conservative', 'ch01_towel_boundary', 'ch01_watch_claim', 'ch01_photo_support')
        self.assertEqual(self.call('lc_review_titles', 'ch01_d1'), ('Her Bodyguard', 'Feeling Safe'))

    def test_tie_is_mixed(self):
        self.play('ch01_outfit_conservative', 'ch01_towel_boundary', 'ch01_photo_more', 'ch01_stranger_proud')
        self.assertEqual(self.call('lc_review_titles', 'ch01_d1'), ('Still Figuring It Out', 'Keeping Her Options Open'))

    def test_no_mapped_choices_keeps_route_titles(self):
        self.play()
        self.assertEqual(self.call('lc_review_titles', 'ch01_d1'), ('Curious Partner', 'Affectionate Partner'))

    def test_story_fact_overrides_style(self):
        self.call('lc_review_begin', 'ch01_d1')
        for cid in ('ch01_outfit_conservative', 'ch01_towel_boundary', 'ch01_watch_claim'):
            self.call('lc_review_note_choice', cid, self.call('lc_review_stats'))
        self.call('lc_title_fact', 'betrayal_known')
        self.call('lc_review_finish', 'ch01_d1')
        self.assertEqual(self.call('lc_review_titles', 'ch01_d1')[0], 'Betrayed Boyfriend')

    def test_off_hides_tags_and_stickers(self):
        self.play('ch01_towel_honest', 'ch01_towel_boundary', 'ch01_watch_claim')
        self.store.persistent.lc_title_style = 'off'
        self.assertEqual(self.call('lc_review_titles', 'ch01_d1'), ('', ''))
        self.assertEqual(self.call('lc_review_stickers', 'ch01_d1'), [])

    def test_stickers_priority_and_cap(self):
        self.store.ch01_grab_promised_to_ask = True
        self.play('ch01_towel_honest', 'ch01_carry_fix', 'ch01_watch_claim')
        self.assertEqual(self.call('lc_review_stickers', 'ch01_d1'), ['Asked First', 'Told the Truth'])

    def test_missed_it_needs_two_phone_choices(self):
        self.play('ch01_noblanket_phone')
        self.assertNotIn('Missed It', self.call('lc_review_stickers', 'ch01_d1'))
        self.store.lc_review_days = {}
        self.play('ch01_noblanket_phone', 'ch01_watch_ignore')
        self.assertIn('Missed It', self.call('lc_review_stickers', 'ch01_d1'))


if __name__ == '__main__':
    unittest.main()
