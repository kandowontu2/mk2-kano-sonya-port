param(
    [Parameter(Mandatory=$true)][string]$OutputZip,
    [string]$CandidateName=''
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$launcher=Get-Content -LiteralPath (Join-Path $root 'PLAY_MK2_KANO_SONYA.cmd') -Raw
$launcherTarget=[regex]::Match($launcher,
    '(?im)^set "MK2_CANDIDATE_CMD=%~dp0(diagnostic_v[0-9]+_[a-z0-9_]+)\\PLAY_CANDIDATE\.cmd"\s*$')
if(-not $launcherTarget.Success){throw 'Cannot resolve the current playable launcher target.'}
if(-not $CandidateName){$CandidateName=$launcherTarget.Groups[1].Value}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){
    throw 'Use a versioned candidate directory name.'
}
if($CandidateName -ne $launcherTarget.Groups[1].Value){
    throw 'CandidateName differs from the playable CMD target; packaging would create a broken launcher.'
}
$candidate=Join-Path $root $CandidateName
$OutputZip=[IO.Path]::GetFullPath($OutputZip)
if(Test-Path -LiteralPath $OutputZip){throw "Output already exists: $OutputZip"}
$files=@(
    (Join-Path $root 'PLAY_MK2_KANO_SONYA.cmd'),
    (Join-Path $root 'PLAYTEST_README.txt'),
    (Join-Path $candidate 'PLAY_CANDIDATE.cmd'),
    (Join-Path $candidate 'mkport_candidate.exe'),
    (Join-Path $candidate 'roms\mk2ks\mk2ks.mdata')
)
foreach($dir in @('roms','samples','artwork')){
    $files+=Get-ChildItem -LiteralPath (Join-Path $root $dir) -File -Recurse |
        ForEach-Object FullName
}
$files=@($files | Sort-Object -Unique)
foreach($file in $files){
    if(-not (Test-Path -LiteralPath $file -PathType Leaf)){
        throw "Missing package input: $file"
    }
}
$before=@{}
foreach($file in $files){$before[$file]=(Get-FileHash -LiteralPath $file).Hash}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$stream=[IO.File]::Open($OutputZip,[IO.FileMode]::CreateNew)
$archive=[IO.Compression.ZipArchive]::new(
    $stream,[IO.Compression.ZipArchiveMode]::Create,$false)
try {
    foreach($file in $files){
        $relative=$file.Substring($root.Length).TrimStart('\','/').Replace('\','/')
        [IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
            $archive,$file,$relative,[IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
} finally {
    $archive.Dispose()
    $stream.Dispose()
}
foreach($file in $files){
    if((Get-FileHash -LiteralPath $file).Hash -ne $before[$file]){
        throw "Package input changed during creation: $file"
    }
}
$zip=[IO.Compression.ZipFile]::OpenRead($OutputZip)
try {
    if($zip.Entries.Count -ne $files.Count){throw 'Archive entry count mismatch.'}
    $names=@($zip.Entries | ForEach-Object FullName)
    foreach($required in @('PLAY_MK2_KANO_SONYA.cmd',
            "$CandidateName/mkport_candidate.exe",
            "$CandidateName/roms/mk2ks/mk2ks.mdata",
            'roms/mk2.zip','samples/mk2ks/kano_select.wav')){
        if($required -notin $names){throw "Missing archive entry: $required"}
    }
} finally {$zip.Dispose()}
Write-Output "Package: $OutputZip"
Write-Output "Entries: $($files.Count)"
Write-Output "SHA256: $((Get-FileHash -LiteralPath $OutputZip).Hash)"
