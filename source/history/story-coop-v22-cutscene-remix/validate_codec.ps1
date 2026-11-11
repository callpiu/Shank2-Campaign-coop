$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw 'Use 32-bit Windows PowerShell.' }
$reference = Join-Path (Split-Path -Parent $PSScriptRoot) 'story-coop-v07-dialogue\test_legacy_bink.ps1'
$source = Get-Content -LiteralPath $reference -Raw
$ffi = [regex]::Match($source, "(?ms)^Add-Type @'\r?\n(.*?)\r?\n'@")
if (!$ffi.Success) { throw 'Could not locate legacy Bink bindings.' }
Add-Type -TypeDefinition $ffi.Groups[1].Value
$codec = 'E:\SteamLibrary\steamapps\common\Shank 2\bin\binkw32.dll'
if ((Get-FileHash -LiteralPath $codec).Hash -ne '2d2beb4f5b38f9bda358543e1fd437af45a95d37066f926a1e0f105d304f419b') { throw 'Original game codec hash mismatch.' }
$library = [LegacyBinkTest]::LoadLibraryW($codec)
if ($library -eq [IntPtr]::Zero) { throw 'Cannot open original game codec.' }
$movies = @()
try {
    $open = [LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($library,'_BinkOpen@8'),[LegacyBinkTest+Open])
    $decode = [LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($library,'_BinkDoFrame@4'),[LegacyBinkTest+Decode])
    $next = [LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($library,'_BinkNextFrame@4'),[LegacyBinkTest+One])
    $close = [LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($library,'_BinkClose@4'),[LegacyBinkTest+One])
    foreach ($file in Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'remixed') -File -Filter '*.bik') {
        $handle = $open.Invoke($file.FullName,0)
        if ($handle -eq [IntPtr]::Zero) { throw ('Cannot open ' + $file.Name) }
        try {
            for ($frame = 0; $frame -lt 8; $frame++) {
                if ($decode.Invoke($handle) -ne 0) { throw ('Decode error: ' + $file.Name) }
                $next.Invoke($handle)
            }
            $movies += $file.Name
        } finally { $close.Invoke($handle) }
    }
} finally { $null = [LegacyBinkTest]::FreeLibrary($library) }
if ($movies.Count -ne 27) { throw 'Expected 27 movies.' }
@{ movies = $movies; frames_each = 8; original_codec = $true } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'codec-validation.json') -Encoding UTF8
Write-Output ('Original codec opened and decoded ' + $movies.Count + ' movies.')
