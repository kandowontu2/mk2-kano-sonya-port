param([Parameter(Mandatory=$true)][string]$CaseName,[string]$CandidateName='diagnostic_v2753_native_friendship_palette',
    [ValidateSet('kano','sonya')][string]$Target='kano',[ValidateSet(1,2)][int]$Side=1,
    [ValidateSet('native','block2','block_first','lp_first','stock_lp','stock_lk','stock_block','wrong_button','reversed','expired','extra_button','no_down','no_lp','no_block','airborne')][string]$Profile='native',[switch]$Render)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned names required'}
$out=Join-Path $root $CaseName;$candidate=Join-Path $root $CandidateName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Current build input changed: $($item.Name)"}}
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Matched executable/payload required'}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($exe,$payload,"$candidate/build-info.json","$root/mk2ks_human_shang_probe.lua",$PSCommandPath)
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@("$root/mk2ks_morph_guest_probe_v3145.lua","$root/mk2/mk2-maincpu.bin","$root/mk3/mk3-maincpu.bin")
$tracked=@($tracked | Select-Object -Unique)
$resolvedEvidence=(Get-Item -LiteralPath $out).FullName
$resolvedRoot=(Get-Item -LiteralPath $root).FullName
if(-not $resolvedEvidence.StartsWith($resolvedRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe evidence leaf'}
& compact.exe /C /I /Q "/S:$resolvedEvidence" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot enable evidence compression'}
$script="$root/mk2ks_morph_guest_probe_v3145.lua"
$snapshotSize='400x300'
if($Render){$tracked+="$root/mk2ks_morph_render_probe.lua";$snapshotSize='400x254'}
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_MORPH_CAPTURE_OUT=$out;$env:MK2KS_MORPH_CAPTURE_RENDER=if($Render){'1'}else{'0'}
    $env:MK2KS_HUMAN_SHANG_SIDE="$Side";$env:MK2KS_HUMAN_SHANG_TARGET=$Target;$env:MK2KS_HUMAN_SHANG_PROFILE=$Profile
    & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -nothrottle -noautoframeskip -frameskip 0 -str 80 -snapsize $snapshotSize -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $script 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    if((Get-Content -LiteralPath "$out/run.log" -Raw) -match 'LUA ERROR|stack traceback|Fatal error|access violation'){$code=1}
    foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Probe input changed: $file"}}
    $luaErrors=@(Select-String -LiteralPath "$out/run.log" -SimpleMatch '[LUA ERROR]')
    [ordered]@{exit_code=$code;lua_errors=$luaErrors.Count;candidate=$CandidateName;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
        target=$Target;side=$Side;profile=$Profile;passed=$false;scope='input_only_human_morph_diagnostic_independent_verification_pending';input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code (independent verification pending)"
}finally{
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}

