$ErrorActionPreference='Stop'
$pairedFinalTools=$PSScriptRoot
$pairedFinalRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$pairedFinalBuild=$PSCommandPath
$pairedPrevious=Join-Path $PSScriptRoot 'build_native_paired_stumble_table.ps1'
$pairedWrapper=Get-Content -LiteralPath $pairedPrevious -Raw
$changes=@(
 @('8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C2600884D43E6B6C479','8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479'),
 @('$pairedRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path','$pairedRoot=$pairedFinalRoot'),
 @('$pairedBuildPath=$PSCommandPath','$pairedBuildPath=$pairedFinalBuild'),
 @('$originalBuild=Join-Path $PSScriptRoot ''build_native_ai_response.ps1''','$originalBuild=Join-Path $pairedFinalTools ''build_native_ai_response.ps1''')
)
foreach($pair in $changes){
 if(([regex]::Matches($pairedWrapper,[regex]::Escape($pair[0]))).Count -ne 1){throw 'Unique precompile wrapper correction required'}
 $pairedWrapper=$pairedWrapper.Replace($pair[0],$pair[1])
}
$failureFolder=Join-Path $pairedFinalRoot 'audit_native_paired_stumble_precompile_path_failure'
if(Test-Path -LiteralPath $failureFolder){throw 'Preserve original path-wrapper failure'}
New-Item -ItemType Directory -Path $failureFolder | Out-Null
[ordered]@{passed=$false;phase='precompile_wrapper_path';nativeBuildStarted=$false;
 error='Dynamic ScriptBlock has an empty PSScriptRoot; original wrapper stopped before compiler/asset creation';
 priorWrapperSHA256=(Get-FileHash -LiteralPath (Join-Path $pairedFinalTools 'build_native_paired_stumble_table_bound.ps1')).Hash;
 fullPortAcceptance=$false;goalStatus='active'} | ConvertTo-Json |
 Out-File -LiteralPath (Join-Path $failureFolder 'failure.json') -Encoding utf8
& ([scriptblock]::Create($pairedWrapper))
