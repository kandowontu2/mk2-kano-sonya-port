"""Finite current earned freeze/shatter audio journal and terminal-only cleanup.

Keep full objective and prior five groups. No redundant whole parent audit,
raw media, copied builds or invented complete-port acceptance.
"""
import ctypes,datetime,gzip,json,subprocess
from pathlib import Path
import capture_current_subzero_audio_v6213 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v6220_current_subzero_audio_progress'

def read_log(path):
 opener=gzip.open if path.suffix=='.gz'else open
 with opener(path,'rt',encoding='utf-8')as reader:return reader.read()

def native_rows(path):
 opener=gzip.open if path.suffix=='.gz'else open
 with opener(path,'rt',encoding='utf-8')as reader:
  return [line.strip()for line in reader if line.startswith('MK2_EARNED_SUBZERO_')and
          not line.startswith(('MK2_EARNED_SUBZERO_GUEST','MK2_EARNED_SUBZERO_GFX','MK2_EARNED_SUBZERO_RGB'))]

def inactive_channels(text,headers):
 rows=[capture.fields(line)for line in text.splitlines()if line.startswith('MK2_TOMB_MIX_CHANNEL ')]
 need(len(rows)==14*len(headers),'Full enabled14channel callback inventory')
 for index,header in enumerate(headers):
  group=rows[index*14:(index+1)*14]
  need([r['channel']for r in group]==[str(n)for n in range(14)]and all(
   r['index']==str(index+1)and r['frame']==header['frame']and r['seconds']==header['seconds']and
   r['sample']=='4294967295'and r['loop']=='0'and r['paused']=='0'and r['writes']=='0'and r['assistance']=='none'for r in group),
   'Entire original actual inactive-source/channel/callback contract')
 return len(rows)

def allocated(path):
 high=ctypes.c_ulong(0);fn=ctypes.windll.kernel32.GetCompressedFileSizeW
 fn.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong)];fn.restype=ctypes.c_ulong
 low=fn(str(path),ctypes.byref(high));return high.value*2**32+low

