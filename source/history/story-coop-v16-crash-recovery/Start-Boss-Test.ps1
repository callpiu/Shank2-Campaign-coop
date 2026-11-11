param([switch]$PrepareOnly)
$ErrorActionPreference='Stop'
$running=Get-CimInstance Win32_Process -Filter "Name LIKE 'shank2%'"
if($running){throw 'A Shank 2 window is already running; preserve current progress.'}
$root=Join-Path (Split-Path $PSScriptRoot -Parent) 'story-coop-v14-transitions\game'
$source=Join-Path $PSScriptRoot 'dev\keyboard-chs.exe'
$records=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'build-validation.json') -Raw | ConvertFrom-Json
$expected=@($records | Where-Object {$_.name -eq 'keyboard-chs.exe'})
if($expected.Count -ne 1){throw 'Expected one exact test build.'}
$sha=[Security.Cryptography.SHA256]::Create()
try{$digest=[BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($source))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
if($digest -ne $expected[0].sha256){throw 'Test executable checksum mismatch.'}
$test=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'deferred-validation.json') -Raw | ConvertFrom-Json
if(!$test.passed -or $test.old_implementation_escaped_stack_pointers -ne 2){throw 'Lifetime regression did not pass.'}
$target=Join-Path $root 'bin\shank2-coop-v16-boss-fixes-test.exe'
Copy-Item -LiteralPath $source -Destination $target
if($PrepareOnly){Write-Output $target;return}
$oldApp=$env:SteamAppId;$oldGame=$env:SteamGameId
try{
 $env:SteamAppId='102840';$env:SteamGameId='102840'
 $p=Start-Process -FilePath $target -WorkingDirectory (Join-Path $root 'bin') -WindowStyle Normal -PassThru
 Write-Output ('Started isolated v16 boss test PID '+$p.Id)
 $python=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
 & $python (Join-Path $PSScriptRoot 'install_assist.py') $p.Id
 if($LASTEXITCODE -ne 0){throw 'Test window started, but assistance failed. Keep the window and diagnose; do not silently test without assistance.'}
}finally{$env:SteamAppId=$oldApp;$env:SteamGameId=$oldGame}
