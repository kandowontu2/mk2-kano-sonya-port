param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet('kano','sonya','liu_kang','kung_lao','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax')][string]$Player='sonya',
    [ValidateRange(600,1500)][int]$BootFrame=605,[ValidateRange(30,200)][int]$Seconds=95,
    [ValidateRange(96,370)][int]$ConfirmAge=264,
    [string]$CandidateName='diagnostic_v1836_ball_register_boundary',
    [ValidateSet('original','guard_wait','guard_until_close')][string]$Approach='guard_until_close',
    [ValidateSet('retreat','jump_guard','guard_hold','neutral_hold')][string]$Policy='retreat')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence names required'}
$out=Join-Path $root $CaseName;$candidate=Join-Path $root $CandidateName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}}
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Matched build required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$root/mk2ks_cpu_recovery_probe_v1438.lua","$root/mk2ks_physical_p2_cpu_continuation_v1997.lua","$root/mk2ks_physical_p2_cpu_round_trace_v1998.lua","$root/mk2ks_physical_p2_cpu_overlap_trace_v1999.lua","$root/mk2ks_physical_p2_cpu_choice_trace_v2035.lua","$root/mk2ks_native_cpu_bicycle_display_v3024.lua","$root/mk2ks_native_cpu_mobility_boundary_v3025.lua","$root/mk2/mk2-maincpu.bin")
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@("$root/mk2ks_physical_p2_cpu_continuation_v3095.lua","$root/mk2ks_native_cpu_human_hold_wrapper_v3096.lua")
$tracked+=@("$root/mk2ks_physical_p2_cpu_square_trace_v2038.lua","$root/mk2ks_physical_p2_cpu_square_display_v2039.lua","$root/mame-mkp/src/devices/cpu/tms34010/tms34010.cpp","$root/mame-mkp/src/devices/cpu/tms34010/34010gfx.hxx","$root/mame-mkp/src/devices/cpu/tms34010/34010ops.hxx")
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
$tracked=@($tracked | Select-Object -Unique)
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
# Inherit lossless NTFS compression only inside this newly created evidence leaf.
$resolvedEvidence=(Get-Item -LiteralPath $out).FullName
$resolvedRoot=(Get-Item -LiteralPath $root).FullName
if(-not $resolvedEvidence.StartsWith($resolvedRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe evidence leaf'}
& compact.exe /C /I /Q "/S:$resolvedEvidence" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot enable evidence compression'}
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Player;$env:MK2KS_TEST_BOOT_FRAME="$BootFrame";$env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_CPU_PAIR_APPROACH=$Approach
    $env:MK2KS_CPU_CONTINUATION_POLICY=$Policy
    $env:MK2KS_CPU_PAIR_CONFIRM_AGE="$ConfirmAge"
    $env:MK2KS_FLOOR_OUT=$out

    & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -nothrottle -noautoframeskip -frameskip 0 -str $Seconds -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_native_cpu_human_hold_wrapper_v3096.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}}
    [ordered]@{exit_code=$code;candidate=$CandidateName;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;player=$Player;boot_frame=$BootFrame;confirm_age=$ConfirmAge;approach=$Approach;policy=$Policy;cpu_slot=2;human_slot=1;assistance='none';cheats_enabled=$false;passed=$false;scope='natural_P2_CPU_human_hold_actual_branch_discovery_full_render_verification_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code (independent verification pending)"
}finally{
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
