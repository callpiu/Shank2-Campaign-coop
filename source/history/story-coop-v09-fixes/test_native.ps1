$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'Use x86 PowerShell.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class Fix09Test {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr s,uint t,uint a);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]public delegate int Pair(IntPtr a,IntPtr b);
 public static Pair Bind(int p){return (Pair)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Pair));}
}
'@
$v=0x20000000;$mem=[Fix09Test]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(16384),0x3000,0x40)
if($mem.ToInt32() -ne $v){throw 'Allocation failed.'}
$bytes=[IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'native-test.bin'));[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
function Put([int]$Offset,[int]$Value){[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$Offset),$Value)}
function Get([int]$Offset){return [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$Offset))}
$common=[Fix09Test]::Bind($v+0x400);$boolean=[Fix09Test]::Bind($v+0x440);$recall=[Fix09Test]::Bind($v+0x480)
$p1=$v+0x2200;$p2=$v+0x2300;$sim=$v+0x2400;$foreign=$v+0x2500
Put 0x1804 5;Put 0x180c $p1;Put 0x1810 $p2;Put 0x1824 $sim
Put 0x2220 $sim;Put 0x2320 $sim;Put 0x2520 $sim
$resetHash=[BitConverter]::ToInt32([IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'reset-hash.bin')),0)
$checks=0
foreach($actor in @($p1,$p2,$foreign)) {
 foreach($matched in @($true,$false)) {
  Put 0x2008 $(if($matched){$resetHash}else{123});Put 0x2108 $actor;Put 0x1004 0
  $r=$common.Invoke([IntPtr]($v+0x2000),[IntPtr]($v+0x2100))
  $wanted=if($matched -and $actor -ne $foreign){0}else{1}
  if($r -ne 0x12345678 -or (Get 0x1024) -ne $wanted -or (Get 0x1004) -ne 0){throw 'Scoped cleanup/passthrough/return mismatch.'}
  $checks++
 }
}
Put 0x2008 $resetHash;Put 0x2108 $p1;Put 0x1804 0
$null=$common.Invoke([IntPtr]($v+0x2000),[IntPtr]($v+0x2100))
if((Get 0x1024) -ne 1){throw 'Noncampaign action was changed.'};$checks++
Put 0x1804 5;Put 0x1004 $p2
$null=$common.Invoke([IntPtr]($v+0x2000),[IntPtr]($v+0x2100))
if((Get 0x1024) -ne 0 -or (Get 0x1004) -ne $p2){throw 'Nested scope was not restored.'};$checks++
if($boolean.Invoke([IntPtr]$p2,[IntPtr]$sim) -ne 0 -or $boolean.Invoke([IntPtr]$p1,[IntPtr]$sim) -ne 1 -or $boolean.Invoke([IntPtr]$p2,[IntPtr]($sim+4)) -ne 1){throw 'Scope actor/simulation boundary failed.'};$checks+=3
Put 0x1004 0
if($boolean.Invoke([IntPtr]$p2,[IntPtr]$sim) -ne 1){throw 'Regular multiplayer bool was changed.'};$checks++
Put 0x1028 ($v+0x2800);Put 0x2280 42;Put 0x2284 99
$null=$recall.Invoke([IntPtr]$p2,[IntPtr]($v+0x2900))
if((Get 0x102c) -ne $v+0x2900 -or (Get 0x1030) -ne $v+0x2800 -or (Get 0x1034) -ne 0 -or (Get 0x1038) -ne 0 -or (Get 0x1010) -ne 1){throw 'Physics recall ABI failed.'}
if((Get 0x2280) -ne 42 -or (Get 0x2284) -ne 99){throw 'Recall modified actor extensions.'};$checks++
Put 0x1028 0
$null=$recall.Invoke([IntPtr]$p2,[IntPtr]($v+0x2900))
if((Get 0x1010) -ne 1){throw 'Missing body was not skipped.'};$checks++
@{passed=$checks;scope_restored=$true;multiplayer_outside_cleanup_preserved=$true;physics_only_recall_abi=$true;gameplay=$null} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'native-tests.json') -Encoding UTF8
Write-Output "Passed $checks native fix scope/ABI cases."
