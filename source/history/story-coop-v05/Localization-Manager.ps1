param([string]$GamePath,[switch]$NoShow)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
. (Join-Path $PSScriptRoot 'Game-Paths.ps1')
if(!$GamePath) {$GamePath=Find-ShankGameFolder $PSScriptRoot}
$script:chsManagerBusy=$false
$form=New-Object Windows.Forms.Form
$form.Text='Shank 2 故事双人 v0.5 · 汉化管理'
$form.ClientSize=New-Object Drawing.Size(740,335)
$form.StartPosition='CenterScreen';$form.FormBorderStyle='FixedDialog';$form.MaximizeBox=$false
$form.Font=New-Object Drawing.Font('Microsoft YaHei UI',10)
$title=New-Object Windows.Forms.Label
$title.Text='Shank 2 · 文字汉化与过场字幕';$title.AutoSize=$true;$title.Location=New-Object Drawing.Point(20,18)
$form.Controls.Add($title)
$path=New-Object Windows.Forms.TextBox
$path.Name='GamePath';$path.Text=$GamePath;$path.Location=New-Object Drawing.Point(20,57);$path.Size=New-Object Drawing.Size(590,28)
$form.Controls.Add($path)
$browse=New-Object Windows.Forms.Button
$browse.Name='Browse';$browse.Text='选择目录…';$browse.Location=New-Object Drawing.Point(620,55);$browse.Size=New-Object Drawing.Size(100,32)
$form.Controls.Add($browse)
$status=New-Object Windows.Forms.Label
$status.Name='Status';$status.Location=New-Object Drawing.Point(20,103);$status.Size=New-Object Drawing.Size(700,54)
$form.Controls.Add($status)
$help=New-Object Windows.Forms.Label
$help.Text="安装 69 项文字／字体／界面与 27 个字幕视频。请先关闭游戏。`r`n原资源备份保存在游戏内 .storycoop-chs，卸载前请保留。"
$help.Location=New-Object Drawing.Point(20,166);$help.Size=New-Object Drawing.Size(700,55)
$form.Controls.Add($help)
$buttons=@{}
foreach($entry in @(@('Install','安装／更新'),@('Verify','校验'),@('Remove','卸载汉化'),@('Open','打开资源目录'),@('Close','关闭'))) {
    $button=New-Object Windows.Forms.Button
    $button.Name=$entry[0];$button.Text=$entry[1]
    $button.Location=New-Object Drawing.Point((20+$buttons.Count*143),245);$button.Size=New-Object Drawing.Size(128,42)
    $buttons[$entry[0]]=$button;$form.Controls.Add($button)
}
function Update-ChsManagerStatus {
    if(!(Test-ShankGameFolder $path.Text)) {$status.Text='请选择含 bin 和 data-pc 的 Steam 原版 Shank 2 目录。';return}
    $state=Join-Path $path.Text '.storycoop-chs\state.json';$count=0
    if(Test-Path -LiteralPath $state) {
        try {$s=Get-Content -LiteralPath $state -Raw -Encoding UTF8 | ConvertFrom-Json;$count=@($s.files).Count} catch {$status.Text='安装记录无法读取，请使用校验查看详情。';return}
    }
    $status.Text=('当前目录：'+$path.Text+"`r`n登记已安装 "+$count+' / 96 项；操作前会校验原版程序和资源。')
}
function Invoke-ChsManagerAction([string]$Action) {
    if($script:chsManagerBusy) {return}
    $script:chsManagerBusy=$true
    try {
        $browse.Enabled=$false;$path.Enabled=$false
        foreach($b in $buttons.Values) {$b.Enabled=$false}
        $status.Text='正在校验并处理文件，请稍候…';[Windows.Forms.Application]::DoEvents()
        & (Join-Path $PSScriptRoot 'Coop-Localization.ps1') -Action $Action -Group All -GamePath $path.Text -NoUI | Out-Null
        Update-ChsManagerStatus
        $status.Text=('操作完成。'+"`r`n"+$status.Text)
        $form.Tag='Success'
    } catch {
        $form.Tag='Error';$status.Text=$_.Exception.Message
        if(!$NoShow) {$null=[Windows.Forms.MessageBox]::Show($form,$_.Exception.Message,'汉化操作未完成','OK','Error')}
    } finally {
        foreach($b in $buttons.Values) {$b.Enabled=$true}
        $browse.Enabled=$true;$path.Enabled=$true;$script:chsManagerBusy=$false
    }
}
$browse.Add_Click({
    $picker=New-Object Windows.Forms.FolderBrowserDialog
    $picker.Description='选择 Steam 原版 Shank 2 游戏目录'
    try {if($picker.ShowDialog($form) -eq 'OK') {$path.Text=$picker.SelectedPath}} finally {$picker.Dispose()}
})
$path.Add_TextChanged({Update-ChsManagerStatus})
$buttons.Install.Add_Click({Invoke-ChsManagerAction 'Install'})
$buttons.Verify.Add_Click({Invoke-ChsManagerAction 'Verify'})
$buttons.Remove.Add_Click({Invoke-ChsManagerAction 'Remove'})
$buttons.Open.Add_Click({
    if(Test-ShankGameFolder $path.Text) {Start-Process -FilePath 'explorer.exe' -ArgumentList ('"'+(Join-Path $path.Text 'data-pc')+'"') | Out-Null}
})
$buttons.Close.Add_Click({$form.Close()})
Update-ChsManagerStatus
if($NoShow) {return $form}
try {$null=$form.ShowDialog()} finally {$form.Dispose()}
