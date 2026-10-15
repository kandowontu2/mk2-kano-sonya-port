param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet('sonya','sub_zero')][string]$Victim='sonya',[switch]$Followup,
    [string]$CandidateName='diagnostic_v277_native_battle_photos')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple versioned evidence name'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned candidate names'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$payload=Join-Path $candidate 'roms/mk2ks/mk2ks.mdata'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate input changed: $($item.Name)"}}
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Candidate build changed'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$tracked=@($exe,$payload,"$candidate/build-info.json","$root/mk2ks_join_airthrow_probe.lua","$root/mk2ks_restart_airthrow.lua","$root/mk2ks_selector_exit_test.lua",
    "$PSScriptRoot/verify_restart_airthrow.py",$PSCommandPath)
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.json'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER='kano';$env:MK2KS_P2_FIGHTER='stock';$env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_AIR_JOIN_VICTIM=$Victim
    $env:MK2KS_AIR_JOIN_FOLLOWUP=if($Followup){'1'}else{'0'}
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str 90 -snapsize 400x300 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script "$root/mk2ks_join_airthrow_probe.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content "$out/run.log" -Raw
    $extra=@()
    if($Followup){$extra+='--followup'}
    python "$out/input_sources/verify_restart_airthrow.py" "$out/run.log" --cold @extra | Out-File "$out/independent_verification.json" -Encoding utf8
    $verificationCode=$LASTEXITCODE
    [ordered]@{exit_code=$exitCode;victim=$Victim;followup=$Followup.IsPresent;observer_pass=$log.Contains('MK2_AIR_JOIN_RESULT pass=true');
        independent_verification_exit_code=$verificationCode;candidate=$CandidateName;candidate_executable_sha256=$build.executable_sha256;
        payload_sha256=$build.payload_sha256;scope='cold_native_join_diagnosis_not_post_ending_acceptance';input_hashes=$hashes} |
        ConvertTo-Json -Depth 3 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$exitCode"
    if($exitCode -ne 0 -or $verificationCode -ne 0){throw 'Preserve failed cold airthrow evidence'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
