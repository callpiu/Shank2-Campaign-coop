param([string]$Fixture,[string]$Report)
$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'x86 required'}
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class TeleportTest {
 [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p, UIntPtr s, uint t, uint a);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Run();
 public static Run Hook(int p){return (Run)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Run));}
}
'@
$v=0x20000000;$mem=[TeleportTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(65536),0x3000,0x40)
if($mem.ToInt32() -ne $v){throw 'allocation failed'}
$bytes=[IO.File]::ReadAllBytes($Fixture)
function Reset {[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)}
function Get-I([int]$o){[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$o))}
function Set-I([int]$o,[int]$value){[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$o),$value)}
$fixed=[TeleportTest]::Hook($v+0x1800);$stock=[TeleportTest]::Hook($v+0x1840)
$cases=New-Object Collections.ArrayList
Reset;$null=$stock.Invoke()
if((Get-I 0x9000) -ne 1 -or (Get-I 0x5070) -ne 0){throw 'Original single-context reproduction failed'}
$null=$cases.Add(@{case='original_moves_only_triggering_player';passed=$true})
foreach($slot in @(0,1)){
 Reset;Set-I 0x6008 ($v+0x4000+0x1000*$slot)
 $ret=$fixed.Invoke()
 if((Get-I 0x9000) -ne 2 -or (Get-I 0x4070) -ne (Get-I 0x2008) -or (Get-I 0x5070) -ne (Get-I 0x2008) -or (Get-I 0x4074) -ne (Get-I 0x200c) -or (Get-I 0x5074) -ne (Get-I 0x200c)){throw 'Pair not moved'}
 if($ret -ne 1 -or (Get-I 0x6008) -ne $v+0x4000+0x1000*$slot -or (Get-I 0x6004) -ne 0x1234 -or (Get-I 0x600c) -ne 0x5678){throw 'Return value or original context changed'}
 if((Get-I 0x9100) -ne $v+0x4000+0x1000*$slot -or (Get-I 0x9104) -eq (Get-I 0x9100)){throw 'Trigger/partner order or dedup failed'}
 $null=$cases.Add(@{case=('both_players_trigger_'+$slot);passed=$true})
}
foreach($case in @(
 @{name='other_mode';offset=0x3004;value=0},
 @{name='other_destination';offset=0x2008;value=0},
 @{name='other_height';offset=0x200c;value=0},
 @{name='no_simulation';offset=0x3024;value=0},
 @{name='foreign_actor_simulation';offset=0x4020;value=0},
 @{name='foreign_partner_simulation';offset=0x5020;value=0},
 @{name='missing_partner';offset=0x3010;value=0},
 @{name='same_actor_in_both_slots';offset=0x3010;value=($v+0x4000)},
 @{name='nonplayer_context';offset=0x300c;value=($v+0x5100)}
)){
 Reset;Set-I $case.offset $case.value;$null=$fixed.Invoke()
 if((Get-I 0x9000) -ne 1){throw ('Fallback changed: '+$case.name)}
 $null=$cases.Add(@{case=$case.name;passed=$true})
}
@{case_count=$cases.Count;cases=@($cases);actual_x86=$true;game_process_modified=$false} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$cases.Count+' x86 boss teleport regressions, native single-player reproduction and paired movement.')
