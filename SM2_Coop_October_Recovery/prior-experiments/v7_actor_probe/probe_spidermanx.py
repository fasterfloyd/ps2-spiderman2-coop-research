"""Read-only SPIDERMANX actor probe. Does not spawn actors or write memory."""
import json,struct,time,datetime,sys,traceback
from pathlib import Path
from pine_client import Pine,PineError,verify,P2_ENABLE,P2_MASK,P2_ACK

GAME='SLUS-20776'
HERO=0x00B305A0
HERO_SIZE=0x7D8
TYPE=0x39
VTABLE=0x00646D20
OUTPUT=Path(__file__).resolve().parent/'P2_ACTOR_PROBE_V7.json'

def reads(p, addrs):
    """Batch PINE read32 commands; never issues writes."""
    out=[]
    for i in range(0,len(addrs),96):
        chunk=addrs[i:i+96]
        resp=p.transact([b'\x02'+struct.pack('<I',a) for a in chunk])
        if len(resp)!=4*len(chunk):raise PineError('Read32 batch length mismatch')
        out.extend(struct.unpack('<'+'I'*len(chunk),resp))
    return out

def read_actor(p):
    words=reads(p,[HERO+i for i in range(0,HERO_SIZE,4)])
    data=struct.pack('<'+'I'*len(words),*words)
    vtbl,cls=words[4],words[5]
    name=data[0x20:0x30].split(b'\0')[0].decode('ascii','replace')
    if (vtbl,cls,name)!=(VTABLE,TYPE,'SPIDERMANX'):
        raise PineError('Live hero object not found at 0x%08X (vtable %08X, class %X, name %r). No changes made.'%(HERO,vtbl,cls,name))
    return data

def analyze(samples):
    if len(samples)<2:return []
    out=[]
    for off in range(0,HERO_SIZE-8,4):
        triples=[[struct.unpack_from('<f',s,off+i)[0] for i in (0,4,8)] for s in samples]
        if any(not all(-200000.0<x<200000.0 and x==x for x in row) for row in triples):continue
        ranges=[max(row[i] for row in triples)-min(row[i] for row in triples) for i in range(3)]
        changed=sum(r>0.015 for r in ranges)
        # Geometric candidates only, not proof of world coordinates
        if changed>=2:
            out.append({'offset':'0x%03X'%off,'ranges':[round(v,4) for v in ranges],
                        'start':[round(v,3) for v in triples[0]],'end':[round(v,3) for v in triples[-1]]})
    return sorted(out,key=lambda x:sum(min(abs(v),1000) for v in x['ranges']),reverse=True)[:40]

def main():
    print('Spider-Man 2 PS2 — PLAYER 2 Actor Probe v7 (READ ONLY)')
    print('This discovers Player 1 actor state; it does NOT add a second Spider-Man.')
    p=None
    try:
        p=Pine(timeout=5)
        serial=verify(p)
        base=read_actor(p)
        ack=p.read32(P2_ACK)
        print('GAME: %s | v6 hook active'%serial)
        print('LIVE HERO: 0x%08X, class 0x%X, SPIDERMANX verified'%(HERO,TYPE))
        print('Move PLAYER 1 around in the game for 10 seconds. The tool records his actor state.')
        samples=[base]; times=[0.0]
        start=time.monotonic()
        for i in range(1,11):
            time.sleep(max(0,start+i-(time.monotonic())))
            samples.append(read_actor(p));times.append(round(time.monotonic()-start,2))
            print('Captured %d/10'%i,flush=True)
        changed=[{'offset':'0x%03X'%off,'before':'0x%08X'%struct.unpack_from('<I',samples[0],off)[0],
                 'after':'0x%08X'%struct.unpack_from('<I',samples[-1],off)[0]}
                 for off in range(0,HERO_SIZE,4) if len({s[off:off+4] for s in samples})>1]
        report={
          'game':serial,'date':datetime.datetime.now().astimezone().isoformat(),
          'experiment':'v7 read-only SPIDERMANX actor identification; not multiplayer',
          'actor_address':'0x%08X'%HERO,'class_id':'0x%02X'%TYPE,'vtable':'0x%08X'%VTABLE,
          'name':'SPIDERMANX','object_size_from_factory':'0x7D8',
          'factory_allocation_call':'0x004CDDBC','constructor_call':'0x004CDDD0',
          'constructor':'0x002B9044',
          'p2_enabled':p.read32(P2_ENABLE),'p2_input_mask':p.read32(P2_MASK),
          'p2_ack_delta':(p.read32(P2_ACK)-ack)&0xffffffff,
          'sample_times_seconds':times,'changed_word_count':len(changed),
          'changed_words':changed[:160],
          'candidate_float_triplets_not_confirmed_positions':analyze(samples),
          'limitations':['Cannot instantiate a second Spider-Man','Cannot move or render Player 2',
              'Candidate float triplets are not verified player position coordinates',
              'Actor pointer is verified only for supplied savestates and must be checked in each running game']}
        OUTPUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
        print('SUCCESS. Saved',OUTPUT.name)
        print('Changed actor words:',len(changed),'| Candidate 3-float groups:',len(report['candidate_float_triplets_not_confirmed_positions']))
        print('Player 2 input bridge is unchanged. Upload the JSON for analysis.')
    except (OSError,PineError,ValueError) as exc:
        print('CHECK FAILED:',exc)
        print('Game and v6 hook must be running. No memory was modified.')
        raise SystemExit(1)
    finally:
        if p:p.close()
if __name__=='__main__':
    main()
