param([string]$Fixture)
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 process required.' }
$reference=Join-Path (Split-Path -Parent $PSScriptRoot) 'story-coop-v11-retry-score\test_native.ps1'
$binding=[regex]::Match((Get-Content -LiteralPath $reference -Raw),"(?ms)^Add-Type @'\r?\n(.*?)\r?\n'@")
if (!$binding.Success) { throw 'Missing x86 bindings.' }
Add-Type -TypeDefinition $binding.Groups[1].Value
$base=0x20000000
$mem=[RetryScoreTest]::VirtualAlloc([IntPtr]$base,[UIntPtr]::new(0x10000),0x3000,0x40)
if ($mem.ToInt32() -ne $base) { throw 'Fixture allocation failed.' }
$b=[IO.File]::ReadAllBytes($Fixture)
function Reset { [Runtime.InteropServices.Marshal]::Copy($b,0,$mem,$b.Length) }
function Write-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($base+$Offset),$Value) }
function Read-Word([int]$Offset) { [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($base+$Offset)) }
function Assert-Word([int]$Offset,[int]$Expected) {
    $actual=Read-Word $Offset
    if ($actual -ne $Expected) { throw ('Expected '+$Expected+', got '+$actual+' at '+$Offset) }
}
function Invoke-Case([int]$Entry,[int]$Expected) {
    $out=([RetryScoreTest]::Bind($base+$Entry)).Invoke()
    if ($out -ne $Expected) { throw ('Entry '+$Entry+' returned '+$out+'; expected '+$Expected) }
}
# Same P2, same factor, same continuation; original gate skips campaign.
Reset
Invoke-Case 0x900 0x41200000
Assert-Word 0x8408 0
Invoke-Case 0xa00 0x41500000
Assert-Word 0x8408 1
Assert-Word 0x8308 ($base+0x8100)
# Each registered player uses its own factor.
Write-Word 0x8308 ($base+0x8000)
Invoke-Case 0xa00 0x40e00000
Assert-Word 0x8308 ($base+0x8000)
Assert-Word 0x8408 2
# Survival's native positive result bypasses the added campaign checks.
foreach ($entry in @(0x900,0xa00)) {
    Reset
    Write-Word 0x7004 0
    Write-Word 0x8400 1
    Invoke-Case $entry 0x41500000
    Assert-Word 0x8408 1
}
foreach ($case in @(@(0x7004,0),@(0x7804,1),@(0x8120,0),@(0x8308,$base+0x8200),@(0x8308,0))) {
    Reset
    Write-Word $case[0] $case[1]
    $actor=Read-Word 0x8308
    Invoke-Case 0xa00 0x41200000
    Assert-Word 0x8408 0
    Assert-Word 0x8308 $actor
}
Write-Output 'x86 projectile gate passed: original failure, P2 x1.30, P1 isolation, Survival, rejected contexts, unchanged actor and preserved registers.'
