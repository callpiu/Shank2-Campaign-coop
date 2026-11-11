function Test-ShankGameFolder([string]$Path) {
    if([string]::IsNullOrWhiteSpace($Path)) {return $false}
    return ((Test-Path -LiteralPath (Join-Path $Path 'bin\shank2.exe') -PathType Leaf) -and
            (Test-Path -LiteralPath (Join-Path $Path 'data-pc\ui\campaignscreen.chui') -PathType Leaf))
}
function Get-SavedGameFolder([string]$SettingsPath) {
    try {
        if(Test-Path -LiteralPath $SettingsPath) {
            $saved=Get-Content -LiteralPath $SettingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
            if(Test-ShankGameFolder ([string]$saved.gamePath)) {return [IO.Path]::GetFullPath([string]$saved.gamePath)}
        }
    } catch { }
    return ''
}
function ConvertFrom-VdfPath([string]$Value) {return $Value.Replace('\\','\').Replace('\"','"')}
function Get-SteamLibraryFolders([string]$SteamRoot) {
    $paths=New-Object Collections.Generic.List[string]
    if([string]::IsNullOrWhiteSpace($SteamRoot)) {return}
    $paths.Add($SteamRoot)
    $vdf=Join-Path $SteamRoot 'steamapps\libraryfolders.vdf'
    if(Test-Path -LiteralPath $vdf -PathType Leaf) {
        try {
            $text=Get-Content -LiteralPath $vdf -Raw -Encoding UTF8
            foreach($match in [regex]::Matches($text,'"(?:path|[0-9]+)"\s*"((?:\\.|[^"\\])*)"')) {
                $path=ConvertFrom-VdfPath $match.Groups[1].Value
                if([IO.Path]::IsPathRooted($path)) {$paths.Add($path)}
            }
        } catch { }
    }
    return $paths | Select-Object -Unique
}
function Find-ShankGameFolder([string]$PackageRoot,[string[]]$SteamRoots=@(),[switch]$SkipSystemDiscovery) {
    $saved=Get-SavedGameFolder (Join-Path $PackageRoot 'loadouts.json')
    if($saved) {return $saved}
    foreach($candidate in @($PackageRoot,(Split-Path -Parent $PackageRoot))) {
        if(Test-ShankGameFolder $candidate) {return [IO.Path]::GetFullPath($candidate)}
    }
    $roots=New-Object Collections.Generic.List[string]
    foreach($root in $SteamRoots) {if($root) {$roots.Add($root)}}
    if(!$SkipSystemDiscovery) {
        foreach($key in @('HKCU:\Software\Valve\Steam','HKLM:\SOFTWARE\WOW6432Node\Valve\Steam','HKLM:\SOFTWARE\Valve\Steam')) {
            $steam=Get-ItemProperty -LiteralPath $key -ErrorAction SilentlyContinue
            foreach($property in @('SteamPath','InstallPath')) {if($steam.$property) {$roots.Add([string]$steam.$property)}}
        }
        foreach($folder in @([Environment]::GetFolderPath('ProgramFilesX86'),[Environment]::GetFolderPath('ProgramFiles'))) {
            if($folder) {$roots.Add((Join-Path $folder 'Steam'))}
        }
    }
    foreach($steamRoot in ($roots | Select-Object -Unique)) {
        foreach($library in (Get-SteamLibraryFolders $steamRoot)) {
            $common=Join-Path $library 'steamapps\common'
            $names=New-Object Collections.Generic.List[string]
            $manifest=Join-Path $library 'steamapps\appmanifest_102840.acf'
            if(Test-Path -LiteralPath $manifest -PathType Leaf) {
                try {
                    $text=Get-Content -LiteralPath $manifest -Raw -Encoding UTF8
                    $match=[regex]::Match($text,'"installdir"\s*"((?:\\.|[^"\\])*)"')
                    if($match.Success) {
                        $name=ConvertFrom-VdfPath $match.Groups[1].Value
                        if($name -and $name -notin @('.','..') -and [IO.Path]::GetFileName($name) -eq $name) {$names.Add($name)}
                    }
                } catch { }
            }
            $names.Add('Shank 2')
            foreach($name in $names) {
                $candidate=Join-Path $common $name
                if(Test-ShankGameFolder $candidate) {return [IO.Path]::GetFullPath($candidate)}
            }
        }
    }
    return ''
}
