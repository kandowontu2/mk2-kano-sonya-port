param([string]$CaseName='audit_v299_projectile_choreography_assets_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence name'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$payload=Join-Path $root 'diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.mdata'
$tracked=@($PSCommandPath,$payload,[IO.Path]::ChangeExtension($payload,'choreography.json'),
    "$root/tools/build_native_projectile_choreography.py","$root/tools/test_native_projectile_choreography.py",
    "$root/tools/build_native_projectile_impacts.py","$root/tools/test_native_projectile_impacts.py",
    "$root/tools/build_native_projectiles.py","$root/tools/build_mk2ks_mk3.py","$root/tools/upgrade_ksui_previews.py",
    "$root/mame-mkp/src/mame/midway/midtunit_m.cpp","$root/mame-mkp/src/mame/midway/midtunit.cpp",
    "$root/diagnostic_v293_native_projectile_impacts/mkport_candidate.exe",
    "$root/diagnostic_v293_native_projectile_impacts/roms/mk2ks/mk2ks.mdata",
    "$root/PLAY_MK2_KANO_SONYA.cmd","$root/diagnostic_v277_native_battle_photos/PLAY_CANDIDATE.cmd",
    "$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe",
    "$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata")
foreach($kind in @('knife','ring')){
    $reference="$root/audit_v297_original_${kind}_release_full"
    $tracked+=@("$reference/result.json","$reference/run.log")
    $tracked+=Get-ChildItem -LiteralPath "$reference/input_sources" -File | Select-Object -ExpandProperty FullName
}
$before=[ordered]@{}
foreach($path in $tracked){$before[$path]=(Get-FileHash -LiteralPath $path).Hash}
if($before[$payload] -ne '51BD733DE93015DB71FAA7E5172D68D90832622173D776D1725AEABF27E33E82'){
    throw 'Unexpected choreography payload'
}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$before | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){
    if([IO.Path]::GetExtension($path) -in '.py','.ps1','.cpp'){
        Copy-Item -LiteralPath $path -Destination "$out/input_sources"
    }
}
Push-Location $root
try {
    $ErrorActionPreference='Continue'
    & python -m unittest discover -s tools -p test_native_projectile_choreography.py -v 2>&1 |
        Out-File "$out/choreography_tests.log" -Encoding utf8
    $choreographyCode=$LASTEXITCODE
    & python -m unittest discover -s tools -p test_native_projectile_impacts.py -v 2>&1 |
        Out-File "$out/impact_asset_regression.log" -Encoding utf8
    $impactCode=$LASTEXITCODE
    $ErrorActionPreference='Stop'
    $after=[ordered]@{}
    foreach($path in $tracked){
        $after[$path]=(Get-FileHash -LiteralPath $path).Hash
        if($after[$path] -ne $before[$path]){throw "Input changed: $path"}
    }
    $after | ConvertTo-Json | Out-File "$out/input_hashes_after.json" -Encoding utf8
    $newLog=Get-Content "$out/choreography_tests.log" -Raw
    $oldLog=Get-Content "$out/impact_asset_regression.log" -Raw
    $pass=$choreographyCode -eq 0 -and $impactCode -eq 0 -and
        $newLog.Contains('Ran 13 tests') -and $oldLog.Contains('Ran 7 tests')
    [ordered]@{passed=$pass;scope='payload_assets_and_original_input_only_reference_not_port_runtime';
        choreography_test_exit=$choreographyCode;impact_asset_regression_exit=$impactCode;tests=20;
        payload_sha256=$before[$payload];native_runtime_changed=$false;native_runtime_verified=$false;
        original_game_releases_verified=4;full_goal_complete=$false;production_unchanged=$true;
        input_hashes=$before} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    if(-not $pass){throw 'Choreography asset checkpoint failed'}
    Get-Content "$out/result.json"
} finally {Pop-Location}
