"""One-shot experimental factory call via existing P2 input bridge. Not real multiplayer."""
import time,threading,tkinter as tk
from tkinter import ttk,messagebox
from pine_client import Pine,PineError,verify
P2REQ=0x000FF114;P2RES=0x000FF118;P2STAGE=0x000FF11C
DISPATCH_WORD=0x0C03F600
HERO=0x00B305A0

def spawn():
    p=Pine(timeout=2)
    try:
        verify(p)
        if p.read32(0x000FF054)!=DISPATCH_WORD:raise PineError('v8 dispatch is NOT installed. Enable v8 cheat and restart PCSX2.')
        if p.read32(0x000FD800)!=0x27BDFF80 or p.read32(0x000FDA00)!=0x00677230:raise PineError('v8 code/data mismatch; do not trigger.')
        if p.read32(HERO+0x10)!=0x00646D20 or p.read32(HERO+0x14)!=0x39 or not p.read32(HERO):
            raise PineError('Spider-Man actor not found at the known address for this save; test aborted.')
        p.write32(P2REQ,0);p.write32(P2STAGE,0);p.write32(P2RES,0)
        p.write32(P2REQ,1)
        end=time.monotonic()+7
        stage=0
        while time.monotonic()<end:
            time.sleep(.12)
            stage=p.read32(P2STAGE)
            if stage in (3,0xFFFFFFFE,0xFFFFFFFD):break
        if stage==3:
            obj=p.read32(P2RES)
            if obj==HERO:return 'Factory returned Player 1 pointer again — no second actor confirmed.'
            if not (0x00100000 <= obj <= 0x01FFF800):return f'Factory returned 0x{obj:08X} outside expected RAM object range. No visible P2 confirmed.'
            try:vt=p.read32(obj+0x10);kind=p.read32(obj+0x14)
            except PineError:return f'Factory returned 0x{obj:08X} but actor fields could not be read.'
            if kind==0x39 and vt==0x00646D20:return f'New SPIDERMANX object at 0x{obj:08X} (different from Player 1)! Look around in game. Rendering and gameplay are NOT yet verified.'
            return f'Factory returned 0x{obj:08X}, type 0x{kind:X}, vtable 0x{vt:08X}. Second Spider-Man not confirmed.'
        if stage==0xFFFFFFFE:return 'Game rejected the attempt: Player 1 actor validation failed.'
        if stage==0xFFFFFFFD:return 'Game factory returned no object. No second Spider-Man.'
        if stage==2:return 'Game reached the factory but did not finish. If frozen, disable v8 and restart PCSX2.'
        return f'No factory completion reported (stage {stage}). Check game; disable v8 if unstable.'
    finally:p.close()

class Window:
    def __init__(self):
        self.root=tk.Tk();self.root.title('Spider-Man 2 (PS2) — TRY SECOND SPIDER-MAN v8');self.root.geometry('635x315')
        wrap=ttk.Frame(self.root,padding=18);wrap.pack(fill='both',expand=True)
        ttk.Label(wrap,text='SECOND SPIDER-MAN — IN-GAME FACTORY TEST',font=('Segoe UI',15,'bold')).pack(anchor='w',pady=(0,10))
        ttk.Label(wrap,text='This actually invokes the SPIDERMANX game factory ONCE. Experimental: can crash; a returned actor might not be visible. Back up your save first.',wraplength=565).pack(anchor='w')
        self.btn=ttk.Button(wrap,text='TRY CREATE SECOND SPIDER-MAN',command=self.go);self.btn.pack(pady=17)
        self.status=tk.StringVar(value='Start free roam in PCSX2, then press the button. Do not save progress during this test.')
        ttk.Label(wrap,textvariable=self.status,wraplength=580).pack(anchor='w',pady=8)
        ttk.Label(wrap,text='Your v6 Player 2 input bridge remains installed, but is not yet connected to any new actor.',wraplength=565).pack(anchor='w',pady=6)
    def go(self):
        if not messagebox.askyesno('Experimental in-game creation','This can freeze or crash PCSX2 and might create no visible character. Have you backed up your save and started free roam?'):return
        self.btn.config(state='disabled');self.status.set('Sending one-time SPIDERMANX factory request...')
        def worker():
            try:result=spawn()
            except Exception as exc:result='Test failed: '+str(exc)
            self.root.after(0,lambda:self.done(result))
        threading.Thread(target=worker,daemon=True).start()
    def done(self,result):self.status.set(result);self.btn.config(state='normal')
    def run(self):self.root.mainloop()
if __name__=='__main__':Window().run()
