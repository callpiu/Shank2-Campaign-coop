param([string]$GamePath,[switch]$SmokeTest)
$ErrorActionPreference='Stop'
$argsForSettings=@{SmokeTest=$SmokeTest}
if ($GamePath) { $argsForSettings.GamePath=$GamePath }
& (Join-Path $PSScriptRoot 'Coop-Key-Settings.ps1') @argsForSettings
