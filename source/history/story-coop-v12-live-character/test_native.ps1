param([string]$Fixture,[string]$Ids)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required' }
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class CharacterQueueTest {
    [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p, UIntPtr s, uint t, uint a);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Merge();
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Select(uint player, uint skin);
    public static Merge Rows(int p) { return (Merge)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Merge)); }
    public static Select Queue(int p) { return (Select)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Select)); }
}
'@
$v=0x20000000
$mem=[CharacterQueueTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(16384),0x3000,0x40)
if ($mem.ToInt32() -ne $v) { throw 'Fixture allocation failed' }
$bytes=[IO.File]::ReadAllBytes($Fixture)
$catalog=Get-Content -LiteralPath $Ids -Raw | ConvertFrom-Json
$hashes=$catalog.skins
$weapons=$catalog.weapons
function Reset-Fixture { [Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length) }
function Get-I([int]$o) { [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$o)) }
function Get-U([int]$o) { [BitConverter]::ToUInt32([BitConverter]::GetBytes((Get-I $o)),0) }
function Set-I([int]$o,[int]$x) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$o),$x) }
function Get-B([int]$o) { [Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+$o)) }
$merge=[CharacterQueueTest]::Rows($v+0x500)
$select=[CharacterQueueTest]::Queue($v+0x180)
Reset-Fixture
if ($merge.Invoke() -ne $v+0x1100 -or (Get-I 0x1128) -ne $v+0x1140+17*0x90) { throw 'Merged vector length' }
for ($i=0;$i -lt 17;$i++) {
    if ((Get-U (0x1140+$i*0x90)) -ne $hashes[$i] -or (Get-B (0x1140+$i*0x90+0x69)) -ne 0) { throw "Wrong row $i" }
}
if ((Get-B 0x2269) -ne 1 -or (Get-B 0x2a69) -ne 1) { throw 'Modified original assets' }
Set-I 0x2100 0
Set-I 0x2128 0
if ($merge.Invoke() -ne 0 -or (Get-I 0x1128) -ne $v+0x1140) { throw 'Malformed vector not rejected' }
Reset-Fixture
Set-I (0x2200+0x90) (Get-I 0x2200)
if ($merge.Invoke() -ne 0) { throw 'Duplicate used in place of missing skin' }
Reset-Fixture
if ($select.Invoke(0,[uint32]$hashes[1]) -ne 1 -or (Get-U 0x1c14) -ne $hashes[1] -or (Get-I 0x1c18) -ne 1111 -or (Get-I 0x1c1c) -ne 2222) { throw 'Same-family selection clobbered equipment' }
if ((Get-U 0x1c54) -ne $hashes[12]) { throw 'P1 overwrote P2 selection' }
if ($select.Invoke(1,[uint32]$hashes[2]) -ne 1 -or (Get-U 0x1c54) -ne $hashes[2] -or (Get-I 0x1c44) -ne 0x6e616873 -or (Get-U 0x1c58) -ne $weapons[0] -or (Get-U 0x1c5c) -ne $weapons[1]) { throw 'P2 cross-family defaults' }
if ((Get-I 0x1c60) -ne 3334 -or (Get-I 0x1c64) -ne 3) { throw 'P2 consumable and count changed' }
if ($select.Invoke(0,[uint32]$hashes[16]) -ne 1 -or (Get-U 0x1c14) -ne $hashes[16] -or (Get-I 0x1c04) -ne 0x69726f63 -or (Get-U 0x1c18) -ne $weapons[2] -or (Get-U 0x1c1c) -ne $weapons[3]) { throw 'P1 cross-family defaults' }
if ($select.Invoke(2,[uint32]$hashes[0]) -ne 0 -or $select.Invoke(1,0xfeed) -ne 0 -or (Get-U 0x1c54) -ne $hashes[2]) { throw 'Invalid slot or skin accepted' }
Write-Output 'Passed x86 selector tests: all 17 rows, source immutability, malformed/duplicate rejection, both players and families, compatible defaults, invalid inputs.'
