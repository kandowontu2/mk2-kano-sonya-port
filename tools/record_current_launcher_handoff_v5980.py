"""Current checked launcher handoff plus explicit full-requirement audit.

Keep the complete native-roster objective active. Distinguish tested native
behaviors from missing broad integration and final portable-release proof.
No copying or promoting compiled files, no old settings/public ZIP changes.
"""
import datetime,json,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5981_current_launcher_handoff_progress'
PARENT=ROOT/'audit_v5974_current_pit_queue_rng_progress/progress.json'

def run():
 need(not OUT.exists(),'Fresh immutable full-objective launcher handoff')
 current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Previous turn is progress; complete original scope retained')
 proofpath=ROOT/'audit_v5979_current_launcher_identity_checked/report.json';proof=json.loads(proofpath.read_text())
 need(proof['passed']and proof['candidate']==current.NAME and proof['actualROMAuditExitCode']==0 and
      proof['actualForwardingCMDBootExitCode']==0 and proof['actualOSExecutablePathBound']and
      proof['currentExePayloadAndAll16VoicesChecked']and proof['ordinaryNoAutobootColdStartupAccepted']and
      proof['preExistingUserSettingsUnchanged']and proof['oldPublicLauncherAndZIPUnchanged']and
      len(proof['actualSourceCheckerDenialSimulations'])==4 and not proof['actualProtectedFilesModifiedForTests']and
      not proof['interactiveVideoAndPhysicalAudioDeviceAcceptance']and not proof['fullPortAcceptance'],
      'Exact new checked launcher, real clean cold startup and explicit headless/device/full-scope limits')
 pins=dict(proof['inputHashes']);pins[str(PARENT)]=sha(PARENT);pins[str(proofpath)]=sha(proofpath)
 native=proof['actualNativeColdBootIdentity']
 need(native['ExecutablePath']==str(ROOT/current.NAME/'mkport_candidate.exe')and
      '-autoboot_script'not in native['CommandLine']and '-nocheat'in native['CommandLine']and '-samples'in native['CommandLine'],
      'Actual ordinary native command uses tested candidate and no controller assistance')
 query="Get-CimInstance Win32_Process -Filter 'ProcessId="+str(native['ProcessId'])+"' | Select-Object ProcessId,Name,ExecutablePath,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 checked=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(checked)if checked else[]
 if isinstance(jobs,dict):jobs=[jobs]
 need(not any(j==native for j in jobs),'Exact observed native PID/name/creation/executable/full command remains terminal')
 layoutpath=ROOT/'artwork/mk2ks/default.lay';layout=ET.parse(layoutpath).getroot()
 need(layout.tag=='mamelayout'and len(layout)==1 and layout[0].tag=='view'and layout[0].attrib=={'name':'Native game'}and
      len(layout[0])==1 and layout[0][0].tag=='screen'and layout[0][0].attrib=={'index':'0'}and
      len(layout[0][0])==1 and layout[0][0][0].tag=='bounds'and
      layout[0][0][0].attrib=={'x':'0','y':'0','width':'4','height':'3'},
      'Actual external artwork is native screen only; no portrait/bezel/text/selection-hint elements')
 pins[str(layoutpath)]=sha(layoutpath)
 declarations={
  'ui':'audit_v5445_current_ui_visual_progress/progress.json',
  'specials':'audit_v5322_current_subzero_all_special_body_shadow_progress/progress.json',
  'campaigns':'audit_v5698_current_campaign_four_case_matrix_checked/report.json',
  'endingPixels':'audit_v5732_current_four_case_ending_pixels_progress/progress.json',
  'endingAudio':'audit_v5747_current_four_case_ending_audio_progress/progress.json',
  'ownFinishers':'audit_v5466_current_primary_audio_qualified_progress/progress.json',
  'reptileVictims':'audit_v5507_current_reptile_overlap_qualified_progress/progress.json',
  'cageVictims':'audit_v5520_current_cage_sections_qualified_progress/progress.json',
  'barakaVictims':'audit_v5531_current_baraka_qualified_progress/progress.json'}
 evidence={}
 for key,leaf in declarations.items():
  path=ROOT/leaf;value=json.loads(path.read_text());need(value['passed'],'Retained actual current finite requirement proof '+key)
  evidence[key]=dict(path=str(path),sha256=sha(path));pins[str(path)]=sha(path)
 ui=json.loads(Path(evidence['ui']['path']).read_text());campaign=json.loads(Path(evidence['campaigns']['path']).read_text())
 need(ui['currentBothSlotSelectionLadderFirstMatchPixelsAccepted']and ui['completeObservedNativeSelectionNamesAudioAccepted']and
      campaign['actualNativeFourCaseBossOwnEndingAttractMatrixAccepted']and campaign['executableSHA256']==current.EXE_SHA and
      campaign['guestSHA256']==current.GUEST_SHA and len(campaign['cases'])==4,
      'Actual finite selection-to-fight and all four genuine current boss/own-ending/attract configurations, not old proxy evidence')
 audit=[
  dict(requirement='Dedicated top-row portraits; native blinking border/center number/animated poses; aligned background; true native selection and match IDs; own ladder icons; immediate selector teardown; native names and name shadows',
       status='proven for the current declared both-character/both-slot native selection-ladder-first-match configurations',evidence=[evidence['ui']],
       widerReleaseIntegratedRegressionComplete=False),
  dict(requirement='No persistent selection hints or portrait/pose overlays during ladder and gameplay',
       status='current native transition evidence plus actual screen-only external layout; no extra artwork elements',
       evidence=[evidence['ui'],dict(path=str(layoutpath),sha256=sha(layoutpath))]),
  dict(requirement='Complete native-feeling moves, stable gameplay, native grounding and floor shadows',
       status='eight signature moves and current declared complete human cycles/body/shadow/KO/recovery plus retained CPU/morph work have finite proof; broader arena/CPU/overlap and choreography scope remains unproven',
       evidence=[evidence['specials']],complete=False),
  dict(requirement='Natural finishers and all victim/cinematic/native audio consumers',
       status='own finishers and named stock-victim/current Pit/Tomb finite cases are qualified; wider victims, special phases, cinematic raster/audio and unexercised sound-priority/voice branches remain open',
       evidence=[evidence[k]for k in('ownFinishers','reptileVictims','cageVictims','barakaVictims')]+[dict(path=str(PARENT),sha256=sha(PARENT))],complete=False),
  dict(requirement='Actual natural campaigns, both bosses, own endings and return to attract in both slots',
       status='four genuine current character/slot configurations qualified; whole own-ending pixel/audio follow-through retained; do not transfer that evidence to all campaign combat/audio branches',
       evidence=[evidence[k]for k in('campaigns','endingPixels','endingAudio')]),
  dict(requirement='CMD file opens the tested current ROM/build without scripted play',status='new checked current playtest CMD delivered and real12second cold boot verified; older default launcher preserved',
       evidence=[dict(path=str(proofpath),sha256=sha(proofpath))],launcher=proof['userTaskLauncher'],finalRelease=False),
  dict(requirement='Matching refreshed release ZIP and dependency-aware cleanup of obsolete data',
       status='prior32.49GiB plus1.67GiB obsolete cleanup retained; current small logs compressed, but the existing portable ZIP is still v1836 and final integrated package/cleanup remains unfinished',
       refreshedCurrentZIP=False,finishedRelease=False)]
 sealed=[proofpath,ROOT/'tools/check_current_playtest_v5975.ps1',ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd',
         Path(proof['userTaskLauncher']),ROOT/'tools/verify_current_playtest_launcher_v5976.py',
         ROOT/'tools/verify_current_launcher_identity_v5978.py',Path(__file__).resolve()]
 for folder in(ROOT/'audit_v5977_current_checked_launcher',ROOT/'audit_v5979_current_launcher_identity_checked'):
  for p in folder.rglob('*'):
   if p.is_file()and p.suffix.lower()in('.json','.log','.cfg','.txt'):sealed.append(p)
 for p in sealed:pins[str(p)]=sha(p)
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All prior/current/compiled/user-dirty/old public/new launcher/evidence bytes unchanged')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before=sum(allocated(p)for p in sealed)
 for path in sealed:
  digest=sha(path);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True)
  need(done.returncode==0 and sha(path)==digest,'Exact bounded completed source/text losslessly compressed, no backup copies')
 after=sum(allocated(p)for p in sealed)
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],requirementAudit=audit,newInputHashes=pins,
             previousGoalTurnClassification='progress:5974 sealed complete actual observed native sound-priority/RNG decisions with previous full source/audio/state/fault suites',
             thisGoalTurnClassification='progress: identified stale public launcher; added a separate checked5219 launcher and user-task forwarding CMD. Actual Windows PowerShell validates matched executable/payload/all16voices, four RAM-only denial simulations reject, full native ROM audit passes and ordinary12second no-autoboot cold startup from another cwd exits0 without warnings. Actual OS executable identity resolves CMD relative invocation; user settings/old public files remain untouched. Explicit original requirement audit and screen-only external artwork verify current known scopes and remaining gaps; full goal stays active.',
             newCurrentCheckedPlaytestLauncherAdded=True,currentMatchedLauncher=proof['matchedCurrentLauncher'],userTaskLauncher=proof['userTaskLauncher'],
             currentNoWarningOrdinaryStartupAccepted=True,actualROMAuditExitCode=0,actualColdBootExitCode=0,
             existingOldPublicLauncherAndZIPUnchanged=True,preExistingUserSettingsUnchanged=True,
             noExternalPortraitOrSelectionHintElements=True,interactiveVideoAndPhysicalAudioDeviceAcceptance=False,
             refreshedReleaseZIP=False,fullPortAcceptance=False,newBuilds=0,newRawRecordings=0,newDeletedFiles=0,
             consumedLauncherTestSessions=[36496,65035],exactCapturedNativeProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
             sealedTextFiles=len(sealed),sealedAllocatedBytesBefore=before,sealedAllocatedBytesAfter=after,sealedAllocatedBytesReclaimed=before-after,
             next='Use the new current checked CMD for current-state playtesting. Continue genuine broader move/arena/CPU/repeated/KO/overlap and finisher/victim/morph/secret/cinematic integration, retain completed natural campaigns/own-ending proof, then finish combined native UI/audio regression and a matching portable current/final package with bounded temporary verification and dependency-aware cleanup. Do not redefine all-aspects success as this launcher smoke test or recreate retired raw/build history.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,'Full-objective handoff/audit losslessly sealed')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','remaining','requirementAudit')},indent=2),flush=True)

if __name__=='__main__':run()
