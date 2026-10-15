# Exact, bounded evidence inventory for the 441275AC boundary-state candidate.
# This is not full-roster acceptance and does not install or package the build.
$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$expectedExe='441275ACEAF434C5917F72781936E212D7C9786A40F1516F5FA5A992276DD7AB'
$expectedPayload='31B89318C7D9C6A15706063A1A953D80E5F426AF6EC980009B5040626CAE206B'
$cases=[System.Collections.Generic.List[object]]::new()
function Add-Case([string]$name,[string]$family,[string]$marker) {
    $cases.Add([pscustomobject]@{name=$name;family=$family;marker=$marker})
}
foreach ($mode in @('mirrors','jumps','lifecycle','wins','basics')) {
    foreach ($fighter in @('kano','sonya')) {
        $marker=switch ($mode) {
            mirrors {'MK2KS_MIRROR_RESULT pass=true '}
            jumps {'MK2KS_JUMP_SUITE pass=true failures=0'}
            lifecycle {'MK2KS_LIFECYCLE_RESULT pass=true '}
            wins {'MK2KS_EXIT_RESULT pass=true '}
            basics {'MK2KS_BASIC_RESULT pass=true checks=20 errors=0'}
        }
        Add-Case "regression_v43_edges_observed_${mode}_${fighter}" $mode $marker
    }
}
Add-Case 'regression_v43_edges_observed_grid' 'grid' 'MK2KS_GRID_RESULT pass=true checks=31 failures=0'
Add-Case 'regression_v43_edges_observed_navigation' 'navigation' 'MK2KS_NAV_RESULT pass=true checks=10 failures=0'
foreach ($side in 1,2) {
    $fighter=if ($side -eq 1) {'sonya'} else {'kano'}
    foreach ($victim in @('kano','sonya','kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax')) {
        foreach ($edge in @('left','right')) {
            Add-Case "regression_v43_edges_p${side}_${fighter}_vs_${victim}_corner_${edge}" 'corners' 'MK2KS_LEG_RESULT pass=true '
        }
    }
}
foreach ($fighter in @('kano','sonya')) {
    foreach ($mode in @('hit','block','miss','short','boundary','minimum','held','airborne','recharge','wrong_button')) {
        Add-Case "regression_v43_edges_ball_${fighter}_${mode}" 'cannonball' 'MK2KS_BALL_RESULT pass=true '
    }
    foreach ($mode in @('ground','air','block','air_block','far','reversed','expired','wrong_button','airborne','with_block')) {
        Add-Case "regression_v43_edges_square_${fighter}_${mode}" 'square-wave' 'MK2KS_SQUARE_RESULT pass=true '
    }
    foreach ($mode in @('native','legacy','chord','reversed','expired','wrong_button','airborne','with_block')) {
        Add-Case "regression_v43_edges_commands_${fighter}_${mode}" 'projectiles' 'MK2KS_PROJECTILES_RESULT pass=true '
    }
}
foreach ($mode in @('rounds','mash')) {
    foreach ($side in 1,2) { foreach ($victim in @('kano','sonya','kitana','sub_zero')) {
        $observer=if ($side -eq 2 -and $victim -in @('kitana','sub_zero')) {'_p2hud'} else {''}
        Add-Case "regression_v43_edges_leg_${mode}${observer}_side${side}_${victim}" 'leg-rounds' 'MK2KS_LEG_LIFECYCLE_RESULT pass=true '
    } }
}
foreach ($side in 1,2) { foreach ($victim in @('kano','sonya')) {
    $delay=3-$side
    Add-Case "regression_v43_edges_leg_interrupt_side${side}_${victim}_delay${delay}" 'startup-interruption' 'MK2KS_LEG_INTERRUPT_RESULT pass=true '
} }
if ($cases.Count -ne 144 -or @($cases.name | Sort-Object -Unique).Count -ne 144) { throw 'Incorrect evidence inventory.' }
$results=@()
foreach ($case in $cases) {
    $dir=Join-Path $portRoot $case.name
    $result=Get-Content -LiteralPath (Join-Path $dir 'result.json') -Raw | ConvertFrom-Json
    $log=Get-Content -LiteralPath (Join-Path $dir 'run.log') -Raw
    if ($result.case -ne $case.name -or -not $result.passed -or $result.exit_code -ne 0 -or
        $result.executable_sha256 -ne $expectedExe -or $result.payload_sha256 -ne $expectedPayload -or
        -not $log.Contains($case.marker) -or $log -match '(?i)fatal error|exception at|access violation|error in emu') {
        throw "Invalid or failed evidence: $($case.name)"
    }
    if ($case.family -notin @('grid','navigation','basics')) {
        foreach ($marker in @('MK2KS_EXIT_RESULT pass=true ','MK2KS_DISPLAY_RESULT pass=true ',
            'MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0')) {
            if (-not $log.Contains($marker)) { throw "Missing $marker in $($case.name)" }
        }
    }
    if ($case.family -eq 'basics') {
        foreach ($marker in @('MK2KS_MOVE_RESULT pass=true ','stalled_frames=0 trap_frames=0',
            'MK2KS_ROSTER_RESULT roster_errors=0 identity_errors=0')) {
            if (-not $log.Contains($marker)) { throw "Missing $marker in $($case.name)" }
        }
    }
    $results += [ordered]@{family=$case.family;result=$result;log_sha256=(Get-FileHash -LiteralPath (Join-Path $dir 'run.log')).Hash}
}
$fixedHashes=@{
    'diagnostic_v43_edge_candidate\mkport_edges.exe'=$expectedExe
    'diagnostic_v43_jump_candidate\roms\mk2ks\mk2ks.mdata'=$expectedPayload
    'mame-mkp\mkport.exe'='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    'roms_v22_clean\mk2ks\mk2ks.mdata'='2F29937E0144FE54E490BB6D6C0BEBB99496CDF551F228C38F975F7EFEED31FF'
    'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs\MK2-Kano-Sonya-v42-2026-09-05.zip'='1568AB02D4E639B4EE45F922F380597F680605A1FACD7DF352F7AE260DBB91A8'
}
foreach ($path in $fixedHashes.Keys) {
    $absolute=if ([System.IO.Path]::IsPathRooted($path)) {$path} else {Join-Path $portRoot $path}
    if ((Get-FileHash -LiteralPath $absolute).Hash -ne $fixedHashes[$path]) { throw "Artifact changed: $path" }
}
$assetLog=Join-Path $portRoot 'diagnostic_v43_edge_candidate\asset-tests.log'
if (Test-Path -LiteralPath $assetLog) { throw "Refusing to overwrite evidence: $assetLog" }
Push-Location $portRoot
try {
    $assetOutput=& 'C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe' -m unittest discover -s tools -p 'test_*.py' -v 2>&1
    $assetExit=$LASTEXITCODE
    $assetOutput | Out-File -LiteralPath $assetLog -Encoding utf8
    $assetText=Get-Content -LiteralPath $assetLog -Raw
    if ($assetExit -ne 0 -or $assetText -notmatch 'Ran 14 tests' -or $assetText -notmatch '(?m)^OK\s*$') {
        throw 'Asset tests did not pass all fourteen cases.'
    }
} finally { Pop-Location }
$out=Join-Path $portRoot 'diagnostic_v43_edge_candidate\verification.json'
if (Test-Path -LiteralPath $out) { throw "Refusing to overwrite evidence: $out" }
$sourceHashes=@{}
foreach ($path in @('mk2ks_selector_exit_test.lua','mk2ks_leg_lifecycle_test.lua','mk2ks_leg_interrupt_test.lua',
    'mame-mkp\src\mame\midway\midtunit_m.cpp','mame-mkp\src\devices\cpu\tms34010\tms34010.cpp')) {
    $sourceHashes[$path]=(Get-FileHash -LiteralPath (Join-Path $portRoot $path)).Hash
}
[ordered]@{status='Partial candidate verification; NOT full port acceptance';
    executable_sha256=$expectedExe;payload_sha256=$expectedPayload;total=$results.Count;
    asset_tests=14;asset_test_log_sha256=(Get-FileHash -LiteralPath $assetLog).Hash;
    source_hashes_at_aggregation=$sourceHashes;installed_v42_and_release_zip_unchanged=$true;
    remaining=@('Interruption by a live projectile during paired motion','Boss rejection and late finish-state leg behavior',
        'Further reselect/join/morph paths','Remaining moves, voices, sounds, finishers, AI and progression');cases=$results} |
    ConvertTo-Json -Depth 8 | Out-File -LiteralPath $out -Encoding utf8
Write-Output "Verified $($results.Count) exact candidate cases; installed v42 and release ZIP unchanged."
