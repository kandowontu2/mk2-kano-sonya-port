param([ValidateSet(1,2)][int]$Worker)
# Compression-only assistance to the existing archive job. Never removes or
# edits source folders. The original job remains the sole removal authority.
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$archiveRoot=Join-Path $root '_archive/legacy_evidence_v284'
$plan=Get-Content -LiteralPath "$archiveRoot/plan.json" -Raw | ConvertFrom-Json
if($plan.root -ne $root){throw 'Archive plan belongs to another workspace'}
$batches=@();$batch=@();$bytes=0L
foreach($target in $plan.targets){
    if($batch.Count -ge 100 -or ($batch.Count -gt 0 -and $bytes+$target.bytes -gt 2GB)){
        $batches+=,@($batch);$batch=@();$bytes=0L
    }
    $batch+=$target;$bytes+=$target.bytes
}
if($batch.Count){$batches+=,@($batch)}
Push-Location $root
try {
    for($index=$batches.Count;$index -ge 1;$index--){
        if(($index % 2) -ne ($Worker % 2)){continue}
        $progress=Get-Content -LiteralPath "$archiveRoot/progress.json" -Raw | ConvertFrom-Json
        # Stay well ahead of the primary job. Publishing uses a completed,
        # closed archive; it never exposes the compressor's partial output.
        if($index -le $progress.completed_batches+5){break}
        $label='batch_{0:D3}' -f $index
        $archive=Join-Path $archiveRoot "$label.7z"
        if(Test-Path -LiteralPath $archive){continue}
        $temp=Join-Path $archiveRoot "prefill_${Worker}_${label}.7z"
        if(Test-Path -LiteralPath $temp){throw 'Refusing to overwrite a prefill attempt'}
        $names=@()
        foreach($target in $batches[$index-1]){
            if($target.version -ge 260 -or $target.version -in $plan.test_fixture_versions_preserved -or
               (Split-Path $target.path -Parent) -ne $root -or
               -not $target.path.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase) -or
               (Resolve-Path -LiteralPath $target.path).Path -ne $target.path){throw 'Unsafe prefill source'}
            $names+=$target.name
        }
        & 'C:/Program Files/7-Zip/7z.exe' a -t7z $temp @names -mx=3 -md=64m -mmt=2 -ms=on -bso0 -bsp0 -bse1 2>&1 |
            Out-File -LiteralPath "$archiveRoot/prefill_${Worker}_${label}.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Prefill compression failed; no source folders were changed'}
        & 'C:/Program Files/7-Zip/7z.exe' t $temp -bso0 -bsp0 -bse1 2>&1 |
            Out-File -LiteralPath "$archiveRoot/prefill_${Worker}_${label}.verify.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Prefill verification failed; no source folders were changed'}
        $progress=Get-Content -LiteralPath "$archiveRoot/progress.json" -Raw | ConvertFrom-Json
        if($index -le $progress.completed_batches+1 -or (Test-Path -LiteralPath $archive)){
            # Only our exact generated staging file is discarded. The primary
            # job's archive and all source files are left untouched.
            Remove-Item -LiteralPath $temp -Force
            continue
        }
        try {
            Move-Item -LiteralPath $temp -Destination $archive -ErrorAction Stop
        } catch {
            if(Test-Path -LiteralPath $archive){Remove-Item -LiteralPath $temp -Force;continue}
            throw
        }
        Write-Output "Compression prefilled $label; original folders untouched"
    }
} finally {Pop-Location}
'Compression prefill finished; primary archive job still owns all verification/removal'
