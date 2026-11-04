"""Patch one verified selector line in an existing v8 .pnach. Reversible, with backup."""
from pathlib import Path
import sys,os,shutil,tempfile,datetime
NAME='SLUS-20776_E2DFCE12.pnach'
A='// === SM2 EXPERIMENTAL SECOND SPIDERMAN V8 START ==='
B='// === SM2 EXPERIMENTAL SECOND SPIDERMAN V8 END ==='
OLD='patch=1,EE,000FDA00,word,00677230'
NEW='patch=1,EE,000FDA00,word,00677220'

def edit(folder, undo=False):
    path=Path(folder)/NAME
    if not path.is_file(): raise ValueError(f'Expected {NAME} in selected folder. No changes made.')
    src=path.read_text(encoding='utf-8-sig')
    if src.count(A)!=1 or src.count(B)!=1: raise ValueError('The v8 patch block was not found exactly once. No changes made.')
    a=src.index(A);b=src.index(B,a)+len(B)
    inside=src[a:b]
    frm,to=(NEW,OLD) if undo else (OLD,NEW)
    if inside.count(frm)!=1 or inside.count(to)!=0:
        raise ValueError('The v8 selector has unexpected content, or is already in the requested state. No changes made.')
    # Preserve every other cheat and line without modification.
    result=src[:a]+inside.replace(frm,to,1)+src[b:]
    backup=path.with_name(path.name+'.before_v8_1_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    shutil.copy2(path,backup)
    with tempfile.NamedTemporaryFile(dir=path.parent,mode='w',encoding='utf-8',prefix='.sm2-v81-',delete=False) as fp:
        temp=Path(fp.name)
        fp.write(result)
    try:os.replace(temp,path)
    finally:
        if temp.exists():temp.unlink()
    return backup

def main():
    import tkinter as tk
    from tkinter import filedialog,messagebox
    root=tk.Tk();root.withdraw()
    folder=filedialog.askdirectory(title='Select PCSX2 cheats folder containing v8 patch')
    if not folder:return
    try:
        undo='--undo' in sys.argv
        saved=edit(folder,undo)
        messagebox.showinfo('SM2 Second Spider-Man v8.1',('Selector fix reverted to v8.' if undo else 'v8.1 class selector correction installed.')+'\nBackup saved:\n'+str(saved)+'\nClose PCSX2 completely and restart before testing.')
    except Exception as ex: messagebox.showerror('No changes made',str(ex))
    root.destroy()
if __name__=='__main__':main()
