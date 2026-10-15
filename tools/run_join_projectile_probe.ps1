param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet('kano','sonya')][string]$Target,
    [ValidateSet('hit','block','miss')][string]$Scenario='hit',
    [string]$Candidate='diagnostic_v277_native_battle_photos',[ValidateSet(1,2)][int]$Side=1,[switch]$Impact,[switch]$Choreography,[switch]$Render,[switch]$Bridge)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
if($Candidate -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned candidate directory'}
$candidateRoot=Join-Path $root $Candidate
$exe=Join-Path $candidateRoot 'mkport_candidate.exe'
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$tracked=@($exe,"$candidateRoot/roms/mk2ks/mk2ks.mdata","$root/mk2ks_join_projectile_probe.lua","$root/mk2ks_restart_lifecycle.lua",
    "$root/mk2ks_selector_exit_test.lua","$root/mk2ks_projectile_contact.lua",$PSCommandPath)
$autoboot="$root/mk2ks_join_projectile_probe.lua"
$snapshotSize='400x300'
if($Impact){$autoboot="$root/mk2ks_projectile_impact_probe.lua";$tracked+=$autoboot;$snapshotSize='400x254'}
if($Choreography){$autoboot="$root/mk2ks_projectile_choreography_probe.lua";$tracked+=@($autoboot,"$root/mk2ks_projectile_impact_probe.lua");$snapshotSize='400x254'}
if($Render){$autoboot="$root/mk2ks_projectile_render_probe.lua";$tracked+=@($autoboot,"$root/mk2ks_projectile_choreography_probe.lua","$root/mk2ks_projectile_impact_probe.lua");$snapshotSize='400x254'}
if($Bridge){$autoboot="$root/mk2ks_projectile_observer_bridge_probe.lua";$tracked+=@($autoboot,"$root/mk2ks_projectile_choreography_probe.lua","$root/mk2ks_projectile_impact_probe.lua");$snapshotSize='400x254'}
$hashes=[ordered]@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Target;$env:MK2KS_P2_FIGHTER='stock';$env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_PROJECTILE_CONTACT=$Scenario;$env:MK2KS_PROJECTILE_SIDE="$Side";$env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    if($Choreography -or $Render -or $Bridge){$env:MK2KS_PROJECTILE_CHOREOGRAPHY='1'}
    if($Bridge){$env:MK2KS_PROJECTILE_OBSERVER_ONLY='1'}
    & $exe mk2ks -rompath "$candidateRoot/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str 100 -snapsize $snapshotSize `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $autoboot 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed during case: $path"}}
    $log=Get-Content "$out/run.log" -Raw
    [ordered]@{exit_code=$code;target=$Target;side=$Side;candidate=$Candidate;scenario=$Scenario;observer_pass=$log.Contains('MK2_JOIN_LIFE_RESULT pass=true ');
        scope='cold_diagnostic_not_post_ending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code"
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
