"""Keep the reviewed v0.5 sources intact; compose an isolated v0.8 launcher."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;DEV=HERE/'launcher';BASE=HERE.parent/'story-coop-v05'
def replace(s,a,b):
 assert s.count(a)==1,(a[:90],s.count(a))
 return s.replace(a,b,1)
s=(BASE/'Coop-Launcher.ps1').read_text(encoding='utf-8-sig')
s=replace(s,"if ($SmokeTest) {\n", """if ($SmokeTest) {
    if(@($form.Controls | Where-Object {$_ -is [Windows.Forms.CheckBox]}).Count) {throw 'Feature switches must not appear in the launcher.'}
    if((Get-Settings).ContainsKey('features')) {throw 'Launcher must not save feature switches.'}
""")
(DEV/'Coop-Launcher.ps1').write_text(s,encoding='utf-8-sig')
s=(BASE/'Launcher-Strings.ps1').read_text(encoding='utf-8-sig').replace('v0.5','v0.8')
s=s.replace("F6 recalls Player 2.'", "F6 recalls P2. F7 toggles the camera.'")
s=s.replace("F6 手动召回 2P。'", "F6 手动召回 2P；F7 切换镜头。'")
(DEV/'Launcher-Strings.ps1').write_text(s,encoding='utf-8-sig')
s=(BASE/'Manage-Coop.ps1').read_text(encoding='utf-8-sig')
s=s.replace("'shank2-coop-v05-'", "'shank2-coop-v08-'")
start=s.index('    $running=Get-Process');end=s.index('\nfunction Assert-Ui',start)
s=s[:start]+"""    $running=Get-CimInstance Win32_Process -Filter "Name like 'shank2%'" | Where-Object {$_.ExecutablePath -and [IO.Path]::GetDirectoryName($_.ExecutablePath) -eq $bin}
    if($running) {throw 'Close the game in this folder before changing its mod files.'}
}
function Assert-Executable {
    if(!(Test-Path -LiteralPath $target)) {return}
    $allowed=@()
    foreach($lang in @('en','chs')) {
        $r=Get-Content -LiteralPath (Join-Path $PSScriptRoot ($mode+'-'+$lang+'-addon.json')) -Raw | ConvertFrom-Json
        $allowed+=@($r.output_sha256)
    }
    if(Test-Path -LiteralPath $receipt) {
        $r=Get-Content -LiteralPath $receipt -Raw | ConvertFrom-Json
        if($r.format -eq 1 -and $r.baseline_sha256 -in $allowed) {$allowed+=@($r.installed_sha256)}
    }
    if((Hash-Bytes ([IO.File]::ReadAllBytes($target))) -notin $allowed) {throw 'Unrecognized development executable; refusing to overwrite or remove.'}
}
"""+s[end:]
s=replace(s,"if(!(Test-Path -LiteralPath $other)) {", "if(!(Test-Path -LiteralPath $other) -and !(Test-Path -LiteralPath (Join-Path $bin 'shank2-coop-v05-keyboard.exe')) -and !(Test-Path -LiteralPath (Join-Path $bin 'shank2-coop-v05-pads.exe'))) {")
needle="$config=New-Config $settings"
s=replace(s,needle,"""function Hash-File([string]$Path) {
    $stream=[IO.File]::OpenRead($Path);$hash=[Security.Cryptography.SHA256]::Create()
    try {return ([BitConverter]::ToString($hash.ComputeHash($stream))).Replace('-','').ToLowerInvariant()}
    finally {$stream.Dispose();$hash.Dispose()}
}
$addon=Get-Content -LiteralPath (Join-Path $PSScriptRoot ($mode+'-'+$language+'-addon.json')) -Raw | ConvertFrom-Json
if($result.Length -ne $addon.source_size -or (Hash-Bytes $result) -ne $addon.input_sha256) {throw 'Development overlay baseline mismatch.'}
foreach($patch in $addon.patches) {
    $before=From-Hex $patch.before;$after=From-Hex $patch.after
    for($i=0;$i -lt $before.Length;$i++) {if($result[[int]$patch.offset+$i] -ne $before[$i]) {throw 'Overlay precondition failed.'}}
    $after.CopyTo($result,[int]$patch.offset)
}
$result=[byte[]]($result+[Convert]::FromBase64String($addon.append))
if($result.Length -ne $addon.target_size -or (Hash-Bytes $result) -ne $addon.output_sha256) {throw 'Overlay reconstruction mismatch.'}
$baseline=$addon.output_sha256
# Both enhancements always start enabled; ignore obsolete optional settings.
# F7 remains an in-session camera toggle in the unchanged native camera code.
$features=@{sharedCamera=$true;dialogueMix=$true}
foreach($pair in @(@('sharedCamera','camera_offset'),@('dialogueMix','audio_offset'))) {
    $offset=[int]$addon.($pair[1])
    if($offset -lt 0 -or $offset+4 -gt $result.Length) {throw 'Invalid feature offset.'}
    [BitConverter]::GetBytes([int]$features[$pair[0]]).CopyTo($result,$offset)
}
if($features.dialogueMix) {
    $assets=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'movie-assets.json') -Raw | ConvertFrom-Json
    foreach($asset in $assets) {
        $original=Join-Path $root ('data\\movies\\'+$asset.file)
        $enhanced=Join-Path $root ('data\\movies\\coop_dialogue_enhanced\\'+$asset.file)
        if(!(Test-Path -LiteralPath $original) -or !(Test-Path -LiteralPath $enhanced)) {throw 'Enhanced cutscene resources are missing. Stage the complete enhanced movie set before launching.'}
        if((Hash-File $original) -ne $asset.input_sha256 -or (Hash-File $enhanced) -ne $asset.output_sha256) {throw ('Unsupported or changed cutscene: '+$asset.file+'. Restore the matching movie resources before launching.')}
    }
}
$config=New-Config $settings""")
s=replace(s,'players=$settings.players} | ConvertTo-Json', 'players=$settings.players;features=$features} | ConvertTo-Json')
s=s.replace('v0.5','v0.8')
# Preserve the real shared UI names and previous-version presence guards.
s=s.replace('coopv08.chui','coopv05.chui').replace("'shank2-coop-v08-keyboard.exe')) -and", "'shank2-coop-v05-keyboard.exe')) -and").replace("'shank2-coop-v08-pads.exe'))) {", "'shank2-coop-v05-pads.exe'))) {")
(DEV/'Manage-Coop.ps1').write_text(s,encoding='utf-8-sig')
manifest=json.loads((HERE.parent/'story-coop-v07-dialogue/enhanced-manifest.json').read_text())
(DEV/'movie-assets.json').write_text(json.dumps([{k:r[k] for k in ['file','input_sha256','output_sha256']} for r in manifest['files']],indent=2))
(DEV/'Start-Coop.ps1').write_text("& (Join-Path $PSScriptRoot 'Coop-Launcher.ps1')\n",encoding='utf-8-sig')
print('Development launcher composed; both enhancements always enabled, F7 retained, no feature switches.')
