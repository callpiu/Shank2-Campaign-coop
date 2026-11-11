"""Verify Windows maps each new image; never resume or run game/Steam code."""
import ctypes as C
from ctypes import wintypes as W
import json
import sys
from flow import HERE,CODE,DATA
if len(sys.argv)>1:
    from pathlib import Path
    HERE=Path(sys.argv[1]).resolve()

k=C.WinDLL('kernel32',use_last_error=True)
class Startup(C.Structure):
    _fields_=[('cb',W.DWORD),('reserved',W.LPWSTR),('desktop',W.LPWSTR),('title',W.LPWSTR),
        ('x',W.DWORD),('y',W.DWORD),('xs',W.DWORD),('ys',W.DWORD),('xc',W.DWORD),('yc',W.DWORD),
        ('fill',W.DWORD),('flags',W.DWORD),('show',W.WORD),('count',W.WORD),('bytes',C.c_void_p),
        ('input',W.HANDLE),('output',W.HANDLE),('error',W.HANDLE)]
class Process(C.Structure):
    _fields_=[('process',W.HANDLE),('thread',W.HANDLE),('pid',W.DWORD),('tid',W.DWORD)]
class Region(C.Structure):
    _fields_=[('base',C.c_void_p),('allocation',C.c_void_p),('allocationProtection',W.DWORD),
        ('partition',W.WORD),('size',C.c_size_t),('state',W.DWORD),('protection',W.DWORD),('kind',W.DWORD)]
k.CreateProcessW.argtypes=[W.LPCWSTR,W.LPWSTR,C.c_void_p,C.c_void_p,W.BOOL,W.DWORD,C.c_void_p,W.LPCWSTR,C.POINTER(Startup),C.POINTER(Process)]
k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
k.VirtualQueryEx.argtypes=[W.HANDLE,C.c_void_p,C.POINTER(Region),C.c_size_t];k.VirtualQueryEx.restype=C.c_size_t
k.TerminateProcess.argtypes=[W.HANDLE,W.UINT];k.WaitForSingleObject.argtypes=[W.HANDLE,W.DWORD];k.CloseHandle.argtypes=[W.HANDLE]
rows=[]
builds={row['name']:row for row in json.loads((HERE/'builds.json').read_text())}
for p in sorted((HERE/'dev').glob('*.exe')):
    start=Startup();start.cb=C.sizeof(start);proc=Process()
    if not k.CreateProcessW(str(p),None,None,None,False,0x08000004,None,str(p.parent),C.byref(start),C.byref(proc)):
        raise RuntimeError(f'{p.name}: {C.WinError(C.get_last_error())}')
    try:
        regions=[]
        for address,expected in ((int(builds[p.name]['code'],16),(0x20,)),(int(builds[p.name]['data'],16),(0x04,0x08))):
            region=Region();assert k.VirtualQueryEx(proc.process,address,C.byref(region),C.sizeof(region))
            # Fresh writable MEM_IMAGE pages can be PAGE_WRITECOPY until the
            # process writes them; both have the required writable semantics.
            assert region.state==0x1000 and region.protection in expected,(p.name,hex(address),hex(region.protection))
            regions.append(dict(address=hex(address),protection=hex(region.protection)))
        header=C.create_string_buffer(1024);got=C.c_size_t()
        assert k.ReadProcessMemory(proc.process,0x400000,header,1024,C.byref(got)) and got.value==1024
        assert header.raw==p.read_bytes()[:1024]
        rows.append(dict(name=p.name,mapped_by_windows=True,main_thread_never_resumed=True,regions=regions))
    finally:
        k.TerminateProcess(proc.process,0);k.WaitForSingleObject(proc.process,5000)
        k.CloseHandle(proc.thread);k.CloseHandle(proc.process)
assert len(rows)==4
(HERE/'image-load-validation.json').write_text(json.dumps(dict(passed=True,builds=rows,steam_code_executed=False),indent=2)+'\n',encoding='utf-8')
print('PASS: Windows mapped all 4 images and their RX/RW sections; no game code executed.')
