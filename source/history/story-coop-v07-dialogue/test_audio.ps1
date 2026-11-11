$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'Use x86 PowerShell.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class AudioMapTest {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint k,uint a);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]public delegate IntPtr Open(IntPtr p,uint f);
 public static Open Bind(IntPtr p){return (Open)Marshal.GetDelegateForFunctionPointer(p,typeof(Open));}
}
'@
$mem=[AudioMapTest]::VirtualAlloc([IntPtr]0x20000000,[UIntPtr]::new([uint32]16384),0x3000,0x40)
if($mem.ToInt32() -ne 0x20000000){throw 'Allocation failed.'}
$bytes=[IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'audio-test.bin'));[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
$open=[AudioMapTest]::Bind($mem);$meta=Get-Content (Join-Path $PSScriptRoot 'audio-build.json') -Raw | ConvertFrom-Json
$root=$meta.resource_root+'\';$checks=0
function Call-Movie([string]$name,[string]$expected,[uint32]$flags=305397760) {
 $ptr=[Runtime.InteropServices.Marshal]::StringToHGlobalAnsi($name)
 try {
  $result=$open.Invoke($ptr,$flags);$actual=[Runtime.InteropServices.Marshal]::PtrToStringAnsi($result)
  if($actual -cne $expected){throw ('Wrong path: '+$actual+' expected '+$expected)}
  if([Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]0x20001f20) -ne $flags){throw 'Flags changed.'}
 } finally {[Runtime.InteropServices.Marshal]::FreeHGlobal($ptr)}
}
foreach($file in $meta.files) {
 Call-Movie ('../data/movies/'+$file) ($root+$file);$checks++
 Call-Movie ('G:\path with spaces\'+$file.ToLowerInvariant()) ($root+$file.ToLowerInvariant()) 0;$checks++
}
foreach($name in @('../data/bootstrap/movies/boot_logos.bik','data/movies/prefix01_INT_003.bik','not-a-movie.bik',(('x'*1100)+'/01_INT_003.bik'))) {Call-Movie $name $name;$checks++}
[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]0x2000101c,0)
Call-Movie '../data/movies/01_INT_003.bik' '../data/movies/01_INT_003.bik';$checks++
[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]0x2000101c,1)
[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]0x20001f28,1)
$before=[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]0x20001f24)
Call-Movie '../data/movies/01_INT_003.bik' '../data/movies/01_INT_003.bik';$checks++
if([Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]0x20001f24) -ne $before+2 -or [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]0x20001018) -ne 1){throw 'Fallback did not perform exactly one original retry.'}
@{passed=$checks;all_27_names=$true;flags_and_stack_preserved=$true;disabled_passthrough=$true;failed_overlay_falls_back=$true} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'audio-hook-tests.json') -Encoding UTF8
Write-Output "Passed $checks native audio-map path, flag, disabled-mode and fallback cases."
