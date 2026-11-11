param([string]$Fixture)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required' }
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class RetryScoreTest {
    [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p, UIntPtr s, uint t, uint a);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Call();
    public static Call Bind(int p) { return (Call)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Call)); }
}
'@
$v = 0x20000000
$mem = [RetryScoreTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(8192),0x3000,0x40)
if ($mem.ToInt32() -ne $v) { throw 'Fixture allocation failed' }
$bytes = [IO.File]::ReadAllBytes($Fixture)
function Reset-Fixture { [Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length) }
function Get-Word([int]$Offset) { [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$Offset)) }
function Set-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$Offset),$Value) }
function Check-Retry([int]$P1,[int]$P2,[int]$Calls=1) {
    if ($retry.Invoke() -ne 51 -or (Get-Word 0x1070) -ne $Calls) { throw 'Native this/flags/call count' }
    if ((Get-Word 0x1a50) -ne $P1 -or (Get-Word 0x1b50) -ne $P2) { throw "Wrong score, expected $P1 / $P2" }
}
$retry = [RetryScoreTest]::Bind($v+0x600)
Reset-Fixture
Check-Retry 425 875
if ((Get-Word 0x1850) -ne 425 -or (Get-Word 0x1950) -ne 875) { throw 'Modified old inventories' }
Set-Word 0x1a50 432
Set-Word 0x1b50 955
Check-Retry 432 955 2
Reset-Fixture
Set-Word 0x1850 0
Check-Retry 0 875
Reset-Fixture
Set-Word 0x1074 0
Check-Retry 110 260
Reset-Fixture
Set-Word 0x1074 2
Check-Retry 110 260
Reset-Fixture
Set-Word 0x1078 1
Check-Retry 110 260
Reset-Fixture
Set-Word 0x1004 0
Check-Retry 110 260
Reset-Fixture
Set-Word 0x1168 ($v+0x1300)
Check-Retry 110 260
Reset-Fixture
Set-Word 0x100c ($v+0x1500)
Check-Retry 110 260
Reset-Fixture
Set-Word 0x1524 0
Check-Retry 110 260
Reset-Fixture
Set-Word 0x1b08 ($v+0x1600)
Check-Retry 110 260
Reset-Fixture
Set-Word 0x1720 ($v+0x1300)
Check-Retry 110 260
Write-Output 'Passed 12 x86 score-retention scenarios (independence, zero, repeated retry, nonzero defaults, and boundary cases).'
