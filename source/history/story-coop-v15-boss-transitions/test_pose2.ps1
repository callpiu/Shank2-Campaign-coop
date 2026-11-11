param([string]$Fixture,[string]$Report)
$ErrorActionPreference='Stop'
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class Pose2Test {
 [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint a,uint b);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Run();
 public static Run Hook(int p){return (Run)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Run));}
}
'@
$v=0x20000000;$mem=[Pose2Test]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(65536),0x3000,0x40)
if($mem.ToInt32() -ne $v -or [IntPtr]::Size -ne 4){throw 'x86 allocation'}
$bytes=[IO.File]::ReadAllBytes($Fixture)
function Reset{[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)}
function Get-I([int]$o){[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$o))}
function Set-I([int]$o,[int]$n){[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$o),$n)}
$run=[Pose2Test]::Hook($v+0x1800)
Reset
if($run.Invoke() -ne 7 -or (Get-I 0x9000) -ne 2){throw 'Expected boss then female draw'}
if((Get-I 0x9270) -ne -1 -or (Get-I 0x9500) -ne 0x5b1eb075 -or (Get-I 0x9508) -ne 0x3dcccccd){throw 'Wrong split pose'}
for($i=0;$i -lt 0x26c;$i++){
 foreach($o in @(0x4000,0x5000)){
  if([Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+$o+$i)) -ne $bytes[$o+$i]){throw 'Source packet mutated'}
 }
}
$count=1
foreach($case in @(@(0x3004,0),@(0x407c,1),@(0x507c,1),@(0x4070,-1),@(0x4070,99),@(0x5000,0),@(0x6000,0))){
 Reset;Set-I $case[0] $case[1];$null=$run.Invoke()
 if((Get-I 0x9000) -ne 1){throw 'Fallback changed'}
 $count++
}
@{passed=$true;cases=$count;correct_boss_to_victim_direction=$true;source_packets_unchanged=$true} | ConvertTo-Json | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$count+' x86 boss-to-victim rendering regressions, both 620-byte source packets unchanged.')
