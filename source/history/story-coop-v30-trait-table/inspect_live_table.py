"""Read every persistent trait row after the real game's boot settings read."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
GAME=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
sys.path.insert(0,str(WORK/'story-coop-v28-trait-descriptions'))
from build_descriptions import summaries,name_hash,sha,TABLE_OFFSET,STRING_OFFSET


def main(pid):
    target=GAME/'bin/shank2.exe'
    row=next(r for r in json.loads((WORK/'story-coop-v28-trait-descriptions/builds.json').read_text()) if r['sha256']==sha(target.read_bytes()))
    k=C.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenProcess.restype=W.HANDLE
    k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
    k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
    k.CloseHandle.argtypes=[W.HANDLE]
    handle=k.OpenProcess(0x1010,False,pid)
    if not handle:raise C.WinError(C.get_last_error())
    try:
        path=C.create_unicode_buffer(32768);length=W.DWORD(len(path))
        if not k.QueryFullProcessImageNameW(handle,0,path,C.byref(length)):raise C.WinError(C.get_last_error())
        assert Path(path.value).resolve()==target.resolve()
        def read(a,n):
            b=C.create_string_buffer(n);done=C.c_size_t()
            if not k.ReadProcessMemory(handle,a,b,n,C.byref(done)) or done.value!=n:raise C.WinError(C.get_last_error())
            return b.raw
        def u(a):return struct.unpack('<I',read(a,4))[0]
        d=int(row['data'],16)
        count=u(d+0x600)
        assert count==116 and read(d+0x620,4)==b'S2K1','Boot has not read the current valid settings file.'
        actual=[]
        for i,(name,item) in enumerate(summaries()[row['language']].items()):
            key,ptr=struct.unpack('<II',read(d+TABLE_OFFSET+i*8,8))
            assert key==name_hash(name),(name,hex(key))
            assert d+STRING_OFFSET<=ptr<d+0x1000
            text=read(ptr,256).split(b'\0')[0].decode('utf8')
            assert text==item['text'],name
            actual.append(dict(skin=name,key=hex(key),text=text,matches=True))
        assert read(0x4ee3b0,7)==bytes.fromhex('6aff687e876f00')
        report=dict(passed=True,pid=pid,exe=str(target),sha256=row['sha256'],language=row['language'],
            native_settings_bytes_read=count,all_17_rows_and_texts_intact_after_real_startup=True,
            table_offset=hex(TABLE_OFFSET),no_test_assists=True,rows=actual)
        (HERE/'live-table-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
    finally:k.CloseHandle(handle)


if __name__=='__main__':main(int(sys.argv[1]))
