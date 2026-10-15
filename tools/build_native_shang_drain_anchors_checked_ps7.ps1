param([switch]$ValidateOnly)
$ErrorActionPreference='Stop'
$preparationPath=Join-Path $PSScriptRoot 'build_native_shang_drain_anchors_ps7.ps1'
$preparation=Get-Content -LiteralPath $preparationPath -Raw
$mistyped='A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DDBCDC6'
$correct='A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DBCDC6'
if(([regex]::Matches($preparation,[regex]::Escape($mistyped))).Count -ne 1){throw 'Unique validation-only digest transcription boundary required'}
$preparation=$preparation.Replace($mistyped,$correct)
$pinBoundary="(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'))"
if(([regex]::Matches($preparation,[regex]::Escape($pinBoundary))).Count -ne 1){throw 'Unique preparation provenance boundary required'}
$preparation=$preparation.Replace($pinBoundary,"(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'),`$preparationPath)")
& ([scriptblock]::Create($preparation))
