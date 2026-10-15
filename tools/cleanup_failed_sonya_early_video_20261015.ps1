$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskCase=[IO.Path]::GetFullPath((Join-Path $taskRoot 'video_sonya_early_ladder_20261015'))
if(-not $taskCase.StartsWith($taskRoot+'\') -or (Get-Item -LiteralPath $taskCase).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe case path'}
$taskTerminal=Get-Content -LiteralPath (Join-Path $taskCase 'terminal.json') -Raw | ConvertFrom-Json
if($taskTerminal.fullPlaythrough -or $taskTerminal.exitCodes.mame -ne 0 -or $taskTerminal.exitCodes.ffmpeg -ne 0){throw 'Expected terminal failed completion attempt'}
$taskResult=Select-String -LiteralPath (Join-Path $taskCase 'run.log') -Pattern '^MK2_NAT_CAMPAIGN_RESULT '
if($taskResult.Count -ne 1 -or $taskResult.Line -notmatch 'ending=-1 ending_completed=-1'){throw 'Actual unfinished result required'}
if(@(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*video_sonya_early_ladder_20261015\*' -and $_.Name -in @('mkport_candidate.exe','ffmpeg.exe','python.exe') }).Count){throw 'Case process still live'}
$taskRows=@()
foreach($taskName in @('native_audio.wav','video.mp4')){
 $taskPath=Join-Path $taskCase $taskName
 $taskItem=Get-Item -LiteralPath $taskPath
 if($taskItem.PSIsContainer -or $taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint -or $taskItem.DirectoryName -ne $taskCase){throw 'Unsafe temporary target'}
 $taskRows+=@{name=$taskName;bytes=$taskItem.Length;sha256=(Get-FileHash -LiteralPath $taskPath).Hash}
 Remove-Item -LiteralPath $taskPath
 if(Test-Path -LiteralPath $taskPath){throw 'Not removed'}
}
@{removed=$taskRows;reason='Terminal200000 fields; Kitana not cleared and no ending; failed media not a deliverable';archived=$false;logsPreserved=$true} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskCase 'failed_temp_cleanup.json')
$taskRows | ConvertTo-Json -Compress
