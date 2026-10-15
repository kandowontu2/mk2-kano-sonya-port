param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateSet('kano','sonya')][string]$Fighter='kano',
    [ValidateSet('kano','sonya')][string]$Target='sonya',
    [ValidateSet(1,2)][int]$SourceSide=1,
    [ValidateSet(1,2)][int]$NewSide=1,
    [ValidateSet('none','projectile','mobility','sequence','pair','airthrow','lifecycle','mobility_contact','projectile_choreography')][string]$SpecialMode='none',
    [ValidateSet('hit','block','miss')][string]$ContactScenario='hit',
    [ValidateSet('sonya','sub_zero')][string]$AirVictim='sonya',
    [switch]$AirFollowup,
    [ValidateRange(0,140)][int]$FirstCommandAge=0,
    [ValidateSet('guard','retreat')][string]$ChargeStrategy='guard',
    [string]$CandidateName='diagnostic_v277_native_battle_photos'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$exe=Join-Path $root "$CandidateName/mkport_candidate.exe"
$rompath=Join-Path $root "$CandidateName/roms"
$buildPath=Join-Path $root "$CandidateName/build-info.json"
$build=Get-Content -LiteralPath $buildPath -Raw | ConvertFrom-Json
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or
   (Get-FileHash -LiteralPath "$rompath/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Selected candidate build mismatch'}
$currentCandidate=$CandidateName -eq 'diagnostic_v300_native_projectile_choreography'
if($currentCandidate){
    foreach($item in $build.input_hashes.PSObject.Properties){
        if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate build source mismatch: $($item.Name)"}
    }
}
if($SpecialMode -eq 'projectile_choreography'){
    if($CandidateName -ne 'diagnostic_v300_native_projectile_choreography'){throw 'Use the matched full choreography candidate'}
    foreach($item in $build.input_hashes.PSObject.Properties){
        if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate build source mismatch: $($item.Name)"}
    }
}
$harness=Join-Path $root 'mk2ks_post_ending_restart.lua'
$verifier=Join-Path $PSScriptRoot 'verify_post_ending_restart.py'
$assistanceVerifier=Join-Path $PSScriptRoot 'check_post_restart_assistance.py'
$tracked=@($exe,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),$harness,$PSCommandPath,
    (Join-Path $root 'mk2ks_cpu_ladder_trace.lua'),(Join-Path $root 'mk2ks_selector_exit_test.lua'),$verifier,$assistanceVerifier,
    (Join-Path $root "audit_v276_full_p${SourceSide}_photos_$Fighter/run.log"),
    (Join-Path $root 'mk2ks_p2_tower_probe.lua'),(Join-Path $root 'mk2ks_finish_range_test.lua'),
    (Join-Path $root 'mk2ks_finish_state_trace.lua'),(Join-Path $root 'mk2ks_native_shang_morph.lua'),
    (Join-Path $root 'mk2/mk2-maincpu.bin'),(Join-Path $PSScriptRoot 'verify_p2_tower.py'),
    (Join-Path $PSScriptRoot 'verify_p2_campaign.py'))
