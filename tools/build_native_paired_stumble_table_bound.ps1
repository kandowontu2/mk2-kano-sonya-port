$ErrorActionPreference='Stop'
# The first wrapper stopped before compiling because its literal hash had
# one extra '8'. Preserve it; correct only that precompile comparison.
$pairedBoundRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$pairedPrevious=Join-Path $PSScriptRoot 'build_native_paired_stumble_table.ps1'
$pairedWrapper=Get-Content -LiteralPath $pairedPrevious -Raw
$incorrect='8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C2600884D43E6B6C479'
$correct='8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479'
if(([regex]::Matches($pairedWrapper,[regex]::Escape($incorrect))).Count -ne 1){throw 'Unique failed precompile literal required'}
$guard=Get-Content -LiteralPath (Join-Path $pairedBoundRoot 'audit_native_paired_stumble_table_bounded_source/report.json') -Raw | ConvertFrom-Json
if($guard.proposedGuestSHA256 -cne $correct){throw 'Actual independently qualified whole guest required'}
$failedFolder=Join-Path $pairedBoundRoot 'audit_native_paired_stumble_precompile_failure'
if(Test-Path -LiteralPath $failedFolder){throw 'Never overwrite precompile failure'}
New-Item -ItemType Directory -Path $failedFolder | Out-Null
[ordered]@{passed=$false;phase='precompile_guard';nativeBuildStarted=$false;newBuilds=0;
 originalWrapper=$pairedPrevious;originalWrapperSHA256=(Get-FileHash -LiteralPath $pairedPrevious).Hash;
 incorrectLiteral=$incorrect;actualQualifiedGuestSHA256=$correct;fullPortAcceptance=$false;goalStatus='active'} |
 ConvertTo-Json | Out-File -LiteralPath (Join-Path $failedFolder 'failure.json') -Encoding utf8
& ([scriptblock]::Create($pairedWrapper.Replace($incorrect,$correct)))
