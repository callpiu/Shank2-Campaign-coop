param([string]$GamePath,[switch]$NoUI)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms
. (Join-Path $PSScriptRoot 'Game-Paths.ps1')
. (Join-Path $PSScriptRoot 'Launcher-Strings.ps1')
. (Join-Path $PSScriptRoot 'Launcher-Preferences.ps1')
$script:uiLanguage=Get-SavedUiLanguage (Join-Path $PSScriptRoot 'launcher-settings.json')
try {
    if(!$GamePath) {$GamePath=Find-ShankGameFolder $PSScriptRoot}
    if(!(Test-ShankGameFolder $GamePath) -and !$NoUI) {
        $dialog=New-Object Windows.Forms.FolderBrowserDialog
        $dialog.Description=Get-UiText 'chooseFolder'
        try {if($dialog.ShowDialog() -ne 'OK') {return};$GamePath=$dialog.SelectedPath} finally {$dialog.Dispose()}
    }
    if(!(Test-ShankGameFolder $GamePath)) {throw (Get-UiText 'gameFolderRequired')}
    foreach($mode in @('Keyboard','Pads')) {$null=& (Join-Path $PSScriptRoot 'Manage-Coop.ps1') -Action Remove -InputMode $mode -GamePath $GamePath}
    if($NoUI) {Write-Output 'Removed v0.4 from selected game folder.'} else {$null=[Windows.Forms.MessageBox]::Show((Get-UiText 'removed'),(Get-UiText 'windowTitle'))}
} catch {
    if($NoUI) {throw}
    $null=[Windows.Forms.MessageBox]::Show($_.Exception.Message,(Get-UiText 'removeError'))
}
