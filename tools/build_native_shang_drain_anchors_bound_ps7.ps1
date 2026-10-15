param([switch]$ValidateOnly)
$ErrorActionPreference='Stop'
$taskScriptRoot=$PSScriptRoot
$taskScriptPath=$PSCommandPath
$preparationPath=Join-Path $taskScriptRoot 'build_native_shang_drain_anchors_ps7.ps1'
$preparation=Get-Content -LiteralPath $preparationPath -Raw
function Replace-BoundPreparation([string]$before,[string]$after){
 if(([regex]::Matches($script:preparation,[regex]::Escape($before))).Count -ne 1){throw "Exact bound preparation boundary required: $before"}
 $script:preparation=$script:preparation.Replace($before,$after)
}
Replace-BoundPreparation 'A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DDBCDC6' 'A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DBCDC6'
Replace-BoundPreparation "(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'))" "(Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'),`$preparationPath)"
$preparation=$preparation.Replace('$PSScriptRoot','$taskScriptRoot').Replace('$PSCommandPath','$taskScriptPath')
$boundWrapper=@'
$drainWrapper=$drainWrapper.Replace('$drainRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path','$drainRoot=$anchorRoot')
$drainWrapper=$drainWrapper.Replace('$drainBuildPath=$PSCommandPath','$drainBuildPath=$taskScriptPath')
$drainWrapper=$drainWrapper.Replace("Join-Path `$PSScriptRoot 'build_native_ai_response.ps1'","Join-Path `$taskScriptRoot 'build_native_ai_response.ps1'")
'@
Replace-BoundPreparation '$anchorTokens=$null;$anchorErrors=$null' ($boundWrapper+"`n"+'$anchorTokens=$null;$anchorErrors=$null')
Replace-BoundPreparation '& ([scriptblock]::Create($drainWrapper))' 'Invoke-Expression $drainWrapper'
Invoke-Expression $preparation
