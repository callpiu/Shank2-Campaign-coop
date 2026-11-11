"""Read the exact live skin rows consumed by the native damage calculator.

No remote calls, hooks or writes: follow 4d1d30/406620/508440/506560's
documented pointer paths and inspect the same original skin-vector rows.
"""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import re
import struct
import sys

from build_traits import HERE, DIAG, sha


def main(pid):
    k=C.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD]
    k.OpenProcess.restype=W.HANDLE
    k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
    k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
    k.CloseHandle.argtypes=[W.HANDLE]
    h=k.OpenProcess(0x1010,False,pid)
    if not h:raise C.WinError(C.get_last_error())
    try:
        target=HERE.parent/'story-coop-v14-transitions/game/bin/shank2-story-coop-v27-test.exe'
        path=C.create_unicode_buffer(32768);length=W.DWORD(len(path))
        if not k.QueryFullProcessImageNameW(h,0,path,C.byref(length)):raise C.WinError(C.get_last_error())
        assert Path(path.value).resolve()==target.resolve()
        row=next(r for r in json.loads((HERE/'builds.json').read_text()) if r['language']=='chs')
        assert sha(target.read_bytes())==row['sha256']
        def read(a,size):
            b=C.create_string_buffer(size);done=C.c_size_t()
            if not k.ReadProcessMemory(h,a,b,size,C.byref(done)) or done.value!=size:raise C.WinError(C.get_last_error())
            return b.raw
        def u(a):return struct.unpack('<I',read(a,4))[0]
        def f(a):return struct.unpack('<f',read(a,4))[0]
        def hashed(s):
            v=0
            for b in s.encode():v=(v*0x1003f+b)&0xffffffff
            return v
        lua=(target.parent.parent/'data/bootstrap/skins.lua').read_text(encoding='utf8')
        names={hashed(s):s for s in re.findall(r'\b(?:name|tag)\s*=\s*"([^"]+)"',lua)}
        manager=u(0x7dccb4)
        begin,end=u(manager+0x38),u(manager+0x3c)
        assert 0<=end-begin<=0x3000 and (end-begin)%0x30==0
        groups={u(a):a for a in range(begin,end,0x30)}
        players=[]
        for slot in range(2):
            actor=u(DIAG+12+slot*4)
            assert actor
            prop=u(actor+0x158)
            group_hash=u(u(prop+0x9c)+0x30)
            # 406620 -> 406560 -> 4078e0 -> optional 4064a0.
            state=actor+0x28
            flag=u(actor+0x24)
            if read(flag,1)!=b'\0':state=u(state+0xc8)
            skin_hash=u(state+0x104)
            group=groups[group_hash]
            skin_begin,skin_end=u(group+0x24),u(group+0x28)
            assert 0<=skin_end-skin_begin<=0x10000 and (skin_end-skin_begin)%0x90==0
            skins={u(a):a for a in range(skin_begin,skin_end,0x90)}
            skin=skins[skin_hash]
            tag_begin,tag_end=u(skin+0x70),u(skin+0x74)
            assert 0<=tag_end-tag_begin<=0x1000 and (tag_end-tag_begin)%8==0
            tags={names.get(u(a),hex(u(a))):f(a+4) for a in range(tag_begin,tag_end,8)}
            players.append(dict(slot=slot+1,actor=hex(actor),state=hex(state),
                family=names[group_hash],skin=names[skin_hash],skin_row=hex(skin),
                actor_damage_base=f(u(prop+0x98)+0xa8),skin_damage_base=f(skin+0x8c),damage_tags=tags))
        result=dict(pid=pid,build_sha256=row['sha256'],generation=u(DIAG+32),read_only=True,players=players)
        report=json.dumps(result,indent=2)
        print(report)
        (HERE/f'live-skin-table-{pid}-generation{result["generation"]}.json').write_text(report+'\n',encoding='utf8')
    finally:k.CloseHandle(h)


if __name__=='__main__':main(int(sys.argv[1]))
