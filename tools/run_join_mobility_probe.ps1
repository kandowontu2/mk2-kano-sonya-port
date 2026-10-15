param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet('kano','sonya')][string]$Target,
    [ValidateSet('hit','block','miss')][string]$Scenario='hit',
    [string]$CandidateName='diagnostic_v277_native_battle_photos',[ValidateSet(1,2)][int]$Side=1)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned candidate names'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$payload=Join-Path $candidate 'roms/mk2ks/mk2ks.mdata'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate input changed: $($item.Name)"}}
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Candidate build changed'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$tracked=@($exe,$payload,"$candidate/build-info.json","$root/mk2ks_join_mobility_probe.lua","$root/mk2ks_restart_lifecycle.lua",
    "$root/mk2ks_selector_exit_test.lua","$root/mk2ks_mobility_contact.lua",$PSCommandPath,
    "$PSScriptRoot/verify_restart_lifecycle.py","$PSScriptRoot/verify_mobility_contact.py","$PSScriptRoot/verify_current_lifecycle.py",
    "$PSScriptRoot/verify_projectile_contact.py")
$hashes=[ordered]@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.json'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Target;$env:MK2KS_P2_FIGHTER='stock';$env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_MOBILITY_CONTACT=$Scenario;$env:MK2KS_MOBILITY_SIDE="$Side";$env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str 100 -snapsize 400x300 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script "$root/mk2ks_join_mobility_probe.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed during case: $path"}}
    $log=Get-Content "$out/run.log" -Raw
    python "$out/input_sources/verify_restart_lifecycle.py" "$out/run.log" --target $Target --side $Side --mobility-contact --cold |
        Out-File "$out/independent_verification.json" -Encoding utf8
    $verificationCode=$LASTEXITCODE
    $passed=$code -eq 0 -and $verificationCode -eq 0 -and $log.Contains('MK2_JOIN_LIFE_RESULT pass=true ') -and $log -notmatch '(?i)fatal error|\[LUA ERROR\]|access violation|exception at'
    [ordered]@{passed=$passed;exit_code=$code;target=$Target;side=$Side;scenario=$Scenario;observer_pass=$log.Contains('MK2_JOIN_LIFE_RESULT pass=true ');
        candidate=$CandidateName;candidate_executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
        cheats=$false;memory_assistance='none';independent_verification_exit_code=$verificationCode;
        scope='cold_native_CPU_start_real_challenger_join_601_field_mobility_contact_not_post_ending_or_full_CPU_variety';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code"
    if(-not $passed){throw 'Preserve failed mobility evidence'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
