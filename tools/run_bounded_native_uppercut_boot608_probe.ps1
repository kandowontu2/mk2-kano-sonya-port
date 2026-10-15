# Distinct ordinary coin/start timing; no prescribed CPU or guest-state writes.
$ErrorActionPreference='Stop'
$taskRunnerSource=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'run_bounded_native_uppercut_probe.ps1') -Raw
$taskOld="'audit_bounded_native_uppercut_runtime'"
if(($taskRunnerSource.Split($taskOld).Count-1) -ne 1){throw 'Unique fresh case boundary'}
$taskRunnerSource=$taskRunnerSource.Replace($taskOld,"'audit_bounded_native_uppercut_boot608_runtime'")
$env:MK2KS_TEST_BOOT_FRAME='608'
$env:MK2KS_CPU_PAIR_CONFIRM_AGE='264'
# Scriptblock has no script-root binding: resolve the same explicit task root.
$taskRunnerSource=$taskRunnerSource.Replace('$taskRoot=Split-Path $PSScriptRoot -Parent',
 '$taskRoot="C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port"')
& ([ScriptBlock]::Create($taskRunnerSource))
