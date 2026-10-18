param(
    [ValidateSet('game','finish','root','asm','art','cycle','sound-info','sound','clean','sound-clean')]
    [string]$Target = 'game'
)
$ErrorActionPreference = 'Stop'
$configPath = Join-Path $PSScriptRoot ('dosbox-' + $Target + '.conf')
$romhackPath = Split-Path -Parent $PSScriptRoot
$executablePath = Join-Path $romhackPath 'toolchain/dosbox-x/mingw-build/mingw/dosbox-x.exe'
if (!(Test-Path -LiteralPath $executablePath)) { throw 'Bundled DOSBox-X is missing.' }
if ((Get-Content -Raw -LiteralPath $configPath) -notmatch '(?m)^videodriver=dummy\s*$') {
    throw 'Refusing a compilation configuration without the headless video driver.'
}
$startInfo = [System.Diagnostics.ProcessStartInfo]::new()
$startInfo.FileName = $executablePath
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
# Enforce the driver before SDL startup as well as in DOSBox's configuration.
$startInfo.Environment['SDL_VIDEODRIVER'] = 'dummy'
$startInfo.Environment['SDL_AUDIODRIVER'] = 'dummy'
foreach ($argument in @('-conf', $configPath, '-fastlaunch', '-exit')) {
    $startInfo.ArgumentList.Add($argument)
}
$buildProcess = [System.Diagnostics.Process]::Start($startInfo)
$standardOutput = $buildProcess.StandardOutput.ReadToEndAsync()
$standardError = $buildProcess.StandardError.ReadToEndAsync()
$started = Get-Date
$windowChecks = 0
try {
    try { $buildProcess.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal } catch {}
    while (!$buildProcess.WaitForExit(100)) {
        $buildProcess.Refresh()
        if ($buildProcess.HasExited) { break }
        # DOSBox can apply its own startup priority after Process.Start.
        # Keep the user's background-build priority throughout compilation.
        if ($buildProcess.PriorityClass -ne [System.Diagnostics.ProcessPriorityClass]::BelowNormal) {
            $buildProcess.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
        }
        $windowChecks++
        if ($buildProcess.MainWindowHandle -ne [IntPtr]::Zero) {
            throw 'The supposedly headless compiler created a window; refusing to continue.'
        }
        if (((Get-Date) - $started).TotalSeconds -gt 180) {
            throw 'Background compilation exceeded its bounded runtime.'
        }
    }
    $stdout = $standardOutput.GetAwaiter().GetResult()
    $stderr = $standardError.GetAwaiter().GetResult()
    if ($buildProcess.ExitCode -ne 0) {
        throw ('Headless DOSBox failed. ' + $stdout + $stderr)
    }
    $basePath = Join-Path $romhackPath 'baseline/mk2-rebuild-main'
    if ($Target -in @('clean','sound-clean')) { $basePath = Join-Path $romhackPath 'baseline/clean_program' }
    $successName = switch ($Target) { 'sound-clean' {'SP_OK.TXT'} 'clean' {'POK.TXT'} 'game' {'POK.TXT'} 'finish' {'FOK.TXT'} 'sound' {'SP_OK.TXT'} default {$null} }
    $failureName = switch ($Target) { 'sound-clean' {'SPFAIL.TXT'} 'clean' {'PFAIL.TXT'} 'game' {'PFAIL.TXT'} 'finish' {'FFAIL.TXT'} 'sound' {'SPFAIL.TXT'} default {$null} }
    if ($failureName -and (Test-Path -LiteralPath (Join-Path $basePath $failureName))) {
        throw ('Native build reported failure; inspect ' + $failureName + ' and the assembler logs.')
    }
    if ($successName) {
        $receipt = Get-Item -LiteralPath (Join-Path $basePath $successName)
        if ($receipt.LastWriteTime -lt $started.AddSeconds(-2)) {
            throw 'The build success marker is stale.'
        }
    }
    [pscustomobject]@{
        Target = $Target
        ProcessId = $buildProcess.Id
        VideoDriver = 'dummy'
        CreatedWindow = $false
        WindowChecks = $windowChecks
        ExitCode = $buildProcess.ExitCode
        Seconds = [math]::Round(((Get-Date) - $started).TotalSeconds, 2)
    } | ConvertTo-Json
} finally {
    if (!$buildProcess.HasExited) { $buildProcess.Kill(); $buildProcess.WaitForExit() }
    $buildProcess.Dispose()
}
