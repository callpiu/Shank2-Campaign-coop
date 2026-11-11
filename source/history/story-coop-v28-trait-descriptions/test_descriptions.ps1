param([string]$Fixture,[string]$CasesPath)
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
[Runtime.InteropServices.Marshal]::Copy($b,0,$mem,$b.Length)
function Write-Word([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($base+$Offset),$Value) }
function Read-Word([int]$Offset) { [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($base+$Offset)) }
function Bits($Value) { [BitConverter]::ToInt32([BitConverter]::GetBytes([uint32]$Value),0) }
function Invoke-Case([int]$Entry,[int]$Expected) {
    $out=([RetryScoreTest]::Bind($base+$Entry)).Invoke()
    if ($out -ne $Expected) { throw ('Entry '+$Entry+' returned '+$out+'; expected '+$Expected) }
}
$caseRows=Get-Content -LiteralPath $CasesPath -Raw | ConvertFrom-Json
foreach ($row in $caseRows) {
    Write-Word 0x5580 (Bits $row.hash)
    Invoke-Case 0x1000 ([int]$row.expected)
    if ((Read-Word 0x7008) -ne ($base+0x8000)) { throw 'Wrong owning screen.' }
}
foreach ($mode in @(0,2)) { Write-Word 0x5004 $mode; Invoke-Case 0x1000 ($base+0x5570) }
Write-Word 0x5004 1
Write-Word 0x8020 1
Invoke-Case 0x1000 ($base+0x5570)
Write-Word 0x8020 3
Write-Word 0x5580 12345
Invoke-Case 0x1000 ($base+0x5570)
Invoke-Case 0x1100 ($base+0xa090)
$horror=$caseRows | Where-Object name -eq 'horror'
if ((Read-Word 0x7000) -ne $horror.expected) { throw 'Selection did not refresh summary.' }
Invoke-Case 0x1200 0x777
if ((Read-Word 0x7018) -ne 0x1234) { throw 'Native apply argument changed.' }
$corina=$caseRows | Where-Object name -eq 'corina'
if ((Read-Word 0x7000) -ne $corina.expected) { throw 'Second player initial row not refreshed.' }
Invoke-Case 0x1340 123
if ((Read-Word 0x7000) -ne ($base+0x5570)) { throw 'Summary remained on equipment page.' }
Invoke-Case 0x1300 123
if ((Read-Word 0x7000) -ne $corina.expected) { throw 'Summary did not return on character page.' }
foreach ($initial in $caseRows) {
    Write-Word 0x8020 0
    Write-Word 0x81e8 (Bits $initial.hash)
    Invoke-Case 0x1200 0x777
    if ((Read-Word 0x7000) -ne ($base+0x5570)) { throw 'Population did not start with a clear hidden summary.' }
    Invoke-Case 0x1380 123
    if ((Read-Word 0x8020) -ne 3 -or (Read-Word 0x7000) -ne ($base+0x5570)) { throw 'Old first-show bypass was not reproduced.' }
    Write-Word 0x8020 0
    Invoke-Case 0x1200 0x777
    Invoke-Case 0x13c0 123
    if ((Read-Word 0x8020) -ne 3 -or (Read-Word 0x7000) -ne $initial.expected) { throw ('First-show text missing for '+$initial.name) }
}
Write-Output 'Old first-show failure reproduced; all 17 initial summaries now display without selection events.'
Write-Output 'Native trait column lookup, callbacks, per-player initialization, visibility and registers passed.'
