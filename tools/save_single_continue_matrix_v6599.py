"""Eight real single-player continuations; preserve full remaining port scope.

Recheck every native trace against the strongest complete gate, all executed
input pins and actual terminal identity. Preserve rejected captures, exact
historical source/doc bytes and disclosed native/inspection PNGs. No build,
ROM copy, deletion, savestate or native replay is performed by this receipt.
"""
import ctypes,datetime,gzip,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
import single_continue_faults_v6596 as current
ROOT,need,sha,gate,rows=current.ROOT,current.need,current.sha,current.gate,current.rows
OUT=ROOT/'audit_v6600_single_continue_matrix_checked'
ROUTES=[
 ('kano',1,'kano','audit_v6584_single_continue_controls_same_native_checked','audit_v6583_single_continue_controls_kano_p1_to_kano'),
 ('kano',1,'sonya','audit_v6585_single_continue_controls_kano_p1_to_sonya','audit_v6585_single_continue_controls_kano_p1_to_sonya'),
 ('kano',2,'kano','audit_v6595_single_continue_origins_strict_checked','audit_v6591_single_continue_visible_kano_p2_to_kano'),
 ('kano',2,'sonya','audit_v6597_single_continue_actual_faults_kano_p2_to_sonya','audit_v6593_single_continue_origins_kano_p2_to_sonya'),
 *[(f,s,t,f'audit_v6598_single_continue_faults_{f}_p{s}_to_{t}',f'audit_v6598_single_continue_faults_{f}_p{s}_to_{t}')for f,s,t in
   [('sonya',1,'kano'),('sonya',1,'sonya'),('sonya',2,'kano'),('sonya',2,'sonya')]],
]

