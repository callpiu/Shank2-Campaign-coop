$ErrorActionPreference='Stop'
$testRoot='G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test'
$oldTest=Join-Path $testRoot 'bin\shank2-coop-v07-dialogue-test.exe'
$newTest=Join-Path $testRoot 'bin\shank2-coop-v07-background-test.exe'
$active=@(Get-CimInstance Win32_Process -Filter "Name like 'shank2%'")
if(@($active | Where-Object {$_.ExecutablePath -notin @($oldTest,$newTest)}).Count){throw 'A different Shank 2 game is running; it was left untouched.'}
foreach($game in $active) {
 $process=Get-Process -Id $game.ProcessId
 Stop-Process -Id $game.ProcessId
 if(-not $process.WaitForExit(5000)){throw 'The old isolated test has not exited.'}
}
$manifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'enhanced-manifest.json') -Raw | ConvertFrom-Json
if(!$manifest.complete -or $manifest.files.Count -ne 27){throw 'Enhanced movie set is incomplete.'}
$folder=Join-Path $testRoot 'data\movies\coop_dialogue_enhanced'
$null=New-Item -ItemType Directory -Path $folder -Force
foreach($row in $manifest.files) {
 $source=Join-Path (Join-Path $PSScriptRoot 'enhanced') $row.file
 $target=Join-Path $folder $row.file
 if((Get-FileHash -LiteralPath $source).Hash -ne $row.output_sha256){throw ('Damaged enhanced source: '+$row.file)}
 if((Test-Path -LiteralPath $target) -and (Get-FileHash -LiteralPath $target).Hash -ne $row.output_sha256){throw ('Unrecognized enhanced target: '+$row.file)}
 Copy-Item -LiteralPath $source -Destination $target
}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'shank2-coop-v07-background-test.exe') -Destination $newTest
$oldApp=$env:SteamAppId;$oldGame=$env:SteamGameId
try {
 $env:SteamAppId='102840';$env:SteamGameId='102840'
 $game=Start-Process -FilePath $newTest -WorkingDirectory (Join-Path $testRoot 'bin') -WindowStyle Hidden -PassThru
 Write-Output ('BACKGROUND_TEST_PID='+$game.Id)
} finally {$env:SteamAppId=$oldApp;$env:SteamGameId=$oldGame}
