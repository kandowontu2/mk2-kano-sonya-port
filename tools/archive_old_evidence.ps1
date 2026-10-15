param([switch]$Execute)
# Consolidate historical output, never sources/current inputs. Archive verification
# completes before any original directory is removed; every batch is recoverable.
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$archiveRoot=Join-Path $root '_archive/legacy_evidence_v284'
$sevenzip='C:/Program Files/7-Zip/7z.exe'
if(-not(Test-Path -LiteralPath $sevenzip)){throw 'Verified archiving requires the installed 7-Zip tool'}
$protected=[Collections.Generic.HashSet[int]]::new()
foreach($version in @(42,43,249)){$null=$protected.Add($version)}
foreach($test in Get-ChildItem -LiteralPath $PSScriptRoot -Filter 'test_*.py' -File){
    foreach($hit in [regex]::Matches((Get-Content -LiteralPath $test.FullName -Raw),'(?:audit|diagnostic|regression|control|baseline)_v(\d+)')){
        $null=$protected.Add([int]$hit.Groups[1].Value)
    }
}
$targets=@()
foreach($dir in Get-ChildItem -LiteralPath $root -Directory){
    if($dir.Name -notmatch '^(audit|diagnostic|regression|control|trace|pilot|reference)_v(\d+)_'){continue}
    $version=[int]$Matches[2]
    if($version -ge 260 -or $protected.Contains($version)){continue}
    if($dir.Attributes -band [IO.FileAttributes]::ReparsePoint){continue}
    $bytes=0L;$files=0;$links=$false
    foreach($entry in Get-ChildItem -LiteralPath $dir.FullName -Recurse -Force){
        if($entry.Attributes -band [IO.FileAttributes]::ReparsePoint){$links=$true;break}
        if(-not $entry.PSIsContainer){$bytes+=$entry.Length;$files++}
    }
    if($links){continue}
    $targets+=[pscustomobject]@{name=$dir.Name;path=$dir.FullName;version=$version;bytes=$bytes;files=$files}
}
$plan=[ordered]@{root=$root;operation='verified recoverable 7z archives, then removal of archived historical directories';
    current_versions_260_and_newer_preserved=$true;test_fixture_versions_preserved=@($protected | Sort-Object);
    target_folders=$targets.Count;logical_bytes=($targets | Measure-Object bytes -Sum).Sum;targets=$targets}
