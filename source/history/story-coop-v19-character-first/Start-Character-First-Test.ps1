param([switch]$PrepareOnly)
$ErrorActionPreference='Stop'
& (Join-Path (Split-Path $PSScriptRoot -Parent) 'story-coop-v18-prelevel-duo\Start-Prelevel-Test.ps1') -BuildDirectory $PSScriptRoot -Version 19 -PrepareOnly:$PrepareOnly
