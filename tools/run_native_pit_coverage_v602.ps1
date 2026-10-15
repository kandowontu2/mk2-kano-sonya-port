param([string]$CaseName='audit_v617_native_pit_slots_mirrors_checked_inputs')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Never overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try {
 $tests=0;$cases=@();$rasters=@();$inputs=@{}
 foreach($suite in @('test_native_pit_assets_v602','test_native_pit_scene_v602_v4','test_native_pit_mirrors_v602','test_native_pit_raster_v602')){
  & $python -m unittest discover -s tools -p "$suite.py" -v 2>&1 | Out-File "$out/$suite.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual baseline/corruption suite failed: $suite"}
  $testText=Get-Content "$out/$suite.log" -Raw
  if($testText -notmatch 'Ran (\d+) tests'){throw 'Missing executed test count'}
  $tests+=[int]$Matches[1]
 }
 $folders=@()
 foreach($fighter in @('kano','sonya')){
  foreach($side in @(1,2)){
   $prefix=if($side -eq 1){'audit_v603'}else{'audit_v610'}
   $folder="$root/${prefix}_native_pit_${fighter}_p${side}";$key="${fighter}_p${side}"
   $arguments=@('tools/verify_native_pit_scene_v602_v4.py',$folder,$fighter,'--side',"$side")
   if($side -eq 1){
    $reference=if($fighter -eq 'kano'){"$root/audit_v592_pit_actual_lookup_kano_p1"}else{"$root/audit_v599_native_pit_sonya_p1_uppercut"}
    $arguments+=@('--reference',$reference)
    $inputs["$reference/run.log"]=(Get-FileHash -LiteralPath "$reference/run.log").Hash
   }
   & $python @arguments | Out-File "$out/$key.json" -Encoding utf8
   if($LASTEXITCODE -ne 0){throw "Actual native physical-slot verification failed: $key"}
   $cases+=Get-Content "$out/$key.json" -Raw | ConvertFrom-Json
   & $python tools/verify_native_pit_raster_v602.py $folder $fighter "$out/$key.json" | Out-File "$out/${key}_raster.json" -Encoding utf8
   if($LASTEXITCODE -ne 0){throw "Actual timed raster verification failed: $key"}
   $rasters+=Get-Content "$out/${key}_raster.json" -Raw | ConvertFrom-Json
   $folders+=$folder
  }
  $folder="$root/audit_v615_${fighter}_p2_mirror_palette";$key="${fighter}_p2_mirror"
  $reference=if($fighter -eq 'kano'){"$root/audit_v611_native_pit_kano_p2_boot604"}else{"$root/audit_v613_sonya_p2_mirror_boot605"}
  & $python tools/verify_native_pit_mirrors_v602.py $folder $fighter $reference | Out-File "$out/$key.json" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual native mirror verification failed: $key"}
  $cases+=Get-Content "$out/$key.json" -Raw | ConvertFrom-Json
  & $python tools/verify_native_pit_raster_v602.py $folder $fighter "$out/$key.json" | Out-File "$out/${key}_raster.json" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Actual native mirror raster verification failed: $key"}
  $rasters+=Get-Content "$out/${key}_raster.json" -Raw | ConvertFrom-Json
  $folders+=@($folder,$reference)
 }
 foreach($folder in $folders){
  $manifest=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
  foreach($entry in $manifest.PSObject.Properties){
   if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Capture input changed: $($entry.Name)"}
   $inputs[$entry.Name]=$entry.Value
  }
  foreach($file in Get-ChildItem -LiteralPath $folder -File -Recurse){$inputs[$file.FullName]=(Get-FileHash -LiteralPath $file.FullName).Hash}
 }
 $tracked=@($PSCommandPath,"$root/tools/build_native_pit_fall_v2.py","$root/tools/verify_native_pit_assets_v602.py",
  "$root/tools/test_native_pit_assets_v602.py","$root/tools/verify_native_pit_scene_v602_v4.py","$root/tools/test_native_pit_scene_v602_v4.py",
  "$root/tools/verify_native_pit_mirrors_v602.py","$root/tools/test_native_pit_mirrors_v602.py",
  "$root/tools/verify_native_pit_raster_v602.py","$root/tools/test_native_pit_raster_v602.py",
  "$root/tools/inspect_native_pit_pixels_v602.py","$root/mk2/mk2-maincpu.bin","$root/mk3/mk3-maincpu.bin",
  "$root/mk2ks_natural_campaign_probe_v11.lua","$root/tools/run_natural_campaign_probe_v11.ps1",
  "$root/diagnostic_v601_native_pit_position_assets/asset-report.json",
  "$root/diagnostic_v601_native_pit_position_assets/native-palette-preview.png")
 $tracked+=@(Get-ChildItem -LiteralPath "$root/diagnostic_v595_pit_sprite_drafts" -File | Select-Object -ExpandProperty FullName)
 foreach($file in $tracked){$inputs[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.py','.ps1','.lua'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
 $inputs | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($file in $inputs.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $inputs[$file]){throw "Verified input changed: $file"}}
 $frameTotal=($rasters | Measure-Object checked_frames -Sum).Sum
 $pixelTotal=($rasters | Measure-Object opaque_pixels -Sum).Sum
 [ordered]@{passed=$true;fullPortAcceptance=$false;candidate='diagnostic_v602_native_pit_position';tests=$tests;
  checkedInputs=$inputs.Count;cases=$cases;rasters=$rasters;fallingRasterFrames=$frameTotal;opaqueBodyPixels=$pixelTotal;
  retainedCheckerBoundary='audit_v616_checker_boundary';retainedReentrantObserver='audit_v614_kano_p2_mirror_palette';
  scope='Both actual physical slots plus P2 mirror victims: seven native Pit episodes, bounded copies, exact original constructor palette sources, complete native exits and genuine paid continues. 133 fixed-phase falling rasters. Not impact shake/foreground/audio, P1 mirror victims, cleared towers or whole-port/release acceptance.';
  inputHashes=$inputs} | ConvertTo-Json -Depth 12 | Out-File "$out/result.json" -Encoding utf8
 "$tests native Pit baseline/corruption tests, $frameTotal falling rasters and $pixelTotal opaque body pixels passed; full acceptance remains false."
} finally {Pop-Location}
