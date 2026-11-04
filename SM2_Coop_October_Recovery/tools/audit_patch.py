#!/usr/bin/env python3
"""Read-only audit of an already-existing PCSX2 Spider-Man 2 PNACH file."""
import pathlib, sys, re, hashlib
if len(sys.argv)!=2:
 print('Usage: python audit_patch.py PATH_TO_PNACH');sys.exit(2)
p=pathlib.Path(sys.argv[1]); raw=p.read_bytes(); text=raw.decode('utf-8',errors='replace')
entries={}
for line in text.splitlines():
 m=re.match(r'^\s*patch\s*=\s*1\s*,\s*EE\s*,\s*([0-9a-fA-F]{8})\s*,\s*word\s*,\s*([0-9a-fA-F]{8})',line,re.I)
 if m: entries.setdefault(int(m.group(1),16),[]).append(int(m.group(2),16))
print('File:',p,'\nSHA256:',hashlib.sha256(raw).hexdigest())
print('Patch entries:',sum(len(v) for v in entries.values()))
print('v8 factory dispatcher (0x000FD800):', 'present' if 0xFD800 in entries else 'not found')
selector=entries.get(0xFDA00,[])
print('Factory class selector 0x000FDA00:', ', '.join(f'{v:08X}' for v in selector) if selector else 'not found')
print('v8.1 selector fix:', 'present' if 0x00677220 in selector else 'not found')
print('Old v8 wrong selector:', 'present' if 0x00677230 in selector else 'not found')
print('One-shot request stub (0x000FF114):', 'present' if 0xFF114 in entries else 'not found (may be used as runtime data)')
print('WARNING: Inspection only. This does not verify game behavior or safe patches.')
