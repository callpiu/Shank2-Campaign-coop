function Get-SavedUiLanguage([string]$Path) {
    try {
        if(Test-Path -LiteralPath $Path) {
            $preferences=Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
            $language=([string]$preferences.language).ToLowerInvariant()
            if($preferences.format -eq 1 -and $language -in @('en','zh')) {return $language}
        }
    } catch { }
    return 'en'
}
function Save-UiLanguage([string]$Path,[ValidateSet('en','zh')][string]$Language) {
    $target=[IO.Path]::GetFullPath($Path)
    $temporary=Join-Path ([IO.Path]::GetDirectoryName($target)) ('.launcher-language-'+[Guid]::NewGuid().ToString('N')+'.tmp')
    try {
        $json=[ordered]@{format=1;language=$Language.ToLowerInvariant()} | ConvertTo-Json
        [IO.File]::WriteAllText($temporary,$json,(New-Object Text.UTF8Encoding($false)))
        # PowerShell 5.1 binds plain $null to an empty string for this overload.
        if([IO.File]::Exists($target)) {[IO.File]::Replace($temporary,$target,[NullString]::Value)} else {[IO.File]::Move($temporary,$target)}
    } finally {
        if([IO.File]::Exists($temporary)) {[IO.File]::Delete($temporary)}
    }
}
