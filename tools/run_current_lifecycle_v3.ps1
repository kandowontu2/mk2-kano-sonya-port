param([Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateSet('blade','bicycle')][string]$Move,
    [ValidateSet(1,2)][int]$Side=1,
    [ValidateSet('kano','sonya','kitana','sub_zero')][string]$Victim,
    [string]$CandidateName='diagnostic_v635_native_shadow_rows')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence and candidate names'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$payload=Join-Path $candidate 'roms/mk2ks/mk2ks.mdata'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate input changed: $($item.Name)"}}
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Candidate build changed'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$harness=Join-Path $root "mk2ks_${Move}_lifecycle_test.lua"
$tracked=@($exe,$payload,$harness,"$root/mk2ks_lifecycle_trace.lua","$root/mk2ks_selector_exit_test.lua",$PSCommandPath)
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@("$candidate/build-info.json")
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
$tracked+=@("$root/mk2ks_native_shang_morph.lua")
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
$hashes=[ordered]@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $attacker=if($Move -eq 'blade'){'kano'}else{'sonya'}
    $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){$attacker}else{$Victim}
    $env:MK2KS_P2_FIGHTER=if($Side -eq 2){$attacker}else{$Victim}
    $env:MK2KS_TWO_PLAYER='1';$env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1';$env:MK2KS_LIFECYCLE_TRACE='1'
    Set-Item -LiteralPath "Env:MK2KS_$($Move.ToUpper())_SIDE" -Value "$Side"
    & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str 120 -snapsize 400x254 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $harness 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed during case: $path"}}
    $log=Get-Content "$out/run.log" -Raw
    $markers=@("MK2KS_$($Move.ToUpper())_LIFECYCLE_RESULT pass=true ",'MK2KS_EXIT_RESULT pass=true ',
        'MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0')
    $passed=$code -eq 0 -and $log -notmatch '(?i)fatal error|\[LUA ERROR\]|access violation|exception at'
    foreach($marker in $markers){$passed=$passed -and $log.Contains($marker)}
    [ordered]@{observer_passed=$passed;exit_code=$code;move=$Move;side=$Side;victim=$Victim;cheats=$false;memory_assistance='none';
        production_inputs_match_v277=($CandidateName -eq 'diagnostic_v277_native_battle_photos');candidate=$CandidateName;
        candidate_executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
        input_hashes=$hashes;scope='cold_native_two_human_repeated_moves_KO_next_round_not_post_ending_or_CPU';
        independent_verification_pending=$true} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal observer_pass=$passed"
    if(-not $passed){throw 'Preserve failed lifecycle evidence'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}

