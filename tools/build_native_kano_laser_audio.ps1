$ErrorActionPreference='Stop'
# One private audio candidate, no public promotion or duplicate sample data.
$originalBuild=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$nativeLaserRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$nativeLaserBuildPath=$PSCommandPath
$laserGuard=Join-Path $nativeLaserRoot 'audit_native_kano_laser_audio_call_frame_source/report.json'
if((Get-FileHash -LiteralPath $laserGuard).Hash -ne '9CB742D893F28786EBD43577ABD5D12945462EA621CE710F91E7407C5B2B6C22'){throw 'Exact whole audio call-frame qualification required'}
$buildSource=Get-Content -LiteralPath $originalBuild -Raw
function Replace-ExactLaserBuildBoundary([string]$before,[string]$after) {
 if(([regex]::Matches($script:buildSource,[regex]::Escape($before))).Count -ne 1){throw "Unique original build boundary required: $before"}
 $script:buildSource=$script:buildSource.Replace($before,$after)
}
Replace-ExactLaserBuildBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_kano_laser_audio'"
Replace-ExactLaserBuildBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_kano_laser_burst'"
Replace-ExactLaserBuildBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_kano_laser_audio_call_frame_source/report.json'"
Replace-ExactLaserBuildBoundary "'source_native_ai_response'" "'source_native_kano_laser_audio'"
Replace-ExactLaserBuildBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or $guard.controlUnitCases.Count -ne 38 -or $guard.markerWordUnitCases.Count -ne 95 -or $guard.hostAudioUnitCases.totalOperations -ne 388 -or $guard.auxiliaryWordUnitCases.Count -ne 18 -or $guard.totalSampleChannels -ne 19 -or $guard.negativeFaultsRejected.Count -ne 8 -or $guard.proposedGuestSHA256 -ne ''AB1A0AEAE5BBE6457D591C8B9491E439E4DCA8F08A2E37A3710A3FA67769EF6E'''
Replace-ExactLaserBuildBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.initializedGuestByteDelta'
Replace-ExactLaserBuildBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one private Kano laser audio candidate: six complete original48k assets, true actor voice routing and dedicated five-slot lifetime pool. Public CMD unchanged; compiler cache retired after terminal.'
Replace-ExactLaserBuildBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Private laser audio candidate. Original charge/beam/Kano-Sonya victim screams/burst recordings; stock victims retain native MK2 dispatcher; original five-slot allocator in dedicated channels14..18. All prior gameplay conserved. Source-only acceptance, not native PCM or full port acceptance.'
Replace-ExactLaserBuildBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$nativeLaserRoot'
$assetPins=@'
 foreach($record in $guard.audioAssets){
  $audioPath=Join-Path $portRoot ('audit_native_kano_laser_original_samples/'+$record.name+'.wav')
  $audioPin=$guard.inputHashes.PSObject.Properties[(Join-Path $portRoot 'audit_native_kano_laser_original_samples/asset_report.json')]
  if(-not $audioPin){throw 'Original asset receipt pin missing'}
  $audioReceipt=Get-Content -LiteralPath $audioPin.Name -Raw | ConvertFrom-Json
  $wavePin=$audioReceipt.inputHashes.PSObject.Properties[$audioPath]
  if(-not $wavePin -or (Get-FileHash -LiteralPath $audioPath).Hash -ne $wavePin.Value){throw "Whole original audio asset changed: $audioPath"}
  $compiled[$audioPath]=$wavePin.Value
 }
'@
Replace-ExactLaserBuildBoundary ' Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"' ($assetPins+"`n"+' Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"')
$assetLinks=@'
  foreach($record in $guard.audioAssets){
   $audioPath=Join-Path $portRoot ('audit_native_kano_laser_original_samples/'+$record.name+'.wav')
   New-Item -ItemType HardLink -Path (Join-Path "$out/samples/mk2ks" ($record.name+'.wav')) -Target $audioPath | Out-Null
  }
'@
Replace-ExactLaserBuildBoundary '  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null' ($assetLinks+"`n"+'  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null')
Replace-ExactLaserBuildBoundary '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;' '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;laser_audio_assets=$guard.audioAssets;total_sample_channels=19;'
if(([regex]::Matches($buildSource,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile provenance boundaries required'}
$buildSource=$buildSource.Replace('$PSCommandPath','$nativeLaserBuildPath')
& ([scriptblock]::Create($buildSource))
