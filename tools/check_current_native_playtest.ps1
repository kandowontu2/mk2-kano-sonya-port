$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskCandidate = Join-Path $taskRoot 'diagnostic_native_selector_layers_long'
function Assert-CurrentHash([string]$Path, [string]$Expected) {
    $taskStream = [IO.File]::OpenRead($Path)
    $taskHasher = [Security.Cryptography.SHA256]::Create()
    try { $taskActual = [BitConverter]::ToString($taskHasher.ComputeHash($taskStream)).Replace('-', '') }
    finally { $taskStream.Dispose(); $taskHasher.Dispose() }
    if ($taskActual -ne $Expected) {
        throw "Current playtest file missing or changed: $Path"
    }
}
Assert-CurrentHash (Join-Path $taskCandidate 'build-info.json') 'F06150835A253E079449F6C1234509F3640B25A81284900C84B912EE45B309F1'
$taskBuild = Get-Content -LiteralPath (Join-Path $taskCandidate 'build-info.json') -Raw | ConvertFrom-Json
if ($taskBuild.name -ne 'diagnostic_native_selector_layers_long' -or $taskBuild.total_sample_channels -ne 19) {
    throw 'Unexpected current build identity.'
}
Assert-CurrentHash (Join-Path $taskCandidate 'mkport_candidate.exe') 'EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A'
Assert-CurrentHash (Join-Path $taskCandidate 'roms\mk2ks\mk2ks.mdata') 'A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
Assert-CurrentHash (Join-Path $taskRoot 'roms\mk2.zip') 'B9867A2D5F20D27A2E27FDC9799E44BE7FB6269948DBC1BE8EF53A8CB4C79EDD'
Assert-CurrentHash (Join-Path $taskRoot 'roms\mk2ks.zip') 'C0EDD2B71C70604A6FDB049D0279CF0110002ADCB19A58C000D8D36BDF7D5DAE'
$taskSamples = @{}
foreach ($taskItem in $taskBuild.input_hashes.PSObject.Properties) {
    if ($taskItem.Name -match '[\\/]([^\\/]+\.wav)$') {
        $taskLeaf = $Matches[1]
        if ($taskSamples.ContainsKey($taskLeaf) -and $taskSamples[$taskLeaf] -ne $taskItem.Value) {
            throw "Conflicting sound provenance: $taskLeaf"
        }
        $taskSamples[$taskLeaf] = $taskItem.Value
    }
}
if ($taskSamples.Count -ne 23) { throw 'Expected all 23 current waveform assets.' }
foreach ($taskLeaf in $taskSamples.Keys) {
    $taskSample = Join-Path $taskCandidate "samples\mk2ks\$taskLeaf"
    if (-not (Test-Path -LiteralPath $taskSample -PathType Leaf)) {
        $taskSample = Join-Path $taskRoot "samples\mk2ks\$taskLeaf"
    }
    Assert-CurrentHash $taskSample $taskSamples[$taskLeaf]
}
# Ask the actual executable to resolve and audit the same ROM search path
# used for ordinary play. Hashes alone do not prove complete ROM resolution.
$taskAudit = & (Join-Path $taskCandidate 'mkport_candidate.exe') mk2ks -rompath "$taskCandidate/roms;$taskRoot/roms" -verifyroms 2>&1
$taskAuditExit = $LASTEXITCODE
if ($taskAuditExit -ne 0 -or ($taskAudit -join "`n") -notmatch '1 romsets found, 1 were OK\.') {
    throw "Current native ROM audit failed: $($taskAudit -join ' ')"
}
Write-Output 'Current tested executable, ROM assets and all 23 sound files match.'
Write-Output 'Native ROM audit: complete mk2ks ROM set is good, with no checksum warning.'
Write-Output 'File checks passed. Release acceptance is documented separately in RELEASE.json.'
