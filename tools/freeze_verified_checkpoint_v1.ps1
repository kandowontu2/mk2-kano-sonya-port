param([Parameter(Mandatory=$true)][string]$CaseName,
 [string]$ReportName='verification.json',[string[]]$ExtraFiles=@(),[string[]]$ExtraDirectories=@())
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned checkpoint required'}
$out=Join-Path $root $CaseName
$report=Join-Path $out $ReportName
$manifest=Join-Path $out 'input_hashes.json'
if(Test-Path -LiteralPath $manifest){throw 'Refusing to replace a frozen manifest'}
$proof=Get-Content -LiteralPath $report -Raw | ConvertFrom-Json
$inputs=$proof.inputHashes
if($null -eq $inputs){$inputs=$proof.checked_inputs}
if($null -eq $inputs){throw 'No checked-input inventory in report'}
$hashes=[ordered]@{}
foreach($item in $inputs.PSObject.Properties){
 if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Verified input changed: $($item.Name)"}
 $hashes[$item.Name]=$item.Value
}
$extra=@($PSCommandPath,$report)+$ExtraFiles
foreach($directory in $ExtraDirectories){$extra+=@(Get-ChildItem -LiteralPath $directory -File -Recurse | ForEach-Object {$_.FullName})}
$extra+=@(Get-ChildItem -LiteralPath $out -File | Where-Object {$_.Name -notin 'input_hashes.json','manifest-check.json'} | ForEach-Object {$_.FullName})
foreach($file in $extra){
 $absolute=(Resolve-Path -LiteralPath $file).Path
 $hashes[$absolute]=(Get-FileHash -LiteralPath $absolute).Hash
}
$frozen=Join-Path $out 'frozen_tools'
New-Item -ItemType Directory -Path $frozen | Out-Null
foreach($file in @($hashes.Keys)){
 if([IO.Path]::GetExtension($file) -notin '.py','.ps1','.lua'){continue}
 $copy=Join-Path $frozen ([IO.Path]::GetFileName($file))
 if(Test-Path -LiteralPath $copy){
  if((Get-FileHash -LiteralPath $copy).Hash -ne $hashes[$file]){throw "Conflicting frozen source basename: $file"}
 }else{Copy-Item -LiteralPath $file -Destination $copy}
 $hashes[$copy]=(Get-FileHash -LiteralPath $copy).Hash
}
$hashes | ConvertTo-Json -Depth 4 | Out-File -LiteralPath $manifest -Encoding utf8
$changed=@()
foreach($item in $hashes.GetEnumerator()){
 if((Get-FileHash -LiteralPath $item.Key).Hash -ne $item.Value){$changed+=$item.Key}
}
[ordered]@{checked_inputs=$hashes.Count;changed_inputs=$changed;manifest_sha256=(Get-FileHash -LiteralPath $manifest).Hash;
 scope='Frozen retained evidence and source inputs, not an expanded gameplay or full-port acceptance claim'} |
 ConvertTo-Json -Depth 4 | Out-File -LiteralPath (Join-Path $out 'manifest-check.json') -Encoding utf8
if($changed.Count){throw 'Checkpoint inputs changed while freezing'}
"${CaseName}: $($hashes.Count) inputs frozen; zero changed"
