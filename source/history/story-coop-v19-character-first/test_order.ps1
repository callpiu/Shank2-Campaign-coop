param([string]$Fixture,[string]$Ids,[string]$Report,[uint32]$BeginHint=0x75328c)
$ErrorActionPreference='Stop'
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class OrderTest {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint k,uint a);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]public delegate int Run(int op);
 public static Run Bind(int p){return (Run)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Run));}
 public static uint Read(int p){return unchecked((uint)Marshal.ReadInt32(new IntPtr(p)));}
 public static void Write(int p,uint v){Marshal.WriteInt32(new IntPtr(p),unchecked((int)v));}
}
'@
$v=0x20000000;$mem=[OrderTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(65536),0x3000,0x40)
if([IntPtr]::Size -ne 4 -or $mem.ToInt32() -ne $v){throw 'x86 allocation'}
$bytes=[IO.File]::ReadAllBytes($Fixture);$skins=Get-Content -LiteralPath $Ids -Raw | ConvertFrom-Json
$run=[OrderTest]::Bind($v+0x1800)
function Set-U([int]$o,[uint32]$n){[OrderTest]::Write($v+$o,$n)}
function Get-U([int]$o){[OrderTest]::Read($v+$o)}
function Reset{[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)}
function Assert-OriginalConfig{
 for($i=0;$i -lt 128;$i++){
  if([Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x5800+$i)) -ne $bytes[0x5800+$i]){throw 'Unconfirmed choice escaped transaction'}
 }
}
function Role([uint32]$skin){Set-U 0x81e8 $skin;$null=$run.Invoke(1);$null=$run.Invoke(2)}
function Equipment($m,$r,$t){Set-U 0x81dc $m;Set-U 0x81e0 $r;Set-U 0x81e4 $t;Set-U 0x8020 2;$null=$run.Invoke(8)}
$shank=@($skins|Where-Object {$_.family -eq 'shank'})[1].hash
$corina=@($skins|Where-Object {$_.family -eq 'corina'})[1].hash
$checks=0
Reset;$null=$run.Invoke(0)
if((Get-U 0x8020) -ne 3 -or (Get-U 0x303c) -ne 0 -or (Get-U 0x3014) -ne 0){throw 'P1 did not open with character first'}
$checks++
Role $corina
if((Get-U 0x8020) -ne 0 -or (Get-U 0x303c) -ne 1 -or (Get-U 0x3014) -ne 0){throw 'Role confirm did not enter same-player equipment'}
if((Get-U 0x3028) -ne 0 -or (Get-U 0x3e08) -ne 0){throw 'Character confirm prematurely advanced player/level'}
Assert-OriginalConfig;$checks++
Equipment 111 222 333;$null=$run.Invoke(2)
if((Get-U 0x8020) -ne 3 -or (Get-U 0x303c) -ne 0 -or (Get-U 0x3014) -ne 1){throw 'P2 did not open with character first'}
Assert-OriginalConfig;$checks++
Role $shank
if((Get-U 0x8020) -ne 0 -or (Get-U 0x303c) -ne 1){throw 'P2 role->equipment failed'}
Equipment 444 555 666
if((Get-U 0x3030) -ne 1 -or (Get-U 0x3e08) -ne 1 -or (Get-U 0x3010) -ne 0){throw 'Final P2 equipment did not commit and launch once'}
if((Get-U 0x5814) -ne $corina -or (Get-U 0x5854) -ne $shank -or (Get-U 0x5818) -ne 111 -or (Get-U 0x5858) -ne 444){throw 'Cross-family roles or equipment lost'}
if((Get-U 0x3e40) -ne 111 -or (Get-U 0x3e4c) -ne $corina){throw 'Native callback received wrong player'}
$checks++
Reset;$null=$run.Invoke(0);Role $corina;$null=$run.Invoke(5);$null=$run.Invoke(2)
if((Get-U 0x8020) -ne 3 -or (Get-U 0x303c) -ne 0 -or (Get-U 0x3014) -ne 0){throw 'Back from first weapon did not return to same character'}
Assert-OriginalConfig;$checks++
Reset;$null=$run.Invoke(0);Role $shank;Equipment 111 222 333;$null=$run.Invoke(2)
$null=$run.Invoke(5);$null=$run.Invoke(2)
if((Get-U 0x3014) -ne 0 -or (Get-U 0x8020) -ne 3){throw 'Back from P2 character did not return to P1 character'}
Assert-OriginalConfig;$checks++
Reset;$null=$run.Invoke(0);Role $shank;Equipment 111 222 333;$null=$run.Invoke(2)
Set-U 0x8024 0;$null=$run.Invoke(3)
Assert-OriginalConfig
if((Get-U 0x3010) -ne 0 -or (Get-U 0x301c) -ne 0){throw 'Cancel failed to clear role-first transaction'}
$checks++
foreach($skin in $skins){
 Reset;$null=$run.Invoke(0);Role $skin.hash
 if((Get-U 0x3054) -ne $skin.hash -or (Get-U 0x8020) -ne 0 -or (Get-U 0x3014) -ne 0){throw 'A role could not advance to equipment'}
 Assert-OriginalConfig;$checks++
}
Reset;Set-U 0x3000 0;$null=$run.Invoke(0)
if((Get-U 0x8020) -ne 0 -or (Get-U 0x3010) -ne 0){throw 'Non-scoped menu order changed'}
$checks++
Reset;$null=$run.Invoke(0);$null=$run.Invoke(2)
if((Get-U 0x3f14) -ne ($v+0x3320)){throw 'Character page still prompts Start instead of Continue'}
$checks++
Role $shank;Equipment 111 222 333;$null=$run.Invoke(2);Role $corina
Set-U 0x8020 2;$null=$run.Invoke(2)
if((Get-U 0x3f14) -ne $BeginHint){throw 'P2 last weapon must prompt Begin'}
$checks++
@{passed=$true;cases=$checks;all_17_roles=$true;character_before_equipment=$true;
 cross_family_commit=$true;back_and_cancel_checked=$true;gameplay_verified=$false} |
 ConvertTo-Json | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$checks+' native x86 role-first flow, all characters, shared commit and back/cancel cases.')
