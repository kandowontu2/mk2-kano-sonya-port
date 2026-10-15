"""Fresh repaired candidate: original entire four-case physical UI/pixel gate.

Selection navigation, portraits, animated pose, stock cursor border/number,
teardown, native ladder and true first-match identities/name shadows. Every
displayed frame stays in RAM and is also compared to the prior accepted whole
frame digest. No older runtime acceptance transfer or complete audio claim.
"""
import datetime,hashlib,inspect,io,json,re,subprocess,time,traceback,unittest
from pathlib import Path
import current_ui_audio_ram_v5427 as original
import native_projectile_identifiers_context_v6509 as candidate
import capture_current_cmd_specials_v6261 as host
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
BASE=ROOT/'audit_v6529_repaired_selection_pixels_ram'
OUT=ROOT/'audit_v6530_repaired_selection_pixels_checked'
COMPLETED=[]

def bindings():
 source=inspect.getsource(original.capture)
 changes={
  "proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)":
  """started=time.time();proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  identity=None;host_errors=[]
  try:
   time.sleep(2);jobs=host.census();save(folder/'live_census.json',jobs)
   matches=[j for j in jobs if j['ProcessId']==proc.pid and j['ParentProcessId']==os.getpid() and j['createdUnix']>=started and j['ExecutablePath'] and Path(j['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve() and str(folder) in j['CommandLine']]
   need(len(matches)==1,'Actual exact direct native child, creation time and full isolated command')
   identity=matches[0];save(folder/'native_identity.json',identity)
  except Exception as e:host_errors.append(repr(e))""",
  "log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()":
  """save(folder/'native_terminal.json',dict(nativePID=proc.pid,exitCode=code,naturalTerminal=True,observationErrors=host_errors,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 need(not any(j['ProcessId']==proc.pid for j in host.census()),'Same actual native process terminal')
 need(identity is not None and not host_errors,'Exact identity observation, preserved terminal before qualification')
 log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()""",
 }
 for a,b in changes.items():need(source.count(a)==1,'Only full original UI candidate/transport identity adaptation '+a);source=source.replace(a,b,1)
 scope=dict(original.__dict__,__file__=__file__,current=candidate,BASE=BASE,host=host,time=time)
 exec(compile(source,__file__+'::entire_original_four_case_ui_capture','exec'),scope)
 return scope['capture']

