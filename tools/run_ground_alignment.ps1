param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet(1,2)][int[]]$Sides=@(1,2),
    [ValidateSet('kano','sonya','sub_zero')][string[]]$Fighters=@('kano','sonya','sub_zero'),
    [switch]$ArcSnapshots
)
$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$harness=Join-Path $portRoot 'mk2ks_ground_alignment_test.lua'
$visualScript=Join-Path $PSScriptRoot 'check_floor_shadow_alignment.py'
$arcScript=Join-Path $PSScriptRoot 'check_shadow_arc_alignment.py'
$tracked=@($Executable,(Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'),$harness,$PSCommandPath,
    (Join-Path $portRoot 'mk2ks_selector_exit_test.lua'),$visualScript,$arcScript)
$hashes=@{}
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
function Assert-Unchanged {
    foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}}
}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $portRoot
try {
    foreach($side in $Sides){foreach($fighter in $Fighters){
        Assert-Unchanged
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=if($side -eq 1){$fighter}else{'kitana'}
        $env:MK2KS_P2_FIGHTER=if($side -eq 2){$fighter}else{'kitana'}
        $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2KS_PIN_FIGHTERS='0';$env:MK2KS_PROBE_NATIVE_ROSTER='0'
        if($ArcSnapshots){$env:MK2KS_GROUND_ARC_SNAPSHOTS='1'}
        $case="${CasePrefix}_side${side}_${fighter}_kitana"
        $out=Join-Path $portRoot $case
        if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms" `
            -artpath "$portRoot\artwork" -skip_gameinfo -video none -sound none -nothrottle -str 40 -snapsize 400x300 `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        Assert-Unchanged
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $passed=$exitCode -eq 0 -and $log -notmatch '(?i)fatal error|exception at|access violation|error in emu|\[LUA ERROR\]'
        $markers=@('MK2KS_GROUND_RESULT pass=true ','MK2KS_DISPLAY_RESULT pass=true ',
            'MK2KS_STABILITY stalled_frames=0 trap_frames=0')
        if($fighter -ne 'sub_zero') {
            $markers+=@('MK2KS_EXIT_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ')
        } else {
            # This control contains no added fighter: the parent's custom-name
            # and shadow assertions deliberately have zero applicable samples.
            # The floor observer checks both actual selected stock identities.
            $markers+=@('leaks=0 identity_errors=0 name_checks=0 name_errors=0','p2_identity_errors=0')
        }
        foreach($marker in $markers){
            $passed=$passed -and $log.Contains($marker)
        }
        [ordered]@{case=$case;passed=$passed;side=$side;fighter=$fighter;exit_code=$exitCode;
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$tracked[1]];file_hashes=$hashes} |
            ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed"
        if(-not $passed){$failed+=$case}
    }}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if($failed.Count){throw "Ground alignment cases failed: $($failed -join ', ')"}
if (@($Sides).Count -eq 2 -and @($Fighters).Count -eq 3) {
    Assert-Unchanged
    & python $visualScript $CasePrefix --root $portRoot
    if ($LASTEXITCODE -ne 0) {throw 'Airborne floor-shadow screen-space comparison failed'}
    if($ArcSnapshots){
        & python $arcScript $CasePrefix --root $portRoot
        if($LASTEXITCODE -ne 0){throw 'Multi-height floor-shadow comparison failed'}
    }
}
