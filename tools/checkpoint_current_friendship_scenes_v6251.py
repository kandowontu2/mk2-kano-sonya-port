"""Add current complete Friendship scenes and lossless terminal-only storage."""
import ctypes,datetime,json,subprocess
from pathlib import Path
import qualify_current_friendship_scenes_v6249 as qualified
ROOT,need,sha=qualified.ROOT,qualified.need,qualified.sha
OUT=ROOT/'audit_v6252_current_friendship_scene_progress'
PARENT=qualified.capture.PARENT

def allocated(path):
 high=ctypes.c_ulong(0)
 fn=ctypes.windll.kernel32.GetCompressedFileSizeW
 fn.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong)];fn.restype=ctypes.c_ulong
 low=fn(str(path),ctypes.byref(high))
 need(low!=0xffffffff,'Actual file allocation readable')
 return(high.value<<32)|low

def run():
 need(not OUT.exists(),'Fresh current full-scope journal')
 qualified.capture.current.expected()
 reportpath=qualified.OUT/'report.json';report=json.loads(reportpath.read_text())
 parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Full original scope kept')
 need(report['passed']and report['currentBothSlotFullFriendshipRasterPaletteShadowsFadeCleanupAccepted']and
      report['wholeVisibleFields']==6400 and report['exactRGBPixels']==650240000 and report['earnedKOs']==8 and
      report['actualPixelFaultsRejected']==12 and report['actualNativeFaultsRejected']==8,
      'Actual current both-character/both-slot full scenes and effective faults')
 need({(c['fighter'],c['physicalSlot'])for c in report['cases']}=={(f,s)for f in('kano','sonya')for s in(1,2)},
      'Complete native context matrix')
 pins=report['inputHashes'].copy()
 need(all(sha(p)==h for p,h in pins.items()),'Every actual evidence input byte still exact')
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',
   "Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe'\" | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"],
   capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual native census empty before terminal file compression')
 files=[]
 for case in report['cases']:
  folder=Path(case['folder']).resolve();need(folder.parent==ROOT and folder.name.startswith(('audit_v6246_','audit_v6248_')),
       'Exact bounded terminal capture folder')
  terminal=json.loads((folder/'native_terminal.json').read_text())
  need(terminal['nativeExit']==0 and terminal['naturalTerminal'],'Confirmed native terminal leaf only')
  files.extend(p.resolve()for p in folder.glob('*.json'))
 files.append(reportpath.resolve())
 storage=[]
 for p in files:
  h=sha(p);before=allocated(p)
  result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,text=True)
  need(result.returncode==0 and sha(p)==h,'Lossless exact terminal JSON compression')
  storage.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,allocatedBefore=before,allocatedAfter=allocated(p)))
 for p in(PARENT,reportpath,Path(__file__).resolve(),ROOT/'tools/capture_current_friendship_scene_v6247.py'):
  pins[str(p)]=sha(p)
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Current portable playtest unchanged')
 pins[str(archive)]=sha(archive)
 need(all(sha(p)==h for p,h in pins.items()),'All current proof inputs exact after lossless compression')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],inputHashes=pins,currentFriendshipSceneReport=str(reportpath),
      previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: all4 actual current5219 physical Friendship scenes native-terminal;6400whole RGB fields source-exact through shadows/fade/cleanup; real pixel and ID/cleanup faults rejected; completed initial host-parser failure qualified without native rerun; exact terminal JSONs losslessly compressed',
      currentBothSlotFullFriendshipRasterPaletteShadowsFadeCleanupAccepted=True,
      actualCurrentFriendshipContexts=4,wholeVisibleFields=6400,exactRGBPixels=650240000,
      collisionEarnedKOs=8,physicalNativeRows=report['physicalNativeRows'],actualNativeAndPixelFaultsRejected=20,
      nativeBoots=4,nativeGamesInterrupted=0,nativeGamesRerunForHostError=0,
      initialHostParserFailurePreserved=True,originalInitialHostInvocationPassed=False,
      completeFriendshipAudioWaveformAccepted=False,allFriendshipVictimMirrorCPUContextsAccepted=False,
      exactTerminalJSONFilesCompressed=len(storage),compression=storage,
      allocatedBytesReclaimed=sum(s['allocatedBefore']-s['allocatedAfter']for s in storage),
      newBuilds=0,newSourceDirectoryCopies=0,newRawMedia=0,currentReleaseZIPUnchanged=True,
      fullPortAcceptance=False,fullGoalComplete=False,
      nextActions=['Qualify current complete Friendship effect/voice waveform where only older-build proof exists',
                   'Audit remaining actual feature/branch gaps and complete combined normal-launcher acceptance; reuse proven campaigns/endings'])
 OUT.mkdir();qualified.capture.save(OUT/'progress.json',result)
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','compression')},indent=2),flush=True)

if __name__=='__main__':run()
