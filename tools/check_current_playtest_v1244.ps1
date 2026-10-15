$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $root 'diagnostic_v1219_owned_native_headed_reaction'
$build=Get-Content -LiteralPath (Join-Path $candidate 'build-info.json') -Raw | ConvertFrom-Json
$expectedExe='C9742947468338618044B97922D8106231CE6710208111BCB2C90518AFF7130F'
$expectedPayload='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D'
if($build.name -ne 'diagnostic_v1219_owned_native_headed_reaction' -or
   $build.executable_sha256 -ne $expectedExe -or $build.payload_sha256 -ne $expectedPayload){
    throw 'Current test build manifest does not match the tested candidate.'
}
if((Get-FileHash -LiteralPath (Join-Path $candidate 'mkport_candidate.exe')).Hash -ne $expectedExe -or
   (Get-FileHash -LiteralPath (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata')).Hash -ne $expectedPayload){
    throw 'Current test executable or ROM payload is missing or changed.'
}
exit 0
