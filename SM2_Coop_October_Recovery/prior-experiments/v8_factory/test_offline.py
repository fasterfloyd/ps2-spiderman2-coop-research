from pathlib import Path
import tempfile,struct,unittest,importlib.util
from install_v8 import edit,V6_A,V6_B,V8_A,V8_B,OLD,NEW,FILENAME
P=Path(__file__).resolve().parent
class Test(unittest.TestCase):
 def test_code_and_factory_address(self):
  b=(P/'spawn_dispatch.bin').read_bytes()
  self.assertEqual(len(b),0xCC)
  self.assertEqual(struct.unpack_from('<I',b,0x7c)[0],0x0C133020)
  self.assertEqual(struct.unpack_from('<I',b,0)[0],0x27BDFF80)
 def test_install_uninstall(self):
  with tempfile.TemporaryDirectory() as t:
   f=Path(t)/FILENAME
   text='gametitle=Spider-Man 2\npatch=1,EE,00012340,word,11111111\n'+V6_A+'\n[Bridge]\n'+OLD+' // original game noop\n'+V6_B+'\n'
   f.write_text(text)
   backup=edit(t)
   update=f.read_text()
   self.assertTrue(backup.exists())
   self.assertEqual(update.count(NEW),1)
   self.assertNotIn(OLD,update)
   self.assertEqual(update.count(V8_A),1)
   self.assertIn('000FD800',update)
   self.assertIn('000FDA00',update)
   self.assertIn('00012340',update)
   with self.assertRaises(ValueError):edit(t)
   edit(t,remove=True)
   result=f.read_text()
   self.assertIn(OLD,result)
   self.assertNotIn(V8_A,result)
   self.assertIn('00012340',result)
 def test_reject_clashing_patches(self):
  with tempfile.TemporaryDirectory() as t:
   f=Path(t)/FILENAME
   initial=V6_A+'\n'+OLD+'\n'+V6_B+'\npatch=1,EE,000FD800,word,12345678\n'
   f.write_text(initial)
   with self.assertRaisesRegex(ValueError,'another|Another'):edit(t)
   self.assertEqual(f.read_text(),initial)
 def test_v6_code_still_valid(self):
  import json
  j=json.loads((P/'v8_layout.json').read_text())
  self.assertEqual(j['v8_dispatch_jal'],0x0C03F600)
  elf=Path('/mnt/data/SLUS_207.76').read_bytes()
  addr=0x004CC080
  off=addr-0x000FF000
  self.assertEqual(struct.unpack_from('<I',elf,off)[0],0x27BDFFD0)
if __name__=='__main__':unittest.main(verbosity=2)
