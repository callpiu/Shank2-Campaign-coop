$ErrorActionPreference = 'Stop'
if (Get-Process shank* -ErrorAction SilentlyContinue) {
    throw 'Close the running Shank 2 window before starting the isolated probe.'
}
$bin = 'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test\bin'
if (!(Test-Path -LiteralPath (Join-Path $bin 'shank2-coop-v09-fixes-test.exe') -PathType Leaf)) {
    throw 'The isolated test game is unavailable.'
}
$name = 'shank2-coop-cyclops-probe.exe'
$target = Join-Path $bin $name
Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination $target
$previousApp = $env:SteamAppId
$previousGame = $env:SteamGameId
try {
    $env:SteamAppId = '102840'
    $env:SteamGameId = '102840'
    $p = Start-Process -FilePath $target -WorkingDirectory $bin -PassThru
    Write-Output "Cyclops probe PID: $($p.Id)"
} finally {
    $env:SteamAppId = $previousApp
    $env:SteamGameId = $previousGame
}
