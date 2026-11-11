param([switch]$PrepareOnly)
$ErrorActionPreference='Stop'
if(!$PrepareOnly -and (Get-CimInstance Win32_Process -Filter "Name LIKE 'shank2%'")){
 throw 'Keep current progress: close the previous game before loading the new UI resources.'
}
$game=Join-Path (Split-Path $PSScriptRoot -Parent) 'story-coop-v14-transitions\game'
$record=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'build-validation.json') -Raw | ConvertFrom-Json
foreach($lang in @('en','chs')){
 $name='campaigncoopv20'+$lang+'.chui'
 $source=Join-Path $PSScriptRoot ('dev\'+$name)
 $sha=[Security.Cryptography.SHA256]::Create()
 try{$hash=[BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($source))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
 if($hash -ne $record.hud.$lang.sha256){throw ('HUD hash mismatch: '+$name)}
 Copy-Item -LiteralPath $source -Destination (Join-Path $game ('data-pc\ui\'+$name))
}
& (Join-Path (Split-Path $PSScriptRoot -Parent) 'story-coop-v18-prelevel-duo\Start-Prelevel-Test.ps1') -BuildDirectory $PSScriptRoot -Version 20 -PrepareOnly:$PrepareOnly
