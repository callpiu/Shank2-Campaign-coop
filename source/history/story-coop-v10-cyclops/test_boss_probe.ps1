param([string]$Fixture)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required' }
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class CyclopsProbeTest {
    [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p, UIntPtr s, uint t, uint a);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Call();
    public static Call Bind(int p) { return (Call)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Call)); }
}
'@
$v = 0x20000000
$mem = [CyclopsProbeTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(8192),0x3000,0x40)
if ($mem.ToInt32() -ne $v) { throw 'Fixture allocation failed' }
$bytes = [IO.File]::ReadAllBytes($Fixture)
[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
function Get-Word([int]$Offset) { [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$Offset)) }
function Set-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$Offset),$Value) }
$attempt = [CyclopsProbeTest]::Bind($v+0x600)
$resolve = [CyclopsProbeTest]::Bind($v+0x640)
$damage = [CyclopsProbeTest]::Bind($v+0x680)
if ($attempt.Invoke() -ne 61 -or (Get-Word 0x1004) -ne 1 -or (Get-Word 0x1008) -ne ($v+0x1600) -or (Get-Word 0x100c) -ne 7) { throw 'Attempt context/return' }
if ($resolve.Invoke() -ne 1 -or (Get-Word 0x1010) -ne 1 -or (Get-Word 0x1014) -ne 0) { throw 'Missing target / native flags' }
Set-Word 0x103c ($v+0x1800)
if ($resolve.Invoke() -ne ($v+0x1801) -or (Get-Word 0x1010) -ne 2 -or (Get-Word 0x1014) -ne ($v+0x1800) -or (Get-Word 0x1034) -ne 1) { throw 'Resolved target / native flags' }
if ($damage.Invoke() -ne 73 -or (Get-Word 0x1018) -ne 1 -or (Get-Word 0x1020) -ne ($v+0x1800) -or (Get-Word 0x1024) -ne 0x43700000 -or (Get-Word 0x1028) -ne 0x42a00000 -or (Get-Word 0x102c) -ne 0x41a00000 -or (Get-Word 0x1038) -ne 1) { throw 'Damage call/health trace/flags' }
Set-Word 0x1204 0
if ($attempt.Invoke() -ne 61 -or $resolve.Invoke() -ne ($v+0x1801) -or $damage.Invoke() -ne 73 -or (Get-Word 0x1004) -ne 1 -or (Get-Word 0x1010) -ne 2 -or (Get-Word 0x1018) -ne 1) { throw 'Unscoped passthrough' }
Write-Output 'Passed 5 x86 trace scenarios: attempt, missing target, valid target, damage and HP, unscoped passthrough.'
