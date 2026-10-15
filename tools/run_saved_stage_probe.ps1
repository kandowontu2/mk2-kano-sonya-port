param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [Parameter(Mandatory=$true)][string]$State,
    [Parameter(Mandatory=$true)][int]$OriginalFrame,
    [int]$Seconds=60,
    [switch]$TraceCpu,
    [ValidateSet('mk2ks_saved_stage12_probe.lua','mk2ks_saved_ending_probe.lua')][string]$HarnessName='mk2ks_saved_stage12_probe.lua'
)
$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
if ($CaseName -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple case name.'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$State=(Resolve-Path -LiteralPath $State).Path
$harness=Join-Path $portRoot $HarnessName
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$tracked=@($Executable,$payload,$State,$harness)
$hashes=@{}
foreach ($file in $tracked) {$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$out=Join-Path $portRoot $CaseName
if (Test-Path -LiteralPath $out) {throw "Refusing to overwrite evidence: $out"}
New-Item -ItemType Directory -Path $out | Out-Null
$savedOrigin=$env:MK2KS_SAVED_GLOBAL_FRAME
$savedTrace=$env:MK2KS_SAVED_TRACE_PATH
$env:MK2KS_SAVED_GLOBAL_FRAME="$OriginalFrame"
if ($TraceCpu) {$env:MK2KS_SAVED_TRACE_PATH=Join-Path $out 'cpu_trace.log'}
$debugArgs=if ($TraceCpu) {@('-debug','-debugger','none')} else {@()}
Push-Location $out
try {
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms" `
        -artpath "$portRoot\artwork" -video none -sound none -nothrottle -log -str $Seconds @debugArgs `
        -state $State -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" `
        -snapshot_directory "$out\snap" -autoboot_script $harness 2>&1 |
        Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach ($file in $tracked) {
        if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Input changed: $file"}
    }
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    $result=($log -split "`n" | Where-Object {$_ -match '^MK2KS_SAVED_(STAGE|ENDING)_RESULT '}) | Select-Object -Last 1
    $watchdog=if (Test-Path -LiteralPath "$out\error.log") {
        @(Select-String -LiteralPath "$out\error.log" -Pattern 'Reset caused by the watchdog').Count
    } else {0}
    [ordered]@{case=$CaseName;exit_code=$exitCode;state_sha256=$hashes[$State];
        executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
        harness_sha256=$hashes[$harness];original_frame=$OriginalFrame;
        cpu_trace_path=$(if ($TraceCpu) {Join-Path $out 'cpu_trace.log'} else {''});
        watchdog_log_entries=$watchdog;summary=$result} | ConvertTo-Json |
        Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output $result
    Write-Output "watchdog_log_entries=$watchdog"
    if ($exitCode -ne 0 -or -not $result) {throw "Saved-stage probe failed: $CaseName"}
} finally {
    Pop-Location
    if ($null -eq $savedOrigin) {Remove-Item Env:MK2KS_SAVED_GLOBAL_FRAME -ErrorAction SilentlyContinue}
    else {$env:MK2KS_SAVED_GLOBAL_FRAME=$savedOrigin}
    if ($null -eq $savedTrace) {Remove-Item Env:MK2KS_SAVED_TRACE_PATH -ErrorAction SilentlyContinue}
    else {$env:MK2KS_SAVED_TRACE_PATH=$savedTrace}
}
