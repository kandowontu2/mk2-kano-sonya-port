param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [string]$Executable,
    [string]$PayloadRomDirectory,
    [ValidateSet(1,2)][int]$Side=1,
    [switch]$RequireFacing,
    [ValidateRange(75,150)][int]$Seconds=95
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$exe=if($Executable){(Resolve-Path -LiteralPath $Executable).Path}else{Join-Path $root 'diagnostic_v264_native_stock_body_trial/mkport_candidate.exe'}
$rompath=if($PayloadRomDirectory){(Resolve-Path -LiteralPath $PayloadRomDirectory).Path}else{Join-Path $root 'diagnostic_v264_native_stock_body_trial/roms'}
$harness=Join-Path $root 'mk2ks_kano_contact_capture.lua'
$out=Join-Path $root "${CasePrefix}_side${Side}"
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite contact evidence'}
$tracked=@($exe,$harness,$PSCommandPath,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),
    (Join-Path $root 'mk2ks_finish_state_trace.lua'),(Join-Path $root 'mk2ks_selector_exit_test.lua'))
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){'kano'}else{'sonya'}
    $env:MK2KS_P2_FIGHTER=if($Side -eq 1){'sonya'}else{'kano'}
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TWO_PLAYER='1'
    if($Side -eq 1){$env:MK2KS_TEST_ROUND_WIN='1'}else{$env:MK2KS_TEST_ROUND_LOSS='1'}
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2_TRACE_NATIVE_FINISH='kano';$env:MK2_TRACE_NATIVE_FINISH_SIDE="$Side"
    $env:MK2_TRACE_INPUT_ONLY_APPROACH='1';$env:MK2_TRACE_FINISH_ACTORS='1'
    $env:MK2_TRACE_FINISH_SNAPSHOTS='1'
    $env:MK2_TRACE_SKELETON_OBJECT='1'
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -skip_gameinfo -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $completed=$exitCode -eq 0 -and $log.Contains('MK2_CONTACT_CAPTURE_RESULT complete=true ') -and
        $log.Contains('MK2_FINISH_INPUT_APPROACH ') -and $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    $facing=$log.Contains('MK2_CONTACT_FACING_RESULT pass=true ')
    $passed=$completed -and (-not $RequireFacing -or $facing)
    [ordered]@{passed=$passed;capture_completed=$completed;native_contact_fidelity_verified=$false;
        skeleton_facing_verified=$facing;require_facing=$RequireFacing.IsPresent;exit_code=$exitCode;
        side=$Side;seconds=$Seconds;assistance='round_health_only';position_writes_allowed=$false;input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$out capture_completed=$completed"
    if(-not $passed){throw 'Contact capture or required facing assertion failed'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
