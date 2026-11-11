param(
    [ValidateSet('Install','Launch','Verify','Remove')][string]$Action='Launch',
    [ValidateSet('Keyboard','Pads')][string]$InputMode='Keyboard',
    [string]$GamePath,[string]$LoadoutPath
)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'Game-Paths.ps1')
if(!$GamePath -and $LoadoutPath) {$GamePath=Get-SavedGameFolder $LoadoutPath}
if(!$GamePath) {$GamePath=Find-ShankGameFolder $PSScriptRoot}
if(!(Test-ShankGameFolder $GamePath)) {throw 'Select the Shank 2 folder containing bin and data-pc.'}
$root=(Resolve-Path -LiteralPath $GamePath).Path
$bin=Join-Path $root 'bin';$mode=$InputMode.ToLowerInvariant()
$target=Join-Path $bin ('shank2-coop-v05-'+$mode+'.exe')
$receipt=$target+'.coop-install.json'
$recipe=Get-Content (Join-Path $PSScriptRoot ($mode+'-recipe.json')) -Raw | ConvertFrom-Json
$chsRecipe=Get-Content (Join-Path $PSScriptRoot ($mode+'-chs-recipe.json')) -Raw | ConvertFrom-Json
$catalog=Get-Content (Join-Path $PSScriptRoot 'catalog.json') -Raw | ConvertFrom-Json
$uiFiles=@(
    @{source='campaignscreen.chui';target='campaigncoopv05.chui';en='ui-recipe.json';chs='ui-chs-recipe.json'},
    @{source='pausedialog.chui';target='pausecoopv05.chui';en='pause-en-recipe.json';chs='pause-chs-recipe.json'},
    @{source='singleplayerloadoutscreen.chui';target='equipcoopv05.chui';en='equip-en-recipe.json';chs='equip-chs-recipe.json'}
)
function Hash-Bytes([byte[]]$Bytes) {
    $h=[Security.Cryptography.SHA256]::Create()
    try {return ([BitConverter]::ToString($h.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant()} finally {$h.Dispose()}
}
function From-Hex([string]$Hex) {
    $b=New-Object byte[] ($Hex.Length/2)
    for($i=0;$i -lt $b.Length;$i++) {$b[$i]=[Convert]::ToByte($Hex.Substring($i*2,2),16)}
    return ,$b
}
function Reconstruct([byte[]]$Source,$Recipe) {
    if($Source.Length -ne $Recipe.source_size -or (Hash-Bytes $Source) -ne $Recipe.input_sha256) {throw 'Unsupported original file.'}
    $s=New-Object IO.MemoryStream
    try {
        if($Recipe.format -eq 2) {$chunks=$Recipe.chunks}
        else {
            $s.Write($Source,0,$Source.Length)
            foreach($p in $Recipe.patches) {
                $before=From-Hex $p.before;$after=From-Hex $p.after
                for($i=0;$i -lt $before.Length;$i++) {if($Source[[int]$p.offset+$i] -ne $before[$i]) {throw 'Patch precondition failed.'}}
                $s.Position=[int]$p.offset;$s.Write($after,0,$after.Length)
            }
            $s.Position=$Source.Length;$chunks=$Recipe.append
        }
        foreach($c in $chunks) {
            if($null -ne $c.copy) {$s.Write($Source,[int]$c.copy,[int]$c.length)}
            elseif($null -ne $c.fill) {
                $fill=New-Object byte[] ([int]$c.length)
                if($c.fill -ne 0) {for($i=0;$i -lt $fill.Length;$i++) {$fill[$i]=[byte]$c.fill}}
                $s.Write($fill,0,$fill.Length)
            } else {$literal=[Convert]::FromBase64String($c.literal);$s.Write($literal,0,$literal.Length)}
        }
        $result=$s.ToArray()
    } finally {$s.Dispose()}
    if($result.Length -ne $Recipe.target_size -or (Hash-Bytes $result) -ne $Recipe.output_sha256) {throw 'Reconstruction verification failed.'}
    return ,$result
}
function Assert-NotRunning {
    $running=Get-Process -Name 'shank2-coop-v05-keyboard','shank2-coop-v05-pads' -ErrorAction SilentlyContinue | Where-Object {$_.Path -and [IO.Path]::GetDirectoryName($_.Path) -eq $bin}
    if($running) {throw 'Close the v0.5 co-op game before changing its files.'}
}
function Assert-Executable {
    if(!(Test-Path -LiteralPath $target)) {return}
    $allowed=@($recipe.output_sha256,$chsRecipe.output_sha256)
    # Exact baselines of the previously distributed v0.5 test build. Permit
    # configured copies only when their receipt and full installed hash agree.
    $previous=@{
        keyboard=@('f718f5e24a5457bda031ffaf4dcb10ce54efd8c8de21c72adb0e38f7fb9fcff4','ca067b30b56a532dd745d711c20162ea59a3890565cfc64440daef4b618156fc')
        pads=@('e5d3ba3302c378d767087005b0396878edd0f88c59328a016d5db2386247d1e4','067286af998be85398400542ef386e8ed8de6663bba02a9e57a2de570c6c352e')
    }
    $allowed+=@($previous[$mode])
    if(Test-Path -LiteralPath $receipt) {
        $r=Get-Content -LiteralPath $receipt -Raw | ConvertFrom-Json
        if($r.format -eq 1 -and $r.baseline_sha256 -in $allowed) {$allowed+=@($r.installed_sha256)}
    }
    if((Hash-Bytes ([IO.File]::ReadAllBytes($target))) -notin $allowed) {throw 'Unrecognized co-op executable; refusing to overwrite or remove.'}
}
function Assert-Ui($Entry) {
    $path=Join-Path $root ('data-pc\ui\'+$Entry.target)
    $allowed=@()
    foreach($language in @('en','chs')) {
        $r=Get-Content (Join-Path $PSScriptRoot $Entry.$language) -Raw | ConvertFrom-Json
        $allowed+=@($r.output_sha256)
    }
    if((Test-Path -LiteralPath $path) -and (Hash-Bytes ([IO.File]::ReadAllBytes($path))) -notin $allowed) {throw ('Unrecognized custom UI: '+$Entry.target)}
}
function New-Config($Settings) {
    $result=New-Object byte[] 128
    if(@($Settings.players).Count -ne 2) {throw 'Exactly two loadouts are required.'}
    for($i=0;$i -lt 2;$i++) {
        $entry=$Settings.players[$i]
        $skin=@($catalog.skins | Where-Object {$_.id -ceq [string]$entry.skin})
        if($skin.Count -ne 1) {throw 'Unknown character.'}
        $weapons=$catalog.weapons.($skin[0].family);$chosen=@()
        foreach($slot in @('melee','ranged','consumable')) {
            $valid=@($weapons.$slot | Where-Object {$_.id -ceq [string]$entry.$slot})
            if($valid.Count -ne 1) {throw ('Invalid '+$slot+' for player '+($i+1))}
            $chosen+=[uint32]$valid[0].hash
        }
        $o=$i*64
        [BitConverter]::GetBytes([uint32]1).CopyTo($result,$o)
        [Text.Encoding]::ASCII.GetBytes([string]$skin[0].family).CopyTo($result,$o+4)
        [BitConverter]::GetBytes([uint32]$skin[0].hash).CopyTo($result,$o+20)
        for($j=0;$j -lt 3;$j++) {[BitConverter]::GetBytes([uint32]$chosen[$j]).CopyTo($result,$o+24+4*$j)}
        [BitConverter]::GetBytes([uint32]3).CopyTo($result,$o+36)
    }
    return ,$result
}
function Commit-Files($Files) {
    $done=New-Object Collections.ArrayList
    try {
        foreach($f in $Files) {
            $old=$null;if(Test-Path -LiteralPath $f.path) {$old=[IO.File]::ReadAllBytes($f.path)}
            $temp=$f.path+'.'+[guid]::NewGuid().ToString('N')+'.tmp'
            try {
                [IO.File]::WriteAllBytes($temp,$f.bytes)
                if($null -ne $old) {[IO.File]::Replace($temp,$f.path,[NullString]::Value)} else {[IO.File]::Move($temp,$f.path)}
                $null=$done.Add(@{path=$f.path;bytes=$old})
            } finally {if(Test-Path -LiteralPath $temp) {Remove-Item -LiteralPath $temp}}
        }
    } catch {
        for($i=$done.Count-1;$i -ge 0;$i--) {
            $f=$done[$i]
            if($null -eq $f.bytes) {Remove-Item -LiteralPath $f.path} else {[IO.File]::WriteAllBytes($f.path,$f.bytes)}
        }
        throw
    }
}
if($Action -eq 'Remove') {
    Assert-NotRunning;Assert-Executable
    foreach($e in $uiFiles) {Assert-Ui $e}
    foreach($p in @($target,$receipt)) {if(Test-Path -LiteralPath $p) {Remove-Item -LiteralPath $p}}
    $other=Join-Path $bin ('shank2-coop-v05-'+$(if($mode -eq 'keyboard') {'pads'} else {'keyboard'})+'.exe')
    if(!(Test-Path -LiteralPath $other)) {
        foreach($e in $uiFiles) {$p=Join-Path $root ('data-pc\ui\'+$e.target);if(Test-Path -LiteralPath $p) {Remove-Item -LiteralPath $p}}
    }
    Write-Output 'Removed this v0.5 input mode. Original game and earlier mods preserved.';return
}
$pending=@();$language=$null
foreach($e in $uiFiles) {
    $source=[IO.File]::ReadAllBytes((Join-Path $root ('data-pc\ui\'+$e.source)));$hash=Hash-Bytes $source
    $selected=$null
    foreach($l in @('en','chs')) {
        $r=Get-Content (Join-Path $PSScriptRoot $e.$l) -Raw | ConvertFrom-Json
        if($hash -eq $r.input_sha256) {$selected=$r;$selectedLanguage=$l;break}
    }
    if($null -eq $selected) {throw ('Unsupported UI source: '+$e.source)}
    if($language -and $language -ne $selectedLanguage) {throw 'Mixed English/Chinese UI files; restore a consistent localization.'}
    $language=$selectedLanguage
    $pending+=@(@{path=(Join-Path $root ('data-pc\ui\'+$e.target));bytes=(Reconstruct $source $selected)})
}
$result=Reconstruct ([IO.File]::ReadAllBytes((Join-Path $bin 'shank2.exe'))) $recipe
$baseline=$recipe.output_sha256
if($language -eq 'chs') {
    & (Join-Path $PSScriptRoot 'Coop-Localization.ps1') -Action Verify -Group Text -GamePath $root -NoUI | Out-Null
    $result=Reconstruct $result $chsRecipe;$baseline=$chsRecipe.output_sha256
}
$settings=@{players=@(@{skin='shank';melee='machete';ranged='throwingknives';consumable='weapon_grenade'},@{skin='corina';melee='sword';ranged='revolver';consumable='weapon_grenade'})}
if($LoadoutPath) {$settings=Get-Content -LiteralPath $LoadoutPath -Raw | ConvertFrom-Json}
$config=New-Config $settings
if($recipe.config_size -ne 128 -or $recipe.config_offset -lt 0 -or $recipe.config_offset+128 -gt $result.Length) {throw 'Invalid configuration layout.'}
$config.CopyTo($result,[int]$recipe.config_offset);$installed=Hash-Bytes $result
if($Action -eq 'Verify') {Write-Output ('Verified v0.5 '+$mode+' '+$language+' executable and all three UI reconstructions.');return}
Assert-NotRunning;Assert-Executable
foreach($e in $uiFiles) {Assert-Ui $e}
$pending+=@(@{path=$target;bytes=$result})
$receiptBytes=[Text.Encoding]::UTF8.GetBytes((@{format=1;baseline_sha256=$baseline;installed_sha256=$installed;players=$settings.players} | ConvertTo-Json -Depth 8))
$pending+=@(@{path=$receipt;bytes=$receiptBytes})
Commit-Files $pending
Write-Output ('Installed: '+$target)
if($Action -eq 'Launch') {
    $oldApp=$env:SteamAppId;$oldGame=$env:SteamGameId
    try {
        $env:SteamAppId='102840';$env:SteamGameId='102840'
        $p=Start-Process -FilePath $target -WorkingDirectory $bin -WindowStyle Hidden -PassThru
    } finally {$env:SteamAppId=$oldApp;$env:SteamGameId=$oldGame}
    Write-Output ('Started PID '+$p.Id+'. Select CAMPAIGN MODE.')
}
