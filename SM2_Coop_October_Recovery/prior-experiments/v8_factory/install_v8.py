"""Apply/remove a reversible one-shot SPIDERMANX factory experiment on top of v6."""
from pathlib import Path
import datetime, shutil, tempfile, os, sys
HERE=Path(__file__).resolve().parent
FILENAME='SLUS-20776_E2DFCE12.pnach'
V6_A='// === SM2 PLAYER2 INPUT BRIDGE V6 START ==='
V6_B='// === SM2 PLAYER2 INPUT BRIDGE V6 END ==='
V8_A='// === SM2 EXPERIMENTAL SECOND SPIDERMAN V8 START ==='
V8_B='// === SM2 EXPERIMENTAL SECOND SPIDERMAN V8 END ==='
OLD='patch=1,EE,000FF054,word,0C149456'
NEW='patch=1,EE,000FF054,word,0C03F600'
START=0x000FD800;STOP=0x000FD8CC

def edit(folder,remove=False):
    target=Path(folder)/FILENAME
    if not target.exists():raise ValueError('No '+FILENAME+'. Install and verify v6 first.')
    before=target.read_text('utf-8-sig')
    if before.count(V6_A)!=1 or before.count(V6_B)!=1:raise ValueError('Known v6 block not found, or duplicate markers. No changes made.')
    if before.count(V8_A)!=before.count(V8_B) or before.count(V8_A)>1:raise ValueError('Broken or duplicate v8 block. No changes made.')
    va=before.index(V6_A);vb=before.index(V6_B,va)
    v6=before[va:vb]
    if remove:
        if V8_A not in before:raise ValueError('v8 is not installed.')
        if v6.count(NEW)!=1:raise ValueError('v8 modified hook missing. Manual review needed; untouched.')
        out=before[:va]+v6.replace(NEW,OLD,1)+before[vb:]
        a=out.index(V8_A);b=out.index(V8_B,a)+len(V8_B)
        out=out[:a]+out[b:]
    else:
        if V8_A in before:raise ValueError('v8 already installed, just use SHOW_SECOND_SPIDERMAN.bat.')
        if v6.count(OLD)!=1:raise ValueError('v6 dispatch instruction differs from expected. No changes made.')
        # Refuse unowned patches at overlapping scratch addresses.
        reserved=set(range(START,STOP,4))|{0x000FDA00,0x000FF054,0x000FF114,0x000FF118,0x000FF11C}
        for raw in before[:va].splitlines()+before[vb:].splitlines():
            if not raw.strip().lower().startswith('patch='):continue
            fields=[s.strip() for s in raw.split(',')]
            if len(fields)<3:continue
            try:addr=int(fields[2],16)
            except ValueError:continue
            if addr in reserved:raise ValueError(f'Another mod already patches 0x{addr:08X}. Uninstall that mod first.')
        out=before[:va]+v6.replace(OLD,NEW,1)+before[vb:]
        out=out.rstrip()+'\n\n'+V8_A+'\n'+(HERE/'V8_ADDITIONAL_PATCH.txt').read_text().strip()+'\n'+V8_B+'\n'
    backup=target.with_name(target.name+'.before_v8_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    shutil.copy2(target,backup)
    with tempfile.NamedTemporaryFile(dir=target.parent,mode='w',encoding='utf-8',prefix='.v8-',delete=False) as f:
        temp=Path(f.name);f.write(out)
    try:os.replace(temp,target)
    finally:
        if temp.exists():temp.unlink()
    return backup

def cli():
    import tkinter as tk
    from tkinter import filedialog,messagebox
    root=tk.Tk();root.withdraw()
    folder=filedialog.askdirectory(title='Choose your PCSX2 cheats folder (v6 must already be installed)')
    if folder:
        try:
            remove='--remove' in sys.argv
            backup=edit(folder,remove)
            messagebox.showinfo('SM2 P2 v8',('Removed experimental v8.' if remove else 'Experimental v8 installed.')+'\nBackup: '+str(backup)+'\nFully close and restart PCSX2 before testing.')
        except Exception as e:messagebox.showerror('SM2 P2 v8: no changes made',str(e))
    root.destroy()
if __name__=='__main__':cli()
