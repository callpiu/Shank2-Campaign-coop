"""Read-only status for the exact isolated v26 test process."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys
from build import HERE, WORK

pid=int(sys.argv[1])
record=next(row for row in json.loads((HERE/'builds.json').read_text()) if row['language']=='chs')
data=int(record['data'],16)
kernel=C.WinDLL('kernel32',use_last_error=True)
kernel.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD]
kernel.OpenProcess.restype=W.HANDLE
kernel.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
kernel.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
kernel.CloseHandle.argtypes=[W.HANDLE]
h=kernel.OpenProcess(0x1010,False,pid)
if not h: raise C.WinError(C.get_last_error())
try:
    name=C.create_unicode_buffer(32768); length=W.DWORD(len(name))
    if not kernel.QueryFullProcessImageNameW(h,0,name,C.byref(length)):raise C.WinError(C.get_last_error())
    path=WORK/'story-coop-v14-transitions/game/bin/shank2-story-coop-v26-test.exe'
    assert Path(name.value).resolve()==path.resolve()
    def read(a,n):
        b=C.create_string_buffer(n);done=C.c_size_t()
        if not kernel.ReadProcessMemory(h,a,b,n,C.byref(done)) or done.value!=n: raise C.WinError(C.get_last_error())
        return b.raw
    def n(a): return struct.unpack('<I',read(a,4))[0]
    cfg=read(data+0x80,116)
    assist=json.loads((HERE/f'assist-{pid}.json').read_text())
    stats=int(assist['counters'],16)
    report=dict(pid=pid,submenu=hex(n(data)),mode=n(data+4),input_mode=n(data+0x84),
        config_read_bytes=n(data+0x600),pause_flow_stage=n(0x7ff004),
        player1=hex(n(0x7ff00c)),player2=hex(n(0x7ff010)),
        prelevel_active=hex(n(0x808010)),prelevel_player=n(0x808014),
        prelevel_confirmations=[n(0x808028),n(0x80802c)],config_magic=cfg[:4].decode('ascii'),
        assist_hits=[n(stats),n(stats+4)])
    print(json.dumps(report))
finally:
    kernel.CloseHandle(h)
