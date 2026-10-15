param([string]$CaseName='audit_v573_sonya_display_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 $testCount=0
 foreach($suite in @('test_cpu_recovery_v545','test_cpu_followup_v545','test_sonya_display_transition_v545')){
  & $python "tools/$suite.py" 2>&1 | Out-File "$out/$suite.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual baseline/corruption suite failed: $suite"}
  $log=Get-Content "$out/$suite.log" -Raw
  if($log -notmatch 'Ran ([0-9]+) tests'){throw 'Actual test count missing'}
  $testCount+=[int]$Matches[1]
 }
 & $python tools/verify_sonya_display_transition_v545.py --output "$out/verification.json" | Out-File "$out/verification.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual display verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 $inputs=@{}
 $prior=Get-Content 'audit_v569_current_cpu_followup_checked_inputs/input_hashes.json' -Raw | ConvertFrom-Json
 foreach($entry in $prior.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Prior checked input changed: $($entry.Name)"}
  $inputs[$entry.Name]=$entry.Value
 }
 foreach($folder in @('audit_v570_sonya_native_display_provenance','audit_v571_sonya_native_display_transition')){
  $before=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $before.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Fresh display input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
 }
 foreach($folder in @('audit_v569_current_cpu_followup_checked_inputs','audit_v570_sonya_native_display_provenance','audit_v571_sonya_native_display_transition','audit_v572_sonya_display_checker_boundary')){
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $deps=@'
import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
import verify_sonya_display_transition_v545 as v
print(json.dumps(dict(paths=sorted({str(Path(m.__file__).resolve())for m in list(sys.modules.values())if getattr(m,'__file__',None)and Path(m.__file__).resolve().parent==v.ROOT/'tools'and Path(m.__file__).suffix=='.py'}),numpy=v.np.__version__,pillow=v.Image.__version__,python=sys.version),indent=2))
'@
 & $python -c $deps | Out-File "$out/dependencies.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Dependency closure failed'}
 $closure=Get-Content "$out/dependencies.json" -Raw | ConvertFrom-Json
 foreach($file in @($closure.paths)+@($PSCommandPath,"$root/tools/test_sonya_display_transition_v545.py",$python,"$root/mk3/mk3-maincpu.bin")){
  $inputs[$file]=(Get-FileHash -LiteralPath $file).Hash
  if([IO.Path]::GetExtension($file) -in '.py','.ps1'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}
 }
 foreach($file in Get-ChildItem -LiteralPath $out -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 foreach($entry in $inputs.GetEnumerator()){if((Get-FileHash -LiteralPath $entry.Key).Hash -ne $entry.Value){throw "Checked evidence changed: $($entry.Key)"}}
 $inputs | ConvertTo-Json | Out-File "$out/input_hashes.json" -Encoding utf8
 [ordered]@{
  passed=$proof.passed;fullPortAcceptance=$false;candidate='diagnostic_v545_native_roll_edge_clearance';tests=$testCount;checkedInputs=$inputs.Count;
  displayActorFields=$proof.actor_fields;consecutiveRenderedFrames=$proof.frame_done_images;exactVisibleBodyPixels=$proof.exact_visible_body_pixels;
  correction='Earlier visual diagnosis reversed mirror-match identities: green normal palette is P1 CPU, white alternate palette is P2 human. No inverted standing-block defect is established by this capture.';
  nativeTransition='Bicycle first native ready1961; last cycling cache1962; ordinary upright cache1963 and double-buffered rendered field1964; original new high-punch setup1970.';
  proof=$proof;
  gameBuildLauncherZipChanges='none';
  remaining='Five unresolved crouching roll contacts; wider CPU/victim/slot/contact/interrupt/KO coverage; all-arena floor shadows; full towers/continues/bosses/finishers/endings/audio; final matched production CMD and ZIP';
  scope='Fresh unassisted Sonya mirror leg/bicycle-miss/ordinary-control display transition, plus unchanged bounded v569 contracts; not full port'
 } | ConvertTo-Json -Depth 14 | Out-File "$out/result.json" -Encoding utf8
 Get-Content "$out/result.json" -Raw | ConvertFrom-Json | Select-Object passed,fullPortAcceptance,tests,checkedInputs,displayActorFields,consecutiveRenderedFrames,exactVisibleBodyPixels | ConvertTo-Json
}finally{Pop-Location}
