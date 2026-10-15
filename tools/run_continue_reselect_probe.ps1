param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kano','sonya','liu_kang')][string]$Fighter='kano',
    [ValidateSet('sub_zero','kano','sonya')][string]$Target='sub_zero'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence case name'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
New-Item -ItemType Directory -Path $out | Out-Null
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Fighter
    $env:MK2KS_RESELECT_TARGET=$Target
    $env:MK2KS_P2_FIGHTER='stock'
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_ROUND_WIN=if($Fighter -eq 'liu_kang'){'0'}else{'1'}
    $env:MK2KS_ALLOW_NATURAL_LOSS='1'
    $env:MK2KS_ALLOW_CONTINUE_RESELECT='1'
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
    if($Fighter -ne 'liu_kang'){$env:MK2KS_ASSERT_HUD_SHADOW='1'}
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
        -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
        -str 250 -snapsize 400x300 -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" `
        -snapshot_directory "$out\snap" -autoboot_script "$root\mk2ks_continue_reselect_probe.lua" `
        2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    $targetId=switch($Target){'sub_zero'{8} 'kano'{17} 'sonya'{18}}
    $passed=$LASTEXITCODE -eq 0 -and
        $log -match 'MK2KS_CONTINUE_LOSS frame=' -and
        ($Fighter -eq 'liu_kang' -or $log -match 'MK2KS_CAMPAIGN_CONTINUED frame=') -and
        $log -match "MK2KS_RESELECT_MATCH frame=\d+ target=$Target id=$targetId " -and
        $log -match "MK2KS_RESELECT_COMBAT frame=\d+ target=$Target id=$targetId actor=$targetId" -and
        ($Target -eq 'sub_zero' -or $log -match "MK2KS_RESELECT_SHADOW target=$Target matched=\d+ expected=\d+ pass=true") -and
        $log -match 'MK2KS_EXIT_RESULT pass=true ' -and
        $log -match 'MK2KS_DISPLAY_RESULT pass=true ' -and
        ($Fighter -eq 'liu_kang' -or $log -match 'MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0'
    if(-not $passed){throw 'Continue reselect did not pass lifecycle checks'}
    [ordered]@{fighter=$Fighter;target=$Target;executable_sha256=(Get-FileHash $Executable).Hash;
        payload_sha256=(Get-FileHash (Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata')).Hash;
        passed=$passed} |
        ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed"
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
