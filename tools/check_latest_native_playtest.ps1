$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskCandidate = Join-Path $taskRoot 'diagnostic_native_cpu_finisher_spacing'
function Get-LatestPlaytestSHA256([string]$Path) {
    $taskStream = [IO.File]::OpenRead($Path)
    $taskHash = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($taskHash.ComputeHash($taskStream)).Replace('-', '') }
    finally { $taskStream.Dispose(); $taskHash.Dispose() }
}
function Assert-LatestPlaytestHash([string]$Path, [string]$Expected) {
    if ((Get-LatestPlaytestSHA256 $Path) -ne $Expected) {
        throw "Latest checked playtest file is changed: $Path"
    }
}
$taskManifest = Join-Path $taskCandidate 'build-info.json'
Assert-LatestPlaytestHash $taskManifest '3770A7285088541D2330E975A56849C794AB525F336552060C0B7508E4A1C2D8'
$taskBuild = Get-Content -LiteralPath $taskManifest -Raw | ConvertFrom-Json
$taskExpectedExe = 'D2BCD3908BE847561A1F980586F2ECC89CAB4D7FFB56C22EC63B30584DC3C53D'
$taskExpectedPayload = 'A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
$taskExpectedGuest = '65BF7919A99073B0235FDA82B40078FF1663D16236522F088462361404F5648D'
if ($taskBuild.name -ne 'diagnostic_native_cpu_finisher_spacing' -or
    $taskBuild.executable_sha256 -ne $taskExpectedExe -or
    $taskBuild.payload_sha256 -ne $taskExpectedPayload -or
    $taskBuild.expected_guest_sha256 -ne $taskExpectedGuest) {
    throw 'Latest manifest does not identify the actually tested EXE/guest/payload.'
}
Assert-LatestPlaytestHash (Join-Path $taskCandidate 'mkport_candidate.exe') $taskExpectedExe
Assert-LatestPlaytestHash (Join-Path $taskCandidate 'roms\mk2ks\mk2ks.mdata') $taskExpectedPayload
Assert-LatestPlaytestHash (Join-Path $taskRoot 'roms\mk2.zip') 'B9867A2D5F20D27A2E27FDC9799E44BE7FB6269948DBC1BE8EF53A8CB4C79EDD'
Assert-LatestPlaytestHash (Join-Path $taskRoot 'roms\mk2ks.zip') 'C0EDD2B71C70604A6FDB049D0279CF0110002ADCB19A58C000D8D36BDF7D5DAE'

# These immutable finite runtime receipts prove both latest CPU finisher fixes.
# They do not assert completion of every arena, cinematic or audio context.
$taskChecks = @{
    'audit_native_cpu_finisher_spacing_child_checked\report.json' = '35B9495B3F753C8353EDA05970E413D2931C7DEFAEDB91E2F0A4FF13C0A4C8DD'
    'audit_native_sonya_cpu_finisher_checked\report.json' = 'D285957FC1070E062ED964A113CCCE769171FB6A747B2B4979CFEC112821EAD4'
    'audit_native_current_ui_owned_checked\report.json' = 'FB7A9B9E6DF4D85507779CC4E80CE0AE2E0BA9588DF8431E4BF53326D63A03B5'
}
foreach ($taskPair in $taskChecks.GetEnumerator()) {
    $taskReport = Join-Path $taskRoot $taskPair.Key
    Assert-LatestPlaytestHash $taskReport $taskPair.Value
    $taskAcceptance = Get-Content -LiteralPath $taskReport -Raw | ConvertFrom-Json
    if (-not $taskAcceptance.passed) { throw 'A required finite native runtime receipt is not accepted.' }
}

# Resolve each waveform as MAME's ordered samplepath does: latest overlay first,
# then the shared set. Ignore repeated historical pins only when hashes agree.
$taskSamples = @{}
foreach ($taskItem in $taskBuild.input_hashes.PSObject.Properties) {
    if ($taskItem.Name -match '[\\/]samples[\\/]mk2ks[\\/]([^\\/]+\.wav)$') {
        $taskLeaf = $Matches[1]
        if ($taskSamples.ContainsKey($taskLeaf) -and $taskSamples[$taskLeaf] -ne $taskItem.Value) {
            throw "Conflicting compiled waveform provenance: $taskLeaf"
        }
        $taskSamples[$taskLeaf] = $taskItem.Value
    }
}
if ($taskSamples.Count -ne 17) { throw 'The complete seventeen-waveform current sample set is required.' }
foreach ($taskLeaf in $taskSamples.Keys) {
    $taskSample = Join-Path (Join-Path $taskCandidate 'samples\mk2ks') $taskLeaf
    if (-not (Test-Path -LiteralPath $taskSample -PathType Leaf)) {
        $taskSample = Join-Path (Join-Path $taskRoot 'samples\mk2ks') $taskLeaf
    }
    Assert-LatestPlaytestHash $taskSample $taskSamples[$taskLeaf]
}
Write-Output 'Latest checked EXE, ROM assets, native runtime receipts and all seventeen waveforms match.'
Write-Output 'Checked playtest: remaining integration and finished release verification are still in progress.'
