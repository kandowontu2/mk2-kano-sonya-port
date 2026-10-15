param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [string[]]$Victims=@('kung_lao','liu_kang','cage','baraka','kitana','mileena',
        'shang_tsung','raiden','sub_zero','reptile','scorpion','jax','kano','sonya'),
    [ValidateSet(1,2)][int[]]$Sides=@(1,2),
    [switch]$DonorReviewSnapshots,
    [switch]$BounceTrace
)
$ErrorActionPreference='Stop'
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix.'}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_airthrow_probe.lua'
$tracked=@($Executable,$payload,$harness,(Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
$hashes=@{}
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $root
try {
    foreach($victim in $Victims){foreach($side in $Sides){
        foreach($file in $tracked){
            if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}
        }
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=if($side -eq 1){'kano'}else{$victim}
        $env:MK2KS_P2_FIGHTER=if($side -eq 2){'kano'}else{$victim}
        $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_AIRTHROW_SIDE="$side"
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2KS_PIN_FIGHTERS='0'
        $env:MK2KS_PROBE_NATIVE_ROSTER='0'
        if($DonorReviewSnapshots){$env:MK2KS_AIRTHROW_DONOR_REVIEW_SNAPSHOTS='1'}
        if($BounceTrace){$env:MK2KS_AIRTHROW_BOUNCE_TRACE='1'}
        $case="${CasePrefix}_${victim}_p${side}"
        $out=Join-Path $root $case
        if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str 40 -snapsize 400x300 -snapshot_directory "$out\snap" `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        foreach($file in $tracked){
            if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}
        }
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $distance=[regex]::Match($log,'MK2KS_AIRTHROW_STATE age=72 distance=(\d+)')
        $passed=$exitCode -eq 0 -and
            $log.Contains('MK2KS_AIRTHROW_RESULT observed_throw=true damage=16 id=17,') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $distance.Success -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        if($DonorReviewSnapshots){
            $passed=$passed -and (Test-Path -LiteralPath (Join-Path "$out\snap" 'kano_airthrow_age096.png'))
        }
        [ordered]@{case=$case;passed=$passed;victim=$victim;side=$side;
            donor_review_snapshots=$DonorReviewSnapshots.IsPresent;bounce_trace=$BounceTrace.IsPresent;
            separation=if($distance.Success){[int]$distance.Groups[1].Value}else{$null};
            exit_code=$exitCode;executable_sha256=$hashes[$Executable];
            payload_sha256=$hashes[$payload];harness_sha256=$hashes[$harness]} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed separation=$(if($distance.Success){$distance.Groups[1].Value}else{'missing'})"
        if(-not $passed){$failed+=$case}
    }}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
if($failed.Count){throw "Air-throw victim cases failed: $($failed -join ', ')"}
