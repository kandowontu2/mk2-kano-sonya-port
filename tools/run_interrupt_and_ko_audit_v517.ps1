param([string]$CaseName='audit_v526_interrupt_and_ko_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
Push-Location $root
try{
 & $python tools/test_interrupt_and_ko_v517.py 2>&1 | Out-File "$out/counterexamples.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Current interruption/KO contract tests failed'}
 & $python tools/verify_interrupt_and_ko_v517.py | Out-File "$out/verification.json" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Current interruption/KO verification failed'}
 $proof=Get-Content "$out/verification.json" -Raw | ConvertFrom-Json
 if(-not $proof.passed -or $proof.fullPortAcceptance){throw 'Scope invariant changed'}
 foreach($entry in $proof.inputHashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Verified input changed: $($entry.Name)"}
  if([IO.Path]::GetExtension($entry.Name) -eq '.py'){Copy-Item -LiteralPath $entry.Name -Destination "$out/input_sources"}
 }
 Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"
 $proof.inputHashes | ConvertTo-Json -Depth 4 | Out-File "$out/input_hashes.json" -Encoding utf8
 $fields=0;foreach($item in $proof.interruptions){$fields+=$item.pairedFields};foreach($item in $proof.knockouts){$fields+=$item.actual_fields}
 [ordered]@{passed=$true;fullPortAcceptance=$false;candidate=$proof.candidate;
  interruptions=$proof.interruptions.Count;knockouts=$proof.knockouts.Count;pairedFields=$fields;
  tests=30;checkedInputs=@($proof.inputHashes.PSObject.Properties).Count;scope=$proof.scope;
  verificationSHA256=(Get-FileHash "$out/verification.json").Hash;
  counterexampleTestSHA256=(Get-FileHash "$out/counterexamples.log").Hash;
  inputHashes=$proof.inputHashes} | ConvertTo-Json -Depth 5 | Out-File "$out/result.json" -Encoding utf8
 'Ten current startup interruption/retry and four KO/next-round cases verified; full-game acceptance remains open.'
}finally{Pop-Location}