if(-not $Execute){$plan | ConvertTo-Json -Depth 5;exit}
if(Test-Path -LiteralPath $archiveRoot){throw 'Refusing to overwrite an archive run'}
if((Get-PSDrive -Name ([IO.Path]::GetPathRoot($root).TrimEnd('\').TrimEnd(':'))).Free -lt 3GB){throw 'At least 3 GB free is required for verified staging'}
$live=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match 'mkport|mame'} | Select-Object -ExpandProperty CommandLine)
foreach($target in $targets){
    if($target.path -eq $root -or (Split-Path $target.path -Parent) -ne $root -or -not $target.path.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Target escapes the named workspace'}
    foreach($command in $live){if($command -and $command.Contains($target.path)){throw 'A historical target is active'}}
}
New-Item -ItemType Directory -Path $archiveRoot -Force | Out-Null
$plan | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$archiveRoot/plan.json" -Encoding utf8
$freeBefore=(Get-PSDrive -Name C).Free
$batches=@();$batch=@();$batchBytes=0L
foreach($target in $targets){
    if($batch.Count -ge 100 -or ($batch.Count -gt 0 -and $batchBytes+$target.bytes -gt 2GB)){
        $batches+=,@($batch);$batch=@();$batchBytes=0L
    }
    $batch+=$target;$batchBytes+=$target.bytes
}
if($batch.Count){$batches+=,@($batch)}
$records=@();$index=0
Push-Location $root
try {
    foreach($batch in $batches){
        $index++;$label='batch_{0:D3}' -f $index
        $archive=Join-Path $archiveRoot "$label.7z"
        $names=@($batch | Select-Object -ExpandProperty name)
        $before=[ordered]@{}
        foreach($target in $batch){
            foreach($file in Get-ChildItem -LiteralPath $target.path -File -Recurse -Force){
                $relative=$file.FullName.Substring($root.Length+1)
                $before[$relative]=[ordered]@{bytes=$file.Length;sha256=(Get-FileHash -LiteralPath $file.FullName).Hash}
            }
        }
        $before | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$archiveRoot/$label.files.json" -Encoding utf8
        & $sevenzip a -t7z $archive @names -mx=3 -md=64m -mmt=2 -ms=on -bso0 -bsp0 -bse1 2>&1 |
            Out-File -LiteralPath "$archiveRoot/$label.archive.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Archive creation failed; original directories retained'}
        & $sevenzip t $archive -bso0 -bsp0 -bse1 2>&1 | Out-File -LiteralPath "$archiveRoot/$label.verify.log" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Archive CRC verification failed; original directories retained'}
        $archiveSizes=@{};$entryPath=$null
        $listing=& $sevenzip l $archive -slt -ba
        if($LASTEXITCODE -ne 0){throw 'Archive inventory failed; originals retained'}
        foreach($line in $listing){
            if($line.StartsWith('Path = ')){$entryPath=$line.Substring(7).Replace('/','\')}
            elseif($entryPath -and $line.StartsWith('Size = ')){$archiveSizes[$entryPath]=[int64]$line.Substring(7)}
        }
        foreach($relative in $before.Keys){
            if(-not $archiveSizes.ContainsKey($relative) -or $archiveSizes[$relative] -ne $before[$relative].bytes){throw 'Archive does not contain every original file at its exact path/size'}
        }
        # Recheck every source file after the archive is finalized. Changed source
        # evidence is never discarded just because an older archive tests green.
        foreach($relative in $before.Keys){
            $file=Join-Path $root $relative
            if((Get-Item -LiteralPath $file).Length -ne $before[$relative].bytes -or
                (Get-FileHash -LiteralPath $file).Hash -ne $before[$relative].sha256){throw 'Source changed during archiving; originals retained'}
        }
        $currentCount=0
        foreach($target in $batch){$currentCount+=@(Get-ChildItem -LiteralPath $target.path -File -Recurse -Force).Count}
        if($currentCount -ne $before.Count){throw 'Historical folder contents changed; originals retained'}
        foreach($target in $batch){
            $resolved=(Resolve-Path -LiteralPath $target.path).Path
            if($resolved -ne $target.path -or (Split-Path $resolved -Parent) -ne $root -or
                -not $resolved.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase) -or
                $target.version -ge 260 -or $protected.Contains($target.version)){throw 'Unsafe removal target'}
            Remove-Item -LiteralPath $resolved -Recurse -Force
        }
        $records+=[ordered]@{archive="$label.7z";archive_sha256=(Get-FileHash -LiteralPath $archive).Hash;
            folders=$names;source_files=$before.Count;logical_bytes=($batch | Measure-Object bytes -Sum).Sum;
            archive_bytes=(Get-Item -LiteralPath $archive).Length;crc_verified=$true;source_sha256_rechecked=$true;original_directories_removed=$true}
        [ordered]@{completed_batches=$index;total_batches=$batches.Count;records=$records} | ConvertTo-Json -Depth 6 |
            Out-File -LiteralPath "$archiveRoot/progress.json" -Encoding utf8
        Write-Output "$label verified and archived: $($batch.Count) historical folders"
    }
} finally {Pop-Location}
[ordered]@{complete=$true;target_folders=$targets.Count;logical_bytes=$plan.logical_bytes;free_before=$freeBefore;
    free_after=(Get-PSDrive -Name C).Free;archives=$records;current_build_and_fixtures_preserved=$true;
    recovery='Extract the relevant batch .7z into the mk2port root to restore its original folder names; .files.json contains original SHA256 hashes'} |
    ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$archiveRoot/result.json" -Encoding utf8
'Historical-folder consolidation complete; every removed folder is recoverable from its verified archive'
