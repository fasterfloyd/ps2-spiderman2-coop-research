import unittest,tempfile,struct,subprocess,zipfile
from pathlib import Path
from FIX_V8_TO_V81 import edit,A,B,OLD,NEW,NAME
class Tests(unittest.TestCase):
 def test_pnach_exact_update_and_undo(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/NAME
   start='gametitle=Spider-Man 2\npatch=1,EE,00012340,word,11111111\n'+A+'\n'+OLD+'\n'+B+'\n'
   p.write_text(start)
   saved=edit(d)
   self.assertTrue(saved.exists());self.assertIn(NEW,p.read_text());self.assertNotIn(OLD,p.read_text())
   with self.assertRaises(ValueError):edit(d)
   edit(d,undo=True)
   self.assertEqual(start,p.read_text())
 def test_data_selector_static(self):
  elf=Path('/mnt/data/SLUS_207.76').read_bytes()
  f=lambda a: elf[a-0x100000+0x1000:a-0x100000+0x1000+24]
  self.assertTrue(f(0x00677220).startswith(b'spidermanx:'))
  self.assertTrue(f(0x00677230).startswith(b'SPIDERMANX'))
 def test_button_checks_new_selector(self):
  txt=(Path(__file__).parent/'second_spiderman_button.py').read_text()
  self.assertIn('0x000FDA00)!=0x00677220',txt)
  self.assertIn('0x0060A274)!=0x00677220',txt)
if __name__=='__main__':unittest.main(verbosity=2)
