param([string]$CaseName='audit_v576_roll_turn_checked_inputs')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try{
 $testCount=0
 foreach($suite in @('test_cpu_recovery_v545','test_cpu_followup_v545','test_sonya_display_transition_v545','test_roll_turn_contacts_v545')){
  & $python "tools/$suite.py" 2>&1 | Out-File "$out/$suite.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual suite failed: $suite"}
  $log=Get-Content "$out/$suite.log" -Raw
  if($log -notmatch 'Ran ([0-9]+) tests'){throw 'Actual test count missing'}
  $testCount+=[int]$Matches[1]
 }
 & $python tools/inspect_roll_turn_contacts_v545.py | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual roll-turn diagnostic verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 $inputs=@{}
 $prior=Get-Content 'audit_v573_sonya_display_checked_inputs/input_hashes.json' -Raw | ConvertFrom-Json
 foreach($entry in $prior.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Prior checked input changed: $($entry.Name)"}
  $inputs[$entry.Name]=$entry.Value
 }
 foreach($entry in $proof.inputHashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Fresh diagnostic evidence changed: $($entry.Name)"}
  $inputs[$entry.Name]=$entry.Value
 }
 foreach($folder in @('audit_v573_sonya_display_checked_inputs','audit_v575_roll_pose_checker_boundary')){
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $script=@'
import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
import inspect_roll_turn_contacts_v545 as v
print(json.dumps(sorted({str(Path(m.__file__).resolve())for m in list(sys.modules.values())if getattr(m,'__file__',None)and Path(m.__file__).resolve().parent==v.ROOT/'tools'and Path(m.__file__).suffix=='.py'})))
'@
 & $python -c $script | Out-File "$out/dependencies.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual dependency closure failed'}
 $closure=Get-Content "$out/dependencies.json" -Raw | ConvertFrom-Json
 foreach($file in @($closure)+@($PSCommandPath,"$root/tools/test_roll_turn_contacts_v545.py",$python)){
  $inputs[$file]=(Get-FileHash -LiteralPath $file).Hash
  if([IO.Path]::GetExtension($file)-in '.py','.ps1'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}
 }
 foreach($file in Get-ChildItem -LiteralPath $out -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 foreach($entry in $inputs.GetEnumerator()){if((Get-FileHash -LiteralPath $entry.Key).Hash -ne $entry.Value){throw "Checked evidence changed: $($entry.Key)"}}
 $inputs | ConvertTo-Json | Out-File "$out/input_hashes.json" -Encoding utf8
 [ordered]@{
  diagnosticVerified=$proof.diagnosticVerified;fullPortAcceptance=$false;contactFidelityAccepted=$false;planeCorrectionClaim=$false;
  candidate='diagnostic_v545_native_roll_edge_clearance';tests=$testCount;checkedInputs=$inputs.Count;
  freshCases=$proof.cases.Count;pairedCallbackRecords=$proof.pairedCallbackRecords;
  comparisons=($proof.cases|Measure-Object -Property comparisons -Sum).Sum;nextFrameDoneImages=($proof.cases|Measure-Object -Property snapshots -Sum).Sum;
  observedNativeContacts=5;observedNativeMisses=1;cases=$proof.cases;
  gameBuildLauncherZipChanges='none';
  remaining='Contact-fitting decision for the five turns, wider CPU/victim/slot/contact coverage, all-arena shadows, complete campaign/continues/bosses/finishers/endings/audio, final matched production launcher and ZIP';
  scope=$proof.scope
 }|ConvertTo-Json -Depth 12|Out-File "$out/result.json" -Encoding utf8
 Get-Content "$out/result.json" -Raw|ConvertFrom-Json|Select-Object diagnosticVerified,fullPortAcceptance,contactFidelityAccepted,tests,checkedInputs,freshCases,pairedCallbackRecords,comparisons,nextFrameDoneImages|ConvertTo-Json
}finally{Pop-Location}
