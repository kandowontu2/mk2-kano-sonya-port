$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$out=Join-Path $root 'audit_v1537_active_launcher_checked'
if(Test-Path -LiteralPath $out){throw 'Preserve existing evidence'}
$launcher=Join-Path $root 'PLAY_CURRENT_V1517_TEST_BUILD.cmd'
$checker=Join-Path $root 'tools\check_active_playtest_v1536.ps1'
$candidate=Join-Path $root 'diagnostic_v1517_active_launch_timer'
$reports=@('audit_v1520_active_launch_timer_checked','audit_v1522_active_launch_ui_checked','audit_v1523_active_launch_ground_shadow_checked','audit_v1524_active_launch_human_matrix_checked','audit_v1525_active_launch_cpu_display_checked','audit_v1535_active_launch_interruption_checked')
$tracked=@($launcher,$checker,$PSCommandPath,(Join-Path $candidate 'mkport_candidate.exe'),
    (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata'),(Join-Path $candidate 'build-info.json'),
    (Join-Path $root 'PLAY_CURRENT_V1411_TEST_BUILD.cmd'),(Join-Path $root 'tools\check_current_playtest_v1436.ps1'),
    (Join-Path $root 'diagnostic_v1411_native_grab_audio\play\cfg\default.cfg'),
    (Join-Path $root 'diagnostic_v1411_native_grab_audio\play\cfg\mk2ks.cfg'))
foreach($proof in $reports){
    $path=Join-Path $root "$proof\report.json"
    $report=Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
    if(-not $report.passed -or $report.candidate -ne 'diagnostic_v1517_active_launch_timer'){throw "Regression not accepted: $proof"}
    $tracked+=$path
}
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
New-Item -ItemType Directory -Path $out | Out-Null
$oldLocation=Get-Location
try{
    Set-Location -LiteralPath (Split-Path $root -Parent)
    & $launcher -video none -sound none -str 2 -nothrottle 2>&1 | Out-File (Join-Path $out 'run.log') -Encoding utf8
    $code=$LASTEXITCODE
}finally{Set-Location -LiteralPath $oldLocation.Path}
foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Changed launch input: $file"}}
$log=Get-Content -LiteralPath (Join-Path $out 'run.log') -Raw
$passed=$code -eq 0 -and $log -notmatch 'WRONG CHECKSUMS|might not run correctly|\[LUA ERROR\]|fatal error|access violation'
[ordered]@{passed=$passed;exit_code=$code;candidate='diagnostic_v1517_active_launch_timer';
    launcher=$launcher;ordinary_boot_from_other_working_directory=$true;seconds=2;
    diagnostic_autoboot_used=$false;older_launchers_changed=$false;older_control_settings_changed=$false;settings_isolated=$true;
    repeatedCPUFixtureAccepted=$false;bothSlotsSquareInterruptionAccepted=$false;
    scope='matched_CMD_and_external_voice_asset_boot_smoke_not_full_interactive_audio_campaign_or_release_acceptance';
    inputHashes=$hashes;fullPortAccepted=$false} | ConvertTo-Json -Depth 4 | Out-File (Join-Path $out 'report.json') -Encoding utf8
if(-not $passed){throw "Ordinary current CMD boot failed: $code"}
'Current v1517 CMD boot passed; previous CMD and controls preserved.'
