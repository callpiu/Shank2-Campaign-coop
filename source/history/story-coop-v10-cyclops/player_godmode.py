"""Temporary, process-only player damage immunity for the Cyclops diagnostic."""
import argparse
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'story-coop-v05'))
import native  # establishes the project's local dependency path
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

SITE = 0x4ee3b0
ORIGINAL = bytes.fromhex('6aff687e876f00')


def routine(asm, address, diag=0x7ff000, resume=SITE+7, replay=True):
    # Damage receiver is the first stdcall argument. Preserve volatile registers
    # and flags, and skip only current, registered campaign-player receivers.
    tail = f'push -1; push 0x6f877e; jmp {resume}' if replay else f'jmp {resume}'
    return asm(f'''pushfd
    push eax
    push edx
    cmp dword ptr [{diag+4}],5
    jne original
    mov eax,[esp+16]
    test eax,eax
    jz original
    mov eax,[eax+8]
    test eax,eax
    jz original
    cmp eax,[{diag+12}]
    je player
    cmp eax,[{diag+16}]
    jne original
    player:
    mov edx,[{diag+36}]
    test edx,edx
    jz original
    cmp [eax+0x20],edx
    jne original
    pop edx
    pop eax
    popfd
    ret 16
    original:
    pop edx
    pop eax
    popfd
    {tail}''', address)


def install(pid):
    kernel = C.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [W.DWORD,W.BOOL,W.DWORD]
    kernel.OpenProcess.restype = W.HANDLE
    kernel.ReadProcessMemory.argtypes = [W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
    kernel.WriteProcessMemory.argtypes = kernel.ReadProcessMemory.argtypes
    kernel.VirtualAllocEx.argtypes = [W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,W.DWORD]
    kernel.VirtualAllocEx.restype = C.c_void_p
    kernel.VirtualProtectEx.argtypes = [W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,C.POINTER(W.DWORD)]
    kernel.FlushInstructionCache.argtypes = [W.HANDLE,C.c_void_p,C.c_size_t]
    kernel.CloseHandle.argtypes = [W.HANDLE]
    handle = kernel.OpenProcess(0x438,False,pid)
    if not handle:
        raise C.WinError(C.get_last_error())

    def read(addr, n):
        out, got = C.create_string_buffer(n), C.c_size_t()
        if not kernel.ReadProcessMemory(handle,addr,out,n,C.byref(got)) or got.value != n:
            raise C.WinError(C.get_last_error())
        return out.raw

    def write(addr, data):
        got = C.c_size_t()
        if not kernel.WriteProcessMemory(handle,addr,data,len(data),C.byref(got)) or got.value != len(data):
            raise C.WinError(C.get_last_error())
        assert read(addr,len(data)) == data
        if not kernel.FlushInstructionCache(handle,addr,len(data)):
            raise C.WinError(C.get_last_error())

    try:
        assert read(0x7ff900,4) == b'CYCP', 'Not a Cyclops diagnostic process'
        assert read(SITE,7) == ORIGINAL, 'Unexpected damage entry; refusing to overwrite'
        remote = kernel.VirtualAllocEx(handle,None,4096,0x3000,0x04)
        if not remote or remote >= 0x80000000:
            raise RuntimeError('Cannot allocate x86 diagnostic thunk')
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm = lambda text, addr: bytes(ks.asm(text,addr)[0])
        blob = routine(asm,remote)
        write(remote,blob)
        previous = W.DWORD()
        if not kernel.VirtualProtectEx(handle,remote,4096,0x20,C.byref(previous)):
            raise C.WinError(C.get_last_error())
        if not kernel.VirtualProtectEx(handle,SITE,7,0x40,C.byref(previous)):
            raise C.WinError(C.get_last_error())
        try:
            write(SITE,asm(f'jmp {remote}; nop; nop',SITE))
        except Exception:
            write(SITE,ORIGINAL)
            raise
        finally:
            ignored = W.DWORD()
            kernel.VirtualProtectEx(handle,SITE,7,previous.value,C.byref(ignored))
        return dict(pid=pid,thunk=hex(remote),site=hex(SITE),players_only=True,
                    lifetime='current process only; close game to remove',saved_files_modified=False)
    finally:
        kernel.CloseHandle(handle)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pid',type=int)
    result=install(parser.parse_args().pid)
    Path(__file__).with_name('player-godmode-runtime.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
