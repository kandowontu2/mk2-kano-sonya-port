$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$out=Join-Path $root 'audit_v594_pit_lookup_checked_inputs'
if(Test-Path -LiteralPath $out){throw 'Never overwrite evidence'}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try{
    $python='C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe'
    & $python tools/test_pit_lookup_defect_v545_v2.py 2>&1 | Out-File "$out/tests.log" -Encoding utf8
    if($LASTEXITCODE-ne 0){throw 'Pit proof boundary tests failed'}
    & $python tools/verify_pit_lookup_defect_v545.py | Out-File "$out/proof.json" -Encoding utf8
    if($LASTEXITCODE-ne 0){throw 'Pit defect proof failed'}
    $proof=Get-Content "$out/proof.json" -Raw | ConvertFrom-Json
    $pins=@{}
    foreach($item in $proof.inputHashes.PSObject.Properties){$pins[$item.Name]=$item.Value}
    foreach($case in @('audit_v585_pit_group_provenance_kano_p1','audit_v592_pit_actual_lookup_sonya_p1')){
        $metadata=Get-Content "$case/result.json" -Raw | ConvertFrom-Json
        if($metadata.exit_code-ne 0-or $metadata.assistance-ne 'none'-or $metadata.unassisted_clear_proven){throw 'Terminal input-only diagnostic required'}
        foreach($item in $metadata.input_hashes.PSObject.Properties){
            if((Get-FileHash -LiteralPath $item.Name).Hash-ne $item.Value){throw "Diagnostic input changed: $($item.Name)"}
            if($pins.ContainsKey($item.Name)-and $pins[$item.Name]-ne $item.Value){throw 'Shared diagnostic input mismatch'}
            $pins[$item.Name]=$item.Value
        }
        Get-ChildItem -LiteralPath $case -File -Recurse | ForEach-Object {$pins[$_.FullName]=(Get-FileHash -LiteralPath $_.FullName).Hash}
    }
    foreach($file in @($PSCommandPath,'tools/test_pit_lookup_defect_v545_v2.py','tools/verify_pit_lookup_defect_v545.py')){
        $actual=(Resolve-Path -LiteralPath $file).Path;$pins[$actual]=(Get-FileHash -LiteralPath $actual).Hash
    }
    foreach($item in $pins.GetEnumerator()){if((Get-FileHash -LiteralPath $item.Key).Hash-ne $item.Value){throw "Checked input changed: $($item.Key)"}}
    $pins | ConvertTo-Json | Out-File "$out/checked_inputs.json" -Encoding utf8
    [ordered]@{passed=$true;defectEstablished=$true;fixed=$false;fullPortAcceptance=$false;tests=16;checkedInputs=$pins.Count;
        candidate=$proof.candidate;scope=$proof.scope;sonya_scope=$proof.sonyaScope;
        source_executable_payload_unchanged=$true;old_checker_boundary_preserved='audit_v593_pit_checker_boundary'} |
        ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    Get-Content "$out/result.json"
}finally{Pop-Location}
