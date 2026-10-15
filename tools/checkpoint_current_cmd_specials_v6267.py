"""Record current normal-CMD gameplay integration without broadening acceptance."""
import datetime,json,subprocess
from pathlib import Path
import verify_current_cmd_special_matrix_v6265 as matrix
import checkpoint_current_friendship_scenes_v6251 as storage
ROOT,need,sha=matrix.ROOT,matrix.need,matrix.sha
OUT=ROOT/'audit_v6268_current_cmd_gameplay_progress'
PARENT=ROOT/'audit_v6259_current_friendship_audio_progress/progress.json'

def main():
 need(not OUT.exists(),'Fresh immutable integration journal')
 need(not matrix.capture.prior.census(),'Actual native census empty before final journal')
 parent=json.loads(PARENT.read_text());r=json.loads((matrix.OUT/'report.json').read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Entire original unfinished scope preserved')
 need(r['passed']and r['canonicalUserCMDAllEightMovesBothSlotsIntegrated']and r['actualCanonicalCMDColdBoots']==16 and r['actualVerifiedSpecialCycles']==32 and len(r['actualSemanticFaultsRejected'])==194,'Full actual canonical-CMD move/slot/cycle gate and real faults')
 pins=dict(r['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All executed sources, production launchers and native evidence unchanged')
 files=[]
 for move in matrix.original.SPECS:
  for side in(1,2):
   folder=ROOT/f'audit_v6264_current_cmd_special_{move}_p{side}'
   terminal=json.loads((folder/'native_terminal.json').read_text())
   need(terminal['exitCode']==0 and terminal['naturalTerminal']and not terminal['observationErrors'],'Each actual native terminal completed')
   files.extend(p.resolve()for p in folder.rglob('*')if p.is_file())
 files.extend((matrix.OUT/'report.json',ROOT/'audit_v6262_current_cmd_special_knife_p1/result.json'))
 allocations=[]
 for p in files:
  need(p.parent==matrix.OUT or p.is_relative_to(ROOT/'audit_v6262_current_cmd_special_knife_p1')or any(p.is_relative_to(ROOT/f'audit_v6264_current_cmd_special_{m}_p{s}')for m in matrix.original.SPECS for s in(1,2)),'Exact bounded finished test artifact')
  h=sha(p);result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
  need(result.returncode==0 and sha(p)==h,'Terminal-only lossless artifact compression')
  allocations.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,allocatedBytes=storage.allocated(p)))
  pins[str(p)]=h
 for p in(PARENT,matrix.OUT/'report.json',Path(__file__).resolve(),Path(matrix.__file__),Path(storage.__file__)):
  pins[str(p)]=sha(p)
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Existing matched portable playtest unchanged')
 pins[str(archive)]=sha(archive)
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],inputHashes=pins,
  previousGoalTurnClassification='no progress: conversational acknowledgement only; revalidated current files and took the next actual integration test',
  thisGoalTurnClassification='progress: all sixteen actual canonical user-CMD boots completed; every own special repeats twice in both slots with true selected actors and ordinary movement/jump/punch recovery; original 194 actual semantic faults rejected',
  candidate=matrix.current.NAME,canonicalUserCMDAllEightMovesBothSlotsIntegrated=True,actualCanonicalCMDBoots=16,actualSpecialCycles=32,actualContiguousOwnedPostFields=r['actualContiguousPostFields'],actualNativeRGBFields=r['actualFullRGBFields'],actualSourceBoundBodyParts=r['sourceBoundBodyCandidates'],actualSemanticFaultsRejected=194,
  priorUnstartedHostQuotingFailurePreserved=True,nativeGamesInterrupted=0,nativeGamesRerunForObservationTimeout=0,newBuilds=0,newZIPs=0,newRawMedia=0,terminalArtifacts=allocations,logicalArtifactBytes=sum(a['logicalBytes']for a in allocations),allocatedArtifactBytes=sum(a['allocatedBytes']for a in allocations),
  priorUIShadowsFriendshipCampaignEndingEvidenceRetained=True,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,
  nextActions=['Audit finite remaining native stage-finisher and character-state branches against current evidence','Complete combined visual/audio release acceptance and matching handoff; no duplicate builds or raw recordings'])
 need(not matrix.capture.prior.census()and all(sha(p)==h for p,h in pins.items()),'Actual terminal and immutable evidence confirmed')
 OUT.mkdir();p=OUT/'progress.json';p.write_text(json.dumps(report,indent=2)+'\n')
 h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless final compact journal')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','terminalArtifacts')},indent=2),flush=True)

if __name__=='__main__':main()
