$ErrorActionPreference='Stop'
# Reuse the actual compile/restore/hardlink/compress/cache-retirement workflow.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeSpacingBuildRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeSpacingBuildPath=$PSCommandPath
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactSpacingBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "One original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactSpacingBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_cpu_finisher_spacing'"
Replace-ExactSpacingBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_cpu_finisher_dispatch'"
Replace-ExactSpacingBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_cpu_finisher_spacing_source/report.json'"
Replace-ExactSpacingBuildBoundary "'source_native_ai_response'" "'source_native_cpu_finisher_spacing'"
Replace-ExactSpacingBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRepairAccepted -or $guard.initializedGuestByteDelta -ne 6 -or $guard.actualFaultsRejected.Count -ne 12 -or $guard.ownDistanceProfiles.Count -ne 2'
Replace-ExactSpacingBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactSpacingBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling dedicated true-ID CPU finisher distance profiles: Kano80 and Sonya128, both variants. Native approach/action code unchanged; public CMD unchanged; temporary compiler cache will be retired.'
Replace-ExactSpacingBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Only6 initialized distance-row bytes changed: true Kano17 and Sonya18 CPU first/second finisher approach targets match own human command range. Existing effective rows, approach/actions, identities, cache, audio, images and RNG unchanged. Runtime positioning/art required; no new second-finisher choreography claim.'
Replace-ExactSpacingBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeSpacingBuildRoot'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeSpacingBuildPath')
& ([scriptblock]::Create($buildSource))
