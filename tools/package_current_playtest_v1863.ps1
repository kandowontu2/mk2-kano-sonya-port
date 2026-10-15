$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut=Join-Path $taskRoot 'release_v1863_current_playtest'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite a package'}
$taskCandidate=Join-Path $taskRoot 'diagnostic_v1836_ball_register_boundary'
$taskBuild=Get-Content -LiteralPath "$taskCandidate\build-info.json" -Raw | ConvertFrom-Json
if($taskBuild.executable_sha256 -ne '34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E' -or $taskBuild.payload_sha256 -ne '5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D'){throw 'Matched current test build only'}
foreach($taskItem in $taskBuild.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $taskItem.Name).Hash -ne $taskItem.Value){throw 'Changed compiled input'}}
$taskFiles=[ordered]@{}
$taskFiles['mkport.exe']="$taskCandidate\mkport_candidate.exe"
$taskFiles['roms/mk2.zip']="$taskRoot\roms\mk2.zip"
foreach($taskFile in Get-ChildItem -LiteralPath "$taskRoot\roms\mk2ks" -File){$taskFiles['roms/mk2ks/'+$taskFile.Name]=$taskFile.FullName}
$taskFiles['roms/mk2ks/mk2ks.mdata']="$taskCandidate\roms\mk2ks\mk2ks.mdata"
foreach($taskFile in Get-ChildItem -LiteralPath "$taskRoot\samples\mk2ks" -File){$taskFiles['samples/mk2ks/'+$taskFile.Name]=$taskFile.FullName}
foreach($taskFile in Get-ChildItem -LiteralPath "$taskRoot\artwork" -File){$taskFiles['artwork/'+$taskFile.Name]=$taskFile.FullName}
foreach($taskName in @('PLAY.cmd','CHECK_FILES.ps1','README.txt')){$taskFiles[$taskName]="$PSScriptRoot\playtest_release_v1862\$taskName"}
$taskFiles['LICENSE']="$taskRoot\mame-mkp\COPYING"
$taskHashes=[ordered]@{};$taskSources=[ordered]@{}
foreach($taskItem in $taskFiles.GetEnumerator()){
 if($taskItem.Key -match '(^[\/]|:|(^|[\/])\.\.([\/]|$))'){throw 'Unsafe archive name'}
 $taskHashes[$taskItem.Key]=(Get-FileHash -LiteralPath $taskItem.Value).Hash
 $taskSources[$taskItem.Value]=$taskHashes[$taskItem.Key]
}
if($taskHashes['mkport.exe'] -ne $taskBuild.executable_sha256 -or $taskHashes['roms/mk2ks/mk2ks.mdata'] -ne $taskBuild.payload_sha256){throw 'Changed executable/payload'}
if(@($taskFiles.Keys | Where-Object {$_ -like 'samples/mk2ks/*.wav'}).Count -lt 16){throw 'All tested voice assets required'}
$taskManifest=[ordered]@{candidate=$taskBuild.name;releaseStatus='CURRENT PLAYTEST - unfinished';fullPortAcceptance=$false;files=$taskHashes}
$taskJSON=$taskManifest | ConvertTo-Json -Depth 6
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskJSON | Out-File -LiteralPath "$taskOut\RELEASE.json" -Encoding utf8
$taskSources | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut\sources_before.json" -Encoding utf8
Add-Type -AssemblyName System.IO.Compression.FileSystem
$taskZIP=Join-Path $taskOut 'MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip'
$taskPrefix='MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST/'
$taskArchive=[IO.Compression.ZipFile]::Open($taskZIP,[IO.Compression.ZipArchiveMode]::Create)
try{
 foreach($taskItem in $taskFiles.GetEnumerator()){
  [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($taskArchive,$taskItem.Value,$taskPrefix+$taskItem.Key,[IO.Compression.CompressionLevel]::Optimal) | Out-Null
 }
 [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($taskArchive,"$taskOut\RELEASE.json",$taskPrefix+'RELEASE.json',[IO.Compression.CompressionLevel]::Optimal) | Out-Null
 foreach($taskDirectory in @('artwork/','play/')){$taskArchive.CreateEntry($taskPrefix+$taskDirectory) | Out-Null}
}finally{$taskArchive.Dispose()}
foreach($taskItem in $taskSources.GetEnumerator()){if((Get-FileHash -LiteralPath $taskItem.Key).Hash -ne $taskItem.Value){throw 'Source changed while packaging'}}
[ordered]@{passed=$true;zip=$taskZIP;zipSHA256=(Get-FileHash -LiteralPath $taskZIP).Hash;zipBytes=(Get-Item -LiteralPath $taskZIP).Length;files=$taskHashes.Count;candidate=$taskBuild.name;currentStatePlaytest=$true;portableRuntimeVerificationPending=$true;fullPortAcceptance=$false;sourceHashes=$taskSources} | ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$taskOut\package-report.json" -Encoding utf8
Get-Content -LiteralPath "$taskOut\package-report.json" -TotalCount 12
