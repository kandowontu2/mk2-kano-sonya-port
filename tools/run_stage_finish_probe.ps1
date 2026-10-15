param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kano','sonya')][string[]]$Fighters=@('kano','sonya'),
    [int]$Seconds=205
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence prefix.'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_finish_state_trace.lua'
$ladderHarness=Join-Path $root 'mk2ks_cpu_ladder_trace.lua'
$baseHarness=Join-Path $root 'mk2ks_selector_exit_test.lua'
$tracked=@($Executable,$payload,$harness,$ladderHarness,$baseHarness,$PSCommandPath)
$hashes=@{}
foreach ($path in $tracked) {$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $root
try {
    foreach ($fighter in $Fighters) {
        foreach ($path in $tracked) {
            if ((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]) {
                throw "Input changed: $path"
            }
        }
        Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
            Remove-Item
        $env:MK2KS_TEST_FIGHTER=$fighter
        $env:MK2KS_P2_FIGHTER='stock'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='0'
        $env:MK2KS_TEST_ROUND_WIN='1'
        $env:MK2KS_DIAGNOSTIC_ALL_STAGES='1'
        $env:MK2KS_DIAGNOSTIC_CPU_HEALTH='1'
        $env:MK2KS_DIAGNOSTIC_P1_REGEN='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2_TRACE_LADDER='1'
        $env:MK2_TRACE_STAGE_FINISH=$fighter
        $env:MK2_TRACE_INPUT_ONLY_APPROACH='1'
        $env:MK2_TRACE_STAGE_GATE='1'
        $env:MK2_TRACE_FINISH_SNAPSHOTS='1'
        $case="${CasePrefix}_${fighter}"
        $out=Join-Path $root $case
        if (Test-Path -LiteralPath $out) {throw "Refusing to overwrite evidence: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        foreach ($path in $tracked) {
            if ((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]) {
                throw "Input changed: $path"
            }
        }
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $parser=if ($fighter -eq 'kano') {'FFFAA200'} else {'FFFAA400'}
        $winner=if ($fighter -eq 'kano') {'0011'} else {'0012'}
        $gate=[regex]::Match($log,
            'MK2_STAGE_GATE frame=(\d+) age=\d+ arena=1 at=FF8773A0 ')
        $approach=[regex]::Match($log,
            'MK2_FINISH_INPUT_APPROACH frame=(\d+) age=\d+ gap=(\d+)')
        $snapshots=@(Get-ChildItem -LiteralPath "$out\snap\mk2ks" -Filter '*.png' -ErrorAction SilentlyContinue).Count
        $passed=$exitCode -eq 0 -and $approach.Success -and
            [int]$approach.Groups[2].Value -le 65 -and
            $gate.Success -and
            $log.Contains("at=$parser ") -and
            $log.Contains('at=FF876D20 ') -and
            $log -match 'MK2_FINISH_STATE frame=\d+ arena=1 mode=3 stage=1 ' -and
            $log -match "MK2KS_NATIVE_WIN frame=\d+ winner=$winner " -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
            $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
            $log.Contains('MK2KS_CPU_DIAGNOSTIC_LADDER_RESULT requested=nil injected=false') -and
            $snapshots -ge 3 -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        [ordered]@{case=$case;passed=$passed;fighter=$fighter;target_arena=1;
            exit_code=$exitCode;assisted_ladder=$true;input_only_stage_command=$true;
            approach_gap=if($approach.Success){[int]$approach.Groups[2].Value}else{$null};
            native_stage_handoff_frame=if($gate.Success){[int]$gate.Groups[1].Value}else{$null};
            snapshot_count=$snapshots;executable_sha256=$hashes[$Executable];
            payload_sha256=$hashes[$payload];harness_sha256=$hashes[$harness];
            runner_sha256=$hashes[$PSCommandPath]} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed approach_gap=$($approach.Groups[2].Value) handoff_frame=$($gate.Groups[1].Value)"
        if (-not $passed) {$failed+=$case}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    foreach ($key in $saved.Keys) {Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if ($failed.Count) {throw "Stage finish cases failed: $($failed -join ', ')"}
