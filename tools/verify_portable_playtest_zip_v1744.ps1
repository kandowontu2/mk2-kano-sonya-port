$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskOut=Join-Path $taskRoot 'audit_v1744_portable_playtest_zip_checked'
if(Test-Path -LiteralPath $taskOut){throw 'Preserve prior evidence'}
$taskPackage=Join-Path $taskRoot 'release_v1743_current_playtest'
$taskInfo=Get-Content -LiteralPath "$taskPackage\package-report.json" -Raw | ConvertFrom-Json
if(-not $taskInfo.passed -or (Get-FileHash -LiteralPath $taskInfo.zip).Hash -ne $taskInfo.zipSHA256){throw 'Matched package required'}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$taskArchive=[IO.Compression.ZipFile]::OpenRead($taskInfo.zip)
try{
 $taskEntries=@($taskArchive.Entries | ForEach-Object {$_.FullName})
 if(($taskEntries | Select-Object -Unique).Count -ne $taskEntries.Count){throw 'Duplicate archive entries'}
 foreach($taskName in $taskEntries){if($taskName -match '(^[\/]|:|(^|[\/])\.\.([\/]|$))'){throw 'Unsafe archive entry'}}
}finally{$taskArchive.Dispose()}
New-Item -ItemType Directory -Path "$taskOut\extracted" | Out-Null
[IO.Compression.ZipFile]::ExtractToDirectory($taskInfo.zip,"$taskOut\extracted")
$taskPortable=Join-Path "$taskOut\extracted" 'MK2_Kano_Sonya_v1597_CURRENT_PLAYTEST'
$taskManifest=Get-Content -LiteralPath "$taskPortable\RELEASE.json" -Raw | ConvertFrom-Json
$taskActual=@(Get-ChildItem -LiteralPath $taskPortable -File -Recurse | ForEach-Object {$_.FullName.Substring($taskPortable.Length+1).Replace('\','/')})
$taskExpected=@('RELEASE.json')+@($taskManifest.files.PSObject.Properties.Name)
if(@(Compare-Object ($taskActual | Sort-Object) ($taskExpected | Sort-Object)).Count){throw 'Exact complete package inventory required'}
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$taskPortable\CHECK_FILES.ps1"
if($LASTEXITCODE -ne 0){throw 'Portable package hash guard failed'}
Push-Location $taskPortable
try{
 & "$taskPortable\mkport.exe" mk2ks -rompath roms -verifyroms 2>&1 | Out-File -LiteralPath "$taskOut\rom-audit.log" -Encoding utf8
 $taskROMExit=$LASTEXITCODE
}finally{Pop-Location}
if($taskROMExit -ne 0){throw 'Extracted package ROM audit failed'}
$taskROMLog=Get-Content -LiteralPath "$taskOut\rom-audit.log" -Raw
if($taskROMLog -notmatch 'romset mk2ks.*is good'){throw 'No authoritative good ROM result'}
# Invoke the CMD from a DIFFERENT cwd with no Python or developer guard scripts.
Push-Location ([IO.Path]::GetTempPath())
try{
 & "$taskPortable\PLAY.cmd" -skip_gameinfo -video none -sound none -noautoframeskip -frameskip 0 -nothrottle -str 8 2>&1 | Out-File -LiteralPath "$taskOut\cmd-boot.log" -Encoding utf8
 $taskBootExit=$LASTEXITCODE
}finally{Pop-Location}
$taskBootLog=Get-Content -LiteralPath "$taskOut\cmd-boot.log" -Raw
if($taskBootExit -ne 0 -or $taskBootLog -notmatch 'Average speed:' -or $taskBootLog -match 'WRONG CHECKSUMS|might not run correctly|fatal error|LUA ERROR|missing|not found'){throw 'Extracted current CMD cold boot failed'}
foreach($taskItem in $taskManifest.files.PSObject.Properties){if((Get-FileHash -LiteralPath (Join-Path $taskPortable $taskItem.Name)).Hash -ne $taskItem.Value){throw 'Package input mutated during boot'}}
if((Get-FileHash -LiteralPath $taskInfo.zip).Hash -ne $taskInfo.zipSHA256){throw 'ZIP mutated'}
[ordered]@{passed=$true;candidate=$taskManifest.candidate;zip=$taskInfo.zip;zipSHA256=$taskInfo.zipSHA256;zipBytes=$taskInfo.zipBytes;files=$taskInfo.files;extractedFilesExactlyMatchManifest=$true;allPackagedHashesMatch=$true;romAuditExit=$taskROMExit;cmdColdBootExit=$taskBootExit;cmdRunsFromDifferentWorkingDirectory=$true;developmentWorkspaceNotRequired=$true;noPythonOrDiagnosticScriptsInPackage=$true;currentStatePlaytest=$true;finishedRelease=$false;fullPortAcceptance=$false;scope='Exact ZIP inventory/hashes, extracted ROM audit and normal cold CMD boot using headless video/audio. GUI interaction, all gameplay and final release not certified.'} | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut\report.json" -Encoding utf8
Get-Content -LiteralPath "$taskOut\report.json" -TotalCount 22
