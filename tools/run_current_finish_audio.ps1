param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [ValidateSet('kano','sonya')][string[]]$Fighters=@('kano','sonya'),
    [ValidateSet(1,2)][int]$Side=1,
    [string]$CandidateName=''
)
$ErrorActionPreference='Stop'
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$root=Split-Path $PSScriptRoot -Parent
$launcher=Join-Path $root 'PLAY_MK2_KANO_SONYA.cmd'
$harness=Join-Path $root 'mk2ks_finish_state_trace.lua'
$candidateMatch=[regex]::Match((Get-Content -LiteralPath $launcher -Raw),
    'set "MK2_CANDIDATE_CMD=%~dp0([^"\r\n]+)\\PLAY_CANDIDATE\.cmd"')
if(-not $candidateMatch.Success){throw 'Root launcher candidate path could not be resolved'}
$explicitCandidate=[bool]$CandidateName
if(-not $CandidateName){$CandidateName=$candidateMatch.Groups[1].Value}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned candidate directory name'}
$candidate=Join-Path $root $CandidateName
$usedLauncher=if($explicitCandidate){Join-Path $candidate 'PLAY_CANDIDATE.cmd'}else{$launcher}
if(-not (Test-Path -LiteralPath $usedLauncher -PathType Leaf)){throw "Candidate launcher missing: $usedLauncher"}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    foreach($fighter in $Fighters){
        Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
            Remove-Item
        $opponent=if($fighter -eq 'kano'){'sonya'}else{'kano'}
        $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){$fighter}else{'kitana'}
        $env:MK2KS_P2_FIGHTER=if($Side -eq 1){$opponent}else{$fighter}
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='1'
        if($Side -eq 1){$env:MK2KS_TEST_ROUND_WIN='1'}
        else{$env:MK2KS_TEST_ROUND_LOSS='1'}
        $env:MK2_TRACE_NATIVE_FINISH=$fighter
        $env:MK2_TRACE_NATIVE_FINISH_SIDE="$Side"
        $env:MK2_TRACE_INPUT_ONLY_APPROACH='1'
        if($fighter -eq 'kano'){$env:MK2_TRACE_SKELETON_OBJECT='1'}
        $out=Join-Path $root "${CasePrefix}_${fighter}_p${Side}"
        if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        $mix=Join-Path $out 'game_mix.wav'
        & $usedLauncher -video none -nothrottle -str 95 -wavwrite $mix `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" `
            -snapshot_directory "$out\snap" -autoboot_script $harness 2>&1 |
            Out-File -LiteralPath "$out\run.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw "$fighter fatality audio run exited $LASTEXITCODE"}
        if(-not (Test-Path -LiteralPath $mix)){throw "$fighter fatality mix was not recorded"}
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        if($log -notmatch 'MK2_NATIVE_FINISH_ACTION ' -or
           $log -notmatch 'MK2KS_EXIT_RESULT pass=true ' -or
           $log -notmatch 'MK2KS_STABILITY stalled_frames=0 trap_frames=0'){
            throw "$fighter finisher did not complete cleanly"
        }
        $cueMatches=@{}
        if($fighter -eq 'kano'){
            $cue='kano_extract'
            $sample=Join-Path $root "samples\mk2ks\$cue.wav"
            $match=& python (Join-Path $PSScriptRoot 'verify_voice_in_mix.py') $mix $sample 40 85
            if($LASTEXITCODE -ne 0){throw "$fighter $cue matching failed"}
            Write-Output "$fighter $cue $match"
            $score=[regex]::Match($match,'correlation=([0-9.]+) gain=([0-9.]+)')
            if(-not $score.Success -or
               [double]$score.Groups[1].Value -lt 0.55 -or
               [double]$score.Groups[2].Value -le 0.1){
                throw "$fighter $cue is not confidently audible in the actual game mix"
            }
            $cueMatches[$cue]=$match
        } else {
            $joint=& python (Join-Path $PSScriptRoot 'verify_sonya_finish_mix.py') $mix
            if($LASTEXITCODE -ne 0){throw 'Sonya finish cues did not pass the joint mix fit'}
            $joint | ForEach-Object {Write-Output $_}
            $cueMatches['joint_fit']=@($joint)
        }
        [ordered]@{fighter=$fighter;side=$Side;launcher_sha256=(Get-FileHash $usedLauncher).Hash;
            candidate_name=$CandidateName;explicit_candidate=$explicitCandidate;
            executable_sha256=(Get-FileHash (Join-Path $candidate 'mkport_candidate.exe')).Hash;
            payload_sha256=(Get-FileHash (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata')).Hash;
            mix_sha256=(Get-FileHash $mix).Hash;mix_bytes=(Get-Item $mix).Length;
            matches=$cueMatches} | ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
