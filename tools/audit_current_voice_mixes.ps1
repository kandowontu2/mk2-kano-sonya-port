param([string]$OutputName='audit_v290_voice_mix_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite audio evidence'}
New-Item -ItemType Directory -Path $out | Out-Null
$cases=@()
foreach($side in 1,2){
    $prefix=if($side -eq 1){'audit_v290_twohuman_voice_mix'}else{'audit_v290_current_voice_mix'}
    $folder=Join-Path $root "${prefix}_inputs_p$side"
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.passed -or $original.side -ne $side){throw 'Missing accepted recorded voice cases'}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1','.py','.cmd'){
            $path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Original audio script changed: $path"}
        }else{
            if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Original audio build/sample changed: $($item.Name)"}
        }
    }
    foreach($target in 'kano','sonya'){
        $name="${prefix}_${target}_p$side";$case=Join-Path $root $name
        $result=Get-Content "$case/result.json" -Raw | ConvertFrom-Json
        if($result.mix_sha256 -ne (Get-FileHash "$case/game_mix.wav").Hash){throw "Recorded mix changed: $name"}
        $log=Get-Content "$case/run.log" -Raw
        $winner=if($target -eq 'kano'){'0011'}else{'0012'}
        if($log -notmatch "MK2KS_NATIVE_WIN frame=\d+ winner=$winner " -or $log -notmatch 'MK2KS_EXIT_RESULT pass=true ' -or
           $log -notmatch 'MK2KS_STABILITY stalled_frames=0 trap_frames=0'){throw "Actual voice gameplay not accepted: $name"}
        $scores=[ordered]@{}
        foreach($cue in 'select','wins'){
            $match=python "$PSScriptRoot/verify_voice_in_mix.py" "$case/game_mix.wav" "$root/samples/mk2ks/${target}_${cue}.wav" 0 70
            if($LASTEXITCODE -ne 0 -or $match -notmatch 'correlation=([0-9.]+)' -or [double]$Matches[1] -lt 0.8){throw "Actual voice match rejected: $name $cue"}
            $scores[$cue]=$match
        }
        $cases+=[ordered]@{name=$name;side=$side;target=$target;voice_matches=$scores;mix_sha256=$result.mix_sha256;log_sha256=(Get-FileHash "$case/run.log").Hash}
    }
}
[ordered]@{passed=$true;cases=$cases;production_game_changed=$false;scope='current_v277_actual_root_CMD_two_human_selection_and_win_voices_both_slots';
    original_P1_CPU_case_not_accepted='audit_v290_current_voice_mix_kano_p1 did not reach a win; it is not audio or CPU-tower acceptance';
    all_game_audio_complete=$false} | ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
'Four recorded current-build selection/win voice cases independently verified'
