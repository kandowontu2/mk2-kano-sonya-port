param([string]$CaseName='audit_v605_native_pit_checked_inputs')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Never overwrite verified evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 $tests=0
 foreach($suite in @('test_native_pit_assets_v602','test_native_pit_scene_v602')){
  & $python -m unittest discover -s tools -p "$suite.py" -v 2>&1 | Out-File "$out/$suite.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual baseline/corruption suite failed: $suite"}
  $text=Get-Content "$out/$suite.log" -Raw
  if($text -notmatch 'Ran (\d+) tests'){throw 'Missing executed test count'}
  $tests+=[int]$Matches[1]
 }
 $cases=@();$inputs=@{}
 foreach($fighter in @('kano','sonya')){
  $folder="$root/audit_v603_native_pit_${fighter}_p1"
  $reference=if($fighter -eq 'kano'){"$root/audit_v592_pit_actual_lookup_kano_p1"}else{"$root/audit_v599_native_pit_sonya_p1_uppercut"}
  & $python tools/verify_native_pit_scene_v602_v3.py $folder $fighter $reference | Out-File "$out/$fighter.json" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual native Pit verification failed: $fighter"}
  $cases+=Get-Content "$out/$fighter.json" -Raw | ConvertFrom-Json
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Capture input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
  $inputs["$reference/run.log"]=(Get-FileHash -LiteralPath "$reference/run.log").Hash
 }
 $tracked=@($PSCommandPath,"$root/tools/build_native_pit_fall_v2.py","$root/tools/verify_native_pit_assets_v602.py",
  "$root/tools/test_native_pit_assets_v602.py","$root/tools/verify_native_pit_scene_v602_v3.py","$root/tools/test_native_pit_scene_v602.py",
  "$root/mk2/mk2-maincpu.bin","$root/mk3/mk3-maincpu.bin",
  "$root/diagnostic_v601_native_pit_position_assets/asset-report.json",
  "$root/diagnostic_v601_native_pit_position_assets/native-palette-preview.png")
 $tracked+=@(Get-ChildItem -LiteralPath "$root/diagnostic_v595_pit_sprite_drafts" -File | Select-Object -ExpandProperty FullName)
 foreach($file in $tracked){$inputs[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.py','.ps1'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;candidate='diagnostic_v602_native_pit_position';tests=$tests;
  checkedInputs=$inputs.Count;cases=$cases;retainedCheckerBoundary='audit_v604_pit_checker_boundary';
  scope='Two actual P1 victims: both native Pit lookups, own loop/impact, centered origin, bounded component copies, native completion and genuine paid continue into sustained own-ID fight. Not P2/alternate costumes, complete visual/audio or full tower/port/release acceptance.';
  inputHashes=$inputs} | ConvertTo-Json -Depth 9 | Out-File "$out/result.json" -Encoding utf8
 "$tests native asset/actual-scene baseline and corruption tests passed; full acceptance remains false."
} finally {Pop-Location}
