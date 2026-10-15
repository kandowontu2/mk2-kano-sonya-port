$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if($taskRoot -ne 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'){throw 'Unexpected workspace'}
$taskPython='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
$taskChecker=Join-Path $taskRoot 'tools/verify_native_arena_geometry_v1583.py'
$taskProtected=@($taskChecker,(Join-Path $taskRoot 'tools/verify_native_campaign_palette_v1580.py'),
 (Join-Path $taskRoot 'tools/verify_native_floor_campaign_v1573.py'),$PSCommandPath)
$taskHashes=@{};foreach($taskFile in $taskProtected){$taskHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash}
$taskCases=@(
 [pscustomobject]@{folder='audit_v1564_native_arenas_kano_p1';out='audit_v1583_native_arenas_kano_checked'},
 [pscustomobject]@{folder='audit_v1576_native_arenas_kano_p2';out='audit_v1583_native_arenas_kano_p2_checked'},
 [pscustomobject]@{folder='audit_v1576_native_arenas_sonya_p1';out='audit_v1583_native_arenas_sonya_p1_checked'}
)
foreach($taskCase in $taskCases){
 $taskResult=Get-Content -LiteralPath (Join-Path $taskRoot ($taskCase.folder+'/result.json')) -Raw | ConvertFrom-Json
 if($taskResult.exit_code -ne 0 -or $taskResult.candidate -ne 'diagnostic_v1517_active_launch_timer' -or $taskResult.assistance -ne 'none'){throw 'Actual terminal capture required'}
 if(Test-Path -LiteralPath (Join-Path $taskRoot ($taskCase.out+'/report.json'))){throw 'Never overwrite evidence'}
}
Push-Location $taskRoot
try{
 foreach($taskCase in $taskCases){
  foreach($taskFile in $taskHashes.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskHashes[$taskFile]){throw 'Checker source changed'}}
  "Checking existing immutable capture $($taskCase.folder) sequentially"
  & $taskPython $taskChecker $taskCase.folder --output ($taskCase.out+'/report.json')
  if($LASTEXITCODE -ne 0){throw "Native arena check failed: $($taskCase.folder); preserve report and investigate"}
  $taskProof=Get-Content -LiteralPath (Join-Path $taskRoot ($taskCase.out+'/report.json')) -Raw | ConvertFrom-Json
  if(-not $taskProof.passed -or -not $taskProof.allNineRegularArenasSampled -or $taskProof.fullPortAcceptance){throw 'Exact bounded all-nine arena proof required; not whole-port acceptance'}
  foreach($taskFile in $taskHashes.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskHashes[$taskFile]){throw 'Checker source changed during execution'}}
  "Accepted $($taskCase.folder): $($taskProof.exactScanouts) exact native frames; all move phases and full port remain open"
 }
 'All three remaining saved arena captures checked; no game or capture changed'
}finally{Pop-Location}
