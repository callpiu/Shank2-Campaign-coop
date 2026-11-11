param([string]$Fixture,[string]$Report)
$ErrorActionPreference='Stop'
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class DeferredTest {
 [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint a,uint b);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Run();
 public static Run Hook(int p){return (Run)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Run));}
}
'@
$v=0x20000000;$mem=[DeferredTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(65536),0x3000,0x40)
if($mem.ToInt32() -ne $v -or [IntPtr]::Size -ne 4){throw 'x86 allocation'}
$bytes=[IO.File]::ReadAllBytes($Fixture)
function Reset{[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)}
function Get-I([int]$o){[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$o))}
function Set-I([int]$o,[int]$n){[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$o),$n)}
function Assert-Sources{
 foreach($o in @(0x4000,0x5000)){
  for($i=0;$i -lt 0x26c;$i++){
   if([Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+$o+$i)) -ne $bytes[$o+$i]){throw 'Source packet changed'}
  }
 }
}
$run=[DeferredTest]::Hook($v+0x1800)
$old=[DeferredTest]::Hook($v+0x1900)
$late=[DeferredTest]::Hook($v+0x1a00)
Reset
if($old.Invoke() -ne 7 -or (Get-I 0x7200) -ne 2){throw 'Old regression setup failed'}
$escaped=0
foreach($o in @(0x7000,0x7008)){if((Get-I $o) -notin @(($v+0x4000),($v+0x5000))){$escaped++}}
if($escaped -ne 2){throw 'Old unsafe implementation must fail the lifetime invariant'}
Reset
if($run.Invoke() -ne 7 -or (Get-I 0x9000) -ne 2){throw 'Expected two adapted draws and preserved registers'}
if((Get-I 0x7000) -ne ($v+0x4000) -or (Get-I 0x7008) -ne ($v+0x5000)){throw 'Temporary packet escaped'}
if((Get-I 0x7004) -ne 0x3f292492 -or (Get-I 0x700c) -ne 0x3f292492){throw 'Opacity changed'}
if((Get-I 0x3040) -ne 1 -or (Get-I 0x3044) -ne 2){throw 'Missing adaptation/retention evidence'}
if((Get-I 0x9270) -ne -1 -or (Get-I 0x9500) -ne 0x5b1eb075 -or (Get-I 0x9508) -ne 0x3dcccccd){throw 'Wrong replacement pose'}
Assert-Sources
if($late.Invoke() -ne 7 -or (Get-I 0x9000) -ne 4 -or (Get-I 0x7200) -ne 2){throw 'Deferred pass did not render exactly boss + victim once'}
if((Get-I 0x3040) -ne 2 -or (Get-I 0x3044) -ne 2){throw 'Deferred metrics changed'}
Assert-Sources
$count=3
foreach($start in @(1,20,62)){
 Reset
 for($i=0;$i -lt $start;$i++){Set-I (0x7000+$i*8) ($v+0x4000);Set-I (0x7004+$i*8) 1234}
 Set-I 0x7200 $start
 if($run.Invoke() -ne 7 -or (Get-I 0x7200) -ne ($start+2)){throw 'List boundary changed'}
 for($i=0;$i -lt $start;$i++){if((Get-I (0x7000+$i*8)) -ne ($v+0x4000) -or (Get-I (0x7004+$i*8)) -ne 1234){throw 'Unrelated list entry changed'}}
 if((Get-I (0x7000+$start*8)) -ne ($v+0x4000) -or (Get-I (0x7008+$start*8)) -ne ($v+0x5000)){throw 'Boundary clone escaped'}
 Assert-Sources;$count++
}
Reset;Set-I 0x7200 63
if($run.Invoke() -ne 7 -or (Get-I 0x9000) -ne 1 -or (Get-I 0x7200) -ne 64 -or (Get-I 0x71f8) -ne ($v+0x4000)){throw 'Capacity fallback changed'}
$count++
foreach($case in @(@(0x3004,0),@(0x407c,1),@(0x507c,1),@(0x4070,-1),@(0x4070,99),@(0x5000,0),@(0x6000,0))){
 Reset;Set-I $case[0] $case[1];$null=$run.Invoke()
 if((Get-I 0x9000) -ne 1 -or (Get-I 0x7000) -ne ($v+0x4000)){throw 'Fallback changed'}
 $count++
}
@{passed=$true;cases=$count;old_implementation_escaped_stack_pointers=$escaped;
 native_enqueue_instructions_used=$true;deferred_second_pass_exercised=$true;
 source_packets_unchanged=$true;native_list_capacity=64;gameplay_verified=$false} |
 ConvertTo-Json | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$count+' x86 cases; old hook reproduces two dangling queue entries; new hook retains original packet lifetimes.')
