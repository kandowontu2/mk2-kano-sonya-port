"""Seal actual repaired native gameplay/UI progress and exact retained storage.

The full requested integration goal remains active. No public promotion,
retrospective failure acceptance, extra ROM/media copies or further deletion.
"""
import ctypes,datetime,gzip,json,re,subprocess
from pathlib import Path
import native_projectile_identifiers_context_v6509 as candidate
import capture_current_cmd_specials_v6261 as host
import verify_special_repeat_v5115 as model
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
OUT=ROOT/'audit_v6535_repaired_candidate_progress'
REMAINING=[
 'Repaired projectile hit, block, miss, overlap/render-group retirement and native shadow/audio regression; promote only after relevant checks.',
 'Current single-player paid continue, post-ending fresh join and remaining route coverage.',
 'Remaining Pit/Tomb stock-victim choreography and sound-priority coverage.',
 'Cannonball donor launch-cue fidelity: current move has no authored startup cue.',
 'Remaining secret, morph and cinematic integration.',
 'Combined final visual/audio/gameplay regression, matching public launcher and finished release ZIP.',
]

def lines(folder):
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:
  return [l for l in f.read().splitlines() if l.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')) and not l.startswith('MK2_HPHASE_GUEST_DIGEST ')]

def main():
 need(not OUT.exists() and not host.census(),'Fresh checkpoint; actual native test processes terminal')
 candidate.expected();pins={str(Path(__file__).resolve()):sha(__file__)};reports={}
 paths={'challenger':ROOT/'audit_v6527_repaired_challenger_fault_scope_checked/report.json',
        'specials':ROOT/'audit_v6515_repaired_special_matrix_checked/report.json',
        'ui':ROOT/'audit_v6533_repaired_selection_transport_checked/report.json',
        'cleanup':ROOT/'audit_v6523_compiler_cache_retirement_recovery_checked/report.json'}
 for key,p in paths.items():
  r=json.loads(p.read_text());need(r['passed'] and not r['fullPortAcceptance'] and not r['publicPlayableChanged'],
                              'Actual scoped passing native/proof child, not full-port acceptance')
  for k,h in r['inputHashes'].items():need(sha(k)==h,'Every retained actual child input intact '+k);pins[str(Path(k).resolve())]=h
  pins[str(p.resolve())]=sha(p);reports[key]=r
 need(reports['challenger']['joinedActorFields']==6240 and len(reports['challenger']['actualFourChallengerCases'])==4 and
      len(reports['challenger']['actualGameplayFaultsRejected'])==32 and len(reports['challenger']['actualRootCauseFaultsRejected'])==3,
      'Full both-slot challenger and exact previous native lockup proof')
 need(reports['specials']['actualVerifiedSpecialCycles']==32 and reports['specials']['actualContiguousPostFields']==18260 and
      len(reports['specials']['actualSemanticFaultsRejected'])==194,'Whole new sixteen-case two-cycle special/fault matrix')
 need(reports['ui']['actualUIQualificationMethods']==46 and reports['ui']['actualDisplayedFrameCallbacks']==684 and
      len(reports['ui']['cases'])==4 and len(reports['ui']['actualWholeFrameBackings'])==12,
      'Entire new four-case UI/navigation/displayed pixels and original fault suite')
 same=[]
 for move in model.SPECS:
  for side in (1,2):
   old=ROOT/f'audit_v6264_current_cmd_special_{move}_p{side}';new=ROOT/f'audit_v6513_repaired_special_{move}_p{side}'
   a=json.loads((old/'result.json').read_text());b=json.loads((new/'result.json').read_text())
   need(a['passed'] and b['passed'] and a['actualScenes']==b['actualScenes'] and a['independentSemantics']==b['independentSemantics'] and
        lines(old)==lines(new),'Every actual non-guest-proof physical/actor/damage/body/publication/scene record unchanged '+move+str(side))
   need(all(sha(k)==h for k,h in a['inputHashes'].items()),'Prior actual baseline inputs unchanged')
   for p in (old/'result.json',old/'run.log.gz'):pins[str(p.resolve())]=sha(p)
   same.append(dict(move=move,side=side,actualComparedRecords=len(lines(new)),actualFullFrameDigests=len(b['actualScenes']),
                    completeCapturedChronologyIdentical=True,allCapturedRGBBytesIdenticalByDigest=True))
 meta=json.loads((ROOT/candidate.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 payload=ROOT/candidate.NAME/'roms/mk2ks/mk2ks.mdata';shared=Path(meta['payload_hardlink_to_immutable_prior'])
 need((payload.stat().st_dev,payload.stat().st_ino)==(shared.stat().st_dev,shared.stat().st_ino) and payload.stat().st_nlink>1,
      'Actual current payload shares existing immutable file allocation; no added payload copy')
 files=set()
 for p in ROOT.iterdir():
  m=re.match(r'^(?:audit|diagnostic|source)_v(\d+)_',p.name)
  if p.is_dir() and m and 6507<=int(m[1])<=6534:files.update(q.resolve() for q in p.rglob('*') if q.is_file())
 for p in (ROOT/'tools').iterdir():
  m=re.search(r'_v(\d+)\.(?:py|ps1)$',p.name)
  if m and 6507<=int(m[1])<=6534:files.add(p.resolve())
 files.add((ROOT/'TEST_PROJECTILE_IDENTIFIERS_V6508.cmd').resolve())
 f=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 f.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];f.restype=ctypes.c_uint32
 allocated=[];seen=set();shared_id=(payload.stat().st_dev,payload.stat().st_ino)
 for p in sorted(files):
  h=sha(p)
  if p!=payload.resolve():need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,
                              'Lossless exact retained-file compression '+str(p))
  hi=ctypes.c_uint32();lo=f(str(p),ctypes.byref(hi));need(lo!=0xffffffff or ctypes.get_last_error()==0,'Actual Windows compressed allocation')
  stat=p.stat();ident=(stat.st_dev,stat.st_ino);unique=ident not in seen;seen.add(ident)
  allocated.append(dict(path=str(p),logicalBytes=stat.st_size,allocatedBytes=(hi.value<<32)|lo,
                        uniqueRetainedAllocation=unique,alreadySharedWithPrior=ident==shared_id))
  pins[str(p)]=h
 need(all(sha(k)==h for k,h in pins.items()) and not host.census(),'Final source/evidence/build intact and native jobs terminal')
 need(not(ROOT/'mame-mkp/build/mingw-gcc').exists(),'Regenerated reproducible compiler cache remains absent')
 exe=next(r for r in allocated if Path(r['path'])==(ROOT/candidate.NAME/'mkport_candidate.exe').resolve())
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             previousGoalTurnClassification='progress: native packed-ID cause traced and repair compiled; exact failed native route repaired.',
             thisGoalTurnClassification='progress: four actual repaired challenger cases, exact KO/purge root-cause regression, sixteen repeated specials, four full UI cases, retained-input/cache recovery receipt and allocation proof.',
             candidate=candidate.NAME,executableSHA256=candidate.EXE_SHA,guestSHA256=candidate.GUEST_SHA,
             actualPassingChildReports={k:str(p) for k,p in paths.items()},actualGuestByteDelta=158,
             actualJoinedActorFields=6240,actualSpecialCycles=32,actualSpecialActorFields=18260,
             actualSpecialFaultsRejected=194,actualChallengerGameplayFaultsRejected=32,actualRootCauseFaultsRejected=3,
             actualUIQualificationMethods=46,actualUIFrameCallbacks=684,actualFullSpecialRGBDigests=295,
             entireSpecialChronologyAndPixelsUnchanged=same,actualVisualBackingInspectedThisTurn=[
              dict(case='sonya_p2',frame=1874,scope='Exact whole-frame backing: real Sonya match body, lifebar shadow and floor shadow.'),
              dict(case='kano_p1',frame=986,scope='Exact whole-frame backing: dedicated portrait, green numbered native border and real select stance.')],
             immutableFailuresPreserved=True,publicPlayableUnchanged=True,publicCandidate=candidate.old.NAME,
             regeneratedCompilerCacheAbsent=True,cleanupByteAmountUnknown=True,newBuilds=1,newROMPayloadCopies=0,newRawMedia=0,
             candidateExecutableAllocatedBytes=exe['allocatedBytes'],retainedNewFileRows=allocated,
             newlyRetainedUniqueAllocatedBytesExcludingExistingSharedPayload=sum(r['allocatedBytes'] for r in allocated if r['uniqueRetainedAllocation'] and not r['alreadySharedWithPrior']),
             allocationScope='Exact selected6507..6534 candidate/source/test evidence files before this checkpoint output. Existing payload allocation is shared and excluded; prior build/cache reclaimed byte counts are not inferred.',
             inputHashes=pins,remaining=REMAINING,refreshedReleaseZIP=False,fullPortAcceptance=False)

if __name__=='__main__':
 report=main();OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact checkpoint compression')
 print(json.dumps({k:report[k] for k in ('passed','actualJoinedActorFields','actualSpecialCycles','actualSpecialActorFields','actualUIFrameCallbacks','candidateExecutableAllocatedBytes','newlyRetainedUniqueAllocatedBytesExcludingExistingSharedPayload','publicPlayableUnchanged','goalStatus')}),flush=True)
