param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet(1,2)][int[]]$Sides=@(1,2),
    [ValidateRange(50,140)][int]$ApproachGap=68,
    [ValidateSet('near','block','duck','duck_block','far','air','held','reversed','expired','wrong_button','airborne','with_block')][string[]]$Modes=@('near'),
    [ValidateSet('kano','sonya','kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax')][string[]]$Victims=@('sonya')
)
$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence prefix.'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$romPath="$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms"
$harness=Join-Path $portRoot 'mk2ks_choke_test.lua'
$tracked=@($Executable,(Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'),$harness,
    (Join-Path $portRoot 'mk2ks_selector_exit_test.lua'))
$hashes=@{}
foreach ($file in $tracked) {$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
function Assert-Unchanged {
    foreach ($file in $tracked) {
        if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Build or harness changed: $file"}
    }
}
& $Executable mk2ks -rompath $romPath -verifyroms
if ($LASTEXITCODE -ne 0) {throw 'Selected build failed ROM verification.'}
$savedEnvironment=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$savedEnvironment[$_.Name]=$_.Value}
$failures=@()
Push-Location $portRoot
try {
    foreach ($side in $Sides) {foreach ($victim in $Victims) {foreach ($mode in $Modes) {
        Assert-Unchanged
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=if ($side -eq 1) {'kano'} else {$victim}
        $env:MK2KS_P2_FIGHTER=if ($side -eq 1) {$victim} else {'kano'}
        $env:MK2KS_CHOKE_SIDE="$side";$env:MK2KS_CHOKE_MODE=$mode
        $env:MK2KS_CHOKE_APPROACH_GAP="$ApproachGap"
        $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2KS_PIN_FIGHTERS='0';$env:MK2KS_PROBE_NATIVE_ROSTER='0'
        $case="${CasePrefix}_side${side}_${victim}_${mode}"
        $out=Join-Path $portRoot $case
        if (Test-Path -LiteralPath $out) {throw "Refusing to overwrite evidence: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath $romPath -artpath "$portRoot\artwork" -skip_gameinfo `
            -video none -sound none -nothrottle -str 60 -snapsize 400x300 `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        Assert-Unchanged
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $passed=$exitCode -eq 0 -and $log -notmatch '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]'
        foreach ($marker in @('MK2KS_CHOKE_RESULT pass=true ','MK2KS_EXIT_RESULT pass=true ',
            'MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ',
            'MK2KS_STABILITY stalled_frames=0 trap_frames=0')) {$passed=$passed -and $log.Contains($marker)}
        [ordered]@{case=$case;passed=$passed;side=$side;victim=$victim;mode=$mode;approach_gap=$ApproachGap;
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$tracked[1]];
            file_hashes=$hashes;exit_code=$exitCode} | ConvertTo-Json -Depth 4 |
            Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed"
        if (-not $passed) {$failures+=$case}
    }}}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach ($key in $savedEnvironment.Keys) {Set-Item -LiteralPath "Env:$key" -Value $savedEnvironment[$key]}
}
if ($failures.Count) {throw "Failed native choke cases: $($failures -join ', ')"}
