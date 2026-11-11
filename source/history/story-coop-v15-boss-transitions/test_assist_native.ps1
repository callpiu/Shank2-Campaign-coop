param([string]$Fixture,[string]$Ids,[string]$Report)
$ErrorActionPreference='Stop'
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class AssistTest {
 [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint a,uint b);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Run(IntPtr receiver);
 public static Run Hook(int p){return (Run)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Run));}
}
'@
$v=0x20000000;$mem=[AssistTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(32768),0x3000,0x40)
if([IntPtr]::Size -ne 4 -or $mem.ToInt32() -ne $v){throw 'x86 allocation'}
$bytes=[IO.File]::ReadAllBytes($Fixture);$catalogIds=Get-Content -LiteralPath $Ids -Raw | ConvertFrom-Json
function Reset {[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)}
function Get-I([int]$o){[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$o))}
function Set-U([int]$o,[uint32]$value){$n=[BitConverter]::ToInt32([BitConverter]::GetBytes($value),0);[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$o),$n)}
$run=[AssistTest]::Hook($v+0x500);$count=0
foreach($receiver in @(0x6000,0x6100)){
 Reset
 if($run.Invoke([IntPtr]($v+$receiver)) -ne 124 -or (Get-I 0x1800) -ne 1 -or (Get-I 0x180c) -ne 0){throw 'Player immunity or ABI'}
 $count++
}
foreach($hash in $catalogIds.enemies){
 Reset;Set-U 0x44c0 $hash
 if($run.Invoke([IntPtr]($v+0x6200)) -ne 8 -or (Get-I 0x1810) -ne 0x49742400 -or (Get-I 0x1804) -ne 1){throw 'Enemy boost or native ABI'}
 $count++
}
foreach($hash in $catalogIds.bosses){
 Reset;Set-U 0x44c0 $hash
 if($run.Invoke([IntPtr]($v+0x6200)) -ne 8 -or (Get-I 0x1810) -ne 0x40a00000 -or (Get-I 0x1804) -ne 0){throw 'Boss damage changed'}
 $count++
}
Reset;Set-U 0x44c0 12345;$null=$run.Invoke([IntPtr]($v+0x6200));if((Get-I 0x1810) -ne 0x40a00000){throw 'Unknown actor changed'};$count++
Reset;Set-U 0x3004 0;Set-U 0x44c0 $catalogIds.enemies[0];$null=$run.Invoke([IntPtr]($v+0x6200));if((Get-I 0x1810) -ne 0x40a00000){throw 'Other mode changed'};$count++
Reset;Set-U 0x4320 0;Set-U 0x44c0 $catalogIds.enemies[0];$null=$run.Invoke([IntPtr]($v+0x6200));if((Get-I 0x1810) -ne 0x40a00000){throw 'Foreign simulation changed'};$count++
Reset;Set-U 0x3080 0;Set-U 0x44c0 $catalogIds.enemies[0];$null=$run.Invoke([IntPtr]($v+0x6200));if((Get-I 0x1810) -ne 0){throw 'Zero-damage contact became fatal'};$count++
@{passed=$true;cases=$count;ordinary_enemy_types=$catalogIds.enemies.Count;boss_types_excluded=$catalogIds.bosses.Count;abi_flags_verified=$true} | ConvertTo-Json | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$count+' x86 assist cases; both players, 140 ordinary enemy types, 15 excluded Boss types, zero-contact and scope guards.')
