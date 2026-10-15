"""Revalidate all four current native K/S, P1/P2 boss/own-ending/attract cases.

Aggregate the actual independently checked complete campaigns, source pins,
current initialized guest proofs and native300field ending follow-through.
Never promote this finite matrix to all combat/art/audio/port acceptance.
"""
import gzip,hashlib,json,re,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5698_current_campaign_four_case_matrix_checked'


def run():
 need(not OUT.exists(),'Fresh immutable actual four-case matrix')
 expected=current.expected();need(hashlib.sha256(expected).hexdigest().upper()==current.GUEST_SHA,'Entire current initialized guest independently reconstructed')
 declarations=[('kano',1,'audit_v5235_kano_corrected_p1_campaign_checked','audit_v5231_kano_corrected_p1_campaign',
  'actualCorrectedExecutableNaturalTowerOwnEndingAttractAccepted'),
  ('sonya',1,'audit_v5235_sonya_corrected_p1_campaign_checked','audit_v5231_sonya_corrected_p1_campaign',
  'actualCorrectedExecutableNaturalTowerOwnEndingAttractAccepted'),
  ('kano',2,'audit_v5624_current_kano_p2_campaign_checked','audit_v5622_current_kano_p2_campaign',
  'actualNaturalCurrentKanoP2BossesOwnEndingAttractAccepted'),
  ('sonya',2,'audit_v5691_verified_subzero_sonya_p2_campaign_checked','audit_v5689_verified_subzero_sonya_p2_campaign',
  'actualNaturalCurrentSonyaP2BossesOwnEndingAttractAccepted')]
 pins={};cases=[]
 for fighter,side,checked,observed,acceptance in declarations:
  path=ROOT/checked/'report.json';report=json.loads(path.read_text());folder=ROOT/observed
  native=report['case'];meta=json.loads((folder/'result.json').read_text())
  need(report['passed']and report[acceptance]and native['passed']and native['unassisted_clear_proven']and
   not native['errors']and native['player']==fighter and native['human_slot']==side and
   native['stages_reached']==list(range(13))+[14,15,16]and
   native['ending_starts']==native['ending_completions']==1 and native['actualBossRoundWins']>=4,
   'Entire actual declared native tower/both bosses/own ending case '+fighter+str(side))
  if side==1:
   priorpath=Path(report['priorWholeCampaignAnd18NativeRAMFaultProof']);prior=json.loads(priorpath.read_text())
   need(prior['passed']and len(prior['actualNativeAndRAMProofFaultsRejected'])==18 and
    report['entirePriorFaultQualifiedNativeChronologyByteIdentical']and len(report['actualCurrentRowFaultsRejected'])==2,
    'Full18fault chronology bound to actual current P1 plus actual current native faults')
  else:
   need(len(report['actualNativeAndRAMProofFaultsRejected'])==18 and report['actualAttractFollowThroughFields']==300,
    'All18actual current P2 native/guest faults and full300ordinary attract fields')
  need(meta['passed']and meta['nativeExit']==0 and meta['candidate']==current.NAME and
   meta['executableSHA256']==current.EXE_SHA and meta['guestSHA256']==current.GUEST_SHA and
   meta['fighter']==fighter and meta['physicalSlot']==side and meta['identity']==(17 if fighter=='kano'else 18)and
   meta['rawMediaGuestAudioFilesWritten']==meta['newBuilds']==0 and
   meta['qualifiedTestCandidateMetadataWarning']['metadataMatchesPayload']and
   meta['qualifiedTestCandidateMetadataWarning']['nativeStderrEmpty']and
   not meta['qualifiedTestCandidateMetadataWarning']['releaseMetadataCorrectionStillRequired'],
   'Actual correct current executable/payload/player/metadata terminal, no warning or assistance waiver')
  proof=json.loads((folder/'guest_memory_proof.json').read_text());process=json.loads((folder/'process.json').read_text())
  before=json.loads((folder/'input_hashes_before.json').read_text())
  need(meta['inputHashes']==before and proof['sha256']==current.GUEST_SHA and proof['bytes']==1048576 and
   proof['everyActualByteComparedInRAM']and proof['guestDumpFilesWritten']==0 and
   proof['executableSHA256']==current.EXE_SHA and proof['payloadSHA256']==current.PAYLOAD_SHA and
   proof['captureSourceSHA256']==sha(process['hostSource'])and
   proof['transportSourceSHA256']==sha(process['command'][-1])and
   process['command'][0]==str(ROOT/current.NAME/'mkport_candidate.exe')and '-nocheat'in process['command'],
   'Every actual initialized guest byte and exact real host/controller/executable command')
  for p,h in report['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent immutable source/proof identity across real four-case matrix')
   pins[p]=h
  ending=[];final=[];has_deadline=False
  with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as reader:
   for line in reader:
    need('hex='not in line,'Actual logs never store encoded raw guest/raster/audio buffers')
    if line.startswith('MK2_NAT_CAMPAIGN_ENDING_COMPLETED '):ending.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    elif line.startswith('MK2_NAT_CAMPAIGN_RESULT '):final.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    elif line.startswith('MK2_CAMPAIGN_HOST_DEADLINE '):has_deadline=True
  need(len(ending)==len(final)==1 and not has_deadline and int(final[0]['frame'])-int(ending[0]['frame'])==300 and
   ending[0]['human_slot']==final[0]['human_slot']==str(side)and
   ending[0]['fighter']==final[0]['fighter']==fighter and ending[0]['pictures']=='1,1'and ending[0]['texts']=='3,3',
   'One actual own two-page/two-story ending plus exactly300native attract fields, never a timed stop')
  need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),
   'No raw guest/RGB/audio files or automatic timed-stop screenshot')
  pins[str(path.resolve())]=sha(path)
  cases.append(dict(fighter=fighter,physicalSlot=side,identity=meta['identity'],proof=str(path),capture=str(folder),
   actualStages=native['stages_reached'],actualOwnRoundWins=native['native_own_round_wins'],
   actualBossRoundWins=native['actualBossRoundWins'],actualContinueLosses=native['paid_continue_losses'],
   actualSpecialEntries=native['native_owned_special_entries'],actualOwnEndingCompletions=1,
   actualAttractFollowThroughFields=300,actualNativeExit=0,fullEndingPixelsAccepted=False,fullAudioAccepted=False))
 for p in [Path(__file__),Path(current.__file__)]:pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual complete-case source/proof/evidence bytes intact now')
 return dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
  actualNativeFourCaseBossOwnEndingAttractMatrixAccepted=True,cases=cases,inputHashes=pins,
  actualInitializedGuestBytesComparedInRAMPerCase=1048576,actualAttractFollowThroughFieldsPerCase=300,
  independentWholeCampaignGatesRerunHere=False,
  scope='Revalidated exact four complete current5219 native physical campaigns: Kano/Sonya in P1/P2, true own IDs/real damage/winner calls/both bosses/own photo and story pages/300native attract fields, independently qualified original gates and actual faults. Not every combat/art/ending pixel/audio/branch or complete release acceptance.',
  fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False)


if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual four-case matrix');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
