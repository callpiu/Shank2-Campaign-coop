$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'Use x86 Windows PowerShell for the original game codec.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class LegacyBinkTest {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]public static extern IntPtr LoadLibraryW(string p);
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi,ExactSpelling=true)]public static extern IntPtr GetProcAddress(IntPtr h,string n);
 [DllImport("kernel32.dll")]public static extern bool FreeLibrary(IntPtr h);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]public delegate IntPtr Open([MarshalAs(UnmanagedType.LPStr)]string p,uint flags);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]public delegate int Decode(IntPtr p);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]public delegate void One(IntPtr p);
 public static Delegate Bind(IntPtr p,Type t){if(p==IntPtr.Zero)throw new Exception("Missing codec entry point");return Marshal.GetDelegateForFunctionPointer(p,t);}
}
'@
$codec='E:\SteamLibrary\steamapps\common\Shank 2\bin\binkw32.dll'
$manifest=Get-Content 'G:\shank2\outputs\Shank2-StoryCoop-v0.5-CHS\patch\manifest.json' -Raw | ConvertFrom-Json
if((Get-FileHash -LiteralPath $codec).Hash -ne $manifest.guards.'bin/binkw32.dll'){throw 'Original game codec hash mismatch.'}
$dll=[LegacyBinkTest]::LoadLibraryW($codec)
if($dll -eq [IntPtr]::Zero){throw 'Could not load original game Bink library.'}
$movie=[IntPtr]::Zero
try {
 $open=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkOpen@8'),[LegacyBinkTest+Open])
 $decode=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkDoFrame@4'),[LegacyBinkTest+Decode])
 $next=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkNextFrame@4'),[LegacyBinkTest+One])
 $close=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkClose@4'),[LegacyBinkTest+One])
 $movie=$open.Invoke((Join-Path $PSScriptRoot '01_INT_003-strong.bik'),0)
 if($movie -eq [IntPtr]::Zero){throw 'Original game codec rejected remixed movie.'}
 $status=@()
 for($i=0;$i -lt 8;$i++){$status+=@($decode.Invoke($movie));$next.Invoke($movie)}
 @{original_game_codec_verified=$true;opened_remixed_bik=$true;decoded_frames=8;decode_status=$status;scope='Standalone decoder compatibility; in-game audio output still requires listening.'} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'legacy-codec-test.json') -Encoding UTF8
 Write-Output 'Original game Bink DLL opened and decoded 8 frames of the remixed BIK.'
} finally {if($movie -ne [IntPtr]::Zero){$close.Invoke($movie)};$null=[LegacyBinkTest]::FreeLibrary($dll)}
