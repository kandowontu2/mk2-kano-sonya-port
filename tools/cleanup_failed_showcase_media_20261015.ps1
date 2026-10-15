$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\videos_showcase_20261015'
$taskReceipt=Join-Path $taskRoot 'failed_showcase_media_cleanup.json'
if(Test-Path -LiteralPath $taskReceipt){throw 'Cleanup already recorded'}
$taskPaths=@('kano_primary\native_audio.wav','kano_uppercut\native_audio.wav','kano_uppercut\video.mp4')
$taskRemoved=@()
foreach($taskRelative in $taskPaths){
 $taskPath=[IO.Path]::GetFullPath((Join-Path $taskRoot $taskRelative))
 if(-not $taskPath.StartsWith($taskRoot+'\')){throw 'Outside intended showcase directory'}
 $taskItem=Get-Item -LiteralPath $taskPath
 if($taskItem.PSIsContainer -or $taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint -or $taskItem.Directory.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe temporary target'}
 if(Test-Path -LiteralPath (Join-Path $taskItem.DirectoryName 'verification.json')){throw 'Not a failed case'}
 if(@(Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('python.exe','mkport_candidate.exe','ffmpeg.exe') -and $_.CommandLine -and $_.CommandLine.Contains($taskItem.DirectoryName) }).Count){throw 'Case still in use'}
 $taskRemoved+=@{path=$taskRelative;bytes=$taskItem.Length;sha256=(Get-FileHash -LiteralPath $taskPath).Hash}
 Remove-Item -LiteralPath $taskPath
 if(Test-Path -LiteralPath $taskPath){throw 'Not removed'}
}
@{removed=$taskRemoved;logsAndControllersKept=$true;successfulSourceClipsKept=$true;archiveCreated=$false} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskReceipt
$taskRemoved | ConvertTo-Json -Compress
