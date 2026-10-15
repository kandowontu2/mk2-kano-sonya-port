param([string]$CaseName='audit_v552_roll_integration_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 foreach($suite in @('test_roll_edge_v545','test_full_human_matrix_v545','test_native_ui_flow_v545')) {
  & $python "tools/$suite.py" 2>&1 | Out-File "$out/$suite.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Regression suite failed: $suite"}
 }
 $script=@'
import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
import verify_roll_edge_v545 as edge
import verify_full_human_matrix_v545 as human
import verify_native_ui_flow_v545 as ui
inputs={}
delta=edge.source_delta(inputs)
target=edge.verify_targets(inputs)
matrix=human.verify()
inputs.update(matrix.pop('inputHashes'))
selection=[ui.verify(ui.ROOT/f'audit_v549_ui_{fighter}_p{side}',fighter,side) for fighter in ('kano','sonya') for side in (1,2)]
passed=target['targetedCorrectionVerified'] and matrix['boundedMatrixPassed'] and all(c['passed'] for c in selection)
captures=sorted({c['capture'] for c in target['cases']+matrix['cases']}|{f'audit_v549_ui_{fighter}_p{side}' for fighter in ('kano','sonya') for side in (1,2)})
dependencies=sorted({str(Path(m.__file__).resolve()) for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent==edge.ROOT/'tools' and Path(m.__file__).suffix=='.py'})
print(json.dumps(dict(passed=passed,fullPortAcceptance=False,sourceDelta=delta,rollTargets=target,humanMatrix=matrix,selection=selection,captureFolders=captures,dependencies=dependencies,inputHashes=inputs),indent=2))
raise SystemExit(0 if passed else 1)
'@
 & $python -c $script | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Integration verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 $inputs=@{}
 foreach($entry in $proof.inputHashes.PSObject.Properties){$inputs[$entry.Name]=$entry.Value}
 foreach($name in $proof.captureFolders){
  $folder=Join-Path $root $name
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Capture input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $tracked=@($PSCommandPath,"$root/tools/test_roll_edge_v545.py","$root/tools/test_full_human_matrix_v545.py","$root/tools/test_native_ui_flow_v545.py","$root/mame-mkp/src/devices/cpu/tms34010/34010ops.hxx")+@($proof.dependencies)
 foreach($file in $tracked){$inputs[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.py','.ps1','.hxx'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;candidate='diagnostic_v545_native_roll_edge_clearance';tests=67;checkedInputs=$inputs.Count;
  sourceDelta=$proof.sourceDelta;humanMatrix=$proof.humanMatrix;selection=$proof.selection;rollTargets=$proof.rollTargets;
  scope='Current one-pixel roll attack-plane fit: Liu duck misses both slots; 24/5 hit/block damage and native recoil retained. Fresh 52-case human/Sub-Zero matrix and four complete rendered CSS/ladder/first-match cases pass. Across 28 ducked-roster captures, 23 misses pass and five native contacts remain unresolved, not accepted misses. Not all crouch phases, AI contact/choreography, interruption/KO points, arenas/floor shadows, full tower/continue/boss/finishers/endings/audio or release acceptance.';
  retainedCheckerFailure='audit_v551_roll_checker_record_consistency_gap';productionPromoted=$false;inputHashes=$inputs} | ConvertTo-Json -Depth 12 | Out-File "$out/result.json" -Encoding utf8
 'Targeted roll correction, 52 current human cases and four native UI flows verified; wider scope remains open.'
} finally {Pop-Location}
