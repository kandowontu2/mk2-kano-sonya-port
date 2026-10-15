param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [ValidateRange(90,150)][int]$Seconds=110
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$out=Join-Path $root $CasePrefix
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite original reference evidence'}
$exe=(Resolve-Path -LiteralPath (Join-Path $root '../hbmame/hbmame.exe')).Path
$harness=Join-Path $root 'mk3_sonya_contact_capture.lua'
$selection=Join-Path $root 'mk3_sonya_finish_input_selection.lua'
$verifier=Join-Path $PSScriptRoot 'verify_sonya_contact_reference.py'
$tracked=@($exe,$harness,$selection,$verifier,$PSCommandPath,
    (Join-Path $root 'mk3_fatality_asset_trace.lua'),(Join-Path $root 'mk3/mk3-maincpu.bin'))
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_FATALITY_*'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_FATALITY_*'} | Remove-Item
    $env:MK3_FATALITY_FIGHTER='sonya';$env:MK3_FATALITY_SELECTION_SCRIPT=$selection
    $env:MK3_FATALITY_INPUT_ONLY_APPROACH='1';$env:MK3_FATALITY_ASSET_TRACE='1'
    $env:MK3_FATALITY_OBJECT_TRACE='1';$env:MK3_FATALITY_TRACE_START='3800'
    & $exe mk3 -rompath "$root;$root/../mame0289/roms" -skip_gameinfo -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Original reference input changed: $path"}}
    & python $verifier "$out/run.log" | Out-File -LiteralPath "$out/trajectory_verification.json" -Encoding utf8
    $passed=$exitCode -eq 0 -and $LASTEXITCODE -eq 0
    [ordered]@{passed=$passed;scope='original_projectile_physics_not_port_or_full_input_acceptance';
        original_input_gate_validation_complete=$false;exit_code=$exitCode;seconds=$Seconds;
        assistance='round_health_only';position_writes_allowed=$false;automatic_fatality_cheat=$false;
        input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$out trajectory_reference_pass=$passed"
    if(-not $passed){throw 'Original Sonya projectile reference failed'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_FATALITY_*'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
