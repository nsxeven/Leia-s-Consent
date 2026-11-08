"""Golden Hour glass menu contract: navigation, controls and preserved neighbors."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
UI = (GAME / 'screens/zzzzzzzz_scrapbook_ui.rpy').read_text(encoding='utf-8')
GALLERY = (GAME / 'screens/gallery_screen.rpy').read_text(encoding='utf-8')
STATUS = (GAME / 'screens/status_screen.rpy').read_text(encoding='utf-8')
TAGS = (GAME / 'screens/tag_collection_screen.rpy').read_text(encoding='utf-8')


def screen(src, name):
    return src.split('screen '+name+'(', 1)[1].split('\nscreen ', 1)[0]


class GoldenHourMenuTests(unittest.TestCase):
    def test_left_rail_and_live_scene(self):
        shell = screen(UI, 'lc_glass_menu_backdrop')
        self.assertIn('add Solid("#101521b8")', shell)
        self.assertIn('if main_menu:', shell)
        self.assertIn('add lc_title_bg_now()', shell)
        self.assertIn('use lc_journal_tabs(48)', shell)
        self.assertIn('xpos 354', screen(UI, 'game_menu'))
        tabs = screen(UI, 'lc_journal_tabs')
        self.assertIn('xpos xpos', tabs)
        self.assertIn('gui/glass/nav_active.png', tabs)
        for label in ('SAVE', 'LOAD', 'PREFS', 'HISTORY', 'GALLERY', 'STATUS', 'TAGS', 'MAIN MENU', 'QUIT'):
            self.assertIn('"'+label+'"', UI.split('def lc_journal_tab_rows():', 1)[1].split('\ninit ',1)[0])
        self.assertIn('ShowMenu("lc_tags_screen")', UI)

    def test_each_page_uses_glass_shell(self):
        for name in ('preferences','file_slots','history'):
            self.assertIn('use game_menu(', screen(UI,name))
        for src,name in ((GALLERY,'gallery_screen'),(STATUS,'status_screen'),(TAGS,'lc_tags_screen')):
            self.assertIn('use lc_glass_menu_backdrop()',screen(src,name))
            self.assertIn('gui/glass/panel.png',screen(src,name))
            self.assertNotIn('bg_game_menu.png',screen(src,name))

    def test_all_inventory_controls_survive(self):
        prefs = screen(UI,'preferences')
        for action in ('Preference("display", "window")','Preference("display", "fullscreen")',
                       'Preference("skip", "toggle")','Preference("after choices", "toggle")',
                       'InvertSelected(Preference("transitions", "toggle"))',
                       'ToggleField(persistent, "lc_screen_shake")','ToggleField(persistent, "lc_camera_flash")',
                       'Preference("text speed")','Preference("auto-forward time")',
                       'Preference("music volume")','Preference("sound volume")','Preference("voice volume")',
                       'Preference("mixer lewd volume")','Preference("all mute", "toggle")',
                       'set_choice_display_mode','lc_route_explorer_screen'):
            self.assertIn(action,prefs)
        self.assertIn('set_player_transparency_mode',screen(UI,'lc_info_card'))
        self.assertIn('FileAction(slot)', screen(UI,'file_slots'))
        self.assertIn('FileDelete(slot)', screen(UI,'file_slots'))
        self.assertIn('FilePagePrevious()', screen(UI,'file_slots'))
        self.assertIn('FilePageNext()', screen(UI,'file_slots'))

    def test_live_preview_and_real_sound_samples(self):
        prefs=screen(UI,'preferences')
        self.assertIn('slow_cps (preferences.text_cps if preferences.text_cps else None)',prefs)
        for kind in ('bgm','sfx','voice','lewd'):
            self.assertIn('"'+kind+'", ',prefs)  # sample id, then mixer (#151)
        sample = UI.split('def lc_glass_sound_test(kind):',1)[1].split('\ninit 999',1)[0]
        for name in ('glass_test','ice_clink','leia_laugh','wet01'):
            self.assertIn('"'+name+'"',sample)
        self.assertIn('mixer="music"',UI)
        self.assertIn('mixer="voice"',(GAME/'systems/lc_fx.rpy').read_text(encoding='utf-8'))
        self.assertTrue((GAME/'audio/music/glass_test.ogg').is_file())
        self.assertIn('action Function(lc_glass_sound_test, sample)',screen(UI,'lc_pref_slider'))

    def test_day_review_and_phone_not_restyled(self):
        # Phone navigation is intentionally edited independently of glass menus;
        # tests/test_phone_back_navigation.py guards its behavior.
        import subprocess
        changed=subprocess.check_output(['git','status','--short','--','game/screens/day_review_screen.rpy'],cwd=ROOT,text=True)
        self.assertEqual(changed.strip(),'')
        for name in ('panel','nav_idle','nav_active','bar_honey','bar_peach','bar_amber','bar_pink',
                     'slider_thumb','toggle_off','toggle_on','pill_honey','pill_peach','pill_pink',
                     'sound_test','sound_test_hover'):
            self.assertTrue((GAME/'gui/glass'/(name+'.png')).is_file(),name)


if __name__=='__main__':
    unittest.main()
