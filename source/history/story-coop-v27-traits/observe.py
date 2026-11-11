"""Read the exact isolated process's observed stats; no gameplay writes."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys
from build_traits import HERE, DIAG, sha

pid=int(sys.argv[1])
hotpatched='--hotpatched' in sys.argv[2:]
row=next(r for r in json.loads((HERE/'builds.json').read_text()) if r['language']=='chs')
stats=int(row['stats'],16)
data=int(row['data'],16)
target=HERE.parent/'story-coop-v14-transitions/game/bin/shank2-story-coop-v27-test.exe'
if not hotpatched:assert sha(target.read_bytes())==row['sha256']
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
    assert Path(name.value).resolve()==target.resolve()
    def read(a,n):
        b=C.create_string_buffer(n);done=C.c_size_t()
        if not kernel.ReadProcessMemory(h,a,b,n,C.byref(done)) or done.value!=n: raise C.WinError(C.get_last_error())
        return b.raw
    def n(a):return struct.unpack('<I',read(a,4))[0]
    def hash_name(t):
        v=0
        for c in t.encode():v=(v*0x1003f+c)&0xffffffff
        return v
    lua=(target.parent.parent/'data/bootstrap/skins.lua').read_text(encoding='utf8')
    import re
    skins={hash_name(k):k for k in re.findall(r'\bname\s*=\s*"([^"]+)"',lua)}
    tags={hash_name(k):k for k in re.findall(r'\btag\s*=\s*"([^"]+)"',lua)}
    original_damage=bytes.fromhex('6aff687e876f00')
    result={'pid':pid,'hotpatched':hotpatched,'mode':n(data+4),'stage':n(DIAG+4),'generation':n(DIAG+32),
        'native_damage_entry':read(0x4ee3b0,7)==original_damage,
        'trait_entry_unchanged':read(0x4f3f40,7)==bytes.fromhex('5153558b6c2410'),
        'trait_return_unchanged':read(0x4f4061,5)==bytes.fromhex('5f5e5d5b59'), 'players':[]}
    for i in range(2):
        hp,maximum,current,cnt,tag,mult,before,after=struct.unpack('<IffIIfff',read(stats+i*32,32))
        skin=n(0x7ff800+i*64+20)
        result['players'].append(dict(slot=i+1,actor=hex(n(DIAG+12+i*4)),skin=skins.get(skin,hex(skin)),
            spawn_count=hp,max_hp=maximum,spawn_hp=current,damage_tag_hits=cnt,
            last_tag=tags.get(tag,hex(tag)),multiplier=mult,before=before,after=after))
    report=json.dumps(result,indent=2)
    print(report)
    (HERE/'latest-runtime.json').write_text(report+'\n',encoding='utf8')
finally:
    kernel.CloseHandle(h)
