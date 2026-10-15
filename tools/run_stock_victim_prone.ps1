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
$observer=Join-Path $root 'mk2ks_stock_victim_prone_trace.lua'
$baseHarness=Join-Path $root 'mk2ks_selector_exit_test.lua'
$tracked=@($Executable,$payload,$observer,$baseHarness,$PSCommandPath)
$hashes=@{}
foreach($file in $tracked) {$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $root
try {
    foreach($victim in $Victims) {
        foreach($file in $tracked) {
            if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Input changed: $file"}
        }
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER='kano'
        $env:MK2KS_P2_FIGHTER=$victim
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_TEST_ROUND_WIN='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $case="${CasePrefix}_${victim}"
        $out=Join-Path $root $case
        if (Test-Path -LiteralPath $out) {throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str 44 -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $observer 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $held=($log -split "`n" | Where-Object {$_ -match '^MK2_STOCK_VICTIM_HELD '}) | Select-Object -Last 1
        $passed=$exitCode -eq 0 -and $log.Contains('MK2_STOCK_VICTIM_PRONE_RESULT pass=true ') -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        [ordered]@{case=$case;passed=$passed;held=$held;exit_code=$exitCode;
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
            observer_sha256=$hashes[$observer];harness_sha256=$hashes[$baseHarness]} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed $held"
        if (-not $passed) {$failed+=$case}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys) {Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if ($failed.Count) {throw "Stock victim pose cases failed: $($failed -join ', ')"}
