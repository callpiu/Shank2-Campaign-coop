param([string]$Fixture,[string]$Report,[uint32]$Pose)
$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'x86 required'}
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class PoseTest {
 [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr p, UIntPtr s, uint t, uint a);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] public delegate int Run();
 public static Run Hook(int p){return (Run)Marshal.GetDelegateForFunctionPointer(new IntPtr(p),typeof(Run));}
}
'@
$v=0x20000000;$mem=[PoseTest]::VirtualAlloc([IntPtr]$v,[UIntPtr]::new(65536),0x3000,0x40)
if($mem.ToInt32() -ne $v){throw 'allocation failed'}
$bytes=[IO.File]::ReadAllBytes($Fixture)
function Reset {[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)}
function Get-I([int]$o){[Runtime.InteropServices.Marshal]::ReadInt32([IntPtr]($v+$o))}
function Get-U([int]$o){[BitConverter]::ToUInt32([BitConverter]::GetBytes((Get-I $o)),0)}
function Set-I([int]$o,[int]$value){[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($v+$o),$value)}
$run=[PoseTest]::Hook($v+0x1800)
Reset;$ret=$run.Invoke()
if($ret -ne 0x12345678 -or (Get-I 0x9000) -ne $v+0x6000 -or (Get-I 0x9008) -ne 0x44){throw 'Native call ABI changed'}
if((Get-I 0x9004) -eq $v+0x4000 -or (Get-I 0x9270) -ne -1 -or (Get-U 0x9290) -ne $Pose -or (Get-I 0x9298) -ne 0x3dcccccd){throw 'Own pose copy not used'}
for($i=0;$i -lt 0x26c;$i++){
 $original=[Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x4000+$i))
 $copied=[Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x9200+$i))
 if($original -ne $bytes[0x4000+$i]){throw 'Live/snapshot source was mutated'}
 if($i -eq 0x6c){if($copied -ne 0){throw 'Hidden copy'}}
 elseif($i -notin @(0x70,0x71,0x72,0x73,0x90,0x91,0x92,0x93,0x98,0x99,0x9a,0x9b) -and $original -ne $copied){throw ('Skin, transform or other packet field changed: '+$i)}
}
$cases=New-Object Collections.ArrayList
$null=$cases.Add(@{case='female_own_pose_copy_skin_transform_and_source_unchanged';passed=$true})
foreach($case in @(
 @{name='other_mode';offset=0x3004;value=0},
 @{name='other_actor_family';offset=0x407c;value=1},
 @{name='detached';offset=0x4070;value=-1},
 @{name='missing_parent';offset=0x4070;value=99},
 @{name='other_parent_family';offset=0x507c;value=1},
 @{name='other_packet_type';offset=0x4000;value=0},
 @{name='other_parent_type';offset=0x5000;value=0},
 @{name='missing_snapshot';offset=0x6000;value=0}
)){
 Reset;Set-I $case.offset $case.value;$null=$run.Invoke()
 if((Get-I 0x9004) -ne $v+0x4000){throw ('Native rendering bypassed: '+$case.name)}
 for($i=0;$i -lt 0x26c;$i++){
  if([Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x4000+$i)) -ne [Runtime.InteropServices.Marshal]::ReadByte([IntPtr]($v+0x9200+$i))){throw 'Fallback packet changed'}
 }
 $null=$cases.Add(@{case=$case.name;passed=$true})
}
@{case_count=$cases.Count;cases=@($cases);actual_x86=$true;game_process_modified=$false;render_only=$true} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output ('PASS: '+$cases.Count+' x86 render-only cases, full 620-byte source immutability, skin/transform preservation and native fallback.')
