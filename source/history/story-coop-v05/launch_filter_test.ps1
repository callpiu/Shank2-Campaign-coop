$ErrorActionPreference='Stop'
$testRoot='G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test'
$target=Join-Path $testRoot 'bin\shank2-coop-v05-menu-enter-test.exe'
$live=Get-CimInstance Win32_Process -Filter "ProcessId=16004"
if($live) {
    if($live.ExecutablePath -ne $target) {throw 'Unexpected process; refusing to stop.'}
    $process=Get-Process -Id 16004
    Stop-Process -Id 16004
    if(-not $process.WaitForExit(5000)) {throw 'Test game has not exited.'}
}
$bytes=[IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'shank2-coop-v05-menu-test.exe'))
$snapshot=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'enter-runtime-confirmed.json') -Raw | ConvertFrom-Json
$hex=$snapshot.config
for($i=0;$i -lt 128;$i++) {$bytes[4140032+$i]=[Convert]::ToByte($hex.Substring($i*2,2),16)}
[IO.File]::WriteAllBytes($target,$bytes)
$oldApp=$env:SteamAppId;$oldGame=$env:SteamGameId
try {
    $env:SteamAppId='102840';$env:SteamGameId='102840'
    $process=Start-Process -FilePath $target -WorkingDirectory (Join-Path $testRoot 'bin') -PassThru
    Write-Output ('TEST_PID='+$process.Id)
} finally {$env:SteamAppId=$oldApp;$env:SteamGameId=$oldGame}
