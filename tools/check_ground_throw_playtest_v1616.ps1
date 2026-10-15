$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $root 'diagnostic_v1597_native_ground_throw'
function Get-PlaytestSHA256([string]$Path){
    $stream=[IO.File]::OpenRead($Path)
    $sha=[Security.Cryptography.SHA256]::Create()
    try{return [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','')}
    finally{$stream.Dispose();$sha.Dispose()}
}
$manifest=Join-Path $candidate 'build-info.json'
if((Get-PlaytestSHA256 $manifest) -ne 'AE9DC35933A60B60EC48A6C2005946862637B9B5B2F41A5650FCE7DE905C1512'){
    throw 'Current tested build manifest changed.'
}
$build=Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json
if($build.name -ne 'diagnostic_v1597_native_ground_throw' -or
   (Get-PlaytestSHA256 (Join-Path $candidate 'mkport_candidate.exe')) -ne '9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695' -or
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
