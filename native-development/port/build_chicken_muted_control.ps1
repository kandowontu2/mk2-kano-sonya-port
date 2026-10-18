param([ValidateRange(0,3)][int]$KeepTrack = 0)
$ErrorActionPreference = 'Stop'
$controlName = if ($KeepTrack -eq 0) { 'chicken_muted_control' } else { ('chicken_track{0}_control' -f $KeepTrack) }
$targetPath = Join-Path (Split-Path -Parent $PSScriptRoot) "baseline/$controlName"
if (Test-Path -LiteralPath (Join-Path $targetPath 'OK.TXT')) { throw 'Refusing to overwrite a completed diagnostic build.' }
$failurePath = Join-Path $targetPath 'FAIL.TXT'
if (Test-Path -LiteralPath $failurePath) {
    if ((Get-Content -Raw -LiteralPath $failurePath).Trim() -ne 'FAILED') { throw 'Unexpected failure marker contents.' }
    Remove-Item -LiteralPath $failurePath
}
$startInfo = [Diagnostics.ProcessStartInfo]::new()
$startInfo.FileName = Join-Path (Split-Path -Parent $PSScriptRoot) 'toolchain/dosbox-x/mingw-build/mingw/dosbox-x.exe'
$startInfo.WorkingDirectory = $targetPath
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.WindowStyle = [Diagnostics.ProcessWindowStyle]::Hidden
$startInfo.Environment['SDL_VIDEODRIVER'] = 'dummy'
$startInfo.Environment['SDL_AUDIODRIVER'] = 'dummy'
foreach ($argument in @('-conf',(Join-Path $targetPath 'dosbox.conf'),'-fastlaunch','-exit')) { $startInfo.ArgumentList.Add($argument) }
$buildProcess = [Diagnostics.Process]::Start($startInfo)
$started = Get-Date
try {
    $buildProcess.PriorityClass = [Diagnostics.ProcessPriorityClass]::BelowNormal
    while (!$buildProcess.WaitForExit(100)) {
        $buildProcess.Refresh()
        if ($buildProcess.HasExited) { break }
        if ($buildProcess.MainWindowHandle -ne [IntPtr]::Zero) { throw 'Diagnostic compiler created a window.' }
        if (((Get-Date)-$started).TotalSeconds -gt 180) { throw 'Diagnostic sound build timed out.' }
    }
    if ($buildProcess.ExitCode -ne 0) { throw 'Diagnostic compiler failed.' }
    if (Test-Path -LiteralPath (Join-Path $targetPath 'FAIL.TXT')) { throw 'PLBUILD failed; inspect diagnostic logs.' }
    if ((Get-Content -Raw -LiteralPath (Join-Path $targetPath 'OK.TXT')).Trim() -ne 'DONE') { throw 'Missing completion marker.' }
    foreach ($chip in 2..5) {
        if ((Get-Item -LiteralPath (Join-Path $targetPath "U$chip.ROM")).Length -ne 1048576) { throw 'Wrong control ROM size.' }
    }
    [pscustomobject]@{ExitCode=$buildProcess.ExitCode;CreatedWindow=$false;Seconds=((Get-Date)-$started).TotalSeconds} | ConvertTo-Json
} finally {
    if (!$buildProcess.HasExited) { $buildProcess.Kill(); $buildProcess.WaitForExit() }
    $buildProcess.Dispose()
}
