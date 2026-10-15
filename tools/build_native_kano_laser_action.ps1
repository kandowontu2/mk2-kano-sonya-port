$ErrorActionPreference='Stop'
# One private candidate, existing shared assets, source restoration and exact
# terminal compiler-cache retirement. No public CMD or release promotion.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeLaserRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeLaserBuildPath=$PSCommandPath
$laserGuard=Join-Path $nativeLaserRoot 'audit_native_kano_laser_action_routes_source/report.json'
if((Get-FileHash -LiteralPath $laserGuard).Hash -ne '2C1ACF18F7EDBEBD2839535B7B2242554CC779CE2A4954B858A886BA779A24B7'){throw 'Exact whole source/control/route conservation evidence required'}
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactLaserBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "Unique original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactLaserBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_kano_laser_action'"
Replace-ExactLaserBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_sonya_orb_worker_lifetime'"
Replace-ExactLaserBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_kano_laser_action_routes_source/report.json'"
Replace-ExactLaserBuildBoundary "'source_native_ai_response'" "'source_native_kano_laser_action_routes'"
Replace-ExactLaserBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or $guard.controlUnitCases.Count -ne 38 -or $guard.negativeFaultsRejected.Count -ne 12 -or -not $guard.actualFriendshipFirstFatalityHKChainConserved -or $guard.proposedGuestSHA256 -ne ''E6C2C3FB9D4053DA1CBDC9CFC61E752E9198DA65738A3931F7F169967F734F29'''
Replace-ExactLaserBuildBoundary 'foreach($entry in $guard.stagedSourceHashes.PSObject.Properties){$expected[(Join-Path $repo "src/mame/midway/$($entry.Name)")]=$entry.Value}' 'foreach($file in @(''midtunit.cpp'',''midtunit.h'',''midtunit_m.cpp'')){ $sourcePin=$guard.inputHashes.PSObject.Properties[(Join-Path $stage $file)]; if(-not $sourcePin){throw "Missing actual reviewed stage pin: $file"}; $expected[(Join-Path $repo "src/mame/midway/$file")]=$sourcePin.Value }'
Replace-ExactLaserBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactLaserBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one private native Kano laser action: own victim graphics, full beam phases, red ramp, grey smoke and bones. Public CMD unchanged; temporary compiler cache will be retired.'
Replace-ExactLaserBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Private full laser control candidate. True own victim graphics, contact68/burst164/cleanup196, native winner, human button history and distinct CPU second approach150. Existing Friendship/first fatality fallback preserved. Actual earned activation, roster alignment, effect scene cleanup, audio/flash and full scope remain unaccepted.'
Replace-ExactLaserBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeLaserRoot'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeLaserBuildPath')
& ([scriptblock]::Create($buildSource))
