param([string]$BufferPath)
$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4) {throw 'Use 32-bit Windows PowerShell.'}
Add-Type @'
using System; using System.Runtime.InteropServices;
public static class EnterKeyTest {
 [DllImport("kernel32.dll",SetLastError=true)] public static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint kind,uint protect);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] public delegate uint Step(int down,int paused,int equipment);
 public static Step Bind(IntPtr p) {return (Step)Marshal.GetDelegateForFunctionPointer(p,typeof(Step));}
}
'@
$mem=[EnterKeyTest]::VirtualAlloc([IntPtr]0x20000000,[UIntPtr]::new([uint32]8192),0x3000,0x40)
if($mem.ToInt32() -ne 0x20000000) {throw 'Allocation failed.'}
$bytes=[IO.File]::ReadAllBytes($BufferPath)
[Runtime.InteropServices.Marshal]::Copy($bytes,0,$mem,$bytes.Length)
$step=[EnterKeyTest]::Bind([IntPtr]0x20000d00)
$cases=@(
 @{down=32768;paused=0;expected=16},
 @{down=32768;paused=1;expected=16},
 @{down=32768;paused=1;expected=16},
 @{down=0;paused=1;expected=0},
 @{down=32768;paused=1;expected=4096},
 @{down=32768;paused=0;expected=0},
 @{down=32768;paused=0;expected=0},
 @{down=0;paused=0;expected=0},
 @{down=32768;paused=0;expected=16},
 @{down=0;paused=0;equipment=1;expected=0},
 @{down=32768;paused=0;equipment=1;expected=4096},
 @{down=32768;paused=1;equipment=0;expected=0},
 @{down=0;paused=1;equipment=0;expected=0},
 @{down=32768;paused=1;equipment=0;expected=4096},
 @{down=0;paused=0;equipment=0;expected=0},
 @{down=32768;paused=0;equipment=0;expected=16}
)
foreach($case in $cases) {
 $actual=$step.Invoke($case.down,$case.paused,[int]$case.equipment)
 if($actual -ne $case.expected) {throw ('Unexpected key state: '+$actual+' expected '+$case.expected)}
}
Write-Output ('Passed '+$cases.Count+' native Enter pause/confirm/held-key transitions.')
