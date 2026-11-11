param([string]$Fixture,[string]$Metadata,[string]$Report)
$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'x86 required'}
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class LifecycleTest {
 [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p, UIntPtr s, uint t, uint a);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int InvokeHook(int mode);
 public static InvokeHook Hook(int p) {return (InvokeHook)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(InvokeHook));}
}
'@
$v=0x20000000
$mem=[LifecycleTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(65536),0x3000,0x40)
if($mem.ToInt32() -ne $v){throw 'allocation failed'}
$bytes=[IO.File]::ReadAllBytes($Fixture)
$meta=Get-Content -LiteralPath $Metadata -Raw | ConvertFrom-Json
function Get-U([int]$o){[BitConverter]::ToUInt32([BitConverter]::GetBytes([Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$o))),0)}
$checks=New-Object Collections.ArrayList
foreach($entry in $meta.entries){
 foreach($mode in @(1,2)){
  [Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
  $result=([LifecycleTest]::Hook($entry.entry)).Invoke($mode)
  $off=[int]$entry.offset;$expected=1
  if($mode -eq 1){
   switch($off){0x5c0{$expected=2};0x620{$expected=0};0x660{$expected=17};0x6a0{$expected=17};0x6e0{$expected=0};0x710{$expected=0};0x7a0{$expected=2};0x800{$expected=0}}
  }
  if((Get-U 0x8000) -ne $expected){throw ('call count '+$off+' mode '+$mode)}
  for($i=0;$i -lt $expected;$i++){
   $r=0x8100+20*$i
   if($mode -ne 1){
    if((Get-U ($r+4)) -ne $v+0x7300 -or (Get-U ($r+8)) -ne $v+0x7400){throw 'native arguments changed'}
   } elseif($off -eq 0x5c0){
    if((Get-U $r) -ne 1 -or (Get-U ($r+4)) -ne $v+0x7300 -or (Get-U ($r+8)) -ne $v+0x4c10+8*$i -or (Get-U ($r+12)) -ne 0x22 -or (Get-U ($r+16)) -ne 0x33){throw 'preload arguments'}
   } elseif($off -in @(0x660,0x6a0)){
    $family=[int][bool]$meta.skin_families[$i]
    if((Get-U $r) -ne 2 -or (Get-U ($r+8)) -ne $meta.families[$family] -or (Get-U ($r+12)) -ne $meta.skins[$i] -or (Get-U ($r+16)) -ne 0x33){throw 'skin release arguments'}
   } elseif($off -eq 0x7a0){
    if((Get-U $r) -ne 3 -or (Get-U ($r+4)) -ne $v+0x7300 -or (Get-U ($r+8)) -ne $meta.families[$i]){throw 'family release arguments'}
   }
  }
  $null=$checks.Add(@{offset=('0x{0:x}' -f $off);mode=$mode;native_calls=$expected;passed=$true})
 }
}
@{cases=@($checks);case_count=$checks.Count;actual_x86_hooks=$true;game_process_modified=$false} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$checks.Count+' native lifecycle cases; 17 skins, both family resources, stock-mode fallback and suppressed duplicate calls.')
