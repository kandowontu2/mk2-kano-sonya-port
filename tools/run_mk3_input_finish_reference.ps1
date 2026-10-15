param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [ValidateSet('kano','sonya')][string]$Fighter='kano',
    [ValidateRange(70,180)][int]$Seconds=95
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
$exe=(Resolve-Path -LiteralPath (Join-Path $root '../hbmame/hbmame.exe')).Path
$harness=Join-Path $root 'mk3_fatality_asset_trace.lua'
$selection=Join-Path $root 'mk3_finish_input_selection.lua'
$verifier=Join-Path $PSScriptRoot 'verify_mk3_input_finish_reference.py'
if($Fighter -ne 'kano'){throw 'This first reference uses the native Kano/Sonya two-player route'}
$out=Join-Path $root "${CasePrefix}_${Fighter}"
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite reference evidence'}
$tracked=@($exe,$harness,$selection,$PSCommandPath,$verifier,
    (Join-Path $PSScriptRoot 'verify_kano_victim_sync.py'),(Join-Path $PSScriptRoot 'verify_skeleton_sync.py'),
    (Join-Path $root 'mk3/mk3-maincpu.bin'))
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_FATALITY_*'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try{
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_FATALITY_*'} | Remove-Item
    $env:MK3_FATALITY_FIGHTER=$Fighter
    $env:MK3_FATALITY_SELECTION_SCRIPT=$selection
    $env:MK3_FATALITY_INPUT_ONLY_APPROACH='1'
    $env:MK3_FATALITY_ASSET_TRACE='1'
    $env:MK3_FATALITY_OBJECT_TRACE='1'
    $env:MK3_FATALITY_INPUT_GATE_TRACE='1'
    $env:MK3_FATALITY_TRACE_START='3800'
    & $exe mk3 -rompath "$root;$root\..\mame0289\roms" -skip_gameinfo -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Reference input changed: $path"}}
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    & python $verifier "$out\run.log" | Out-File -LiteralPath "$out\input_reference_verification.json" -Encoding utf8
    $verified=$LASTEXITCODE -eq 0
    $passed=$verified -and $exitCode -eq 0 -and $log.Contains('MK3_FATALITY_INPUT_RESULT pass=true ') -and
        $log -match 'MK3_FATALITY_INPUT_RESULT[^\r\n]*position_writes=0 auto_cheat=false ' -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{passed=$passed;exit_code=$exitCode;fighter=$Fighter;seconds=$Seconds;assistance='round_health_only';position_writes_allowed=$false;automatic_fatality_cheat=$false;input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$out pass=$passed"
    if(-not $passed){throw 'Input-only original MK3 reference failed'}
}finally{
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_FATALITY_*'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
