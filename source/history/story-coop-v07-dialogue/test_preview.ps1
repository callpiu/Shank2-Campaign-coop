$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'Use 32-bit PowerShell.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class MovieRedirectTest {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint k,uint a);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]public delegate IntPtr Open(IntPtr name,uint flags);
 public static Open Bind(IntPtr p){return (Open)Marshal.GetDelegateForFunctionPointer(p,typeof(Open));}
}
'@
$mem=[MovieRedirectTest]::VirtualAlloc([IntPtr]0x20000000,[UIntPtr]::new([uint32]12288),0x3000,0x40)
if($mem.ToInt32() -ne 0x20000000){throw 'Allocation failed.'}
$bytes=[IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'preview-test.bin'))
[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
$open=[MovieRedirectTest]::Bind($mem)
$redirect=[Runtime.InteropServices.Marshal]::PtrToStringAnsi([IntPtr]0x20001200)
$cases=@(
 @{name='data/movies/01_INT_003.bik';match=$true},
 @{name='..\data\movies\01_int_003.BIK';match=$true},
 @{name='G:\folder with spaces\data\movies\01_INT_003.bik';match=$true},
 @{name='01_INT_003.bik';match=$true},
 @{name='data/movies/prefix01_INT_003.bik';match=$false},
 @{name='data/movies/01_END_000.bik';match=$false},
 @{name='data/movies/logo.bik';match=$false},
 @{name=(('x'*1100)+'/01_INT_003.bik');match=$false}
)
$checks=0
foreach($flags in @(0,305397760)) {
 foreach($case in $cases) {
  $name=[Runtime.InteropServices.Marshal]::StringToHGlobalAnsi($case.name)
  try {
   $result=$open.Invoke($name,[uint32]$flags)
   $actual=[Runtime.InteropServices.Marshal]::PtrToStringAnsi($result)
   $expected=if($case.match){$redirect}else{$case.name}
   if($actual -cne $expected){throw 'Wrong movie redirect.'}
   if([Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]0x20001f20) -ne $flags){throw 'Movie flags changed.'}
   $checks++
  } finally {[Runtime.InteropServices.Marshal]::FreeHGlobal($name)}
 }
}
Write-Output "Passed $checks native movie filename/flag/stack redirect cases."
