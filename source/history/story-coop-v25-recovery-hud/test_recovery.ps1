param([string]$Fixture)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required.' }
$reference = Join-Path (Split-Path -Parent $PSScriptRoot) 'story-coop-v11-retry-score\test_native.ps1'
$binding = [regex]::Match((Get-Content -LiteralPath $reference -Raw), "(?ms)^Add-Type @'\r?\n(.*?)\r?\n'@")
if (!$binding.Success) { throw 'Missing test bindings.' }
Add-Type -TypeDefinition $binding.Groups[1].Value
$base = 0x20000000
$mem = [RetryScoreTest]::VirtualAlloc([IntPtr]$base,[UIntPtr]::new(0x2000),0x3000,0x40)
if ($mem.ToInt32() -ne $base) { throw 'Fixture allocation failed.' }
$bytes = [IO.File]::ReadAllBytes($Fixture)
function Reset { [Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length) }
function Write-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($base+$Offset),$Value) }
function Assert-Word([int]$Offset,[int]$Value) {
    $actual = [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($base+$Offset))
    if ($actual -ne $Value) { throw ('Expected '+$Value+', got '+$actual+' at '+$Offset) }
}
function Invoke-Fixture([int]$Entry,[int]$Calls,[int]$Remaining) {
    if (([RetryScoreTest]::Bind($base+$Entry)).Invoke() -ne 0x1234) { throw 'Stack/return mismatch.' }
    Assert-Word 0x1100 $Calls
    Assert-Word 0x1110 0
    Assert-Word 0x1114 $Remaining
}
Reset
Invoke-Fixture 0x40 1 3
Assert-Word 0x1104 0x8ec3ab67
Reset
Invoke-Fixture 0 3 0
Assert-Word 0x1104 0xe824cec2
Assert-Word 0x1108 0x748537b7
Assert-Word 0x110c 0x8ec3ab67
foreach ($case in @(@(0x14a0,0x41a00000),@(0x14a0,0),@(0x14a0,0x7fc00000),@(0x1600,0),@(0x1004,0),@(0x100c,($base+0x1300)),@(0x1024,0x4343),@(0x1118,1),@(0x1120,0),@(0x1124,0),@(0x111c,0x12345678))) {
    Reset
    Write-Word $case[0] $case[1]
    Invoke-Fixture 0 1 3
}
Write-Output 'x86 recovery cases passed: stale screen effects cleared for recovered P2, native stops and other contexts retained.'
