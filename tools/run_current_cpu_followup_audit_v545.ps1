param([string]$CaseName='audit_v569_current_cpu_followup_checked_inputs')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 $testCount=0
 foreach($suite in @('test_cpu_recovery_v545','test_cpu_followup_v545')){
  & $python "tools/$suite.py" 2>&1 | Out-File "$out/$suite.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual baseline/corruption suite failed: $suite"}
  $text=Get-Content "$out/$suite.log" -Raw
  if($text -notmatch 'Ran ([0-9]+) tests'){throw 'Actual test accounting missing'}
  $testCount+=[int]$Matches[1]
 }
 $script=@'
import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
import verify_cpu_recovery_v545_v2 as paired
import verify_cpu_followup_v545 as follow
old=[('kano',604),('cage',605),('kano',605),('liu_kang',605)]
new=[('sonya',602,'bicycle'),('sub_zero',605,'square'),('liu_kang',604,'blade')]
cases=[]
for player,boot in old:
    name=f'audit_v564_cpu_recovery_{player}_boot{boot}'
    cases.append(dict(folder=name,verification=paired.verify(paired.ROOT/name,player)))
for player,boot,move in new:
    name=f'audit_v568_cpu_followup_{player}_boot{boot}'
    cases.append(dict(folder=name,verification=follow.verify(follow.ROOT/name,player,move)))
passed=all(c['verification']['passed'] for c in cases)
dependencies=sorted({str(Path(m.__file__).resolve()) for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent==follow.ROOT/'tools' and Path(m.__file__).suffix=='.py'})
print(json.dumps(dict(passed=passed,cases=cases,dependencies=dependencies),indent=2))
raise SystemExit(0 if passed else 1)
'@
 & $python -c $script | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual full-pair/follow-up verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 $inputs=@{}
 foreach($name in @($proof.cases.folder)){
  $folder=Join-Path $root $name
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Capture input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 foreach($file in Get-ChildItem -LiteralPath "$root/audit_v565_current_cpu_pair_checked_inputs" -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 $prior=Get-Content "$root/audit_v565_current_cpu_pair_checked_inputs/input_hashes.json" -Raw | ConvertFrom-Json
 foreach($entry in $prior.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Prior checked input changed: $($entry.Name)"}
  $inputs[$entry.Name]=$entry.Value
 }
 $tracked=@($PSCommandPath,"$root/tools/test_cpu_followup_v545.py","$root/tools/test_cpu_recovery_v545.py","$root/tools/run_cpu_recovery_probe_v5.ps1","$root/tools/run_cpu_recovery_probe_v6.ps1","$root/mk2ks_cpu_recovery_probe_v4.lua","$root/mk2ks_cpu_recovery_probe_v5.lua","$root/mk2/mk2-maincpu.bin")+@($proof.dependencies)
 foreach($file in $tracked){
  $inputs[$file]=(Get-FileHash -LiteralPath $file).Hash
  if([IO.Path]::GetExtension($file) -in '.py','.ps1','.lua'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}
 }
 & "$root/../mame0289/unidasm.exe" "$root/mk2/mk2-maincpu.bin" -arch tms34010 -basepc 0xff83df00 -skip 31712 -count 160 | Out-File "$out/native_stage_ground_disassembly.txt" -Encoding utf8
 $inputs["$root/../mame0289/unidasm.exe"]=(Get-FileHash -LiteralPath "$root/../mame0289/unidasm.exe").Hash
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;candidate='diagnostic_v545_native_roll_edge_clearance';tests=$testCount;checkedInputs=$inputs.Count;cases=$proof.cases;
  scope='Seven actual natural P1-CPU/P2-human complete grabs, including three fresh full owned post-grab bicycle, square-wave and blade MISS continuations. Complete paired poses/damage/victim flight/individual ready cleanup remain required. Follow-ups require independent real special entries, continuous original state stores with actual registers/live opcodes, every authored startup/active/recovery body field, native fixed-point movement, first floor crossing/landing, original cleanup and first owning regain. Every continuation health store is checked. Not all follow-up hits/blocks/cancels, victims, opposite CPU slot, pixels/shadows/audio, campaigns or final release.';
  correctedPriorLabels=@('v565 Sonya-to-Sonya was labeled square; actual FFF9A400 entry proves bicycle','v565 Sonya-to-Sub-Zero was labeled native jump; actual FFFFCA00 entry proves square-wave');
  remainingNoGrabScout='audit_v564_cpu_recovery_sonya_boot604: no choke occurred; native CPU choice was never forced';
  gameplayChanged=$false;productionPromoted=$false;inputHashes=$inputs} | ConvertTo-Json -Depth 12 | Out-File "$out/result.json" -Encoding utf8
 'Seven current natural full-pair cases and three whole owned miss follow-ups verified; full port acceptance remains false.'
} finally {Pop-Location}
