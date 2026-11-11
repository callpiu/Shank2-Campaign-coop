"""Add one action recorder to the explicitly paused, path-verified diagnostic copy."""
import ctypes as C,struct,sys
from ctypes import wintypes as W
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
k=C.WinDLL('kernel32',use_last_error=True)
k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenProcess.restype=W.HANDLE
k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
k.WriteProcessMemory.argtypes=k.ReadProcessMemory.argtypes
k.VirtualProtectEx.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,C.POINTER(W.DWORD)]
k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
k.FlushInstructionCache.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t]
k.CloseHandle.argtypes=[W.HANDLE]
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
h=k.OpenProcess(0x1438,False,int(sys.argv[1]));assert h
def read(a,n):
 b=C.create_string_buffer(n);got=C.c_size_t();assert k.ReadProcessMemory(h,a,b,n,C.byref(got)) and got.value==n;return b.raw
def write(a,b):
 old=W.DWORD();assert k.VirtualProtectEx(h,a,len(b),0x40,C.byref(old))
 try:
  got=C.c_size_t();assert k.WriteProcessMemory(h,a,C.create_string_buffer(b),len(b),C.byref(got)) and got.value==len(b)
  assert k.FlushInstructionCache(h,a,len(b))
 finally:
  unused=W.DWORD();assert k.VirtualProtectEx(h,a,len(b),old.value,C.byref(unused))
try:
 name=C.create_unicode_buffer(32768);size=W.DWORD(32768)
 assert k.QueryFullProcessImageNameW(h,0,name,C.byref(size))
 assert name.value.lower()==r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test\bin\shank2-coop-revive-probe.exe'.lower()
 a=0x4daaa0;dest=0x7fed00;old=bytes.fromhex('51538b5c240c')
 assert read(a,len(old))==old
 blob=asm('''
pushfd
pushad
cmp dword ptr [0x7ff004], 5
jne done
mov eax, dword ptr [esp+40]
mov eax, dword ptr [eax+8]
cmp eax, dword ptr [0x7ff010]
jne done
mov ecx, dword ptr [esp+44]
cmp ecx, 0x856b1f63
je record
cmp ecx, 0x11198e40
je record
cmp ecx, 0x81580245
jne done
record:
mov edx, dword ptr [0x7ff114]
and edx, 63
shl edx, 4
mov dword ptr [edx+0x7ff900], ecx
mov dword ptr [edx+0x7ff904], eax
mov ecx, dword ptr [0x7ff02c]
mov dword ptr [edx+0x7ff908], ecx
inc dword ptr [0x7ff114]
done:
popad
popfd
push ecx
push ebx
mov ebx, dword ptr [esp+12]
jmp 0x4daaa6
''',dest)
 assert read(dest,len(blob))==b'\xcc'*len(blob)
 write(dest,blob);write(a,asm(f'jmp {dest:#x}',a)+b'\x90')
 print('Native common-action recorder added to paused diagnostic copy')
finally:k.CloseHandle(h)
