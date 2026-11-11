$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4) {throw 'Use 32-bit Windows PowerShell.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class FilterTest {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint k,uint a);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]public delegate uint Row(int category,int always,int unlocked);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]public delegate uint Reset(uint hash);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]public delegate uint Lookup(uint hash,int index);
 public static Delegate Bind(IntPtr p,Type t){return Marshal.GetDelegateForFunctionPointer(p,t);}
}
'@
$mem=[FilterTest]::VirtualAlloc([IntPtr]0x20000000,[UIntPtr]::new([uint32]8192),0x3000,0x40)
if($mem.ToInt32() -ne 0x20000000){throw 'Allocation failed.'}
$bytes=[IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'filter-test.bin'))
[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
$row=[FilterTest]::Bind([IntPtr]0x20000d00,[FilterTest+Row])
$reset=[FilterTest]::Bind([IntPtr]0x20000ec0,[FilterTest+Reset])
$lookup=[FilterTest]::Bind([IntPtr]0x20000f00,[FilterTest+Lookup])
$hashes=Get-Content (Join-Path $PSScriptRoot 'filter-test-hashes.json') -Raw | ConvertFrom-Json
$tests=0
for($category=0;$category -lt 3;$category++) {
 if($reset.Invoke([uint32]$hashes[$category]) -ne 0x12345678){throw 'Native map return changed.'}
 # Source rows 0 and 2 locked; 1 unlocked by progress; 3 always available.
 foreach($c in @(@(0,0,0),@(0,1,1),@(0,0,0),@(1,0,1))) {
  if($row.Invoke($category,$c[0],$c[1]) -ne $c[2]){throw 'Wrong row visibility.'};$tests++
 }
 foreach($c in @(@(0,1),@(1,3),@(2,0))) {
  if($lookup.Invoke([uint32]$hashes[$category],$c[0]) -ne $c[1]){throw 'Wrong filtered source index.'};$tests++
 }
}
# The original pre-level menu must bypass all filtering and remapping.
[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]0x20001800,0)
if($row.Invoke(0,0,0) -ne 1) {throw 'Pre-level row was filtered.'};$tests++
if($lookup.Invoke([uint32]$hashes[0],1) -ne 1) {throw 'Pre-level index was remapped.'};$tests++
if($reset.Invoke([uint32]$hashes[0]) -ne 0x12345678) {throw 'Pre-level native query changed.'};$tests++
Write-Output "Passed $tests native row visibility and non-contiguous selection cases."
