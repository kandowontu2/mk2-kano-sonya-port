param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet(1,2)][int[]]$Sides=@(1,2),
    [ValidateSet('near','block','duck_block','duck','far','air','interrupt','native','held','reversed','expired','wrong_button','airborne','with_block')][string[]]$Modes=@('near','block','duck_block','far','air'),
    [ValidateSet('sonya','kano','kitana','sub_zero')][string]$Victim='sonya',
    [switch]$Interrupt,
    [switch]$Feedback,
    [switch]$Commands
)
$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') { throw 'Use a simple evidence prefix.' }
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
if (([int]$Interrupt.IsPresent+[int]$Feedback.IsPresent+[int]$Commands.IsPresent) -gt 1) { throw 'Select only one specialized observer.' }
$harness=Join-Path $portRoot $(if ($Interrupt) {'mk2ks_blade_interrupt_test.lua'} elseif ($Feedback) {'mk2ks_blade_feedback_test.lua'} elseif ($Commands) {'mk2ks_blade_command_test.lua'} else {'mk2ks_blade_test.lua'})
if ($Interrupt) { $Modes=@('interrupt') }
elseif ($Modes -contains 'interrupt') { throw 'Use -Interrupt for the interruption harness.' }
if ($Commands) {
    foreach ($mode in $Modes) { if ($mode -notin @('native','held','reversed','expired','wrong_button','airborne','with_block')) { throw 'Choose command-test modes explicitly.' } }
} elseif (-not $Interrupt) {
    foreach ($mode in $Modes) { if ($mode -notin @('near','block','duck_block','duck','far','air')) { throw 'Use -Commands for command-test modes.' } }
}
$tracked=@($Executable,(Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'),$harness,
    (Join-Path $portRoot 'mk2ks_selector_exit_test.lua'))
if ($Feedback) { $tracked+=Join-Path $portRoot 'mk2ks_blade_test.lua' }
$hashes=@{}
foreach ($file in $tracked) { $hashes[$file]=(Get-FileHash -LiteralPath $file).Hash }
function Assert-Unchanged {
    foreach ($file in $tracked) {
        if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) { throw "Build or harness changed: $file" }
    }
}
$romPath="$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms"
& $Executable mk2ks -rompath $romPath -verifyroms
if ($LASTEXITCODE -ne 0) { throw 'Selected build failed ROM verification.' }
$savedEnvironment=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object { $savedEnvironment[$_.Name]=$_.Value }
$failures=@()
Push-Location $portRoot
try {
    foreach ($side in $Sides) { foreach ($mode in $Modes) {
        Assert-Unchanged
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=if ($side -eq 1) {'kano'} else {$Victim}
        $env:MK2KS_P2_FIGHTER=if ($side -eq 1) {$Victim} else {'kano'}
        $env:MK2KS_BLADE_SIDE="$side"; $env:MK2KS_BLADE_MODE=$mode
        $env:MK2KS_TEST_CONFIRM='hp'; $env:MK2KS_TEST_CONFIRM_HOLD='8'; $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'; $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $case="${CasePrefix}_side${side}_${Victim}_${mode}"
        $out=Join-Path $portRoot $case
        if (Test-Path -LiteralPath $out) { throw "Refusing to overwrite evidence: $out" }
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath $romPath -artpath "$portRoot\artwork" -skip_gameinfo `
            -video none -sound none -nothrottle -str 65 -snapsize 800x600 `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        Assert-Unchanged
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $passed=$exitCode -eq 0 -and $log -notmatch '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]'
        $moveMarker=if ($Interrupt) {'MK2KS_BLADE_INTERRUPT_RESULT pass=true '} elseif ($Commands) {'MK2KS_BLADE_COMMAND_RESULT pass=true '} else {'MK2KS_BLADE_RESULT pass=true '}
        foreach ($marker in @($moveMarker,'MK2KS_EXIT_RESULT pass=true ',
            'MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ',
            'MK2KS_STABILITY stalled_frames=0 trap_frames=0')) { $passed=$passed -and $log.Contains($marker) }
        if ($Feedback) { $passed=$passed -and $log.Contains('MK2KS_BLADE_FEEDBACK_RESULT pass=true ') }
        [ordered]@{case=$case;passed=$passed;side=$side;mode=$mode;victim=$Victim;
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$tracked[1]];
            file_hashes=$hashes;exit_code=$exitCode} |
            ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed"
        if (-not $passed) { $failures+=$case }
    } }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach ($key in $savedEnvironment.Keys) { Set-Item -LiteralPath "Env:$key" -Value $savedEnvironment[$key] }
}
if ($failures.Count) { throw "Failed blade cases: $($failures -join ', ')" }
