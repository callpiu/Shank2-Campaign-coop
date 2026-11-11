param([string]$Runtime,[string]$Fixture,[string]$Report)
$ErrorActionPreference='Stop'
$manager=. (Join-Path $Runtime 'Localization-Manager.ps1') -GamePath $Fixture -NoShow
$checks=New-Object Collections.ArrayList
try {
    $manager.ShowInTaskbar=$false;$manager.Opacity=0;$manager.Show()
    foreach($name in @('Install','Verify','Remove','Open','Close','Browse')) {
        $control=$manager.Controls.Find($name,$true)[0]
        if(!$control) {throw ('Missing control '+$name)}
        $size=[Windows.Forms.TextRenderer]::MeasureText($control.Text,$control.Font)
        if($size.Width -gt $control.Width - 8 -or $size.Height -gt $control.Height - 4) {throw ('Clipped control '+$name)}
    }
    foreach($action in @('Install','Verify','Install','Remove')) {
        $manager.Tag='Pending'
        $manager.Controls.Find($action,$true)[0].PerformClick()
        if($manager.Tag -ne 'Success') {throw ($action+': '+$manager.Controls.Find('Status',$true)[0].Text)}
        $null=$checks.Add(@{action=$action;success=$true})
    }
    $manager.Controls.Find('GamePath',$true)[0].Text=Join-Path $Fixture 'not-a-game'
    $manager.Tag='Pending';$manager.Controls.Find('Verify',$true)[0].PerformClick()
    if($manager.Tag -ne 'Error') {throw 'Invalid game path did not produce a handled error.'}
    $null=$checks.Add(@{action='invalid_target_error';success=$true})
    @{checks=@($checks);localized_labels_fit=$true;execution='same transactional script, in-process, no child installer'} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Report -Encoding UTF8
    Write-Output 'GUI: install, verify, repeat install, remove, invalid-path error and control-label bounds passed.'
} finally {$manager.Close();$manager.Dispose()}