def run():
 need(not OUT.exists(),'Fresh finite audio checkpoint')
 capture.current.expected();parent=json.loads(capture.PARENT.read_text())
 cases=[];pins={str(capture.PARENT):sha(capture.PARENT),str(Path(__file__)):sha(__file__)}
 folders=[];semantic_faults=0;stereo=callbacks=enabled_channels=0
 disabled={}
 for fighter in ('kano','sonya'):
  for side in (1,2):
   folder=ROOT/f'audit_v6214_current_subzero_{fighter}_p{side}_native_audio';folders.append(folder)
   path=folder/'report.json';r=json.loads(path.read_text());wpath=Path(r['waveformReport']);w=json.loads(wpath.read_text())
   need(r['passed']and r['nativeDCSWaveformAccepted']and not r['samplesEnabled']and w['passed']and
        w['differentChannelSamples']==0 and w['actualSHA256']==w['predictedSHA256']and
        len(w['effectiveActualWholeWaveformFaults'])==4 and len(r['dacFaultsRejected'])==4 and
        len(r['originalSoundROMFaultsRejected'])==8,'Whole actual native PCM, DAC, ROM and16 real byte/source faults')
   reference=ROOT/f'audit_v{6183 if fighter=="sonya"and side==1 else 6178}_current_subzero_{fighter}_p{side}_native_scene_ram/run.log'
   checked=ROOT/f'audit_v6192_current_subzero_{fighter}_p{side}_scene_checked/report.json'
   old=json.loads(checked.read_text());need(old['passed'],'Current independent whole-scene reference qualified')
   prior=native_rows(reference);new=native_rows(folder/'run.log.gz')
   need(new==prior and len(new)>2000,'Every physical native freeze/shatter/lifecycle row equals qualified current scene, not just routine entry')
   need(r['nativeTerminal']['nativeExit']==0 and not r['nativeTerminal']['hostDecodeErrors']and
        all(sha(p)==h for p,h in r['inputHashes'].items()),'Actual native terminal and all executed inputs still bound')
   pins.update(r['inputHashes']);pins[str(path)]=sha(path);pins[str(wpath)]=sha(wpath)
   pins[str(reference)]=sha(reference);pins[str(checked)]=sha(checked)
   stereo+=r['comparedStereoFrames'];callbacks+=r['dacProof']['callbacks'];semantic_faults+=16
   disabled[fighter,side]=r,w
   cases.append(dict(fighter=fighter,physicalSlot=side,samplesEnabled=False,report=str(path),
      exactNativeLifecycleRows=len(new),callbacks=r['dacProof']['callbacks'],stereoFrames=r['comparedStereoFrames']))
 for fighter,side in (('kano',1),('sonya',2)):
  folder=ROOT/f'audit_v6218_current_subzero_{fighter}_p{side}_native_audio';folders.append(folder)
  path=folder/'report.json';r=json.loads(path.read_text());wpath=Path(r['waveformReport']);w=json.loads(wpath.read_text())
  need(r['passed']and r['samplesEnabled']and r['allEnabledImportedSourcesInactive']and w['passed']and
       r['nativeTerminal']['nativeExit']==0 and all(sha(p)==h for p,h in r['inputHashes'].items()),'Actual release-option native terminal/source audio')
  text=read_log(folder/'run.log.gz');positive=inactive_channels(text,r['pcmHeaders'])
  need(positive==r['importedChannelsObserved'],'Every actual enabled channel qualified')
  for label,before,after in (('actual active imported source','sample=4294967295','sample=13'),
                           ('actual channel omitted','channel=13','channel=14')):
   need(before in text,'Actual channel counterexample exists')
   bad=text.replace(before,after,1)
   try:inactive_channels(bad,r['pcmHeaders'])
   except ValueError:pass
   else:raise ValueError('Accepted changed actual enabled channel '+label)
   need(inactive_channels(text,r['pcmHeaders'])==positive,'Full enabled-channel positive restored')
   semantic_faults+=1
  old,ow=disabled[fighter,side]
  need(w['actualSHA256']==ow['actualSHA256']and r['pcmHeaders']==old['pcmHeaders']and
       r['dacHeaders']==old['dacHeaders']and native_rows(folder/'run.log.gz')==native_rows(Path(old['waveformReport']).parent/'run.log.gz'),
       'Every enabled/disabled native PCM and source header plus physical lifecycle equal; no fitted mix')
  stereo+=r['comparedStereoFrames'];callbacks+=r['dacProof']['callbacks'];semantic_faults+=16;enabled_channels+=positive
  pins.update(r['inputHashes']);pins[str(path)]=sha(path);pins[str(wpath)]=sha(wpath)
  cases.append(dict(fighter=fighter,physicalSlot=side,samplesEnabled=True,report=str(path),
    callbacks=r['dacProof']['callbacks'],stereoFrames=r['comparedStereoFrames'],inactiveImportedChannels=positive))
 failures=[]
 for fighter,side in (('kano',1),('sonya',2)):
  folder=ROOT/f'audit_v6216_current_subzero_{fighter}_p{side}_native_audio';folders.append(folder)
  f=json.loads((folder/'failure.json').read_text());t=json.loads((folder/'native_terminal.json').read_text())
  need(not f['passed']and t['nativeExit']==0 and not t['hostDecodeErrors']and 'enabled imported sources inactive'in f['error'],
       'Both original host lifetime-assumption failures retained after genuine native terminal, not game failures/restarts')
  failures.append(dict(path=str(folder/'failure.json'),nativeTerminal=str(folder/'native_terminal.json'),
                       cause='Native completed samples retain source_len; source_num=-1 is the original inactive marker'))
  pins[str(folder/'failure.json')]=sha(folder/'failure.json');pins[str(folder/'native_terminal.json')]=sha(folder/'native_terminal.json')
 query="Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -like '*mk2port*' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual empty current native census before exact terminal-only compression')
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Playable release unchanged')
 files=[p for folder in folders for p in folder.iterdir()if p.is_file()and p.suffix=='.json']
 before={str(p):dict(sha256=sha(p),allocated=allocated(p),logical=p.stat().st_size)for p in files}
 for path in files:
  result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,text=True)
  need(result.returncode==0,'Exact terminal evidence compression')
 need(all(sha(p)==v['sha256']for p,v in before.items())and all(sha(p)==h for p,h in pins.items()),
      'Logical original sources, evidence and release unchanged after terminal compression')
 reclaimed=sum(v['allocated']-allocated(p)for p,v in before.items())
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(capture.PARENT),remaining=parent['remaining'],cases=cases,inputHashes=pins,
  nativeAudioCallbacks=callbacks,comparedStereoFrames=stereo,effectiveActualAudioFaultsRejected=semantic_faults,
  enabledImportedChannelObservations=enabled_channels,preservedHostAssumptionFailures=failures,
  sourceExactCurrentEarnedSubzeroFreezeShatterAudioAccepted=True,
  scope='Complete victim deep-task through natural next CPU; both true own characters/slots native DCS, plus KanoP1/SonyaP2 samples-enabled complete output/source inactivity',
  allFinisherAudioAccepted=False,fullPortAcceptance=False,fullGoalComplete=False,currentReleaseZIPUnchanged=True,
  newBuilds=0,newSourceDirectoryCopies=0,rawMediaFilesWritten=0,nativeGamesInterrupted=0,
  exactTerminalJSONFilesCompressed=len(files),allocatedBytesReclaimed=reclaimed,
  nextActions=['Finish the remaining finisher/cinematic audio checks without duplicating already qualified cases',
               'Broader arena/CPU interaction regression and final integrated release acceptance/cleanup'])

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();capture.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','remaining','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
