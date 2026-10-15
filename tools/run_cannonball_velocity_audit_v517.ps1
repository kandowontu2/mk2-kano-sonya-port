param([string]$CaseName='audit_v519_cannonball_velocity_checked_inputs')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName;if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
$runnerHash=(Get-FileHash -LiteralPath $PSCommandPath).Hash
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try{
 & $python tools/test_cannonball_velocity_v517.py 2>&1 | Out-File "$out/counterexamples.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Reference/corruption tests failed'}
 & $python tools/verify_cannonball_velocity_v517.py | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Independent verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 if(-not $proof.targetedCasesPassed -or $proof.passed -or $proof.fullPortAcceptance){throw 'Scope invariant changed'}
 $proof.inputHashes | Add-Member -NotePropertyName $PSCommandPath -NotePropertyValue $runnerHash
 $proof.inputHashes | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($entry in $proof.inputHashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Verified input changed: $($entry.Name)"}
  if([IO.Path]::GetExtension($entry.Name) -in '.py','.lua','.ps1'){Copy-Item -LiteralPath $entry.Name -Destination "$out/input_sources"}
 }
 Copy-Item -LiteralPath 'diagnostic_v500_native_cannonball_plane/input_sources/midtunit_m.cpp' -Destination "$out/input_sources/midtunit_m_v500.cpp"
 Copy-Item -LiteralPath 'mame-mkp/src/mame/midway/midtunit_m.cpp' -Destination "$out/input_sources/midtunit_m_v517.cpp"
 [ordered]@{passed=$false;targetedCasesPassed=$true;fullPortAcceptance=$false;candidate=$proof.candidate;
  cases=$proof.cases.Count;pairedFields=$proof.pairedFields;tests=8;checkedInputs=@($proof.inputHashes.PSObject.Properties).Count;
  knownCounterexample=$proof.knownCounterexample;scope=$proof.scope;
  verificationSHA256=(Get-FileHash -LiteralPath "$out/verification.json").Hash;
  counterexampleTestSHA256=(Get-FileHash -LiteralPath "$out/counterexamples.log").Hash;inputHashes=$proof.inputHashes} |
  ConvertTo-Json -Depth 5 | Out-File "$out/result.json" -Encoding utf8
 'Nine targeted cases verified; crouch counterexample and full acceptance remain open.'
}finally{Pop-Location}
