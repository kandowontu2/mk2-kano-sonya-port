param([Parameter(Mandatory=$true)][string]$CaseName,
 [ValidateSet('interrupt','ko')][string]$Kind,
 [ValidateSet('blade','bicycle','leg')][string]$Move,
 [ValidateSet(1,2)][int]$Side,
 [ValidateSet('kano','sonya','kitana','sub_zero')][string]$Victim)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned immutable evidence required'}
if($Kind -eq 'ko' -and $Move -eq 'leg'){throw 'Established KO contract covers blade/bicycle'}
if($Kind -eq 'interrupt' -and (($Move -eq 'blade' -and $Victim -ne 'sonya') -or $Victim -notin 'kano','sonya')){throw 'Established interruption fixture required'}
$candidate=Join-Path $root 'diagnostic_v2753_native_friendship_palette'
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Never overwrite executed evidence'}
$build=Get-Content -LiteralPath "$candidate/build-info.json" -Raw | ConvertFrom-Json
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Exact native palette candidate required'}
$driver=if($Kind -eq 'interrupt'){"mk2ks_${Move}_interrupt_v4.lua"}else{"mk2ks_${Move}_lifecycle_test.lua"}
$wrapper="$root/mk2ks_native_combat_regression_v2849.lua"
$tracked=@($exe,$payload,"$candidate/build-info.json",$wrapper,"$root/$driver",$PSCommandPath,
 "$root/mk2ks_interrupt_trace_v3.lua","$root/mk2ks_lifecycle_trace.lua","$root/mk2ks_selector_exit_test.lua",
 "$root/mk2ks_native_shang_morph.lua","$root/mk2/mk2-maincpu.bin")
foreach($item in $build.input_hashes.PSObject.Properties){
 if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Changed compiled input $($item.Name)"}
 $tracked+=$item.Name
}
foreach($directory in 'artwork','roms/mk2ks','samples/mk2ks'){
 $tracked+=@(Get-ChildItem -LiteralPath "$root/$directory" -File | ForEach-Object {$_.FullName})
}
$tracked=@($tracked | Select-Object -Unique)
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
& compact.exe /C $out | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot compress exact new evidence leaf'}
$hashes=[ordered]@{}
foreach($file in $tracked){
 $hashes[$file]=(Get-FileHash -LiteralPath $file).Hash
 if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}
}
$hashes | ConvertTo-Json | Out-File -LiteralPath "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $attacker=if($Move -eq 'blade'){'kano'}else{'sonya'}
 $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){$attacker}else{$Victim}
 $env:MK2KS_P2_FIGHTER=if($Side -eq 2){$attacker}else{$Victim}
 $env:MK2KS_TWO_PLAYER='1';$env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8'
 $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
 $env:MK2KS_LIFECYCLE_TRACE=if($Kind -eq 'ko'){'1'}else{'0'}
 Set-Item -LiteralPath "Env:MK2KS_$($Move.ToUpper())_SIDE" -Value "$Side"
 $env:MK2KS_NATIVE_REGRESSION_DRIVER=$driver;$env:MK2KS_NATIVE_REGRESSION_OUT=$out
 $seconds=if($Kind -eq 'ko'){120}else{65}
 & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -nothrottle -noautoframeskip -frameskip 0 -str $seconds -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $wrapper 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Executed input changed $file"}}
 $log=Get-Content -LiteralPath "$out/run.log" -Raw
 $type=if($Kind -eq 'ko'){'LIFECYCLE'}else{'INTERRUPT'}
 $markers=@("MK2KS_$($Move.ToUpper())_${type}_RESULT pass=true ",'MK2KS_EXIT_RESULT pass=true ',
  'MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0',
  "MK2_NATIVE_COMBAT_GUEST driver=$driver bytes=1048576 writes=0 assistance=none")
 $passed=$code -eq 0 -and $log -notmatch '(?i)fatal error|\[LUA ERROR\]|access violation|exception at'
 foreach($marker in $markers){$passed=$passed -and $log.Contains($marker)}
 [ordered]@{observer_passed=$passed;exit_code=$code;kind=$Kind;move=$Move;side=$Side;victim=$Victim;
  candidate=$build.name;executable_sha256=$build.executable_sha256;candidate_executable_sha256=$build.executable_sha256;
  payload_sha256=$build.payload_sha256;cheats=$false;cheats_enabled=$false;assistance='none';memory_assistance='none';
  guest_writes=0;emulator_resets=0;saved_states_used=$false;input_hashes=$hashes;
  scope='Established unassisted physical interruption/retry or earned KO/next-round fixture with whole actual guest capture';
  independent_verification_pending=$true;fullPortAcceptance=$false} | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code observer_pass=$passed"
 if(-not $passed){throw 'Preserve failed actual combat fixture'}
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
