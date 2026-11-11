param(
    [string]$GamePath = (Split-Path -Parent $PSScriptRoot),
    [switch]$SmokeTest
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()
$game = [IO.Path]::GetFullPath($GamePath)
$bin = Join-Path $game 'bin'
if (!(Test-Path -LiteralPath (Join-Path $bin 'shank2.exe') -PathType Leaf)) {
    throw "Shank 2 directory not found: $game"
}
$keyPath = Join-Path $bin 'Shank2-Coop-Keys.dat'
$dodgePath = Join-Path $bin 'Shank2-Coop-Dodge.dat'
$languagePath = Join-Path $game 'patch\launcher-settings.json'
$magic = [Text.Encoding]::ASCII.GetBytes('S2K1')
$defaults = [int[]]@(0x41,0x44,0x57,0x53,0x20,0x4a,0x4b,0x4c,0x55,0x49,0x0d,0x51,0x4f,
                    0x25,0x27,0x26,0x28,0x60,0x61,0x62,0x63,0x64,0x65,0x67,0x66,0x75,0x76,
                    0x5a,0x43,0x68,0x69)
$script:keys = $defaults.Clone()
$script:inputMode = 0
$script:language = 'en'
if (Test-Path -LiteralPath $languagePath -PathType Leaf) {
    try {
        $old = Get-Content -LiteralPath $languagePath -Raw | ConvertFrom-Json
        if ($old.language -eq 'zh' -or $old.language -eq 'chs') { $script:language = 'zh' }
    } catch {}
}
function Write-Atomic([string]$Path, [byte[]]$Bytes) {
    $temp = $Path + '.' + [Guid]::NewGuid().ToString('N') + '.tmp'
    try {
        [IO.File]::WriteAllBytes($temp,$Bytes)
        if ([IO.File]::Exists($Path)) { [IO.File]::Replace($temp,$Path,[NullString]::Value) }
        else { [IO.File]::Move($temp,$Path) }
    } finally {
        if ([IO.File]::Exists($temp)) { [IO.File]::Delete($temp) }
    }
}
function Read-Keys([byte[]]$Raw) {
    if ($Raw.Length -ne 116 -or [Text.Encoding]::ASCII.GetString($Raw,0,4) -cne 'S2K1') { return }
    $mode = [BitConverter]::ToInt32($Raw,4)
    if ($mode -notin 0,1) { return }
    $values = [int[]]::new(27)
    for ($i=0; $i -lt $values.Length; $i++) {
        $values[$i] = [BitConverter]::ToInt32($Raw,8+4*$i)
        if ($values[$i] -lt 1 -or $values[$i] -gt 254) { return }
    }
    return @{ Keys=$values; Mode=$mode }
}
function Encode-Keys([int]$Mode,[int[]]$Values) {
    $buffer = [byte[]]::new(116)
    $magic.CopyTo($buffer,0)
    [BitConverter]::GetBytes($Mode).CopyTo($buffer,4)
    for ($i=0; $i -lt 27; $i++) {
        [BitConverter]::GetBytes($Values[$i]).CopyTo($buffer,8+4*$i)
    }
    return ,$buffer
}
function Read-Dodge([byte[]]$Raw) {
    if ($Raw.Length -ne 20 -or [Text.Encoding]::ASCII.GetString($Raw,0,4) -cne 'S2D1') { return }
    $values = [int[]]::new(4)
    for ($i=0; $i -lt 4; $i++) {
        $values[$i] = [BitConverter]::ToInt32($Raw,4+4*$i)
        if ($values[$i] -lt 1 -or $values[$i] -gt 254) { return }
    }
    return ,$values
}
function Encode-Dodge([int[]]$Values) {
    $buffer = [byte[]]::new(20)
    [Text.Encoding]::ASCII.GetBytes('S2D1').CopyTo($buffer,0)
    for ($i=0; $i -lt 4; $i++) {
        [BitConverter]::GetBytes($Values[27+$i]).CopyTo($buffer,4+4*$i)
    }
    return ,$buffer
}
function Save-Keys([int]$Mode,[int[]]$Values) {
    $before = if ([IO.File]::Exists($dodgePath)) { [IO.File]::ReadAllBytes($dodgePath) } else { $null }
    Write-Atomic $dodgePath (Encode-Dodge $Values)
    try { Write-Atomic $keyPath (Encode-Keys $Mode $Values) }
    catch {
        if ($null -eq $before) { [IO.File]::Delete($dodgePath) }
        else { Write-Atomic $dodgePath $before }
        throw
    }
}
if (Test-Path -LiteralPath $keyPath -PathType Leaf) {
    $saved = Read-Keys ([IO.File]::ReadAllBytes($keyPath))
    if ($saved) {
        for ($i=0; $i -lt 27; $i++) { $script:keys[$i]=$saved.Keys[$i] }
        $script:inputMode=$saved.Mode
    }
}
if (Test-Path -LiteralPath $dodgePath -PathType Leaf) {
    $savedDodge = Read-Dodge ([IO.File]::ReadAllBytes($dodgePath))
    if ($savedDodge) { for ($i=0; $i -lt 4; $i++) { $script:keys[27+$i]=$savedDodge[$i] } }
}
Add-Type -ReferencedAssemblies 'System.Windows.Forms.dll','System.Drawing.dll' -TypeDefinition @"
using System.Windows.Forms;
public sealed class ShankKeyCapture : Form {
    public int KeyCode { get; private set; }
    protected override bool ProcessCmdKey(ref Message m, Keys keyData) {
        int code = (int)(keyData & Keys.KeyCode);
        if (code > 0 && code < 255) {
            KeyCode = code;
            DialogResult = DialogResult.OK;
            return true;
        }
        return base.ProcessCmdKey(ref m, keyData);
    }
    protected override void OnKeyDown(KeyEventArgs e) {
        int code = (int)e.KeyCode;
        if (code > 0 && code < 255) {
            KeyCode = code;
            e.SuppressKeyPress = true;
            DialogResult = DialogResult.OK;
        } else { base.OnKeyDown(e); }
    }
}
"@
$en = @('Move left','Move right','Move up','Move down','Jump / Confirm (A)',
        'Light attack (X)','Heavy weapon (Y)','Ranged / Interact (B)','Right bumper (RB)',
        'Left bumper (LB)','Pause / Confirm','Left trigger (LT)','Grapple (RT)',
        'Recall 2P','Toggle co-op camera','Dodge left (right stick)','Dodge right (right stick)')
$zh = @('左移','右移','上移','下移','跳跃／确认（A）',
        '轻攻击（X）','重武器（Y）','远程攻击／互动（B）','右肩键（RB）',
        '左肩键（LB）','暂停／确认','左扳机（LT）','抓取（RT）',
        '召回 2P','切换双人镜头','向左闪避（右摇杆）','向右闪避（右摇杆）')
function T([string]$English,[string]$Chinese) {
    if ($script:language -eq 'zh') { return $Chinese }; return $English
}
function Key-Name([int]$Code) {
    $name = [Enum]::GetName([Windows.Forms.Keys],$Code)
    if ($name -match '^D([0-9])$') { return $Matches[1] }
    if ($name -match '^NumPad([0-9])$') { return "Num $($Matches[1])" }
    if ($name) { return $name }; return ('0x{0:X2}' -f $Code)
}
$form = [Windows.Forms.Form]::new()
$form.StartPosition = 'CenterScreen'
$form.AutoScaleMode = 'Dpi'
$form.ClientSize = [Drawing.Size]::new(680,662)
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$form.Font = [Drawing.Font]::new('Segoe UI',9)
function Add-Control([string]$Class,[int]$X,[int]$Y,[int]$W,[int]$H) {
    $ctrl = New-Object ('Windows.Forms.'+$Class)
    $ctrl.SetBounds($X,$Y,$W,$H)
    $form.Controls.Add($ctrl)
    return $ctrl
}
$hint = Add-Control 'Label' 18 13 642 44
$inputLabel = Add-Control 'Label' 18 63 92 23
$modeBox = Add-Control 'ComboBox' 118 59 235 25
$modeBox.DropDownStyle = 'DropDownList'
$langBox = Add-Control 'ComboBox' 528 59 132 25
$langBox.DropDownStyle = 'DropDownList'
[void]$langBox.Items.AddRange(@('English','简体中文'))
$langBox.SelectedIndex = [int]($script:language -eq 'zh')
$heads = @((Add-Control 'Label' 18 94 300 25),(Add-Control 'Label' 349 94 300 25))
$heads[0].Text='1P'
$heads[1].Text='2P'
$labels=@{}
$buttons=@{}
function Edit-Key([int]$Index) {
    $dialog = [ShankKeyCapture]::new()
    try {
        $dialog.Text = T 'Press a key' '按下新键位'
        $dialog.StartPosition='CenterParent'
        $dialog.ClientSize=[Drawing.Size]::new(390,76)
        $dialog.KeyPreview=$true
        $dialog.MinimizeBox=$false
        $dialog.MaximizeBox=$false
        $msg=[Windows.Forms.Label]::new()
        $msg.SetBounds(18,17,355,47)
        $msg.Text = T 'Press the new key, or close this window to cancel.' '按下新键位，或关闭此窗口取消。'
        $dialog.Controls.Add($msg)
        if ($dialog.ShowDialog($form) -ne 'OK') { return }
        $new=$dialog.KeyCode
        for ($j=0; $j -lt $script:keys.Length; $j++) {
            if ($j -ne $Index -and $script:keys[$j] -eq $new) {
                $status.Text = (T 'Key already in use: ' '键位已被占用：') + (Key-Name $new) + ' / ' + $labels[$j].Text
                return
            }
        }
        $script:keys[$Index]=$new
        $buttons[$Index].Text=Key-Name $new
        $status.Text=T 'Unsaved changes' '尚未保存'
    } finally { $dialog.Dispose() }
}
for ($i=0; $i -lt 31; $i++) {
    if ($i -lt 13) { $x=18; $y=120+26*$i }
    elseif ($i -lt 25) {
        $row=$i-13
        if ($row -ge 10) { $row++ }
        $x=349; $y=120+26*$row
    } elseif ($i -lt 27) { $x=18+331*($i-25); $y=545 }
    else { $x=18+331*[int][Math]::Floor(($i-27)/2); $y=458+26*(($i-27)%2) }
    $labels[$i]=Add-Control 'Label' $x ($y+3) 205 22
    $buttons[$i]=Add-Control 'Button' ($x+208) $y 102 24
    $buttons[$i].Tag=$i
    $buttons[$i].Add_Click({param($sender,$eventArgs) Edit-Key ([int]$sender.Tag)})
}
$common = Add-Control 'Label' 18 517 642 23
$status = Add-Control 'Label' 18 581 642 25
$reset = Add-Control 'Button' 18 614 170 31
$save = Add-Control 'Button' 508 614 152 31
function Update-Text {
    $form.Text=T 'Shank 2 Co-op Controls' 'Shank 2 双人键位设置'
    $hint.Text=T 'Run shank2-story-coop.exe directly and choose Campaign Mode → Local Co-op. Save changes here before opening the game.' '直接运行 shank2-story-coop.exe，再选择「战役模式 → 本地双人」。键位保存后在下次打开游戏时生效。'
    $inputLabel.Text=T 'Input mode' '输入方式'
    $common.Text=T 'Shared shortcuts (keyboard or controllers)' '通用快捷键（键盘或手柄模式）'
    $reset.Text=T 'Restore defaults' '恢复默认键位'
    $save.Text=T 'Save settings' '保存设置'
    $picked=$modeBox.SelectedIndex
    if ($picked -lt 0) { $picked=$script:inputMode }
    $modeBox.Items.Clear()
    [void]$modeBox.Items.Add((T 'Shared keyboard' '共用键盘'))
    [void]$modeBox.Items.Add((T 'Two XInput controllers' '两个 XInput 手柄'))
    $modeBox.SelectedIndex=$picked
    $names=if ($script:language -eq 'zh') { $zh } else { $en }
    for ($j=0; $j -lt 31; $j++) {
        $row=if($j -lt 13){$j}elseif($j -lt 23){$j-13}elseif($j -lt 27){$j-12}else{15+(($j-27)%2)}
        $labels[$j].Text=$names[$row]
        $buttons[$j].Text=Key-Name $script:keys[$j]
    }
}
function Update-Enabled {
    for ($j=0; $j -lt 25; $j++) { $buttons[$j].Enabled=($modeBox.SelectedIndex -eq 0) }
    for ($j=27; $j -lt 31; $j++) { $buttons[$j].Enabled=($modeBox.SelectedIndex -eq 0) }
}
$modeBox.Add_SelectedIndexChanged({ Update-Enabled })
$langBox.Add_SelectedIndexChanged({
    $script:language=if ($langBox.SelectedIndex -eq 1) {'zh'} else {'en'}
    $status.Text=''
    Update-Text
    if (!$SmokeTest) {
        try {
            $value=@{format=1;language=$script:language} | ConvertTo-Json -Compress
            Write-Atomic $languagePath ([Text.Encoding]::UTF8.GetBytes($value))
        } catch { $status.Text=$_.Exception.Message }
    }
})
$reset.Add_Click({
    $script:keys=$defaults.Clone()
    Update-Text
    $status.Text=T 'Defaults restored; save to apply.' '已恢复默认键位，请保存。'
})
$save.Add_Click({
    try {
        if (@($script:keys | Sort-Object -Unique).Count -ne 31) {
            $status.Text=T 'Resolve duplicate keys before saving.' '请先调整重复键位。'
            return
        }
        Save-Keys $modeBox.SelectedIndex $script:keys
        $status.Text=T 'Saved. Settings apply the next time the game starts.' '已保存。下次启动游戏时生效。'
    } catch { $status.Text=$_.Exception.Message }
})
Update-Text
Update-Enabled
try {
    if ($SmokeTest) {
        $roundTrip=Read-Keys (Encode-Keys 1 $defaults)
        if ($roundTrip.Mode -ne 1 -or ($roundTrip.Keys -join ',') -cne ($defaults[0..26] -join ',')) { throw 'Key serialization failed.' }
        $dodgeRoundTrip=Read-Dodge (Encode-Dodge $defaults)
        if (($dodgeRoundTrip -join ',') -cne ($defaults[27..30] -join ',')) { throw 'Dodge serialization failed.' }
        $langBox.SelectedIndex=1
        if ($form.Text -notmatch '键位设置' -or $labels[26].Text -ne '切换双人镜头') { throw 'Language update failed.' }
        if ($labels[27].Text -ne '向左闪避（右摇杆）' -or $labels[30].Text -ne '向右闪避（右摇杆）') { throw 'Dodge labels failed.' }
        $modeBox.SelectedIndex=1
        if ($buttons[0].Enabled -or $buttons[27].Enabled -or $buttons[30].Enabled -or !$buttons[26].Enabled) { throw 'Controller mode UI failed.' }
        foreach ($index in @(27,28,29,30)) {
            $measure=[Windows.Forms.TextRenderer]::MeasureText($labels[$index].Text,$form.Font)
            if ($measure.Width -gt $labels[$index].Width -or $buttons[$index].Bottom -gt $common.Top) { throw 'Dodge layout failed.' }
        }
        $fixture=Join-Path ([IO.Path]::GetTempPath()) ('Shank2-key-smoke-'+[Guid]::NewGuid().ToString('N')+'.dat')
        try {
            Write-Atomic $fixture (Encode-Keys 0 $defaults)
            $changed=[int[]]$defaults.Clone()
            $changed[0]=0x5a
            Write-Atomic $fixture (Encode-Keys 1 $changed)
            $saved=Read-Keys ([IO.File]::ReadAllBytes($fixture))
            if ($saved.Mode -ne 1 -or $saved.Keys[0] -ne 0x5a) { throw 'Atomic key update failed.' }
        } finally { if ([IO.File]::Exists($fixture)) { [IO.File]::Delete($fixture) } }
        $oldKeyPath=$keyPath; $oldDodgePath=$dodgePath
        $testFolder=Join-Path ([IO.Path]::GetTempPath()) ('Shank2-dodge-save-'+[Guid]::NewGuid().ToString('N'))
        [void][IO.Directory]::CreateDirectory($testFolder)
        try {
            $keyPath=Join-Path $testFolder 'keys.dat'; $dodgePath=Join-Path $testFolder 'dodge.dat'
            Save-Keys 0 $defaults
            $changed=[int[]]$defaults.Clone(); $changed[0]=0x54; $changed[27]=0x70; $changed[30]=0x73
            Save-Keys 1 $changed
            $saved=Read-Keys ([IO.File]::ReadAllBytes($keyPath))
            $savedDodge=Read-Dodge ([IO.File]::ReadAllBytes($dodgePath))
            if ($saved.Mode -ne 1 -or $saved.Keys[0] -ne 0x54 -or $savedDodge[0] -ne 0x70 -or $savedDodge[3] -ne 0x73) { throw 'Combined save failed.' }
            $beforeDodge=[IO.File]::ReadAllBytes($dodgePath)
            $lock=[IO.File]::Open($keyPath,'Open','ReadWrite','None')
            $rejected=$false
            try { try { Save-Keys 0 $defaults } catch { $rejected=$true } }
            finally { $lock.Dispose() }
            if (!$rejected -or ([Convert]::ToBase64String([IO.File]::ReadAllBytes($dodgePath)) -cne [Convert]::ToBase64String($beforeDodge))) { throw 'Combined save rollback failed.' }
            if ((Read-Keys ([IO.File]::ReadAllBytes($keyPath))).Keys[0] -ne 0x54) { throw 'Legacy key changed after failed save.' }
        } finally {
            $keyPath=$oldKeyPath; $dodgePath=$oldDodgePath
            if ([IO.File]::Exists((Join-Path $testFolder 'keys.dat'))) { [IO.File]::Delete((Join-Path $testFolder 'keys.dat')) }
            if ([IO.File]::Exists((Join-Path $testFolder 'dodge.dat'))) { [IO.File]::Delete((Join-Path $testFolder 'dodge.dat')) }
            [IO.Directory]::Delete($testFolder)
        }
        Write-Output 'Settings UI, legacy 27-key preservation and four dodge keys round trip passed.'
    } else { [void]$form.ShowDialog() }
} finally { $form.Dispose() }

