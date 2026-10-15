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
    foreach ($mode in 'near','block','duck','duck_block','far','air','held','reversed','expired','wrong_button','airborne','with_block') {
        Add-Case "regression_v46_bicycle_inputfix_commands_side${side}_kano_${mode}" 'bicycle' 'MK2KS_BICYCLE_RESULT pass=true '
    }
    foreach ($victim in 'sonya','kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax') {
        Add-Case "regression_v46_bicycle_inputfix_victims_side${side}_${victim}_near" 'bicycle' 'MK2KS_BICYCLE_RESULT pass=true '
    }
    foreach ($victim in 'kano','sonya','kitana','sub_zero') {
        Add-Case "regression_v46_bicycle_rounds_inputfix_side${side}_${victim}" 'bicycle_rounds' 'MK2KS_BICYCLE_LIFECYCLE_RESULT pass=true '
    }
    foreach ($victim in 'kano','sonya') {
        $delay=10-$side
        Add-Case "regression_v46_bicycle_interrupt_verified_side${side}_${victim}_delay${delay}" 'bicycle_interrupt' 'MK2KS_BICYCLE_INTERRUPT_RESULT pass=true '
        Add-Case "regression_v46_bicycle_inputfix_choke_side${side}_${victim}_near" 'choke' 'MK2KS_CHOKE_RESULT pass=true '
    }
}
foreach ($fighter in 'kano','sonya') {
    foreach ($victim in 'kano','sonya') {
        foreach ($mode in 'near','corner_left','corner_right') {
            Add-Case "regression_v46_bicycle_inputfix_leg_${fighter}_vs_${victim}_${mode}" 'leg' 'MK2KS_LEG_RESULT pass=true '
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
        Add-Case "regression_v46_bicycle_inputfix_core_${mode}_${fighter}" $mode $marker
    }
}
Add-Case 'regression_v46_bicycle_inputfix_core_grid' 'grid' 'MK2KS_GRID_RESULT pass=true checks=31 failures=0'
Add-Case 'regression_v46_bicycle_inputfix_core_navigation' 'navigation' 'MK2KS_NAV_RESULT pass=true checks=10 failures=0'
if ($inventory.Count -ne 90 -or @($inventory.name | Sort-Object -Unique).Count -ne 90) {throw 'Invalid lifecycle inventory'}
$verified=@()
foreach ($case in $inventory) {
    $out=Join-Path $portRoot $case.name
    $result=Get-Content -LiteralPath "$out\result.json" -Raw | ConvertFrom-Json
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    if ($result.case -ne $case.name -or -not $result.passed -or $result.exit_code -ne 0 -or
        $result.executable_sha256 -ne $expectedExe -or $result.payload_sha256 -ne $expectedPayload -or
        -not $log.Contains($case.marker) -or $log -match '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]') {
        throw "Invalid evidence: $($case.name)"
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
        $summary=[regex]::Match($log,'MK2KS_BICYCLE_RESULT pass=true [^\r\n]+').Value
        $negative=$case.name -match '_(reversed|expired|wrong_button|airborne|with_block)$'
        $expectedEntries=if ($negative) {0} else {1}
        if (-not $summary.Contains("entries=$expectedEntries ") -or -not $summary.Contains('errors=0')) {throw 'Incomplete input evidence'}
        if ($case.name -match '_(near|air|held)$') {
            $counts=[regex]::Match($summary,'ticks=(\d+) pair_checks=(\d+) releases=1 ')
            if (-not $counts.Success -or [int]$counts.Groups[1].Value -lt 16 -or [int]$counts.Groups[1].Value -gt 48 -or
                [int]$counts.Groups[2].Value -lt ([int]$counts.Groups[1].Value-1)) {throw 'Incomplete paired motion'}
        } elseif (-not $summary.Contains('ticks=0 pair_checks=0 releases=0 ')) {throw 'Unexpected paired motion'}
    } elseif ($case.family -eq 'bicycle_rounds') {
        $cycles=[regex]::Matches($log,'MK2KS_BICYCLE_LIFECYCLE_CYCLE number=(\d+) before=(\d+) after=(\d+) entries=1 ticks=(\d+) releases=1')
        if ($cycles.Count -ne 9 -or $log -notmatch 'cycles=9 huds=\d+ wins=[1-9]\d* next_round=[1-9]\d* palettes=\d+ errors=0') {throw 'Incomplete KO/next-round evidence'}
        for ($index=0;$index -lt 9;$index++) {
            $before=if ($index -eq 8) {161} else {161-$index*22}
            $after=[Math]::Max(0,$before-22)
            $cycle=$cycles[$index]
            if ([int]$cycle.Groups[1].Value -ne ($index+1) -or [int]$cycle.Groups[2].Value -ne $before -or
                [int]$cycle.Groups[3].Value -ne $after -or [int]$cycle.Groups[4].Value -lt 16 -or [int]$cycle.Groups[4].Value -gt 48) {
                throw 'Wrong repeated action damage/cadence'
            }
        }
    } elseif ($case.family -eq 'bicycle_interrupt') {
        $entry=[regex]::Match($log,'MK2KS_BICYCLE_INTERRUPT_EVENT kind=entries frame=(\d+)')
        $hit=[regex]::Match($log,'MK2KS_BICYCLE_INTERRUPT_HIT frame=(\d+)')
        if (-not $entry.Success -or -not $hit.Success -or [int]$hit.Groups[1].Value -le [int]$entry.Groups[1].Value -or
            -not $log.Contains('RECOVERED entries=1 collisions=0 ticks=0 releases=0 health=121,161') -or
            $log -notmatch 'entries=2 collisions=\d+ ticks=48 releases=1 palettes=8 errors=0') {throw 'Counter did not interrupt an active startup and cleanly retry'}
    } elseif ($case.family -eq 'basics') {
        foreach ($marker in @('MK2KS_MOVE_RESULT pass=true ','stalled_frames=0 trap_frames=0','MK2KS_ROSTER_RESULT roster_errors=0 identity_errors=0')) {
            if (-not $log.Contains($marker)) {throw 'Incomplete basic identity/stability'}
        }
    }
    $verified+=[ordered]@{family=$case.family;result=$result;log_sha256=(Get-FileHash -LiteralPath "$out\run.log").Hash;
        result_sha256=(Get-FileHash -LiteralPath "$out\result.json").Hash}
}
$build=Get-Content -LiteralPath "$candidate\build-info.json" -Raw | ConvertFrom-Json
if ((Get-FileHash -LiteralPath "$candidate\mkport_candidate.exe").Hash -ne $expectedExe) {throw 'Candidate changed'}
foreach ($file in $build.input_hashes.PSObject.Properties) {
    if ((Get-FileHash -LiteralPath $file.Name).Hash -ne $file.Value) {throw 'Build source/input changed'}
}
$assets=Get-Content -LiteralPath "$candidate\lifecycle-asset-tests.log" -Raw
if ($assets -notmatch 'Ran 38 tests' -or $assets -notmatch '(?m)^OK\s*$' -or $assets -match 'FAILED|skipped=') {throw 'Asset/input checks incomplete'}
$preserved=@{
    "$portRoot\mame-mkp\mkport.exe"='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs\MK2-Kano-Sonya-v42-2026-09-05.zip'='1568AB02D4E639B4EE45F922F380597F680605A1FACD7DF352F7AE260DBB91A8'
    'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs\MK2-Kano-Sonya-v44-WIP-2026-09-05.zip'='C72E5B40A01CC566167D41FD221B4170D0417A496C132B1B4E044B099EAB5C7F'
}
foreach ($file in $preserved.Keys) {if ((Get-FileHash -LiteralPath $file).Hash -ne $preserved[$file]) {throw 'Installed/release artifact changed'}}
$manifest=Join-Path $candidate 'lifecycle-verification.json'
if (Test-Path -LiteralPath $manifest) {throw 'Refusing to overwrite completed verification'}
$support=@{}
foreach ($file in 'mk2ks_selector_exit_test.lua','mk2ks_bicycle_lifecycle_test.lua','mk2ks_bicycle_interrupt_test.lua',
    'tools/test_selector_input_driver.py','tools/run_bicycle_lifecycle.ps1','tools/run_bicycle_interrupt.ps1','tools/verify_bicycle_lifecycle.ps1') {
    $support[$file]=(Get-FileHash -LiteralPath (Join-Path $portRoot $file)).Hash
}
[ordered]@{executable_sha256=$expectedExe;payload_sha256=$expectedPayload;runtime_cases=90;asset_tests=37;input_driver_tests=1;
    cases=$verified;asset_log_sha256=(Get-FileHash -LiteralPath "$candidate\lifecycle-asset-tests.log").Hash;
    supporting_source_hashes=$support;preserved_artifacts=$preserved;
    change='Shared test driver now releases P2 High Kick. No gameplay, payload, installed build or release changes.';
    remaining=@('Dedicated bicycle corners, projectile, boss and CPU semantics','Move-specific impact feedback and original voices/announcements',
        'Full contact/throw/victim artwork fidelity','Finishers and AI roster participation','Full progression/endings and final integration acceptance')} |
    ConvertTo-Json -Depth 9 | Out-File -LiteralPath $manifest -Encoding utf8
Write-Output 'Verified 90 exact current-candidate runtime cases, 37 asset tests and 1 input-driver test.'
