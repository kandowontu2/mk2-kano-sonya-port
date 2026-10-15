param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kung_lao','liu_kang','cage','baraka','kitana','mileena',
        'shang_tsung','raiden','sub_zero','reptile','scorpion','jax')]
    [string[]]$Victims=@('kung_lao','liu_kang','cage','baraka','kitana','mileena',
        'shang_tsung','raiden','sub_zero','reptile','scorpion','jax')
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence prefix'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_finish_state_trace.lua'
$baseHarness=Join-Path $root 'mk2ks_selector_exit_test.lua'
$tracked=@($Executable,$payload,$harness,$baseHarness,$PSCommandPath)
$hashes=@{}
foreach ($file in $tracked) {$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $root
try {
    foreach ($victim in $Victims) {
        foreach ($file in $tracked) {
            if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Input changed: $file"}
        }
        $reference=Get-Content -LiteralPath (Join-Path $root "diagnostic_v151_stock_prone_${victim}\run.log") -Raw
        $held=[regex]::Match($reference,'MK2_STOCK_VICTIM_HELD[^\r\n]*id=(\d+) health=0 pose=([0-9A-F]{8})')
        if (-not $held.Success) {throw "Missing stock reference ID: $victim"}
        $idHex='{0:X4}' -f [int]$held.Groups[1].Value
        Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
            Remove-Item
        $env:MK2KS_TEST_FIGHTER=$victim
        $env:MK2KS_P2_FIGHTER='sonya'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_TEST_ROUND_LOSS='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2_TRACE_NATIVE_FINISH='sonya'
        $env:MK2_TRACE_NATIVE_FINISH_SIDE='2'
        $env:MK2_TRACE_INPUT_ONLY_APPROACH='1'
        $env:MK2_TRACE_FINISH_ACTORS='1'
        $env:MK2_TRACE_FINISH_SNAPSHOTS='1'
        $case="${CasePrefix}_${victim}"
        $out=Join-Path $root $case
        if (Test-Path -LiteralPath $out) {throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str 95 -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $nativeVictim="MK2_FINISH_ACTORS[^\r\n]*age=2[0-3]\d[^\r\n]*p1=[^\r\n]*:${idHex}:FF[0-9A-F]{6}:"
        # P2's burn transition starts at age 225 in the observed native path.
        $burnVictim="MK2_FINISH_ACTORS[^\r\n]*age=2[0-9]\d[^\r\n]*p1=[^\r\n]*:${idHex}:FE9B0B20:"
        $passed=$exitCode -eq 0 -and $log -match $nativeVictim -and
            $log -match $burnVictim -and
            $log.Contains('MK2_FINISH_INPUT_APPROACH ') -and
            $log.Contains('MK2_FINISH_FIRE_PALETTE ') -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
            $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
            $log -match 'MK2KS_NATIVE_WIN[^\r\n]*winner=0012' -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        [ordered]@{case=$case;passed=$passed;victim=$victim;victim_id=$idHex;
            exit_code=$exitCode;executable_sha256=$hashes[$Executable];
            payload_sha256=$hashes[$payload];harness_sha256=$hashes[$harness]} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed victim_id=$idHex"
        if (-not $passed) {$failed+=$case}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    foreach ($key in $saved.Keys) {Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if ($failed.Count) {throw "P2 Sonya finisher cases failed: $($failed -join ', ')"}
