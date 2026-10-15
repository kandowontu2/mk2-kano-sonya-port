$ErrorActionPreference='Stop'
$taskSource=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'run_bounded_native_uppercut_probe.ps1') -Raw
foreach($taskPair in @(
 @('audit_bounded_native_uppercut_runtime','audit_bounded_native_recovery_counterkick_runtime'),
 @('audit_bounded_native_uppercut_owners_bound_preparation','audit_bounded_native_recovery_counterkick_preparation'),
 @('92F2EBD73A57733ED7638FE90D78F57B10CD238742BB6F02C49BE0123323DE94','A354E43CBC1875176B3E8BF3887A84646CC4F9BF627553A997997D4D893B9B1F'))){
 if(($taskSource.Split($taskPair[0]).Count-1) -ne 1){throw 'Unique runner boundary'}
 $taskSource=$taskSource.Replace($taskPair[0],$taskPair[1])
}
$env:MK2KS_TEST_BOOT_FRAME='608'
$env:MK2KS_CPU_PAIR_CONFIRM_AGE='264'
$taskSource=$taskSource.Replace('$taskRoot=Split-Path $PSScriptRoot -Parent',
 '$taskRoot="C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port"')
& ([ScriptBlock]::Create($taskSource))
