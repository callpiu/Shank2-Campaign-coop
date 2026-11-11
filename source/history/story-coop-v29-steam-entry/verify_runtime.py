"""Record a genuine Steam-parented launch and the clean MOD's live code."""
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

from prepare import HERE,WORK,GAME


def main(pid,build_dir=None,report_dir=None):
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    ps=str(Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe')
    result=subprocess.run([ps,'-NoProfile','-Command',
        f"Get-CimInstance Win32_Process -Filter 'ProcessId={pid}' | Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine | ConvertTo-Json"],capture_output=True,text=True,check=True)
    proc=json.loads(result.stdout)
    assert Path(proc['ExecutablePath']).resolve()==(GAME/'bin/shank2.exe').resolve()
    parent=subprocess.run([ps,'-NoProfile','-Command',
        f"Get-CimInstance Win32_Process -Filter 'ProcessId={int(proc['ParentProcessId'])}' | Select-Object Name,ExecutablePath | ConvertTo-Json"],capture_output=True,text=True,check=True)
    parent=json.loads(parent.stdout);assert parent['Name'].lower()=='steam.exe'
    rows=json.loads(((Path(build_dir) if build_dir else WORK/'story-coop-v28-trait-descriptions')/'builds.json').read_text(encoding='utf8'))
    row=next(r for r in rows if r['sha256']==sha(GAME/'bin/shank2.exe'))
    assert not row['test_assists']
    assert sha(GAME/'bin/shank2-story-coop.exe')==row['sha256']
    sys.path.insert(0,str(WORK/'chs-compat/tools'))
    import pefile
    raw=(GAME/'bin/shank2.exe').read_bytes();pe=pefile.PE(data=raw,fast_load=True)
    k=C.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenProcess.restype=W.HANDLE
    k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
    k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
    k.CloseHandle.argtypes=[W.HANDLE]
    process=k.OpenProcess(0x1010,False,pid)
    if not process:raise C.WinError(C.get_last_error())
    try:
        path=C.create_unicode_buffer(32768);length=W.DWORD(len(path))
        if not k.QueryFullProcessImageNameW(process,0,path,C.byref(length)):raise C.WinError(C.get_last_error())
        assert Path(path.value).resolve()==(GAME/'bin/shank2.exe').resolve()
        def read(address,size):
            b=C.create_string_buffer(size);received=C.c_size_t()
            if not k.ReadProcessMemory(process,address,b,size,C.byref(received)) or received.value!=size:raise C.WinError(C.get_last_error())
            return b.raw
        checks=[]
        for address,size,label in ((0x4ee3b0,7,'Native damage: no invincibility/one-hit hook'),
            (0x4f3fb6,8,'Campaign skin damage traits'),(0x53ed6a,7,'Campaign ranged traits'),
            (int(row['code'],16)+0x1d80,70,'Bilingual right-side trait summary updater'),
            (0x68e15a,5,'Native UI constructor: no test observer')):
            offset=pe.get_offset_from_rva(address-0x400000)
            assert read(address,size)==raw[offset:offset+size]
            checks.append(label)
        if row.get('dodge_keys'):
            for address,size,label in ((0x6655ce,6,'Configured native right-stick dodge bridge'),
                (int(row['code'],16)+0x2200,120,'Independent dodge inputs and physical passthrough')):
                offset=pe.get_offset_from_rva(address-0x400000)
                assert read(address,size)==raw[offset:offset+size]
                checks.append(label)
        data=int(row['data'],16)
        selector=read(data+0x340,32).split(b'\0')[0].decode('ascii')
        assert selector==row['solo_description_asset']
    finally:k.CloseHandle(process)
    steam=Path(parent['ExecutablePath']).parent
    logs=(steam/'logs/gameprocess_log.txt').read_text(encoding='utf8',errors='replace').splitlines()
    logged=[line for line in logs if 'AppID 102840' in line and f'PID {pid} ' in line and 'tracked process' in line]
    assert logged
    report=dict(passed=True,pid=pid,process=proc,parent=parent,sha256=row['sha256'],
        memory_checks=checks,selector_asset=selector,steam_tracking_evidence=logged[-1],
        settings_launch_args=proc['CommandLine'],test_assists=False,game_left_running=True)
    ((Path(report_dir) if report_dir else HERE)/'steam-runtime-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main(int(sys.argv[1]))
