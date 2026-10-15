param([string]$CaseName='audit_v623_floor_display_checked_inputs')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Never overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 & $python -m unittest discover -s tools -p test_native_floor_display_v602.py -v 2>&1 | Out-File "$out/tests.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual native display/coverage baseline and corruption tests failed'}
 $testText=Get-Content "$out/tests.log" -Raw
 if($testText -notmatch 'Ran (\d+) tests'){throw 'Missing executed test count'}
 $tests=[int]$Matches[1];$cases=@();$inputs=@{}
 & $python tools/verify_native_floor_display_v602.py display audit_v621_floor_latch_sonya_p2 sonya audit_v620_floor_sonya_p2 | Out-File "$out/display.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Actual front-buffer/VRAM/palette verification failed'}
 $display=Get-Content "$out/display.json" -Raw | ConvertFrom-Json
 foreach($fighter in @('kano','sonya')){
  & $python tools/verify_native_floor_display_v602.py coverage "audit_v620_floor_${fighter}_p2" $fighter "audit_v610_native_pit_${fighter}_p2" | Out-File "$out/$fighter.json" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual unassisted arena coverage/replay failed: $fighter"}
  $cases+=Get-Content "$out/$fighter.json" -Raw | ConvertFrom-Json
 }
 foreach($name in @('audit_v620_floor_kano_p2','audit_v620_floor_sonya_p2','audit_v621_floor_latch_sonya_p2',
                    'audit_v610_native_pit_kano_p2','audit_v610_native_pit_sonya_p2')){
  $folder=Join-Path $root $name
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Changed actual capture input: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $tracked=@($PSCommandPath,"$root/tools/verify_native_floor_display_v602.py","$root/tools/test_native_floor_display_v602.py",
  "$root/tools/verify_native_pit_scene_v602_v4.py","$root/tools/verify_native_pit_mirrors_v602.py","$root/tools/verify_native_pit_assets_v602.py",
  "$root/tools/inspect_natural_arena_floor_v602.py","$root/mk2ks_natural_campaign_probe_v14.lua",
  "$root/tools/run_natural_campaign_probe_v14.ps1","$root/mk2ks_natural_campaign_probe_v15.lua",
  "$root/tools/run_natural_campaign_probe_v15.ps1","$root/mame-mkp/src/devices/cpu/tms34010/tms34010.cpp",
  "$root/mame-mkp/src/mame/midway/midtunit_v.cpp","$root/mame-mkp/src/frontend/mame/luaengine.cpp",
  "$root/mame-mkp/src/emu/screen.cpp","$root/mame-mkp/src/emu/video.cpp",
  "$root/audit_v622_floor_buffer_boundary/NOTE.txt","$root/audit_v622_floor_buffer_boundary/input_sources/inspect_natural_arena_floor_v602.py")
 foreach($file in $tracked){$inputs[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.py','.ps1','.lua'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 [ordered]@{passed=$true;fullPortAcceptance=$false;floorAcceptance=$false;candidate='diagnostic_v602_native_pit_position';
  tests=$tests;checkedInputs=$inputs.Count;display=$display;coverage=$cases;
  retainedCheckerBoundary='audit_v622_floor_buffer_boundary';
  scope='Two actual P2 runs reach all nine regular arenas with607 retained floor screenshots and unchanged entire native input/health/fight/state replay. Fifteen moving Sonya Dead Pool screenshots bind exactly to actual native display flip/VRAM/palette. This proves buffer association and coverage, NOT desired shadow/ground-contact geometry, P1/secret arenas, a cleared tower or whole-port acceptance.';
  inputHashes=$inputs} | ConvertTo-Json -Depth 12 | Out-File "$out/result.json" -Encoding utf8
 "$tests native display/coverage baseline and corruption tests passed; $($display.pixels) exact displayed pixels. Floor and full acceptance remain false."
} finally {Pop-Location}
