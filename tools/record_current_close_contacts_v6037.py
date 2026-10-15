"""Seal finite genuine contact/throw evidence and keep the whole port goal active."""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6024_current_ordinary_ground_shadow_progress/progress.json'
PROOF=ROOT/'audit_v6036_current_native_contact_relocation_checked/report.json'
OUT=ROOT/'audit_v6038_current_close_contacts_progress'

def run():
 need(not OUT.exists(),'Fresh additive full-objective close-contact checkpoint')
 current.expected();parent=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and not parent['fullPortAcceptance'],
      'Whole previous goal scope and accepted ordinary/portable evidence retained')
 need(proof['passed']and proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and
      proof['guestSHA256']==current.GUEST_SHA and proof['payloadSHA256']==current.PAYLOAD_SHA and
      proof['actualBlockedContacts']==16 and proof['actualUnblockedCloseStrikes']==4 and
      proof['actualOwnAttackerThrows']==proof['actualOwnLivingVictimThrows']==4 and
      proof['actualActorFields']==11412 and proof['nativeBodyCandidates']==23484 and proof['nativeShadowCopies']==695947 and
      len(proof['actualSemanticFaultsRejected'])==56 and proof['wholePairedGroundingBodyAndNativeShadowCleanupAccepted']and
      proof['wholeNativeCollisionKernelExactExceptSourceQualifiedTableRelocation']and proof['nativeBlockHealthAndGuardKernelsByteExact']and
      not proof['allStrikeHitMissBlockBranchesAccepted']and not proof['continuousWholeSceneRGBReplayAccepted']and
      not proof['allArenaCPURepeatedKOOverlapAccepted']and not proof['fullArtAcceptance']and not proof['fullAudioAcceptance']and not proof['fullPortAcceptance'],
      'Whole actual current contact/body/shadow matrix with exact scope limits, no universal acceptance')
 need({(r['fighter'],r['side'],r['state']['trueIdentity'])for r in proof['cases']}==
      {('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)}and
      all(len(r['state']['actualInteractions'])==7 and r['state']['nativeHealthStores']==7 and
          r['state']['stage']==0 and r['state']['actualBlockedContacts']==4 and
          r['state']['ownAttackerAndLivingVictimThrowRolesAccepted']and r['unattributedOtherObjectShadowCopies']==0 for r in proof['cases']),
      'Both own characters/both physical slots, actual living paired victims and complete shadow attribution')
 pins=dict(proof['inputHashes']);pins[str(PARENT)]=sha(PARENT);pins[str(PROOF)]=sha(PROOF);pins[str(Path(__file__).resolve())]=sha(__file__)
 need(all(sha(p)==h for p,h in parent['newInputHashes'].items()),'Previous executed current/failed/source/user/artifact bytes preserved')
 processes=[];folders=[]
 for fighter in('kano','sonya'):
  for side in(1,2):
   folder=ROOT/f'audit_v6031_contacts_{fighter}_p{side}';folders.append(folder)
   process=json.loads((folder/'process.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
   report=json.loads((ROOT/f'audit_v6032_contacts_{fighter}_p{side}_observed/report.json').read_text())
   need(terminal['nativeExit']==0 and report['passed']and report['nativeExit']==0 and
        terminal['pid']==process['pid']==process['actualWindowsIdentity']['ProcessId']and
        terminal['actualWindowsIdentity']==process['actualWindowsIdentity']==report['actualWindowsIdentity'],
        'Every native terminal preserved before postassertions and binds its actual full OS identity')
   processes.append(process)
 failure_folder=ROOT/'audit_v6027_contacts_kano_p1';folders.append(failure_folder)
 stopped=json.loads((failure_folder/'process.json').read_text());processes.append(stopped)
 failure=ROOT/'audit_v6028_contacts_kano_p1_observed/report.json'
 need(not json.loads(failure.read_text())['passed']and stopped['pid']==162832,
      'Executed native61pixel collision-stop/controller43pixel-target failure retained, never counted as contact acceptance')
 for process in processes:
  query="Get-CimInstance Win32_Process -Filter 'ProcessId="+str(process['pid'])+"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
  result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
  need(result.returncode==0,'Actual native process census before sealing completed trace')
  actual=json.loads(result.stdout)if result.stdout.strip()else None
  need(not actual or actual['Name']!='mkport_candidate.exe'or actual['ExecutablePath']!=process['command'][0]or
       actual['CommandLine']!=subprocess.list2cmdline(process['command']),
       'Exact captured process no longer live; unrelated PID reuse is not a termination/restart reason')
 sealed=[PROOF,PARENT,Path(__file__).resolve(),failure]
 for name in('mk2ks_close_contacts_v6025.lua','mk2ks_native_close_spacing_v6029.lua',
              'tools/capture_current_close_contacts_v6026.py','tools/capture_current_native_contacts_v6030.py',
              'tools/qualify_current_close_contacts_v6033.py','tools/qualify_current_contact_relocation_v6035.py'):
  sealed.append(ROOT/name)
 evidence=[ROOT/'audit_v6034_current_close_contacts_checked',ROOT/'audit_v6036_current_native_contact_relocation_checked',
           ROOT/'audit_v6028_contacts_kano_p1_observed']
 evidence.extend(ROOT/f'audit_v6032_contacts_{f}_p{s}_observed'for f in('kano','sonya')for s in(1,2))
 for folder in folders+evidence:
  sealed.extend(p for p in folder.rglob('*')if p.is_file()and p.suffix.lower()in('.json','.log','.cfg','.txt'))
 sealed=list(dict.fromkeys(p.resolve()for p in sealed))
 for p in sealed:need(p.is_relative_to(ROOT),'Only exact workspace completed text selected');pins[str(p)]=sha(p)
 images=[p for folder in folders for p in folder.rglob('*.png')]
 need(len(images)==28,'Only declared6native frames plus one compact sheet per case, no timed-stop/raw recording duplicates')
 for p in images:pins[str(p)]=sha(p)
 views=[dict(path=str(ROOT/folder/name),sha256=sha(ROOT/folder/name),scope=scope)for folder,name,scope in(
  ('audit_v6031_contacts_kano_p1','native_own_ground_throw_phase48.png','Actual own Kano attacker, flipped living stock victim and floor shadow'),
  ('audit_v6031_contacts_sonya_p1','native_stock_ground_throw_phase48.png','Actual own Sonya living victim and original Kitana throw'),
  ('audit_v6031_contacts_sonya_p2','native_own_ground_throw_phase48.png','Actual physicalP2Sonya own paired throw pose and projected shadow'),
  ('audit_v6031_contacts_kano_p2','native_stock_ground_throw_phase48.png','Actual physicalP2Kano living victim and original Kitana throw'))]
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All accepted/failed/current/package/source/settings evidence remains byte-identical')
 before=sum(allocated(p)for p in sealed);logical=sum(p.stat().st_size for p in sealed)
 for p in sealed:
  result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(result.returncode==0 and sha(p)==pins[str(p)],'Exact completed traces/source losslessly compressed, no backups/raw/recovery trees')
 after=sum(allocated(p)for p in sealed)
 audit=parent['requirementAudit']
 audit[2]['status']+=' Current DeadPool/Kitana close-contact sequences in all four own-character/physical-slot contexts qualify16actual blocked branches,4unblocked close strikes,4own throws and4stock Kitana throws of own living victims. All11412paired actor fields,23484native body candidates and695947source-bound shadow copies plus56actual semantic faults checked. Broader strike/throw victims,air throws,arenas,CPU,repeated/KO/overlap,continuous scene/art/audio scope remains open.'
 audit[2]['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],requirementAudit=audit,newInputHashes=pins,
             previousGoalTurnClassification='progress: current ordinary movement/attack/settled crouch/jump/landing plus full paired body/floor/shadow proof and completed text compression; goal remains full scope.',
             thisGoalTurnClassification='progress: actual current physical close approaches/standing and crouching blocked strikes/unblocked strike/own attacker throws/own living victim throws in both slots. Retained and stopped exact diagnostic with impossible43pixel controller target after observing61pixel native collision spacing. Corrected only physical stop distance. Four current terminal native runs clean. Whole original body/shadow/state/health/semantic-row matrix and56faults accepted; original collision-table operand relocation independently source-qualified, no code/game edits. Four genuine throw render frames inspected. Completed text sealed losslessly, no raw/build/recovery copies.',
             currentCloseContactsAndBothThrowRolesBothCharacterSlotMatrixAccepted=True,actualBlockedContacts=16,
             actualUnblockedCloseStrikes=4,actualOwnAttackerThrows=4,actualOwnLivingVictimThrows=4,
             actualActorFields=11412,nativeBodyCandidates=23484,nativeShadowCopies=695947,actualSemanticFaultsRejected=56,
             actualNativeBootsThisTurn=5,actualPassingCurrentContexts=4,controlledDiagnosticSpacingFailureStopped=True,
             stoppedDiagnosticPID=162832,stoppedDiagnosticCreationDate='2026-10-08T09:47:55.86482-04:00',
             stoppedDiagnosticOSIdentityObservedInToolOutput=True,stoppedOnlyAfterExactPIDNameCreationExecutableAndCommandGuard=True,
             capturedNativeProcessRecords=processes,exactCapturedNativeProcessesStillLive=[],
             consumedCaptureAndQualifierSessions=[27231,92339,23915,84085,19187,16088],
             boundedVisualPNGArtifacts=28,boundedVisualPNGBytes=sum(p.stat().st_size for p in images),actuallyInspectedNativeFrames=views,
             newBuilds=0,newZIPs=0,newRawGuestGFXVRAMRGBPCMOrWAVFiles=0,existingMatchedCurrentZIPUnchanged=True,
             allStrikeHitMissBlockBranchesAccepted=False,allArenaCPURepeatedKOOverlapAccepted=False,
             continuousWholeSceneRGBReplayAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
             sealedTextFiles=len(sealed),sealedTextLogicalBytes=logical,sealedAllocatedBytesBefore=before,
             sealedAllocatedBytesAfter=after,sealedAllocatedBytesReclaimed=before-after,
             next='Extend true ordinary and air throws/paired living victims, complete ordinary/special art/ground/shadow/audio phases across arenas, CPU/repeated/KO/overlap and remaining finisher/morph/secret/cinematic consumers. Retain qualified UI, actual campaign/ending/attract and matching portable5219 package. Final integrated natural-all-aspects acceptance remains unproven. No retired build/raw regeneration.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Additive full-scope progress losslessly sealed')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','requirementAudit','remaining','capturedNativeProcessRecords')},indent=2),flush=True)

if __name__=='__main__':run()
