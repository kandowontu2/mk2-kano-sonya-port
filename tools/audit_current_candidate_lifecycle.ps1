param([string]$OutputName='audit_v306_current_lifecycle_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence name'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$candidateRoot=Join-Path $root 'diagnostic_v300_native_projectile_choreography'
$build=Get-Content "$candidateRoot/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}
}
if((Get-FileHash "$candidateRoot/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or
   (Get-FileHash "$candidateRoot/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Candidate identity mismatch'}
$renderCheckpoint=Get-Content "$root/audit_v304_projectile_render_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $renderCheckpoint.passed -or $renderCheckpoint.candidate_executable_sha256 -ne $build.executable_sha256 -or
   $renderCheckpoint.payload_sha256 -ne $build.payload_sha256){throw 'Matched current render checkpoint missing'}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($PSCommandPath,"$PSScriptRoot/run_current_lifecycle.ps1","$PSScriptRoot/verify_current_lifecycle.py",
    "$root/mk2ks_lifecycle_trace.lua","$root/mk2ks_blade_lifecycle_test.lua","$root/mk2ks_bicycle_lifecycle_test.lua",
    "$root/mk2ks_selector_exit_test.lua","$candidateRoot/mkport_candidate.exe","$candidateRoot/roms/mk2ks/mk2ks.mdata",
    "$candidateRoot/build-info.json","$root/audit_v304_projectile_render_final_inputs/result.json")
$hashes=[ordered]@{}
foreach($path in $tracked){
    $hashes[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.json'){
        Copy-Item -LiteralPath $path -Destination "$out/input_sources"
    }
}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$specs=@(@('blade',1,'sonya'),@('blade',2,'sub_zero'),@('bicycle',1,'kano'),@('bicycle',2,'kitana'))
$cases=@()
foreach($spec in $specs){
    $move=$spec[0];$side=$spec[1];$victim=$spec[2]
    $name="audit_v305_current_${move}_p${side}_${victim}";$folder=Join-Path $root $name
    $metadata=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if($metadata.exit_code -ne 0 -or -not $metadata.observer_passed -or
       $metadata.candidate -ne $build.name -or $metadata.candidate_executable_sha256 -ne $build.executable_sha256 -or
       $metadata.payload_sha256 -ne $build.payload_sha256 -or $metadata.move -ne $move -or $metadata.side -ne $side -or
       $metadata.victim -ne $victim -or $metadata.cheats -or $metadata.memory_assistance -ne 'none'){
        throw "Terminal current case identity mismatch: $name"
    }
    foreach($item in $metadata.input_hashes.PSObject.Properties){
        $source=$item.Name
        if([IO.Path]::GetExtension($source) -in '.lua','.ps1'){$source=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($source))}
        if((Get-FileHash -LiteralPath $source).Hash -ne $item.Value){throw "Frozen launch source mismatch: $source"}
        $hashes[$source]=$item.Value
    }
    $hashes["$folder/run.log"]=(Get-FileHash "$folder/run.log").Hash
    $hashes["$folder/result.json"]=(Get-FileHash "$folder/result.json").Hash
    python "$PSScriptRoot/verify_current_lifecycle.py" "$folder/run.log" --move $move --side $side --victim $victim |
        Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Actual current lifecycle failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $cases+=[ordered]@{name=$name;passed=$proof.passed;move=$move;side=$side;victim=$victim;
        cycles=$proof.cycles;fields=$proof.actual_fields;native_health_stores=$proof.health_stores;scope=$proof.scope}
    "$name actual current full move / KO / next-round recovery verified"
}
foreach($path in $hashes.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input/evidence changed: $path"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_after.json" -Encoding utf8
[ordered]@{passed=$true;candidate=$build.name;candidate_executable_sha256=$build.executable_sha256;
    payload_sha256=$build.payload_sha256;current_cold_lifecycle_cases=$cases;
    matched_projectile_render_checkpoint='audit_v304_projectile_render_final_inputs/result.json';
    health_assistance='none';production_unchanged=$true;full_character_integration_complete=$false;
    scope='four_current_cold_two_human_blade_bicycle_repeated_contacts_KO_refill_next_action_not_all_victims_CPU_or_post_ending';
    input_hashes=$hashes} | ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
