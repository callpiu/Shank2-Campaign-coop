param([string]$Package,[string]$Game)
$ErrorActionPreference='Stop'
$form=. (Join-Path $Package 'patch\PatchManager.ps1') -GamePath $Game -NoShow
try {
    $click=[Windows.Forms.Button].GetMethod('OnClick',[Reflection.BindingFlags]'Instance,NonPublic')
    foreach($name in @('Install','Verify','Remove')) {
        $click.Invoke($form.Controls.Find($name,$false)[0],@([EventArgs]::Empty))
        if ($form.Tag -ne 'Success') { throw ('GUI action failed: '+$name+' '+$managerStatus.Text) }
    }
    $managerPath.Text=Join-Path $Game 'not-a-game'
    $click.Invoke($form.Controls.Find('Verify',$false)[0],@([EventArgs]::Empty))
    if ($form.Tag -ne 'Error') { throw 'GUI invalid-path error missing.' }
    if (!$form.Controls.Find('Install',$false)[0].Enabled -or !$managerBrowse.Enabled) { throw 'GUI remained disabled.' }
    Write-Output 'GUI actual Install/Verify/Remove/error events passed.'
} finally {$form.Dispose()}
