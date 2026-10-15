param([string]$CaseName='audit_v325_shang_roster_native',[string]$CandidateName='diagnostic_v324_native_shang_roster',[ValidateRange(60,600)][int]$Seconds=240,[ValidateRange(600,620)][int]$BootFrame=600)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$out=Join-Path $root $CaseName;$candidate=Join-Path $root $CandidateName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
$exe=Join-Path $candidate 'mkport_candidate.exe';$payload=Join-Path $candidate 'roms/mk2ks/mk2ks.mdata'
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Current build input changed: $($item.Name)"}}
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Matched build identity required'}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($exe,$payload,"$candidate/build-info.json","$root/mk2ks_shang_roster_probe.lua","$root/mk2ks_cpu_ladder_trace.lua","$root/mk2ks_selector_exit_test.lua",$PSCommandPath)
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash;if([IO.Path]::GetExtension($path) -in '.lua','.json','.ps1'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER='kano';$env:MK2KS_P2_FIGHTER='stock';$env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_BOOT_FRAME="$BootFrame"
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_ALLOW_NATURAL_LOSS='1'
    $env:MK2KS_DIAGNOSTIC_LADDER_INDEX='14';$env:MK2KS_DIAGNOSTIC_P1_REGEN='1';$env:MK2KS_TRACE_ALL_REGEN='1'
    & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_shang_roster_probe.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Probe input changed: $path"}}
    [ordered]@{exit_code=$code;candidate=$CandidateName;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
        scope='diagnostic_stage14_P1_health_assisted_native_random_morph_observations_independent_verification_pending';
        passed=$false;input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code (independent verification pending)"
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
