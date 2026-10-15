param([string]$CaseName='audit_v565_current_cpu_pair_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 & $python 'tools/test_cpu_recovery_v545.py' 2>&1 | Out-File "$out/tests.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual current baseline/corruption tests failed'}
 $script=@'
import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
import verify_cpu_recovery_v545_v2 as check
accepted=[('kano',604),('cage',605),('kano',605),('liu_kang',605)]
unaccepted=[('sonya',602),('sub_zero',605),('liu_kang',604),('sonya',604)]
def case(player,boot):
    folder=f'audit_v564_cpu_recovery_{player}_boot{boot}'
    result=check.verify(check.ROOT/folder,player)
    return dict(folder=folder,verification=result)
cases=[case(*args) for args in accepted]
retained=[case(*args) for args in unaccepted]
passed=all(c['verification']['passed'] for c in cases) and all(not c['verification']['passed'] for c in retained)
dependencies=sorted({str(Path(m.__file__).resolve()) for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent==check.ROOT/'tools' and Path(m.__file__).suffix=='.py'})
print(json.dumps(dict(passed=passed,accepted=cases,unaccepted=retained,dependencies=dependencies),indent=2))
raise SystemExit(0 if passed else 1)
'@
 & $python -c $script | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Accepted/rejected runtime evidence disagrees with declared scope'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 $inputs=@{}
 $currentFolders=@($proof.accepted.folder)+@($proof.unaccepted.folder)
 foreach($name in $currentFolders) {
  $folder=Join-Path $root $name
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Capture input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
 }
 $retainedFolders=@('audit_v560_cpu_recovery_kano_boot604','audit_v560_cpu_recovery_cage_boot605','audit_v562_cpu_recovery_kano_boot604','audit_v562_cpu_recovery_cage_boot605','audit_v563_pair_checker_boundary')
 foreach($name in @($currentFolders)+$retainedFolders){
  foreach($file in Get-ChildItem -LiteralPath (Join-Path $root $name) -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $tracked=@($PSCommandPath,"$root/tools/test_cpu_recovery_v545.py","$root/tools/verify_cpu_recovery_v545.py","$root/tools/run_cpu_recovery_probe_v2.ps1","$root/tools/run_cpu_recovery_probe_v3.ps1","$root/tools/run_cpu_recovery_probe_v4.ps1","$root/mk2ks_cpu_recovery_probe.lua","$root/mk2ks_cpu_recovery_probe_v2.lua","$root/mk2ks_cpu_recovery_probe_v3.lua","$root/mk2/mk2-maincpu.bin")+@($proof.dependencies)
 foreach($file in $tracked){
  $inputs[$file]=(Get-FileHash -LiteralPath $file).Hash
  if([IO.Path]::GetExtension($file) -in '.py','.ps1','.lua'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}
 }
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;allScoutsAccepted=$false;candidate='diagnostic_v545_native_roll_edge_clearance';tests=63;checkedInputs=$inputs.Count;acceptedCases=$proof.accepted;unacceptedCases=$proof.unaccepted;
  scope='Four current natural P1-CPU/P2-human complete paired grabs: Kano choke versus Kano; Sonya leg versus Cage, Kano and Liu Kang. Every authored held pose/grip, original native damage, release, victim flight and individual owning ready cleanup is checked. Native post-cleanup Main action stores/registers/live opcodes are replayed against every paired callback. Sonya-to-Cage ordinary follow-up proves ordered NEW native setup, action publication and later cleanup; Kano same-state setup retains strict original provenance. Not all victims, CPU slots/moves/outcomes, jump/special follow-ups, KO, bitmap/audio, campaign or release acceptance.';
  openScouts=@('Sonya-to-Sonya: square-wave follow-up state chain is not accepted by this ordinary-follow-up checker','Sonya-to-Sub-Zero: native jump follow-up is not accepted by this ordinary-follow-up checker','Kano-to-Liu-Kang: blade follow-up is not accepted by this ordinary-follow-up checker','Kano-to-Sonya: no choke was observed; natural CPU choices were not forced');
  retainedBoundary='audit_v563_pair_checker_boundary';gameplayChanged=$false;productionPromoted=$false;inputHashes=$inputs} | ConvertTo-Json -Depth 12 | Out-File "$out/result.json" -Encoding utf8
 'Four actual current full paired CPU cases verified; four other natural scouts retained unaccepted. Full port acceptance remains false.'
} finally {Pop-Location}
