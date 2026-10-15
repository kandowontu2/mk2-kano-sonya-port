param([switch]$ValidateOnly)
$ErrorActionPreference='Stop'
$anchorScriptRoot=$PSScriptRoot
$anchorExecutionPath=$PSCommandPath
$preparationPath=Join-Path $anchorScriptRoot 'build_native_shang_drain_anchors_ps7.ps1'
$preparation=Get-Content -LiteralPath $preparationPath -Raw
function Replace-PreparationBoundary([string]$before,[string]$after){
 if(([regex]::Matches($script:preparation,[regex]::Escape($before))).Count -ne 1){throw "Unique preparation boundary required: $before"}
 $script:preparation=$script:preparation.Replace($before,$after)
}
Replace-PreparationBoundary 'A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DDBCDC6' 'A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DBCDC6'
Replace-PreparationBoundary "(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'))" "(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'),`$preparationPath)"
# Script blocks do not inherit the caller's automatic script-path variables.
# Bind preparation explicitly, and only change the three executable wrapper
# bindings; preserve its literal underlying compiler-provenance replacements.
$preparation=$preparation.Replace('$PSScriptRoot','$anchorScriptRoot').Replace('$PSCommandPath','$anchorExecutionPath')
$wrapperBindings=@'
$drainWrapper=$drainWrapper.Replace('$drainRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path','$drainRoot=$anchorRoot')
$drainWrapper=$drainWrapper.Replace('$drainBuildPath=$PSCommandPath','$drainBuildPath=$anchorExecutionPath')
$drainWrapper=$drainWrapper.Replace("Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'","Join-Path `$anchorScriptRoot 'build_native_ai_response.ps1'")
'@
Replace-PreparationBoundary '$anchorTokens=$null;$anchorErrors=$null' ($wrapperBindings+"`n"+'$anchorTokens=$null;$anchorErrors=$null')
& ([scriptblock]::Create($preparation))
