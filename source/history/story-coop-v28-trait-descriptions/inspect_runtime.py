"""Read the exact isolated UI test's loader observation and selected summary."""
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct

from build_descriptions import HERE,BASE,pefile,sha,TABLE_OFFSET


def main():
    test=json.loads((HERE/'current-test.json').read_text())
    target=Path(test['path'])
    assert sha(target.read_bytes())==test['sha256']
    k=C.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenProcess.restype=W.HANDLE
    k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
    k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
    k.CloseHandle.argtypes=[W.HANDLE]
    handle=k.OpenProcess(0x1010,False,test['pid'])
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
        row=next(r for r in json.loads((HERE/'builds.json').read_text()) if r['language']==test['language'])
        assert row['sha256']==test['canonical_sha256']
        data=int(row['data'],16)
        pe=pefile.PE(str(target),fast_load=True)
        predat=BASE+next(s.VirtualAddress for s in pe.sections if s.Name.rstrip(b'\0')==b'.predat')
        ptr,initial_mode,calls=struct.unpack('<3I',read(data+0x5a0,12))
        screen=u(predat+0x10)
        key=u(data+0x580);text=None
        for index in range(17):
            h,p=struct.unpack('<2I',read(data+TABLE_OFFSET+index*8,8))
            if h==key:text=read(p,256).split(b'\0')[0].decode('utf8');break
        result=dict(pid=test['pid'],actual_exe_sha256=test['sha256'],canonical_sha256=row['sha256'],
            loader_calls=calls,mode_when_precreated=initial_mode,
            actual_loaded_selector=read(ptr,48).split(b'\0')[0].decode() if ptr else None,
            current_mode=u(data+4),current_page=u(screen+0x20) if screen else None,
            selected_skin_hash=hex(key),selected_trait_text=text,
            native_damage_entry=read(0x4ee3b0,7)==bytes.fromhex('6aff687e876f00'),
            original_description_callback_unchanged=read(0x68cb24,5)==bytes.fromhex('e89768d7ff'))
        (HERE/'analysis/runtime-observation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(json.dumps(result,indent=2))
    finally:k.CloseHandle(handle)


if __name__=='__main__':main()
