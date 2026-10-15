$ErrorActionPreference='Stop'
$pairedRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$pairedBuildPath=$PSCommandPath
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-PairedBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "Exact original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-PairedBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_paired_stumble_table_ps7'"
Replace-PairedBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_kano_laser_audio'"
Replace-PairedBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_paired_stumble_table_bounded_source/report.json'"
Replace-PairedBuildBoundary "'source_native_ai_response'" "'source_native_paired_stumble_table'"
Replace-PairedBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or -not $guard.actualRootCauseSourceMatched -or $guard.actualGlobalDecoderStores -ne 146 -or $guard.completeProvenanceRows -ne 1800 -or $guard.negativeFaultsRejected.Count -ne 29 -or $guard.initializedGuestByteDelta -ne 79 -or $guard.proposedGuestSHA256 -ne ''8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479'''
Replace-PairedBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-PairedBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$pairedRoot'
Replace-PairedBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one private packed-victim table repair for true Kano17/Sonya18. Original native choreography, all stock rows and audio conserved. Public CMD unchanged; temporary compiler cache retired after terminal.'
Replace-PairedBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Private source-qualified paired-stumble table repair. Both added IDs use owned main35 pose3 with native shared alignment. All17 stock rows and every other guest byte preserved. Native failing campaign and combined regression still required.'
$audioLinks=@'
  if($old.laser_audio_assets.Count -ne 6 -or $old.total_sample_channels -ne 19){throw 'Whole prior native laser audio metadata required'}
  foreach($record in $old.laser_audio_assets){
   $priorAudio=Join-Path "$prior/samples/mk2ks" ($record.name+'.wav')
   $assetPin=$old.input_hashes.PSObject.Properties | Where-Object { [IO.Path]::GetFileName($_.Name) -ceq ($record.name+'.wav') }
   if(@($assetPin).Count -ne 1 -or (Get-FileHash -LiteralPath $priorAudio).Hash -ne $assetPin.Value){throw 'Exact unchanged prior voice waveform required'}
   New-Item -ItemType HardLink -Path (Join-Path "$out/samples/mk2ks" ($record.name+'.wav')) -Target $priorAudio | Out-Null
  }
'@
Replace-PairedBuildBoundary '  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null' ($audioLinks+"`n"+'  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null')
Replace-PairedBuildBoundary '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;' '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;laser_audio_assets=$old.laser_audio_assets;total_sample_channels=19;'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile-provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$pairedBuildPath')
& ([scriptblock]::Create($buildSource))
