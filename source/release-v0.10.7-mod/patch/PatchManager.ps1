param([string]$GamePath,[switch]$NoShow)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()
. (Join-Path $PSScriptRoot 'Game-Paths.ps1')
$managerInfo=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if (!$GamePath) { $GamePath=Find-ShankGameFolder $PSScriptRoot }
$managerForm=[Windows.Forms.Form]::new()
$managerForm.Text='Shank 2 v0.10.3 - '+$managerInfo.display_name
$managerForm.ClientSize=[Drawing.Size]::new(790,300)
$managerForm.AutoScaleMode='Dpi'; $managerForm.StartPosition='CenterScreen'; $managerForm.Font=[Drawing.Font]::new('Segoe UI',9)
$managerPath=[Windows.Forms.TextBox]::new(); $managerPath.SetBounds(18,40,620,27);$managerPath.Text=$GamePath;$managerForm.Controls.Add($managerPath)
$managerBrowse=[Windows.Forms.Button]::new();$managerBrowse.Text='Browse';$managerBrowse.SetBounds(650,38,120,31);$managerForm.Controls.Add($managerBrowse)
$managerStatus=[Windows.Forms.Label]::new();$managerStatus.SetBounds(18,85,750,70);$managerForm.Controls.Add($managerStatus)
$managerHint=[Windows.Forms.Label]::new();$managerHint.SetBounds(18,160,750,48)
$managerHint.Text="Close the game before installing/removing. Launch normally from Steam after installation.`r`nOriginal files are backed up under .shank2-patch in the game directory."
$managerForm.Controls.Add($managerHint)
$managerButtons=@{}
foreach($entry in @(@('Install','Install'),@('Verify','Verify'),@('Remove','Remove'),@('Controls','Keys'),@('Open','Folder'),@('Close','Close'))) {
    $button=[Windows.Forms.Button]::new();$button.Name=$entry[0];$button.Text=$entry[1]
    $button.SetBounds((18+128*$managerButtons.Count),229,120,36);$managerForm.Controls.Add($button);$managerButtons[$entry[0]]=$button
}
$managerButtons.Controls.Visible=[bool]$managerInfo.includes_mod
function Update-PatchStatus {
    if (!(Test-ShankGameFolder $managerPath.Text)) { $managerStatus.Text='Select the Shank 2 game folder (bin + data-pc)';return }
    $p=Join-Path $managerPath.Text '.shank2-patch\state.json'
    if (Test-Path -LiteralPath $p) {
        try { $s=Get-Content -LiteralPath $p -Raw -Encoding UTF8 | ConvertFrom-Json;$managerStatus.Text='Installed'+$s.profile+' '+$s.version+"`r`n"+$managerPath.Text }
        catch { $managerStatus.Text='Receipt unreadable' }
    } else { $managerStatus.Text='Not installed by this manager'+"`r`n"+$managerPath.Text }
}
function Invoke-PatchAction([string]$Action) {
    if ($script:managerBusy) {return};$script:managerBusy=$true
    try {
        foreach($b in $managerButtons.Values){$b.Enabled=$false};$managerBrowse.Enabled=$false;$managerPath.Enabled=$false
        $managerStatus.Text='Working';[Windows.Forms.Application]::DoEvents()
        & (Join-Path $PSScriptRoot 'Install-Patch.ps1') -Action $Action -GamePath $managerPath.Text -NoUI | Out-Null
        Update-PatchStatus;$managerStatus.Text='Completed'+"`r`n"+$managerStatus.Text;$managerForm.Tag='Success'
    } catch {
        $managerForm.Tag='Error';$managerStatus.Text=$_.Exception.Message
        if (!$NoShow) {[void][Windows.Forms.MessageBox]::Show($managerForm,$_.Exception.Message,'Shank 2','OK','Error')}
    } finally {
        foreach($b in $managerButtons.Values){$b.Enabled=$true};$managerBrowse.Enabled=$true;$managerPath.Enabled=$true;$script:managerBusy=$false
    }
}
$managerButtons.Install.Add_Click({Invoke-PatchAction 'Install'})
$managerButtons.Verify.Add_Click({Invoke-PatchAction 'Verify'})
$managerButtons.Remove.Add_Click({Invoke-PatchAction 'Remove'})
$managerButtons.Controls.Add_Click({ & (Join-Path $PSScriptRoot 'Coop-Key-Settings.ps1') -GamePath $managerPath.Text })
$managerButtons.Open.Add_Click({if(Test-ShankGameFolder $managerPath.Text){Start-Process explorer.exe -ArgumentList ('"'+$managerPath.Text+'"')}})
$managerButtons.Close.Add_Click({$managerForm.Close()})
$managerBrowse.Add_Click({
    $p=[Windows.Forms.FolderBrowserDialog]::new()
    try {if($p.ShowDialog($managerForm) -eq 'OK'){$managerPath.Text=$p.SelectedPath}} finally {$p.Dispose()}
})
$managerPath.Add_TextChanged({Update-PatchStatus})
Update-PatchStatus
if ($NoShow) {return $managerForm}
try {[void]$managerForm.ShowDialog()} finally {$managerForm.Dispose()}
