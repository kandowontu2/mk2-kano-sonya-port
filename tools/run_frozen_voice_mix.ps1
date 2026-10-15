param([Parameter(Mandatory=$true)][string]$CasePrefix,[ValidateSet(1,2)][int]$Side=1,[switch]$TwoHuman)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$out=Join-Path $root "${CasePrefix}_inputs_p$Side"
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite voice evidence'}
$candidate=Join-Path $root 'diagnostic_v277_native_battle_photos'
$tracked=@($PSCommandPath,"$PSScriptRoot/run_current_voice_mix.ps1","$PSScriptRoot/verify_voice_in_mix.py",
    "$root/mk2ks_selector_exit_test.lua","$root/PLAY_MK2_KANO_SONYA.cmd","$candidate/PLAY_CANDIDATE.cmd",
    "$candidate/mkport_candidate.exe","$candidate/roms/mk2ks/mk2ks.mdata")
foreach($sample in 'kano_select','sonya_select','kano_wins','sonya_wins'){$tracked+="$root/samples/mk2ks/$sample.wav"}
$hashes=[ordered]@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.cmd'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    & "$PSScriptRoot/run_current_voice_mix.ps1" -CasePrefix $CasePrefix -Side $Side -Fighters kano,sonya -TwoHuman:$TwoHuman 2>&1 |
        Out-File "$out/run.log" -Encoding utf8
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Voice input changed: $path"}}
    $cases=@()
    foreach($target in 'kano','sonya'){
        $name="${CasePrefix}_${target}_p$Side";$folder=Join-Path $root $name
        $result=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
        if($result.fighter -ne $target -or $result.side -ne $Side -or $result.executable_sha256 -ne $hashes["$candidate/mkport_candidate.exe"] -or
           $result.payload_sha256 -ne $hashes["$candidate/roms/mk2ks/mk2ks.mdata"] -or $result.mix_sha256 -ne (Get-FileHash "$folder/game_mix.wav").Hash){throw "Actual recorded mix/result mismatch: $name"}
        $cases+=[ordered]@{name=$name;mix_sha256=$result.mix_sha256;mix_bytes=$result.mix_bytes;log_sha256=(Get-FileHash "$folder/run.log").Hash}
    }
    [ordered]@{passed=$true;side=$Side;two_human_requested=$TwoHuman.IsPresent;cases=$cases;input_hashes=$hashes;
        scope='actual_root_CMD_v277_Kano_Sonya_selection_and_win_voices_in_rendered_game_mix_not_all_audio_or_finisher_fidelity'} |
        ConvertTo-Json -Depth 5 | Out-File "$out/result.json" -Encoding utf8
    "Current v277 selection/win voices verified in actual game mixes on P$Side"
} finally {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
