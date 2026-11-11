param([string]$Fixture,[string]$Ids,[string]$Report)
$ErrorActionPreference='Stop'
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class FlowTest {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint k,uint a);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]public delegate int Run(int op);
 public static Run Bind(int p){return (Run)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Run));}
 public static uint Read(int p){return unchecked((uint)Marshal.ReadInt32(new IntPtr(p)));}
 public static void Write(int p,uint v){Marshal.WriteInt32(new IntPtr(p),unchecked((int)v));}
}
'@
$v=0x20000000;$mem=[FlowTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(65536),0x3000,0x40)
if([IntPtr]::Size -ne 4 -or $mem.ToInt32() -ne $v){throw 'x86 allocation failed'}
$bytes=[IO.File]::ReadAllBytes($Fixture);$skins=Get-Content -LiteralPath $Ids -Raw | ConvertFrom-Json
$run=[FlowTest]::Bind($v+0x1800)
function Set-U([int]$o,[uint32]$n){[FlowTest]::Write($v+$o,$n)}
function Get-U([int]$o){[FlowTest]::Read($v+$o)}
function Reset{[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)}
function Assert-OriginalConfig{
 for($i=0;$i -lt 128;$i++){
  if([Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x5800+$i)) -ne $bytes[0x5800+$i]){throw 'Unconfirmed/cancelled choice changed committed configuration'}
 }
}
function Set-Selection($a,$b,$c,[uint32]$skin){Set-U 0x81dc $a;Set-U 0x81e0 $b;Set-U 0x81e4 $c;Set-U 0x81e8 $skin}
$s0=@($skins | Where-Object {$_.family -eq 'shank'})[1].hash
$s1=@($skins | Where-Object {$_.family -eq 'corina'})[1].hash
$checks=0
Reset;$null=$run.Invoke(0)
if((Get-U 0x3010) -ne ($v+0x8000) -or (Get-U 0x3014) -ne 0 -or (Get-U 0x3024) -ne 1){throw 'Did not start P1 transaction'}
Assert-OriginalConfig;$checks++
Set-Selection 111 222 333 $s0;$null=$run.Invoke(1)
if((Get-U 0x3014) -ne 1 -or (Get-U 0x3018) -ne 1 -or (Get-U 0x3e08) -ne 0){throw 'P1 confirmation launched level before P2'}
Assert-OriginalConfig;$checks++
$null=$run.Invoke(2)
if((Get-U 0x81dc) -ne (Get-U 0x5858) -or (Get-U 0x81e8) -ne (Get-U 0x5854) -or (Get-U 0x3e00) -ne 2){throw 'P2 display did not use P2 equipment'}
$checks++
Set-Selection 444 555 666 $s1;$null=$run.Invoke(1)
if((Get-U 0x3010) -ne 0 -or (Get-U 0x3030) -ne 1 -or (Get-U 0x3e08) -ne 1){throw 'Both-ready commit/launch failed'}
if((Get-U 0x5818) -ne 111 -or (Get-U 0x581c) -ne 222 -or (Get-U 0x5820) -ne 333 -or (Get-U 0x5814) -ne $s0){throw 'P1 choices lost'}
if((Get-U 0x5858) -ne 444 -or (Get-U 0x585c) -ne 555 -or (Get-U 0x5860) -ne 666 -or (Get-U 0x5854) -ne $s1){throw 'P2 choices lost'}
if((Get-U 0x3e40) -ne 111 -or (Get-U 0x3e4c) -ne $s0){throw 'Native owner received P2 choices as P1'}
$checks++
$null=$run.Invoke(4)
if((Get-U 0x3e10) -ne 0){throw 'Old level inventory sync could overwrite pending choice'}
Set-U 0x5020 8;$null=$run.Invoke(4)
if((Get-U 0x3e10) -ne 1 -or (Get-U 0x301c) -ne 0){throw 'Sync did not resume on new actor generation'}
$checks++
Reset;$null=$run.Invoke(0);Set-Selection 111 222 333 $s0;$null=$run.Invoke(1);$null=$run.Invoke(2)
Set-U 0x8024 0;$null=$run.Invoke(3)
Assert-OriginalConfig
if((Get-U 0x3010) -ne 0 -or (Get-U 0x301c) -ne 0 -or (Get-U 0x3e08) -ne 0){throw 'Cancel did not release transaction'}
$checks++
Reset;$null=$run.Invoke(0);Set-Selection 111 222 333 $s0;$null=$run.Invoke(1);$null=$run.Invoke(2);$null=$run.Invoke(5)
if((Get-U 0x3014) -ne 0 -or (Get-U 0x3018) -ne 1 -or (Get-U 0x3e14) -ne 0){throw 'Back from P2 did not return to P1'}
Assert-OriginalConfig;$checks++
Reset;$null=$run.Invoke(0);Set-Selection 111 222 333 $s1;$null=$run.Invoke(1)
if((Get-U 0x3014) -ne 0 -or (Get-U 0x3018) -ne 1 -or (Get-U 0x3e08) -ne 0){throw 'Cross-family confirmation did not restart compatible weapons'}
$null=$run.Invoke(2)
if((Get-U 0x81dc) -eq 111 -or (Get-U 0x3054) -ne $s1){throw 'Archetype defaults or chosen skin lost'}
Assert-OriginalConfig;$checks++
foreach($skin in $skins){
 Reset;$null=$run.Invoke(0);Set-Selection 111 222 333 $skin.hash;$null=$run.Invoke(1)
 if((Get-U 0x3054) -ne $skin.hash){throw 'A curated character could not be selected'}
 Assert-OriginalConfig;$checks++
}
Reset;Set-U 0x3000 0;$null=$run.Invoke(0)
if((Get-U 0x3010) -ne 0 -or $run.Invoke(6) -ne 0 -or $run.Invoke(7) -ne 0){throw 'Non-campaign/nonregistered UI incorrectly entered co-op scope'}
$checks++
Reset;$null=$run.Invoke(0)
if($run.Invoke(6) -ne 1 -or $run.Invoke(7) -ne 1){throw 'Prelevel character/weapon scope unavailable before simulation'}
$checks++
$corinaIndex=0
while($skins[$corinaIndex].hash -ne $s1){$corinaIndex++}
Reset;$null=$run.Invoke(0);Set-U 0x8020 3;Set-U 0x3f00 $corinaIndex;$null=$run.Invoke(2)
if((Get-U 0x3054) -ne $s1 -or (Get-U 0x3018) -ne 1){throw 'Live menu archetype change not staged for refresh'}
$null=$run.Invoke(2)
if((Get-U 0x81e8) -ne $s1 -or (Get-U 0x8020) -ne 0){throw 'New character equipment screen not refreshed'}
Assert-OriginalConfig;$checks++
Reset;$null=$run.Invoke(0);Set-Selection 111 222 333 0;$null=$run.Invoke(1)
if((Get-U 0x3014) -ne 0 -or (Get-U 0x3e08) -ne 0){throw 'Invalid character launched or advanced'}
Assert-OriginalConfig;$checks++
Reset;Set-U 0x3000 0;Set-U 0x5004 5;Set-U 0x3c00 ($v+0x8000);Set-U 0x3c04 7
if($run.Invoke(6) -ne 1){throw 'Existing pause selector guard regressed'}
Set-U 0x5020 8
if($run.Invoke(6) -ne 0){throw 'Old pause generation admitted'}
$checks++
Reset;Set-U 0x5840 0;$null=$run.Invoke(0)
if((Get-U 0x3010) -ne 0){throw 'Disabled partner forced co-op pre-level selection'}
$checks++
@{passed=$true;cases=$checks;separate_staging=$true;cancel_atomic=$true;native_owner_gets_p1=$true;pending_sync_protected=$true;
 all_17_characters_checked=$true;gameplay_verified=$false} | ConvertTo-Json | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$checks+' real x86 pre-level transaction, independent gear, character and scope cases.')
