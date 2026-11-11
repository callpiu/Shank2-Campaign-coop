param([string]$Fixture)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required.' }
$reference = Join-Path (Split-Path -Parent $PSScriptRoot) 'story-coop-v11-retry-score\test_native.ps1'
$binding = [regex]::Match((Get-Content -LiteralPath $reference -Raw), "(?ms)^Add-Type @'\r?\n(.*?)\r?\n'@")
if (!$binding.Success) { throw 'Missing x86 fixture binding.' }
Add-Type -TypeDefinition $binding.Groups[1].Value
$base = 0x20000000
$mem = [RetryScoreTest]::VirtualAlloc([IntPtr]$base,[UIntPtr]::new(8192),0x3000,0x40)
if ($mem.ToInt32() -ne $base) { throw 'Cannot allocate fixture.' }
$bytes = [IO.File]::ReadAllBytes($Fixture)
function Read-Word([int]$Offset) { [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($base+$Offset)) }
function Write-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($base+$Offset),$Value) }
function Assert-Word([int]$Offset,[int]$Value) {
    if ((Read-Word $Offset) -ne $Value) { throw ("Unexpected fixture value at {0:x}: {1} (expected {2})" -f $Offset,(Read-Word $Offset),$Value) }
}
function Invoke-Case([int]$Entry,[int]$EventType,[int]$Value,[int]$Pickup,[int]$Combo,[int]$Reset) {
    [Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
    Write-Word 0x1000 $EventType
    Write-Word 0x1118 $Value
    if (([RetryScoreTest]::Bind($base+$Entry)).Invoke() -ne 0) { throw 'Stack imbalance.' }
    Assert-Word 0x1008 $Pickup
    Assert-Word 0x1014 $Combo
    Assert-Word 0x1020 $Reset
    Assert-Word 0x1024 1
    Assert-Word 0x1028 ($base+0x1100)
    if ($Pickup) {
        Assert-Word 0x100c $Value
        Assert-Word 0x1010 2
        Assert-Word 0x102c ($base+0x1200+0x638)
        Assert-Word 0x1030 -1
    }
    if ($Combo) {
        Assert-Word 0x1018 $Value
        Assert-Word 0x101c ($base+0x1500)
        Assert-Word 0x1034 ($base+0x1200+0x638)
    }
}
$grenade = -399534997
Invoke-Case 0 0x745e44a1 $grenade 1 1 0
Invoke-Case 0x40 0x745e44a1 $grenade 1 0 0
Invoke-Case 0x40 0x745e44a1 0x23456789 1 0 0
Invoke-Case 0x40 0x6e12f610 23 0 1 0
Invoke-Case 0x40 0x6e12f610 0 0 1 0
Invoke-Case 0x40 0x0f814409 0 0 0 1
Invoke-Case 0x40 0x12345678 0 0 0 0
Write-Output 'Reproduced the exact grenade-ID leak in the original x86 branch; fixed pickup, genuine combos, reset and event forwarding passed.'
