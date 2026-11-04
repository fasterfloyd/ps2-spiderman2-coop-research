"""PCSX2 PINE IPC: local only. Stdlib; no installs. IPC spec commands: 0x02 read32, 0x06 write32."""
import socket, struct
HOST='127.0.0.1'; PORT=28011

class PineError(Exception):
    pass

class Pine:
    def __init__(self,port=PORT,timeout=2):
        self.s=socket.create_connection((HOST,int(port)),timeout)
        self.s.settimeout(timeout)
    def close(self):
        self.s.close()
    def read_exact(self,n):
        d=bytearray()
        while len(d)<n:
            x=self.s.recv(n-len(d))
            if not x:raise PineError('PCSX2 disconnected')
            d.extend(x)
        return bytes(d)
    def transact(self,commands):
        data=b''.join(commands)
        self.s.sendall(struct.pack('<I',len(data)+4)+data)
        length=struct.unpack('<I',self.read_exact(4))[0]
        if length<5 or length>256000:raise PineError('Invalid IPC reply length')
        payload=self.read_exact(length-4)
        if payload[0]!=0:raise PineError('PCSX2 rejected memory request (game not running?)')
        return payload[1:]
    def read32(self,address):
        d=self.transact([b'\x02'+struct.pack('<I',address)])
        if len(d)!=4:raise PineError('Unexpected read32 reply')
        return struct.unpack('<I',d)[0]
    def write32(self,address,value):
        d=self.transact([b'\x06'+struct.pack('<II',address,value&0xffffffff)])
        if d:raise PineError('Unexpected write32 reply')
    def string(self,op):
        d=self.transact([bytes([op])])
        if len(d)<4:raise PineError('Unexpected string reply')
        length=struct.unpack_from('<I',d)[0]
        if len(d)!=4+length:raise PineError('Unexpected string size')
        return d[4:].rstrip(b'\x00').decode('utf-8','replace')

HOOK=0x00519234; STUB=0x000FF000; FRAME=0x000FF100
P2_ENABLE=0x000FF104; P2_MASK=0x000FF108
P2_ACK=0x000FF10C; P2_ECHO=0x000FF110
EXPECTED_JAL=0x0C03FC00; EXPECTED_STUB=0x27BDFFD0

def verify(p):
    serial=p.string(0x0C)
    if not serial.upper().startswith('SLUS-20776'):
        raise PineError('Wrong game: '+serial+'; need Spider-Man 2 2004 USA SLUS-20776')
    hook=p.read32(HOOK);stub=p.read32(STUB)
    if hook!=EXPECTED_JAL or stub!=EXPECTED_STUB:
        raise PineError('v6 patch not active; check PCSX2 Cheats and restart. Hook=%08X Stub=%08X'%(hook,stub))
    # check a v6-specific instruction so v1 is not misidentified as v6
    if p.read32(STUB+0x2C)!=0x11200006:
        raise PineError('v1 or another patch detected; v6 input bridge code not active')
    return serial
