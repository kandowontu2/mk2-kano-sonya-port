$ErrorActionPreference='Stop'
# Reuse the exact private compile/restore/compress/hardlink/cache-retirement
# workflow. Both fixes remain unaccepted in native gameplay until retested.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeOrbPaletteRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeOrbPaletteBuildPath=$PSCommandPath
$paletteGuard=Join-Path $nativeOrbPaletteRoot 'audit_native_sonya_orb_palette_source/report.json'
if((Get-FileHash -LiteralPath $paletteGuard).Hash -ne '784A5A6A8A0CB956917CF18CCE4DBC49C7C7FDBE8C7590B6C5917EF955E6C7D6'){throw 'Exact reviewed real-failure/cursor/palette successor proof required'}
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactOrbPaletteBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "Unique original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactOrbPaletteBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_sonya_orb_palette'"
Replace-ExactOrbPaletteBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_cpu_finisher_spacing'"
Replace-ExactOrbPaletteBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_sonya_orb_palette_source/report.json'"
Replace-ExactOrbPaletteBuildBoundary "'source_native_ai_response'" "'source_native_sonya_orb_palette'"
Replace-ExactOrbPaletteBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or $guard.motionUnitCases.Count -ne 10 -or $guard.parserUnitCases.Count -ne 72 -or $guard.actualTypedFaultsRejected.Count -ne 3 -or $guard.originalPaletteColors -ne 32 -or $guard.originalPaletteBytes -ne 66 -or $guard.proposedGuestSHA256 -ne ''1DD4B1AB4F5EC082F90409ECEBF0F02A55AC78EFF4C4B2759C47C2E2F51ABEB7'''
Replace-ExactOrbPaletteBuildBoundary 'foreach($entry in $guard.stagedSourceHashes.PSObject.Properties){$expected[(Join-Path $repo "src/mame/midway/$($entry.Name)")]=$entry.Value}' 'foreach($file in @(''midtunit.cpp'',''midtunit.h'',''midtunit_m.cpp'')){ $sourcePin=$guard.inputHashes.PSObject.Properties[(Join-Path $stage $file)]; if(-not $sourcePin){throw "Missing actual reviewed stage pin: $file"}; $expected[(Join-Path $repo "src/mame/midway/$file")]=$sourcePin.Value }'
Replace-ExactOrbPaletteBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactOrbPaletteBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one private orb cursor/palette repair: runtime-proven 32-bit animation bound and original magenta record through native typed allocation. Public CMD unchanged; temporary compiler cache will be retired.'
Replace-ExactOrbPaletteBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Private Sonya second finisher successor: full-width four-pose cursor bound and owned original32-color native palette with synchronous typed request. Source-only qualifications reject both prior defects. Earned native rendering/explosion/sound/cleanup and all final release gates remain required.'
Replace-ExactOrbPaletteBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeOrbPaletteRoot'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeOrbPaletteBuildPath')
& ([scriptblock]::Create($buildSource))
