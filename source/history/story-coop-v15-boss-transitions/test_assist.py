"""Temporary test-only damage thunk; no EXE, resources or save data are written."""
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
from pathlib import Path
import struct
import sys
from build_teleport import HERE,Ks,KS_ARCH_X86,KS_MODE_32

SITE=0x4ee3b0
ORIGINAL=bytes.fromhex('6aff687e876f00')
TABLE=json.loads((HERE/'enemy-whitelist.json').read_text())
ENEMIES=sorted({r['hash'] for r in TABLE['enemies'] if r['one_hit']})

def routine(asm,code,diag=0x7ff000,get_descriptor=0x406620,resume=SITE+7,replay=True):
    table=code+0x1000;counts=code+0x1800
    tail=f'push -1;push 0x6f877e;jmp {resume}' if replay else f'jmp {resume}'
    return asm(f'''pushfd;pushad
        cmp dword ptr [{diag+4}],5
        jne original
        mov eax,[esp+40]
        test eax,eax
        jz original
        mov esi,[eax+8]
        test esi,esi
        jz original
        mov edx,[{diag+36}]
        test edx,edx
        jz original
        cmp [esi+0x20],edx
        jne original
        cmp esi,[{diag+12}]
        je player
        cmp esi,[{diag+16}]
        je player
        mov eax,[esp+44]
        test eax,eax
        jle original
        cmp eax,0x7f800000
        jae original
        mov ecx,esi
        call {get_descriptor}
        test eax,eax
        jz original
        mov eax,[eax+0xc0]
        mov edi,{table}
        mov ecx,{len(ENEMIES)}
        search:
        cmp eax,[edi]
        je enemy
        add edi,4
        dec ecx
        jnz search
        inc dword ptr [{counts+8}]
        jmp original
        enemy:
        mov dword ptr [esp+44],0x49742400
        inc dword ptr [{counts+4}]
        jmp original
        player:
        inc dword ptr [{counts}]
        popad;popfd;ret 16
        original:
        popad;popfd
        {tail}''',code)

