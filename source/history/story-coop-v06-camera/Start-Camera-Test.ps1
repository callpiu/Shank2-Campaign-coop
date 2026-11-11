$ErrorActionPreference='Stop'
if(Get-CimInstance Win32_Process -Filter "Name like 'shank2%'" | Select-Object -First 1) {throw 'Close the current Shank 2 game before starting this isolated development test.'}
$testRoot='G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test'
$bin=Join-Path $testRoot 'bin'
if(!(Test-Path -LiteralPath (Join-Path $bin 'shank2.exe'))) {throw 'The isolated full test game is missing.'}
$target=Join-Path $bin 'shank2-coop-v06-camera-test.exe'
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'shank2-coop-v06-camera-test.exe') -Destination $target
$oldApp=$env:SteamAppId;$oldGame=$env:SteamGameId
try {
    $env:SteamAppId='102840';$env:SteamGameId='102840'
    $game=Start-Process -FilePath $target -WorkingDirectory $bin -WindowStyle Hidden -PassThru
    Write-Output ('Camera development test PID '+$game.Id+'. F7 toggles shared framing; F6 remains manual recall.')
} finally {$env:SteamAppId=$oldApp;$env:SteamGameId=$oldGame}
