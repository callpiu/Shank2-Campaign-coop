param([string]$OldFixture,[string]$NewFixture,[string]$Ids,[string]$Report)
$ErrorActionPreference='Stop'
$layoutReport=$Report
. (Join-Path (Split-Path $PSScriptRoot -Parent) 'story-coop-v19-character-first\test_order.ps1') $NewFixture $Ids ($Report+'.order.json') 0x20003350
$oldBytes=[IO.File]::ReadAllBytes($OldFixture)
[Runtime.InteropServices.Marshal]::Copy($oldBytes,0,$mem,$oldBytes.Length)
$null=$run.Invoke(0)
if((Get-U 0x8020) -ne 3 -or (Get-U 0x3f20) -ne 0 -or (Get-U 0x3f24) -ne 0){throw 'Original incomplete-OnShow regression was not reproduced'}
Reset;$null=$run.Invoke(0)
if((Get-U 0x8020) -ne 3 -or (Get-U 0x3f20) -ne 1 -or (Get-U 0x3f24) -ne 7){throw 'Character panel reset or weapon metadata incomplete'}
if((Get-U 0x3e08) -ne 0 -or (Get-U 0x3028) -ne 0){throw 'Initialization triggered a selection callback'}
Assert-OriginalConfig
Role $shank
if((Get-U 0x8020) -ne 0 -or (Get-U 0x3f20) -ne 0){throw 'Role confirm did not return to native weapon panel'}
Equipment 111 222 333;$null=$run.Invoke(2)
if((Get-U 0x3014) -ne 1 -or (Get-U 0x3f20) -ne 1 -or (Get-U 0x3f24) -ne 7){throw 'P2 character introduction not initialized after refresh'}
@{passed=$true;old_issue_reproduced=$true;both_players_info_panel_initialized=$true;
 all_three_weapon_metadata_initialized=$true;no_gameplay_callbacks_during_initialization=$true;
 role_first_regressions=27;gameplay_verified=$false} |
 ConvertTo-Json | Set-Content -LiteralPath $layoutReport -Encoding UTF8
Write-Output 'PASS: reproduced old panel reset/missing metadata, complete P1/P2 initialization, and 27 role-first regressions.'
