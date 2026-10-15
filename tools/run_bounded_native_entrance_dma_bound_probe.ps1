$ErrorActionPreference='Stop'
$taskWrapper=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'run_bounded_native_entrance_dma_probe.ps1') -Raw
$taskWrapper=$taskWrapper.Replace('Join-Path $PSScriptRoot',
 "Join-Path 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools'")
& ([ScriptBlock]::Create($taskWrapper))
