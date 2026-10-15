param()
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$source=Join-Path $root 'diagnostic_v1110_owned_native_split'
$out=Join-Path $root 'diagnostic_v1130_owned_split_invariant_blood'
$payload=Join-Path $root 'audit_v1128_owned_split_blood_encoding\roms\mk2ks\mk2ks.mdata'
if(Test-Path -LiteralPath $out){throw 'Never overwrite candidate/evidence'}
$info=Get-Content -LiteralPath "$source\build-info.json" -Raw | ConvertFrom-Json
foreach($item in $info.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Source input changed: $($item.Name)"}}
if((Get-FileHash -LiteralPath "$source\mkport_candidate.exe").Hash -ne $info.executable_sha256){throw 'Exact compiled executable required'}
$encoding=Get-Content -LiteralPath "$root\audit_v1128_owned_split_blood_encoding\report.json" -Raw | ConvertFrom-Json
if((Get-FileHash -LiteralPath $payload).Hash -ne $encoding.payloadSHA256 -or $encoding.guestCodeChanged -or !$encoding.everyNonbloodIndexAndAlphaUnchanged){throw 'Blood-only encoded payload required'}
$inputs=@{}
foreach($item in $info.input_hashes.PSObject.Properties){if([IO.Path]::GetExtension($item.Name) -ne '.mdata'){$inputs[$item.Name]=$item.Value}}
$inputs[$payload]=$encoding.payloadSHA256
New-Item -ItemType Directory -Path "$out\roms\mk2ks" | Out-Null
Copy-Item -LiteralPath "$source\mkport_candidate.exe" -Destination "$out\mkport_candidate.exe"
Copy-Item -LiteralPath $payload -Destination "$out\roms\mk2ks\mk2ks.mdata"
Copy-Item -LiteralPath "$source\input_sources" -Destination "$out\input_sources" -Recurse
Copy-Item -LiteralPath $PSCommandPath -Destination "$out\input_sources"
[ordered]@{name='diagnostic_v1130_owned_split_invariant_blood';executable_sha256=$info.executable_sha256;payload_sha256=$encoding.payloadSHA256;input_hashes=$inputs;compiled_executable_source='diagnostic_v1110_owned_native_split';assembly='data-only payload change, exact existing compiled source/executable preserved';no_recompile_claimed=$true} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out\build-info.json" -Encoding utf8
if((Get-FileHash -LiteralPath "$out\mkport_candidate.exe").Hash -ne $info.executable_sha256 -or (Get-FileHash -LiteralPath "$out\roms\mk2ks\mk2ks.mdata").Hash -ne $encoding.payloadSHA256){throw 'Candidate integrity failed'}
Get-Content -LiteralPath "$out\build-info.json"
