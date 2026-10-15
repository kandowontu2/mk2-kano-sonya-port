$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$expectedExe='B1DA05A999230413182123E87DF905D252B9BB7C7F0A4B6B09A8FEAEC13043FF'
$expectedPayload='91001C2E6551CB850F919971D67806DE31D5F34D97C6CE0D9764B4F367F19DB3'
$candidate=Join-Path $portRoot 'diagnostic_v44_feedback_candidate'
$inventory=[Collections.Generic.List[object]]::new()
function Add-Case([string]$Name,[string]$Family,[string]$Marker) {
    $inventory.Add([pscustomobject]@{name=$Name;family=$Family;marker=$Marker})
}
foreach ($side in 1,2) {
    foreach ($mode in 'near','far','block','duck_block','air') {
        Add-Case "regression_v44_feedback_sonya_side${side}_sonya_${mode}" 'feedback' 'MK2KS_BLADE_FEEDBACK_RESULT pass=true '
    }
    foreach ($mode in 'near','block','duck_block','far') {
        Add-Case "regression_v44_feedback_mirror_side${side}_kano_${mode}" 'feedback' 'MK2KS_BLADE_FEEDBACK_RESULT pass=true '
    }
    Add-Case "regression_v44_feedback_interrupt_side${side}_sonya_interrupt" 'interrupt' 'MK2KS_BLADE_INTERRUPT_RESULT pass=true '
    foreach ($mode in 'native','held','reversed','expired','wrong_button','airborne','with_block') {
        Add-Case "regression_v44_feedback_inputs_side${side}_sonya_${mode}" 'inputs' 'MK2KS_BLADE_COMMAND_RESULT pass=true '
    }
}
foreach ($fighter in 'kano','sonya') {
    foreach ($mode in 'native','legacy','chord','reversed','expired','wrong_button','airborne','with_block') {
        Add-Case "regression_v44_feedback_commands_${fighter}_${mode}" 'commands' 'MK2KS_PROJECTILES_RESULT pass=true '
    }
    foreach ($mode in 'hit','block','miss','short','boundary','minimum','held','airborne','recharge','wrong_button') {
        Add-Case "regression_v44_feedback_ball_${fighter}_${mode}" 'ball' 'MK2KS_BALL_RESULT pass=true '
    }
    foreach ($mode in 'ground','air','block','air_block','far','reversed','expired','wrong_button','airborne','with_block') {
        Add-Case "regression_v44_feedback_square_${fighter}_${mode}" 'square' 'MK2KS_SQUARE_RESULT pass=true '
    }
    foreach ($mode in 'mirrors','jumps','lifecycle','wins','basics') {
        $marker=switch ($mode) {
            mirrors {'MK2KS_MIRROR_RESULT pass=true '}
            jumps {'MK2KS_JUMP_SUITE pass=true failures=0'}
            lifecycle {'MK2KS_LIFECYCLE_RESULT pass=true '}
            wins {'MK2KS_EXIT_RESULT pass=true '}
            basics {'MK2KS_BASIC_RESULT pass=true checks=20 errors=0'}
        }
        Add-Case "regression_v44_feedback_core_${mode}_${fighter}" $mode $marker
    }
}
Add-Case 'regression_v44_feedback_core_grid' 'grid' 'MK2KS_GRID_RESULT pass=true checks=31 failures=0'
Add-Case 'regression_v44_feedback_core_navigation' 'navigation' 'MK2KS_NAV_RESULT pass=true checks=10 failures=0'
if ($inventory.Count -ne 102 -or ($inventory.name | Sort-Object -Unique).Count -ne 102) { throw 'Invalid exact test inventory' }
$results=@()
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
            if (-not $log.Contains($marker)) { throw "Missing $marker in $($case.name)" }
        }
    }
    if ($case.family -eq 'feedback') {
        foreach ($marker in @('MK2KS_BLADE_RESULT pass=true ',
            'pose_checks=38 palette_checks=38 alignment_checks=10 errors=0','swishes=1 ')) {
            if (-not $log.Contains($marker)) { throw "Incomplete blade timing/feedback: $($case.name)" }
        }
        $hit=$case.name -match '_(near|air)$'
        $marker=if ($hit) {'requests=1 starts=1 allocations=8 insertions=8 cleanups=8 palette_checks=112 swishes=1 cuts=1 grunts=1 deliveries=2'} else {'requests=0 starts=0 allocations=0 insertions=0 cleanups=0 palette_checks=0 swishes=1 cuts=0 grunts=0 deliveries=1'}
        if (-not $log.Contains($marker)) { throw "Incomplete native blood/DCS transmission evidence: $($case.name)" }
    }
    if ($case.family -eq 'interrupt' -and -not $log.Contains('entries=2 strikes=1 creates=2 errors=0')) {
        throw "Incomplete actual interruption and retry: $($case.name)"
    }
    if ($case.family -eq 'inputs') {
        $marker=if ($case.name -match '_(native|held)$') {'entries=1 strikes=1 creates=1 blood=1 errors=0'} else {'entries=0 strikes=0 creates=0 blood=0 errors=0'}
        if (-not $log.Contains($marker)) { throw "Incomplete input rejection/repeat evidence: $($case.name)" }
    }
    if ($case.family -eq 'basics') {
        foreach ($marker in @('MK2KS_MOVE_RESULT pass=true ','stalled_frames=0 trap_frames=0',
            'MK2KS_ROSTER_RESULT roster_errors=0 identity_errors=0')) {
            if (-not $log.Contains($marker)) { throw "Missing $marker in $($case.name)" }
        }
    }
    $results+=[ordered]@{family=$case.family;result=$result;log_sha256=(Get-FileHash -LiteralPath "$out\run.log").Hash}
}
$fixed=@{
    'diagnostic_v44_feedback_candidate\mkport_feedback.exe'=$expectedExe
    'diagnostic_v44_blade_candidate\roms\mk2ks\mk2ks.mdata'=$expectedPayload
    'diagnostic_v44_blade_candidate\mkport_blade.exe'='A3479747FBE10CE8F191CF2EA40FE8E6F949FA46FBB02984B84839B832401AF0'
    'mame-mkp\src\mame\midway\midtunit_m.cpp'='7D3DA1619783A5C4126913A7C91487237A7AD2B9E28C069F359854B752567A69'
    'mame-mkp\mkport.exe'='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    'roms_v22_clean\mk2ks\mk2ks.mdata'='2F29937E0144FE54E490BB6D6C0BEBB99496CDF551F228C38F975F7EFEED31FF'
    'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs\MK2-Kano-Sonya-v42-2026-09-05.zip'='1568AB02D4E639B4EE45F922F380597F680605A1FACD7DF352F7AE260DBB91A8'
    'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs\MK2-Kano-Sonya-v44-WIP-2026-09-05.zip'='C72E5B40A01CC566167D41FD221B4170D0417A496C132B1B4E044B099EAB5C7F'
}
foreach ($path in $fixed.Keys) {
    $absolute=if ([IO.Path]::IsPathRooted($path)) {$path} else {Join-Path $portRoot $path}
    if ((Get-FileHash -LiteralPath $absolute).Hash -ne $fixed[$path]) { throw "Artifact changed: $path" }
}
$assetLog=Join-Path $candidate 'asset-tests-final.log'
$manifest=Join-Path $candidate 'verification.json'
if ((Test-Path -LiteralPath $assetLog) -or (Test-Path -LiteralPath $manifest)) { throw 'Do not overwrite existing verification evidence' }
Push-Location $portRoot
try {
    & 'C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe' -m unittest discover -s tools -p 'test_*.py' -v 2>&1 |
        Out-File -LiteralPath $assetLog -Encoding utf8
    if ($LASTEXITCODE -ne 0) { throw 'Asset tests failed' }
} finally { Pop-Location }
$assetText=Get-Content -LiteralPath $assetLog -Raw
if ($assetText -notmatch 'Ran 20 tests' -or $assetText -notmatch '(?m)^OK\s*$') { throw 'Expected twenty asset tests' }
$sourceHashes=@{}
foreach ($path in @('mk2ks_selector_exit_test.lua','mk2ks_blade_test.lua','mk2ks_blade_interrupt_test.lua',
    'mk2ks_blade_feedback_test.lua','mk2ks_blade_command_test.lua','tools\run_blade.ps1',
    'tools\build_mk2ks_mk3.py','tools\build_native_blade.py','tools\test_native_blade.py',
    'mame-mkp\src\mame\midway\midtunit_m.cpp','mame-mkp\src\mame\midway\midtunit.cpp')) {
    $sourceHashes[$path]=(Get-FileHash -LiteralPath (Join-Path $portRoot $path)).Hash
}
[ordered]@{status='Native blade feedback and command milestone; NOT full move or port acceptance';
    executable_sha256=$expectedExe;payload_sha256=$expectedPayload;total=$results.Count;asset_tests=20;
    asset_test_log_sha256=(Get-FileHash -LiteralPath $assetLog).Hash;source_hashes_at_aggregation=$sourceHashes;
    installed_v42_and_both_release_zips_unchanged=$true;cases=$results;
    remaining=@('Repeated blade/KO/next-round and corner/full-victim testing','Operator blood-disable runtime coverage',
        'Full leg-grab suite rerun on current build','Original character-specific voices, remaining moves/finishers, AI and complete progression')} |
    ConvertTo-Json -Depth 8 | Out-File -LiteralPath $manifest -Encoding utf8
Write-Output "Verified $($results.Count) exact feedback candidate cases and twenty asset tests; installed build and both releases unchanged."
