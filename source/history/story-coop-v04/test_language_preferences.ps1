$ErrorActionPreference='Stop'
$stage=Join-Path $PSScriptRoot 'preference-test'
$preference=Join-Path $stage 'launcher-settings.json'
$loadouts=Join-Path $stage 'loadouts.json'
. (Join-Path $stage 'Launcher-Preferences.ps1')
function Hash-File([string]$Path) {
    $hash=[Security.Cryptography.SHA256]::Create()
    try {return [BitConverter]::ToString($hash.ComputeHash([IO.File]::ReadAllBytes($Path)))} finally {$hash.Dispose()}
}
$initialLoadouts=Hash-File $loadouts
$cases=New-Object Collections.ArrayList
function Check-Startup([string]$Name,[string]$Expected) {
    $before=if(Test-Path -LiteralPath $preference){Hash-File $preference}else{$null}
    $output=& powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File (Join-Path $stage 'Coop-Launcher.ps1') -SmokeTest
    if($LASTEXITCODE -ne 0 -or ($output -join ' ') -notmatch ('startup='+$Expected+',')) {throw ('Startup case failed: '+$Name)}
    $after=if(Test-Path -LiteralPath $preference){Hash-File $preference}else{$null}
    if($before -ne $after -or (Hash-File $loadouts) -ne $initialLoadouts) {throw 'Smoke test modified real settings.'}
    if(@(Get-ChildItem -LiteralPath $stage -Filter '.smoke-language-*').Count -or @(Get-ChildItem -LiteralPath $stage -Filter '.launcher-language-*').Count) {throw 'Temporary preference files were not cleaned up.'}
    $null=$cases.Add(@{case=$Name;startup=$Expected;result='passed'})
}
if(Test-Path -LiteralPath $preference) {Remove-Item -LiteralPath $preference}
if((Get-SavedUiLanguage $preference) -ne 'en') {throw 'Fresh default must be English.'}
Check-Startup 'fresh install defaults to English' 'en'
Save-UiLanguage $preference 'zh'
if((Get-SavedUiLanguage $preference) -ne 'zh') {throw 'Chinese was not saved.'}
Check-Startup 'reopen restores Chinese' 'zh'
Save-UiLanguage $preference 'en'
if((Get-SavedUiLanguage $preference) -ne 'en') {throw 'English was not saved.'}
Check-Startup 'reopen restores English' 'en'
[IO.File]::WriteAllText($preference,'{invalid json')
Check-Startup 'malformed preference falls back to English' 'en'
[IO.File]::WriteAllText($preference,'{"format":1,"language":"fr"}')
Check-Startup 'unsupported preference falls back to English' 'en'
@{passed=$cases.Count;cases=@($cases);loadouts_unchanged=$true;dropdown_persistence_and_control_checks='passed in every startup test'} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'preference-tests.json') -Encoding UTF8
Write-Output ('PASS: '+$cases.Count+' startup/persistence cases, dropdown writes, settings unchanged, temporary files cleaned.')
