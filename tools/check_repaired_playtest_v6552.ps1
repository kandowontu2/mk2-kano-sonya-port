$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskCandidate = Join-Path $taskRoot 'diagnostic_v6508_native_projectile_identifiers'
function Get-PlaytestSHA256([string]$Path) {
    $taskStream = [IO.File]::OpenRead($Path)
    $taskHash = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($taskHash.ComputeHash($taskStream)).Replace('-', '') }
    finally { $taskStream.Dispose(); $taskHash.Dispose() }
}
$taskManifest = Join-Path $taskCandidate 'build-info.json'
if ((Get-PlaytestSHA256 $taskManifest) -ne '6501AC50794C1F3A2658FE464BF42C64D9844C424127B4AB51874813779B6CE4') {
    throw 'The tested build manifest is missing or changed.'
}
# Build metadata is immutable compile-time provenance. Later runtime acceptance
# is recorded separately; this is a checked playtest, not a finished release.
$taskAcceptance = Join-Path $taskRoot 'audit_v6558_repaired_projectile_storage\report.json'
if ((Get-PlaytestSHA256 $taskAcceptance) -ne '53EB5454A8F69CE7FD99BAF42CDC8A1654AB1B1B8F0B74B0B5C00BA665AEAA52') {
    throw 'The repaired-build runtime qualification is missing or changed.'
}
$taskBuild = Get-Content -LiteralPath $taskManifest -Raw | ConvertFrom-Json
$taskExpectedExe = '2FBD8BECEC0E4F673647B936976343D1CE47A8B5D5206C26C12355E9D7874334'
$taskExpectedPayload = 'A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
if ($taskBuild.name -ne 'diagnostic_v6508_native_projectile_identifiers' -or
    $taskBuild.executable_sha256 -ne $taskExpectedExe -or $taskBuild.payload_sha256 -ne $taskExpectedPayload) {
    throw 'The manifest does not identify the tested executable/ROM pair.'
}
if ((Get-PlaytestSHA256 (Join-Path $taskCandidate 'mkport_candidate.exe')) -ne $taskExpectedExe -or
    (Get-PlaytestSHA256 (Join-Path $taskCandidate 'roms\mk2ks\mk2ks.mdata')) -ne $taskExpectedPayload) {
    throw 'The tested executable or ROM payload is missing or changed.'
}
$taskSampleCount = 0
foreach ($taskItem in $taskBuild.input_hashes.PSObject.Properties) {
    if ($taskItem.Name -match '[\\/]samples[\\/]mk2ks[\\/]([^\\/]+\.wav)$') {
        $taskSample = Join-Path (Join-Path $taskRoot 'samples\mk2ks') $Matches[1]
        if ((Get-PlaytestSHA256 $taskSample) -ne $taskItem.Value) {
            throw "Tested voice asset missing or changed: $taskSample"
        }
        $taskSampleCount++
    }
}
if ($taskSampleCount -ne 16) { throw 'The complete tested sixteen-voice asset set is required.' }
Write-Output 'Checked v6508 executable, ROM payload and all sixteen voice assets.'
