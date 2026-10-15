param(
    [Parameter(Mandatory=$true)][string]$ZipPath,
    [Parameter(Mandatory=$true)][string]$CandidateName
)
$ErrorActionPreference='Stop'
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){
    throw 'Use a versioned candidate directory name.'
}
$root=Split-Path $PSScriptRoot -Parent
$ZipPath=(Resolve-Path -LiteralPath $ZipPath).Path
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip=[IO.Compression.ZipFile]::OpenRead($ZipPath)
$seen=[collections.generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$verified=0
try {
    foreach($entry in $zip.Entries){
        $relative=$entry.FullName.Replace('/','\')
        if($entry.FullName.StartsWith('/') -or $entry.FullName -match '(^|/)\.\.(/|$)' -or
            -not $seen.Add($entry.FullName)){
            throw "Unsafe or duplicate ZIP entry: $($entry.FullName)"
        }
        $source=[IO.Path]::GetFullPath((Join-Path $root $relative))
        if(-not $source.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase) -or
            -not (Test-Path -LiteralPath $source -PathType Leaf)){
            throw "No matching package input: $($entry.FullName)"
        }
        if($entry.Length -ne (Get-Item -LiteralPath $source).Length){
            throw "ZIP length differs from source: $($entry.FullName)"
        }
        $sha=[Security.Cryptography.SHA256]::Create()
        $stream=$entry.Open()
        try {
            $digest=[Convert]::ToHexString($sha.ComputeHash($stream))
        } finally {
            $stream.Dispose()
            $sha.Dispose()
        }
        if($digest -ne (Get-FileHash -LiteralPath $source).Hash){
            throw "ZIP content differs from source: $($entry.FullName)"
        }
        $verified++
    }
    foreach($required in @('PLAY_MK2_KANO_SONYA.cmd','PLAYTEST_README.txt',
        "$CandidateName/PLAY_CANDIDATE.cmd",
        "$CandidateName/mkport_candidate.exe",
        "$CandidateName/roms/mk2ks/mk2ks.mdata",
        'roms/mk2.zip','samples/mk2ks/kano_select.wav')){
        if(-not $seen.Contains($required)) {throw "Missing ZIP entry: $required"}
    }
} finally {$zip.Dispose()}
Write-Output "Verified $verified ZIP entries byte-for-byte against current release inputs."
Write-Output "ZIP SHA256: $((Get-FileHash -LiteralPath $ZipPath).Hash)"
