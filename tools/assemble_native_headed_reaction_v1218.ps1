param()
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$source=Join-Path $root 'diagnostic_v1130_owned_split_invariant_blood'
$out=Join-Path $root 'diagnostic_v1219_owned_native_headed_reaction'
$payload=Join-Path $root 'audit_v1217_native_headed_reaction_encoding\roms\mk2ks\mk2ks.mdata'
if(Test-Path -LiteralPath $out){throw 'Never overwrite candidate/evidence'}
$info=Get-Content -LiteralPath "$source\build-info.json" -Raw | ConvertFrom-Json
foreach($item in $info.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Source input changed: $($item.Name)"}}
if((Get-FileHash -LiteralPath "$source\mkport_candidate.exe").Hash -ne $info.executable_sha256){throw 'Exact compiled executable required'}
$encoding=Get-Content -LiteralPath "$root\audit_v1217_native_headed_reaction_encoding\report.json" -Raw | ConvertFrom-Json
if(!( $encoding.passed -and $encoding.allOtherPayloadBytesUnchanged -and $encoding.allGraphicsAndPalettesUnchanged -and $encoding.originalFivePoseAndLoopGrammarUnchanged) -or $encoding.guestCodeChanged -or (Get-FileHash -LiteralPath $payload).Hash -ne $encoding.payloadSHA256){throw 'Exact body-reference-only conversion required'}
$inputs=@{}
foreach($item in $info.input_hashes.PSObject.Properties){if([IO.Path]::GetExtension($item.Name) -ne '.mdata'){$inputs[$item.Name]=$item.Value}}
$inputs[$payload]=$encoding.payloadSHA256
foreach($file in @($PSCommandPath,"$root\tools\encode_native_headed_reaction_v1217.py","$root\audit_v1217_native_headed_reaction_encoding\report.json")){$inputs[$file]=(Get-FileHash -LiteralPath $file).Hash}
New-Item -ItemType Directory -Path "$out\roms\mk2ks" | Out-Null
Copy-Item -LiteralPath "$source\mkport_candidate.exe" -Destination "$out\mkport_candidate.exe"
Copy-Item -LiteralPath $payload -Destination "$out\roms\mk2ks\mk2ks.mdata"
Copy-Item -LiteralPath "$source\input_sources" -Destination "$out\input_sources" -Recurse
Copy-Item -LiteralPath $PSCommandPath -Destination "$out\input_sources"
[ordered]@{name='diagnostic_v1219_owned_native_headed_reaction';executable_sha256=$info.executable_sha256;payload_sha256=$encoding.payloadSHA256;input_hashes=$inputs;compiled_executable_source='diagnostic_v1110_owned_native_split';assembly='data-only primary55 body-reference correction in six owned blocks; exact compiled source/executable reused';no_recompile_claimed=$true;runtime_verification_pending=$true} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\build-info.json" -Encoding utf8
if((Get-FileHash -LiteralPath "$out\mkport_candidate.exe").Hash -ne $info.executable_sha256 -or (Get-FileHash -LiteralPath "$out\roms\mk2ks\mk2ks.mdata").Hash -ne $encoding.payloadSHA256){throw 'Candidate integrity failed'}
'Created diagnostic_v1219_owned_native_headed_reaction; runtime verification pending'
