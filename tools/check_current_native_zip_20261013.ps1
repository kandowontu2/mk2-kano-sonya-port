$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskRelease=Join-Path $taskRoot 'release_current_native_playtest_20261013'
$taskZip=Join-Path $taskRelease 'MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013.zip'
if((Get-FileHash -LiteralPath $taskZip).Hash -ne '9481CF6938EF23CBBA58101C3E0118B137E3005C7A04E9CB0E95B4E3362B8842'){throw 'Archive changed'}
$taskAudit=Join-Path $taskRoot 'audit_current_native_zip_portable_check_20261013'
if(Test-Path -LiteralPath $taskAudit){throw 'Never overwrite an executed check'}
New-Item -ItemType Directory -Path $taskAudit | Out-Null
$taskTemp=Join-Path $taskAudit 'temporary_extracted_package'
New-Item -ItemType Directory -Path $taskTemp | Out-Null
$taskResolved=[IO.Path]::GetFullPath($taskTemp)
if($taskResolved -ne [IO.Path]::GetFullPath((Join-Path $taskAudit 'temporary_extracted_package')) -or -not $taskResolved.StartsWith([IO.Path]::GetFullPath($taskAudit)+[IO.Path]::DirectorySeparatorChar)){throw 'Unsafe temporary target'}
try {
 Add-Type -AssemblyName System.IO.Compression.FileSystem
 [IO.Compression.ZipFile]::ExtractToDirectory($taskZip,$taskResolved)
 $taskPlay=Join-Path $taskResolved 'MK2_Kano_Sonya_Playtest\PLAY.cmd'
 $taskOutput=& $taskPlay --check 2>&1
 $taskExit=$LASTEXITCODE
 $taskOutput | Set-Content -LiteralPath (Join-Path $taskAudit 'check.log')
 if($taskExit -ne 0 -or ($taskOutput -join "`n") -notmatch 'complete mk2ks ROM set is good'){throw 'Portable check failed'}
 [ordered]@{passedPortableHashAndROMCheck=$true;extractedCMDChecked=$true;exitCode=$taskExit;interactiveBootTested=$false;fullPortAccepted=$false;temporaryExtractionRemoved=$true}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $taskAudit 'report.json')
 $taskOutput
} finally {
 $taskActual=(Resolve-Path -LiteralPath $taskResolved).Path
 if($taskActual -ne $taskResolved){throw 'Temporary target resolution changed'}
 if(Get-ChildItem -LiteralPath $taskActual -Recurse -Force | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}){throw 'Refuse cleanup through reparse points'}
 Remove-Item -LiteralPath $taskActual -Recurse -Force
}
