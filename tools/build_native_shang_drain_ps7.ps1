param([switch]$ValidateOnly)
$ErrorActionPreference='Stop'
$drainRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$drainBuildPath=$PSCommandPath
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-DrainBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "Exact original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-DrainBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_shang_owned_drain'"
Replace-DrainBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_paired_stumble_table_ps7'"
Replace-DrainBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_shang_drain_build_source/report.json'"
Replace-DrainBuildBoundary "'source_native_ai_response'" "'source_native_shang_owned_drain'"
Replace-DrainBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRepairAccepted -or $guard.nativeRuntimeAccepted -or -not $guard.bothQualifiedFragmentsApplied -or $guard.actualCppFaultsRejected.Count -ne 50 -or $guard.helperInstructionModelCases -ne 2052 -or -not $guard.exactFourNativeCMPIInstructionsAccepted -or -not $guard.actualPredecessorANDIOpcodeRejected -or $guard.initializedGuestByteDelta -ne 1008 -or $guard.initializedOwnedByteDelta -ne 24 -or $guard.proposedGuestSHA256 -ne ''6E8B1150216909FDF8144E7CF9F6D3F9FE654C9C99264CBAA29B6D9E7DF4BDD1'' -or $guard.expectedOwnedWindowSHA256 -ne ''8168174141F3772576C8D928B388D36115E8E7451DC117F573EAE44E3A868525'' -or $guard.expectedGraphicsReservationSHA256 -ne ''11680901F6BB2C03EF14676EF8C6BAB8D45B93520AC8FEDDD4606023A1498153'''
Replace-DrainBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta;initialized_owned_byte_delta=$guard.initializedOwnedByteDelta;expected_owned_sha256=$guard.expectedOwnedWindowSHA256;expected_shang_graphics_sha256=$guard.expectedGraphicsReservationSHA256;expected_shang_graphics_start=0x1fb0000;expected_shang_graphics_bytes=65536'
Replace-DrainBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$drainRoot'
Replace-DrainBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one complete private owned Shang-victim repair for Kano17/Sonya18. Both initialized ROM windows and new GFX require native verification. Public CMD unchanged; temporary compiler cache retired after terminal.'
Replace-DrainBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Source-qualified owned Shang victim lead-in, three-phase shrinking streams and real-victim costume palette routing. All original effective table words/native timing/skeleton/cache/finish handoff conserved. No ID aliases or gameplay assistance. Both initialized ROM windows and native GFX, then original physical campaign/art/audio replay still required.'
$audioLinks=@'
  if($old.laser_audio_assets.Count -ne 6 -or $old.total_sample_channels -ne 19){throw 'Whole prior native laser audio metadata required'}
  foreach($record in $old.laser_audio_assets){
   $priorAudio=Join-Path "$prior/samples/mk2ks" ($record.name+'.wav')
   $assetPin=$old.input_hashes.PSObject.Properties | Where-Object { [IO.Path]::GetFileName($_.Name) -ceq ($record.name+'.wav') }
   if(@($assetPin).Count -ne 1 -or (Get-FileHash -LiteralPath $priorAudio).Hash -ne $assetPin.Value){throw 'Exact unchanged prior waveform required'}
   New-Item -ItemType HardLink -Path (Join-Path "$out/samples/mk2ks" ($record.name+'.wav')) -Target $priorAudio | Out-Null
  }
'@
Replace-DrainBuildBoundary '  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null' ($audioLinks+"`n"+'  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null')
Replace-DrainBuildBoundary '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;' '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;laser_audio_assets=$old.laser_audio_assets;total_sample_channels=19;both_rom_windows_need_native_verification=$true;'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile-provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$drainBuildPath')
if($ValidateOnly){
 $drainTokens=$null;$drainErrors=$null
 [System.Management.Automation.Language.Parser]::ParseInput($buildSource,[ref]$drainTokens,[ref]$drainErrors) | Out-Null
 if($drainErrors.Count){throw ($drainErrors | Out-String)}
 [ordered]@{passed=$true;validationOnly=$true;powershellVersion=$PSVersionTable.PSVersion.ToString();allExactBuildBoundariesMatched=$true;buildExecuted=$false;root=$drainRoot} | ConvertTo-Json -Compress
 exit 0
}
& ([scriptblock]::Create($buildSource))
