param([string]$CaseName='audit_v631_floor_pass_checked_inputs')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Never overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 & $python -m unittest discover -s tools -p test_native_floor_pass_v602.py -v 2>&1 | Out-File "$out/tests.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual drawing-pass baseline/corruption tests failed'}
 $testText=Get-Content "$out/tests.log" -Raw
 if($testText -notmatch 'Ran (\d+) tests'){throw 'Missing executed test count'}
 $tests=[int]$Matches[1];$cases=@();$inputs=@{}
 foreach($fighter in @('kano','sonya')){
  & $python tools/verify_native_floor_pass_v602.py "audit_v630_floor_pass_${fighter}_p2" $fighter "audit_v620_floor_${fighter}_p2" | Out-File "$out/$fighter.json" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual native drawing pass failed: $fighter"}
  $cases+=Get-Content "$out/$fighter.json" -Raw | ConvertFrom-Json
 }
 foreach($name in @('audit_v630_floor_pass_kano_p2','audit_v630_floor_pass_sonya_p2',
                    'audit_v620_floor_kano_p2','audit_v620_floor_sonya_p2')){
  $folder=Join-Path $root $name
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Changed actual capture input: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $tracked=@($PSCommandPath,"$root/tools/verify_native_floor_pass_v602.py","$root/tools/test_native_floor_pass_v602.py",
  "$root/tools/inspect_natural_arena_floor_v602_v3.py","$root/tools/inspect_natural_arena_floor_v602.py",
  "$root/tools/verify_native_floor_display_v602.py","$root/tools/verify_native_pit_scene_v602_v4.py",
  "$root/tools/verify_native_pit_mirrors_v602.py","$root/tools/verify_native_pit_assets_v602.py",
  "$root/mk2ks_natural_campaign_probe_v20.lua","$root/tools/run_natural_campaign_probe_v20.ps1",
  "$root/mame-mkp/src/mame/midway/midtunit_v.cpp","$root/mame-mkp/src/frontend/mame/luaengine.cpp",
  "$root/mame-mkp/src/emu/emumem_het.cpp","$root/mame-mkp/src/devices/cpu/tms34010/tms34010.cpp",
  "$root/audit_v629_floor_erasure_boundary/NOTE.txt",
  "$root/audit_v629_floor_erasure_boundary/input_sources/inspect_natural_arena_floor_v602_v2.py",
  "$root/audit_v629_floor_erasure_boundary/input_sources/test_native_floor_pass_v602_first.py")
 foreach($file in $tracked){$inputs[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.py','.ps1','.lua'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;floorAcceptance=$false;candidate='diagnostic_v602_native_pit_position';
  tests=$tests;checkedInputs=$inputs.Count;cases=$cases;
  retainedCheckerBoundary='audit_v629_floor_erasure_boundary';
  scope='Thirty actual P2 Dead Pool samples: 7,864,320 indexed VRAM words and 3,048,000 displayed pixels exactly reconstructed from actual PRE-draw-pass state, including native foreground and both imported bodies/floor silhouettes. Earlier erasure, desired native-style geometry/grounding, all arenas/P1 and whole-game acceptance remain unproven.';
  inputHashes=$inputs} | ConvertTo-Json -Depth 12 | Out-File "$out/result.json" -Encoding utf8
 "$tests actual native drawing-pass baseline/corruption tests passed; $($inputs.Count) inputs rechecked. Desired floor and whole-port acceptance remain false."
} finally {Pop-Location}
