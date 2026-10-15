param([Parameter(Mandatory=$true)][string]$CaseName,
 [ValidateSet('knife','ball','blade','choke','ring','square','bicycle','leg')][string]$Move,
 [ValidateSet(1,2)][int]$Side=1,[ValidateSet('block','miss','duck_block')][string]$Scenario,
 [ValidateSet('kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax','kano','sonya')][string]$Victim='sub_zero',
 [string]$CandidateName='diagnostic_v3172_native_morph_shadow')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($Move -ne 'bicycle' -or $Scenario -ne 'block'){throw 'Only the bounded real Bicycle block fixture'}
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned case name required'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned candidate required'}
$candidate=Join-Path $root $CandidateName;$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build source changed: $($item.Name)"}}
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Matched build required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$root/mk2ks_human_special_negative_v9.lua","$root/mk2ks_human_bicycle_block_trace_v3345.lua","$root/mk2/mk2-maincpu.bin","$root/mk3/mk3-maincpu.bin")
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$resolvedRoot=(Get-Item -LiteralPath $root).FullName
$resolvedEvidence=(Get-Item -LiteralPath $out).FullName
if(-not $resolvedEvidence.StartsWith($resolvedRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or (Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe evidence leaf'}
& compact.exe /C /I /Q "/S:$resolvedEvidence" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot enable lossless evidence compression'}
$tracked=@($tracked | Select-Object -Unique)
$hashes=@{};$snapshots=@{}
foreach($file in $tracked){
 $resolved=(Resolve-Path -LiteralPath $file).Path
 if(-not $resolved.StartsWith($resolvedRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Workspace inputs only'}
 $hashes[$file]=(Get-FileHash -LiteralPath $file).Hash
 if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){
  $destination=Join-Path "$out/input_sources/tree" $resolved.Substring($resolvedRoot.Length+1)
  New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
  Copy-Item -LiteralPath $file -Destination $destination
  if((Get-FileHash -LiteralPath $destination).Hash -ne $hashes[$file]){throw 'Exact source snapshot required'}
  $snapshots[$file]=$destination
 }
}
$snapshots | ConvertTo-Json | Out-File "$out/source_snapshot_paths.json" -Encoding utf8
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $env:MK2KS_HUMAN_SPECIAL_MOVE=$Move;$env:MK2KS_HUMAN_SPECIAL_SIDE="$Side";$env:MK2KS_HUMAN_SPECIAL_SCENARIO=$Scenario;$env:MK2KS_HUMAN_SPECIAL_VICTIM=$Victim
 $env:MK2KS_BBLOCK_OUT=$out
 & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -noautoframeskip -frameskip 0 -nothrottle -str 65 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_human_bicycle_block_trace_v3345.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 if((Get-Content -LiteralPath "$out/run.log" -Raw) -match 'LUA ERROR|stack traceback|Fatal error|access violation'){$code=1}
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}}
 [ordered]@{exit_code=$code;candidate=$build.name;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;move=$Move;side=$Side;scenario=$Scenario;victim=$Victim;cheats_enabled=$false;assistance='none';passed=$false;snapshot_schema=2;scope='current_human_bicycle_block_whole_guest_native_trace_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code (independent verification pending)"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