def main():
 need(not BASE.exists() and not OUT.exists() and not host.census(),'Fresh UI gate and no conflicting native game')
 guest=candidate.expected();meta=json.loads((ROOT/candidate.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 pins=dict(meta['input_hashes']);prior=ROOT/'audit_v3736_guarded_native_ui_qualified_ram_checked/report.json'
 old=json.loads(prior.read_text());need(old['passed'],'Original whole model and effective failure gates actually qualified')
 for p in (Path(original.model.__file__),Path(original.faults.__file__),ROOT/'mk2ks_native_ui_flow_v2_probe.lua'):
  need(sha(p)==old['inputHashes'][str(p.resolve())],'Original full UI controller/state/pixel/fault source unchanged')
 for p in (Path(__file__),Path(original.__file__),Path(candidate.__file__),Path(host.__file__),
           Path(original.qualified.__file__),Path(original.model.__file__),Path(original.faults.__file__),prior,
           ROOT/'mk2ks_current_ui_audio_ram_v5427.lua',ROOT/'mk2ks_native_ui_flow_v2_probe.lua',
           ROOT/candidate.NAME/'mkport_candidate.exe',ROOT/candidate.NAME/'build-info.json',
           ROOT/candidate.NAME/'roms/mk2ks/mk2ks.mdata',ROOT/'roms/mk2ks/mk2ks.ui',
           ROOT/'samples/mk2ks/kano_select.wav',ROOT/'samples/mk2ks/sonya_select.wav',ROOT/'mk2/mk2-maincpu.bin'):
  pins[str(p.resolve())]=sha(p)
 need(sha(ROOT/'roms/mk2ks/mk2ks.ui')==original.model.UI_SHA,'Original independently modeled portrait/name asset')
 capture=bindings();ram={};backs=[]
 for fighter,side in original.faults.CASES:
  c=capture(fighter,side,True,guest,pins);key=f'{fighter}_p{side}'
  priorlog=ROOT/'audit_v5440_current_ui_audio_ram'/f'{key}_samples'/'run.log'
  priorprogress=ROOT/'audit_v5445_current_ui_visual_progress/progress.json'
  oldprogress=json.loads(priorprogress.read_text())
  need(oldprogress['passed'] and sha(priorlog)==oldprogress['newInputHashes'][str(priorlog)],'Prior accepted entire actual UI pixel trace unchanged')
  oldrows=original.records(priorlog.read_text(),'RGB_DIGEST')
  need(c['headers']==oldrows,'Every newly displayed native frame byte digest/clock/key identical to prior accepted full UI')
  for frame in (986,1288,1874):
   backing=ROOT/f'audit_v3196_ui_{key}'/'snap'/f'ui_{frame:04d}.png'
   need(sha(backing)==oldprogress['newInputHashes'][str(backing)],'Actual retained whole-frame visual backing unchanged')
   row=next(r for r in c['headers'] if int(r['frame'])==frame)
   import numpy as np
   from PIL import Image
   rgb=np.asarray(Image.open(backing).convert('RGB'));need(rgb.shape==(254,400,3),'Complete unscaled backing')
   bgra=np.empty((254,400,4),np.uint8);bgra[:,:,:3]=rgb[:,:,::-1];bgra[:,:,3]=255
   need(hashlib.sha256(bgra.tobytes()).hexdigest().upper()==row['sha256'],'Every actual candidate displayed byte matches retained visual backing')
   backs.append(dict(case=key,frame=frame,backing=str(backing),sha256=row['sha256'],everyActualRGB32ByteMatches=True))
   pins[str(backing)]=sha(backing)
  pins[str(priorlog)]=sha(priorlog);pins[str(priorprogress)]=sha(priorprogress)
  ram[key]=(c['folder'],c['log'],c['images']);COMPLETED.append(c['result'])
 original.qualified.RAM_CASES=ram
 stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(original.qualified.ActualRAMFaults))
 print(stream.getvalue(),flush=True);need(result.wasSuccessful(),'Whole original reported-failure UI state and actual-pixel faults rejected with restored positives')
 for p in BASE.rglob('*'):
  if p.is_file():
   need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'No new raw guest/raster/audio file')
   pins[str(p.resolve())]=sha(p);h=sha(p)
   need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact UI evidence compression')
 need(all(sha(p)==h for p,h in pins.items()) and not host.census(),'All actual UI inputs/evidence intact and native games terminal')
 return dict(passed=True,candidate=candidate.NAME,executableSHA256=candidate.EXE_SHA,guestSHA256=candidate.GUEST_SHA,
             cases=COMPLETED,currentBothSlotSelectionLadderFirstMatchPixelsAccepted=True,
             allDisplayedFramesIdenticalToPriorAcceptedUI=True,actualWholeFrameBackings=backs,
             actualUIQualificationMethods=result.testsRun,qualificationLog=stream.getvalue(),
             actualDisplayedFrameCallbacks=sum(c['actualDisplayedFrameCallbacks'] for c in COMPLETED),
             inputHashes=pins,newNativeBoots=4,newBuilds=0,newRawMedia=0,publicPlayableChanged=False,
             floorShadowScope='Whole byte-identical first-match frames backed by existing native PNGs; not all arena or airborne shadow acceptance.',
             fullLaddersAccepted=False,allAudioContextsAccepted=False,fullPortAcceptance=False,goalStatus='active')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable UI result')
 try:report=main()
 except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),completedCases=COMPLETED,fullPortAcceptance=False)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact UI report compression')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','completedCases','inputHashes','qualificationLog','actualWholeFrameBackings')},indent=2),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
