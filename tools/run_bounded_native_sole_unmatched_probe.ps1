$ErrorActionPreference='Stop'
$taskSource=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'run_bounded_native_uppercut_probe.ps1') -Raw
foreach($taskPair in @(
 @('audit_bounded_native_uppercut_runtime','audit_bounded_native_sole_unmatched_runtime'),
 @('audit_bounded_native_uppercut_owners_bound_preparation','audit_bounded_native_sole_unmatched_preparation'),
 @('92F2EBD73A57733ED7638FE90D78F57B10CD238742BB6F02C49BE0123323DE94','B30365D976622189F36968E9E9117F385AA4F32A67AE2BAFA7FA7D63CC738057'))){
 if(($taskSource.Split($taskPair[0]).Count-1) -ne 1){throw 'Unique runner boundary'}
 $taskSource=$taskSource.Replace($taskPair[0],$taskPair[1])
}
$env:MK2KS_TEST_BOOT_FRAME='608'
$env:MK2KS_CPU_PAIR_CONFIRM_AGE='264'
$taskSource=$taskSource.Replace('$taskRoot=Split-Path $PSScriptRoot -Parent',
 '$taskRoot="C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port"')
& ([ScriptBlock]::Create($taskSource))
