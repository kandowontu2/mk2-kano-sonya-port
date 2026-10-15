$ErrorActionPreference='Stop'
# Reuse the exact private compile/restore/compress/hardlink/cache-retirement
# workflow. Native201 longer-distance orb worker lifetime remains source-only pending earned retests.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeOrbWorkerLifetimeRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeOrbWorkerLifetimeBuildPath=$PSCommandPath
$workerGuard=Join-Path $nativeOrbWorkerLifetimeRoot 'audit_native_sonya_orb_worker_lifetime_source/report.json'
if((Get-FileHash -LiteralPath $workerGuard).Hash -ne '45184F9EE617E5055FBD18266BBA78425B1BE4624629B7279F3E96D3DC41C349'){throw 'Exact reviewed real-failure/cursor/palette successor proof required'}
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactOrbWorkerLifetimeBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "Unique original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactOrbWorkerLifetimeBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_sonya_orb_worker_lifetime'"
Replace-ExactOrbWorkerLifetimeBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_cpu_finisher_spacing'"
Replace-ExactOrbWorkerLifetimeBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_sonya_orb_worker_lifetime_source/report.json'"
Replace-ExactOrbWorkerLifetimeBuildBoundary "'source_native_ai_response'" "'source_native_sonya_orb_worker_lifetime'"
Replace-ExactOrbWorkerLifetimeBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or $guard.motionUnitCases.Count -ne 10 -or $guard.parserUnitCases.Count -ne 72 -or $guard.actualTypedFaultsRejected.Count -ne 3 -or $guard.independentNativeWorkerCategory -ne ''0201'' -or $guard.winnerTimingChanged -or $guard.choreographyTruncated -or $guard.initializedByteDeltaFromCloudLifetime -ne 2 -or $guard.proposedGuestSHA256 -ne ''9A0778B63D591D0E53B1DD06FABC67DF8C0982D4209221439BDA094E6EABC706'''
Replace-ExactOrbWorkerLifetimeBuildBoundary 'foreach($entry in $guard.stagedSourceHashes.PSObject.Properties){$expected[(Join-Path $repo "src/mame/midway/$($entry.Name)")]=$entry.Value}' 'foreach($file in @(''midtunit.cpp'',''midtunit.h'',''midtunit_m.cpp'')){ $sourcePin=$guard.inputHashes.PSObject.Properties[(Join-Path $stage $file)]; if(-not $sourcePin){throw "Missing actual reviewed stage pin: $file"}; $expected[(Join-Path $repo "src/mame/midway/$file")]=$sourcePin.Value }'
Replace-ExactOrbWorkerLifetimeBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactOrbWorkerLifetimeBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one private native201 orb-worker lifetime repair: preserve all long-distance travel/wrap/retire and own cleanup without winner delay. Proven cloud repair retained. Public CMD unchanged; temporary compiler cache will be retired.'
Replace-ExactOrbWorkerLifetimeBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Private Sonya orb successor: only independent worker category immediate100 to native201 changes. All travel/wrap/retire,144field own winner timing and sole ownership conserved; actual P1/P2 cloud13x5 cleanup repair retained. Native both-slot wall-distance object/cache/palette teardown, full audio and final release gates remain required.'
Replace-ExactOrbWorkerLifetimeBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeOrbWorkerLifetimeRoot'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeOrbWorkerLifetimeBuildPath')
& ([scriptblock]::Create($buildSource))
