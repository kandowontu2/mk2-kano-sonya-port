$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $portRoot 'diagnostic_v45_choke_release_candidate'
$expectedExe='FD8A14306C20F61920BB02AEEC715496D7F3188E27BC3F030F027473BA3DB546'
$expectedPayload='C6A77F803191830D471F0127D540AF27039C259ABAC9A9235804B83DFE1A3ED9'
$inventory=[Collections.Generic.List[object]]::new()
function Add-Case([string]$Name,[string]$Family,[string]$Marker) {
    $inventory.Add([pscustomobject]@{name=$Name;family=$Family;marker=$Marker})
}
foreach ($side in 1,2) {
    foreach ($victim in 'kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax') {
        $prefix=if ($victim -eq 'shang_tsung') {'regression_v45_choke_final_motion'} else {'regression_v45_choke_final_stock'}
        Add-Case "${prefix}_side${side}_${victim}_near" 'choke' 'MK2KS_CHOKE_RESULT pass=true '
    }
    foreach ($mode in 'near','block','duck','duck_block','air','far','held','reversed','expired','wrong_button','airborne','with_block') {
        Add-Case "regression_v45_choke_final_inputs_side${side}_sonya_${mode}" 'choke' 'MK2KS_CHOKE_RESULT pass=true '
    }
    Add-Case "regression_v45_choke_final_mirror_side${side}_kano_near" 'choke' 'MK2KS_CHOKE_RESULT pass=true '
    foreach ($victim in 'sonya','kano','kitana','sub_zero') {
        Add-Case "regression_v45_choke_rounds_side${side}_${victim}" 'choke-rounds' 'MK2KS_CHOKE_LIFECYCLE_RESULT pass=true '
    }
    foreach ($victim in 'kano','sonya') {
        Add-Case "regression_v45_choke_release_blade_side${side}_${victim}" 'blade-rounds' 'MK2KS_BLADE_LIFECYCLE_RESULT pass=true '
    }
}
foreach ($fighter in 'kano','sonya') {
    foreach ($victim in 'kano','sonya') {
        foreach ($mode in 'near','corner_left','corner_right') {
            Add-Case "regression_v45_choke_release_leg_${fighter}_vs_${victim}_${mode}" 'leg' 'MK2KS_LEG_RESULT pass=true '
        }
    }
    foreach ($mode in 'native','wrong_button','with_block') {
        Add-Case "regression_v45_choke_release_projectiles_${fighter}_${mode}" 'projectiles-smoke' 'MK2KS_PROJECTILES_RESULT pass=true '
    }
    foreach ($mode in 'hit','minimum') {
        Add-Case "regression_v45_choke_release_ball_${fighter}_${mode}" 'ball-smoke' 'MK2KS_BALL_RESULT pass=true '
    }
    foreach ($mode in 'ground','air') {
        Add-Case "regression_v45_choke_release_square_${fighter}_${mode}" 'square-smoke' 'MK2KS_SQUARE_RESULT pass=true '
    }
    foreach ($mode in 'mirrors','jumps','lifecycle','wins','basics') {
        $marker=switch ($mode) {
            mirrors {'MK2KS_MIRROR_RESULT pass=true '}
            jumps {'MK2KS_JUMP_SUITE pass=true failures=0'}
            lifecycle {'MK2KS_LIFECYCLE_RESULT pass=true '}
            wins {'MK2KS_EXIT_RESULT pass=true '}
            basics {'MK2KS_BASIC_RESULT pass=true checks=20 errors=0'}
        }
        Add-Case "regression_v45_choke_release_core_${mode}_${fighter}" $mode $marker
    }
}
Add-Case 'regression_v45_choke_release_core_grid' 'grid' 'MK2KS_GRID_RESULT pass=true checks=31 failures=0'
Add-Case 'regression_v45_choke_release_core_navigation' 'navigation' 'MK2KS_NAV_RESULT pass=true checks=10 failures=0'
if ($inventory.Count -ne 100 -or @($inventory.name | Sort-Object -Unique).Count -ne 100) {throw 'Invalid exact choke inventory'}
$verified=@()
foreach ($case in $inventory) {
    $out=Join-Path $portRoot $case.name
    $result=Get-Content -LiteralPath "$out\result.json" -Raw | ConvertFrom-Json
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    if ($result.case -ne $case.name -or -not $result.passed -or $result.exit_code -ne 0 -or
        $result.executable_sha256 -ne $expectedExe -or $result.payload_sha256 -ne $expectedPayload -or
        -not $log.Contains($case.marker) -or $log -match '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]') {
        throw "Invalid or failed evidence: $($case.name)"
    }
    if ($case.family -notin 'grid','navigation','basics') {
        foreach ($marker in @('MK2KS_EXIT_RESULT pass=true ','MK2KS_DISPLAY_RESULT pass=true ',
            'MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0')) {
            if (-not $log.Contains($marker)) {throw "Missing $marker in $($case.name)"}
        }
    }
    if ($case.family -eq 'choke') {
        $positive=$case.name -match '_(near|held)$'
        $negative=$case.name -match '_(reversed|expired|wrong_button|airborne|with_block)$'
        $expectedEntries=if ($negative) {0} else {1}
        $summary=[regex]::Match($log,'MK2KS_CHOKE_RESULT pass=true [^\r\n]+').Value
        $detail=if ($positive) {'pairs=22 pair_checks=22 pulses=4 releases=1'} else {'pairs=0 pair_checks=0 pulses=0 releases=0'}
        if (-not $summary.Contains("entries=$expectedEntries ") -or -not $summary.Contains($detail) -or -not $summary.Contains('errors=0')) {throw "Incomplete choreography/input evidence: $($case.name)"}
        if ($positive -and @([regex]::Matches($log,'MK2KS_CHOKE_VELOCITY_REQUEST frame=')).Count -ne 1) {throw "Missing native velocity request: $($case.name)"}
    }
    if ($case.family -eq 'choke-rounds' -and -not $log.Contains('cycles=7 huds=3 wins=1 ')) {throw "Incomplete choke KO/next-round evidence: $($case.name)"}
    if ($case.family -eq 'blade-rounds' -and -not $log.Contains('cycles=8 hud_entries=3 wins=1 ')) {throw "Incomplete blade KO/next-round evidence: $($case.name)"}
    if ($case.family -eq 'basics') {
        foreach ($marker in @('MK2KS_MOVE_RESULT pass=true ','stalled_frames=0 trap_frames=0','MK2KS_ROSTER_RESULT roster_errors=0 identity_errors=0')) {
            if (-not $log.Contains($marker)) {throw "Incomplete core identity/stability: $($case.name)"}
        }
    }
    $verified+=[ordered]@{family=$case.family;result=$result;log_sha256=(Get-FileHash -LiteralPath "$out\run.log").Hash}
}
$build=Get-Content -LiteralPath "$candidate\build-info.json" -Raw | ConvertFrom-Json
if ((Get-FileHash -LiteralPath "$candidate\mkport_candidate.exe").Hash -ne $expectedExe) {throw 'Candidate changed'}
foreach ($buildInput in $build.input_hashes.PSObject.Properties) {
    if ((Get-FileHash -LiteralPath $buildInput.Name).Hash -ne $buildInput.Value) {throw "Build source/input changed: $($buildInput.Name)"}
}
$assets=Get-Content -LiteralPath "$candidate\asset-tests-final.log" -Raw
if ($assets -notmatch 'Ran 30 tests' -or $assets -notmatch '(?m)^OK\s*$' -or $assets -match 'FAILED|skipped=') {throw 'Asset checks incomplete'}
if ((Get-FileHash -LiteralPath "$portRoot\mame-mkp\mkport.exe").Hash -ne '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891') {throw 'Installed v42 changed'}
$releaseRoot='C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs'
$releases=@{
    'MK2-Kano-Sonya-v42-2026-09-05.zip'='1568AB02D4E639B4EE45F922F380597F680605A1FACD7DF352F7AE260DBB91A8'
    'MK2-Kano-Sonya-v44-WIP-2026-09-05.zip'='C72E5B40A01CC566167D41FD221B4170D0417A496C132B1B4E044B099EAB5C7F'
}
foreach ($releaseName in $releases.Keys) {
    if ((Get-FileHash -LiteralPath (Join-Path $releaseRoot $releaseName)).Hash -ne $releases[$releaseName]) {throw "Released ZIP changed: $releaseName"}
}
$manifest=Join-Path $candidate 'verification.json'
if (Test-Path -LiteralPath $manifest) {throw 'Refusing to overwrite completed verification'}
[ordered]@{executable_sha256=$expectedExe;payload_sha256=$expectedPayload;runtime_cases=100;asset_tests=30;
    cases=$verified;asset_log_sha256=(Get-FileHash -LiteralPath "$candidate\asset-tests-final.log").Hash;
    installed_cmd='Unchanged v42';release_zips=$releases;
    observer_note='Shang Tsung reruns observe motion after native body separation has finished; earlier failed observer logs remain preserved.';
    remaining=@('Choke exact audio and full corner/interruption/boss/CPU semantics','Remaining native specials including Sonya bicycle','Original character voices and announcer','Finishers','AI roster participation','Complete progression and endings','Full integration acceptance; no installed/release promotion')} |
    ConvertTo-Json -Depth 8 | Out-File -LiteralPath $manifest -Encoding utf8
Write-Output 'Verified 100 exact current-candidate runtime cases and 30 asset tests.'
