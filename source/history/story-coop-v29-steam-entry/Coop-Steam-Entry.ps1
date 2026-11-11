param(
    [ValidateSet('Enable','Disable','Sync','Verify')][string]$Action='Enable',
    [string]$GamePath=(Split-Path -Parent $PSScriptRoot)
)
$ErrorActionPreference='Stop'
$stockSha='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
$game=(Resolve-Path -LiteralPath $GamePath).Path.TrimEnd('\')
$steamExe=Join-Path $game 'bin\shank2.exe'
$modExe=Join-Path $game 'bin\shank2-story-coop.exe'
$meta=Join-Path $game '.storycoop-steam'
$statePath=Join-Path $meta 'state.json'
$original=Join-Path $meta 'shank2.original.exe'
$buildsPath=Join-Path $PSScriptRoot 'steam-entry-builds.json'

function Hash([string]$Path) {
    $stream=[IO.File]::OpenRead($Path)
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { ([BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
    finally { $stream.Dispose(); $algorithm.Dispose() }
}
function Write-Atomic([string]$Path,[byte[]]$Bytes) {
    $temporary=$Path+'.steam-entry-'+[Guid]::NewGuid().ToString('N')+'.tmp'
    try {
        [IO.File]::WriteAllBytes($temporary,$Bytes)
        if (Test-Path -LiteralPath $Path) { [IO.File]::Replace($temporary,$Path,[NullString]::Value) }
        else { [IO.File]::Move($temporary,$Path) }
    } finally {
        if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Force }
    }
}
function Read-State {
    if (Test-Path -LiteralPath $statePath) {
        $s=Get-Content -LiteralPath $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($s.Version -ne 1 -or $s.OriginalSHA256 -ne $stockSha) { throw 'Unrecognized Steam entry receipt.' }
        return $s
    }
    return $null
}
function Refuse-RunningGame {
    $prefix=$game+'\'
    foreach ($proc in @([Diagnostics.Process]::GetProcesses() | Where-Object {$_.ProcessName -like 'shank2*'})) {
        try { $imagePath=$proc.MainModule.FileName } catch { throw 'Cannot inspect a running Shank process; preserve it and retry after it exits.' }
        if ($imagePath -and $imagePath.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase)) {
            throw 'Shank 2 is running in this installation. Exit it before changing the Steam entry.'
        }
    }
}

if (!(Test-Path -LiteralPath $steamExe -PathType Leaf)) { throw 'Steam game entry bin\shank2.exe was not found.' }
$state=Read-State
$current=Hash $steamExe
if ($Action -eq 'Verify') {
    $enabled=$state -and $state.Enabled
    $active=$enabled -and ($current -eq $state.ActiveModSHA256)
    [PSCustomObject]@{Enabled=[bool]$enabled;Active=[bool]$active;SteamEntrySHA256=$current;
        OriginalBackupValid=((Test-Path -LiteralPath $original) -and ((Hash $original) -eq $stockSha));
        ReenableRequired=[bool]($enabled -and ($current -eq $stockSha));
        EntryMatchesDirectMOD=([bool]((Test-Path -LiteralPath $modExe) -and ($current -eq (Hash $modExe))))} | ConvertTo-Json
    exit 0
}
if ($Action -eq 'Sync' -and !($state -and $state.Enabled)) {
    [PSCustomObject]@{Enabled=$false;Synced=$false;Reason='Steam integration is disabled.'} | ConvertTo-Json
    exit 0
}
Refuse-RunningGame
[IO.Directory]::CreateDirectory($meta) | Out-Null
$lock=Join-Path $meta 'update.lock'
$lockStream=[IO.File]::Open($lock,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {
    # Re-read inside the lock; reject foreign edits rather than overwriting them.
    $state=Read-State
    $current=Hash $steamExe
    if ($current -ne $stockSha -and !($state -and $state.Enabled -and ($current -eq $state.ActiveModSHA256))) {
        throw 'Steam entry differs from both the original and the recorded MOD. No files changed.'
    }
    if ($Action -eq 'Disable') {
        if ($current -ne $stockSha -and (!(Test-Path -LiteralPath $original) -or (Hash $original) -ne $stockSha)) {
            throw 'Verified original backup is missing. No files changed.'
        }
        if ($current -eq $stockSha) { $payload=[IO.File]::ReadAllBytes($steamExe) }
        else { $payload=[IO.File]::ReadAllBytes($original) }
        $newState=[ordered]@{Version=1;Enabled=$false;AppID=102840;OriginalSHA256=$stockSha;ActiveModSHA256=$null}
        $expected=$stockSha
    } else {
        if (!(Test-Path -LiteralPath $modExe -PathType Leaf)) { throw 'Install the direct MOD before enabling its Steam entry.' }
        $modSha=Hash $modExe
        $builds=Get-Content -LiteralPath $buildsPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $knownBuilds=@($builds | Where-Object {$_.SHA256 -eq $modSha})
        if ($knownBuilds.Count -ne 1 -or $knownBuilds[0].TestAssists) { throw 'MOD build is not an allowlisted clean build.' }
        foreach ($asset in $knownBuilds[0].Assets) {
            if ($asset.Name -notmatch '^[A-Za-z0-9_.-]+\.chui$') { throw 'Invalid UI resource name in build manifest.' }
            $assetPath=Join-Path $game ('data-pc\ui\'+$asset.Name)
            if (!(Test-Path -LiteralPath $assetPath) -or (Hash $assetPath) -ne $asset.SHA256) {
                throw ('Missing or mismatched UI resource: '+$asset.Name)
            }
        }
        if (Test-Path -LiteralPath $original) {
            if ((Hash $original) -ne $stockSha) { throw 'Original backup has changed. No files changed.' }
        } else {
            if ($current -ne $stockSha) { throw 'Cannot back up an unrecognized original entry.' }
            [IO.File]::WriteAllBytes($original,[IO.File]::ReadAllBytes($steamExe))
            if ((Hash $original) -ne $stockSha) { throw 'Original backup verification failed.' }
        }
        $payload=[IO.File]::ReadAllBytes($modExe)
        $newState=[ordered]@{Version=1;Enabled=$true;AppID=102840;OriginalSHA256=$stockSha;
            ActiveModSHA256=$modSha;Language=$knownBuilds[0].Language;TestAssists=$false}
        $expected=$modSha
    }
    $previous=[IO.File]::ReadAllBytes($steamExe)
    $stateBytes=$null
    if (Test-Path -LiteralPath $statePath) { $stateBytes=[IO.File]::ReadAllBytes($statePath) }
    try {
        if ($current -ne $expected) { Write-Atomic $steamExe $payload }
        if ((Hash $steamExe) -ne $expected) { throw 'Steam entry write verification failed.' }
        $newState['UpdatedUTC']=[DateTime]::UtcNow.ToString('o')
        $text=$newState | ConvertTo-Json -Depth 5
        Write-Atomic $statePath ([Text.Encoding]::UTF8.GetBytes($text))
    } catch {
        Write-Atomic $steamExe $previous
        if ($null -ne $stateBytes) { Write-Atomic $statePath $stateBytes }
        elseif (Test-Path -LiteralPath $statePath) { Remove-Item -LiteralPath $statePath }
        throw
    }
    [PSCustomObject]@{Action=$Action;Enabled=[bool]$newState.Enabled;SteamEntrySHA256=$expected;
        OriginalBackup=$original;SourceMOD=$modExe;TestAssists=$false} | ConvertTo-Json
} finally {
    $lockStream.Dispose()
    Remove-Item -LiteralPath $lock -Force
}
