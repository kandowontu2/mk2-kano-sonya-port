"""Add full paired airborne evidence and storage seal without shrinking the goal."""
import copy,datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6038_current_close_contacts_progress/progress.json'
PROOF=ROOT/'audit_v6066_current_air_packed_shadow_checked/report.json'
STORAGE=ROOT/'audit_v6058_current_air_trace_storage_sealed/report.json'
OUT=ROOT/'audit_v6064_current_air_roles_progress'

def run():
 need(not OUT.exists(),'Fresh additive full-scope current-air-role checkpoint')
 current.expected();parent=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text());storage=json.loads(STORAGE.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and not parent['fullPortAcceptance'],
      'Every original remaining group and accepted ordinary/selector/campaign/package scope retained')
 need(proof['passed']and proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and
      proof['guestSHA256']==current.GUEST_SHA and proof['payloadSHA256']==current.PAYLOAD_SHA and proof['actualAirCatches']==16 and
      proof['actualActorFields']==13992 and proof['exactPairedOrdinaryJumpTicks']==2432 and
      proof['actualOrdinaryGuardActivations']==26 and proof['interruptedGuardPulses']==6 and
      len(proof['actualSemanticFaultsRejected'])==65 and proof['wholePairedAirBodyGroundShadowCleanupAccepted']and
      proof['everyOriginalNativeClipBoundaryAccepted']and proof['originalPackedFlipYBorrowAccepted']and proof['originalCooperativeSameOrNextFieldHandoffAccepted']and
      not proof['stockJaxCallbackInvocationLedgerAccepted']and not proof['allGuardPulsesActivated']and
      not proof['allArenaCPURepeatedKOOverlapAccepted']and not proof['continuousWholeSceneRGBReplayAccepted']and
      not proof['fullArtAcceptance']and not proof['fullAudioAcceptance']and not proof['fullPortAcceptance'],
      'Complete16 real catches/paired every-field body-shadow/2432normal jump ticks/65 faults and exact incomplete scopes')
 need({(c['fighter'],c['side'],c['victim'],c['state']['trueIdentity'])for c in proof['cases']}==
      {(f,s,v,17 if f=='kano'else 18)for f,v in(('kano','kitana'),('kano','sonya'),('kano','jax'),('sonya','jax'))for s in(1,2)}and
      all(len(c['state']['actualAirCycles'])==2 and c['state']['stage']==0 and c['unattributedOtherObjectShadowCopies']==0 for c in proof['cases']),
      'Every real cold-selected own character/physical slot/living victim context retained, no excluded shadow objects')
 need(storage['passed']and storage['storageOnly']and storage['retainedNativeCaptureFolders']==13 and
      storage['retainedPassingNativeCaptures']==8 and storage['retainedFailedNativeDiagnostics']==5 and
      not storage['actualLiveNativeCensus']and not storage['exactCapturedProcessesStillLive']and storage['filesDeleted']==0 and
      storage['boundedNativePNGArtifacts']==68,'Actual terminal identity census and lossless bounded storage seal, no erased evidence')
 pins=dict(proof['inputHashes']);pins.update(storage['inputHashes']);pins.update(storage['protectedMatchedArtifactHashes'])
 for p in(PARENT,PROOF,STORAGE,Path(__file__).resolve()):pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in parent['newInputHashes'].items()),'All original source/user/settings/build/package/accepted/failed prior bytes preserved')
 frames=[dict(path=str(ROOT/folder/file),sha256=sha(ROOT/folder/file),scope=scope)for folder,file,scope in(
  ('audit_v6049_air_kano_p1_sonya','air_preview.png','Whole repeated true Kano catches of real Sonya, ordinary followups and recovered shadows'),
  ('audit_v6049_air_sonya_p2_jax','air_preview.png','Whole repeated stock Jax catches of trueP2Sonya; actual return punches/interruptions and native recovery'),
  ('audit_v6049_air_kano_p2_sonya','native_air_final.png','Full realP2Kano andP1Sonya final ground/stance, lifebar names and floor shadows'),
  ('audit_v6049_air_kano_p2_jax','native_air_2_phase48.png','Full actual originalJax throw of realP2Kano living body and native shadow'))]
 for r in frames:pins[r['path']]=r['sha256']
 extras=[PROOF,STORAGE,Path(__file__).resolve(),ROOT/'tools/qualify_current_air_cooperative_handoff_v6059.py',
         ROOT/'audit_v6056_current_air_native_lookup_checked/report.json',ROOT/'audit_v6060_current_air_cooperative_handoff_checked/report.json',
         ROOT/'tools/qualify_current_air_native_clip_v6061.py',ROOT/'tools/seal_current_air_traces_v6057.py',
         ROOT/'audit_v6062_current_air_native_clip_checked/report.json',ROOT/'tools/qualify_current_air_packed_shadow_v6065.py']
 for p in extras:need(p.is_relative_to(ROOT)and p.is_file(),'Only exact completed current proof text sealed');pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Current native/proof/failure/source/render/build/requested ZIP bytes stable')
 before=sum(allocated(p)for p in extras)
 for p in extras:
  result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(result.returncode==0 and sha(p)==pins[str(p)],'Exact completed proof text losslessly sealed, no raw/recovery/build copies')
 after=sum(allocated(p)for p in extras)
 audit=copy.deepcopy(parent['requirementAudit'])
 audit[2]['status']+=' Current DeadPool airborne matrix adds16real catches across Kano/Kitana, Kano/Sonya, Kano/Jax and livingSonya/Jax in both slots. All13992paired actor fields, every native body candidate, projected source shadow row,2432exact fractional pre/post normal jump ticks and65semantic faults qualify native recovery/grounding/shadows.26actual ordinary guards;6stockJax guards interrupted by real24damage and not credited. StockJax callback invocation ledger, broader arenas/CPU/KO/overlap, complete art/audio and final integrated acceptance remain open.'
 audit[2]['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],requirementAudit=audit,newInputHashes=pins,
  previousGoalTurnClassification='no progress: acknowledgement alone; revalidated saved native terminals and existing build before this work.',
  thisGoalTurnClassification='progress: independently qualified whole real airborne role/repeated recovery/paired ordinary followup/body/clip/FIFO/source-projected-shadow matrix. Retained failed mutation-scope, duplicate-native-lookup, cooperative-field-order, exact-zero-native-clipping and scalar packed-shadow flip-borrow assumptions. Only diagnostic assertions changed; no game edits. Actual rendered frames inspected. Completed native traces/source/proof losslessly compressed and matching current build/payload/ZIP rehashed.',
  currentAirRolesBothPhysicalSlotsAccepted=True,actualAirCatches=16,actualActorFields=proof['actualActorFields'],
  nativeBodyCandidates=proof['nativeBodyCandidates'],nativeShadowCopies=proof['nativeShadowCopies'],exactNormalJumpTicks=2432,
  actualSemanticFaultsRejected=65,actualOrdinaryGuardActivations=26,interruptedStockGuardPulsesNotCredited=6,
  stockJaxCallbackInvocationLedgerAccepted=False,allGuardPulsesActivated=False,
  actualNewNativeBootsThisTurn=0,retainedNativeBootsInNewlyQualifiedMatrix=13,
  boundedNativePNGArtifacts=68,boundedNativePNGBytes=storage['boundedNativePNGBytes'],actuallyInspectedNativeFrames=frames,
  exactCapturedNativeProcessesStillLive=[],nativeProcessTerminalStorageSeal=str(STORAGE),
  consumedPriorNativeCaptureSessions=[82666,36014,26397,21028,63188,60900,74932,31210,84424,23265,26435,87569,22549],
  consumedThisTurnToolSessions=[83913,68810,98018,63095,23235,56494,30142,49975],
  sealedTextFiles=storage['sealedTextFiles']+len(extras),sealedTextLogicalBytes=storage['sealedTextLogicalBytes']+sum(p.stat().st_size for p in extras),
  allocatedTraceBytesReclaimed=storage['allocatedBytesReclaimed'],allocatedExtraProofBytesReclaimed=before-after,
  totalAllocatedBytesReclaimed=storage['allocatedBytesReclaimed']+before-after,filesDeleted=0,
  newBuilds=0,newZIPs=0,newRawGuestGFXVRAMRGBPCMOrWAVFiles=0,existingMatchedCurrentZIPUnchanged=True,
  allArenaCPURepeatedKOOverlapAccepted=False,continuousWholeSceneRGBReplayAccepted=False,
  fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
  next='Complete source-bound air-throw trajectory/callback invocation coverage and settled post-hit controls. Extend remaining true move/victim/arena/CPU/repeated/KO/overlap/art/audio and finisher/morph/secret/cinematic consumers. Preserve qualified selector/ladder/name shadows and actual campaign/own-ending/attract plus matching portable5219 package. Final integrated natural-all-aspects acceptance remains unproven; no retired raw/build regeneration.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Whole full-objective additive checkpoint losslessly retained')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','requirementAudit','remaining')},indent=2),flush=True)

if __name__=='__main__':run()
