param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet('kano','sonya')][string]$Winner='kano',
 [ValidateSet(1,2)][int]$Side=1,[ValidateRange(180,1200)][int]$Seconds=600)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName;$candidate=Join-Path $root 'diagnostic_v786_native_fighter_fade_exclusions'
if(Test-Path -LiteralPath $out){throw 'Do not overwrite evidence'}
$build=Get-Content -LiteralPath "$candidate/build-info.json" -Raw | ConvertFrom-Json
$tracked=@($PSCommandPath,"$root/mk2ks_native_stage_performer_v805.lua","$candidate/mkport_candidate.exe",
 "$candidate/roms/mk2ks/mk2ks.mdata","$candidate/build-info.json","$root/mk2/mk2-maincpu.bin")
foreach($item in $build.input_hashes.PSObject.Properties){
 if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}
 $tracked+=$item.Name
}
if((Get-FileHash -LiteralPath "$candidate/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or
 (Get-FileHash -LiteralPath "$candidate/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Matched candidate required'}
$tracked+=Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName}
$tracked=@($tracked | Select-Object -Unique);$hashes=@{}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File -LiteralPath "$out/inputs_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $env:MK2KS_STAGE_SIDE="$Side";$env:MK2KS_STAGE_WINNER=$Winner;$env:MK2KS_STAGE_OUT=$out
 & "$candidate/mkport_candidate.exe" mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -samplepath "$root/samples" -samples -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -samplerate 48000 -wavwrite "$out/native_mix.wav" -noautoframeskip -frameskip 0 -nothrottle -str $Seconds -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_native_stage_performer_v805.lua" 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Executed input changed: $file"}}
 [ordered]@{exit_code=$code;winner=$Winner;side=$Side;seconds=$Seconds;guest_writes=0;assistance='none';passed=$false;fullPortAcceptance=$false;scope='native stage performer through earned wins/paid rematches; verification pending';mix_sha256=(Get-FileHash -LiteralPath "$out/native_mix.wav").Hash;input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code (verification pending)"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
