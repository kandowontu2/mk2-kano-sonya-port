param([string]$CaseName='audit_v735_original_babality_directions')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[A-Za-z0-9_-]+$'){throw 'Use a simple case name'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite reference'}
$exe=(Resolve-Path -LiteralPath (Join-Path $root '../hbmame/hbmame.exe')).Path
$harness=Join-Path $root 'mk3_babality_direction_reference_v735.lua'
$inputs=@($exe,$harness,$PSCommandPath,(Join-Path $root 'mk3_finish_input_selection.lua'),(Join-Path $root 'mk3/mk3-maincpu.bin'))
$hashes=@{}
foreach($path in $inputs){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path $out | Out-Null
$hashes | ConvertTo-Json | Out-File -LiteralPath "$out/inputs_before.json" -Encoding utf8
Copy-Item -LiteralPath $harness -Destination $out
Copy-Item -LiteralPath $PSCommandPath -Destination $out
Copy-Item -LiteralPath (Join-Path $root 'mk3_finish_input_selection.lua') -Destination $out
Push-Location $root
try{
    & $exe mk3 -rompath "$root;$root\..\mame0289\roms" -skip_gameinfo -nocheat -video none -sound none -nothrottle -str 120 -snapsize 400x300 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $inputs){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $pass=$exitCode -eq 0 -and $log.Contains('MK3_BABA_REFERENCE_RESULT ram_writes=0 cheats=false finished=true') -and $log -notmatch '(?i)\[LUA ERROR\]|fatal error|exception at|access violation'
    [ordered]@{passed=$pass;exit_code=$exitCode;ram_writes=0;cheats=$false;scope='original MK3 command routing only';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$out pass=$pass"
    if(-not $pass){throw 'Original command reference failed'}
}finally{Pop-Location}
