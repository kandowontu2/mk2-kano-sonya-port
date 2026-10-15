param([switch]$ValidateOnly)
$ErrorActionPreference='Stop'
$preparationPath=Join-Path $PSScriptRoot 'build_native_shang_drain_anchors_ps7.ps1'
$preparation=Get-Content -LiteralPath $preparationPath -Raw
function Replace-FinalPreparation([string]$before,[string]$after){
 if(([regex]::Matches($script:preparation,[regex]::Escape($before))).Count -ne 1){throw "Exact final preparation boundary required: $before"}
 $script:preparation=$script:preparation.Replace($before,$after)
}
Replace-FinalPreparation 'A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DDBCDC6' 'A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DBCDC6'
Replace-FinalPreparation "(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'))" "(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'),`$preparationPath)"
# Execute the reviewed wrapper in this actual script scope: its boundary
# helpers intentionally use script-scoped variables and native script paths.
Replace-FinalPreparation '& ([scriptblock]::Create($drainWrapper))' 'Invoke-Expression $drainWrapper'
Invoke-Expression $preparation