def install(pid,render_pose=False,*,expected_path=None,manifest_path=None,report_dir=None):
    if render_pose:
        raise RuntimeError('pose2 retained dangling stack packets; use the v16 disk build instead.')
    if (expected_path is None)!=(manifest_path is None):
        raise ValueError('An isolated executable and its exact build manifest are both required.')
    site=0x511460 if render_pose else SITE
    expected_entry=bytes.fromhex('e99bb72e0090') if render_pose else ORIGINAL
    length=len(expected_entry)
    k=C.WinDLL('kernel32',use_last_error=True);nt=C.WinDLL('ntdll')
    k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenProcess.restype=W.HANDLE
    k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
    k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
    k.WriteProcessMemory.argtypes=k.ReadProcessMemory.argtypes
    k.VirtualAllocEx.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,W.DWORD];k.VirtualAllocEx.restype=C.c_void_p
    k.VirtualProtectEx.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,C.POINTER(W.DWORD)]
    k.FlushInstructionCache.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t]
    k.CloseHandle.argtypes=[W.HANDLE]
    nt.NtSuspendProcess.argtypes=[W.HANDLE];nt.NtSuspendProcess.restype=W.LONG
    nt.NtResumeProcess.argtypes=[W.HANDLE];nt.NtResumeProcess.restype=W.LONG
    k.CreateToolhelp32Snapshot.argtypes=[W.DWORD,W.DWORD];k.CreateToolhelp32Snapshot.restype=W.HANDLE
    k.OpenThread.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenThread.restype=W.HANDLE
    k.Wow64GetThreadContext.argtypes=[W.HANDLE,C.c_void_p]
    class Thread(C.Structure):
        _fields_=[('size',W.DWORD),('usage',W.DWORD),('id',W.DWORD),('owner',W.DWORD),('priority',W.LONG),('delta',W.LONG),('flags',W.DWORD)]
    k.Thread32First.argtypes=[W.HANDLE,C.POINTER(Thread)];k.Thread32Next.argtypes=k.Thread32First.argtypes
    h=k.OpenProcess(0x1c38,False,pid)
    if not h:raise C.WinError(C.get_last_error())
    def read(addr,n):
        b=C.create_string_buffer(n);got=C.c_size_t()
        if not k.ReadProcessMemory(h,addr,b,n,C.byref(got)) or got.value!=n:raise C.WinError(C.get_last_error())
        return b.raw
    def write(addr,b):
        got=C.c_size_t()
        if not k.WriteProcessMemory(h,addr,C.create_string_buffer(b),len(b),C.byref(got)) or got.value!=len(b):raise C.WinError(C.get_last_error())
        assert read(addr,len(b))==b
        if not k.FlushInstructionCache(h,addr,len(b)):raise C.WinError(C.get_last_error())
    try:
        path=C.create_unicode_buffer(32768);size=W.DWORD(32768)
        if not k.QueryFullProcessImageNameW(h,0,path,C.byref(size)):raise C.WinError(C.get_last_error())
        expected=Path(expected_path) if expected_path else HERE.parent/'story-coop-v14-transitions/game/bin/shank2-coop-v15-boss-fixes-test.exe'
        assert Path(path.value).resolve()==expected.resolve()
        manifest=Path(manifest_path) if manifest_path else HERE/'combined-validation.json'
        build=next(r for r in json.loads(manifest.read_text()) if r['name']=='keyboard-chs.exe')
        assert hashlib.sha256(expected.read_bytes()).hexdigest()==build['sha256']
        assert read(site,length)==expected_entry
        checks=json.loads((HERE/('pose2-validation.json' if render_pose else 'assist-validation.json')).read_text(encoding='utf-8-sig'))
        assert checks['passed']
        if not render_pose:assert checks['boss_types_excluded']==15
        remote=k.VirtualAllocEx(h,None,8192,0x3000,0x04)
        if not remote or remote>=0x80000000:raise RuntimeError('No x86 test memory')
        ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
        if render_pose:
            from pose2 import routine as pose_routine
            blob=pose_routine(asm,remote)
        else:blob=routine(asm,remote)
        assert len(blob)<4096
        write(remote,blob);write(remote+0x1000,struct.pack('<'+str(len(ENEMIES))+'I',*ENEMIES))
        old=W.DWORD()
        if not k.VirtualProtectEx(h,remote,4096,0x20,C.byref(old)):raise C.WinError(C.get_last_error())
        # Freeze only this game and reject a suspended EIP inside the replaced prologue.
        if nt.NtSuspendProcess(h)!=0:raise RuntimeError('Could not suspend the isolated game')
        try:
            snapshot=k.CreateToolhelp32Snapshot(4,0)
            if snapshot==C.c_void_p(-1).value:raise C.WinError(C.get_last_error())
            try:
                item=Thread();item.size=C.sizeof(item);more=k.Thread32First(snapshot,C.byref(item))
                while more:
                    if item.owner==pid:
                        thread=k.OpenThread(0x48,False,item.id)
                        if not thread:raise C.WinError(C.get_last_error())
                        try:
                            storage=C.create_string_buffer(732);ctx=(C.addressof(storage)+15)&~15
                            C.memmove(ctx,struct.pack('<I',0x10001),4)
                            if not k.Wow64GetThreadContext(thread,ctx):raise C.WinError(C.get_last_error())
                            eip=struct.unpack('<I',C.string_at(ctx+184,4))[0]
                            assert eip and not site<=eip<site+length,'Thread in prologue; resume and retry after pausing'
                        finally:k.CloseHandle(thread)
                    more=k.Thread32Next(snapshot,C.byref(item))
            finally:k.CloseHandle(snapshot)
            assert read(site,length)==expected_entry
            if not k.VirtualProtectEx(h,site,length,0x40,C.byref(old)):raise C.WinError(C.get_last_error())
            try:
                try:write(site,asm(f'jmp {remote}',site)+b'\x90'*(length-5))
                except BaseException:write(site,expected_entry);raise
            finally:
                ignored=W.DWORD();k.VirtualProtectEx(h,site,length,old.value,C.byref(ignored))
        finally:
            if nt.NtResumeProcess(h)!=0:raise RuntimeError('Resume failed for isolated game')
        report=dict(pid=pid,thunk=hex(remote),counters=hex(remote+0x1800),players_invincible=True,
                    ordinary_enemy_types=len(ENEMIES),boss_types_excluded=15,lifetime='current process only',
                    saved_files_modified=False,distribution_modified=False)
        if render_pose:report=dict(pid=pid,thunk=hex(remote),render_only=True,boss='boss_militia',native_grab_unchanged=True,gameplay_pending=True)
        report['executable']=str(expected)
        (Path(report_dir or HERE)/f'{"pose2" if render_pose else "assist"}-{pid}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report))
    finally:k.CloseHandle(h)

if __name__=='__main__':install(int(sys.argv[1]),'--pose2' in sys.argv)
