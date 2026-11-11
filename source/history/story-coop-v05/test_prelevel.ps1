$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'Use 32-bit Windows PowerShell.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class PrelevelTest {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint k,uint a);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]public delegate uint Run(int op,int context,int stage,int confirmed);
 public static Run Bind(IntPtr p){return (Run)Marshal.GetDelegateForFunctionPointer(p,typeof(Run));}
}
'@
$mem=[PrelevelTest]::VirtualAlloc([IntPtr]0x20000000,[UIntPtr]::new([uint32]16384),0x3000,0x40)
if($mem.ToInt32() -ne 0x20000000){throw 'Allocation failed.'}
$bytes=[IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'prelevel-test.bin'))
[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
$run=[PrelevelTest]::Bind([IntPtr]0x20002000)
function Write32($offset,$value){[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr](0x20000000+$offset),[int]$value)}
function Read32($offset){[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr](0x20000000+$offset))}
function Reset-Case {
 $zeros=New-Object byte[] 8192
 [Runtime.InteropServices.Marshal]::Copy($zeros,0,[IntPtr]0x20001000,8192)
 foreach($o in @(0x1800,0x1840)){Write32 $o 1;Write32 ($o+20) 123;Write32 ($o+24) 11;Write32 ($o+28) 22;Write32 ($o+32) 33;Write32 ($o+36) 3}
 Write32 0x31dc 101;Write32 0x31e0 102;Write32 0x31e4 103
}
function Select-OtherWeapons {Write32 0x31dc 201;Write32 0x31e0 202;Write32 0x31e4 203}
function Assert-Weapons($a,$b,$c) {
 if((Read32 0x1818) -ne $a -or (Read32 0x181c) -ne $b -or (Read32 0x1820) -ne $c){throw 'P1 confirmed equipment was lost or partially written.'}
 if((Read32 0x1858) -ne 11 -or (Read32 0x185c) -ne 22 -or (Read32 0x1860) -ne 33){throw 'P2 equipment was changed.'}
}
$checks=0
foreach($stage in @(0,5)) {
 Reset-Case;$null=$run.Invoke(0,0,$stage,0)
 if((Read32 0x31dc) -ne 11 -or (Read32 0x31e0) -ne 22 -or (Read32 0x31e4) -ne 33){throw 'Pre-level default equipment did not use the launcher only as its initial value.'};$checks++
 Select-OtherWeapons;$null=$run.Invoke(1,0,$stage,1);Assert-Weapons 201 202 203;$checks++
 if((Read32 0x1380) -ne 1 -or (Read32 0x13a0) -ne 1){throw 'Native show/hide chain changed.'};$checks++
 if((Read32 0x1824) -ne 3 -or (Read32 0x1170) -ne 0 -or (Read32 0x1174) -ne 0){throw 'Ammo or menu lifecycle changed.'};$checks++
 Reset-Case;$null=$run.Invoke(0,0,$stage,0);Select-OtherWeapons;$null=$run.Invoke(1,0,$stage,0);Assert-Weapons 11 22 33;$checks++
}
Reset-Case;$null=$run.Invoke(0,1,5,0)
if((Read32 0x31dc) -ne 101){throw 'In-level menu defaults were overwritten.'};$checks++
Select-OtherWeapons;$null=$run.Invoke(1,1,5,1);Assert-Weapons 11 22 33;$checks++
Reset-Case;Write32 0x1800 0;$null=$run.Invoke(0,0,0,0);Select-OtherWeapons;$null=$run.Invoke(1,0,0,1);Assert-Weapons 11 22 33;$checks++
Reset-Case;$null=$run.Invoke(0,0,0,0);Select-OtherWeapons;Write32 0x31e4 0;$null=$run.Invoke(1,0,0,1);Assert-Weapons 11 22 33;$checks++
Write-Output "Passed $checks native pre-level defaults, confirmation, cancel, stale-stage and player-isolation cases."
