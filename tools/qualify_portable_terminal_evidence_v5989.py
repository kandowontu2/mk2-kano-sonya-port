"""Qualify actual5987 terminal boots and finish its owned extraction cleanup.

No re-extraction or native rerun: the real windowed boot exited0 with D3D and
DirectSound, but broad NOT FOUND matched normal optional-device diagnostics.
Fix the cleanup's Python-string backslash loss using a raw PowerShell string.
The original failed report/source/logs stay immutable, not overwritten.
"""
import base64,datetime,gzip,json,os,re,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OLD=ROOT/'audit_v5988_current_portable_playtest_checked'
OUT=ROOT/'audit_v5990_current_portable_terminal_checked'
PS=Path(os.environ['SystemRoot'])/'System32/WindowsPowerShell/v1.0/powershell.exe'

def save(name,data):
 (OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def ps(code):
 data=base64.b64encode(code.encode('utf-16le')).decode()
 return subprocess.run([str(PS),'-NoProfile','-EncodedCommand',data],capture_output=True,text=True)

def run():
 need(not OUT.exists(),'Fresh additive actual-terminal qualification')
 current.expected()
 failed=json.loads((OLD/'report.json').read_text())
 need(not failed['passed']and 'Actual finite portable CMD boot terminal zero'in failed['error']and
      'Unsafe temporary cleanup target'in failed['cleanupError'],'Retain the actual broad-match and cleanup-guard failures')
 meta_path=ROOT/'release_v5986_current_playtest/package-report.json';meta=json.loads(meta_path.read_text())
 parent_path=ROOT/'audit_v5983_current_launcher_handoff_progress/progress.json';parent=json.loads(parent_path.read_text())
 pins=json.loads((OLD/'source_pins.json').read_text())
 pins.update({str(p):sha(p)for p in OLD.rglob('*')if p.is_file()})
 pins.update({str(Path(__file__).resolve()):sha(__file__),str(parent_path):sha(parent_path)})
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and meta['passed']and all(sha(p)==h for p,h in pins.items()),
      'Actual current pair/package/failed evidence/full requirements preserved')
 temp_identity=json.loads((OLD/'temporary_identity.json').read_text());temporary=Path(temp_identity['exactPath'])
 package=temporary/'MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST'
 need(package.is_dir()and all(sha(package/p)==h for p,h in meta['archiveMemberHashes'].items()),
      'Existing single extraction is exact, including every actually corrupted/restored dependency')
 check=json.loads((OLD/'checker_positive.json').read_text());faults=json.loads((OLD/'actual_dependency_faults.json').read_text())
 audit=json.loads((OLD/'rom_audit.json').read_text())
 need(check['exitCode']==0 and 'all sixteen voice assets'in check['stdout']and len(faults)==4 and
      {(f['relativePath'],f['offset'])for f in faults}=={('mkport.exe',512),('roms/mk2ks/mk2ks.mdata',0),('samples/mk2ks/sonya_wins.wav',44),('artwork/mk2ks/default.lay',5)}and
      all(f['actualTemporaryByteChanged']and f['rejectedExitCode']==1 and f['restoredExitCode']==0 and f['relativePath']in f['deniedOutput']and
          f['restoredSHA256']==meta['archiveMemberHashes'][f['relativePath']]for f in faults),
      'Whole actual checker accepts package and denies all four real temporary faults with exact positive restoration')
 need(audit['exitCode']==0 and 'romset mk2ks [mk2] is good'in audit['stdout']and audit['stderr']=='',
      'Actual external-cwd packaged ROM audit terminal0')
 OUT.mkdir();save('input_pins.json',pins)
 census=ps("Get-CimInstance Win32_Process | Select-Object ProcessId,Name,ExecutablePath,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress")
 need(census.returncode==0,'Fresh actual OS process state')
 jobs=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(jobs,dict):jobs=[jobs]
 boots=[]
 for label in('headless','windowed_default_backends'):
  process=json.loads((OLD/(label+'_process.json')).read_text())
  live=json.loads((OLD/(label+'_live_census.json')).read_text())
  terminal=json.loads((OLD/(label+'_terminal.json')).read_text())
  old_terminal=json.loads((OLD/(label+'_terminal_census.json')).read_text())
  stdout=gzip.open(OLD/(label+'_stdout.log.gz'),'rt',encoding='utf-8').read()
  stderr=gzip.open(OLD/(label+'_stderr.log.gz'),'rt',encoding='utf-8').read()
  native=[j for j in live if j['ExecutablePath']and os.path.normcase(j['ExecutablePath'])==os.path.normcase(str(package/'mkport.exe'))and j['createdUnix']>=process['startedUnix']]
  need(len(native)==1 and terminal['exitCode']==0 and terminal['observedUnix']>native[0]['createdUnix']and
       not any(j==native[0]for j in old_terminal)and not any(j==native[0]for j in jobs),
       'Actual live executable/PID/name/creation/full-command instance and finite exit0 independently rechecked terminal')
  cmd=native[0]['CommandLine']or''
  need('-nocheat'in cmd and '-samples'in cmd and '-samplerate 48000'in cmd and '-str 12'in cmd and
       all(s not in cmd for s in(str(ROOT),'-autoboot_script','-cheat '))and
       'Checked current playtest:'in stdout and stderr==''and not re.search(
       r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|stack traceback|access violation|Could not find XAudio2|failed to initialize',stdout,re.I),
       'Actual standalone checked CMD no development dependency, cheats, diagnostic inputs or genuine ROM/runtime/backend errors')
  if label=='headless':need('-video none -sound none'in cmd,'Original exact finite headless command')
  else:
   need('-window -nomaximize -verbose'in cmd and '-video none'not in cmd and '-sound none'not in cmd and
        'Direct3D: Device created at 400x300'in stdout and 'Direct3D: HLSL initialized'in stdout and
        'DirectSound: Primary buffer: 48000 Hz, 16 bits, 2 channels'in stdout,
        'Actual ordinary windowed native video device/HLSL and physical audio buffer initialized, not assumed XAudio')
   optional=[line for line in stdout.splitlines()if 'not found'in line.lower()]
   need(len(optional)==7 and all(line.startswith('Optional ')for line in optional),'Only normal declared optional-device/shared-region not-found messages')
  boots.append(dict(label=label,nativeIdentity=native[0],actualFiniteExitCode=terminal['exitCode'],
                    physicalBackendInitializationObserved=label=='windowed_default_backends',
                    originalTerminalLogSHA256=sha(OLD/(label+'_stdout.log.gz'))))
 save('qualified_actual_native_boots.json',boots)
 # Explicitly recheck prior user settings, not merely infer isolation from paths.
 settings_path=ROOT/'audit_v5979_current_launcher_identity_checked/settings_before.json'
 settings=json.loads(settings_path.read_text());need(all(sha(p)==h for p,h in settings.items()),'Every prior measured user/default/old setting unchanged')
 pins[str(settings_path)]=sha(settings_path)
 inventory=[dict(path=str(p.relative_to(temporary)),bytes=p.stat().st_size,sha256=sha(p))for p in temporary.rglob('*')if p.is_file()]
 save('temporary_inventory.json',inventory)
 pngs=[p for p in inventory if p['path'].lower().endswith('.png')]
 need(len(pngs)==2,'Both real finite -str boots generated a small final PNG, explicitly counted')
 code=r"""$ErrorActionPreference='Stop'
$taskExpected='TARGET'
$taskResolved=(Resolve-Path -LiteralPath $taskExpected).ProviderPath
$taskTemp=[IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\')
if($taskResolved -ne $taskExpected -or [IO.Path]::GetDirectoryName($taskResolved) -ne $taskTemp -or
   [IO.Path]::GetFileName($taskResolved) -notlike 'mk2-portable-v5987-*'){throw 'Unsafe temporary cleanup target'}
$taskItems=@(Get-Item -LiteralPath $taskResolved)+@(Get-ChildItem -LiteralPath $taskResolved -Force -Recurse)
if(@($taskItems | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'No reparse-point deletion'}
if(@(Get-CimInstance Win32_Process | Where-Object {($_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskResolved+'\',[StringComparison]::OrdinalIgnoreCase)) -or ($_.CommandLine -and $_.CommandLine.Contains($taskResolved))}).Count){throw 'Temporary native/launcher process remains live'}
$taskBytes=($taskItems | Where-Object {-not $_.PSIsContainer} | Measure-Object Length -Sum).Sum
$taskFiles=@($taskItems | Where-Object {-not $_.PSIsContainer}).Count
Remove-Item -LiteralPath $taskResolved -Recurse -Force
if(Test-Path -LiteralPath $taskResolved){throw 'Temporary extraction still exists'}
@{removedExactPath=$taskResolved;removedFiles=$taskFiles;logicalBytesRemoved=$taskBytes;removed=$true;recoverableFromRetainedZIP=$true} | ConvertTo-Json -Compress
""".replace('TARGET',str(temporary).replace("'","''"))
 deletion=ps(code);save('cleanup_command_result.json',dict(exitCode=deletion.returncode,stdout=deletion.stdout,stderr=deletion.stderr))
 need(deletion.returncode==0 and not temporary.exists(),'Exact owned temporary extraction removed after verified native terminal state')
 removal=json.loads(deletion.stdout);save('temporary_cleanup.json',removal)
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All original sources/failed evidence/package/settings bytes remain unchanged')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             parent=str(parent_path),remaining=parent['remaining'],requirementAudit=parent['requirementAudit'],
             retainedFailedCollector=str(OLD/'report.json'),actualTerminalEvidenceQualifiedWithoutRerun=True,
             zip=meta['zip'],zipSHA256=meta['zipSHA256'],zipBytes=meta['zipBytes'],
             standalonePackageCheckerAccepted=True,actualTemporaryDependencyFaultsRejected=len(faults),actualROMAuditPassed=True,
             actualNativeBoots=boots,developmentRuntimeToolsOnPATH=False,preExistingUserSettingsUnchanged=True,
             temporaryExtractionRemoved=removal,automaticTimedStopPNGs=pngs,
             priorNoRawRecordingWordingCorrection='Two older pinned 1692-byte timed-stop PNGs are retained. Two new timed-stop PNGs were counted and deleted with the owned extraction; no raw RGB/audio/guest dumps were created.',
             physicalVideoAudioBackendInitializationObserved=True,interactiveVisualAudibleQualityAccepted=False,
             integratedWholeReleaseRegressionComplete=False,fullPortAcceptance=False,newBuilds=0,newZIPs=0,newRawRGBOrAudioRecordings=0,
             inputHashes=pins)

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 save('report.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','requirementAudit')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
