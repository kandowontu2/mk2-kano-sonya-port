"""Seal real current ordinary-control body/floor/shadow evidence; full goal active."""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6024_current_ordinary_ground_shadow_progress'
PARENT=ROOT/'audit_v5992_current_portable_release_progress/progress.json'
PROOF=ROOT/'audit_v6022_current_ordinary_kitana_raw_checked/report.json'

def run():
 need(not OUT.exists(),'Fresh additive ordinary native-roster checkpoint')
 current.expected();parent=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
      parent['portableCurrentPlaytestVerified']and not parent['fullPortAcceptance'],'Previous goal turn is concrete portable-release progress; original whole goal remains')
 need(proof['passed']and proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and
      proof['guestSHA256']==current.GUEST_SHA and proof['payloadSHA256']==current.PAYLOAD_SHA and
      proof['actualCurrentBothCharactersBothPhysicalSlotsOrdinaryGroundingAndNativeShadowsAccepted']and
      proof['allThreeSettledCrouchAttacksActuallyActivated']and proof['all24SourceDefinedWalkVelocityPositionUpdatesExact']and
      proof['originalKitana11x40RawKnockbackShadowRowsAccepted']and proof['originalSignedUnconditionalScannerUsedWithoutPointerFitting']and
      proof['actualActorFields']==12328 and proof['nativeBodyCandidates']==24246 and proof['nativeShadowCopies']==741730 and
      len(proof['actualSemanticFaultsRejected'])==48 and not proof['genericImportedRawSpriteAcceptance']and
      not proof['actualBlockedStrikeContactAccepted']and not proof['allOrdinaryStrikeHitMissBlockBranchesAccepted']and
      not proof['allArenaCPUOrKOOverlapAccepted']and not proof['continuousWholeRGBSceneReplayAccepted']and
      not proof['fullArtAcceptance']and not proof['fullAudioAcceptance']and not proof['fullPortAcceptance'],
      'Whole current real ordinary state/health/body/shadow/fault matrix and all remaining scope limits explicit')
 need({(r['fighter'],r['side'],r['state']['trueIdentity'])for r in proof['cases']}==
      {('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)}and
      all(r['state']['stage']==0 and r['state']['actualPhases']==25 and r['state']['nativeHealthStores']==2 and
          r['state']['allThreePreviouslyUnactivatedCrouchAttacksNowActivated']and
          len(r['state']['actualOrdinaryActionPhases'])==12 and len(r['state']['actualJumps'])==3 and
          r['unattributedOtherObjectShadowCopies']==0 for r in proof['cases']),
      'Exactly both characters/both physical slots; all normal actions and genuine jump/landing paths actually observed')
 pins=dict(proof['inputHashes']);pins[str(PARENT)]=sha(PARENT);pins[str(PROOF)]=sha(PROOF);pins[str(Path(__file__).resolve())]=sha(__file__)
 need(all(sha(p)==h for p,h in parent['newInputHashes'].items()),'All previous portable/current/old source/evidence bytes unchanged')
 native=[];folders=[]
 for name in('audit_v5995_basic_kano_p1','audit_v5999_basic_kano_p1'):
  folders.append(ROOT/name)
 for fighter in('kano','sonya'):
  for side in(1,2):folders.extend((ROOT/f'audit_v6003_basic_{fighter}_p{side}',ROOT/f'audit_v6012_basic_{fighter}_p{side}'))
 for folder in folders:
  process=json.loads((folder/'process.json').read_text());native.append(process)
  query="Get-CimInstance Win32_Process -Filter 'ProcessId="+str(process['pid'])+"' | Select-Object ProcessId,Name,ExecutablePath,CommandLine,CreationDate | ConvertTo-Json -Compress"
  result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
  need(result.returncode==0,'Actual terminal process census before sealing completed trace')
  jobs=json.loads(result.stdout)if result.stdout.strip()else[]
  if isinstance(jobs,dict):jobs=[jobs]
  need(not any(j['Name']=='mkport_candidate.exe'and str(folder)in(j['CommandLine']or'')for j in jobs),
       'No captured native job remains live; unrelated/reused PID is not a restart/termination reason')
 sealed=[Path(__file__).resolve(),PROOF]
 source_names=('mk2ks_basic_ground_shadow_v5993.lua','mk2ks_basic_ground_binding_v5997.lua','mk2ks_basic_ground_separator_v6001.lua',
               'mk2ks_basic_settled_crouch_v6007.lua','tools/capture_current_basic_ground_v5994.py','tools/capture_current_basic_binding_v5998.py',
               'tools/capture_current_basic_separator_v6002.py','tools/capture_current_settled_basic_v6008.py','tools/capture_current_basic_previews_v6011.py',
               'tools/qualify_current_basic_ground_v6014.py','tools/qualify_current_basic_walk_timing_v6016.py',
               'tools/qualify_current_basic_contact_scope_v6018.py','tools/qualify_current_basic_kitana_raw_v6021.py')
 sealed.extend(ROOT/name for name in source_names)
 evidence_folders=[ROOT/'audit_v5996_basic_kano_p1_observed',ROOT/'audit_v6000_basic_kano_p1_observed',
                   ROOT/'audit_v6010_settled_basic_kano_p1_observed',ROOT/'audit_v6015_current_ordinary_ground_shadow_checked',
                   ROOT/'audit_v6017_current_ordinary_walk_timing_checked',ROOT/'audit_v6019_current_ordinary_contact_scope_checked']
 for fighter in('kano','sonya'):
  for side in(1,2):evidence_folders.extend((ROOT/f'audit_v6004_basic_{fighter}_p{side}_observed',ROOT/f'audit_v6013_basic_{fighter}_p{side}_observed'))
 for folder in folders+evidence_folders:
  sealed.extend(p for p in folder.rglob('*')if p.is_file()and p.suffix.lower()in('.json','.log','.cfg','.txt'))
 sealed=list(dict.fromkeys(p.resolve()for p in sealed))
 for p in sealed:
  need(p.is_relative_to(ROOT),'Only exact in-workspace completed source/text files selected');pins[str(p)]=sha(p)
 images=[p for folder in folders for p in folder.rglob('*.png')]
 need(len(images)==24 and sum(p.stat().st_size for p in images)==4050146,'Only declared24bounded native visual proofs, no timed-stop/raw capture duplicates')
 for p in images:pins[str(p)]=sha(p)
 visual=[dict(path=str(ROOT/folder/name),sha256=sha(ROOT/folder/name),scope=scope)for folder,name,scope in(
  ('audit_v6012_basic_kano_p1','native_idle_phase12.png','Actual own Kano stance/HUD and native floor contact, no selection overlay'),
  ('audit_v6012_basic_kano_p1','native_forward_jump_phase12.png','Actual Kano airborne pose and original projected shadow'),
  ('audit_v6012_basic_sonya_p1','native_idle_phase12.png','Actual own Sonya stance/HUD and native floor contact, no selection overlay'),
  ('audit_v6012_basic_sonya_p1','native_forward_jump_phase12.png','Actual Sonya airborne pose and original projected shadow'),
  ('audit_v6012_basic_kano_p2','native_crouch_phase12.png','Actual physicalP2Kano crouch and stock opponent'),
  ('audit_v6012_basic_sonya_p2','native_standing_block_phase12.png','Actual physicalP2Sonya guard and stock opponent'))]
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'Every accepted/failed/current/compiled/user-dirty/source/artifact byte preserved')
 before=sum(allocated(p)for p in sealed);logical=sum(p.stat().st_size for p in sealed)
 for p in sealed:
  result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(result.returncode==0 and sha(p)==pins[str(p)],'Exact completed trace/source losslessly compressed, no copy/backups')
 after=sum(allocated(p)for p in sealed)
 audit=parent['requirementAudit']
 audit[2]['status']+=' Current whole25ordinary-control phase sequences in both character/slot DeadPool/Kitana configurations now qualify complete native state/health/body/floor/shadow geometry, including actual settled crouch punches/kicks/uppercuts, all24signed walking updates, jump/landing and exact stock knockback shadow rows. Broader hit/miss/block/arena/CPU/KO/overlap and artistic/audio/full-scene coverage still open.'
 audit[2]['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],requirementAudit=audit,newInputHashes=pins,
             previousGoalTurnClassification='progress: matching portable current playtest ZIP/checker/ROM audit/two startup modes verified and sole extraction removed.',
             thisGoalTurnClassification='progress: created current real ordinary-controls/body/shadow tests. Retained two frame0 binding failures, four queued-exit admission failures and a pre-native preview-graft failure. Settled crouch timing activates all three previously ignored attacks. Four current true-ID/physical-slot25phase runs exit0 with complete clean recovery. Whole original body/shadow kernels qualify12328actor fields/24246body candidates/741730native shadow copies; exact original signed scanner adds real stock Kitana11x40knockback without fitting.48real mutations reject; complete native health and24walking-cycle ledgers exact. Six real rendered native scenes inspected. Finished source/text losslessly compressed; executable/payload/package/user settings unchanged. Full goal stays active.',
             currentOrdinaryGroundBodyShadowBothCharacterSlotMatrixAccepted=True,settledCrouchAttacksActuallyActivated=True,
             actualActorFields=12328,nativeBodyCandidates=24246,nativeShadowCopies=741730,actualSemanticFaultsRejected=48,
             actualCurrentOrdinaryContexts=4,actualNativeBootsThisTurn=10,actualPreNativeGraftFailures=1,
             initialCrouchAttackAttemptsNotCountedAsActivation=True,allOrdinaryStrikeHitMissBlockBranchesAccepted=False,
             actualBlockedStrikeContactAccepted=False,continuousWholeRGBSceneReplayAccepted=False,
             allArenaCPUOrKOOverlapAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
             existingMatchedCurrentZIPUnchanged=True,newBuilds=0,newZIPs=0,newRawGuestVRAMRGBPCMOrWAVFiles=0,
             boundedVisualPNGArtifacts=24,boundedVisualPNGBytes=4050146,actuallyInspectedNativeFrames=visual,
             capturedNativeProcessRecords=native,exactCapturedNativeProcessesStillLive=[],
             consumedCaptureAndQualifierSessions=[63397,43284,87392,87611,58986,74247,9547,80787,27315,1077,75965,74039],
             sealedTextFiles=len(sealed),sealedTextLogicalBytes=logical,sealedAllocatedBytesBefore=before,
             sealedAllocatedBytesAfter=after,sealedAllocatedBytesReclaimed=before-after,
             next='Exercise actual close-range hit/miss/block branches (re-approach after native knockback, not injected positions) and ordinary/air throws with full paired victims/body/floor/shadow cleanup. Extend complete ordinary/special move phases across arenas/CPU/repeated/KO/overlap and remaining finisher/victim/morph/secret/cinematic consumers. Retain completed genuine campaign/ending/attract and portable5219 proof. Final combined scene/art/audio release acceptance remains open; do not claim all-aspects completion or regenerate retired builds/raw recordings.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,'Additive full-objective progress sealed')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','requirementAudit','remaining','capturedNativeProcessRecords')},indent=2),flush=True)

if __name__=='__main__':run()
