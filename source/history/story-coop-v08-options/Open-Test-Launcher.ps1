$ErrorActionPreference='Stop'
$launcher=Join-Path $PSScriptRoot 'launcher\Coop-Launcher.ps1'
$game='G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test'
$startInfo=New-Object Diagnostics.ProcessStartInfo
$startInfo.FileName="$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe"
$startInfo.Arguments='-NoProfile -ExecutionPolicy Bypass -File "'+$launcher+'" -GamePath "'+$game+'"'
$startInfo.UseShellExecute=$false
# Hide only the console. STARTUPINFO's SW_HIDE also hid the WinForms dialog.
$startInfo.CreateNoWindow=$true
$process=[Diagnostics.Process]::Start($startInfo)
Write-Output ('DEVELOPMENT_LAUNCHER_PID='+$process.Id)
