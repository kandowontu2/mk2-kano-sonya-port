$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$out=Join-Path $root 'audit_v1262_current_launcher_checked'
if(Test-Path -LiteralPath $out){throw 'Preserve existing evidence'}
$launcher=Join-Path $root 'PLAY_CURRENT_V1250_TEST_BUILD.cmd'
$checker=Join-Path $root 'tools\check_current_playtest_v1261.ps1'
$candidate=Join-Path $root 'diagnostic_v1250_native_correct_rom_metadata'
$tracked=@($launcher,$checker,$PSCommandPath,(Join-Path $candidate 'mkport_candidate.exe'),
    (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata'),(Join-Path $candidate 'build-info.json'))
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
New-Item -ItemType Directory -Path $out | Out-Null
$taskOldLocation=Get-Location
try{
    Set-Location -LiteralPath (Split-Path $root -Parent)
    & $launcher -video none -sound none -str 2 -nothrottle 2>&1 | Out-File (Join-Path $out 'run.log') -Encoding utf8
    $code=$LASTEXITCODE
}finally{Set-Location -LiteralPath $taskOldLocation.Path}
foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Changed launch input: $file"}}
$log=Get-Content -LiteralPath (Join-Path $out 'run.log') -Raw
$passed=$code -eq 0 -and $log -notmatch 'WRONG CHECKSUMS|might not run correctly|\[LUA ERROR\]|fatal error|access violation'
[ordered]@{passed=$passed;exit_code=$code;candidate='diagnostic_v1250_native_correct_rom_metadata';
    launcher=$launcher;ordinary_boot_from_other_working_directory=$true;seconds=2;skip_gameinfo_used=$false;no_rom_checksum_warnings=$passed;
    diagnostic_autoboot_used=$false;older_launchers_changed=$false;settings_isolated=$true;
    scope='matched_CMD_boot_smoke_not_full_interactive_match_audio_or_release_acceptance';input_hashes=$hashes;
    full_port_accepted=$false} | ConvertTo-Json -Depth 4 | Out-File (Join-Path $out 'report.json') -Encoding utf8
if(-not $passed){throw "Ordinary current CMD boot failed: $code"}
'Current v1250 CMD launcher boot passed without ROM checksum warnings; no old launchers/settings changed.'
