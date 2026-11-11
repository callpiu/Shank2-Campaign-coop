$ErrorActionPreference='Stop'
# Load the already-tested FFI definitions and verify the original codec hash.
. (Join-Path $PSScriptRoot 'test_legacy_bink.ps1')
$dll=[LegacyBinkTest]::LoadLibraryW($codec)
if($dll -eq [IntPtr]::Zero){throw 'Original codec reload failed.'}
$rows=@()
try {
 $open=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkOpen@8'),[LegacyBinkTest+Open])
 $decode=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkDoFrame@4'),[LegacyBinkTest+Decode])
 $next=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkNextFrame@4'),[LegacyBinkTest+One])
 $close=[LegacyBinkTest]::Bind([LegacyBinkTest]::GetProcAddress($dll,'_BinkClose@4'),[LegacyBinkTest+One])
 foreach($file in Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'enhanced') -Filter '*.bik' -File) {
  $movie=$open.Invoke($file.FullName,0)
  if($movie -eq [IntPtr]::Zero){throw ('Original codec rejected '+$file.Name)}
  try {
   $status=@();for($i=0;$i -lt 8;$i++) {$status+=@($decode.Invoke($movie));$next.Invoke($movie)}
   if(@($status | Where-Object {$_ -ne 0}).Count){throw ('Decode error in '+$file.Name)}
   $rows+=@{file=$file.Name;frames_decoded=8;all_status_zero=$true}
  } finally {$close.Invoke($movie)}
 }
 if($rows.Count -ne 27){throw 'Expected 27 enhanced movies.'}
 @{movie_count=$rows.Count;original_game_codec=$true;results=$rows;scope='Native header/video decode compatibility; per-movie listening not claimed.'} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'legacy-batch-tests.json') -Encoding UTF8
 Write-Output ('Original game codec opened and decoded '+$rows.Count+' enhanced movies.')
} finally {$null=[LegacyBinkTest]::FreeLibrary($dll)}
