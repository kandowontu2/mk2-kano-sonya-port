param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory
)
$ErrorActionPreference='Stop'
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name'}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    $env:MK2KS_TEST_FIGHTER='scorpion'
    $env:MK2KS_P2_FIGHTER='kitana'
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TWO_PLAYER='1'
    $env:MK2KS_TEST_ROUND_WIN='1'
    $env:MK2_TRACE_SCORPION_FIRE='1'
    $env:MK2_TRACE_INPUT_ONLY_APPROACH='1'
    $env:MK2_TRACE_APPROACH_GAP='160'
    $env:MK2_TRACE_FINISH_SNAPSHOTS='1'
    $env:MK2_TRACE_POST_FINISH_SCENE_SNAPSHOTS='1'
    New-Item -ItemType Directory -Path $out | Out-Null
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
        -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
        -str 95 -snapsize 400x300 -cfg_directory "$out\cfg" `
        -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
        -autoboot_script "$root\mk2ks_finish_state_trace.lua" 2>&1 |
        Out-File -LiteralPath "$out\run.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Stock finish control exited $LASTEXITCODE"}
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    if($log -notmatch 'MK2_FINISH' -or $log -notmatch 'MK2_POST_FINISH_SCENE_SNAPSHOT' -or
       $log -notmatch 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' -or
       $log -match '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'){
        throw 'Stock finish control did not reach a clean post-finish scene'
    }
    Write-Output "Stock Scorpion finish control: $out"
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
