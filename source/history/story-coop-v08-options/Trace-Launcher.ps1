$ErrorActionPreference='Stop'
$log=Join-Path $PSScriptRoot 'launcher-startup.log'
try {
    [IO.File]::AppendAllText($log,('Entered wrapper '+[DateTime]::UtcNow.ToString('o')+"`r`n"))
    & (Join-Path $PSScriptRoot 'launcher\Coop-Launcher.ps1') -GamePath 'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test'
    [IO.File]::AppendAllText($log,"Launcher returned normally`r`n")
} catch {
    [IO.File]::AppendAllText($log,($_ | Out-String))
    exit 1
}
