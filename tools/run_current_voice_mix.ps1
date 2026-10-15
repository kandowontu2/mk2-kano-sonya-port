param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [ValidateSet('kano','sonya','liu_kang','kitana','jax')][string[]]$Fighters=@('kano','sonya'),
    [ValidateSet(1,2)][int]$Side=1,
    [switch]$TraceSound,
    [switch]$TwoHuman,
    [string]$CandidateDirectory=''
)
$ErrorActionPreference='Stop'
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$root=Split-Path $PSScriptRoot -Parent
$harness=Join-Path $root $(if($TraceSound){'mk2ks_voice_port_trace.lua'}else{'mk2ks_selector_exit_test.lua'})
if($CandidateDirectory){
    $candidate=(Resolve-Path -LiteralPath (Join-Path $root $CandidateDirectory)).Path
    $launcher=Join-Path $candidate 'PLAY_CANDIDATE.cmd'
}else{
    $launcher=Join-Path $root 'PLAY_MK2_KANO_SONYA.cmd'
    $candidateMatch=[regex]::Match((Get-Content -LiteralPath $launcher -Raw),
        'set "MK2_CANDIDATE_CMD=%~dp0([^"\r\n]+)\\PLAY_CANDIDATE\.cmd"')
    if(-not $candidateMatch.Success){throw 'Root launcher candidate path could not be resolved'}
    $candidate=Join-Path $root $candidateMatch.Groups[1].Value
}
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    foreach($fighter in $Fighters){
        $stockFighter=$fighter -in @('liu_kang','kitana','jax')
        if($stockFighter -and $Side -ne 1){throw 'Stock voice baseline is P1-only.'}
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){$fighter}else{'kitana'}
        $env:MK2KS_P2_FIGHTER=if($stockFighter -or $TwoHuman -and $Side -eq 1){'sub_zero'}elseif($Side -eq 1){'stock'}else{$fighter}
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER=if($stockFighter -or $Side -eq 2 -or $TwoHuman){'1'}else{'0'}
        if($Side -eq 1){$env:MK2KS_TEST_ROUND_WIN='1'}
        else{$env:MK2KS_TEST_ROUND_LOSS='1'}
        $out=Join-Path $root "${CasePrefix}_${fighter}_p${Side}"
        if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        $mix=Join-Path $out 'game_mix.wav'
        & $launcher -video none -nothrottle -str 70 -wavwrite $mix `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" `
            -snapshot_directory "$out\snap" -autoboot_script $harness 2>&1 |
            Out-File -LiteralPath "$out\run.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw "$fighter audio run exited $LASTEXITCODE"}
        if(-not (Test-Path -LiteralPath $mix)){throw "$fighter mix was not recorded"}
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $winner=switch($fighter){'kano'{'0011'} 'sonya'{'0012'} 'liu_kang'{'0001'} 'kitana'{'0004'} 'jax'{'000B'}}
        if($log -notmatch "MK2KS_NATIVE_WIN frame=\d+ winner=$winner " -or
           $log -notmatch 'MK2KS_EXIT_RESULT pass=true ' -or
           $log -notmatch 'MK2KS_STABILITY stalled_frames=0 trap_frames=0'){
            throw "$fighter voice run failed gameplay assertions"
        }
        foreach($cue in $(if($stockFighter){@()}else{@('select','wins')})){
            $sample=Join-Path $root "samples\mk2ks\${fighter}_${cue}.wav"
            $match=& python (Join-Path $PSScriptRoot 'verify_voice_in_mix.py') $mix $sample 0 70
            if($LASTEXITCODE -ne 0){throw "$fighter $cue voice matching failed"}
            Write-Output "$fighter $cue $match"
            if($match -notmatch 'correlation=([0-9.]+)' -or [double]$Matches[1] -lt 0.8){
                throw "$fighter $cue voice was not confidently present in the actual game mix"
            }
        }
        [ordered]@{fighter=$fighter;side=$Side;launcher_sha256=(Get-FileHash $launcher).Hash;
            executable_sha256=(Get-FileHash (Join-Path $candidate 'mkport_candidate.exe')).Hash;
            payload_sha256=(Get-FileHash (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata')).Hash;
            mix_sha256=(Get-FileHash $mix).Hash;mix_bytes=(Get-Item $mix).Length} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