$tracked+=Join-Path $root 'mk2ks_restart_projectile.lua'
$tracked+=Join-Path $PSScriptRoot 'verify_restart_projectile.py'
if($currentCandidate){
    $tracked+=@($buildPath)+@($build.input_hashes.PSObject.Properties | Select-Object -ExpandProperty Name)
}
if($SpecialMode -eq 'projectile_choreography'){
    $tracked+=@($buildPath,"$root/mk2ks_restart_lifecycle.lua","$root/mk2ks_projectile_contact.lua",
        "$root/mk2ks_projectile_choreography_probe.lua","$root/mk2ks_projectile_impact_probe.lua",
        "$PSScriptRoot/verify_restart_lifecycle.py","$PSScriptRoot/verify_projectile_contact.py",
        "$PSScriptRoot/verify_projectile_choreography.py","$PSScriptRoot/build_native_projectile_choreography.py",
        "$PSScriptRoot/build_native_projectile_impacts.py","$PSScriptRoot/verify_current_lifecycle.py",
        "$root/diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.choreography.json")
    $tracked+=@($build.input_hashes.PSObject.Properties | Select-Object -ExpandProperty Name)
}
if($SpecialMode -eq 'mobility'){
    $tracked+=Join-Path $root 'mk2ks_restart_mobility.lua'
    $tracked+=Join-Path $PSScriptRoot 'verify_restart_mobility.py'
}
if($SpecialMode -eq 'sequence'){
    $tracked+=Join-Path $root 'mk2ks_restart_sequence.lua'
    $tracked+=Join-Path $PSScriptRoot 'verify_restart_sequence.py'
}
if($SpecialMode -eq 'pair'){
    $tracked+=Join-Path $root 'mk2ks_restart_pair.lua'
    $tracked+=Join-Path $PSScriptRoot 'verify_restart_pair.py'
}
if($SpecialMode -eq 'airthrow'){
    if($Target -ne 'kano'){throw 'Only Kano has a standalone air throw'}
    $tracked+=Join-Path $root 'mk2ks_restart_airthrow.lua'
    $tracked+=Join-Path $PSScriptRoot 'verify_restart_airthrow.py'
}
if($SpecialMode -eq 'lifecycle'){
    $tracked+=Join-Path $root 'mk2ks_restart_lifecycle.lua'
    $tracked+=Join-Path $root 'mk2ks_lifecycle_trace.lua'
    $tracked+=Join-Path $root 'mk2ks_blade_lifecycle_test.lua'
    $tracked+=Join-Path $root 'mk2ks_bicycle_lifecycle_test.lua'
    $tracked+=Join-Path $PSScriptRoot 'verify_restart_lifecycle.py'
    $tracked+=Join-Path $PSScriptRoot 'verify_current_lifecycle.py'
}
if($SpecialMode -eq 'mobility_contact'){
    $tracked+=Join-Path $root 'mk2ks_restart_lifecycle.lua'
    $tracked+=Join-Path $root 'mk2ks_mobility_contact.lua'
    $tracked+=Join-Path $PSScriptRoot 'verify_restart_lifecycle.py'
    $tracked+=Join-Path $PSScriptRoot 'verify_current_lifecycle.py'
    $tracked+=Join-Path $PSScriptRoot 'verify_mobility_contact.py'
}
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$drive=Get-PSDrive -Name ([IO.Path]::GetPathRoot($out).TrimEnd('\').TrimEnd(':'))
if($null -eq $drive.Free -or $drive.Free -lt 256MB){throw 'At least 256 MB free space is required to record the test evidence'}
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
# Record exact inputs before launch, including when an external interruption
# prevents the final verification/result files from being written.
$hashes | ConvertTo-Json -Depth 3 | Out-File -LiteralPath "$out/input_hashes_before.json" -Encoding utf8
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
foreach($path in $tracked){
    if([IO.Path]::GetExtension($path) -in @('.lua','.ps1','.py','.json','.cpp','.h')){
        Copy-Item -LiteralPath $path -Destination "$out/input_sources"
    }
}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Fighter;$env:MK2KS_RESTART_TARGET=$Target;$env:MK2KS_P2_FIGHTER='stock'
    $env:MK2KS_RESTART_SOURCE_SIDE="$SourceSide"
    $env:MK2KS_RESTART_NEW_SIDE="$NewSide"
    $env:MK2KS_RESTART_SPECIAL=$SpecialMode
    $env:MK2KS_MOBILITY_CONTACT=$ContactScenario
    if($currentCandidate){$env:MK2KS_TRACE_ALL_REGEN='1'}
    if($SpecialMode -eq 'projectile_choreography'){
        $env:MK2KS_PROJECTILE_CONTACT=$ContactScenario
        $env:MK2KS_PROJECTILE_CHOREOGRAPHY='1';$env:MK2KS_PROJECTILE_OBSERVER_ONLY='1'
        $env:MK2KS_TRACE_ALL_REGEN='1'
    }
    if($SpecialMode -eq 'lifecycle'){$env:MK2KS_LIFECYCLE_TRACE='1'}
    $env:MK2KS_AIR_JOIN_VICTIM=$AirVictim
    $env:MK2KS_AIR_JOIN_FOLLOWUP=if($AirFollowup){'1'}else{'0'}
    $env:MK2KS_RESTART_FIRST_COMMAND_AGE="$FirstCommandAge"
    $env:MK2KS_RESTART_SEQUENCE_FIRST_COMMAND_AGE="$FirstCommandAge"
    $env:MK2KS_RESTART_PAIR_FIRST_COMMAND_AGE="$FirstCommandAge"
    $env:MK2KS_RESTART_CHARGE_STRATEGY=$ChargeStrategy
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_ROUND_WIN='1';$env:MK2KS_ROUND_WIN_STRATEGY='rapid_uppercut'
    $env:MK2KS_DIAGNOSTIC_ALL_STAGES='1';$env:MK2KS_DIAGNOSTIC_CPU_HEALTH='1';$env:MK2KS_DIAGNOSTIC_P1_REGEN='1'
    $env:MK2KS_ASSERT_MULTI_PROGRESS_MIN_STAGE='16';$env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2KS_ENDING_TRACE_ALL='1';$env:MK2KS_STAGE_VISUAL_SNAPSHOTS='1'
    if($SourceSide -eq 2){
        Remove-Item Env:MK2KS_TEST_ROUND_WIN,Env:MK2KS_DIAGNOSTIC_ALL_STAGES,Env:MK2KS_DIAGNOSTIC_CPU_HEALTH,Env:MK2KS_DIAGNOSTIC_P1_REGEN,Env:MK2KS_ASSERT_MULTI_PROGRESS_MIN_STAGE
        $env:MK2KS_TEST_FIGHTER=if($Fighter -eq 'kano'){'sonya'}else{'kano'}
        $env:MK2KS_P2_FIGHTER=$Fighter;$env:MK2KS_TWO_PLAYER='1';$env:MK2KS_TEST_ROUND_LOSS='1'
        $env:MK2_TRACE_NATIVE_FINISH=$Fighter;$env:MK2_TRACE_NATIVE_FINISH_SIDE='2'
        $env:MK2_TRACE_INPUT_ONLY_APPROACH='1';$env:MK2_TRACE_FINISH_ACTORS='1'
        $env:MK2_RANGE_EXPECT='activate';$env:MK2_RANGE_MULTIPLE_FINISHES='1'
        $env:MK2_P2_TOWER_HEALTH_ASSIST='1';$env:MK2_P2_POST_ENDING_RESTART='1'
    }
    $snapshotSize=if($SpecialMode -eq 'projectile_choreography'){'400x254'}else{'400x300'}
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str 2400 -snapsize $snapshotSize `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $extraVerify=@()
    if($AirFollowup){$extraVerify+='--air-followup'}
    & python $verifier "$out/run.log" --fighter $Fighter --target $Target --source-side $SourceSide --new-side $NewSide --special-mode $SpecialMode @extraVerify |
        Out-File -LiteralPath "$out/restart_verification.json" -Encoding utf8
    $independent=$LASTEXITCODE -eq 0
    $assistanceArgs=@()
    if($currentCandidate -or $SpecialMode -eq 'projectile_choreography'){$assistanceArgs+='--all-regen'}
    & python $assistanceVerifier "$out/run.log" --fighter $Fighter --source-side $SourceSide @assistanceArgs |
        Out-File -LiteralPath "$out/assistance_verification.json" -Encoding utf8
    $assistanceExcluded=$LASTEXITCODE -eq 0
    $snapshots=@('attract','css','highlight_140','highlight_156','match','combat_120','combat_600')
    if($SpecialMode -eq 'projectile'){$snapshots+=@('projectile_08','projectile_16')}
    $missing=@($snapshots | Where-Object {-not (Test-Path -LiteralPath "$out/snap/restart_$_.png")})
    if($SpecialMode -eq 'airthrow'){
        $missing+=@('css','highlight','match','ready','final','pose_24','pose_32','pose_40','pose_48','pose_56','pose_64','pose_72','pose_80','pose_96','pose_120') |
            Where-Object {-not (Test-Path -LiteralPath "$out/snap/air_join_$_.png")}
    }
    if($SpecialMode -in @('lifecycle','mobility_contact','projectile_choreography')){
        $missing+=@('css','highlight','match','complete') | Where-Object {-not (Test-Path -LiteralPath "$out/snap/join_life_$_.png")}
    }
    if($SpecialMode -eq 'mobility_contact'){
        $missing+=@('8','18','40','ready') | Where-Object {-not (Test-Path -LiteralPath "$out/snap/mob_contact_$_.png")}
    }
    $tower=if($SourceSide -eq 1){$log.Contains('ended=true completed=true diagnostic=false,false') -and $log.Contains('identity_errors=0 stage_errors=0')}
        else{$log.Contains('MK2_P2_TOWER_RESULT pass=true ') -and $log.Contains('MK2_RANGE_RESULT pass=true ')}
    $passed=$exitCode -eq 0 -and $independent -and $assistanceExcluded -and $tower -and $missing.Count -eq 0 -and $log.Contains('MK2_RESTART_RESULT pass=true ') -and
        $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
        $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log -notmatch '(?i)fatal error|\[LUA ERROR\]|exception at|access violation'
    [ordered]@{passed=$passed;independent_verification=$independent;restart_health_assistance_excluded=$assistanceExcluded;missing_snapshots=$missing;exit_code=$exitCode;fighter=$Fighter;target=$Target;cheats_enabled=$false;
        candidate=$CandidateName;candidate_executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
        source_side=$SourceSide;new_game_side=$NewSide;
        special_mode=$SpecialMode;
        contact_scenario=$ContactScenario;
        air_victim=$AirVictim;
        air_followup=$AirFollowup.IsPresent;
        first_command_age=$FirstCommandAge;
        charge_strategy=$ChargeStrategy;
        tower_assistance='health_only';restart_assistance='none';
        all_campaign_regeneration_logged=$currentCandidate;
        scope="full_p${SourceSide}_assisted_tower_both_ending_pages_then_input_only_new_p${NewSide}_game_not_unassisted_tower";input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed"
    if(-not $passed){throw 'Post-ending new-game restart acceptance failed; preserve evidence'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
