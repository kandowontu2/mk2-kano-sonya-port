param([switch]$ValidateOnly)
$ErrorActionPreference='Stop'
$anchorRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$anchorReportPath=Join-Path $anchorRoot 'audit_native_shang_drain_anchors_source/report.json'
$anchorReport=Get-Content -Raw -LiteralPath $anchorReportPath | ConvertFrom-Json
$priorGuardPath=Join-Path $anchorRoot 'audit_native_shang_drain_build_source/report.json'
$priorGuard=Get-Content -Raw -LiteralPath $priorGuardPath | ConvertFrom-Json
$terminalPath=Join-Path $anchorRoot 'audit_native_shang_repair_terminal_sampled_checked/report.json'
$terminal=Get-Content -Raw -LiteralPath $terminalPath | ConvertFrom-Json
if(-not $anchorReport.passed -or -not $anchorReport.coordinateOnlyRepair -or -not $anchorReport.ownPixelsPalettesTimingSkeletonUnchanged -or $anchorReport.changedHighBytes -ne 18 -or $anchorReport.actualCppFaultsRejected.Count -ne 36 -or -not $terminal.finiteSonyaNormalShrinkingCrashAndOrdinaryRecoveryAccepted -or $terminal.fullPortAcceptance){throw 'Actual repaired fatality recovery and exact coordinate-only source proof required'}
if(-not $priorGuard.passed -or $priorGuard.actualCppFaultsRejected.Count -ne 50 -or $priorGuard.helperInstructionModelCases -ne 2052){throw 'Inherited whole helper/native opcode source qualification required'}
$pins=@{}
foreach($proof in @($anchorReport,$priorGuard,$terminal)){
 foreach($entry in $proof.inputHashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value -or ($pins.ContainsKey($entry.Name) -and $pins[$entry.Name] -ne $entry.Value)){throw "Frozen reviewed input changed: $($entry.Name)"}
  $pins[$entry.Name]=$entry.Value
 }
}
$stage=Join-Path $anchorRoot 'source_native_shang_drain_anchors'
$staged=@{}
foreach($entry in $anchorReport.stagedSourceHashes.PSObject.Properties){
 $path=Join-Path $stage $entry.Name
 if((Get-FileHash -LiteralPath $path).Hash -ne $entry.Value){throw 'Exact qualified staged coordinate driver required'}
 $pins[$path]=$entry.Value
 if($entry.Name -in @('midtunit.cpp','midtunit.h','midtunit_m.cpp')){$staged[$entry.Name]=$entry.Value}
}
foreach($path in @($anchorReportPath,$priorGuardPath,$terminalPath,$PSCommandPath,(Join-Path $PSScriptRoot 'build_native_shang_drain_ps7.ps1'),(Join-Path $PSScriptRoot 'build_native_ai_response.ps1'))){$pins[$path]=(Get-FileHash -LiteralPath $path).Hash}
$guardFolder=Join-Path $anchorRoot 'audit_native_shang_drain_anchors_build_source'
$guard=[ordered]@{passed=$true;sourceOnlyAccepted=$true;nativeRepairAccepted=$false;nativeRuntimeAccepted=$false;
 bothQualifiedFragmentsApplied=$true;actualCppFaultsRejected=$priorGuard.actualCppFaultsRejected;anchorCppFaultsRejected=$anchorReport.actualCppFaultsRejected;
 helperInstructionModelCases=2052;exactFourNativeCMPIInstructionsAccepted=$true;actualPredecessorANDIOpcodeRejected=$true;
 initializedGuestByteDelta=18;guestDeltaScope='Coordinate bytes relative to actual compiled v1, not total initialization';initializedOwnedByteDelta=67;
 proposedGuestSHA256=$anchorReport.proposedGuestSHA256;expectedOwnedWindowSHA256=$anchorReport.proposedOwnedSHA256;expectedGraphicsReservationSHA256=$anchorReport.proposedNewGraphicsSHA256;
 stagedSourceHashes=$staged;inputHashes=$pins;fullPortAcceptance=$false;
 originalNaturalIntegrationRequirements=$anchorReport.originalNaturalIntegrationRequirements;originalRemainingWorkGroups=$anchorReport.originalRemainingWorkGroups}
$drainWrapper=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'build_native_shang_drain_ps7.ps1') -Raw
function Replace-AnchorBoundary([string]$before,[string]$after){
 if(([regex]::Matches($script:drainWrapper,[regex]::Escape($before))).Count -ne 1){throw "Unique original wrapper boundary required: $before"}
 $script:drainWrapper=$script:drainWrapper.Replace($before,$after)
}
Replace-AnchorBoundary "diagnostic_native_shang_owned_drain'" "diagnostic_native_shang_drain_anchors'"
Replace-AnchorBoundary "diagnostic_native_paired_stumble_table_ps7'" "diagnostic_native_shang_owned_drain'"
Replace-AnchorBoundary "audit_native_shang_drain_build_source/report.json'" "audit_native_shang_drain_anchors_build_source/report.json'"
Replace-AnchorBoundary "source_native_shang_owned_drain'" "source_native_shang_drain_anchors'"
Replace-AnchorBoundary '$guard.initializedGuestByteDelta -ne 1008' '$guard.initializedGuestByteDelta -ne 18 -or $guard.anchorCppFaultsRejected.Count -ne 36'
Replace-AnchorBoundary '$guard.initializedOwnedByteDelta -ne 24' '$guard.initializedOwnedByteDelta -ne 67'
Replace-AnchorBoundary '6E8B1150216909FDF8144E7CF9F6D3F9FE654C9C99264CBAA29B6D9E7DF4BDD1' '0A9F9DED78F7724B62C4394AF902F76D67C490427E4D804A45E1F28C26EC6FC1'
Replace-AnchorBoundary '8168174141F3772576C8D928B388D36115E8E7451DC117F573EAE44E3A868525' 'A720502ACD03162A0A4ABCAC2266950E343FFD6ADF80C22E0675D1CD31DDBCDC6'
Replace-AnchorBoundary 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta' 'guest_coordinate_byte_delta_relative_prior=$guard.initializedGuestByteDelta'
Replace-AnchorBoundary 'Compiling one complete private owned Shang-victim repair for Kano17/Sonya18.' 'Compiling the coordinate-only Shang shrinking alignment successor for true Kano17/Sonya18.'
$anchorTokens=$null;$anchorErrors=$null
[System.Management.Automation.Language.Parser]::ParseInput($drainWrapper,[ref]$anchorTokens,[ref]$anchorErrors) | Out-Null
if($anchorErrors.Count){throw ($anchorErrors | Out-String)}
if($ValidateOnly){[ordered]@{passed=$true;validationOnly=$true;allImmutableInputsChecked=$true;coordinateBytes=18;anchorFaultsRejected=36;buildExecuted=$false}|ConvertTo-Json -Compress;exit 0}
if(Test-Path -LiteralPath $guardFolder){throw 'Fresh build guard required'}
New-Item -ItemType Directory -Path $guardFolder | Out-Null
$guard | ConvertTo-Json -Depth 12 | Out-File -LiteralPath (Join-Path $guardFolder 'report.json') -Encoding utf8
& ([scriptblock]::Create($drainWrapper))
