param([string]$CaseName='audit_v508_current_special_matrix_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned case name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try{
 & $python tools/test_current_special_matrix_v500.py 2>&1 | Out-File "$out/counterexamples.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Contract/counterexample tests failed'}
 & $python tools/verify_current_special_matrix_v500.py | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Independent verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 if(-not $proof.boundedMatrixPassed -or $proof.passed -or $proof.fullPortAcceptance){throw 'Scope/report invariant changed'}
 $proof.inputHashes | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 foreach($entry in $proof.inputHashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Verified input changed: $($entry.Name)"}
  if([IO.Path]::GetExtension($entry.Name) -in '.py'){Copy-Item -LiteralPath $entry.Name -Destination "$out/input_sources"}
 }
 Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"
 [ordered]@{passed=$false;boundedMatrixPassed=$true;fullPortAcceptance=$false;candidate=$proof.candidate;
  positiveCases=$proof.positiveCases.Count;negativeCases=$proof.negativeCases.Count;
  originalCases=$proof.originalCases.Count;originalDuckPhaseCases=$proof.originalDuckPhaseCases.Count;
  widerDuckCases=$proof.widerDuckObservations.Count;
  widerDuckContacts=@($proof.widerDuckObservations | Where-Object status -EQ 'duck_contact_needs_fidelity_review').Count;
  widerDuckKinematicsUnproven=@($proof.widerDuckObservations | Where-Object status -EQ 'duck_miss_kinematics_unproven').Count;
  pairedFields=$proof.pairedFields;tests=20;checkedInputs=$proof.inputHashes.PSObject.Properties.Count;
  scope=$proof.scope;inputHashes=$proof.inputHashes} | ConvertTo-Json -Depth 5 | Out-File "$out/result.json" -Encoding utf8
 'Bounded current matrix verified; wider cannonball and full acceptance remain false.'
}finally{Pop-Location}
