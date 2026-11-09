import unittest
from pathlib import Path
GAME=Path(__file__).resolve().parents[1]/"game"
class BreakfastCGs(unittest.TestCase):
 def test_assets_definitions_and_gallery(self):
  v=(GAME/"chapters/ch01/ch01_day2_visuals.rpy").read_text()
  g=(GAME/"systems/gallery_data.rpy").read_text()
  for n,f in [("01","Breakfast_01"),("02","Breakfast_02"),("03","Breakfast_03"),("04","Breakfast_04")]:
   self.assertIn("ch01_d2_breakfast_"+n,v); self.assertIn(f+".webp",v); self.assertTrue((GAME/f"images/cg/ch02/CH2D2_CG_{f}.webp").exists())
  self.assertIn("ch01_d2_breakfast_julian_pov",v); self.assertIn("BreakfastCloseup_01.webp",v)
  self.assertIn('mature=True',g)
 def test_sequence_and_reply_prompt(self):
  s=(GAME/"chapters/ch01/zzzz_ch01_day2_polish_revision.rpy").read_text()
  self.assertIn("call screen lc_breakfast_julian_pov",s); self.assertIn('phone_offer_reply("maya", "ch01_d2_maya_lunch_reply"',s)
  self.assertLess(s.index("ch01_d2_breakfast_02"),s.index("ch01_d2_maya_lunch_reply"))
 if __name__=='__main__': unittest.main()
