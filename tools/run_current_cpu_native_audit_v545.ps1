param([string]$CaseName='audit_v556_current_cpu_native_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 foreach($suite in @('test_natural_cpu_moves_v545','test_cpu_ring_v545')) {
  & $python "tools/$suite.py" 2>&1 | Out-File "$out/$suite.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual baseline/corruption suite failed: $suite"}
 }
 $script=@'
import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
import verify_natural_cpu_moves_v545 as natural
import verify_cpu_projectile_followup_v545 as shot
folders=['audit_v554_cpu_kano_boot605','audit_v554_cpu_kano_boot606','audit_v554_cpu_sonya_boot601','audit_v554_cpu_sonya_boot604']
cases=[natural.verify(natural.ROOT/f) for f in folders]
ring=[('audit_v555_cpu_ring_block','block','v2'),('audit_v555_cpu_ring_duck','duck_miss','v3')]
cases += [shot.verify(shot.ROOT/f,18,scenario,version) for f,scenario,version in ring]
union=set().union(*(set(c.get('observed_moves',[])) for c in cases))|{'ring'}
passed=all(c.get('passed') for c in cases) and union==set(natural.SPECS)
dependencies=sorted({str(Path(m.__file__).resolve()) for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent==natural.ROOT/'tools' and Path(m.__file__).suffix=='.py'})
print(json.dumps(dict(passed=passed,cases=cases,captureFolders=folders+[f for f,_,_ in ring],observedMoves=sorted(union),dependencies=dependencies),indent=2))
raise SystemExit(0 if passed else 1)
'@
 & $python -c $script | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Current native CPU verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 $inputs=@{}
 foreach($name in $proof.captureFolders) {
  $folder=Join-Path $root $name
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Capture input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $tracked=@($PSCommandPath,"$root/tools/test_natural_cpu_moves_v545.py","$root/tools/test_cpu_ring_v545.py","$root/mk2/mk2-maincpu.bin")+@($proof.dependencies)
 foreach($file in $tracked){
  $inputs[$file]=(Get-FileHash -LiteralPath $file).Hash
  if([IO.Path]::GetExtension($file) -in '.py','.ps1'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}
 }
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;candidate='diagnostic_v545_native_roll_edge_clearance';tests=47;checkedInputs=$inputs.Count;cases=$proof.cases;observedMoves=$proof.observedMoves;
  scope='All eight natural CPU dispatches observed in actual current-build runs. Four P2 CPU entry-to-ready cases retain original projectile child lifetime checks. One Kano knife release cancellation proves five native hurt-list poses and ready after damage, with already-spawned child completing independently. Two P1 Sonya CPU ring cases prove block impact/chip and held duck miss plus cleanup and AI walking. Not all contact outcomes, victims, slots, cancels, rectangles, rendered art, audio, full towers or release acceptance.';
  retainedFailures=@('audit_v533_current_cpu_diagnostic','audit_v537_ring_mutator_preentry_failure','audit_v538_cpu_cancel_checker_boundary_failure');
  gameplayChanged=$false;productionPromoted=$false;inputHashes=$inputs} | ConvertTo-Json -Depth 10 | Out-File "$out/result.json" -Encoding utf8
 'Current bounded natural CPU dispatch, ring block/duck and native knife cancellation verified; full-port acceptance remains false.'
} finally {Pop-Location}
