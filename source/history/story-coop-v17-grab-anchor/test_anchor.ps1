param([string]$Fixture,[string]$Report,[float]$PelvisX,[float]$PelvisY)
$ErrorActionPreference='Stop'
$anchorReport=$Report
. (Join-Path (Split-Path $PSScriptRoot -Parent) 'story-coop-v16-crash-recovery\test_deferred.ps1') $Fixture ($Report+'.deferred.json')
function Get-F([int]$o){[BitConverter]::ToSingle([BitConverter]::GetBytes((Get-I $o)),0)}
function Set-F([int]$o,[float]$f){Set-I $o ([BitConverter]::ToInt32([BitConverter]::GetBytes($f),0))}
$cases=@(
 @(1,0,55752.27734375,0,1,1365.2650146484375),
 @(-1,0,55752.27734375,0,1,1365.2650146484375),
 @(0,-1,500,1,0,300),
 @(1.5,0.3,900,-0.2,0.8,800),
 @(-0.7,0.1,300,0.25,1.2,700)
)
foreach($m in $cases){
 Reset
 for($i=0;$i -lt 6;$i++){Set-F (0x503c+$i*4) $m[$i]}
 if($run.Invoke() -ne 7){throw 'Alignment call or ABI failed'}
 $dx=Get-F 0x94b4;$dy=Get-F 0x94c0
 $worldX=$m[0]*$PelvisX+$m[1]*$PelvisY+$dx
 $worldY=$m[3]*$PelvisX+$m[4]*$PelvisY+$dy
 if([Math]::Abs($worldX-$m[2]) -gt 0.01 -or [Math]::Abs($worldY-$m[5]) -gt 0.01){throw 'Pelvis did not land on original grab anchor'}
 $allowed=@(0x44,0x45,0x46,0x47,0x50,0x51,0x52,0x53,0x6c,0x70,0x71,0x72,0x73,0x90,0x91,0x92,0x93,0x98,0x99,0x9a,0x9b)
 for($i=0;$i -lt 0x26c;$i++){
  if($i -notin $allowed -and [Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x9470+$i)) -ne [Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x5000+$i))){throw 'Unexpected clone field changed, including shadow matrix'}
 }
 if((Get-I 0x7008) -ne ($v+0x5000)){throw 'Aligned clone leaked into delayed render queue'}
 if($late.Invoke() -ne 7 -or (Get-I 0x9000) -ne 4){throw 'Deferred aligned draw failed'}
 for($i=0;$i -lt 6;$i++){
  if([Math]::Abs((Get-F (0x503c+$i*4))-$m[$i]) -gt 0.01){throw 'Source world transform changed'}
 }
}
@{passed=$true;alignment_cases=$cases.Count;deferred_regressions=14;local_pelvis=@($PelvisX,$PelvisY);
 mirrored_scaled_rotated_sheared_checked=$true;shadow_unchanged=$true;source_unchanged=$true;gameplay_verified=$false} |
 ConvertTo-Json | Set-Content -LiteralPath $anchorReport -Encoding UTF8
Write-Output 'PASS: 5 x86 world-anchor cases, unchanged source/shadow, deferred lifetime regression preserved.'
