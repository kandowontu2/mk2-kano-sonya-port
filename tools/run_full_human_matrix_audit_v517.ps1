param([string]$CaseName='audit_v524_full_human_matrix_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try{
 & $python tools/test_full_human_matrix_v517.py 2>&1 | Out-File "$out/counterexamples.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Contract tests failed'}
 & $python tools/verify_full_human_matrix_v517.py | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Fresh matrix verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 if(-not $proof.boundedMatrixPassed -or $proof.passed -or $proof.fullPortAcceptance){throw 'Scope invariant changed'}
 foreach($entry in $proof.inputHashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Verified input changed: $($entry.Name)"}
  if([IO.Path]::GetExtension($entry.Name) -eq '.py'){Copy-Item -LiteralPath $entry.Name -Destination "$out/input_sources"}
 }
 Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"
 $proof.inputHashes | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 [ordered]@{passed=$false;boundedMatrixPassed=$true;fullPortAcceptance=$false;candidate=$proof.candidate;
  positiveCases=$proof.positiveCases;negativeCases=$proof.negativeCases;pairedFields=$proof.pairedFields;
  tests=8;checkedInputs=@($proof.inputHashes.PSObject.Properties).Count;scope=$proof.scope;
  verificationSHA256=(Get-FileHash "$out/verification.json").Hash;
  counterexampleTestSHA256=(Get-FileHash "$out/counterexamples.log").Hash;
  inputHashes=$proof.inputHashes} | ConvertTo-Json -Depth 5 | Out-File "$out/result.json" -Encoding utf8
 'Fresh 52-case v517 matrix verified; full-game acceptance remains open.'
}finally{Pop-Location}