def main():
 need(not OUT.exists()and not current.current.executed.prior.original.census(),'All exact native jobs naturally terminal; no repeated receipt')
 candidate=current.current.executed.prior.original.current;candidate.expected();pins={};cases=[];faults=[];identities=[]
 for fighter,side,target,proof_name,native_name in ROUTES:
  proof=ROOT/proof_name/'report.json';folder=ROOT/native_name;r=json.loads(proof.read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
  need(r['passed']and r['nativeExit']==0 and not r['fullPortAcceptance']and r['guestSHA256']==candidate.GUEST_SHA and
   r['executableSHA256']==candidate.EXE_SHA and len(r['actualGuestGFXProofs'])==2 and terminal['exitCode']==0 and
   not terminal['observationErrors']and not(folder/'stderr.log').read_text().strip(),'Complete scoped actual native continuation proof')
  need(terminal['nativePID']==r['nativeIdentity']['ProcessId']and r['nativeIdentity']['ParentProcessId']==terminal['cmdPID'],
       'Actual same Windows child/parent birth identity and native terminal')
  identities.append(terminal['nativePID'])
  for p,h in r['inputHashes'].items():need(sha(p)==h,'Every selected qualified executed input intact '+p);pins[p]=h
  with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
  good=gate(text,fighter,side,target);need(good==r['actualSinglePlayerContinue'],'Every full route rechecked by strongest native ownership/no-Game-Over gate')
  e=good['events'];end=e['recover']+180
  for slot in (1,2):
   for at in (e['reLive'],end-1):
    selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_FIELD ')and f'slot={slot} 'in l and f'frame={at} 'in l)
    try:gate(text.replace(selected+'\n','',1),fighter,side,target)
    except(ValueError,AssertionError,KeyError)as error:faults.append(dict(route=[fighter,side,target],kind=f'missing actual boundary {slot}/{at}',rejectedBy=str(error)))
    else:raise ValueError('Missing actual continuation callback admitted')
  selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_MODE ')and f'frame={e["continue"]} 'in l)
  changed=re.sub(r'\bmode=\S+','mode=11',selected,count=1)
  try:gate(text.replace(selected,changed,1),fighter,side,target)
  except(ValueError,AssertionError,KeyError)as error:faults.append(dict(route=[fighter,side,target],kind='Game Over/new-game masquerading as continue',rejectedBy=str(error)))
  else:raise ValueError('New game substituted for real continuation')
  need(gate(text,fighter,side,target)==good,'All complete positives restored')
  cases.append(dict(route=[fighter,side,target],proof=str(proof),nativeCapture=str(folder),nativePID=terminal['nativePID'],
   actual=good,wholeRGBScenes=len(r['actualFullRGBDigests']),childFaultsRejected=len(r['actualFaultsRejected'])))
  pins[str(proof.resolve())]=sha(proof)
 need(len(set(identities))==8 and len({tuple(q['route'])for q in cases})==8,'Eight different complete native games, not reused case names')
 previous=ROOT/'audit_v6566_repaired_native_handoff/report.json';old=json.loads(previous.read_text());doc_migrations=[]
 for path,h in old['inputHashes'].items():
  p=Path(path)
  if sha(p)==h:pins[path]=h;continue
  backup=ROOT/'status_history_v6599'/p.name
  need(p.name in ('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md')and sha(backup)==h,
       'Only intentional documentation alias migration; exact previous bytes preserved')
  doc_migrations.append(dict(path=path,historicalSHA256=h,currentSHA256=sha(p),historicalBytes=str(backup)))
  pins[str(backup.resolve())]=h
 files={Path(__file__).resolve(),previous.resolve()};history_migrations=[];raw=[];visual=[]
 for folder in ROOT.iterdir():
  m=re.match(r'^audit_v(\d+)_',folder.name)
  if folder.is_dir()and m and 6567<=int(m[1])<=6598:
   files.update(p.resolve()for p in folder.rglob('*')if p.is_file())
   report_path=folder/'report.json'
   if report_path.exists():
    historical=json.loads(report_path.read_text())
    for path,h in historical.get('inputHashes',{}).items():
     if sha(path)==h:continue
     copies=[folder/'executed_sources'/Path(path).name,folder/'executed_source.py']
     matches=[p for p in copies if p.exists()and sha(p)==h]
     need(len(matches)==1,'Every historical checker/controller alias change has exact executed source bytes '+path)
     history_migrations.append(dict(report=str(report_path),historicalPath=path,sha256=h,executedBytes=str(matches[0])))
 for p in ROOT.iterdir():
  m=re.search(r'_v(\d+)\.lua$',p.name)
  if m and 6567<=int(m[1])<=6599:files.add(p.resolve())
 for p in(ROOT/'tools').iterdir():
  m=re.search(r'_v(\d+)\.py$',p.name)
  if m and 6567<=int(m[1])<=6599:files.add(p.resolve())
 files.update(p.resolve()for p in(ROOT/'status_history_v6599').rglob('*')if p.is_file())
 for p in sorted(files):
  need(p.suffix.lower()not in ('.bin','.wav','.rgb','.pcm','.vram','.exe','.zip'),'No new build/payload/raw memory or audio transports in this evidence bundle')
  if p.suffix.lower()=='.png':raw.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),origin='native timed-exit snapshot or explicitly retained exact native RAM display for inspection'))
 for filename,source_name,label,frame in [
  ('audit_v6578_single_continue_control_rejection/3606_continue_select.png','audit_v6575_single_continue_ready_kano_p1_to_kano','continue_select',3606),
  ('audit_v6578_single_continue_control_rejection/3664_continue_ladder.png','audit_v6575_single_continue_ready_kano_p1_to_kano','continue_ladder',3664),
  ('audit_v6578_single_continue_control_rejection/3980_continued_match.png','audit_v6575_single_continue_ready_kano_p1_to_kano','continued_match',3980),
  *[(f'audit_v6598_single_continue_faults_sonya_p2_to_sonya/{at}_{name}.png','audit_v6598_single_continue_faults_sonya_p2_to_sonya',name,at)
    for at,name in [(3191,'continue_select'),(3339,'actual_continue_ladder'),(3470,'continued_match')]],
 ]:
  p=ROOT/filename;report=json.loads((ROOT/source_name/'report.json').read_text())
  digest=next(q for q in report['actualFullRGBDigests']if q['frame']==frame and q['label']==label)
  image=Image.open(p);need(image.size==(400,254)and hashlib.sha256(image.convert('RGBA').tobytes('raw','BGRA')).hexdigest().upper()==digest['sha256'],
       'Every inspected PNG independently reproduces the whole native406400-byte screen buffer, including opaque alpha')
  visual.append(dict(path=str(p),frame=frame,transportLabel=label,nativeFullBufferSHA256=digest['sha256'],everyActualPixelAndAlphaMatched=True))
 allocation=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 allocation.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];allocation.restype=ctypes.c_uint32;sizes=[]
 for p in sorted(files):
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact evidence compression')
  hi=ctypes.c_uint32();ctypes.set_last_error(0);lo=allocation(str(p),ctypes.byref(hi));need(lo!=0xffffffff or ctypes.get_last_error()==0,'Actual Windows allocated bytes')
  sizes.append(dict(path=str(p),logicalBytes=p.stat().st_size,allocatedBytes=(hi.value<<32)|lo));pins[str(p)]=h
 for p in (ROOT/'CURRENT_PLAYTEST_STATUS.md',ROOT/'WORKSPACE_CLEANUP_CURRENT.md'):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items())and not current.current.executed.prior.original.census()and not(ROOT/'mame-mkp/build/mingw-gcc').exists(),
      'All current accepted sources/settings/launcher/artifacts intact, native jobs terminal and compiler cache absent')
 remaining=list(old['remaining']);remaining[1]='Post-ending fresh joins and full continued-ladder visual/audio coverage; eight paid single-player real-identity/control routes passed on current repaired build.'
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',candidate=candidate.NAME,
  executableSHA256=candidate.EXE_SHA,guestSHA256=candidate.GUEST_SHA,actualCases=cases,actualNativeGames=8,actualCPUEarnedRoundLosses=16,
  actualContinuedActorFields=sum(q['actual']['continuedActorFields']for q in cases),actualFullRGBScenes=sum(q['wholeRGBScenes']for q in cases),
  actualChildFaultsRejected=sum(q['childFaultsRejected']for q in cases),additionalActualBoundaryAndGameOverFaults=faults,
  inspectedWholeNativePixelBindings=visual,visualInspectionScope='Kano P1 and Sonya P2 selection/match presentations; Sonya P2 transition fully black, actual name/floor shadows present. Early transport ladder labels may still show CSS before native fade, and do not prove a visible ladder.',
  intentionalHistoricalSourceAliasMigrations=history_migrations,intentionalDocumentationMigrations=doc_migrations,
  preservedRejectedReportsUnchanged=True,disclosedPNGFiles=raw,disclosedPNGCount=len(raw),rawGuestGFXRGBPCMWAVTransportFiles=0,
  selectedEvidenceAllocatedBytes=sum(q['allocatedBytes']for q in sizes),selectedEvidenceFileRows=sizes,inputHashes=pins,
  newBuilds=0,newROMPayloadCopies=0,newZIPs=0,regeneratedCompilerCacheAbsent=True,fullPortAcceptance=False,remaining=remaining,
  previousGoalTurnClassification='progress: current repaired playable promoted and normal-CMD projectile cases qualified.',
  thisGoalTurnClassification='progress: eight actual CPU-earned paid single-player continuations qualified with true requested identities, observed ordinary controls, complete180-field recovery tails and source-correct paired/projectile CPU damage attribution.',
  nextAction='Post-ending joins/continued-ladder presentation, remaining native arena/sound/secret/morph/cinematic integration, then combined final regression and matching release.')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n')
 h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact checkpoint compression')
 print(json.dumps({k:result[k]for k in ('passed','actualNativeGames','actualCPUEarnedRoundLosses','actualContinuedActorFields','actualFullRGBScenes','actualChildFaultsRejected','disclosedPNGCount','selectedEvidenceAllocatedBytes','newBuilds','goalStatus')}),flush=True)

if __name__=='__main__':main()
