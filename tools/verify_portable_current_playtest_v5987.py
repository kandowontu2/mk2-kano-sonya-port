"""Actual requested ZIP extraction/checker/ROM/CMD boots outside the workspace.

One temporary extraction, no development PATH, no diagnostic autoboot or guest
state writes. Real temporary dependency faults are restored exactly. Both finite
native boots are settled before assertions. Remove only the owned extraction
after OS-confirmed native terminal state, preserving small evidence not copies.
"""
import base64,datetime,gzip,json,os,re,stat,subprocess,tempfile,time,traceback,zipfile
from pathlib import Path,PurePosixPath
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5988_current_portable_playtest_checked'
PACKAGE=ROOT/'release_v5986_current_playtest/package-report.json'
PARENT=ROOT/'audit_v5983_current_launcher_handoff_progress/progress.json'
PS=Path(os.environ['SystemRoot'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
TEMP=None
ENV=dict(os.environ)
ENV['PATH']=';'.join(str(Path(os.environ['SystemRoot'])/p)for p in('System32','System32/WindowsPowerShell/v1.0',''))
for key in list(ENV):
 if key.startswith(('MK2KS_','MK2_TRACE_','MK2_RANGE_','MK2_P2_')):ENV.pop(key)

def save(name,data):
 (OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def ps(code):
 encoded=base64.b64encode(code.encode('utf-16le')).decode()
 return subprocess.run([str(PS),'-NoProfile','-EncodedCommand',encoded],capture_output=True,text=True,env=ENV,cwd=str(OUT))

def census():
 answer=ps("Get-CimInstance Win32_Process -Filter \"Name='mkport.exe'\" | Select-Object ProcessId,Name,ExecutablePath,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress")
 need(answer.returncode==0,'Authoritative OS native-process census')
 jobs=json.loads(answer.stdout)if answer.stdout.strip()else[]
 return [jobs]if isinstance(jobs,dict)else jobs

def checker(package):
 return subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(package/'CHECK_FILES.ps1')],
                       cwd=str(OUT),env=ENV,capture_output=True,text=True)

def cleanup():
 if TEMP is None:return dict(temporaryExtractionCreated=False)
 # One shell end-to-end. Exact resolved target, actual system-temp parent, owned
 # prefix, no reparse points and no live process using this extraction.
 target=str(TEMP).replace("'","''")
 code="""$ErrorActionPreference='Stop'
$taskExpected='TARGET'
$taskResolved=(Resolve-Path -LiteralPath $taskExpected).ProviderPath
$taskTemp=[IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\')
if($taskResolved -ne $taskExpected -or [IO.Path]::GetDirectoryName($taskResolved) -ne $taskTemp -or
   [IO.Path]::GetFileName($taskResolved) -notlike 'mk2-portable-v5987-*') {throw 'Unsafe temporary cleanup target'}
$taskItems=@(Get-Item -LiteralPath $taskResolved)+@(Get-ChildItem -LiteralPath $taskResolved -Force -Recurse)
if(@($taskItems | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'No reparse-point deletion'}
if(@(Get-CimInstance Win32_Process | Where-Object {($_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskResolved+'\',[StringComparison]::OrdinalIgnoreCase)) -or ($_.CommandLine -and $_.CommandLine.Contains($taskResolved))}).Count){throw 'Temporary native/launcher process remains live'}
$taskBytes=($taskItems | Where-Object {-not $_.PSIsContainer} | Measure-Object Length -Sum).Sum
$taskFiles=@($taskItems | Where-Object {-not $_.PSIsContainer}).Count
Remove-Item -LiteralPath $taskResolved -Recurse -Force
if(Test-Path -LiteralPath $taskResolved){throw 'Temporary extraction still exists'}
@{removedExactPath=$taskResolved;removedFiles=$taskFiles;logicalBytesRemoved=$taskBytes;removed=$true;recoverableFromRetainedZIP=$true} | ConvertTo-Json -Compress
""".replace('TARGET',target)
 result=ps(code)
 need(result.returncode==0,'Bounded exact owned temporary cleanup: '+result.stderr)
 data=json.loads(result.stdout);save('temporary_cleanup.json',data);return data

def boot(package,label,args):
 command=[os.environ['ComSpec'],'/d','/c',str(package/'PLAY.cmd'),*args,'-str','12']
 started=time.time()
 process=subprocess.Popen(command,cwd=str(OUT),env=ENV,stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 save(label+'_process.json',dict(pid=process.pid,hostPID=os.getpid(),startedUnix=started,command=command))
 time.sleep(3)
 jobs=census();running=process.poll()is None
 save(label+'_live_census.json',jobs)
 # An observation timeout is not terminal and must never restart the boot.
 while True:
  try:stdout,stderr=process.communicate(timeout=30);break
  except subprocess.TimeoutExpired:
   save(label+'_waiting_census.json',census())
   print(label+': same finite native boot still being observed; no restart',flush=True)
 with gzip.open(OUT/(label+'_stdout.log.gz'),'wt',encoding='utf-8')as writer:writer.write(stdout)
 with gzip.open(OUT/(label+'_stderr.log.gz'),'wt',encoding='utf-8')as writer:writer.write(stderr)
 save(label+'_terminal.json',dict(exitCode=process.returncode,observedUnix=time.time()))
 exe=package/'mkport.exe'
 live=[j for j in jobs if j['ExecutablePath']and os.path.normcase(j['ExecutablePath'])==os.path.normcase(str(exe))and j['createdUnix']>=started]
 need(running and len(live)==1,'One actual live package-local native instance')
 native=live[0];cmd=native['CommandLine']or''
 need(all(s not in cmd for s in(str(ROOT),'-autoboot_script','-cheat '))and '-nocheat'in cmd and '-samples'in cmd and '-samplerate 48000'in cmd,
      'Ordinary package-local native command, enabled voices/48k/no diagnostic input/no development paths')
 later=census();save(label+'_terminal_census.json',later)
 need(not any(j==native for j in later),'Exact PID/name/creation/executable/full-command instance terminal')
 need(process.returncode==0 and 'Checked current playtest:'in stdout and not re.search(
      r'WRONG CHECKSUMS|NOT FOUND|might not run correctly|LUA ERROR|fatal error|stack traceback|access violation|Could not find XAudio2|failed to initialize',stdout+stderr,re.I),
      'Actual finite portable CMD boot terminal zero without ROM/runtime/backend errors')
 backend=dict(xaudioInitialized='Sound: XAudio2 initialized.'in stdout+stderr,
              d3dLogPresent=bool(re.search('Direct3D|Direct3d|D3D',stdout+stderr)))
 return dict(label=label,nativeIdentity=native,exitCode=process.returncode,backendLogEvidence=backend,
             stdoutSHA256=sha(OUT/(label+'_stdout.log.gz')),stderrSHA256=sha(OUT/(label+'_stderr.log.gz')))

def run():
 global TEMP
 need(not OUT.exists(),'Fresh immutable portable runtime evidence, never overwrite')
 current.expected();parent=json.loads(PARENT.read_text());meta=json.loads(PACKAGE.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and meta['passed']and meta['portableRuntimeVerificationPending'],
      'Actual full-objective parent and current requested package')
 archive_path=Path(meta['zip']);need(sha(archive_path)==meta['zipSHA256'],'Actual retained ZIP bytes')
 pins=dict(meta['sourceHashes']);pins.update({str(PACKAGE):sha(PACKAGE),str(archive_path):sha(archive_path),str(Path(__file__).resolve()):sha(__file__)})
 need(all(sha(p)==h for p,h in pins.items()),'Every actual package source/input unchanged')
 OUT.mkdir();save('source_pins.json',pins)
 TEMP=Path(tempfile.mkdtemp(prefix='mk2-portable-v5987-',suffix=' space')).resolve()
 save('temporary_identity.json',dict(exactPath=str(TEMP),hostPID=os.getpid(),createdUnix=time.time(),runtimePATH=ENV['PATH']))
 need(TEMP.parent==Path(tempfile.gettempdir()).resolve()and not str(TEMP).startswith(str(ROOT)),
      'One package verification extraction outside development workspace')
 with zipfile.ZipFile(archive_path)as archive:
  entries=archive.infolist();names=[i.filename for i in entries]
  need(len(names)==len(set(names))==meta['files']+2 and archive.testzip()is None,'Whole archive unique members/CRCs')
  top={PurePosixPath(n).parts[0]for n in names};need(len(top)==1,'One exact package root')
  for item in entries:
   rel=PurePosixPath(item.filename)
   need(not rel.is_absolute()and '..'not in rel.parts and ':'not in item.filename and '\\'not in item.filename and
        not stat.S_ISLNK(item.external_attr>>16),'Only safe archive-relative non-symlink members')
  archive.extractall(TEMP)
 package=TEMP/next(iter(top))
 need(all(sha(package/p)==h for p,h in meta['archiveMemberHashes'].items()),'Every complete extracted byte equals retained tested archive')
 positive=checker(package);save('checker_positive.json',dict(exitCode=positive.returncode,stdout=positive.stdout,stderr=positive.stderr))
 need(positive.returncode==0 and 'all sixteen voice assets'in positive.stdout,'Unmodified actual Windows checker accepts standalone extraction with Windows-only PATH')
 faults=[]
 for relative,offset in(('mkport.exe',512),('roms/mk2ks/mk2ks.mdata',0),('samples/mk2ks/sonya_wins.wav',44),('artwork/mk2ks/default.lay',5)):
  target=package/relative;original_sha=sha(target)
  with target.open('r+b')as writer:
   writer.seek(offset);original=writer.read(1);need(len(original)==1,'One actual test byte');writer.seek(offset);writer.write(bytes([original[0]^1]))
  try:denied=checker(package)
  finally:
   with target.open('r+b')as writer:writer.seek(offset);writer.write(original)
  restored=checker(package)
  fault=dict(relativePath=relative,offset=offset,actualTemporaryByteChanged=True,rejectedExitCode=denied.returncode,
             deniedOutput=denied.stdout+denied.stderr,restoredSHA256=sha(target),restoredExitCode=restored.returncode)
  faults.append(fault);save('actual_dependency_faults.json',faults)
  need(denied.returncode!=0 and relative in denied.stdout+denied.stderr and sha(target)==original_sha and restored.returncode==0,
       'Actual changed dependency denied and exactly restored before any native boot')
 audit=subprocess.run([str(package/'mkport.exe'),'mk2ks','-rompath',str(package/'roms'),'-verifyroms'],
                      cwd=str(OUT),env=ENV,capture_output=True,text=True)
 save('rom_audit.json',dict(exitCode=audit.returncode,stdout=audit.stdout,stderr=audit.stderr))
 need(audit.returncode==0 and 'is good'in audit.stdout and not re.search('NOT FOUND|WRONG CHECKSUMS|INCORRECT|BAD DUMP',audit.stdout+audit.stderr,re.I),
      'Native ROM audit resolves all packaged dependencies from external cwd')
 boots=[boot(package,'headless',['-video','none','-sound','none']),
        boot(package,'windowed_default_backends',['-window','-nomaximize','-verbose'])]
 save('native_boots.json',boots)
 need(all(sha(package/p)==h for p,h in meta['archiveMemberHashes'].items()),'All dependency-fault bytes exactly restored and every package input still intact')
 temporary_files=[dict(path=str(p.relative_to(TEMP)),bytes=p.stat().st_size,sha256=sha(p))for p in TEMP.rglob('*')if p.is_file()]
 save('temporary_inventory.json',temporary_files)
 pngs=[p for p in temporary_files if p['path'].lower().endswith('.png')]
 removal=cleanup()
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All authoritative existing source/settings/build/package bytes remain unmodified')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             parent=str(PARENT),remaining=parent['remaining'],requirementAudit=parent['requirementAudit'],
             zip=str(archive_path),zipSHA256=meta['zipSHA256'],zipBytes=meta['zipBytes'],
             standalonePackageCheckerAccepted=True,actualTemporaryDependencyFaultsRejected=len(faults),
             actualROMAuditPassed=True,actualNativeBoots=boots,developmentRuntimeToolsOnPATH=False,
             temporaryExtractionRemoved=removal,automaticTimedStopPNGs=pngs,
             priorNoRawRecordingWordingCorrection='Earlier -str runs also wrote two pinned 1692-byte automatic final PNGs; no raw RGB/audio/guest dumps were created. Prior evidence is retained, not rewritten.',
             physicalDeviceBackendInitializationObserved=boots[1]['backendLogEvidence'],
             interactiveVisualAudibleQualityAccepted=False,integratedWholeReleaseRegressionComplete=False,
             fullPortAcceptance=False,newBuilds=0,newZIPs=0,newRawRGBOrAudioRecordings=0,inputHashes=pins)

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  OUT.mkdir(exist_ok=True)
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
  # Failure evidence survives, temporary copies do not, unless a real process
  # remains live: in that case cleanup refuses and records the exact handle.
  if TEMP is not None and TEMP.exists():
   try:report['temporaryExtractionRemoved']=cleanup()
   except Exception as cleanup_error:report['cleanupError']=repr(cleanup_error)
 save('report.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','requirementAudit')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
