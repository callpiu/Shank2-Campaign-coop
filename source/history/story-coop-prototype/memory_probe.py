"""Read-only diagnostics for the isolated Shank 2 test process."""
import ctypes as C
from ctypes import wintypes as W
import struct, sys, json
k=C.WinDLL('kernel32',use_last_error=True)
k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD]; k.OpenProcess.restype=W.HANDLE
k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
k.VirtualQueryEx.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t]; k.VirtualQueryEx.restype=C.c_size_t
k.CloseHandle.argtypes=[W.HANDLE]
class MBI(C.Structure):
    _fields_=[('base',C.c_void_p),('alloc',C.c_void_p),('aprotect',W.DWORD),('partition',W.WORD),('size',C.c_size_t),('state',W.DWORD),('protect',W.DWORD),('type',W.DWORD)]
class Process:
    def __init__(self,pid):
        self.h=k.OpenProcess(0x410,False,pid)
        if not self.h: raise C.WinError(C.get_last_error())
    def read(self,a,n):
        out=C.create_string_buffer(n); got=C.c_size_t()
        if not k.ReadProcessMemory(self.h,C.c_void_p(a),out,n,C.byref(got)):return b''
        return out.raw[:got.value]
    def u32(self,a):
        b=self.read(a,4);return struct.unpack('<I',b)[0] if len(b)==4 else None
    def scan(self,patterns):
        a=0; found={n:[] for n in patterns}
        while a<0x80000000:
            m=MBI()
            if not k.VirtualQueryEx(self.h,C.c_void_p(a),C.byref(m),C.sizeof(m)):break
            start=m.base or 0;end=start+m.size
            if m.state==0x1000 and not m.protect&0x101 and m.protect&0xff in (2,4,8,0x20,0x40,0x80):
                for part in range(start,end,1024*1024):
                    data=self.read(part,min(end-part,1024*1024))
                    for name,pat in patterns.items():
                        pos=data.find(pat)
                        while pos>=0:
                            found[name].append(part+pos);pos=data.find(pat,pos+1)
            if end<=a:break
            a=end
        return found
    def close(self): k.CloseHandle(self.h)
def xinput():
    class GAMEPAD(C.Structure):
        _fields_=[('buttons',W.WORD),('lt',C.c_ubyte),('rt',C.c_ubyte),('lx',C.c_short),('ly',C.c_short),('rx',C.c_short),('ry',C.c_short)]
    class STATE(C.Structure):_fields_=[('packet',W.DWORD),('pad',GAMEPAD)]
    dll=C.WinDLL('xinput1_4');out=[]
    for i in range(4):
        s=STATE();result=dll.XInputGetState(i,C.byref(s));out.append({'index':i,'connected':result==0})
    return out
if __name__=='__main__':
    result={'xinput':xinput()}
    if len(sys.argv)>1:
        p=Process(int(sys.argv[1])); pats={'xinput_device':struct.pack('<I',0x75e8c4),'campaign_mode':struct.pack('<II',0x75023c,0x7502a4)}
        matches=p.scan(pats);result['objects']={}
        for name,addresses in matches.items():
            rows=[]
            for a in addresses:
                if a<0x800000:continue
                row={'address':hex(a)}
                if name=='xinput_device':
                    row.update(device_id=p.u32(a+4),index=list(p.read(a+0x17c,1)),name=p.read(a+0x19c,32).split(b'\0')[0].decode('ascii','replace'))
                else:row.update(sim=hex(p.u32(a+8) or 0))
                rows.append(row)
            result['objects'][name]=rows
        if len(sys.argv)>2:
            diag=int(sys.argv[2],16); raw=p.read(diag,64);result['diagnostics']=[hex(n) for n in struct.unpack('<16I',raw)] if len(raw)==64 else None
        p.close()
    print(json.dumps(result,indent=2))
