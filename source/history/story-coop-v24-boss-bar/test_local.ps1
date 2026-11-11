param([string]$Fixture)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required.' }
$reference = Join-Path (Split-Path -Parent $PSScriptRoot) 'story-coop-v11-retry-score\test_native.ps1'
$ffi = [regex]::Match((Get-Content -LiteralPath $reference -Raw), "(?ms)^Add-Type @'\r?\n(.*?)\r?\n'@")
if (!$ffi.Success) { throw 'Missing test FFI.' }
Add-Type -TypeDefinition $ffi.Groups[1].Value
$base = 0x20000000
$mem = [RetryScoreTest]::VirtualAlloc([IntPtr]$base,[UIntPtr]::new(0x5000),0x3000,0x40)
if ($mem.ToInt32() -ne $base) { throw 'Fixture allocation failed.' }
$bytes = [IO.File]::ReadAllBytes($Fixture)
function Reset { [Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length) }
function Write-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($base+$Offset),$Value) }
function Assert-Word([int]$Offset,[int]$Value) {
    $actual = [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($base+$Offset))
    if ($actual -ne $Value) { throw ('Expected '+$Value+', got '+$actual+' at '+$Offset) }
}
function Invoke-Code([int]$Offset,[int]$Expected) {
    $actual = ([RetryScoreTest]::Bind($base+$Offset)).Invoke()
    if ($actual -ne $Expected) { throw ('Return mismatch at '+$Offset+': '+$actual) }
}
$hud = $base+0x313c
Reset
Invoke-Code 0 $hud
Invoke-Code 0x40 $hud
Invoke-Code 0x80 1
Invoke-Code 0xc0 1
Assert-Word 0x410c 41
Assert-Word 0x4100 2

Reset
Invoke-Code 0x40 $hud
Invoke-Code 0 0
Invoke-Code 0xc0 1
Invoke-Code 0x80 0
Assert-Word 0x410c 51
Assert-Word 0x4100 1
Assert-Word 0x4104 1
Assert-Word 0x4108 1
Assert-Word 0x31a0 $hud
Write-Word 0x4110 1
Invoke-Code 0xc0 0
Assert-Word 0x31a0 ($base+0x30e0)
Invoke-Code 0 $hud
Assert-Word 0x4100 2

foreach ($case in @(@(0x1004,0),@(0x1010,0),@(0x1010,1),@(0x2000,($base+0x4300)))) {
    Reset
    Write-Word $case[0] $case[1]
    Invoke-Code 0x40 $hud
    Invoke-Code 0 $hud
    Assert-Word 0x4100 2
    Assert-Word 0x4108 0
}
Write-Output 'x86 cases passed: overlapping old actions share a bar, duplicate suppressed in co-op, first action completes, later action works, non-co-op paths preserved.'
