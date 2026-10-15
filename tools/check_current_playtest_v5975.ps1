$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskCandidate = Join-Path $taskRoot 'diagnostic_v5219_current_payload_rom_metadata'
function Get-PlaytestSHA256([string]$Path) {
    # Works in Windows PowerShell without inheriting PowerShell 7 modules.
    $taskStream = [IO.File]::OpenRead($Path)
    $taskHash = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($taskHash.ComputeHash($taskStream)).Replace('-', '') }
    finally { $taskStream.Dispose(); $taskHash.Dispose() }
}
$taskManifest = Join-Path $taskCandidate 'build-info.json'
if ((Get-PlaytestSHA256 $taskManifest) -ne '72F19E2E6CA566B6D4EF99C092831E8D988F97A037A32E8372B576519A18E526') {
    throw 'The tested build manifest is missing or changed.'
}
$taskBuild = Get-Content -LiteralPath $taskManifest -Raw | ConvertFrom-Json
$taskExpectedExe = 'A6BC32F526C78A5BD72ED1960EAE56AB40701D7FE881D70A93E031AEB87AB944'
$taskExpectedPayload = 'A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
if ($taskBuild.name -ne 'diagnostic_v5219_current_payload_rom_metadata' -or
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
Write-Output 'Checked v5219 executable, ROM payload and all sixteen voice assets.'
