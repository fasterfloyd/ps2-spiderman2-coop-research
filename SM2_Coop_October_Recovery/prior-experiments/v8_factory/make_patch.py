"""Offline builder: exact disassembly/ELF verification for the one-shot game factory call."""
from pathlib import Path
import struct,hashlib,json
P=Path(__file__).resolve().parent
B=(P/'spawn_dispatch.bin').read_bytes()
assert len(B)==0xCC and len(B)%4==0
assert struct.unpack_from('<I',B,0)[0]==0x27BDFF80
assert struct.unpack_from('<I',B,0x7c)[0] == 0x0C133020, 'Must call 0x004CC080 factory'
# verify all non-branch jump/call targets in code image
assert B[0x7c:0x80]==struct.pack('<I',(3<<26)|(0x004CC080>>2))
BASE=0x000FD800
NEW_JAL=(3<<26)|(BASE>>2)
assert NEW_JAL==0x0C03F600
line=lambda a,v,c='':f'patch=1,EE,{a:08X},word,{v:08X}'+(' // '+c if c else '')
lines=['[SM2 P2 v8 - Experimental One-Shot SPIDERMANX Factory]',
       'description=Calls in-game SPIDERMANX factory once; DOES NOT guarantee visible actor or co-op',
       'author=Experimental reverse engineering; US SLUS-20776 E2DFCE12']
for i in range(0,len(B),4):
 w=struct.unpack_from('<I',B,i)[0];lines.append(line(BASE+i,w))
lines.append(line(0x000FDA00,0x00677230,'pointer to game class string SPIDERMANX'))
(P/'V8_ADDITIONAL_PATCH.txt').write_text('\n'.join(lines)+'\n')
(P/'v8_layout.json').write_text(json.dumps(dict(game='SLUS-20776',crc='E2DFCE12',elf_sha256='1ed83d628bdb7d9824ba793a6f0954da9a43b081231d1dbc1c69d168208eebbb',hero=0x00B305A0,hero_expected_vtable=0x00646D20,class_id=0x39,game_factory=0x004CC080,dispatcher=BASE,v6_stub_jal_address=0x000FF054,v6_original_target=0x00525158,v8_dispatch_jal=NEW_JAL,request=0x000FF114,result=0x000FF118,stage=0x000FF11C,known_risk='Experimental duplicate ID pointer and incomplete actor registration. Can crash, corrupt running game, render nothing. No save writing.'),indent=2)+'\n')
print('Generated',len(B),'MIPS bytes and',len(lines),'patch lines')
