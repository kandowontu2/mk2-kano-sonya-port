"""Four clean native continued UI contexts; full port goal remains active.

Immutable additive receipts preserve failed diagnostics, exact source versions,
whole native inspection-image bindings and intentional documentation migrations.
No game replay, build, payload copy, ZIP or deletion is made by this receipt.
"""
import ctypes,datetime,gzip,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
import continue_viewport_contract_v6610 as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
OUT=ROOT/'audit_v6621_continue_viewport_matrix_checked'

def main():
 need(not OUT.exists()and not contract.original.prior.current.executed.prior.original.census(),
      'Fresh matrix receipt; all native jobs actually terminal')
 contract.context.expected();cases=[];pins={};files={Path(__file__).resolve()};pids=[]
 for fighter,side in [('kano',1),('kano',2),('sonya',1),('sonya',2)]:
  target=fighter;proof=ROOT/f'audit_v6615_continue_viewport_checked_{fighter}_p{side}_to_{target}/report.json'
  extra=ROOT/f'audit_v6618_continue_extra_pixels_{fighter}_p{side}_to_{target}/report.json'
  good=json.loads(proof.read_text());pixels=json.loads(extra.read_text());folder=Path(good['nativeCapture'])
  terminal=json.loads((folder/'native_terminal.json').read_text())
  need(good['passed']and pixels['passed']and not good['fullPortAcceptance']and not pixels['fullPortAcceptance']and
       terminal['exitCode']==0 and not terminal['observationErrors']and
       terminal['nativePID']==good['nativeIdentity']['ProcessId']and
       terminal['cmdPID']==good['nativeIdentity']['ParentProcessId'],'Distinct naturally completed actual native child/parent')
  for report in (good,pixels):
   for p,h in report['inputHashes'].items():need(sha(p)==h,'Every actual qualified source/asset/proof intact '+p);pins[p]=h
  with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
  state=contract.gate(text,fighter,side,target)
  need(state==good['actualSinglePlayerContinue']and state['actualOtherPlayerStartupKeyReleased']and
       len(good['actualFaultsRejected'])==18,'Whole genuine natural loss/paid continuation/UI state rechecked')
  render=good['actualUIPixels'];need(render['blink_colors']>=2 and render['native_name_shadow_checks']>=4 and
       pixels['selectedPlayerLadderIcon']['fullSourceRasterMatches']>=3 and
       render['continuedViewport']['offscreenRasterRenderingNotClaimed'],'Actual native pixel proofs, not offscreen raster claims')
  pids.append(terminal['nativePID']);cases.append(dict(fighter=fighter,side=side,target=target,proof=str(proof),
   additionalPixelProof=str(extra),nativeCapture=str(folder),nativePID=terminal['nativePID'],actual=state,
   actualUIPixels=render,ownLadderIcon=pixels['selectedPlayerLadderIcon'],wholeRGBCallbacks=len(good['actualFullRGBDigests']),
   faultsRejected=len(good['actualFaultsRejected'])+len(pixels['additionalActualImageFaultsRejected'])))
 need(len(set(pids))==4,'Four different actual clean native games, not renamed shared captures')
 previous=ROOT/'audit_v6600_single_continue_matrix_checked/report.json';history=json.loads(previous.read_text());migrations=[]
 for p,h in history['inputHashes'].items():
  if sha(p)==h:continue
  path=Path(p);backup=ROOT/'status_history_v6608'/path.name
  need(path.name in ('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md')and sha(backup)==h,
       'Only intentional documentation changes; exact old pinned bytes preserved')
  migrations.append(dict(path=p,historicalSHA256=h,currentSHA256=sha(p),historicalBytes=str(backup)))
  pins[str(backup.resolve())]=h
 bindings=[];oldfolder=ROOT/'audit_v6604_continue_presentation_sonya_p2_to_sonya'
 old=json.loads((oldfolder/'report.json').read_text())
 need(old['passed']is False and old['error']=="ValueError('Final continued highlight is the requested native character')",
      'Original transport-mismatch capture rejection unchanged')
 for frame in (3900,3960,4116,4242):
  p=oldfolder/f'inspect_{frame}.png';image=Image.open(p);need(image.size==(400,254),'Exact native inspection dimensions')
  raw=image.convert('RGBA').tobytes('raw','BGRA');digest=hashlib.sha256(raw).hexdigest().upper()
  original=next(q for q in old['actualFullRGBDigests']if q['frame']==frame and q['label']==f'ui_{frame:04d}.png')
  need(len(raw)==406400 and digest==original['sha256'],'Every native inspected RGB+opaque-alpha byte bound to actual display')
  bindings.append(dict(path=str(p),bytes=p.stat().st_size,wholeNativeBufferSHA256=digest,everyPixelAndAlphaMatched=True))
 for p in ROOT.iterdir():
  m=re.search(r'_v(\d+)\.lua$',p.name)
  if m and 6601<=int(m[1])<=6620:files.add(p.resolve())
  a=re.match(r'^audit_v(\d+)_',p.name)
  if p.is_dir()and a and 6601<=int(a[1])<=6619:files.update(q.resolve()for q in p.rglob('*')if q.is_file())
 for p in(ROOT/'tools').iterdir():
  m=re.search(r'_v(\d+)\.py$',p.name)
  if m and 6601<=int(m[1])<=6620:files.add(p.resolve())
 files.update(p.resolve()for p in(ROOT/'status_history_v6608').rglob('*')if p.is_file())
 files.update((ROOT/name).resolve()for name in ('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 allocation=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 allocation.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];allocation.restype=ctypes.c_uint32;sizes=[];media=[]
 for p in sorted(files):
  need(p.suffix.lower()not in ('.exe','.zip','.bin','.rgb','.wav','.pcm','.vram'),
       'No new executable/payload/raw transport copies in selected evidence')
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,
       'Lossless selected source/proof/inspection compression')
  hi=ctypes.c_uint32();ctypes.set_last_error(0);lo=allocation(str(p),ctypes.byref(hi))
  need(lo!=0xffffffff or ctypes.get_last_error()==0,'Actual Windows allocated-file size')
  sizes.append(dict(path=str(p),logicalBytes=p.stat().st_size,allocatedBytes=lo+(hi.value<<32)));pins[str(p)]=h
  if p.suffix.lower()=='.png':media.append(str(p))
 need(len(media)==4 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and all(sha(p)==h for p,h in pins.items()),
      'Exactly4 disclosed native inspection PNGs, source pins intact and compiler cache absent')
 remaining=list(history['remaining']);remaining[1]=('Released-input cross-character continues and post-continue ordinary controls; broader continued-ladder audio/stages and post-ending fresh joins. Four same-character, both-slot, stage-zero released-input continued UI/viewport cases now pass.')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',fullPortAcceptance=False,
  candidate=contract.context.NAME,executableSHA256=contract.context.EXE_SHA,guestSHA256=contract.context.GUEST_SHA,
  actualCases=cases,actualCleanNativeGames=4,actualCPUEarnedRoundLosses=8,actualContinuedActorFields=sum(q['actual']['continuedActorFields']for q in cases),
  actualWholeNativeDisplayCallbacks=sum(q['wholeRGBCallbacks']for q in cases),actualFaultsRejected=sum(q['faultsRejected']for q in cases),
  inspectedNativePixelBindings=bindings,disclosedPNGFiles=media,selectedEvidenceAllocatedBytes=sum(q['allocatedBytes']for q in sizes),selectedEvidenceFiles=sizes,
  intentionalDocumentationMigrations=migrations,preservedEarlierFailuresAndExactSources=True,
  historicalP2InputIsolationNotAccepted=True,offscreenRasterRenderingNotClaimed=True,
  newBuilds=0,newROMPayloadCopies=0,newZIPs=0,compilerCacheAbsent=True,deletedFiles=0,inputHashes=pins,remaining=remaining,
  previousGoalTurnClassification='progress: startup input leak identified, corrected native continue captured; last conversational acknowledgement alone added no work.',
  thisGoalTurnClassification='progress: four released-input genuine paid continues complete original native UI/viewport/owned-match/name-shadow and actual regression checks; old failures preserved.',
  nextAction='Released-input cross-character/ordinary controls, continued audio and post-ending fresh joins; remaining arena/voice/cannonball startup/secret/morph/cinematic work; combined final acceptance and matching release ZIP.')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact matrix report compression')
 print(json.dumps({k:result[k]for k in ('passed','actualCleanNativeGames','actualCPUEarnedRoundLosses','actualContinuedActorFields','actualWholeNativeDisplayCallbacks','actualFaultsRejected','selectedEvidenceAllocatedBytes','goalStatus')}),flush=True)

if __name__=='__main__':main()
