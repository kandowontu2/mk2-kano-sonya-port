$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $portRoot 'diagnostic_v46_bicycle_asset_candidate'
$expectedExe='FCA7B8174C7D019236835ECFBEB8E8254622CE4405CA8842CAD04782F47FE96A'
$expectedPayload='5CA9EE80B2737F7A295554C22BF3D4068C2552F90C744BA1D125B41251945D55'
$inventory=[Collections.Generic.List[object]]::new()
function Add-Case([string]$Name,[string]$Family,[string]$Marker) {
    $inventory.Add([pscustomobject]@{name=$Name;family=$Family;marker=$Marker})
}
foreach ($side in 1,2) {
    foreach ($victim in 'kano','sonya') {
        Add-Case "regression_v46_bicycle_asset_mirrors_side${side}_${victim}_near" 'bicycle' 'MK2KS_BICYCLE_RESULT pass=true '
        Add-Case "regression_v46_bicycle_verified_choke_side${side}_${victim}_near" 'choke' 'MK2KS_CHOKE_RESULT pass=true '
    }
    foreach ($mode in 'block','duck','duck_block','far','air','held','reversed','expired','wrong_button','airborne','with_block') {
        Add-Case "regression_v46_bicycle_verified_inputs_side${side}_kano_${mode}" 'bicycle' 'MK2KS_BICYCLE_RESULT pass=true '
    }
    foreach ($victim in 'kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax') {
        Add-Case "regression_v46_bicycle_verified_stock_side${side}_${victim}_near" 'bicycle' 'MK2KS_BICYCLE_RESULT pass=true '
    }
}
foreach ($fighter in 'kano','sonya') {
    foreach ($victim in 'kano','sonya') {
        foreach ($mode in 'near','corner_left','corner_right') {
            Add-Case "regression_v46_bicycle_verified_leg_${fighter}_vs_${victim}_${mode}" 'leg' 'MK2KS_LEG_RESULT pass=true '
        }
    }
    foreach ($mode in 'mirrors','jumps','lifecycle','wins','basics') {
        $marker=switch ($mode) {
            mirrors {'MK2KS_MIRROR_RESULT pass=true '}
            jumps {'MK2KS_JUMP_SUITE pass=true failures=0'}
            lifecycle {'MK2KS_LIFECYCLE_RESULT pass=true '}
            wins {'MK2KS_EXIT_RESULT pass=true '}
            basics {'MK2KS_BASIC_RESULT pass=true checks=20 errors=0'}
        }
        Add-Case "regression_v46_bicycle_verified_core_${mode}_${fighter}" $mode $marker
    }
}
Add-Case 'regression_v46_bicycle_verified_core_grid' 'grid' 'MK2KS_GRID_RESULT pass=true checks=31 failures=0'
Add-Case 'regression_v46_bicycle_verified_core_navigation' 'navigation' 'MK2KS_NAV_RESULT pass=true checks=10 failures=0'
if ($inventory.Count -ne 78 -or @($inventory.name | Sort-Object -Unique).Count -ne 78) {throw 'Invalid bicycle inventory'}
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
    foreach ($file in $result.file_hashes.PSObject.Properties) {
        if ((Get-FileHash -LiteralPath $file.Name).Hash -ne $file.Value) {throw "Case input changed: $($file.Name)"}
    }
    if ($case.family -notin 'grid','navigation','basics') {
        foreach ($marker in @('MK2KS_EXIT_RESULT pass=true ','MK2KS_DISPLAY_RESULT pass=true ',
            'MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0')) {
            if (-not $log.Contains($marker)) {throw "Missing $marker in $($case.name)"}
        }
    }
    if ($case.family -eq 'bicycle') {
        $positive=$case.name -match '_(near|air|held)$'
        $negative=$case.name -match '_(reversed|expired|wrong_button|airborne|with_block)$'
        $summary=[regex]::Match($log,'MK2KS_BICYCLE_RESULT pass=true [^\r\n]+').Value
        $expectedEntries=if ($negative) {0} else {1}
        if (-not $summary.Contains("entries=$expectedEntries ") -or -not $summary.Contains('errors=0')) {throw "Input observation incomplete: $($case.name)"}
        if ($positive) {
            $counts=[regex]::Match($summary,'ticks=(\d+) pair_checks=(\d+) releases=1 ')
            if (-not $counts.Success -or [int]$counts.Groups[1].Value -lt 16 -or [int]$counts.Groups[1].Value -gt 48 -or
                [int]$counts.Groups[2].Value -lt ([int]$counts.Groups[1].Value - 1)) {throw "Paired choreography observation incomplete: $($case.name)"}
        } elseif (-not $summary.Contains('ticks=0 pair_checks=0 releases=0 ')) {throw "Unexpected paired flight: $($case.name)"}
    }
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
$assets=Get-Content -LiteralPath "$candidate\asset-tests.log" -Raw
if ($assets -notmatch 'Ran 37 tests' -or $assets -notmatch '(?m)^OK\s*$' -or $assets -match 'FAILED|skipped=') {throw 'Asset checks incomplete'}
$reference=Get-Content -LiteralPath "$portRoot\diagnostic_v46_bicycle_assets\original-reference-audit.json" -Raw | ConvertFrom-Json
if (-not $reference.passed -or $reference.cases.Count -ne 6) {throw 'Original reference audit incomplete'}
foreach ($case in $reference.cases) {
    $log=Join-Path $portRoot "diagnostic_v46_mk3_bicycle_$($case.mode)\run.log"
    if ((Get-FileHash -LiteralPath $log).Hash -ne $case.log_sha256) {throw 'Original reference log changed'}
}
if ((Get-FileHash -LiteralPath "$portRoot\mame-mkp\mkport.exe").Hash -ne '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891') {throw 'Installed v42 changed'}
$releaseRoot='C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs'
$releases=@{
    'MK2-Kano-Sonya-v42-2026-09-05.zip'='1568AB02D4E639B4EE45F922F380597F680605A1FACD7DF352F7AE260DBB91A8'
    'MK2-Kano-Sonya-v44-WIP-2026-09-05.zip'='C72E5B40A01CC566167D41FD221B4170D0417A496C132B1B4E044B099EAB5C7F'
}
foreach ($name in $releases.Keys) {
    if ((Get-FileHash -LiteralPath (Join-Path $releaseRoot $name)).Hash -ne $releases[$name]) {throw "Released ZIP changed: $name"}
}
$manifest=Join-Path $candidate 'verification.json'
if (Test-Path -LiteralPath $manifest) {throw 'Refusing to overwrite completed verification'}
$support=@{}
foreach ($file in 'tools/build_mk2ks_mk3.py','tools/test_native_bicycle.py','tools/audit_bicycle_reference.py','mk3_bicycle_reference.lua','mk2ks_bicycle_test.lua','tools/run_native_bicycle.ps1') {
    $support[$file]=(Get-FileHash -LiteralPath (Join-Path $portRoot $file)).Hash
}
[ordered]@{executable_sha256=$expectedExe;payload_sha256=$expectedPayload;runtime_cases=78;asset_tests=37;
    cases=$verified;asset_log_sha256=(Get-FileHash -LiteralPath "$candidate\asset-tests.log").Hash;
    original_reference=$reference;supporting_source_hashes=$support;installed_cmd='Unchanged v42';release_zips=$releases;
    remaining=@('Bicycle KO/next-round, corners, interruption, projectile, boss and CPU semantics',
        'Full stock-body contact/artwork fidelity', 'Move-specific sound, original voices and announcements',
        'Full throw and victim behavior', 'Finishers', 'AI roster participation', 'Complete progression and endings',
        'Other-special comprehensive regression and full integration acceptance; no installed/release promotion')} |
    ConvertTo-Json -Depth 8 | Out-File -LiteralPath $manifest -Encoding utf8
Write-Output 'Verified 78 exact current-candidate runtime cases and 37 asset tests.'
