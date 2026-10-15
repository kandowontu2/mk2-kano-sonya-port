$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $root 'diagnostic_v1411_native_grab_audio'
$build=Get-Content -LiteralPath (Join-Path $candidate 'build-info.json') -Raw | ConvertFrom-Json
$expectedExe='01EF3950691A890BAA41723D99935E44A28B09A7431EA78EC5DBF8E0E90630C3'
$expectedPayload='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D'
function Get-PlaytestSHA256([string]$Path){
    # Windows PowerShell launched by CMD need not inherit PowerShell 7 modules.
    $stream=[IO.File]::OpenRead($Path)
    $sha=[Security.Cryptography.SHA256]::Create()
    try{return [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','')}
    finally{$stream.Dispose();$sha.Dispose()}
}
if($build.name -ne 'diagnostic_v1411_native_grab_audio' -or
   $build.executable_sha256 -ne $expectedExe -or $build.payload_sha256 -ne $expectedPayload){
    throw 'Current test build manifest does not match the tested candidate.'
}
if((Get-PlaytestSHA256 (Join-Path $candidate 'mkport_candidate.exe')) -ne $expectedExe -or
   (Get-PlaytestSHA256 (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata')) -ne $expectedPayload){
    throw 'Current test executable or ROM payload is missing or changed.'
}
exit 0
