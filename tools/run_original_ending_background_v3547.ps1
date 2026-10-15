param([Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateRange(60,300)][int]$Seconds=180)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence leaf required'}
$candidate=Join-Path $root 'diagnostic_v3172_native_morph_shadow'
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Do not overwrite evidence'}
$build=Get-Content -LiteralPath "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Compiled input changed: $($item.Name)"}
}
$exe="$candidate/mkport_candidate.exe"
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256){throw 'Actual unchanged executable required'}
$tracked=@($exe,"$candidate/build-info.json",$PSCommandPath,
    "$root/mk2ks_original_ending_background_v3546.lua","$root/mk2ks_current_ending_presentation_v680_v4.lua",
    "$root/mk2/mk2-maincpu.bin","$root/roms/mk2.zip")
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked=@($tracked | Select-Object -Unique)
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$resolvedEvidence=(Get-Item -LiteralPath $out).FullName
$resolvedRoot=(Get-Item -LiteralPath $root).FullName
if(-not $resolvedEvidence.StartsWith($resolvedRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or
   (Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe capture leaf'}
& compact.exe /C /I /Q "/S:$resolvedEvidence" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot compress fresh capture leaf'}
$hashes=@{};$snapshots=@{}
foreach($file in $tracked){
    $resolved=(Resolve-Path -LiteralPath $file).Path
    if(-not $resolved.StartsWith($resolvedRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Workspace input required'}
    $hashes[$file]=(Get-FileHash -LiteralPath $file).Hash
    if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){
        $destination=Join-Path "$out/input_sources/tree" $resolved.Substring($resolvedRoot.Length+1)
        New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $file -Destination $destination
        if((Get-FileHash -LiteralPath $destination).Hash -ne $hashes[$file]){throw 'Exact frozen input snapshot required'}
        $snapshots[$file]=$destination
    }
}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$snapshots | ConvertTo-Json | Out-File "$out/source_snapshot_paths.json" -Encoding utf8
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER='liu_kang';$env:MK2KS_TEST_BOOT_FRAME='600'
    $env:MK2KS_CAMPAIGN_SIDE='1';$env:MK2KS_CAMPAIGN_STRATEGY='uppercut';$env:MK2KS_CAMPAIGN_OUT=$out
    & $exe mk2 -rompath "$root/roms" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -nosamples -noautoframeskip -frameskip 0 -nothrottle -str $Seconds -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_original_ending_background_v3546.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    if((Get-Content -LiteralPath "$out/run.log" -Raw) -match 'LUA ERROR|stack traceback|Fatal error|access violation'){$code=1}
    foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Actual input changed: $file"}}
    [ordered]@{exit_code=$code;candidate='diagnostic_v3172_native_morph_shadow';game='mk2';
        executable_sha256=$build.executable_sha256;player='liu_kang';human_slot=1;cpu_slot=2;
        seconds=$Seconds;assistance='stage14_combat_health_only';cheats_enabled=$false;
        snapshot_schema=2;raw_audio_files_written=0;new_builds_or_rom_copies=0;
        passed=$false;unassisted_clear_proven=$false;
        scope='original_stock_MK2_ending_background_assisted_reference_not_natural_campaign';
        input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code (original background verification pending)"
}finally{
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
