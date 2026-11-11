$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'Portraits.ps1')
$catalog=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'catalog.json') -Raw | ConvertFrom-Json
$auditPath=Join-Path $PSScriptRoot 'portrait-audit'
$null=New-Item -ItemType Directory -Path $auditPath -Force
try {
    foreach($skin in $catalog.skins) {
        $image=Get-CoopPortrait 'E:\SteamLibrary\steamapps\common\Shank 2' $skin.id
        if(!$image) {throw ('No portrait: '+$skin.id)}
        $image.Save((Join-Path $auditPath ($skin.id+'.png')),[Drawing.Imaging.ImageFormat]::Png)
    }
    'Decoded all 17 portraits for independent pixel validation'
} finally {Close-CoopPortraits}
