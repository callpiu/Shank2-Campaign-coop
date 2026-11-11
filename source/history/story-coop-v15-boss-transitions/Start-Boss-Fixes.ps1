$ErrorActionPreference='Stop'
throw 'Render prototype failed runtime validation (2026-11-06). Do not relaunch this build until the display hook is repaired. Released v0.8.3 remains unchanged.'
$running=Get-CimInstance Win32_Process -Filter "Name LIKE 'shank2%'"
if($running){throw 'Keep your progress: close the current Shank 2 window before starting this separate test.'}
$root=Join-Path (Split-Path $PSScriptRoot -Parent) 'story-coop-v14-transitions\game'
$source=Join-Path $PSScriptRoot 'combined\keyboard-chs.exe'
$records=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'combined-validation.json') -Raw | ConvertFrom-Json
$expected=@($records | Where-Object {$_.name -eq 'keyboard-chs.exe'})
if($expected.Count -ne 1){throw 'Expected exactly one keyboard Chinese test build.'}
if((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected.sha256){throw 'Test executable validation mismatch.'}
$target=Join-Path $root 'bin\shank2-coop-v15-boss-fixes-test.exe'
Copy-Item -LiteralPath $source -Destination $target
$oldApp=$env:SteamAppId;$oldGame=$env:SteamGameId
try{
 $env:SteamAppId='102840';$env:SteamGameId='102840'
 $p=Start-Process -FilePath $target -WorkingDirectory (Join-Path $root 'bin') -WindowStyle Normal -PassThru
 Write-Output ('Started isolated combined boss-fixes test PID '+$p.Id)
}finally{$env:SteamAppId=$oldApp;$env:SteamGameId=$oldGame}
