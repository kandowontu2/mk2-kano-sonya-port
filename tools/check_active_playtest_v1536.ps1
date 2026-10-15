$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $root 'diagnostic_v1517_active_launch_timer'
function Get-PlaytestSHA256([string]$Path){
    $stream=[IO.File]::OpenRead($Path)
    $sha=[Security.Cryptography.SHA256]::Create()
    try{return [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','')}
    finally{$stream.Dispose();$sha.Dispose()}
}
$manifest=Join-Path $candidate 'build-info.json'
if((Get-PlaytestSHA256 $manifest) -ne 'B6E7AC14813D7796BAF11DF9C9A2B278BF1DA96591659B279B9E3C642376AA1F'){
    throw 'Current tested build manifest changed.'
}
$build=Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json
if($build.name -ne 'diagnostic_v1517_active_launch_timer' -or
   (Get-PlaytestSHA256 (Join-Path $candidate 'mkport_candidate.exe')) -ne 'B0142C979C56C3906E8645D47CBE5CBE37D7AB33931A3447E3A6911DEC4911E8' -or
   (Get-PlaytestSHA256 (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata')) -ne '5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D'){
    throw 'Current tested executable/ROM pair is missing or changed.'
}
$sampleCount=0
foreach($item in $build.input_hashes.PSObject.Properties){
    if($item.Name -match '[\\/]samples[\\/]mk2ks[\\/]([^\\/]+\.wav)$'){
        $sample=Join-Path (Join-Path $root 'samples\mk2ks') $Matches[1]
        if((Get-PlaytestSHA256 $sample) -ne $item.Value){throw "Tested voice asset missing or changed: $sample"}
        $sampleCount++
    }
}
if($sampleCount -lt 16){throw 'Incomplete tested voice asset manifest.'}
exit 0
