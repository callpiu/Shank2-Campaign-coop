param([string]$Fixture)
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required.' }
$reference=Join-Path (Split-Path -Parent $PSScriptRoot) 'story-coop-v11-retry-score\test_native.ps1'
$binding=[regex]::Match((Get-Content -LiteralPath $reference -Raw),"(?ms)^Add-Type @'\r?\n(.*?)\r?\n'@")
if (!$binding.Success) { throw 'Missing x86 bindings.' }
Add-Type -TypeDefinition $binding.Groups[1].Value
$base=0x20000000
$mem=[RetryScoreTest]::VirtualAlloc([IntPtr]$base,[UIntPtr]::new(0x4000),0x3000,0x40)
if ($mem.ToInt32() -ne $base) { throw 'Fixture allocation failed.' }
$b=[IO.File]::ReadAllBytes($Fixture)
function Reset { [Runtime.InteropServices.Marshal]::Copy($b,0,$mem,$b.Length) }
function Write-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($base+$Offset),$Value) }
function Assert-Word([int]$Offset,[int]$Value) {
    $actual=[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($base+$Offset))
    if ($actual -ne $Value) { throw ('Expected '+$Value+', got '+$actual+' at '+$Offset) }
}
function Invoke-Case([int]$Entry,[int]$Expected) {
    $out=([RetryScoreTest]::Bind($base+$Entry)).Invoke()
    if ($out -ne $Expected) { throw ('Entry '+$Entry+' returned '+$out+'; expected '+$Expected) }
}
Reset
Invoke-Case 0x1000 1
Invoke-Case 0x1040 1
Invoke-Case 0x1080 1
Invoke-Case 0x10c0 0
Invoke-Case 0x1300 0
Invoke-Case 0x1340 0
Invoke-Case 0x1380 0
foreach ($case in @(@(0x2004,0),@(0x2604,1),@(0x28a0,0),@(0x2610,0))) {
    Reset
    Write-Word $case[0] $case[1]
    Invoke-Case 0x1040 0
    Invoke-Case 0x1080 1
    Invoke-Case 0x1140 1234
    Assert-Word 0x2420 0
}
Reset
Write-Word 0x2604 2
Invoke-Case 0x1100 1234
Assert-Word 0x2400 1
Assert-Word 0x2404 0x42c80000
Assert-Word 0x2408 0x42c80000
Assert-Word 0x2420 0
Write-Word 0x2604 4
Invoke-Case 0x1140 1234
Assert-Word 0x2420 1
Assert-Word 0x2424 0x42c80000
Write-Word 0x2604 5
Invoke-Case 0x1200 0x41700000
Invoke-Case 0x1280 0x41700000
Assert-Word 0x240c 1
Assert-Word 0x2414 0x3fc00000
Assert-Word 0x2418 0x41200000
Assert-Word 0x241c 0x41700000
Assert-Word 0x242c 1
Reset
Write-Word 0x2004 0
Invoke-Case 0x1280 0x41700000
Assert-Word 0x242c 0
Reset
Write-Word 0x28a0 0
Invoke-Case 0x1380 0
Write-Output 'x86 traits passed: registered actors, reject component impostors, both slots, spawn HP, damage-tag replay, and native passthrough.'
