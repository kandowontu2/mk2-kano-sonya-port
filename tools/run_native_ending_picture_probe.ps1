param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$CandidateName,
    [Parameter(Mandatory=$true)][string]$OracleDirectory,
    [ValidateSet('ending','battle')][string]$PictureKind='ending'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$exe=Join-Path $root "$CandidateName/mkport_candidate.exe"
$payload=Join-Path $root "$CandidateName/roms/mk2ks/mk2ks.mdata"
$oracle=(Resolve-Path -LiteralPath $OracleDirectory).Path
$harness=Join-Path $root $(if($PictureKind -eq 'battle'){'mk2ks_battle_pictures_test.lua'}else{'mk2ks_ending_pictures_test.lua'})
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$tracked=@($exe,$payload,$harness,$PSCommandPath,(Join-Path $PSScriptRoot 'build_native_ending_reference.py'),
    (Join-Path $PSScriptRoot 'decode_native_picture.py'),(Join-Path $PSScriptRoot 'upgrade_ksui_previews.py'))
$tracked+=Get-ChildItem -LiteralPath $oracle -File | Select-Object -ExpandProperty FullName
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$prior=$env:MK2KS_ENDING_PICTURE_REFERENCE
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    $env:MK2KS_ENDING_PICTURE_REFERENCE=$oracle
    & $exe mk2ks -rompath "$root/$CandidateName/roms;$root/roms" -verifyroms
    if($LASTEXITCODE -ne 0){throw 'ROM verification failed'}
    & $exe mk2ks -rompath "$root/$CandidateName/roms;$root/roms" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str 10 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -autoboot_script $harness 2>&1 |
        Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $marker=if($PictureKind -eq 'battle'){'MK2KS_BATTLE_PICTURE_RESULT pass=true '}else{'MK2KS_ENDING_PICTURE_RESULT pass=true '}
    $passed=$exitCode -eq 0 -and $log.Contains($marker) -and
        $log -notmatch '(?i)fatal error|\[LUA ERROR\]|exception at|access violation'
    [ordered]@{passed=$passed;exit_code=$exitCode;cheats_enabled=$false;writes=0;
        scope="${PictureKind}_photo_record_pixels_and_palettes_not_runtime_rendering";input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Get-Content -LiteralPath "$out/run.log"
    if(-not $passed){throw 'Original ending photo record verification failed'}
} finally {
    Pop-Location
    if($null -eq $prior){Remove-Item Env:MK2KS_ENDING_PICTURE_REFERENCE -ErrorAction SilentlyContinue}
    else {$env:MK2KS_ENDING_PICTURE_REFERENCE=$prior}
}
