$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$out=Join-Path $root 'audit_v1851_ball_register_launcher_checked'
if(Test-Path -LiteralPath $out){throw 'Preserve existing evidence'}
$launcher=Join-Path $root 'PLAY_CURRENT_V1836_TEST_BUILD.cmd'
$checker=Join-Path $root 'tools\check_ball_register_playtest_v1849.ps1'
$candidate=Join-Path $root 'diagnostic_v1836_ball_register_boundary'
$reports=@('audit_v1837_ball_register_source_checked','audit_v1842_human_ball_p1_render_checked','audit_v1842_human_ball_p2_render_checked','audit_v1846_ball_register_special_matrix_checked')
$tracked=@((Join-Path $root 'PLAY_CURRENT_V1597_TEST_BUILD.cmd'),(Join-Path $root 'diagnostic_v1597_native_ground_throw\play\cfg\default.cfg'),(Join-Path $root 'diagnostic_v1597_native_ground_throw\play\cfg\mk2ks.cfg'),(Join-Path $root 'PLAY_LATEST_TEST_BUILD.cmd'),(Join-Path $root 'PLAY_MK2_KANO_SONYA.cmd'),$launcher,$checker,$PSCommandPath,(Join-Path $candidate 'mkport_candidate.exe'),
    (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata'),(Join-Path $candidate 'build-info.json'),
    (Join-Path $root 'PLAY_CURRENT_V1517_TEST_BUILD.cmd'),(Join-Path $root 'diagnostic_v1517_active_launch_timer\play\cfg\default.cfg'),(Join-Path $root 'diagnostic_v1517_active_launch_timer\play\cfg\mk2ks.cfg'),
    (Join-Path $root 'PLAY_CURRENT_V1411_TEST_BUILD.cmd'),(Join-Path $root 'tools\check_current_playtest_v1436.ps1'),
    (Join-Path $root 'diagnostic_v1411_native_grab_audio\play\cfg\default.cfg'),
    (Join-Path $root 'diagnostic_v1411_native_grab_audio\play\cfg\mk2ks.cfg'))
foreach($proof in $reports){
    $path=Join-Path $root "$proof\report.json"
    $report=Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
    if(-not $report.passed -or $report.candidate -ne 'diagnostic_v1836_ball_register_boundary'){throw "Regression not accepted: $proof"}
    $tracked+=$path
}
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
New-Item -ItemType Directory -Path $out | Out-Null
$oldLocation=Get-Location
try{
    Set-Location -LiteralPath (Split-Path $root -Parent)
    & $launcher -video none -sound none -str 8 -nothrottle 2>&1 | Out-File (Join-Path $out 'run.log') -Encoding utf8
    $code=$LASTEXITCODE
}finally{Set-Location -LiteralPath $oldLocation.Path}
foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Changed launch input: $file"}}
$log=Get-Content -LiteralPath (Join-Path $out 'run.log') -Raw
$passed=$code -eq 0 -and $log -notmatch 'WRONG CHECKSUMS|might not run correctly|\[LUA ERROR\]|fatal error|access violation'
[ordered]@{passed=$passed;exit_code=$code;candidate='diagnostic_v1836_ball_register_boundary';
    launcher=$launcher;ordinary_boot_from_other_working_directory=$true;seconds=8;
    diagnostic_autoboot_used=$false;older_launchers_changed=$false;older_control_settings_changed=$false;settings_isolated=$true;
    repeatedCPUFixtureAccepted=$false;bothSlotsSquareInterruptionAccepted=$false;
    scope='matched_CMD_and_external_voice_asset_boot_smoke_not_full_interactive_audio_campaign_or_release_acceptance';
    inputHashes=$hashes;fullPortAccepted=$false} | ConvertTo-Json -Depth 4 | Out-File (Join-Path $out 'report.json') -Encoding utf8
if(-not $passed){throw "Ordinary current CMD boot failed: $code"}
'Current v1836 CMD boot passed; previous CMD and controls preserved.'
