$ErrorActionPreference='Stop'
try {
    & (Join-Path $PSScriptRoot 'Coop-Launcher.ps1')
} catch {
    $log=Join-Path $PSScriptRoot 'startup-error.log'
    try {$_ | Out-String | Set-Content -LiteralPath $log -Encoding UTF8} catch { }
    Add-Type -AssemblyName System.Windows.Forms
    $null=[Windows.Forms.MessageBox]::Show(('Could not open the launcher. Details: '+$log),'Shank 2 Story Co-op')
}
