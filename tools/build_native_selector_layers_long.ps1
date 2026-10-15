param([switch]$ValidateOnly)
$ErrorActionPreference='Stop'
$layerRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$layerBuildScriptPath=$PSCommandPath
$baseBuildPath=Join-Path $PSScriptRoot 'build_native_ai_response.ps1'
$source=Get-Content -LiteralPath $baseBuildPath -Raw
function Replace-LayerBoundary([string]$before,[string]$after){
 if(([regex]::Matches($script:source,[regex]::Escape($before))).Count -ne 1){throw "Exact original build boundary required: $before"}
 $script:source=$script:source.Replace($before,$after)
}
Replace-LayerBoundary '$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path' '$portRoot=$layerRoot'
Replace-LayerBoundary "`$name='diagnostic_native_ai_response'" "`$name='diagnostic_native_selector_layers_long'"
Replace-LayerBoundary "'diagnostic_native_attract_bios'" "'diagnostic_native_shang_drain_anchors'"
Replace-LayerBoundary "'audit_native_ai_response_source/report.json'" "'audit_native_selector_layers_long_source/report.json'"
Replace-LayerBoundary "'source_native_ai_response'" "'source_native_selector_layers_long'"
Replace-LayerBoundary '$guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8' '$guard.nativeRuntimeAccepted -or $guard.fullPortAcceptance -or -not $guard.actualCppFullHighConservationAccepted -or -not $guard.earlierActualA8PointerDepthOpcodeRejected -or $guard.actualCppFaultsRejected.Count -ne 106 -or $guard.onlyCSSCreationCallsChanged.Count -ne 2 -or $guard.ownPhotoDepth -ne 81 -or $guard.nativeNumberDepth -ne 82 -or -not $guard.gameplayAnimationGeometryAudioTeardownUnchanged'
Replace-LayerBoundary 'initialized_guest_byte_delta=$guard.expectedGuestChangedBytes' 'initialized_guest_byte_delta=$guard.changedHighBytes;expected_owned_sha256=$guard.proposedOwnedSHA256;expected_shang_graphics_sha256=$guard.proposedNewGraphicsSHA256;expected_shang_graphics_start=0x1fb0000;expected_shang_graphics_bytes=65536'
Replace-LayerBoundary 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.' 'Compiling one native CSS photo/number layering successor. Fighter pose geometry, combat and native teardown conserved; public CMD/ZIP unchanged. Temporary cache retires after actual compiler terminal.'
Replace-LayerBoundary 'Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.' 'Two CSS-only sorted sprite-registration hooks: own top-row photos depth51h and native player numbers52h. All stock photo/body depths, fighter animations, geometry, combat, owned shrinking, audio and original teardown conserved. Actual initialized windows and complete UI transitions still require native verification.'
$audioLinks=@'
  if($old.laser_audio_assets.Count -ne 6 -or $old.total_sample_channels -ne 19){throw 'Whole prior native laser audio metadata required'}
  foreach($record in $old.laser_audio_assets){
   $priorAudio=Join-Path "$prior/samples/mk2ks" ($record.name+'.wav')
   $assetPin=$old.input_hashes.PSObject.Properties | Where-Object { [IO.Path]::GetFileName($_.Name) -ceq ($record.name+'.wav') }
   if(@($assetPin).Count -ne 1 -or (Get-FileHash -LiteralPath $priorAudio).Hash -ne $assetPin.Value){throw 'Exact unchanged prior waveform required'}
   New-Item -ItemType HardLink -Path (Join-Path "$out/samples/mk2ks" ($record.name+'.wav')) -Target $priorAudio | Out-Null
  }
'@
Replace-LayerBoundary '  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null' ($audioLinks+"`n"+'  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null')
Replace-LayerBoundary '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;' '   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;laser_audio_assets=$old.laser_audio_assets;total_sample_channels=19;both_rom_windows_need_native_verification=$true;'
if(([regex]::Matches($source,[regex]::Escape('$PSCommandPath'))).Count -ne 2){throw 'Both original compile-provenance boundaries required'}
$source=$source.Replace('$PSCommandPath','$layerBuildScriptPath')
$tokens=$null;$errors=$null
[System.Management.Automation.Language.Parser]::ParseInput($source,[ref]$tokens,[ref]$errors) | Out-Null
if($errors.Count){throw ($errors | Out-String)}
$proof=Get-Content -LiteralPath (Join-Path $layerRoot 'audit_native_selector_layers_long_source/report.json') -Raw | ConvertFrom-Json
if(-not $proof.passed -or $proof.actualCppFaultsRejected.Count -ne 106 -or $proof.nativeRuntimeAccepted -or $proof.fullPortAcceptance){throw 'Exact guarded native-source proof required'}
foreach($entry in $proof.inputHashes.PSObject.Properties){if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Frozen input changed: $($entry.Name)"}}
foreach($entry in $proof.stagedSourceHashes.PSObject.Properties){if((Get-FileHash -LiteralPath (Join-Path "$layerRoot/source_native_selector_layers_long" $entry.Name)).Hash -ne $entry.Value){throw 'Exact qualified staged driver required'}}
if($ValidateOnly){[ordered]@{passed=$true;validationOnly=$true;faultsRejected=106;allOriginalBuildBoundariesMatched=$true;buildExecuted=$false}|ConvertTo-Json -Compress;exit 0}
Invoke-Expression $source
