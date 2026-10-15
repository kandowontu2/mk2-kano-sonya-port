$ErrorActionPreference='Stop'
# Reuse the complete existing compile/restore/compress/cache-retirement workflow.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeFinisherBuildRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeFinisherBuildPath=$PSCommandPath
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "One original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_cpu_finisher_dispatch'"
Replace-ExactBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_ai_response'"
Replace-ExactBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_cpu_finisher_dispatch_source/report.json'"
Replace-ExactBuildBoundary "'source_native_ai_response'" "'source_native_cpu_finisher_dispatch'"
Replace-ExactBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRepairAccepted -or $guard.initializedGuestByteDelta -ne 122 -or $guard.actualFaultsRejected.Count -ne 12 -or $guard.tables.Count -ne 2'
Replace-ExactBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one two-table true-ID finisher dispatch repair; original identities, cache loop, owned choreography, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.'
Replace-ExactBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Two native performer tables extended to real Kano17/Sonya18 existing owned finish actions. All existing effective rows, native cache/animation code, choreography, identities, biographies, audio, images and RNG conserved. CPU and ordinary runtime regression required.'
Replace-ExactBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeFinisherBuildRoot'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile script provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeFinisherBuildPath')
& ([scriptblock]::Create($buildSource))
