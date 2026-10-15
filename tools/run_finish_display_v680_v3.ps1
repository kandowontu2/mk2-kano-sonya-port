param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateSet('kano','sonya')][string]$Fighter='kano',
    [ValidateSet('kano','sonya','sub_zero','raiden')][string]$Victim='sonya',
    [ValidateRange(60,128)][int]$ApproachGap=65,
    [string]$CandidateName='diagnostic_v680_native_pit_initial_cache'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned candidate'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$rompath=Join-Path $candidate 'roms'
$buildPath=Join-Path $candidate 'build-info.json'
$build=Get-Content -LiteralPath $buildPath -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Actual build input changed: $($item.Name)"}}
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or
   (Get-FileHash -LiteralPath "$rompath/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Candidate build mismatch'}
$harness=Join-Path $root 'mk2ks_finish_display_v680_v3.lua'
$verifier=Join-Path $PSScriptRoot 'verify_unassisted_finish.py'
$tracked=@($exe,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),$harness,$PSCommandPath,
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),(Join-Path $root 'mk2ks_finish_range_test.lua'),
    (Join-Path $root 'mk2ks_finish_state_trace.lua'),(Join-Path $root 'mk2ks_native_shang_morph.lua'),
    (Join-Path $root 'mk2ks_unassisted_finish_probe.lua'),$verifier,$buildPath,(Join-Path $root 'mk2/mk2-maincpu.bin'))
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | Select-Object -ExpandProperty FullName)
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | Select-Object -ExpandProperty FullName)
$tracked+=@(Get-ChildItem -LiteralPath "$root/samples" -File -Recurse | Select-Object -ExpandProperty FullName)
$tracked=@($tracked | Select-Object -Unique)
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json -Depth 3 | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){
    if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.json'){
        Copy-Item -LiteralPath $path -Destination "$out/input_sources"
    }
}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Fighter;$env:MK2KS_P2_FIGHTER=$Victim
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
    $env:MK2KS_TEST_ROUND_WIN='1';$env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2_TRACE_NATIVE_FINISH=$Fighter;$env:MK2_TRACE_NATIVE_FINISH_SIDE='1'
    $env:MK2_TRACE_INPUT_ONLY_APPROACH='1';$env:MK2_TRACE_APPROACH_GAP="$ApproachGap"
    $env:MK2_TRACE_FINISH_ACTORS='1';$env:MK2_TRACE_FINISH_SNAPSHOTS='1';$env:MK2_RANGE_EXPECT='activate'
    $env:MK2_TRACE_FINISH_SOUND='1';$env:MK2_TRACE_FINISH_SOUND_CALLER='1'
    $env:MK2_TRACE_KISS_CALLS='1';$env:MK2_TRACE_KISS_SNAPSHOTS='1'
    $env:MK2_TRACE_FINISH_CALLS='1';$env:MK2_TRACE_FINISH_FINE_SNAPSHOTS='1'
    $env:MK2KS_FLOOR_OUT=$out
    if($Fighter -eq 'kano'){$env:MK2_TRACE_SKELETON_OBJECT='1'}
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -samplepath "$root/samples" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -samplerate 48000 -wavwrite "$out/native_audio.wav" -noautoframeskip -frameskip 0 -nothrottle -str 95 -snapsize 400x254 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $match=[regex]::Match($log,'MK2_UNASSISTED_RESULT fighter=(\w+) damage_events=(\d+) total_damage=(\d+) wins=(\d+) errors=(\d+) writers=([0-9A-F,]+) writes=0 assistance=none')
    $nativeDamage=$match.Success -and $match.Groups[1].Value -eq $Fighter -and
        [int]$match.Groups[2].Value -ge 8 -and [int]$match.Groups[3].Value -ge 322 -and
        [int]$match.Groups[4].Value -ge 2 -and $match.Groups[5].Value -eq '0' -and
        $match.Groups[6].Value -eq 'FF836700'
    & 'C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe' $verifier "$out/run.log" --fighter $Fighter --victim $Victim |
        Out-File "$out/native_damage_verification.json" -Encoding utf8
    $independent=$LASTEXITCODE -eq 0
    $passed=$exitCode -eq 0 -and $nativeDamage -and $independent -and $log.Contains('MK2_RANGE_RESULT pass=true ') -and
        $log.Contains('MK2_FINISH_INPUT_APPROACH ') -and $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log -notmatch '(?i)MK2_FINISH_POSITION_ASSIST|fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{passed=$passed;native_damage_observed=$nativeDamage;independent_verification=$independent;fighter=$Fighter;victim=$Victim;
        candidate=$CandidateName;candidate_executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
        executable_sha256=$build.executable_sha256;human_slot=1;
        approach_gap=$ApproachGap;exit_code=$exitCode;cheats_enabled=$false;assistance='none';
        scope='native_p1_damage_and_finisher_input_not_full_tower';input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed native_damage=$nativeDamage"
    if(-not $passed){throw 'Unassisted finisher case failed'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
