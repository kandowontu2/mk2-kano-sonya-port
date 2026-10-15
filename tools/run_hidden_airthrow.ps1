param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateRange(0,240)][int]$EdgeShiftFrames=0,
    [ValidateSet(0,14,15,16)][int]$HiddenId=0,
    [ValidateSet(0,1,2)][int]$AttackerSide=0,
    [ValidateSet('both','left','right')][string]$EdgeDirection='both'
)
$ErrorActionPreference='Stop'
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix.'}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_hidden_airthrow_probe.lua'
$romPath="$PayloadRomDirectory;$root\roms_v22_clean;$root\roms"
$tracked=@($Executable,$payload,$harness,(Join-Path $root 'mk2ks_airthrow_probe.lua'),
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
$hashes=@{}
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' |
    ForEach-Object {$saved[$_.Name]=$_.Value}
$failures=@()
Push-Location $root
try {
    $directions=if($EdgeShiftFrames -eq 0){@('none')}
        elseif($EdgeDirection -eq 'both'){@('left','right')}
        else{@($EdgeDirection)}
    $ids=if($HiddenId -eq 0){@(14,15,16)}else{@($HiddenId)}
    $sides=if($AttackerSide -eq 0){@(1,2)}else{@($AttackerSide)}
    foreach($id in $ids){
        foreach($side in $sides){
            foreach($direction in $directions){
            foreach($file in $tracked){
                if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){
                    throw "Input changed during matrix: $file"
                }
            }
            Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
            $env:MK2KS_TEST_FIGHTER=if($side -eq 1){'kano'}else{'sonya'}
            $env:MK2KS_P2_FIGHTER=if($side -eq 1){'sonya'}else{'kano'}
            $env:MK2KS_TWO_PLAYER='1'
            $env:MK2KS_TEST_CONFIRM='hp'
            $env:MK2KS_TEST_CONFIRM_HOLD='8'
            $env:MK2KS_AIRTHROW_SIDE="$side"
            $env:MK2KS_DIAGNOSTIC_HIDDEN_ID="$id"
            if($EdgeShiftFrames -gt 0){
                $env:MK2KS_AIRTHROW_EDGE_SHIFT="$EdgeShiftFrames"
                $env:MK2KS_AIRTHROW_EDGE_DIRECTION=$direction
            }
            $case="${CasePrefix}_${id}_p${side}"
            if($EdgeShiftFrames -gt 0){$case="${case}_${direction}"}
            $out=Join-Path $root $case
            if(Test-Path -LiteralPath $out){throw "Refusing to overwrite evidence: $out"}
            New-Item -ItemType Directory -Path $out | Out-Null
            & $Executable mk2ks -rompath $romPath -artpath "$root\artwork" -skip_gameinfo `
                -video none -sound none -nothrottle -str 40 -snapsize 400x300 `
                -snapshot_directory "$out\snap" -cfg_directory "$out\cfg" `
                -nvram_directory "$out\nvram" -autoboot_script $harness 2>&1 |
                Out-File -LiteralPath "$out\run.log" -Encoding utf8
            $exitCode=$LASTEXITCODE
            $log=Get-Content -LiteralPath "$out\run.log" -Raw
            $pass=$exitCode -eq 0 -and
                $log.Contains("MK2KS_AIRTHROW_RESULT observed_throw=true damage=12 id=17,$id") -and
                $log.Contains("MK2KS_HIDDEN_AIR_RESULT id=$id pose=true recovery=true damage=12") -and
                $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
                $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
            $state=[regex]::Match($log,'MK2KS_AIRTHROW_STATE age=72 distance=(\d+) p1=(-?\d+),')
            if($EdgeShiftFrames -gt 0){$pass=$pass -and $state.Success}
            [ordered]@{case=$case;passed=$pass;exit_code=$exitCode;hidden_id=$id;attacker_side=$side;
                edge_shift_frames=$EdgeShiftFrames;edge_direction=$direction;
                separation=if($state.Success){[int]$state.Groups[1].Value}else{$null};
                attacker_x=if($state.Success){[int]$state.Groups[2].Value}else{$null};
                executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
                harness_sha256=$hashes[$harness]} | ConvertTo-Json -Depth 3 |
                Out-File -LiteralPath "$out\result.json" -Encoding utf8
            Write-Output "$case pass=$pass separation=$($state.Groups[1].Value)"
            if(-not $pass){$failures+=$case}
            }
        }
    }
} finally {
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($name in $saved.Keys){[Environment]::SetEnvironmentVariable($name,$saved[$name],'Process')}
    Pop-Location
}
if($failures.Count){throw "Hidden air-throw failures: $($failures -join ', ')"}
