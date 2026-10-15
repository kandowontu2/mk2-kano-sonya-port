"""Requalify all current complete scenes including terminal6245 parser failure.

No runtime rerun. Actual full-frame comparison counts/digests are bound to the
immutable executed source and decoded source-qualified PNGs. Retain the failed
host invocation as failed, not as a successful original capture invocation.
"""
import copy,datetime,gzip,inspect,json,re
from pathlib import Path
import capture_current_friendship_scene_v6245 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v6250_current_friendship_scenes_checked'

class TextPath:
 def __init__(self,text):self.text=text
 def read_text(self,encoding):return self.text

def reject(rows,fighter,side,tag,key,value):
 changed=copy.deepcopy(rows);index=next(i for i,(t,r)in enumerate(changed)if t==tag)
 need(changed[index][1][key]!=value,'Actual native fault is nonvacuous')
 changed[index][1][key]=value
 try:capture.original.audio.audio.scene.check(changed,fighter,side)
 except ValueError as error:return dict(kind=tag+'.'+key,rejectedBy=str(error))
 raise ValueError('Actual native selected-ID/cleanup corruption accepted')

def check(fighter,side):
 leaf='audit_v6246'if(fighter,side)==('kano',1)else'audit_v6248'
 folder=ROOT/f'{leaf}_current_{fighter}_friendship_scene_p{side}'
 terminal=json.loads((folder/'native_terminal.json').read_text())
 need(terminal['nativeExit']==0 and terminal['naturalTerminal']and not terminal['hostDecodeErrors'],
      'Exact actual native natural terminal0 before host parsing')
 wi=terminal['actualWindowsIdentity']
 need(wi['Name']=='mkport_candidate.exe'and Path(wi['ExecutablePath']).resolve()==(ROOT/capture.current.NAME/'mkport_candidate.exe').resolve(),
      'Actual current native executable identity and creation captured')
 pins=json.loads((folder/'inputs.json').read_text())
 need(all(sha(p)==h for p,h in pins.items()),'Every executed compiled/controller/reference input unchanged')
 frames=json.loads((folder/'visible_frames.json').read_text());mismatches=json.loads((folder/'mismatches.json').read_text())
 reference,window,refs,reference_pins=capture.original.reference(fighter,side)
 need(len(frames)==1600 and not mismatches,'Whole native window, no masked differing frames')
 with gzip.open(folder/'run.log.gz','rt')as log:text=log.read()
 logged=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_CURRENT_FRIEND_CHECKED ')]
 finish=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_FSTREAM_RESULT ')]
 need(len(logged)==1600 and len(finish)==1 and int(finish[0]['screenframes'])==1600 and
      int(finish[0]['window'])==window and int(finish[0]['frame'])==window+1601,
      'Every complete visible comparison followed by original requested stop phase')
 need(not re.search(r'LUA ERROR|Lua error|stack traceback|fatal error|access violation',text+(folder/'stderr.log').read_text(),re.I),
      'Native/observer stop is clean')
 pixels=None
 for i,(row,ref,record)in enumerate(zip(frames,refs,logged)):
  path=Path(ref['path']);need(sha(path)==ref['wanted']==row['referencePNG_SHA256'],'Exact independently source-qualified PNG')
  actual=capture.np.asarray(capture.Image.open(path).convert('RGB'))
  need(actual.shape==(254,400,3),'Complete original scene dimensions')
  digest=capture.digest(actual.tobytes())
  need(row['frame']==window+i+1 and row['exactPixels']==400*254 and
       row['currentRGB_SHA256']==row['referenceRGB_SHA256']==digest and
       all(str(v)==record[k]for k,v in row.items()if k!='referencePNG'),
       'Every current full RGB comparison/count/digest equals independently decoded reference')
  if pixels is None:pixels=capture.original.pixel_faults(actual.copy(),actual)
 parser=capture.original.audio.audio.scene.previous.parse
 rows=parser(TextPath(text));old_rows=[(tag,row)for tag,row in parser(reference/'run.log')if not tag.startswith('SHADOW_')]
 need(rows==old_rows,'Every actual original native physical input/health/pose/owner/audio-cue/winner/cleanup row exact')
 control=capture.original.audio.audio.scene.check(rows,fighter,side)
 chronology=capture.original.audio.audio.native.runtime(rows,fighter,side,'positive')
 faults=[reject(rows,fighter,side,'SELECT_ID','actual','1'),reject(rows,fighter,side,'RESULT','cleanup','false')]
 need(capture.original.audio.audio.scene.check(rows,fighter,side)==control,'Entire unmodified native positive restored')
 # Executed source compared actual raw RGB with np.count_nonzero and recorded
 # both raw digests before the separate parser adaptation could fail.
 source=(ROOT/'tools/capture_current_friendship_scene_v6245.py').read_text()
 need('differing=int(np.count_nonzero(np.any(actual!=expected,axis=2)))'in source and
      'currentRGB_SHA256=digest(actual.tobytes())'in source and
      source.index("save(folder/'native_terminal.json'")<source.index('parser=original.audio.audio.scene.previous.parse'),
      'Actual complete byte comparison and terminal persist before failed parser')
 if leaf=='audit_v6246':
  failure=json.loads((folder/'failure.json').read_text())
  need(not failure['passed']and 'One exact original parser RAM input adaptation'in failure['error'],
       'Original post-terminal host failure retained honestly')
 else:
  report=json.loads((folder/'report.json').read_text());need(report['passed']and report['candidate']==capture.current.NAME,
       'Other fresh corrected-parser capture invocation succeeded')
 for p in folder.rglob('*'):
  if p.is_file():pins[str(p)]=sha(p)
 pins.update(reference_pins)
 return dict(fighter=fighter,physicalSlot=side,folder=str(folder),nativeScene=control,nativeCueChronology=chronology,
      wholeVisibleFields=1600,exactRGBPixels=1600*400*254,actualPixelFaults=pixels,actualNativeFaults=faults,
      physicalNativeRows=len(rows),naturalNativeExitCode=0,originalHostInvocationPassed=leaf!='audit_v6246'),pins

def run():
 need(not OUT.exists(),'Fresh complete matrix qualification')
 capture.current.expected();cases=[];pins={}
 for f in('kano','sonya'):
  for s in(1,2):
   case,actual=check(f,s);cases.append(case)
   for p,h in actual.items():need(p not in pins or pins[p]==h,'Consistent actual matrix inputs');pins[p]=h
 for p in(Path(__file__).resolve(),ROOT/'tools/capture_current_friendship_scene_v6247.py',capture.PARENT):pins[str(p)]=sha(p)
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=capture.current.NAME,
      cases=cases,inputHashes=pins,wholeVisibleFields=6400,exactRGBPixels=6400*400*254,
      physicalNativeRows=sum(c['physicalNativeRows']for c in cases),earnedKOs=8,
      actualPixelFaultsRejected=12,actualNativeFaultsRejected=8,
      currentBothSlotFullFriendshipRasterPaletteShadowsFadeCleanupAccepted=True,
      preservedInitialPostTerminalParserFailure=True,nativeGamesRerunForHostError=0,
      completeFriendshipAudioWaveformAccepted=False,allFriendshipVictimMirrorCPUContextsAccepted=False,
      newBuilds=0,newSourceCopies=0,rawMediaWritten=0,fullPortAcceptance=False)
 OUT.mkdir();capture.save(OUT/'report.json',result)
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','cases')},indent=2),flush=True)

if __name__=='__main__':run()
