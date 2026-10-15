param([Parameter(Mandatory=$true)][ValidateSet('kano','sonya')][string]$Player,
 [ValidateSet(1,2)][int]$ConfirmFirst=1,[ValidateSet(1,2)][int]$Winner=1)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $root 'diagnostic_v1130_owned_split_invariant_blood'
$out=Join-Path $root "audit_v1177_${Player}_mirror_finish_winner_p${Winner}_confirm_p${ConfirmFirst}"
if(Test-Path -LiteralPath $out){throw 'Never overwrite evidence'}
$build=Get-Content -LiteralPath "$candidate/build-info.json" -Raw | ConvertFrom-Json
$exe=Join-Path $candidate 'mkport_candidate.exe'
$payload=Join-Path $candidate 'roms/mk2ks/mk2ks.mdata'
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Matched build required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$root/mk2ks_natural_mirror_finish_v1166.lua","$root/mk2ks_natural_mirror_finish_display_v1176.lua")
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
$hashes=@{}
foreach($file in ($tracked | Select-Object -Unique)){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
foreach($item in $build.input_hashes.PSObject.Properties){if($hashes[$item.Name] -ne $item.Value){throw "Changed build input $($item.Name)"}}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Copy-Item -LiteralPath $PSCommandPath,"$root/mk2ks_natural_mirror_finish_v1166.lua","$root/mk2ks_natural_mirror_finish_display_v1176.lua" -Destination "$out/input_sources"
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $env:MK2KS_TEST_FIGHTER=$Player;$env:MK2KS_MIRROR_CONFIRM_FIRST="$ConfirmFirst";$env:MK2KS_REPTILE_AUDIT_DIR=$out;$env:MK2KS_MIRROR_WINNER="$Winner"
 $env:MK2_TRACE_NATIVE_FINISH_SIDE="$Winner";$env:MK2_TRACE_NATIVE_FINISH=$Player;$env:MK2KS_FLOOR_OUT=$out
 & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -samplepath "$root/samples" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -noautoframeskip -frameskip 0 -nothrottle -str 95 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_natural_mirror_finish_display_v1176.lua" 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $hashes.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed $file"}}
 [ordered]@{exit_code=$code;candidate=$build.name;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;player=$Player;confirm_first=$ConfirmFirst;winner=$Winner;seconds=95;assistance='none';guest_writes=0;cheats_enabled=$false;passed=$false;scope='natural_physical_mirror_finisher_diagnostic_verification_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
 "Natural mirror finish $Player winner=P$Winner first=P$ConfirmFirst terminal exit=$code; independent verification pending"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
