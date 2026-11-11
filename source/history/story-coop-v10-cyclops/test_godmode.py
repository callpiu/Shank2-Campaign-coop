"""Run player-only immunity machine code against controlled x86 receivers."""
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from player_godmode import routine,Ks,KS_ARCH_X86,KS_MODE_32

v=0x20000000
k=Ks(KS_ARCH_X86,KS_MODE_32)
asm=lambda s,a:bytes(k.asm(s,a)[0])
buf=bytearray(8192)
blocks={0:routine(asm,v,v+0x1000,v+0x300,False),
        0x300:asm(f'inc dword ptr [{v+0x1010}]; mov eax,7; ret 16',v+0x300),
        0x400:asm(f'''mov eax,[esp+4]; mov edx,99
            push 4; push 3; push 2; push eax
            mov eax,123; stc; call {v}; adc eax,0; ret 4''',v+0x400)}
for o,b in blocks.items():buf[o:o+len(b)]=b
for a,x in {0x1004:5,0x100c:v+0x1100,0x1024:v+0x1200,0x1120:v+0x1200,
            0x1308:v+0x1100,0x1408:v+0x1500,0x1520:v+0x1200}.items():struct.pack_into('<I',buf,a,x)
with tempfile.TemporaryDirectory() as t:
 p=Path(t)/'test.bin';p.write_bytes(buf)
 script=Path(t)/'test.ps1'
 script.write_text('''param([string]$File)
$ErrorActionPreference='Stop'
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class GodTest {
[DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint a,uint b);
[UnmanagedFunctionPointer(CallingConvention.StdCall)]public delegate int Call(IntPtr p);
public static Call Bind(int p){return (Call)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Call));}
}
'@
$v=0x20000000
$m=[GodTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(8192),0x3000,0x40)
if($m.ToInt32() -ne $v){throw 'Allocation'}
$b=[IO.File]::ReadAllBytes($File);[Runtime.InteropServices.Marshal]::Copy($b,0,$m,$b.Length)
$f=[GodTest]::Bind($v+0x400)
if($f.Invoke([IntPtr]($v+0x1300)) -ne 124){throw 'Player not protected or ABI damaged'}
if([Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+0x1010)) -ne 0){throw 'Player received damage'}
if($f.Invoke([IntPtr]($v+0x1400)) -ne 8){throw 'Foreign actor blocked'}
[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+0x1004),0)
if($f.Invoke([IntPtr]($v+0x1300)) -ne 8){throw 'Noncampaign blocked'}
[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+0x1004),5)
[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+0x1120),0)
if($f.Invoke([IntPtr]($v+0x1300)) -ne 8){throw 'Stale actor blocked'}
Write-Output 'Passed player immunity, foreign/Boss passthrough, noncampaign and stale actor cases.'
''')
 subprocess.run([str(Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'),
                 '-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),str(p)],check=True)
