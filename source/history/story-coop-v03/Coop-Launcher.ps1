param([string]$GamePath = 'E:\SteamLibrary\steamapps\common\Shank 2', [switch]$SmokeTest)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()
$script:catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'catalog.json') -Raw | ConvertFrom-Json
$script:settingsPath = Join-Path $PSScriptRoot 'loadouts.json'
$script:weaponNames = @{
    machete='砍刀';saw='电锯';sledgehammer='大锤';throwingknives='飞刀';pistols='双枪';shotgun='霰弹枪';
    sword='长剑';scythe='镰刀';revolver='左轮手枪';uzi='乌兹冲锋枪';
    weapon_grenade='手雷';weapon_mine='地雷';weapon_molotov='燃烧瓶'
}
$script:panels = @()
$form = New-Object Windows.Forms.Form
$form.Text = 'Shank 2 故事双人 · v0.3 原型'
$form.ClientSize = New-Object Drawing.Size(780,580)
$form.StartPosition = 'CenterScreen'
$form.FormBorderStyle = 'FixedDialog'; $form.MaximizeBox = $false
$form.Font = New-Object Drawing.Font('Microsoft YaHei UI',10)
$form.BackColor = [Drawing.Color]::FromArgb(245,245,247)
function Label-At($Parent,[string]$Text,[int]$X,[int]$Y,[int]$Width=650) {
    $label = New-Object Windows.Forms.Label
    $label.Text=$Text; $label.Location=New-Object Drawing.Point($X,$Y)
    $label.Size=New-Object Drawing.Size($Width,28); $Parent.Controls.Add($label)
    return $label
}
$null=Label-At $form '故事模式本地双人' 24 20
$null=Label-At $form '分别选择角色和三格装备；进入关卡后采用这里保存的配装。' 24 52
$null=Label-At $form '游戏目录' 24 92 100
$pathBox=New-Object Windows.Forms.TextBox
$pathBox.Location=New-Object Drawing.Point(122,90); $pathBox.Size=New-Object Drawing.Size(526,28); $pathBox.Text=$GamePath
$form.Controls.Add($pathBox)
$browse=New-Object Windows.Forms.Button
$browse.Text='浏览…';$browse.Location=New-Object Drawing.Point(662,88);$browse.Size=New-Object Drawing.Size(92,32)
$form.Controls.Add($browse)
$browse.Add_Click({
    $dialog=New-Object Windows.Forms.FolderBrowserDialog
    $dialog.Description='选择包含 bin 和 data-pc 的 Shank 2 游戏目录'
    $dialog.SelectedPath=$pathBox.Text
    if ($dialog.ShowDialog($form) -eq 'OK') {$pathBox.Text=$dialog.SelectedPath}
    $dialog.Dispose()
})
for ($i=0;$i -lt 2;$i++) {
    $group=New-Object Windows.Forms.GroupBox
    $group.Text=([string]($i+1)+'P');$group.Location=New-Object Drawing.Point((24+376*$i),140)
    $group.Size=New-Object Drawing.Size(354,244);$form.Controls.Add($group)
    $controls=@{}
    $labels=@('角色 / 服装','近战装备','远程装备','投掷装备')
    $slots=@('skin','melee','ranged','consumable')
    for ($j=0;$j -lt 4;$j++) {
        $null=Label-At $group $labels[$j] 16 (36+48*$j) 105
        $combo=New-Object Windows.Forms.ComboBox
        $combo.DropDownStyle='DropDownList';$combo.Location=New-Object Drawing.Point(122,(32+48*$j))
        $combo.Size=New-Object Drawing.Size(214,28);$combo.DisplayMember='name';$combo.Tag=$i
        $group.Controls.Add($combo);$controls[$slots[$j]]=$combo
    }
    $script:panels+=$controls
    foreach($skin in $script:catalog.skins) {$null=$controls.skin.Items.Add($skin)}
}
function Refresh-Weapons([int]$Index) {
    $p=$script:panels[$Index];$skin=$p.skin.SelectedItem
    if ($null -eq $skin) {return}
    foreach($slot in @('melee','ranged','consumable')) {
        $old=$p[$slot].SelectedItem.id
        $p[$slot].Items.Clear()
        foreach($weapon in $script:catalog.weapons.($skin.family).$slot) {
            $name=$script:weaponNames[$weapon.id]
            if (!$name) {$name=$weapon.name}
            $null=$p[$slot].Items.Add([pscustomobject]@{id=$weapon.id;name=$name})
        }
        $p[$slot].SelectedIndex=0
        for($n=0;$n -lt $p[$slot].Items.Count;$n++) {
            if ($p[$slot].Items[$n].id -eq $old) {$p[$slot].SelectedIndex=$n;break}
        }
    }
}
foreach($p in $script:panels) {$p.skin.Add_SelectedIndexChanged({Refresh-Weapons ([int]$this.Tag)})}
$script:panels[0].skin.SelectedIndex=0
$script:panels[1].skin.SelectedIndex=12
$null=Label-At $form '输入方式' 24 406 100
$modeBox=New-Object Windows.Forms.ComboBox
$modeBox.DropDownStyle='DropDownList';$modeBox.Location=New-Object Drawing.Point(122,402)
$modeBox.Size=New-Object Drawing.Size(256,28)
$null=$modeBox.Items.Add('共用键盘');$null=$modeBox.Items.Add('两个 XInput 手柄');$modeBox.SelectedIndex=0
$form.Controls.Add($modeBox)
$null=Label-At $form 'F6 手动召回 2P；不会按距离自动回传。' 24 446
$hint=Label-At $form '键盘：1P WASD / 空格；2P 方向键 / 小键盘 0（NumLock 开启）' 24 474 740
$status=Label-At $form '设置仅供此 MOD 使用，原版程序与 v0.2 保留。' 24 540 740
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
        if($saved.gamePath) {$pathBox.Text=$saved.gamePath}
        if($saved.inputMode -eq 'Pads') {$modeBox.SelectedIndex=1}
        for($i=0;$i -lt 2;$i++) {
            $p=$script:panels[$i];$entry=$saved.players[$i]
            foreach($slot in @('skin','melee','ranged','consumable')) {
                for($n=0;$n -lt $p[$slot].Items.Count;$n++) {
                    if($p[$slot].Items[$n].id -eq $entry.$slot) {$p[$slot].SelectedIndex=$n;break}
                }
            }
        }
    } catch {$status.Text='上次配置无法读取，已使用默认双人配装。'}
}
$save=New-Object Windows.Forms.Button
$save.Text='保存配置';$save.Location=New-Object Drawing.Point(414,506);$save.Size=New-Object Drawing.Size(132,32)
$form.Controls.Add($save)
$save.Add_Click({try{$null=Save-Settings;$status.Text='双人配装已保存，下次启动时生效。'}catch{[Windows.Forms.MessageBox]::Show($form,$_.Exception.Message,'无法保存')|Out-Null}})
$launch=New-Object Windows.Forms.Button
$launch.Text='保存并启动';$launch.Location=New-Object Drawing.Point(562,506);$launch.Size=New-Object Drawing.Size(192,32)
$form.Controls.Add($launch)
$launch.Add_Click({
    $launch.Enabled=$false;$save.Enabled=$false
    try {
        $settings=Save-Settings
        $status.Text='正在校验并安装 MOD…';$form.Refresh()
        $messages=& (Join-Path $PSScriptRoot 'Manage-Coop.ps1') -Action Launch -InputMode $settings.inputMode -GamePath $settings.gamePath -LoadoutPath $script:settingsPath
        $status.Text='游戏已启动。选择 CAMPAIGN MODE 进入故事模式。'
        $form.WindowState='Minimized'
    } catch {[Windows.Forms.MessageBox]::Show($form,$_.Exception.Message,'启动失败')|Out-Null;$status.Text='未能启动，请检查游戏目录并关闭已运行的 v0.3。'}
    finally {$launch.Enabled=$true;$save.Enabled=$true}
})
if ($SmokeTest) {
    foreach($panelIndex in 0,1) {
        foreach($skinIndex in 0..($script:catalog.skins.Count-1)) {
            $script:panels[$panelIndex].skin.SelectedIndex=$skinIndex
            $skin=$script:catalog.skins[$skinIndex]
            foreach($slot in @('melee','ranged','consumable')) {
                if ($script:panels[$panelIndex][$slot].Items.Count -ne $script:catalog.weapons.($skin.family).$slot.Count) {throw 'Weapon filter mismatch.'}
            }
        }
    }
    $script:panels[0].skin.SelectedIndex=0
    $script:panels[1].skin.SelectedIndex=12
    $check=Get-Settings
    if ($check.players[0].skin -ne 'shank' -or $check.players[1].skin -ne 'corina') {throw 'Player selections are not independent.'}
    Write-Output 'PASS: 17 skins per player, weapon filtering, independent selections.'
} else { $null=$form.ShowDialog() }
$form.Dispose()
