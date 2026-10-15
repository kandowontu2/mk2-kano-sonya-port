param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('basics','jumps','lifecycle','recovery','wins','grid','navigation','mirrors')]
    [string[]]$Cases = @('basics','jumps','lifecycle','wins','grid','navigation'),
    [ValidateSet('kano','sonya')][string[]]$Fighters = @('kano','sonya')
)
$ErrorActionPreference = 'Stop'
$portRoot = Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') { throw 'CasePrefix must be a simple directory prefix.' }
$Executable = (Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory = (Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$romPath = "$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms"
$tracked = @($Executable, (Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'))
$scripts = @{
    basics = 'mk2ks_stateful_move_test.lua'; jumps = 'mk2ks_native_jump_test.lua'
    lifecycle = 'mk2ks_selector_exit_test.lua'; recovery = 'mk2ks_selector_exit_test.lua'
    wins = 'mk2ks_selector_exit_test.lua'
    grid = 'mk2ks_native_grid_test.lua'; navigation = 'mk2ks_selector_navigation_test.lua'
    mirrors = 'mk2ks_mirror_palette_test.lua'
}
$tracked += @($scripts.Values | Sort-Object -Unique | ForEach-Object { Join-Path $portRoot $_ })
$hashes = @{}
foreach ($file in $tracked) { $hashes[$file] = (Get-FileHash -LiteralPath $file).Hash }
function Assert-Unchanged {
    foreach ($file in $tracked) {
        if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) { throw "Build or harness changed: $file" }
    }
}
& $Executable mk2ks -rompath $romPath -verifyroms
if ($LASTEXITCODE -ne 0) { throw 'Selected executable/payload failed ROM verification.' }
$savedEnvironment = @{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object { $savedEnvironment[$_.Name] = $_.Value }
$failures = @()
Push-Location $portRoot
try {
    foreach ($mode in $Cases) {
        $sides = if ($mode -eq 'grid') { @('kano') } else { $Fighters }
        foreach ($fighter in $sides) {
            Assert-Unchanged
            Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
            $env:MK2KS_TEST_FIGHTER = $fighter
            $env:MK2KS_P2_FIGHTER = if ($fighter -eq 'kano') { 'sonya' } else { 'kano' }
            $env:MK2KS_TEST_CONFIRM = 'hp'
            $env:MK2KS_TEST_CONFIRM_HOLD = '8'
            $env:MK2KS_TWO_PLAYER = '1'
            $env:MK2KS_ASSERT_NATIVE_DISPLAY = '1'
            $env:MK2KS_ASSERT_HUD_SHADOW = '1'
            # Explicitly disable both old diagnostic memory-writing modes.
            $env:MK2KS_PIN_FIGHTERS = '0'
            $env:MK2KS_PROBE_NATIVE_ROSTER = '0'
            $expected = @('MK2KS_EXIT_RESULT pass=true ', 'MK2KS_DISPLAY_RESULT pass=true ',
                'MK2KS_HUD_SHADOW_RESULT pass=true ', 'MK2KS_STABILITY stalled_frames=0 trap_frames=0')
            switch ($mode) {
                basics {
                    $env:MK2KS_BASIC_ACTIONS = '1'; $env:MK2KS_TEST_MOVE = '0'
                    $expected = @('MK2KS_BASIC_RESULT pass=true checks=20 errors=0',
                        'MK2KS_MOVE_RESULT pass=true ', 'stalled_frames=0 trap_frames=0',
                        'MK2KS_ROSTER_RESULT roster_errors=0 identity_errors=0')
                }
                jumps { $expected += 'MK2KS_JUMP_SUITE pass=true failures=0' }
                mirrors {
                    $env:MK2KS_P2_FIGHTER = $fighter
                    $expected += 'MK2KS_MIRROR_RESULT pass=true '
                }
                lifecycle {
                    $env:MK2KS_TWO_PLAYER = '0'; $env:MK2KS_P2_FIGHTER = 'stock'
                    $env:MK2KS_ASSERT_LIFECYCLE = '1'; $env:MK2KS_TEST_ROUND_LOSS = '1'
                    # Passive CPU play does not guarantee a knockdown. The
                    # separate recovery case forces one with P2 uppercuts.
                    $env:MK2KS_LIFECYCLE_ALLOW_NO_RECOVERY = '1'
                    # The initial ladder and the post-loss return are separate
                    # native entries in this one-player lifecycle run.
                    $expected += @('MK2KS_LIFECYCLE_RESULT pass=true ', 'ladder_entries=2 ')
                }
                recovery {
                    # Script the second human player's uppercuts so the added
                    # fighter actually enters knockdown/get-up, unlike a
                    # passive input-only CPU match which may never do so.
                    $env:MK2KS_ASSERT_LIFECYCLE = '1'; $env:MK2KS_TEST_ROUND_LOSS = '1'
                    $expected += 'MK2KS_LIFECYCLE_RESULT pass=true '
                }
                wins { $env:MK2KS_TEST_ROUND_WIN = '1' }
                grid { $expected = @('MK2KS_GRID_RESULT pass=true checks=31 failures=0') }
                navigation {
                    $env:MK2KS_NAV_FIGHTER = $fighter
                    $expected = @('MK2KS_NAV_RESULT pass=true checks=10 failures=0')
                }
            }
            $case = if ($mode -eq 'grid') { "${CasePrefix}_${mode}" } else { "${CasePrefix}_${mode}_${fighter}" }
            $out = Join-Path $portRoot $case
            if (Test-Path -LiteralPath $out) { throw "Refusing to overwrite evidence: $out" }
            New-Item -ItemType Directory -Path $out | Out-Null
            $seconds = if ($mode -in @('grid','navigation','jumps')) { 45 } else { 65 }
            & $Executable mk2ks -rompath $romPath -artpath "$portRoot\artwork" -skip_gameinfo `
                -video none -sound none -nothrottle -str $seconds -snapsize 400x300 `
                -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
                -autoboot_script (Join-Path $portRoot $scripts[$mode]) 2>&1 |
                Out-File -LiteralPath "$out\run.log" -Encoding utf8
            $exitCode = $LASTEXITCODE
            Assert-Unchanged
            $log = Get-Content -LiteralPath "$out\run.log" -Raw
            $passed = $exitCode -eq 0 -and $log -notmatch '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]'
            foreach ($marker in $expected) { $passed = $passed -and $log.Contains($marker) }
            [ordered]@{ case=$case; passed=$passed; executable_sha256=$hashes[$Executable];
                payload_sha256=$hashes[$tracked[1]]; file_hashes=$hashes; exit_code=$exitCode;
                launch='Direct candidate executable; installed CMD unchanged' } |
                ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\result.json" -Encoding utf8
            Write-Output "$case pass=$passed"
            if (-not $passed) { $failures += $case }
        }
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach ($key in $savedEnvironment.Keys) { Set-Item -LiteralPath "Env:$key" -Value $savedEnvironment[$key] }
}
if ($failures.Count) { throw "Failed native roster cases: $($failures -join ', ')" }
