param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateSet('kano','sonya','kitana','jax')][string]$Fighter='kano',
    [ValidateSet('kano','sonya','kitana','jax')][string]$Opponent='sonya',
    [string]$CandidateName='diagnostic_v277_native_battle_photos'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$exe=Join-Path $root "$CandidateName/mkport_candidate.exe"
$rompath=Join-Path $root "$CandidateName/roms"
$harness=Join-Path $root 'mk2ks_battle_native_acceptance.lua'
$tracked=@($exe,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),$harness,$PSCommandPath,
    (Join-Path $root 'mk2ks_battle_card_probe.lua'),(Join-Path $root 'mk2ks_selector_exit_test.lua'),
    (Join-Path $root 'mk2ks_native_shang_morph.lua'))
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Fighter;$env:MK2KS_P2_FIGHTER=$Opponent;$env:MK2KS_TWO_PLAYER='1'
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
    $addedCharacter=$Fighter -in @('kano','sonya') -or $Opponent -in @('kano','sonya')
    if($addedCharacter){$env:MK2KS_ASSERT_HUD_SHADOW='1'}
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str 35 -snapsize 400x300 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $missing=@(1040..1220 | Where-Object {$_%10 -eq 0} | Where-Object {-not (Test-Path -LiteralPath (Join-Path $out ('snap/battle_card_frame{0:d4}.png' -f $_)))})
    $passed=$exitCode -eq 0 -and $missing.Count -eq 0 -and $log.Contains('MK2KS_BATTLE_NATIVE_RESULT pass=true ') -and
        $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        (-not $addedCharacter -or $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ')) -and
        $log -notmatch '(?i)fatal error|\[LUA ERROR\]|exception at|access violation'
    [ordered]@{passed=$passed;exit_code=$exitCode;fighter=$Fighter;opponent=$Opponent;cheats_enabled=$false;
        writes=0;scope='ordinary_selection_native_battle_render_and_first_combat_not_full_campaign';
        missing_snapshots=$missing;input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed"
    if(-not $passed){throw 'BATTLE photo acceptance failed; preserve evidence'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
