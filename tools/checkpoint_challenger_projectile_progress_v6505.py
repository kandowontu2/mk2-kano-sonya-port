"""Seal three qualified joins, genuine Sonya failure, staged-only repair and storage."""
import datetime,gzip,json,re,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_challenger_boundary_v6489 as checked
from capture_current_continue_v6479 import census
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6506_challenger_projectile_progress'

def main():
 need(not OUT.exists() and not census(),'Fresh terminal-only checkpoint')
 current.expected();cases=[];pins={};faults=0
 for fighter,side,version,suffix in [('kano',1,6490,'checked'),('kano',2,6492,'ram'),('sonya',1,6492,'ram')]:
  folder=ROOT/f'audit_v{version}_current_challenger_{fighter}_p{side}_{suffix}'
  path=folder/'report.json';r=json.loads(path.read_text())
  need(r['passed'] and r['nativeExit']==0 and r['candidate']==current.NAME and
       r['executableSHA256']==current.EXE_SHA and r['payloadSHA256']==current.PAYLOAD_SHA,
       'Three actual correct current terminal join results')
  need(all(sha(p)==h for p,h in r['inputHashes'].items()),'Every executed passing input intact')
  capture=ROOT/f'audit_v6488_current_challenger_{fighter}_p{side}_ram' if version==6490 else folder
  with gzip.open(capture/'run.log.gz','rt')as f:t=f.read()
  good=checked.gate(t,fighter,side)
  need(json.loads(json.dumps(good))==r['actualCurrentChallenger'],'Whole original actual challenger gate reproduced with JSON integer-key normalization')
  cases.append(good);faults+=len(r['actualFaultsRejected']);pins[str(path)]=sha(path)
 repairpath=ROOT/'audit_v6504_projectile_identifiers_source_checked/report.json'
 repair=json.loads(repairpath.read_text())
 need(repair['passed'] and not repair['compiledFixAccepted'] and not repair['nativeFixAccepted'] and
      repair['expectedGuestChangedBytes']==158 and len(repair['actualPreservedFailedRuns'])==4 and
      all(sha(p)==h for p,h in repair['inputHashes'].items()),'Actual failure and qualified uncompiled repair remain distinct')
 pins[str(repairpath)]=sha(repairpath)
 files=[]
 pattern=r'(?:^|_)v(648[6-9]|649\d|650[0-4])(?:_|\.)'
 for parent in (ROOT,ROOT/'tools'):
  for p in parent.iterdir():
   if re.search(pattern,p.name):
    files.extend(q for q in p.rglob('*') if q.is_file()) if p.is_dir() else files.append(p)
 files.append(Path(__file__).resolve());files=list(dict.fromkeys(p.resolve()for p in files))
 need(files and all(str(p).startswith(str(ROOT.resolve())+'\\') for p in files),'Exact finite in-scope evidence files')
 need(not any(p.suffix.lower()in('.exe','.mdata','.zip','.bin','.png','.wav','.pcm','.rgb') for p in files),
      'No raw media, new build, ROM or ZIP copies')
 before=sum(allocated(p)for p in files)
 for p in files:
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,
               'Every exact bounded terminal file losslessly compressed')
  pins[str(p)]=h
 build=ROOT/current.NAME
 for p in (build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata',build/'build-info.json',ROOT/'PLAY_MK2_KANO_SONYA.cmd',
           ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd',ROOT/'tools/check_current_playtest_v5975.ps1'):
  pins[str(p)]=sha(p)
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,
  currentPlayableSHA256=current.EXE_SHA,currentPayloadSHA256=current.PAYLOAD_SHA,
  currentQualifiedChallengerCases=cases,actualJoinedActorFields=sum(c['joinedActorFields']for c in cases),
  completeOriginalCPUFieldsPerCase=600,completeOrdinaryPostJoinFieldsPerSlot=600,actualRecordFaultsRejected=faults,
  actualFailedSonyaP2JoinPreserved=True,actualSameFailedPhysicalChronologyRuns=4,
  actualNativeRootCause=repair['actualNativeRootCause'],stagedSource=repair['stagedSource'],
  independentlyExpectedGuestSHA256=repair['expectedGuestSHA256'],expectedGuestChangedBytes=158,
  sourceNegativeFaultsRejected=len(repair['sourceNegativeFaults']),compiledFixAccepted=False,nativeFixAccepted=False,
  retainedTestAssumptionFailure=str(ROOT/'audit_v6488_current_challenger_kano_p1_ram/report.json'),
  sourcePreflightIssue='New ancestry collector had a duplicate Python keyword before native start; repaired before executing/pinning. No native game interrupted.',
  filesCompressed=len(files),logicalBytes=sum(p.stat().st_size for p in files),allocatedBytesBefore=before,
  allocatedBytes=sum(allocated(p)for p in files),nativeGamesInterrupted=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
  publicPlayableChanged=False,allNativeJobsTerminal=True,fullPortAcceptance=False,fullGoalComplete=False,goalStatus='active',
  remainingConcreteWork=['Compile isolated packed-projectile-ID repair, verify full initialized memory and replay the exact KO/challenger failure in every slot; do not dodge the KO',
                        'Requalify projectile task/render identities, hit/block/miss/cleanup and relevant integrated gameplay after real byte changes',
                        'Remaining current single-player continue/post-ending joins; Pit/Tomb stock-victim choreography and sound-priority; cannonball donor launch cue; secret/morph/cinematic and combined regression/release'],
  previousGoalTurnClassification='progress: four paid cross-continues and whole requirement/schema audit qualified',
  thisGoalTurnClassification='progress: three current CPU/challenger joins qualified; fourth exposed genuine native lockup. Four identical failed physical chronicles plus passive native task/stack ancestry prove missed packed-ID tables; guarded158-byte source repair staged and source-only checked. No compiled/native fix acceptance.',
  inputHashes=pins)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n')
 h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact journal compression')
 print(json.dumps({k:report[k]for k in('passed','actualJoinedActorFields','actualRecordFaultsRejected','filesCompressed','allocatedBytes','newBuilds','nativeFixAccepted','fullGoalComplete')}),flush=True)

if __name__=='__main__':main()
