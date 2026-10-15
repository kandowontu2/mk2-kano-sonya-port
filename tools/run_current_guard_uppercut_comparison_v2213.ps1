param([Parameter(Mandatory=$true)][string]$CaseName,
 [ValidateSet('uppercut_kano','uppercut_sonya','uppercut_liu','uppercut_subzero')][string]$Move,
 [ValidateSet(1,2)][int]$Side=1,[switch]$Air,
 [ValidateSet('kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax','kano','sonya')][string]$Victim='sub_zero',
 [string]$CandidateName='diagnostic_v1836_ball_register_boundary',
 [ValidateSet('neutral','guard_release')][string]$Profile='neutral',[ValidateSet(6,12,24)][int]$Lead=6)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned case name required'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned candidate name required'}
$candidate=Join-Path $root $CandidateName;$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build source changed: $($item.Name)"}}
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Matched build required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$root/mk2ks_guard_uppercut_comparison_v2212.lua")
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@(Get-ChildItem -LiteralPath "$root/samples/mk2ks" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$resolvedEvidence=(Get-Item -LiteralPath $out).FullName
$resolvedRoot=(Get-Item -LiteralPath $root).FullName
if(-not $resolvedEvidence.StartsWith($resolvedRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe fresh evidence leaf'}
& compact.exe /C /I /Q "/S:$resolvedEvidence" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot compress fresh ordinary probe evidence'}
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $env:MK2KS_HUMAN_ORDINARY_OUT=$out;$env:MK2KS_HUMAN_SPECIAL_MOVE=$Move;$env:MK2KS_HUMAN_SPECIAL_SIDE="$Side";$env:MK2KS_HUMAN_SPECIAL_AIR=if($Air){'1'}else{'0'}
 $env:MK2KS_HUMAN_SPECIAL_VICTIM=$Victim;$env:MK2KS_GUARD_PROFILE=$Profile;$env:MK2KS_GUARD_LEAD="$Lead"
 & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -samplepath "$root/samples" -samples -samplerate 48000 -wavwrite "$out/native_mix.wav" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -noautoframeskip -frameskip 0 -nothrottle -str 65 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_guard_uppercut_comparison_v2212.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}}
 [ordered]@{exit_code=$code;candidate=$build.name;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;move=$Move;side=$Side;profile=$Profile;lead=$Lead;air=[bool]$Air;victim=$Victim;cheats_enabled=$false;assistance='none';passed=$false;scope='current_native_guard_comparison_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code (independent verification pending)"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
