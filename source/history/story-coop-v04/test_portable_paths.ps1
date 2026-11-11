param([string]$PackageRoot,[string]$SteamRoot,[string]$ExpectedGame,[string]$EmptyRoot)
$ErrorActionPreference='Stop'
. (Join-Path $PackageRoot 'Game-Paths.ps1')
$config=Join-Path $PackageRoot 'loadouts.json'
if(Test-Path -LiteralPath $config) {throw 'Path test requires a clean extracted package.'}
if(Find-ShankGameFolder $PackageRoot -SkipSystemDiscovery) {throw 'Empty discovery must not read host Steam locations.'}
$found=Find-ShankGameFolder $PackageRoot -SteamRoots @($SteamRoot) -SkipSystemDiscovery
if($found -ne $ExpectedGame) {throw ('Steam VDF/manifest discovery failed: '+$found)}
@{gamePath=$ExpectedGame} | ConvertTo-Json | Set-Content -LiteralPath $config -Encoding UTF8
if((Find-ShankGameFolder $PackageRoot -SkipSystemDiscovery) -ne $ExpectedGame) {throw 'Saved location was not restored.'}
@{gamePath=(Join-Path $EmptyRoot 'missing')} | ConvertTo-Json | Set-Content -LiteralPath $config -Encoding UTF8
if((Find-ShankGameFolder $PackageRoot -SteamRoots @($SteamRoot) -SkipSystemDiscovery) -ne $ExpectedGame) {throw 'Invalid saved location prevented Steam fallback.'}
Remove-Item -LiteralPath $config
if((Find-ShankGameFolder $ExpectedGame -SkipSystemDiscovery) -ne $ExpectedGame) {throw 'Package/game folder detection failed.'}
Write-Output 'PASS: clean fallback, Unicode Steam library/manifest, saved path, stale saved path, game-folder location.'
