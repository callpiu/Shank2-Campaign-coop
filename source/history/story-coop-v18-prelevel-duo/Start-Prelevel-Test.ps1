param([switch]$PrepareOnly,[string]$BuildDirectory=$PSScriptRoot,[int]$Version=18)
$ErrorActionPreference='Stop'
$buildRoot=[IO.Path]::GetFullPath($BuildDirectory)
if(!$PrepareOnly -and (Get-CimInstance Win32_Process -Filter "Name LIKE 'shank2%'")){
 throw 'Keep current progress: close the previous game before launching this separate test.'
}
$root=Join-Path (Split-Path $buildRoot -Parent) 'story-coop-v14-transitions\game'
$records=Get-Content -LiteralPath (Join-Path $buildRoot 'builds.json') -Raw | ConvertFrom-Json
$expected=@($records | Where-Object {$_.name -eq 'keyboard-chs.exe'})
if($expected.Count -ne 1){throw 'Expected one exact test build.'}
$flowCheck=if($Version -eq 20){'layout-validation.json'}elseif($Version -eq 19){'order-validation.json'}else{'flow-validation.json'}
foreach($check in @($flowCheck,'image-load-validation.json')){
 $r=Get-Content -LiteralPath (Join-Path $buildRoot $check) -Raw | ConvertFrom-Json
 if(!$r.passed){throw ('Required test failed: '+$check)}
}
$source=Join-Path $buildRoot 'dev\keyboard-chs.exe'
$sha=[Security.Cryptography.SHA256]::Create()
try{$digest=[BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($source))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
if($digest -ne $expected[0].sha256){throw 'Test executable checksum mismatch.'}
$target=Join-Path $root ('bin\shank2-coop-v'+$Version+'-prelevel-test.exe')
Copy-Item -LiteralPath $source -Destination $target
$build=Get-Content -LiteralPath (Join-Path $buildRoot 'build-validation.json') -Raw | ConvertFrom-Json
foreach($language in @('en','chs')){
 $name='cooppreselv'+$Version+$language+'.chui'
 $asset=Join-Path $buildRoot ('dev\'+$name)
 $hash=[Security.Cryptography.SHA256]::Create()
 try{$assetHash=[BitConverter]::ToString($hash.ComputeHash([IO.File]::ReadAllBytes($asset))).Replace('-','').ToLowerInvariant()}finally{$hash.Dispose()}
 if($assetHash -ne $build.ui.$language.sha256){throw ('UI checksum mismatch: '+$name)}
 Copy-Item -LiteralPath $asset -Destination (Join-Path $root ('data-pc\ui\'+$name))
}
if($PrepareOnly){Write-Output ('Prepared exact test and two added UI assets: '+$target);return}
$oldApp=$env:SteamAppId;$oldGame=$env:SteamGameId
try{
 $env:SteamAppId='102840';$env:SteamGameId='102840'
 $p=Start-Process -FilePath $target -WorkingDirectory (Join-Path $root 'bin') -WindowStyle Normal -PassThru
 Write-Output ('Started isolated pre-level test PID '+$p.Id)
 $python=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
 & $python (Join-Path $buildRoot 'install_assist.py') $p.Id
 if($LASTEXITCODE -ne 0){throw 'Test window started, but assistance failed; preserve this window and diagnose.'}
}finally{$env:SteamAppId=$oldApp;$env:SteamGameId=$oldGame}
