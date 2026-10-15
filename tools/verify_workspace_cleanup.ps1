param([ValidatePattern('^audit_v284_cleanup_[a-z0-9_]+$')][string]$OutputName='audit_v284_cleanup_final_inputs')
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$archiveRoot=Join-Path $root '_archive/legacy_evidence_v284'
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite cleanup verification'}
if(-not(Test-Path -LiteralPath "$archiveRoot/result.json")){throw 'Archive job has not finished'}
$plan=Get-Content -LiteralPath "$archiveRoot/plan.json" -Raw | ConvertFrom-Json
$result=Get-Content -LiteralPath "$archiveRoot/result.json" -Raw | ConvertFrom-Json
$progress=Get-Content -LiteralPath "$archiveRoot/progress.json" -Raw | ConvertFrom-Json
if($plan.root -ne $root -or -not $result.complete -or
   $result.target_folders -ne $plan.target_folders -or
   $progress.completed_batches -ne $progress.total_batches -or
   @($result.archives).Count -ne $progress.total_batches){throw 'Incomplete archive result'}
$removed=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$archiveChecks=@()
foreach($batch in $result.archives){
    if(-not $batch.crc_verified -or -not $batch.source_sha256_rechecked -or
       -not $batch.original_directories_removed){throw 'Archive batch was not verified before removal'}
    $path=Join-Path $archiveRoot $batch.archive
    if((Get-FileHash -LiteralPath $path).Hash -ne $batch.archive_sha256 -or
       (Get-Item -LiteralPath $path).Length -ne $batch.archive_bytes){throw 'Archive changed after verification'}
    $manifestPath=[IO.Path]::ChangeExtension($path,'files.json')
    $manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $files=@($manifest.PSObject.Properties)
    if($files.Count -ne $batch.source_files -or
       ($files | ForEach-Object {$_.Value.bytes} | Measure-Object -Sum).Sum -ne $batch.logical_bytes){throw 'Source manifest count/size mismatch'}
    foreach($name in $batch.folders){
        if([IO.Path]::GetFileName($name) -ne $name -or -not $removed.Add($name)){throw 'Unsafe or duplicate removed folder'}
        if(Test-Path -LiteralPath (Join-Path $root $name)){throw 'Archived original folder was not removed'}
    }
    $archiveChecks+=[ordered]@{archive=$batch.archive;sha256=$batch.archive_sha256;
        source_manifest_sha256=(Get-FileHash -LiteralPath $manifestPath).Hash;files=$files.Count;
        logical_bytes=$batch.logical_bytes;archive_bytes=$batch.archive_bytes}
}
if($removed.Count -ne $plan.target_folders){throw 'Removed-folder count differs from plan'}
$archiveBytes=($archiveChecks | ForEach-Object {$_.archive_bytes} | Measure-Object -Sum).Sum
$recordedArchiveBytes=($result.archives | Measure-Object archive_bytes -Sum).Sum
if($archiveBytes -le 0 -or $archiveBytes -ne $recordedArchiveBytes){throw 'Invalid total archive size'}
foreach($target in $plan.targets){if(-not $removed.Contains($target.name)){throw 'Planned folder missing from verified archive records'}}
$inventory=Get-Content -LiteralPath "$root/audit_v284_disk_recovery/folder_inventory_before.json" -Raw | ConvertFrom-Json
$preserved=0
foreach($folder in $inventory){
    if(-not $removed.Contains($folder.name)){
        if(-not(Test-Path -LiteralPath (Join-Path $root $folder.name) -PathType Container)){throw "Unplanned folder removal: $($folder.name)"}
        $preserved++
    }
}
$build=Get-Content -LiteralPath "$root/diagnostic_v277_native_battle_photos/build-info.json" -Raw | ConvertFrom-Json
foreach($prop in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $prop.Name).Hash -ne $prop.Value){throw "Production input changed: $($prop.Name)"}
}
$prior=Get-Content -LiteralPath "$root/audit_v284_sequence_final_inputs/result.json" -Raw | ConvertFrom-Json
$paths=[ordered]@{executable_sha256="$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe";
    payload_sha256="$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata";
    root_cmd_sha256="$root/PLAY_MK2_KANO_SONYA.cmd";
    candidate_cmd_sha256="$root/diagnostic_v277_native_battle_photos/PLAY_CANDIDATE.cmd";
    installed_generic_exe_sha256="$root/mame-mkp/mkport.exe";
    old_zip_sha256='C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port/MK2_Kano_Sonya_v258_playtest.zip'}
$hashes=[ordered]@{}
foreach($key in $paths.Keys){
    $hashes[$key]=(Get-FileHash -LiteralPath $paths[$key]).Hash
    if($hashes[$key] -ne $prior.hashes.$key){throw "Playable/archive changed: $key"}
}
$outerCmd='C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port/PLAY_MK2_KANO_SONYA.cmd'
$outerHash=(Get-FileHash -LiteralPath $outerCmd).Hash
if($outerHash -ne 'C94CFA01D231BE90597DF799FC8043FCAA18ED467886B347A984B32BFABC91B7'){throw 'Outer launcher changed'}
$modules=@(Select-String -LiteralPath "$root/audit_v284_final_reference_units.log" -Pattern '\((test_[A-Za-z0-9_]+)\.' |
    ForEach-Object {$_.Matches.Groups[1].Value} | Sort-Object -Unique)
if($modules.Count -ne 17){throw 'Reference module list differs from accepted suite'}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $PSScriptRoot
try {
    & python -m unittest @modules -v 2>&1 | Out-File -LiteralPath "$out/reference_tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Post-cleanup reference tests failed'}
} finally {Pop-Location}
$units=Get-Content -LiteralPath "$out/reference_tests.log" -Raw
if($units -notmatch 'Ran 236 tests' -or $units -notmatch '\bOK\s*$' -or $units -match '(?m)^(FAILED|FAIL:|ERROR:)'){throw 'Incomplete reference test result'}
Push-Location $root
try {
    & "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks |
        Out-File -LiteralPath "$out/launcher_verify.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Actual workspace CMD ROM verification failed'}
} finally {Pop-Location}
$tools=[ordered]@{}
foreach($file in Get-ChildItem -LiteralPath $PSScriptRoot -Filter 'test_*.py' -File){$tools[$file.Name]=(Get-FileHash -LiteralPath $file.FullName).Hash}
[ordered]@{complete=$true;removed_folders=$removed.Count;archive_batches=$archiveChecks.Count;
    logical_source_bytes=$plan.logical_bytes;archive_bytes=$archiveBytes;
    logical_footprint_reduction_not_measured_disk_allocation=$plan.logical_bytes-$archiveBytes;
    non_target_preexisting_folders_preserved=$preserved;production_inputs_match_v277=$true;
    playable_and_old_zip_unchanged=$true;hashes=$hashes;outer_cmd_sha256=$outerHash;
    reference_tests_passed=236;reference_modules=$modules;
    reference_log_sha256=(Get-FileHash -LiteralPath "$out/reference_tests.log").Hash;
    launcher_verify_exit=0;archive_sha256_and_manifests_rechecked=$archiveChecks;
    test_source_hashes=$tools;full_character_integration_complete=$false;
    recovery='Extract the relevant _archive/legacy_evidence_v284/batch_NNN.7z into the mk2port root; .files.json records original file hashes';
    disk_space_note='Logical source/archive sizes are not exact NTFS allocated-space savings; drive free-space changes also include unrelated activity'} |
    ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
'Cleanup verified: all archived targets removed, all other original folders retained, current build unchanged, 236 tests and actual launcher verification passed'
