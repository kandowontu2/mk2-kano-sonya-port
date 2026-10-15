param([ValidateSet('604','608')][string]$BootFrame='608')
$ErrorActionPreference='Stop'
$taskSource=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'run_bounded_native_sole_fifo_probe.ps1') -Raw
$taskSource=$taskSource.Replace('Join-Path $PSScriptRoot',"Join-Path 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools'")
$taskSource=$taskSource.Replace('audit_bounded_native_sole_fifo_runtime',"audit_bounded_native_owned_opaque_boot${BootFrame}_runtime")
$taskSource=$taskSource.Replace('audit_bounded_native_sole_fifo_preparation','audit_bounded_native_owned_opaque_preparation')
$taskSource=$taskSource.Replace('0D266B92E364DAF5BBFC6E9F4771FC2801E01DA818D1BDB497694FA9F672CCD3','FAD101AA600B7CB05590F6AFCDCD56B2E105419471B3238F0559DDAD27D66E10F7')
# Correct exact prepared observer hash (never infer identity from a filename).
$taskSource=$taskSource.Replace('FAD101AA600B7CB05590F6AFCDCD56B2E105419471B3238F0559DDAD27D66E10F7','FAD101AA600B7CB05590F6AFCD56B2E105419471B3238F0559DDAD27D66E10F7')
$taskSource=$taskSource.Replace("MK2KS_TEST_BOOT_FRAME='608'","MK2KS_TEST_BOOT_FRAME='$BootFrame'")
& ([ScriptBlock]::Create($taskSource))
