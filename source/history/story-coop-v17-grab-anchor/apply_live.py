"""Apply the validated display-anchor change to the exact paused v16 test.

Old hook and trampoline are retained; only its 6-byte entry jump changes.
Process suspension and EIP checks avoid patching an executing instruction.
No actor position, HP, save, installed game, or on-disk EXE is modified.
"""
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
from pathlib import Path
import struct
import sys
from anchor import HERE,routine,load_anchor
from pose3 import routine as previous_routine
from build_teleport import Ks,KS_ARCH_X86,KS_MODE_32

def apply(pid):
    assert json.loads((HERE/'anchor-validation.json').read_text(encoding='utf-8-sig'))['passed']
    assert json.loads((HERE/'anchor-validation.json.deferred.json').read_text(encoding='utf-8-sig'))['passed']
    expected=HERE.parent/'story-coop-v14-transitions/game/bin/shank2-coop-v16-boss-fixes-test.exe'
    manifest=json.loads((HERE.parent/'story-coop-v16-crash-recovery/build-validation.json').read_text())
    record=next(r for r in manifest if r['name']=='keyboard-chs.exe')
    assert hashlib.sha256(expected.read_bytes()).hexdigest()==record['sha256']
    ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
    entry=asm('jmp 0x7fcc00;nop',0x511460)
    old_code=previous_routine(asm,0x7fcc00,metrics=0x7ffa00)
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
        assert Path(path.value).resolve()==expected.resolve()
        assert read(0x511460,6)==entry
        assert read(0x7fcc00,len(old_code))==old_code
        assert read(0x7fcf80,11)==asm('push ebp;mov ebp,esp;and esp,-8;jmp 0x511466',0x7fcf80)
        remote=k.VirtualAllocEx(h,None,4096,0x3000,0x04)
        if not remote or remote>=0x80000000:raise RuntimeError('No x86 render memory')
        blob=routine(asm,remote,metrics=0x7ffa00)
        assert len(blob)<4096
        write(remote,blob);old=W.DWORD()
        if not k.VirtualProtectEx(h,remote,4096,0x20,C.byref(old)):raise C.WinError(C.get_last_error())
        if nt.NtSuspendProcess(h)!=0:raise RuntimeError('Could not suspend isolated process')
        try:
            snapshot=k.CreateToolhelp32Snapshot(4,0)
            if snapshot==C.c_void_p(-1).value:raise C.WinError(C.get_last_error())
            try:
                item=Thread();item.size=C.sizeof(item);more=k.Thread32First(snapshot,C.byref(item))
                while more:
                    if item.owner==pid:
                        th=k.OpenThread(0x48,False,item.id)
                        if not th:raise C.WinError(C.get_last_error())
                        try:
                            storage=C.create_string_buffer(732);ctx=(C.addressof(storage)+15)&~15
                            C.memmove(ctx,struct.pack('<I',0x10001),4)
                            if not k.Wow64GetThreadContext(th,ctx):raise C.WinError(C.get_last_error())
                            eip=struct.unpack('<I',C.string_at(ctx+184,4))[0]
                            assert eip and not 0x511460<=eip<0x511466,'Thread in replaced prologue'
                        finally:k.CloseHandle(th)
                    more=k.Thread32Next(snapshot,C.byref(item))
            finally:k.CloseHandle(snapshot)
            assert read(0x511460,6)==entry and read(0x7fcc00,len(old_code))==old_code
            counts=struct.unpack('<2I',read(0x7ffa00,8))
            patch=asm(f'jmp {remote};nop',0x511460)
            if not k.VirtualProtectEx(h,0x511460,6,0x40,C.byref(old)):raise C.WinError(C.get_last_error())
            try:
                try:write(0x511460,patch)
                except BaseException:write(0x511460,entry);raise
            finally:
                ignored=W.DWORD();k.VirtualProtectEx(h,0x511460,6,old.value,C.byref(ignored))
        finally:
            if nt.NtResumeProcess(h)!=0:raise RuntimeError('Process resume failed')
        report=dict(pid=pid,thunk=hex(remote),code_size=len(blob),old_counts=list(counts),
            local_pelvis=load_anchor()['local_pelvis'],entry=patch.hex(),render_only=True,
            gameplay_position_unchanged=True,source_packets_unchanged=True,on_disk_exe_unchanged=True,
            visual_validation_pending=True)
        (HERE/f'live-{pid}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report))
    finally:k.CloseHandle(h)

if __name__=='__main__':apply(int(sys.argv[1]))
