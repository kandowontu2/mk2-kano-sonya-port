param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kano','sonya')][string[]]$Fighters = @('sonya','kano'),
    # Fighters retains the original side convention: sonya=P1, kano=P2 grabber.
    [ValidateSet('kano','sonya','kung_lao','liu_kang','cage','baraka','kitana','mileena',
        'shang_tsung','raiden','sub_zero','reptile','scorpion','jax')]
    [string[]]$Victims = @('kano'),
    [ValidateSet('near','far','block','duck','duck_block','air','no_down','no_block','no_lp','extra_button','airborne','held','block2',
        'block_first','lp_first','down_last','block2_first','lp_first_block2','corner_left','corner_right')]
    [string[]]$Cases = @('near','far','block','duck','duck_block','air','no_down','no_block','no_lp','extra_button','airborne','held','block2'),
    [switch]$Trace
)
$ErrorActionPreference = 'Stop'
$portRoot = Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') { throw 'CasePrefix must be a simple directory prefix.' }
$Executable = (Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory = (Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload = Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$buildHash = (Get-FileHash -LiteralPath $Executable).Hash
$payloadHash = (Get-FileHash -LiteralPath $payload).Hash
$harness = Join-Path $portRoot 'mk2ks_selector_exit_test.lua'
$harnessHash = (Get-FileHash -LiteralPath $harness).Hash
& $Executable mk2ks -rompath "$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms" -verifyroms
if ($LASTEXITCODE -ne 0) { throw 'Selected executable/payload failed ROM verification.' }
$env:MK2KS_TEST_CONFIRM = 'hp'
$env:MK2KS_TEST_CONFIRM_HOLD = '8'
$env:MK2KS_TWO_PLAYER = '1'
$env:MK2KS_ASSERT_NATIVE_DISPLAY = '1'
$env:MK2KS_ASSERT_HUD_SHADOW = '1'
$env:MK2KS_TRACE_LEG = if ($Trace) { '1' } else { '0' }
foreach ($setting in @('MK2KS_ASSERT_LIFECYCLE','MK2KS_TEST_ROUND_WIN','MK2KS_TEST_ROUND_LOSS',
    'MK2KS_TEST_PROJECTILES','MK2KS_TRACE_TABLES','MK2KS_TRACE_REACTIONS','MK2KS_TRACE_BALL','MK2KS_TRACE_SQUARE')) {
    Set-Item -LiteralPath "Env:$setting" -Value '0'
}
foreach ($setting in @('MK2KS_TEST_SQUARE','MK2KS_TEST_BALL','MK2KS_BALL_HOLD')) {
    Set-Item -LiteralPath "Env:$setting" -Value ''
}
$failures = @()
Push-Location $portRoot
try {
    foreach ($fighter in $Fighters) {
      foreach ($victim in $Victims) {
        $env:MK2KS_LEG_SIDE = if ($fighter -eq 'sonya') { '1' } else { '2' }
        $env:MK2KS_TEST_FIGHTER = if ($fighter -eq 'sonya') { 'sonya' } else { $victim }
        $env:MK2KS_P2_FIGHTER = if ($fighter -eq 'sonya') { $victim } else { 'sonya' }
        foreach ($mode in $Cases) {
            if ((Get-FileHash -LiteralPath $Executable).Hash -ne $buildHash -or
                (Get-FileHash -LiteralPath $payload).Hash -ne $payloadHash -or
                (Get-FileHash -LiteralPath $harness).Hash -ne $harnessHash) { throw 'Candidate or harness changed during suite.' }
            $env:MK2KS_TEST_LEG = $mode
            $case = "${CasePrefix}_${fighter}_vs_${victim}_${mode}"
            $out = Join-Path $portRoot $case
            if (Test-Path -LiteralPath $out) { throw "Refusing to overwrite evidence: $out" }
            New-Item -ItemType Directory -Path $out | Out-Null
            $seconds = if ($mode -in @('corner_left','corner_right')) {65} else {45}
            & $Executable mk2ks -rompath "$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms" `
                -artpath "$portRoot\artwork" -skip_gameinfo -video none -sound none -nothrottle -str $seconds -snapsize 400x300 `
                -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
                -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
            $exitCode = $LASTEXITCODE
            $log = Get-Content -LiteralPath "$out\run.log" -Raw
            $passed = $exitCode -eq 0 -and $log -match 'MK2KS_LEG_RESULT pass=true ' -and
                $log -match 'MK2KS_EXIT_RESULT pass=true ' -and $log -match 'MK2KS_DISPLAY_RESULT pass=true ' -and
                $log -match 'MK2KS_HUD_SHADOW_RESULT pass=true ' -and
                $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' -and
                $log -notmatch '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]' -and
                (Get-FileHash -LiteralPath $Executable).Hash -eq $buildHash -and
                (Get-FileHash -LiteralPath $payload).Hash -eq $payloadHash -and
                (Get-FileHash -LiteralPath $harness).Hash -eq $harnessHash
            [ordered]@{case=$case;passed=$passed;victim=$victim;grabber_side=$(if($fighter -eq 'sonya'){1}else{2});executable_sha256=$buildHash;payload_sha256=$payloadHash;harness_sha256=$harnessHash;exit_code=$exitCode} |
                ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
            Write-Output "$case pass=$passed"
            if (-not $passed) { $failures += $case }
        }
      }
    }
} finally { Pop-Location }
if ($failures.Count) { throw "Failed leg-grab cases: $($failures -join ', ')" }
