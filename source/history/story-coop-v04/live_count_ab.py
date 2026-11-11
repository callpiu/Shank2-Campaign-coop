"""Reversible diagnostic A/B of one aligned vtable slot in the test process."""
import ctypes as C,struct,sys
from ctypes import wintypes as W
k=C.WinDLL('kernel32',use_last_error=True)
k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenProcess.restype=W.HANDLE
k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
k.WriteProcessMemory.argtypes=k.ReadProcessMemory.argtypes
k.CloseHandle.argtypes=[W.HANDLE]
pid=int(sys.argv[1]);restore=len(sys.argv)>2 and sys.argv[2]=='restore'
h=k.OpenProcess(0x438,False,pid)
if not h:raise C.WinError(C.get_last_error())
try:
 b=C.create_string_buffer(4);n=C.c_size_t()
 assert k.ReadProcessMemory(h,0x75019c,b,4,C.byref(n))
 before=0x6a9560 if restore else 0x7fc800;after=0x7fc800 if restore else 0x6a9560
 assert struct.unpack('<I',b.raw)[0]==before
 value=C.create_string_buffer(struct.pack('<I',after))
 # The executable's read-only vtable requires a temporary page permission.
 k.VirtualProtectEx.argtypes=[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,C.POINTER(W.DWORD)]
 old=W.DWORD();assert k.VirtualProtectEx(h,0x75019c,4,4,C.byref(old))
 try:assert k.WriteProcessMemory(h,0x75019c,value,4,C.byref(n)) and n.value==4
 finally:
  ignored=W.DWORD();assert k.VirtualProtectEx(h,0x75019c,4,old.value,C.byref(ignored))
 print('Restored mod count' if restore else 'Temporarily restored native declared player count')
finally:k.CloseHandle(h)
