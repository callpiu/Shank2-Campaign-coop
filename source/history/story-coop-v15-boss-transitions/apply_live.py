"""Install only the validated teleport callback in the existing isolated game."""
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
from pathlib import Path
import struct
import sys
from build_teleport import HERE,CODE,NATIVE,routine,Ks,KS_ARCH_X86,KS_MODE_32

pid=int(sys.argv[1]);kernel=C.WinDLL('kernel32',use_last_error=True)
kernel.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];kernel.OpenProcess.restype=W.HANDLE
kernel.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
kernel.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
kernel.WriteProcessMemory.argtypes=kernel.ReadProcessMemory.argtypes
kernel.VirtualProtectEx.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,C.POINTER(W.DWORD)]
kernel.FlushInstructionCache.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t]
kernel.CloseHandle.argtypes=[W.HANDLE]
h=kernel.OpenProcess(0x1438,False,pid)
if not h:raise C.WinError(C.get_last_error())
def read(addr,n):
    value=C.create_string_buffer(n);got=C.c_size_t()
    if not kernel.ReadProcessMemory(h,addr,value,n,C.byref(got)) or got.value!=n:raise C.WinError(C.get_last_error())
    return value.raw
def write(addr,value):
    old=W.DWORD()
    if not kernel.VirtualProtectEx(h,addr,len(value),0x40,C.byref(old)):raise C.WinError(C.get_last_error())
    try:
        got=C.c_size_t()
        if not kernel.WriteProcessMemory(h,addr,C.create_string_buffer(value),len(value),C.byref(got)) or got.value!=len(value):raise C.WinError(C.get_last_error())
        if not kernel.FlushInstructionCache(h,addr,len(value)):raise C.WinError(C.get_last_error())
    finally:
        ignored=W.DWORD();kernel.VirtualProtectEx(h,addr,len(value),old.value,C.byref(ignored))

try:
    path=C.create_unicode_buffer(32768);size=W.DWORD(32768)
    if not kernel.QueryFullProcessImageNameW(h,0,path,C.byref(size)):raise C.WinError(C.get_last_error())
    expected=HERE.parent/'story-coop-v14-transitions/game/bin/shank2-coop-v08-keyboard.exe'
    assert Path(path.value).resolve()==expected.resolve()
    expected_hash=next(r['sha256'] for r in json.loads((HERE.parent/'story-coop-v12-live-character/builds.json').read_text()) if r['name']=='keyboard-chs.exe')
    assert hashlib.sha256(expected.read_bytes()).hexdigest()==expected_hash
    checks=json.loads((HERE/'teleport-validation.json').read_text(encoding='utf-8-sig'))
    assert checks['case_count']==12 and all(r['passed'] for r in checks['cases'])
    ks=Ks(KS_ARCH_X86,KS_MODE_32);blob=routine(lambda s,a:bytes(ks.asm(s,a)[0]))
    assert read(CODE,len(blob))==b'\xcc'*len(blob)
    assert read(0x75ae04,4)==struct.pack('<I',NATIVE)
    assert read(0x7ff900,60)==bytes(60)
    before=read(0x7ff000,40)+read(0x7ff800,128)
    write(CODE,blob)
    assert read(CODE,len(blob))==blob
    # Publish an aligned four-byte function pointer only after code is complete.
    write(0x75ae04,struct.pack('<I',CODE))
    assert read(0x75ae04,4)==struct.pack('<I',CODE)
    report=dict(pid=pid,path=str(expected),callback=hex(CODE),only_scene='Slums boss target 55751,1189',
                current_scene_not_moved=True,health_not_written=True,exe_on_disk_unchanged=True,
                runtime_header_and_loadouts_unchanged=before==read(0x7ff000,40)+read(0x7ff800,128),
                gameplay_reproduction_pending=True)
    (HERE/f'live-{pid}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
finally:kernel.CloseHandle(h)
