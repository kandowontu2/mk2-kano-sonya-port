param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateSet('freeze','shock')][string]$Effect='freeze',
    [ValidateSet('kano','sonya','cage')][string]$Victim='kano',
    [ValidateSet(1,2)][int]$Side=1,
    [string]$CandidateName='diagnostic_v272_blue_palette_trial'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned candidate'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$rompath=Join-Path $candidate 'roms'
$harness=Join-Path $root 'mk2ks_blue_palette_test.lua'
$tracked=@($exe,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),$harness,$PSCommandPath,
    (Join-Path $root 'mk2ks_selector_exit_test.lua'))
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_)'} | Remove-Item
    $attacker=if($Effect -eq 'freeze'){'sub_zero'}else{'raiden'}
    $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){$Victim}else{$attacker}
    $env:MK2KS_P2_FIGHTER=if($Side -eq 2){$Victim}else{$attacker}
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2KS_BLUE_EFFECT=$Effect;$env:MK2KS_BLUE_VICTIM=$Victim;$env:MK2KS_BLUE_SIDE="$Side"
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -video none -sound none -nothrottle -str 48 -snapsize 400x300 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $passed=$exitCode -eq 0 -and $log.Contains('MK2_BLUE_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{passed=$passed;effect=$Effect;victim=$Victim;side=$Side;exit_code=$exitCode;
        cheats_enabled=$false;assistance='none';scope='native_shock_freeze_palette';input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed"
    if(-not $passed){throw 'Native blue palette case failed'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
