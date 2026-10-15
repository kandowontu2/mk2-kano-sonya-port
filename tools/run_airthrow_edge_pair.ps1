param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('sonya','sub_zero')][string]$Victim='sonya',
    [int]$EdgeShiftFrames=80
)
$ErrorActionPreference='Stop'
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple case prefix.'}
if($EdgeShiftFrames -lt 1 -or $EdgeShiftFrames -gt 240){throw 'EdgeShiftFrames must be 1..240.'}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$harness=Join-Path $root 'mk2ks_airthrow_probe.lua'
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$tracked=@($Executable,$payload,$harness,(Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
$hashes=@{}
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' |
    ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    foreach($side in 1,2){foreach($direction in 'left','right'){
        foreach($file in $tracked){
            if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}
        }
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=if($side -eq 1){'kano'}else{$Victim}
        $env:MK2KS_P2_FIGHTER=if($side -eq 1){$Victim}else{'kano'}
        $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_AIRTHROW_SIDE="$side"
        $env:MK2KS_AIRTHROW_EDGE_SHIFT="$EdgeShiftFrames"
        $env:MK2KS_AIRTHROW_EDGE_DIRECTION=$direction
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2KS_PIN_FIGHTERS='0'
        $env:MK2KS_PROBE_NATIVE_ROSTER='0'
        $case="${CasePrefix}_${Victim}_p${side}_${direction}"
        $out=Join-Path $root $case
        if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str 42 -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $state=[regex]::Match($log,'MK2KS_AIRTHROW_STATE age=72 distance=(\d+) p1=(-?\d+),')
        $passed=$exitCode -eq 0 -and $state.Success -and
            $log.Contains('MK2KS_AIRTHROW_RESULT observed_throw=true damage=16 id=17,') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        [ordered]@{case=$case;passed=$passed;side=$side;direction=$direction;
            edge_shift_frames=$EdgeShiftFrames;
            attacker_x=if($state.Success){[int]$state.Groups[2].Value}else{$null};
            separation=if($state.Success){[int]$state.Groups[1].Value}else{$null};
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload]} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed x=$($state.Groups[2].Value) separation=$($state.Groups[1].Value)"
        if(-not $passed){throw "Edge air throw failed: $case"}
    }}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
