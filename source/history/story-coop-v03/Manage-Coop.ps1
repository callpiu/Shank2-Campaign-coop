param(
    [ValidateSet('Install','Launch','Verify','Remove')][string]$Action = 'Launch',
    [ValidateSet('Keyboard','Pads')][string]$InputMode = 'Keyboard',
    [string]$GamePath = 'E:\SteamLibrary\steamapps\common\Shank 2',
    [string]$LoadoutPath
)
$ErrorActionPreference = 'Stop'
$modeName = $InputMode.ToLowerInvariant()
$recipe = Get-Content -LiteralPath (Join-Path $PSScriptRoot ($modeName + '-recipe.json')) -Raw | ConvertFrom-Json
$uiRecipe = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'ui-recipe.json') -Raw | ConvertFrom-Json
$catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'catalog.json') -Raw | ConvertFrom-Json
$gameRoot = (Resolve-Path -LiteralPath $GamePath).Path
$binPath = Join-Path $gameRoot 'bin'
$sourcePath = Join-Path $binPath 'shank2.exe'
$targetPath = Join-Path $binPath ('shank2-coop-v03-' + $modeName + '.exe')
$uiSourcePath = Join-Path $gameRoot 'data-pc\ui\campaignscreen.chui'
$uiTargetPath = Join-Path $gameRoot 'data-pc\ui\campaigncoop.chui'
$receiptPath = $targetPath + '.coop-install.json'
function Hash-Bytes([byte[]]$Bytes) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hasher.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant() }
    finally { $hasher.Dispose() }
}
function From-Hex([string]$Hex) {
    $bytes = New-Object byte[] ($Hex.Length / 2)
    for ($i=0; $i -lt $bytes.Length; $i++) { $bytes[$i] = [Convert]::ToByte($Hex.Substring($i*2,2),16) }
    return ,$bytes
}
function Reconstruct([string]$SourcePath, $Recipe) {
    $source = [IO.File]::ReadAllBytes($SourcePath)
    if ($source.Length -ne $Recipe.source_size -or (Hash-Bytes $source) -ne $Recipe.input_sha256) { throw ('Unsupported original file: ' + $SourcePath) }
    $stream = New-Object IO.MemoryStream
    try {
        $stream.Write($source,0,$source.Length)
        foreach ($patch in $Recipe.patches) {
            $before = From-Hex $patch.before; $after = From-Hex $patch.after
            for ($i=0; $i -lt $before.Length; $i++) {
                if ($source[[int]$patch.offset+$i] -ne $before[$i]) { throw 'Patch precondition failed.' }
            }
            $stream.Position = [int]$patch.offset; $stream.Write($after,0,$after.Length)
        }
        $stream.Position = $source.Length
        foreach ($chunk in $Recipe.append) {
            if ($null -ne $chunk.copy) { $stream.Write($source,[int]$chunk.copy,[int]$chunk.length) }
            elseif ($null -ne $chunk.fill) {
                $fill = New-Object byte[] ([int]$chunk.length)
                if ($chunk.fill -ne 0) { for ($i=0; $i -lt $fill.Length; $i++) { $fill[$i] = [byte]$chunk.fill } }
                $stream.Write($fill,0,$fill.Length)
            } else { $literal = [Convert]::FromBase64String($chunk.literal); $stream.Write($literal,0,$literal.Length) }
        }
        $result = $stream.ToArray()
    } finally { $stream.Dispose() }
    if ($result.Length -ne $Recipe.target_size -or (Hash-Bytes $result) -ne $Recipe.output_sha256) { throw 'Reconstruction verification failed.' }
    return ,$result
}
function Assert-ManagedTarget {
    if (Test-Path -LiteralPath $targetPath) {
        $actual = Hash-Bytes ([IO.File]::ReadAllBytes($targetPath))
        $known = $recipe.output_sha256
        if (@($recipe.allowed_previous_sha256) -contains $actual) { return }
        if (Test-Path -LiteralPath $receiptPath) {
            $receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
            if ($receipt.format -eq 1 -and $receipt.baseline_sha256 -eq $recipe.output_sha256) { $known = $receipt.installed_sha256 }
        }
        if ($actual -ne $known) { throw 'Unrecognized co-op executable; refusing to overwrite or remove it.' }
    }
}
function Assert-UiTarget {
    if ((Test-Path -LiteralPath $uiTargetPath) -and (Hash-Bytes ([IO.File]::ReadAllBytes($uiTargetPath))) -ne $uiRecipe.output_sha256) {
        throw 'Unrecognized campaigncoop.chui; refusing to overwrite or remove it.'
    }
}
function Assert-NotRunning {
    $running = Get-Process -Name 'shank2-coop-v03-keyboard','shank2-coop-v03-pads' -ErrorAction SilentlyContinue | Where-Object { $_.Path -and [IO.Path]::GetDirectoryName($_.Path) -eq $binPath }
    if ($running) { throw 'Close the v0.3 co-op game before changing its files.' }
}
function New-Config($Settings) {
    $result = New-Object byte[] 128
    for ($i=0; $i -lt 2; $i++) {
        $entry = $Settings.players[$i]
        $skin = @($catalog.skins | Where-Object { $_.id -ceq [string]$entry.skin })
        if ($skin.Count -ne 1) { throw ('Unknown skin for player ' + ($i+1)) }
        $weapons = $catalog.weapons.($skin[0].family)
        $chosen = @()
        foreach ($slot in @('melee','ranged','consumable')) {
            $valid = @($weapons.$slot | Where-Object { $_.id -ceq [string]$entry.$slot })
            if ($valid.Count -ne 1) { throw ('Invalid ' + $slot + ' for player ' + ($i+1)) }
            $chosen += [uint32]$valid[0].hash
        }
        $o = $i * 64
        [BitConverter]::GetBytes([uint32]1).CopyTo($result,$o)
        [Text.Encoding]::ASCII.GetBytes([string]$skin[0].family).CopyTo($result,$o+4)
        [BitConverter]::GetBytes([uint32]$skin[0].hash).CopyTo($result,$o+20)
        for ($j=0; $j -lt 3; $j++) { [BitConverter]::GetBytes([uint32]$chosen[$j]).CopyTo($result,$o+24+4*$j) }
        [BitConverter]::GetBytes([uint32]3).CopyTo($result,$o+36)
    }
    return ,$result
}
if ($Action -eq 'Remove') {
    Assert-NotRunning; Assert-ManagedTarget; Assert-UiTarget
    if (Test-Path -LiteralPath $targetPath) { Remove-Item -LiteralPath $targetPath }
    if (Test-Path -LiteralPath $receiptPath) { Remove-Item -LiteralPath $receiptPath }
    $other = Join-Path $binPath ('shank2-coop-v03-' + $(if ($modeName -eq 'keyboard') {'pads'} else {'keyboard'}) + '.exe')
    if (!(Test-Path -LiteralPath $other) -and (Test-Path -LiteralPath $uiTargetPath)) { Remove-Item -LiteralPath $uiTargetPath }
    Write-Output 'Removed v0.3 files for this input mode. Original game and v0.2 preserved.'
    return
}
$result = Reconstruct $sourcePath $recipe
$uiResult = Reconstruct $uiSourcePath $uiRecipe
$settings = @{players=@(@{skin='shank';melee='machete';ranged='throwingknives';consumable='weapon_grenade'},@{skin='corina';melee='sword';ranged='revolver';consumable='weapon_grenade'})}
if ($LoadoutPath) { $settings = Get-Content -LiteralPath $LoadoutPath -Raw | ConvertFrom-Json }
if (@($settings.players).Count -ne 2) { throw 'Exactly two loadouts are required.' }
$config = New-Config $settings
if ([int]$recipe.config_size -ne 128 -or [int]$recipe.config_offset -lt 0 -or [int]$recipe.config_offset+128 -gt $result.Length) { throw 'Invalid configuration layout.' }
$config.CopyTo($result,[int]$recipe.config_offset)
$installedHash = Hash-Bytes $result
if ($Action -eq 'Verify') {
    Write-Output ('Verified executable and UI reconstruction; configured SHA256 ' + $installedHash)
    return
}
Assert-NotRunning; Assert-ManagedTarget; Assert-UiTarget
# Both reconstructions and collision guards finish before any destination changes.
[IO.File]::WriteAllBytes($uiTargetPath,$uiResult)
[IO.File]::WriteAllBytes($targetPath,$result)
@{format=1;baseline_sha256=$recipe.output_sha256;installed_sha256=$installedHash;players=$settings.players} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
Write-Output ('Installed: ' + $targetPath)
if ($Action -eq 'Launch') {
    $previousAppId = [Environment]::GetEnvironmentVariable('SteamAppId','Process')
    $previousGameId = [Environment]::GetEnvironmentVariable('SteamGameId','Process')
    try {
        [Environment]::SetEnvironmentVariable('SteamAppId','102840','Process')
        [Environment]::SetEnvironmentVariable('SteamGameId','102840','Process')
        $process = Start-Process -FilePath $targetPath -WorkingDirectory $binPath -ArgumentList '-windowed' -WindowStyle Hidden -PassThru
    } finally {
        [Environment]::SetEnvironmentVariable('SteamAppId',$previousAppId,'Process')
        [Environment]::SetEnvironmentVariable('SteamGameId',$previousGameId,'Process')
    }
    Write-Output ('Started PID ' + $process.Id + '. Choose CAMPAIGN MODE. F6 recalls player 2.')
}
