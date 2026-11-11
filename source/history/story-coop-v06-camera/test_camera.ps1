$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'Use x86 Windows PowerShell.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class CameraFitTest {
 [DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint k,uint a);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]public delegate void Fit(IntPtr state);
 public static Fit Bind(IntPtr p){return (Fit)Marshal.GetDelegateForFunctionPointer(p,typeof(Fit));}
}
'@
$mem=[CameraFitTest]::VirtualAlloc([IntPtr]0x20000000,[UIntPtr]::new([uint32]12288),0x3000,0x40)
if($mem.ToInt32() -ne 0x20000000){throw 'Allocation failed.'}
$bytes=[IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'camera-test.bin'))
[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
$fit=[CameraFitTest]::Bind([IntPtr]0x20002000);$state=[IntPtr]0x20002400
function Set-Float($offset,[single]$value){[Runtime.InteropServices.Marshal]::Copy([BitConverter]::GetBytes($value),0,[IntPtr]($state.ToInt32()+$offset),4)}
function Get-Float($offset){$a=New-Object byte[] 4;[Runtime.InteropServices.Marshal]::Copy([IntPtr]($state.ToInt32()+$offset),$a,0,4);[BitConverter]::ToSingle($a,0)}
function Setup([single]$zoom,[single]$x1,[single]$y1,[single]$x2,[single]$y2,[single]$dt) {
 $zero=New-Object byte[] 64;[Runtime.InteropServices.Marshal]::Copy($zero,0,$state,64)
 Set-Float 8 $zoom;Set-Float 12 $x1;Set-Float 16 $y1;Set-Float 20 $x2;Set-Float 24 $y2;Set-Float 28 $dt
}
$checks=0
foreach($zoom in @(.2,.4,.7,1.2)) {
 Setup $zoom -100 -100 100 -100 (1/60);$fit.Invoke($state)
 if([math]::Abs((Get-Float 40)-$zoom) -gt .00001){throw 'Nearby players changed native zoom.'};$checks++
}
Setup .8 -1100 -100 1100 -100 (1/60);$previous=.8
for($i=0;$i -lt 90;$i++) {
 $fit.Invoke($state);$value=Get-Float 40
 if($value -gt $previous+.00001 -or $value -lt .5-.00001){throw 'Zoom-out was not smooth and bounded.'}
 $previous=$value
}
if([math]::Abs($previous-(640/1260)) -gt .001){throw 'Separated-player framing target is wrong.'};$checks++
Set-Float 12 -100;Set-Float 20 100
for($i=0;$i -lt 180;$i++) {
 $fit.Invoke($state);$value=Get-Float 40
 if($value -lt $previous-.00001 -or $value -gt .80001){throw 'Zoom-in was not smooth and bounded.'}
 $previous=$value
}
if($previous -lt .799){throw 'Nearby zoom did not recover.'};$checks++
Setup .8 -100 -800 100 800 (1/60)
for($i=0;$i -lt 120;$i++){$fit.Invoke($state)}
if([math]::Abs((Get-Float 40)-.5) -gt .0001){throw 'Vertical separation exceeded the 1.6x cap.'};$checks++
foreach($dt in @(0,-1,.5)) {
 Setup .8 -1100 -100 1100 -100 $dt;$fit.Invoke($state);$value=Get-Float 40
 if($value -lt .5 -or $value -gt .80001){throw 'Pause or dt spike exceeded camera limits.'}
 if($dt -le 0 -and [math]::Abs($value-.8) -gt .00001){throw 'Paused camera zoom drifted.'};$checks++
}
Setup .8 -1100 -100 1100 -100 (1/60)
Set-Float 32 .8;[Runtime.InteropServices.Marshal]::WriteInt32([IntPtr]($state.ToInt32()+36),1);Set-Float 8 .4
$fit.Invoke($state);if((Get-Float 40) -gt .40001){throw 'Author zoom change was overwritten.'};$checks++
foreach($bad in @([single]::PositiveInfinity,[single]::NaN,20000000)) {
 Setup .8 0 -100 $bad -100 (1/60);$fit.Invoke($state)
 if([math]::Abs((Get-Float 40)-.8) -gt .00001){throw 'Invalid input changed native camera.'};$checks++
}
Write-Output "Passed $checks native fitter cases (bounded zoom, smooth recovery, dt/invalid guards and authored zoom)."
