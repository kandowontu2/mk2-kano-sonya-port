param([string]$Name='audit_v339_native_shang_roster_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$out=Join-Path $root $Name
if($Name -notmatch '^audit_v[0-9]+_[a-z0-9_]+$' -or (Test-Path -LiteralPath $out)){throw 'Fresh versioned evidence required'}
$candidate=Join-Path $root 'diagnostic_v336_native_cpu_turn_lookup'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
$tracked=@($PSCommandPath,"$candidate/build-info.json","$candidate/mkport_candidate.exe","$candidate/roms/mk2ks/mk2ks.mdata",
    "$root/tools/verify_native_shang_roster.py","$root/tools/test_native_shang_roster.py","$root/tools/test_native_shang_morphs.py",
    "$root/tools/build_native_shang_morphs.py","$root/tools/build_mk2ks_mk3.py","$root/tools/build_native_projectile_impacts.py",
    "$root/tools/upgrade_ksui_previews.py","$root/tools/run_shang_roster_probe.ps1",
    "$root/mk2ks_shang_roster_probe.lua","$root/mk2ks_cpu_ladder_trace.lua","$root/mk2ks_selector_exit_test.lua",
    "$root/mk2/mk2-maincpu.bin","$root/diagnostic_v300_native_projectile_choreography/roms/mk2ks/mk2ks.mdata",
    "$root/diagnostic_v323_native_shang_morph_payload/roms/mk2ks/mk2ks.morph.json",
    "$root/PLAY_MK2_KANO_SONYA.cmd","$root/mame-mkp/mkport.exe")
$tracked+=Get-ChildItem -LiteralPath "$root/mk3" -File | Select-Object -ExpandProperty FullName
$tracked+=$build.input_hashes.PSObject.Properties.Name
$tracked+=Get-ChildItem -LiteralPath "$candidate/input_sources" -File | Select-Object -ExpandProperty FullName
foreach($fighter in @('kano','sonya')) {
    $case=Join-Path $root "audit_v338_shang_${fighter}_full_roster_table"
    $tracked+=Get-ChildItem -LiteralPath $case -File -Recurse | Select-Object -ExpandProperty FullName
}
$tracked=$tracked | Sort-Object -Unique
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($file in $tracked){if($file -in @($PSCommandPath,"$root/tools/verify_native_shang_roster.py","$root/tools/test_native_shang_roster.py","$root/tools/test_native_shang_morphs.py")){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
$python='C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe'
Push-Location $root
try {
    & $python -m unittest discover -s tools -p 'test_native_shang*.py' 2>&1 | Out-File "$out/tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Native art/runtime mutation tests failed'}
    if((Get-Content "$out/tests.log" -Raw) -notmatch 'Ran 37 tests'){throw 'Expected complete 37-test scope'}
    foreach($fighter in @('kano','sonya')){
        & $python tools/verify_native_shang_roster.py "audit_v338_shang_${fighter}_full_roster_table" $fighter --output "$out/$fighter.json" |
            Out-File "$out/${fighter}_verify.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw "Actual $fighter native morph verification failed"}
    }
    foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Audit input changed: $file"}}
    if((Get-FileHash "$root/PLAY_MK2_KANO_SONYA.cmd").Hash -ne '9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' -or
       (Get-FileHash "$root/mame-mkp/mkport.exe").Hash -ne '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'){throw 'Production/installed launcher unexpectedly changed'}
    [ordered]@{passed=$true;tests=37;checked_inputs=$tracked.Count;candidate=$build.name;executable_sha256=$build.executable_sha256;
        payload_sha256=$build.payload_sha256;form_fields=1071;post_restore_fields=240;
        scope='original_assets_and_stage14_health_assisted_native_CPU_random_morph_turn_restore';
        whole_character_integration_complete=$false;production_unchanged=$true;input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$Name passed: 37 tests and both native morph chains; $($tracked.Count) frozen inputs; production unchanged"
} finally {Pop-Location}
