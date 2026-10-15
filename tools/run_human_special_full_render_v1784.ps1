param([Parameter(Mandatory=$true)][string]$CaseName,
 [ValidateSet('knife','ball','blade','choke','ring','square','bicycle','leg')][string]$Move,
 [ValidateSet(1,2)][int]$Side=1,[switch]$Air)
$ErrorActionPreference='Stop';$taskRoot=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned case name required'}
$candidate=Join-Path $taskRoot 'diagnostic_v1597_native_ground_throw';$out=Join-Path $taskRoot $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build source changed: $($item.Name)"}}
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Matched build required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$taskRoot/mk2ks_human_special_matrix_v3.lua","$taskRoot/mk2ks_human_special_full_render_v1783.lua")
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@('34010gfx.hxx','34010ops.hxx' | ForEach-Object {"$taskRoot/mame-mkp/src/devices/cpu/tms34010/$_"})
$tracked+=@(Get-ChildItem -LiteralPath "$taskRoot/artwork" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$taskRoot/roms/mk2ks" -File | ForEach-Object {$_.FullName})
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
# Compression is inherited by new capture files; byte contents are unchanged.
& compact.exe /C $out | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot enable lossless compression on the exact new capture leaf'}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $taskRoot
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $env:MK2KS_HUMAN_SPECIAL_MOVE=$Move;$env:MK2KS_HUMAN_SPECIAL_SIDE="$Side";$env:MK2KS_HUMAN_SPECIAL_AIR=if($Air){'1'}else{'0'}
 $env:MK2KS_HUMAN_SPECIAL_VICTIM='sub_zero';$env:MK2KS_PROJECTILE_DISPLAY_OUT=$out
 & $exe mk2ks -rompath "$candidate/roms;$taskRoot/roms" -artpath "$taskRoot/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -noautoframeskip -frameskip 0 -nothrottle -str 65 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$taskRoot/mk2ks_human_special_full_render_v1783.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}}
 [ordered]@{exit_code=$code;candidate=$build.name;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;move=$Move;side=$Side;air=[bool]$Air;victim='sub_zero';cheats_enabled=$false;assistance='none';passed=$false;scope='consecutive_special_full_render_independent_verification_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code (independent verification pending)"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
