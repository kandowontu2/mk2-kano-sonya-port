$ErrorActionPreference='Stop'
# One private candidate using the reviewed restore/hardlink/compress workflow.
# Source-only input checks are not rendering, cleanup, sound or release gates.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeOrbBuildRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeOrbBuildPath=$PSCommandPath
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactOrbBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "One original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactOrbBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_sonya_orb_dispatch'"
Replace-ExactOrbBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_cpu_finisher_spacing'"
Replace-ExactOrbBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_sonya_orb_dispatch_source/report.json'"
Replace-ExactOrbBuildBoundary "'source_native_ai_response'" "'source_native_sonya_orb_dispatch'"
Replace-ExactOrbBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or $guard.parserUnitCases.Count -ne 72 -or $guard.actualFaultsRejected.Count -ne 13 -or $guard.cpuSecondDistance -ne 256 -or $guard.cpuFirstDistance -ne 128 -or $guard.cpuSecondAction -ne ''FFD7B000'' -or $guard.proposedGuestSHA256 -ne ''02AF8317578D91ED66A8FA5DFE1568077D28F7ADA418E97180DCAA5F6E26144D'''
Replace-ExactOrbBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactOrbBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one private Sonya magenta-orb second-finisher candidate: native input, independent CPU approach, own effect/victim tasks. Public CMD unchanged; original new audio not yet imported. Temporary compiler cache will be retired.'
Replace-ExactOrbBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Private genuine Sonya second fatality with corrected native coordinate copies, independent orb/bone/smoke/victim ownership, adapted Block UUBD HK input and CPU second approach256. First kiss/128 approach and all other player/stock routes unchanged. New original sound assets and native render/physics/cleanup remain unaccepted; no release claim.'
Replace-ExactOrbBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeOrbBuildRoot'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeOrbBuildPath')
& ([scriptblock]::Create($buildSource))
