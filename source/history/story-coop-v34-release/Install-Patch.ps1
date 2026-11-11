param([ValidateSet('Install','Verify','Remove')][string]$Action='Install',[string]$GamePath,[switch]$NoUI)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'Game-Paths.ps1')
if (!$GamePath) { $GamePath=Find-ShankGameFolder $PSScriptRoot }
if (!(Test-ShankGameFolder $GamePath)) {
    if ($NoUI) { throw 'Select the Shank 2 folder containing bin and data-pc.' }
    Add-Type -AssemblyName System.Windows.Forms
    $picker=[Windows.Forms.FolderBrowserDialog]::new()
    $picker.Description='Select Shank 2 / 选择 Shank 2 游戏目录'
    try { if ($picker.ShowDialog() -ne 'OK') { return }; $GamePath=$picker.SelectedPath } finally { $picker.Dispose() }
}
if (!(Test-ShankGameFolder $GamePath)) { throw 'Invalid Shank 2 directory.' }
$root=[IO.Path]::GetFullPath((Resolve-Path -LiteralPath $GamePath).Path).TrimEnd('\')
if ((Get-Item -LiteralPath $root -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse game root refused.' }
$manifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($manifest.format -ne 1 -or !@($manifest.files).Count) { throw 'Invalid or empty manifest.' }
function Target([string]$Relative) {
    if (!$Relative -or [IO.Path]::IsPathRooted($Relative) -or $Relative.Contains(':') -or $Relative -match '(^|[\\/])\.\.([\\/]|$)') { throw 'Unsafe relative path.' }
    $p=[IO.Path]::GetFullPath((Join-Path $root $Relative))
    if (!$p.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Target escapes game.' }
    for ($current=$p; $current.Length -gt $root.Length; $current=[IO.Path]::GetDirectoryName($current)) {
        if ((Test-Path -LiteralPath $current) -and ((Get-Item -LiteralPath $current -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw ('Reparse target refused: '+$current) }
    }
    return $p
}
function Hash-Bytes([byte[]]$Bytes) {
    $h=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($h.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant() } finally { $h.Dispose() }
}
function Hash-File([string]$Path) {
    if (![IO.File]::Exists($Path)) { return $null }
    $h=[Security.Cryptography.SHA256]::Create(); $s=[IO.File]::OpenRead($Path)
    try { return ([BitConverter]::ToString($h.ComputeHash($s))).Replace('-','').ToLowerInvariant() } finally { $s.Dispose();$h.Dispose() }
}
function Atomic([string]$Source,[string]$Dest) {
    [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Dest))
    $temp=$Dest+'.'+[Guid]::NewGuid().ToString('N')+'.tmp'
    try {
        [IO.File]::Copy($Source,$temp,$false)
        if ([IO.File]::Exists($Dest)) { [IO.File]::Replace($temp,$Dest,[NullString]::Value) }
        else { [IO.File]::Move($temp,$Dest) }
    } finally { if ([IO.File]::Exists($temp)) { [IO.File]::Delete($temp) } }
}
function Write-Json([string]$Path,$Value) {
    $temp=$Path+'.'+[Guid]::NewGuid().ToString('N')+'.tmp'
    try {
        [IO.File]::WriteAllText($temp,($Value | ConvertTo-Json -Depth 16),[Text.UTF8Encoding]::new($false))
        Atomic $temp $Path
    } finally { if ([IO.File]::Exists($temp)) { [IO.File]::Delete($temp) } }
}
function Hex([string]$Value) {
    $b=[byte[]]::new($Value.Length/2)
    for($i=0;$i -lt $b.Length;$i++) { $b[$i]=[Convert]::ToByte($Value.Substring(2*$i,2),16) }
    return ,$b
}
function Rebuild([byte[]]$Source,$Recipe) {
    if ($Source.Length -ne $Recipe.source_size -or (Hash-Bytes $Source) -ne $Recipe.input_sha256) { throw 'Unsupported original executable.' }
    $s=[IO.MemoryStream]::new()
    try {
        $s.Write($Source,0,$Source.Length)
        foreach($p in $Recipe.patches) {
            $before=Hex $p.before; $after=Hex $p.after
            if ($before.Length -ne $after.Length) { throw 'Invalid fixed-size patch.' }
            for($i=0;$i -lt $before.Length;$i++) { if ($Source[[int]$p.offset+$i] -ne $before[$i]) { throw 'Executable patch precondition failed.' } }
            $s.Position=[int]$p.offset; $s.Write($after,0,$after.Length)
        }
        $s.Position=$Source.Length
        $append=[Convert]::FromBase64String($Recipe.append); $s.Write($append,0,$append.Length)
        $result=$s.ToArray()
    } finally { $s.Dispose() }
    if ($result.Length -ne $Recipe.target_size -or (Hash-Bytes $result) -ne $Recipe.output_sha256) { throw 'Executable reconstruction mismatch.' }
    return ,$result
}
$meta=Target '.shank2-patch'; $statePath=Target '.shank2-patch/state.json'; $journalPath=Target '.shank2-patch/transaction.json'
$lockPath=Target '.shank2-patch.lock'; $lock=$null; $stage=$null
$rows=@{}; foreach($file in $manifest.files) {
    $null=Target $file.path
    if ($rows.ContainsKey($file.path) -or $file.sha256 -notmatch '^[0-9a-f]{64}$') { throw 'Duplicate or invalid manifest entry.' }
    if ($file.path -notmatch '^(bin/shank2(?:-story-coop)?\.exe|data(?:-pc)?/.+|patch/Coop-Key-Settings\.ps1|Coop-Key-Settings\.cmd)$') { throw 'Target outside package scope.' }
    $rows[$file.path]=$file
}
function Clean-Stage([string]$Relative) {
    if ($Relative -notmatch '^\.shank2-patch/stage-[0-9a-f]{32}$') { throw 'Unsafe staging path.' }
    $path=Target $Relative
    if ([IO.Directory]::Exists($path)) { [IO.Directory]::Delete($path,$true) }
}
function Recover {
    if (!(Test-Path -LiteralPath $journalPath)) { return }
    $j=Get-Content -LiteralPath $journalPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($j.format -ne 1 -or $j.profile -ne $manifest.profile -or $j.action -notin @('Install','Remove')) { throw 'Unknown pending transaction; use its original package.' }
    $null=Target $j.stage
    if ($j.stage -notmatch '^\.shank2-patch/stage-[0-9a-f]{32}$') { throw 'Invalid pending stage.' }
    $current=Hash-File $statePath
    $committed=($current -eq $j.afterHash)
    if (!$committed -and $current -ne $j.beforeHash) { throw 'Pending receipt changed.' }
    foreach($op in $j.operations) {
        if (!$rows.ContainsKey($op.path)) { throw 'Unknown pending target.' }
        $target=Target $op.path
        $hash=Hash-File $target
        if ($hash -ne $op.beforeHash -and $hash -ne $op.afterHash) { throw ('Modified pending target: '+$op.path) }
        if (!$committed -and $op.beforeHash) {
            $copy=Target ($j.stage+'/rollback/'+$op.path)
            if ((Hash-File $copy) -ne $op.beforeHash) { throw 'Recovery data damaged.' }
        }
    }
    foreach($op in $j.operations) {
        if (!$committed -and (Hash-File (Target $op.path)) -ne $op.beforeHash) {
            if ($op.beforeHash) { Atomic (Target ($j.stage+'/rollback/'+$op.path)) (Target $op.path) }
            elseif ([IO.File]::Exists((Target $op.path))) { [IO.File]::Delete((Target $op.path)) }
        }
        if ((!$committed -and $op.newBackup) -or ($committed -and $j.action -eq 'Remove')) {
            $backup=Target ('.shank2-patch/backups/'+$op.path)
            if ([IO.File]::Exists($backup)) { [IO.File]::Delete($backup) }
        }
    }
    Clean-Stage $j.stage
    [IO.File]::Delete($journalPath)
    Write-Output 'Recovered/finished pending transaction.'
}
try {
    $running=@(Get-CimInstance Win32_Process -Filter "Name LIKE 'shank2%'" | Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase) })
    if ($running.Count -and ($Action -ne 'Verify' -or (Test-Path -LiteralPath $journalPath))) { throw 'Close the game in this installation before changing files.' }
    $lock=[IO.File]::Open($lockPath,'CreateNew','Write','None')
    foreach($g in $manifest.guards.PSObject.Properties) { if ((Hash-File (Target $g.Name)) -ne $g.Value) { throw ('Unsupported Steam component: '+$g.Name) } }
    Recover
    $state=$null
    if (Test-Path -LiteralPath $statePath) {
        $state=Get-Content -LiteralPath $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($state.format -ne 1 -or $state.profile -ne $manifest.profile) { throw 'Another package is installed. Uninstall it with its own package before switching profiles.' }
        foreach($entry in $state.files) { if (!$rows.ContainsKey($entry.path)) { throw 'Unknown installed file; use the previous package to uninstall.' } }
    }
    if ($Action -eq 'Remove' -and !$state) { Write-Output 'No installation to remove.'; return }
    if ($Action -eq 'Verify' -and !$state) { throw 'This package is not installed.' }
    $allCurrent=$true
    foreach($file in $manifest.files) {
        $entry=@($state.files | Where-Object path -CEQ $file.path)
        $target=Target $file.path; $current=Hash-File $target
        if ($entry.Count -gt 1) { throw 'Duplicate receipt.' }
        if ($entry.Count -eq 1) {
            $restoredOriginal=if ($entry[0].original_present) { $current -eq $entry[0].original_sha256 } else { $null -eq $current }
            if ($current -ne $entry[0].sha256 -and !($Action -ne 'Verify' -and $restoredOriginal)) { throw ('Modified installed file: '+$file.path) }
            if ($entry[0].original_present -and (Hash-File (Target ('.shank2-patch/backups/'+$file.path))) -ne $entry[0].original_sha256) { throw 'Original backup damaged.' }
        } else {
            if ($file.original_sha256) {
                if ($current -ne $file.original_sha256) { throw ('Restore the Steam original or uninstall the old patch first: '+$file.path) }
            } elseif ($current -and $current -ne $file.sha256) { throw ('Foreign custom file: '+$file.path) }
        }
        if ($current -ne $file.sha256) { $allCurrent=$false }
        if ($Action -eq 'Verify' -and $current -ne $file.sha256) { throw ('Version mismatch: '+$file.path) }
    }
    if ($Action -eq 'Verify') { Write-Output ('Verified '+$manifest.profile+' / '+$manifest.version); return }
    if ($Action -eq 'Install' -and $state -and $allCurrent) {
        if ($state.version -ne $manifest.version) { $state.version=$manifest.version; Write-Json $statePath $state }
        Write-Output 'Already installed and verified.'; return
    }
    [void][IO.Directory]::CreateDirectory($meta)
    $stageRel='.shank2-patch/stage-'+[Guid]::NewGuid().ToString('N'); $stage=Target $stageRel
    [void][IO.Directory]::CreateDirectory($stage)
    $stock=if ($state) { Target '.shank2-patch/backups/bin/shank2.exe' } else { Target 'bin/shank2.exe' }
    if ((Hash-File $stock) -ne $manifest.original_exe_sha256) { throw 'Verified original Steam executable required.' }
    $exeBytes=$null; $operations=@(); $nextFiles=@()
    foreach($file in $manifest.files) {
        $target=Target $file.path; $beforeHash=Hash-File $target
        $entry=@($state.files | Where-Object path -CEQ $file.path)
        $after=Target ($stageRel+'/after/'+$file.path)
        $newBackup=($Action -eq 'Install' -and $entry.Count -eq 0 -and [bool]$beforeHash)
        if ($beforeHash) {
            $rollback=Target ($stageRel+'/rollback/'+$file.path)
            [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($rollback)); [IO.File]::Copy($target,$rollback,$false)
        }
        $afterHash=$null
        if ($Action -eq 'Install') {
            [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($after))
            if ($file.recipe) {
                if ($null -eq $exeBytes) {
                    $recipe=Get-Content -LiteralPath (Join-Path $PSScriptRoot $file.recipe) -Raw -Encoding UTF8 | ConvertFrom-Json
                    $exeBytes=Rebuild ([IO.File]::ReadAllBytes($stock)) $recipe
                }
                [IO.File]::WriteAllBytes($after,$exeBytes)
            } else { [IO.File]::Copy((Join-Path $PSScriptRoot $file.relative),$after,$false) }
            if ((Hash-File $after) -ne $file.sha256 -or (Get-Item -LiteralPath $after).Length -ne $file.size) { throw ('Damaged payload: '+$file.path) }
            $afterHash=$file.sha256
            if ($entry.Count) { $originalHash=$entry[0].original_sha256; $present=$entry[0].original_present }
            else { $originalHash=$beforeHash; $present=[bool]$beforeHash }
            $nextFiles+=@{path=$file.path;sha256=$afterHash;original_sha256=$originalHash;original_present=$present}
            if ($newBackup -and (Test-Path -LiteralPath (Target ('.shank2-patch/backups/'+$file.path)))) { throw 'Unreceipted backup exists; keep it for recovery.' }
        } else {
            if ($entry[0].original_present) {
                [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($after))
                [IO.File]::Copy((Target ('.shank2-patch/backups/'+$file.path)),$after,$false)
                $afterHash=$entry[0].original_sha256
            }
        }
        $operations+=@{path=$file.path;beforeHash=$beforeHash;afterHash=$afterHash;newBackup=$newBackup}
    }
    $afterState=Target ($stageRel+'/next-state.json')
    $afterStateHash=$null
    if ($Action -eq 'Install') { Write-Json $afterState @{format=1;profile=$manifest.profile;version=$manifest.version;files=$nextFiles}; $afterStateHash=Hash-File $afterState }
    Write-Json $journalPath @{format=1;profile=$manifest.profile;action=$Action;stage=$stageRel;beforeHash=(Hash-File $statePath);afterHash=$afterStateHash;operations=$operations}
    try {
        foreach($op in $operations) {
            if ($op.newBackup) { Atomic (Target ($stageRel+'/rollback/'+$op.path)) (Target ('.shank2-patch/backups/'+$op.path)) }
            if ($op.afterHash) { Atomic (Target ($stageRel+'/after/'+$op.path)) (Target $op.path) }
            elseif ([IO.File]::Exists((Target $op.path))) { [IO.File]::Delete((Target $op.path)) }
        }
        if ($afterStateHash) { Atomic $afterState $statePath } else { [IO.File]::Delete($statePath) }
    } catch { $cause=$_; Recover; throw $cause }
    Recover; $stage=$null
    Write-Output ($Action+' completed. Steam launch uses bin/shank2.exe. Saves, display settings and personal key bindings preserved.')
} finally {
    if ($stage -and !(Test-Path -LiteralPath $journalPath)) { Clean-Stage $stageRel }
    if ($lock) { $lock.Dispose(); [IO.File]::Delete($lockPath) }
}
