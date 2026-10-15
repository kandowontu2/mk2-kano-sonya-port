"""Additive whole-transition body/shadow evidence; original full goal remains active."""
import ctypes,datetime,json,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as scope
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5389_current_cpu_ko_round_scene_progress/progress.json'
PROOF=ROOT/'audit_v5393_current_ko_round_body_shadow_checked/report.json'
OUT=ROOT/'audit_v5395_current_ko_round_body_shadow_progress'

def run():
 current.expected();parent=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text());case=proof['case']
 need(parent['passed']and parent['goalStatus']=='active'and parent['remaining']==scope.REMAINING,'Preserve all original unfinished groups verbatim')
 need(proof['passed']and proof['candidate']==current.NAME and proof['reusedExistingNativeCaptures']and
  proof['newNativeBoots']==proof['newBuilds']==proof['rawMediaFilesWritten']==0 and not proof['fullPortAcceptance'],
  'Actual whole-transition proof from existing physically identical native captures, no promotion')
 need(case['allModeWindow']==[3000,3340]and case['actualPhysicalBodyCallKeys']==case['actualPhysicalShadowCallKeys']==680 and
  case['actualNativeBodyCandidates']==case['actualPublishedBodyParts']==1183 and case['actualOwnedShadowComponents']==1026 and
  case['actualSourceBoundShadowCopies']==30255 and case['actualUniqueROMStreams']==94 and case['actualNoncombatCallbacks']==283 and
  case['actualCorpseIneligibleCalls']==158,'Every actual complete body/group/eligibility/projection/stream/cadence retained through noncombat and rebuilt actors')
 need(case['observedBodyAndShadowSourcesThroughActualKOAndRoundRebuildAccepted']and case['noInventedPostFields']and
  case['everyNonretirementPublishedBodyBoundToWholeSceneDMA']and case['entireShadowHardwareStreamBoundToWholeScene']and
  not case['everyPublishedBodyBoundToWholeSceneDMA']and case['actualPreRetirementQueuedButNotDrawnBodyParts']==3 and
  not case['retirementQueueDiscardMechanismSourceProven']and not case['canonicalArtisticGroundingAccepted'],
  'Keep actual three queued-but-undrawn retirement parts and unproven discard mechanism/art scope explicit')
 need(len(proof['actualFaultsRejected'])==15 and all(t['rejectedBy']for t in proof['actualFaultsRejected']),
  'Fifteen effective actual owner/body/geometry/floor/source/camera/pen/missing-body/missing-shadow/missing-DMA faults rejected')
 pins={str(p.resolve()):sha(p)for p in(PARENT,PROOF,Path(__file__),Path(scope.__file__))}
 for table in(parent['newInputHashes'],proof['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'Every retained source/evidence/native/public byte stable: '+p);pins[p]=h
 failure=ROOT/'audit_v5391_current_ko_round_body_shadow_checked/report.json'
 need(not json.loads(failure.read_text())['passed'],'Preserve actual initial too-strong queue-to-DMA assumption failure')
 files=[ROOT/'tools/verify_current_ko_round_body_shadow_v5390.py',ROOT/'tools/verify_current_ko_round_body_shadow_v5392.py',
  Path(__file__).resolve(),failure,PROOF]
 for p in files:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact in-workspace newly retained source/metadata path');pins[str(p.resolve())]=sha(p)
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True)
 need(census.returncode==0,'Actual current native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  ROOT/'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E'}
 for p,h in public.items():need(sha(p)==h,'Public launcher/playable/installed/release unchanged');pins[str(p.resolve())]=h
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);measure=kernel.GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual newly retained metadata/source allocation');allocated+=(high.value<<32)|low
 need(all(sha(p)==h for p,h in pins.items()),'All final evidence and source pins stable')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=scope.REMAINING,
  parentAdditiveJournal=str(PARENT),currentBodyShadowTransitionReport=str(PROOF),
  previousGoalTurnClassification='progress: actual continuous earned KO/rebuild/reveal/next-fight source-bound scene and all340 full displayed fields accepted; 34,544,000 pixels from one native base.',
  thisGoalTurnClassification='progress: complementary existing physical traces independently bind all actual pre-CPU bodies/post-task shadows across341 all-mode fields; all94 ROM streams,1183 body parts,1026 shadow components,30255 shadow copies;15 effective actual-record faults rejected. Actual three queued-but-undrawn retirement parts invalidate universal queue-to-DMA assumption and change the next action to source-bound discard causality.',
  fullObservedKOBodyAndShadowSourceWindowAccepted=True,allModeWindow=[3000,3340],actualNativeBodyParts=1183,
  actualNativeShadowEligibilityCalls=680,actualNativeShadowComponents=1026,actualNativeShadowCopies=30255,actualUniqueROMStreams=94,
  actualNoncombatCallbacks=283,actualZeroHPIneligibleCorpseCalls=158,
  allNonretirementBodyPartsAndEntireShadowStreamBoundToAcceptedScene=True,
  actualRetirementQueuedButUndrawnParts=case['actualUndrawnQueueParts'],retirementQueueDiscardMechanismSourceProven=False,
  sourceObservedBodyCallbackPhase='Actual same-frame pre-CPU ROUND_FIELD pointer validity; old final bodies queued before retirement, no new-body candidates until3210.',
  sourceObservedShadowCallbackPhase='Actual next-frame pre-CPU ROUND_FIELD pointer/body/floor/world-Y publication; no old shadow calls at3208, genuine rebuilt shadows at3209.',
  originalNativeBodyAndShadowKernelsUnchanged=True,noInventedPostFields=True,actualSemanticFaultsRejected=proof['actualFaultsRejected'],
  preservedExecutedProofFailure=str(failure),newNativeBoots=0,newBuilds=0,newDeletedFiles=0,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,
  newRetainedSourceAndMetadataLogicalBytes=sum(p.stat().st_size for p in files),newRetainedSourceAndMetadataAllocatedBytes=allocated,
  nativeProcessCensus=live,publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,
  canonicalArtisticFidelityAccepted=False,allKOContextsArenasBodyShadowArtAudioAccepted=False,newInputHashes=pins,
  inheritedMetricNote='Original reusable checker labels entryBodyPublicationProven/everyReadyBodyComponentSourceBound/actualContiguousActorFields are combat-checker legacy names. There is no special entry in this window;116 genuine POST_FIELD rows and283 genuine NONLIVE callbacks are preserved, not invented. Acceptance is complete actual body/shadow call coverage independently derived from both callback phases, not a universal native/artistic claim.',
  nextAction='Source-bind the actual native queue-discard mechanism at actor retirement without invented DMA, then broaden naturally reached arena/CPU/overlap and KO contexts. Preserve every original unfinished group; final combined UI/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed release ZIP remain required.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable additive native body/shadow journal')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','remaining','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
