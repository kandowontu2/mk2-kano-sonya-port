$ErrorActionPreference='Stop'
$taskSource=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'run_bounded_native_sole_fifo_probe.ps1') -Raw
$taskSource=$taskSource.Replace('Join-Path $PSScriptRoot',"Join-Path 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools'")
$taskSource=$taskSource.Replace('audit_bounded_native_sole_fifo_runtime','audit_bounded_native_entrance_dma_runtime')
$taskSource=$taskSource.Replace('audit_bounded_native_sole_fifo_preparation','audit_bounded_native_entrance_dma_preparation')
$taskSource=$taskSource.Replace('0D266B92E364DAF5BBFC6E9F4771FC2801E01DA818D1BDB497694FA9F672CCD3','7C17FBCE194B113BD59A50513242A27B1157A11C9F438EEEA760BEA389D74F9F')
& ([ScriptBlock]::Create($taskSource))
