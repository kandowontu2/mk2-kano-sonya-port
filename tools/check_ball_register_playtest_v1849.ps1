$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$candidate=Join-Path $root 'diagnostic_v1836_ball_register_boundary'
function Get-PlaytestSHA256([string]$Path){
    $stream=[IO.File]::OpenRead($Path)
    $sha=[Security.Cryptography.SHA256]::Create()
    try{return [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','')}
    finally{$stream.Dispose();$sha.Dispose()}
}
$manifest=Join-Path $candidate 'build-info.json'
if((Get-PlaytestSHA256 $manifest) -ne '16C70EFCAD6E176BECE5D2CE377A388765678729D632E55AAAB7C3D43F0B4B11'){
    throw 'Current tested build manifest changed.'
}
$build=Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json
if($build.name -ne 'diagnostic_v1836_ball_register_boundary' -or
   (Get-PlaytestSHA256 (Join-Path $candidate 'mkport_candidate.exe')) -ne '34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E' -or
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
