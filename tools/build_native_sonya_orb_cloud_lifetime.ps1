$ErrorActionPreference='Stop'
# Reuse the exact private compile/restore/compress/hardlink/cache-retirement
# workflow. Native201 cloud lifetime remains source-only until earned gameplay retests.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeOrbCloudLifetimeRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeOrbCloudLifetimeBuildPath=$PSCommandPath
$cloudGuard=Join-Path $nativeOrbCloudLifetimeRoot 'audit_native_sonya_orb_cloud_lifetime_source/report.json'
if((Get-FileHash -LiteralPath $cloudGuard).Hash -ne 'FBDF70355F4D63DC5B951764D489E3E2DDF34E01F8451C55014239ED62EEA2A2'){throw 'Exact reviewed real-failure/cursor/palette successor proof required'}
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactOrbCloudLifetimeBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "Unique original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactOrbCloudLifetimeBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_sonya_orb_cloud_lifetime'"
Replace-ExactOrbCloudLifetimeBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_cpu_finisher_spacing'"
Replace-ExactOrbCloudLifetimeBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_sonya_orb_cloud_lifetime_source/report.json'"
Replace-ExactOrbCloudLifetimeBuildBoundary "'source_native_ai_response'" "'source_native_sonya_orb_cloud_lifetime'"
Replace-ExactOrbCloudLifetimeBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or $guard.motionUnitCases.Count -ne 10 -or $guard.parserUnitCases.Count -ne 72 -or $guard.actualTypedFaultsRejected.Count -ne 3 -or $guard.fullOriginalCloudGroups -ne 13 -or $guard.cloudFields -ne 65 -or $guard.initializedByteDeltaFromPalette -ne 2 -or $guard.proposedGuestSHA256 -ne ''00D1569853EF6EAE68D7919CE20992AD3DD102F67AC98A25F1F2DF858CF7E4E9'''
Replace-ExactOrbCloudLifetimeBuildBoundary 'foreach($entry in $guard.stagedSourceHashes.PSObject.Properties){$expected[(Join-Path $repo "src/mame/midway/$($entry.Name)")]=$entry.Value}' 'foreach($file in @(''midtunit.cpp'',''midtunit.h'',''midtunit_m.cpp'')){ $sourcePin=$guard.inputHashes.PSObject.Properties[(Join-Path $stage $file)]; if(-not $sourcePin){throw "Missing actual reviewed stage pin: $file"}; $expected[(Join-Path $repo "src/mame/midway/$file")]=$sourcePin.Value }'
Replace-ExactOrbCloudLifetimeBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactOrbCloudLifetimeBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one private native201 cloud-lifetime repair: preserve full13x5 animation and owned cleanup beyond exact100 winner deletion. Cursor/palette fixes conserved. Public CMD unchanged; temporary compiler cache will be retired.'
Replace-ExactOrbCloudLifetimeBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Private Sonya orb successor: only cloud task category immediate100 to native independent201 changes. All13x5 fields, geometry and owned cleanup conserved; earlier cursor/palette fixes retained. Earned gameplay/cloud/cache/palette cleanup, long-distance, sounds and full release gates remain required.'
Replace-ExactOrbCloudLifetimeBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeOrbCloudLifetimeRoot'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeOrbCloudLifetimeBuildPath')
& ([scriptblock]::Create($buildSource))
