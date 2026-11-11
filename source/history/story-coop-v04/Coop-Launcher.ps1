param([string]$GamePath, [switch]$SmokeTest, [string]$PreviewPath)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()
. (Join-Path $PSScriptRoot 'Portraits.ps1')
. (Join-Path $PSScriptRoot 'Launcher-Strings.ps1')
. (Join-Path $PSScriptRoot 'Launcher-Preferences.ps1')
. (Join-Path $PSScriptRoot 'Game-Paths.ps1')
if(!$GamePath) {$GamePath=Find-ShankGameFolder $PSScriptRoot}
$script:catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'catalog.json') -Raw | ConvertFrom-Json
$script:settingsPath = Join-Path $PSScriptRoot 'loadouts.json'
$script:preferencesPath=Join-Path $PSScriptRoot 'launcher-settings.json'
$script:startupLanguage=Get-SavedUiLanguage $script:preferencesPath
$script:uiLanguage=$script:startupLanguage
if($SmokeTest) {$script:preferencesPath=Join-Path $PSScriptRoot ('.smoke-language-'+[Guid]::NewGuid().ToString('N')+'.json')}
$script:panels = @()
$script:textBindings=New-Object Collections.ArrayList
$script:updatingLanguage=$false
function Bind-UiText($Control,[string]$Key) {
    $Control.Text=Get-UiText $Key
    $null=$script:textBindings.Add([pscustomobject]@{control=$Control;key=$Key})
}
$form = New-Object Windows.Forms.Form
Bind-UiText $form 'windowTitle'
$form.ClientSize = New-Object Drawing.Size(940,652)
$form.StartPosition = 'CenterScreen'
$form.FormBorderStyle = 'FixedDialog'; $form.MaximizeBox = $false
$form.Font = New-Object Drawing.Font('Microsoft YaHei UI',10)
$form.BackColor = [Drawing.Color]::FromArgb(245,245,247)
function Label-At($Parent,[string]$Key,[int]$X,[int]$Y,[int]$Width=650) {
    $label = New-Object Windows.Forms.Label
    Bind-UiText $label $Key; $label.Location=New-Object Drawing.Point($X,$Y)
    $label.Size=New-Object Drawing.Size($Width,28); $Parent.Controls.Add($label)
    return $label
}
$null=Label-At $form 'heading' 24 20 560
$null=Label-At $form 'description' 24 52 890
$null=Label-At $form 'language' 624 20 100
$languageBox=New-Object Windows.Forms.ComboBox
$languageBox.DropDownStyle='DropDownList';$languageBox.Location=New-Object Drawing.Point(734,18)
$languageBox.Size=New-Object Drawing.Size(180,28)
$null=$languageBox.Items.Add('English');$null=$languageBox.Items.Add('简体中文');$languageBox.SelectedIndex=$(if($script:uiLanguage -eq 'zh'){1}else{0})
$form.Controls.Add($languageBox)
$null=Label-At $form 'gameFolder' 24 92 100
$pathBox=New-Object Windows.Forms.TextBox
$pathBox.Location=New-Object Drawing.Point(122,90); $pathBox.Size=New-Object Drawing.Size(686,28); $pathBox.Text=$GamePath
$form.Controls.Add($pathBox)
$browse=New-Object Windows.Forms.Button
Bind-UiText $browse 'browse';$browse.Location=New-Object Drawing.Point(822,88);$browse.Size=New-Object Drawing.Size(92,32)
$form.Controls.Add($browse)
$browse.Add_Click({
    $dialog=New-Object Windows.Forms.FolderBrowserDialog
    $dialog.Description=Get-UiText 'chooseFolder'
    $dialog.SelectedPath=$pathBox.Text
    if ($dialog.ShowDialog($form) -eq 'OK') {$pathBox.Text=$dialog.SelectedPath}
    $dialog.Dispose()
})
for ($i=0;$i -lt 2;$i++) {
    $group=New-Object Windows.Forms.GroupBox
    Bind-UiText $group ('player'+($i+1));$group.Location=New-Object Drawing.Point((24+458*$i),140)
    $group.Size=New-Object Drawing.Size(434,306);$form.Controls.Add($group)
    $controls=@{}
    $picture=New-Object Windows.Forms.PictureBox
    $picture.Location=New-Object Drawing.Point(16,32);$picture.Size=New-Object Drawing.Size(100,100)
    $picture.SizeMode='Zoom';$picture.BackColor=[Drawing.Color]::FromArgb(232,232,236)
    $group.Controls.Add($picture);$controls.portrait=$picture
    $labels=@('skin','melee','ranged','consumable')
    $slots=@('skin','melee','ranged','consumable')
    for ($j=0;$j -lt 4;$j++) {
        if($j -eq 0) {$null=Label-At $group $labels[$j] 130 36 280} else {$null=Label-At $group $labels[$j] 16 (154+48*($j-1)) 120}
        $combo=New-Object Windows.Forms.ComboBox
        $combo.DropDownStyle='DropDownList'
        if($j -eq 0) {$combo.Location=New-Object Drawing.Point(130,72);$combo.Size=New-Object Drawing.Size(286,28)} else {$combo.Location=New-Object Drawing.Point(142,(150+48*($j-1)));$combo.Size=New-Object Drawing.Size(274,28)}
        $combo.DisplayMember='name';$combo.Tag=$i
        $group.Controls.Add($combo);$controls[$slots[$j]]=$combo
    }
    $script:panels+=$controls
    foreach($skin in $script:catalog.skins) {$null=$controls.skin.Items.Add((Get-SkinItem $skin))}
}
function Refresh-Portrait([int]$Index) {
    $p=$script:panels[$Index];$skin=$p.skin.SelectedItem
    if($null -eq $skin) {return}
    try {$p.portrait.Image=Get-CoopPortrait $pathBox.Text $skin.id} catch {$p.portrait.Image=$null}
    $p.portrait.AccessibleName=((Get-UiText 'portrait') -f ($Index+1),$skin.name)
}
function Refresh-Weapons([int]$Index) {
    $p=$script:panels[$Index];$skin=$p.skin.SelectedItem
    if ($null -eq $skin) {return}
    Refresh-Portrait $Index
    foreach($slot in @('melee','ranged','consumable')) {
        $old=$p[$slot].SelectedItem.id
        $p[$slot].Items.Clear()
        foreach($weapon in $script:catalog.weapons.($skin.family).$slot) {
            $name=Get-WeaponName $weapon
            $null=$p[$slot].Items.Add([pscustomobject]@{id=$weapon.id;name=$name})
        }
        $p[$slot].SelectedIndex=0
        for($n=0;$n -lt $p[$slot].Items.Count;$n++) {
            if ($p[$slot].Items[$n].id -eq $old) {$p[$slot].SelectedIndex=$n;break}
        }
    }
}
foreach($p in $script:panels) {$p.skin.Add_SelectedIndexChanged({if(!$script:updatingLanguage) {Refresh-Weapons ([int]$this.Tag)}})}
$script:panels[0].skin.SelectedIndex=0
$script:panels[1].skin.SelectedIndex=12
$pathBox.Add_TextChanged({foreach($index in 0,1) {Refresh-Portrait $index}})
$null=Label-At $form 'inputMode' 24 470 100
$modeBox=New-Object Windows.Forms.ComboBox
$modeBox.DropDownStyle='DropDownList';$modeBox.Location=New-Object Drawing.Point(122,466)
$modeBox.Size=New-Object Drawing.Size(256,28)
$null=$modeBox.Items.Add((Get-UiText 'keyboard'));$null=$modeBox.Items.Add((Get-UiText 'pads'));$modeBox.SelectedIndex=0
$form.Controls.Add($modeBox)
$null=Label-At $form 'rescueHint' 24 510 890
$hint=Label-At $form 'keyboardHint' 24 538 890
$status=New-Object Windows.Forms.Label
$status.Location=New-Object Drawing.Point(24,612);$status.Size=New-Object Drawing.Size(890,28);$form.Controls.Add($status)
function Set-Status([string]$Key) {$script:statusKey=$Key;$status.Text=Get-UiText $Key}
Set-Status 'ready'
function Get-Settings {
    $players=@()
    foreach($p in $script:panels) {
        $players+=@{skin=$p.skin.SelectedItem.id;melee=$p.melee.SelectedItem.id;ranged=$p.ranged.SelectedItem.id;consumable=$p.consumable.SelectedItem.id}
    }
    return @{format=1;gamePath=$pathBox.Text;inputMode=$(if($modeBox.SelectedIndex -eq 0){'Keyboard'}else{'Pads'});players=$players}
}
function Save-Settings {
    $settings=Get-Settings
    $settings | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $script:settingsPath -Encoding UTF8
    return $settings
}
if (Test-Path -LiteralPath $script:settingsPath) {
    try {
        $saved=Get-Content -LiteralPath $script:settingsPath -Raw | ConvertFrom-Json
        if(Test-ShankGameFolder ([string]$saved.gamePath)) {$pathBox.Text=$saved.gamePath}
        if($saved.inputMode -eq 'Pads') {$modeBox.SelectedIndex=1}
        for($i=0;$i -lt 2;$i++) {
            $p=$script:panels[$i];$entry=$saved.players[$i]
            foreach($slot in @('skin','melee','ranged','consumable')) {
                for($n=0;$n -lt $p[$slot].Items.Count;$n++) {
                    if($p[$slot].Items[$n].id -eq $entry.$slot) {$p[$slot].SelectedIndex=$n;break}
                }
            }
        }
    } catch {Set-Status 'settingsUnreadable'}
}
$save=New-Object Windows.Forms.Button
Bind-UiText $save 'save';$save.Location=New-Object Drawing.Point(574,574);$save.Size=New-Object Drawing.Size(132,32)
$form.Controls.Add($save)
$save.Add_Click({try{$null=Save-Settings;Set-Status 'saved'}catch{[Windows.Forms.MessageBox]::Show($form,((Get-UiText 'saveError')+"`r`n`r`n"+$_.Exception.Message),(Get-UiText 'saveErrorTitle'))|Out-Null}})
$launch=New-Object Windows.Forms.Button
Bind-UiText $launch 'launch';$launch.Location=New-Object Drawing.Point(722,574);$launch.Size=New-Object Drawing.Size(192,32)
$form.Controls.Add($launch)
$launch.Add_Click({
    $launch.Enabled=$false;$save.Enabled=$false
    try {
        if(!(Test-ShankGameFolder $pathBox.Text)) {throw (Get-UiText 'gameFolderRequired')}
        $settings=Save-Settings
        Set-Status 'installing';$form.Refresh()
        $messages=& (Join-Path $PSScriptRoot 'Manage-Coop.ps1') -Action Launch -InputMode $settings.inputMode -GamePath $settings.gamePath -LoadoutPath $script:settingsPath
        Set-Status 'launched'
        $form.WindowState='Minimized'
    } catch {[Windows.Forms.MessageBox]::Show($form,((Get-UiText 'launchError')+"`r`n`r`n"+$_.Exception.Message),(Get-UiText 'launchErrorTitle'))|Out-Null;Set-Status 'launchFailed'}
    finally {$launch.Enabled=$true;$save.Enabled=$true}
})
function Set-UiLanguage([string]$Code) {
    if($Code -notin @('en','zh')) {throw 'Unsupported UI language'}
    $script:updatingLanguage=$true
    try {
        $script:uiLanguage=$Code
        foreach($binding in $script:textBindings) {$binding.control.Text=Get-UiText $binding.key}
        $modeIndex=$modeBox.SelectedIndex
        $modeBox.Items.Clear();$null=$modeBox.Items.Add((Get-UiText 'keyboard'));$null=$modeBox.Items.Add((Get-UiText 'pads'));$modeBox.SelectedIndex=$modeIndex
        for($index=0;$index -lt 2;$index++) {
            $p=$script:panels[$index];$selected=$p.skin.SelectedItem.id
            $p.skin.BeginUpdate()
            try {
                $p.skin.Items.Clear()
                foreach($skin in $script:catalog.skins) {$null=$p.skin.Items.Add((Get-SkinItem $skin))}
                for($n=0;$n -lt $p.skin.Items.Count;$n++) {if($p.skin.Items[$n].id -eq $selected) {$p.skin.SelectedIndex=$n;break}}
            } finally {$p.skin.EndUpdate()}
            Refresh-Weapons $index
        }
        Set-Status $script:statusKey
    } finally {$script:updatingLanguage=$false}
}
$languageBox.Add_SelectedIndexChanged({
    $code=if($this.SelectedIndex -eq 1){'zh'}else{'en'}
    Set-UiLanguage $code
    try {Save-UiLanguage $script:preferencesPath $code;if($script:statusKey -eq 'languageSaveFailed') {Set-Status 'ready'}} catch {Set-Status 'languageSaveFailed'}
})
try {
if ($SmokeTest) {
    $expectedIndex=if($script:startupLanguage -eq 'zh'){1}else{0}
    if($script:uiLanguage -ne $script:startupLanguage -or $languageBox.SelectedIndex -ne $expectedIndex -or $form.Text -cne (Get-UiText 'windowTitle')) {throw 'Startup language was not restored correctly.'}
    foreach($languageIndex in 0,1,0) {
        $testPlayers=@(
            @{skin='yakuza';melee='saw';ranged='shotgun';consumable='weapon_mine'},
            @{skin='sunshine';melee='scythe';ranged='uzi';consumable='weapon_molotov'}
        )
        for($i=0;$i -lt 2;$i++) {
            foreach($slot in @('skin','melee','ranged','consumable')) {
                $combo=$script:panels[$i][$slot]
                for($n=0;$n -lt $combo.Items.Count;$n++) {if($combo.Items[$n].id -eq $testPlayers[$i][$slot]) {$combo.SelectedIndex=$n;break}}
                if($combo.SelectedItem.id -ne $testPlayers[$i][$slot]) {throw 'Could not prepare a non-default loadout.'}
            }
        }
        $modeBox.SelectedIndex=1
        Set-Status 'saved'
        $firstPortrait=$script:panels[0].portrait.Image;$secondPortrait=$script:panels[1].portrait.Image
        $before=Get-Settings | ConvertTo-Json -Depth 8 -Compress
        $languageBox.SelectedIndex=$languageIndex
        $expectedLanguage=if($languageIndex -eq 1){'zh'}else{'en'}
        if((Get-SavedUiLanguage $script:preferencesPath) -cne $expectedLanguage) {throw 'Selected language was not persisted.'}
        $after=Get-Settings | ConvertTo-Json -Depth 8 -Compress
        if($before -ne $after) {throw 'Language change altered a player loadout or input mode.'}
        if($status.Text -cne (Get-UiText 'saved') -or $modeBox.GetItemText($modeBox.SelectedItem) -cne (Get-UiText 'pads')) {throw 'Dynamic status or input options did not translate.'}
        if(![object]::ReferenceEquals($firstPortrait,$script:panels[0].portrait.Image) -or ![object]::ReferenceEquals($secondPortrait,$script:panels[1].portrait.Image)) {throw 'Language change altered a character portrait.'}
        foreach($key in $script:uiStrings.en.Keys) {if(!$script:uiStrings.zh.ContainsKey($key)) {throw ('Missing Chinese string: '+$key)}}
        foreach($binding in $script:textBindings) {
            if($binding.control.Text -cne (Get-UiText $binding.key)) {throw ('Untranslated control: '+$binding.key)}
            if($binding.control -is [Windows.Forms.Label] -or $binding.control -is [Windows.Forms.Button]) {
                $measure=[Windows.Forms.TextRenderer]::MeasureText($binding.control.Text,$binding.control.Font)
                if($measure.Width -gt $binding.control.ClientSize.Width -or $measure.Height -gt $binding.control.ClientSize.Height) {throw ('Translated text does not fit: '+$binding.key)}
            }
        }
    foreach($panelIndex in 0,1) {
        foreach($skinIndex in 0..($script:catalog.skins.Count-1)) {
            $script:panels[$panelIndex].skin.SelectedIndex=$skinIndex
            $skin=$script:catalog.skins[$skinIndex]
            foreach($slot in @('melee','ranged','consumable')) {
                if ($script:panels[$panelIndex][$slot].Items.Count -ne $script:catalog.weapons.($skin.family).$slot.Count) {throw 'Weapon filter mismatch.'}
            }
            if($null -eq $script:panels[$panelIndex].portrait.Image) {throw ('Missing portrait: '+$skin.id)}
        }
    }
    $script:panels[0].skin.SelectedIndex=0
    $script:panels[1].skin.SelectedIndex=12
    $check=Get-Settings
    if ($check.players[0].skin -ne 'shank' -or $check.players[1].skin -ne 'corina') {throw 'Player selections are not independent.'}
    foreach($panel in $script:panels) {
        foreach($slot in @('skin','melee','ranged','consumable')) {
            $combo=$panel[$slot]
            $expected=[string]$combo.SelectedItem.name
            $actual=$combo.GetItemText($combo.SelectedItem)
            if([string]::IsNullOrWhiteSpace($actual) -or $actual -ne $expected) {throw ('Display text mismatch: '+$slot+' expected='+$expected+' actual='+$actual)}
        }
    }
    }
    if($PreviewPath) {
        $form.CreateControl();$form.PerformLayout()
        $preview=New-Object Drawing.Bitmap($form.Width,$form.Height)
        try {
            $form.DrawToBitmap($preview,(New-Object Drawing.Rectangle(0,0,$form.Width,$form.Height)))
            $previewGraphics=[Drawing.Graphics]::FromImage($preview)
            try {
                function Draw-PreviewControl($Control,[int]$X,[int]$Y) {
                    $null=$Control.Handle
                    $part=New-Object Drawing.Bitmap($Control.Width,$Control.Height)
                    try {$Control.DrawToBitmap($part,(New-Object Drawing.Rectangle(0,0,$Control.Width,$Control.Height)));$previewGraphics.DrawImageUnscaled($part,$X,$Y)} finally {$part.Dispose()}
                    foreach($child in $Control.Controls) {Draw-PreviewControl $child ($X+$child.Left) ($Y+$child.Top)}
                }
                $border=[int](($form.Width-$form.ClientSize.Width)/2)
                $title=$form.Height-$form.ClientSize.Height-$border
                foreach($control in $form.Controls) {Draw-PreviewControl $control ($border+$control.Left) ($title+$control.Top)}
            } finally {$previewGraphics.Dispose()}
            $preview.Save($PreviewPath,[Drawing.Imaging.ImageFormat]::Png)
        } finally {$preview.Dispose()}
    }
    Write-Output ('PASS: startup='+$script:startupLanguage+', language persistence, EN/ZH switching, preserved loadouts/input, 17 portraits per player.')
} else { $null=$form.ShowDialog() }
} finally {
    $form.Dispose()
    Close-CoopPortraits
    if($SmokeTest -and [IO.File]::Exists($script:preferencesPath)) {[IO.File]::Delete($script:preferencesPath)}
}
