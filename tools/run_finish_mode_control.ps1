param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [int]$Seconds=750
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if ($CaseName -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence name.'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$harness=Join-Path $root 'mk2ks_finish_state_trace.lua'
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$tracked=@($Executable,$payload,$harness,(Join-Path $root 'mk2ks_cpu_ladder_trace.lua'),
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
$hashes=@{}
foreach ($path in $tracked) {$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$out=Join-Path $root $CaseName
if (Test-Path -LiteralPath $out) {throw "Refusing to overwrite evidence: $out"}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    $env:MK2KS_TEST_FIGHTER='liu_kang'
    $env:MK2KS_P2_FIGHTER='stock'
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_ROUND_WIN='1'
    $env:MK2KS_DIAGNOSTIC_ALL_STAGES='1'
    $env:MK2KS_DIAGNOSTIC_CPU_HEALTH='1'
    $env:MK2KS_DIAGNOSTIC_P1_REGEN='1'
    $env:MK2_TRACE_LADDER='1'
    New-Item -ItemType Directory -Path $out | Out-Null
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
        -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
        -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
        -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach ($path in $tracked) {
        if ((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]) {throw "Input changed: $path"}
    }
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    $reached=$log -match 'MK2_FINISH_STATE frame=\d+ arena=6 mode=0 stage=6 '
    $left=$log -match 'MK2_FINISH_STATE frame=\d+ arena=7 mode=\d+ stage=7 '
    $finish=$log -match 'MK2_FINISH_STATE frame=\d+ arena=6 mode=3 stage=6 '
    $passed=$exitCode -eq 0 -and $reached -and $left -and
        $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{case=$CaseName;passed=$passed;fighter='liu_kang';
        reached_arena6=$reached;left_arena6=$left;arena6_finish_window=$finish;
        exit_code=$exitCode;assisted_ladder=$true;
        executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
        harness_sha256=$hashes[$harness];runner_sha256=$hashes[$PSCommandPath]} |
        ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed arena6_finish_window=$finish"
    if (-not $passed) {throw "Stock fighter control failed: $CaseName"}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    foreach ($key in $saved.Keys) {Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
