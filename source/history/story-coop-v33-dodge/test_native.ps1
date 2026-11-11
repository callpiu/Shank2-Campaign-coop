param([string]$Fixture)
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw 'x86 required.' }
$reference=Join-Path (Split-Path -Parent $PSScriptRoot) 'story-coop-v11-retry-score\test_native.ps1'
$binding=[regex]::Match((Get-Content -LiteralPath $reference -Raw),"(?ms)^Add-Type @'\r?\n(.*?)\r?\n'@")
Add-Type -TypeDefinition $binding.Groups[1].Value
$base=0x20000000
$mem=[RetryScoreTest]::VirtualAlloc([IntPtr]$base,[UIntPtr]::new(0x10000),0x3000,0x40)
if ($mem.ToInt32() -ne $base) { throw 'Allocation failed.' }
$raw=[IO.File]::ReadAllBytes($Fixture)
[Runtime.InteropServices.Marshal]::Copy($raw,0,$mem,$raw.Length)
function W([int]$Offset,[int]$Value) { [Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($base+$Offset),$Value) }
function Read-Word([int]$Offset) { [Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($base+$Offset)) }
$cases=@(
    @(0,0,123,0,@(0x5a),-32767), @(0,0,123,0,@(0x43),32767),
    @(0,1,123,0,@(0x68),-32767), @(0,1,123,0,@(0x69),32767),
    @(0,0,123,0,@(0x5a,0x43),0), @(0,1,123,0,@(),0),
    @(0,0,123,0,@(0x68),0), @(0,1,123,0,@(0x5a),0),
    @(1,0,123,0,@(0x5a),111), @(0,2,123,0,@(0x5a),111),
    @(0,0,999,0,@(0x5a),111), @(0,0,123,87,@(0x5a),111)
)
foreach($case in $cases) {
    W 0x5084 $case[0]; W 0x700c $case[1]; W 0x7004 $case[2]; W 0x7000 $case[3]
    foreach($key in @(0x5a,0x43,0x68,0x69)) { W (0xa000+4*$key) 0 }
    foreach($key in $case[4]) { W (0xa000+4*$key) 0x8000 }
    W 0x8000 2468; W 0x8004 0x12345678; W 0x8008 0x01230456; W 0x800c ((321 -shl 16)+111)
    $result=([RetryScoreTest]::Bind($base+0x1100)).Invoke()
    if ($result -ne $case[3]) { throw 'Return value/registers changed.' }
    $rx=[Runtime.InteropServices.Marshal]::ReadInt16([IntPtr]($base+0x800c))
    if ($rx -ne $case[5]) { throw "Wrong dodge direction: $rx expected $($case[5])" }
    if ((Read-Word 0x8000) -ne 2468 -or (Read-Word 0x8004) -ne 0x12345678 -or (Read-Word 0x8008) -ne 0x01230456) { throw 'Existing controls modified.' }
    if ([Runtime.InteropServices.Marshal]::ReadInt16([IntPtr]($base+0x800e)) -ne 321) { throw 'Right stick Y modified.' }
}
Write-Output 'Native x86 dodge direction, per-player independence, both-key cancel, focus, physical passthrough and registers passed.'
