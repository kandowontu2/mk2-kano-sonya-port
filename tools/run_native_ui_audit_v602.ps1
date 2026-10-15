param([string]$CaseName='audit_v607_native_ui_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try{
 & $python tools/test_native_ui_flow_v602.py 2>&1 | Out-File "$out/counterexamples.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Current UI contract tests failed'}
 $inputs=@{};$cases=@()
 foreach($fighter in @('kano','sonya')){foreach($side in @(1,2)){
  $folder=Join-Path $root "audit_v606_ui_${fighter}_p${side}"
  & $python -c "import json,sys; sys.path.insert(0,'tools'); import verify_native_ui_flow_v602 as v; print(json.dumps(v.verify(sys.argv[1],sys.argv[2],int(sys.argv[3])),indent=2))" $folder $fighter $side | Out-File "$out/${fighter}_p${side}.json" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Native UI verification failed: $fighter P$side"}
  $proof=Get-Content "$out/${fighter}_p${side}.json" -Raw | ConvertFrom-Json
  if(-not $proof.passed -or $proof.whole_character_integration_complete){throw 'UI scope invariant changed'}
  $cases+=$proof
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Capture input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in @(Get-ChildItem -LiteralPath $folder -File)+@(Get-ChildItem -LiteralPath "$folder/snap" -Recurse -File)){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }}
 $tracked=@($PSCommandPath,"$root/tools/verify_native_ui_flow_v602.py","$root/tools/test_native_ui_flow_v602.py", "$root/tools/verify_native_candidate_v602.py", "$root/tools/verify_cpu_air_runtime.py", "$root/tools/verify_cpu_air_gate.py", "$root/tools/verify_p2_campaign.py", "$root/mk2/mk2-maincpu.bin")
 foreach($file in $tracked){$inputs[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.py','.ps1'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;candidate='diagnostic_v602_native_pit_position';cases=$cases;tests=46;checkedInputs=$inputs.Count;
  scope='Current Kano/Sonya in both slots: actual selection navigation, four-pixel blinking border/player number, unshifted animated backdrop, full portrait/pose cleanup before ladder, both ladder icons, first match true identity and name shadows. Not full tower/continue/floor/CPU/moves/finishers/audio/release acceptance.';
  retainedFailure='audit_v528_ui_checker_gap preserves the initially insufficient one-field navigation checker; new checker requires every settled navigation field';
  inputHashes=$inputs} | ConvertTo-Json -Depth 8 | Out-File "$out/result.json" -Encoding utf8
 'Four current native UI/ladder/first-match cases and 46 regression checks verified.'
}finally{Pop-Location}
