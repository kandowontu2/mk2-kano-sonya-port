param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet(1,2)][int]$Side=1,
 [ValidateRange(2,5)][int]$MatchCount=3)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$candidate=Join-Path $root 'diagnostic_v2753_native_friendship_palette';$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Immutable repeat capture required'}
$build=Get-Content -LiteralPath "$candidate/build-info.json" -Raw | ConvertFrom-Json
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Matched native palette candidate required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$root/mk2ks_repeat_native_friendship_v2819.lua","$root/mk2/mk2-maincpu.bin")
foreach($item in $build.input_hashes.PSObject.Properties){
 if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Changed compiled input $($item.Name)"}
 $tracked+=$item.Name
}
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/samples/mk2ks" -File | ForEach-Object {$_.FullName})
$tracked=@($tracked | Select-Object -Unique)
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
& compact.exe /C $out | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot compress exact new evidence leaf'}
$hashes=@{}
foreach($file in $tracked){
 $hashes[$file]=(Get-FileHash -LiteralPath $file).Hash
 if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}
}
$hashes | ConvertTo-Json | Out-File -LiteralPath "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $env:MK2KS_REPEAT_SIDE="$Side";$env:MK2KS_REPEAT_MATCHES="$MatchCount";$env:MK2KS_REPEAT_OUT=$out
 & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -samplepath "$root/samples" -samples -samplerate 48000 -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -noautoframeskip -frameskip 0 -nothrottle -str 900 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_repeat_native_friendship_v2819.lua" 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Executed input changed $file"}}
 [ordered]@{exit_code=$code;candidate=$build.name;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
  side=$Side;requested_matches=$MatchCount;cheats_enabled=$false;guest_writes=0;assistance='none';emulator_resets=0;saved_states_used=$false;
  passed=$false;scope='uninterrupted repeated native Friendship palette diagnostic, independent checks pending';input_hashes=$hashes}
 | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code (independent verification pending)"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
