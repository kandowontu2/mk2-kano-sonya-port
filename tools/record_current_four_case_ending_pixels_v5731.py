"""Four actual current K/S P1/P2 native ending pipelines, bounded acceptance.

Retain complete capture/terminal/art/hardware proofs and original goal scope.
No new native boot, build, ROM/media copy, release promotion or broad all-game
claim. Independent stock transition choreography and ending audio remain open.
"""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5732_current_four_case_ending_pixels_progress'


def run():
 need(not OUT.exists(),'Fresh immutable full ending checkpoint receipt')
 current.expected()
 parentpath=ROOT/'audit_v5730_current_p2_ending_live_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 matrixpath=ROOT/'audit_v5698_current_campaign_four_case_matrix_checked/report.json'
 matrix=json.loads(matrixpath.read_text())
 need(matrix['passed']and matrix['actualNativeFourCaseBossOwnEndingAttractMatrixAccepted'],
  'Actual four unassisted current native campaign clears already qualified')
 reports=[matrix];paths=[parentpath,matrixpath];cases=[]
 for side in (1,2):
  versions=(5281,5283,5285)if side==1 else(5722,5724,5728)
  for fighter,identity in [('kano',17),('sonya',18)]:
   names=('ending_terminal_pixels','original_ending_pages','complete_native_pixels_hardware')
   proofpaths=[ROOT/f'audit_v{v}_{fighter}_current_p{side}_{name}_checked/report.json'
    for v,name in zip(versions,names)]
   need(all(p.exists()for p in proofpaths),'Actual complete terminal/art/hardware proof required before checkpoint')
   pixel,art,hardware=[json.loads(p.read_text())for p in proofpaths]
   need(all(r['passed']and r['physicalSlot']==side for r in(pixel,art,hardware))and
    pixel[f'actualCurrentP{side}EndingAttractNativeRendererVideoAccepted']and
    pixel['actualColdNativeCampaignExactlyUnchanged']and pixel['candidate']==current.NAME and
    pixel['executableSHA256']==current.EXE_SHA and pixel['actualAttractRendererFields']==300 and
    pixel['oneInitialBaseOnly']and pixel['comparisonTargetsNeverReanchor']and
    pixel['everyActualRetainedPerFieldRAMRecordRequired']and
    len(pixel['actualNativePixelFaultsRejected'])==2,
    'Actual full source-timed current native RAM pixel terminal, same cold true-ID campaign, all300attract fields')
   need(art['candidate']==current.NAME and art['identity']==identity and
    art[f'actualCurrentP{side}EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted']and
    art['actualFullRGBPixelsCompared']==406400 and len(art['pages'])==4 and
    len(art['actualRAMRecordFaultsRejected'])==8 and
    all(p['physicalSlot']==side and p['identity']==identity and p['exactWholeCurrentRGBPixels']==101600
     for p in art['pages']),
    'All four actual early/late own photo/font/black-shadow/common-background pages and actual counterexamples')
   need(hardware['identity']==identity and hardware['nativeExit']==0 and
    hardware['fullEndingVRAMRGBPixelsAccepted']and hardware['metadataNeverSubstitutedForPixels']and
    hardware['everyRawVRAMWordAndRGBPixelAccepted']and hardware['everyQualifiedOriginalEndingPageRetained']and
    not hardware['dummyVRAMUsed']and hardware['actualAttractFields']==300 and
    hardware['completeActualMetadataFields']==pixel['exactConsecutiveNativeVideoFields']and
    hardware['completedRendererClockRecords']==pixel['actualSourceTimedRasterClocks']and
    hardware['actualNativeDisplayIOStores']==pixel['actualDisplayIOStores']and
    len(hardware['actualMetadataFaultsRejected'])==27 and len(hardware['actualTerminalFaultsRejected'])==8,
    'Independent whole native IO/opcode/source-clock/operation/terminal ledger, all27metadata+8terminal faults')
   need(not hardware['independentStockTransitionChoreographyAccepted']and not hardware['allEndingContextsAccepted']and
    not hardware['fullPortAcceptance']and not pixel['completeArtAudioCinematicContextAcceptance'],
    'Finite actual pipeline acceptance does not replace stock choreography/audio/all-context/full-port proof')
   folder=Path(pixel['capture']);meta=json.loads((folder/'result.json').read_text())
   need(meta['passed']and meta['nativeExit']==0 and not meta['endingModelErrors']and
    meta['executableSHA256']==current.EXE_SHA and meta['guestSHA256']==current.GUEST_SHA and
    meta['rawMediaGuestAudioFilesWritten']==0,'Actual completed current native full RAM capture')
   need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),
    'No raw guest/video/audio or timed-stop PNG in these current captures')
   paths.extend(proofpaths);reports.extend([pixel,art,hardware])
   cases.append(dict(fighter=fighter,physicalSlot=side,identity=identity,proofs=list(map(str,proofpaths)),
    completeNativeVideoFields=pixel['exactConsecutiveNativeVideoFields'],actualAttractFields=300,
    exactRGBPixels=pixel['exactRGBPixels'],exactVRAMWords=pixel['exactVRAMWords'],
    completedNativeRasterClocks=pixel['actualSourceTimedRasterClocks'],nativeDisplayIOStores=pixel['actualDisplayIOStores'],
    nativeTimedOperations=hardware['actualOriginalTimedOperations'],earlyLateOwnPages=4,
    actualVRAMRGBFaultsRejected=2,actualRAMPageFaultsRejected=8,
    actualHardwareMetadataFaultsRejected=27,actualTerminalFaultsRejected=8))
 pins={}
 for report in reports:
  for p,h in report['inputHashes'].items():
   need(sha(p)==h and(p not in pins or pins[p]==h),'Every current/prior/source/failure/native/render proof byte unchanged')
   pins[p]=h
 livecases=parent['liveNativeEndingCases'];pids=sorted({c[key]['ProcessId']for c in livecases for key in('nativeProcess','hostProcess')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for c in livecases:
  for key in ('nativeProcess','hostProcess'):
   old=c[key]
   need(not any(j['ProcessId']==old['ProcessId']and j['Name']==old['Name']and
    abs(j['createdUnix']-old['createdUnix'])<0.01 and j['CommandLine']==old['CommandLine']for j in jobs),
    'Both exact native ending captures and hosts terminal; reused PIDs not mistaken for the old job')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public playtest remains unchanged, not full-goal release')
 sources=[ROOT/'tools/verify_current_p2_native_ending_hardware_v5725.py',
  ROOT/'tools/verify_current_p2_native_ending_hardware_bound_v5727.py',Path(__file__)]
 for p in [*paths,*sources,*public]:pins[str(p.resolve())]=sha(p)
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],
  previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: both actual current P2 full cold native campaigns completed;3040Kano+3043Sonya entire ending/all300attract VRAM/RGB fields exact, original photos/story-font/black-shadows/common-background independently accepted. Whole native IO/opcode/clock/terminal ledger and27+8actual faults each accepted. All four actual current P1/P2 complete ending pipelines revalidated, original scope remains.',
  actualCurrentFourCaseNaturalEndingPipelineAccepted=True,cases=cases,
  newP2ConsecutiveVideoFields=sum(c['completeNativeVideoFields']for c in cases if c['physicalSlot']==2),
  allFourConsecutiveVideoFields=sum(c['completeNativeVideoFields']for c in cases),
  actualCampaignMatrixAcceptanceRetained=True,exactNativeEndingCaptureProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedCaptureToolSessions=[78988,4801],consumedGateToolSessions=[28176,42378,49168,79461,73262,15993],
  fullEndingPixelsAcceptedForTheseFourNativeCases=True,completeEndingArtAudioAccepted=False,
  independentStockTransitionChoreographyAccepted=False,allEndingContextsAccepted=False,fullPortAcceptance=False,
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,deletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  sourceInputs=pins,
  next='Both ending capture jobs are terminal and all six new P2 gates passed; do not restart them. Continue complete ending audio/stock transition choreography and wider native Pit/Tomb, move/arena/KO, victim/finisher/morph/secret/cinematic coverage. Final combined regression, dependency-aware obsolete-folder cleanup and matching refreshed release remain required. Preserve all original five work groups; four finite actual ending pipelines are not whole-port completion.')
 need(all(sha(p)==h for p,h in pins.items()),'Every actual input stable before sealing checkpoint')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 # Compress immutable JSON/source only; logs are already streaming gzip.
 sealed=[path,*sources]
 for c in cases:
  if c['physicalSlot']==2:
   folder=ROOT/f"audit_v5720_{c['fighter']}_current_p2_ending_pixels"
   sealed.extend(p for p in folder.rglob('*')if p.is_file()and p.suffix in('.json','.cfg','.log'))
   sealed.extend(Path(p)for p in c['proofs'])
 before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded sealed capture/source/result compression')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Lossless immutable text compression')
 need(all(sha(p)==h for p,h in before.items()),'All full evidence/source bytes preserved; no guessed savings')
 print(json.dumps({k:v for k,v in report.items()if k not in('sourceInputs','remaining')},indent=2),flush=True)


if __name__=='__main__':run()
