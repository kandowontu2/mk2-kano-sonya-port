"""Additive current Subzero continuous native scene evidence and terminal cleanup.

All original requirement groups remain. This finite four-slot DeadPool proof
does not establish normal-health freeze, full audio or all arenas/consumers.
Compress only exact hash-bound completed logs/JSON, including failed transport;
never delete a source, build, review, release or observation.
"""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
import checkpoint_current_kitana_scene_v6121 as storage
ROOT,need,sha,current=storage.ROOT,storage.need,storage.sha,storage.current
PARENT=ROOT/'audit_v6169_current_subzero_shatter_progress/progress.json'
OUT=ROOT/'audit_v6194_current_subzero_native_scene_progress'

def run():
 previous=json.loads(PARENT.read_text());need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,'Whole original port objective preserved')
 pins={str(p.resolve()):sha(p)for p in(PARENT,Path(__file__),Path(storage.__file__))}
 cases=[];targets=[]
 for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
  path=ROOT/f'audit_v6192_current_subzero_{fighter}_p{side}_scene_checked/report.json'
  proof=json.loads(path.read_text());pins[str(path.resolve())]=sha(path)
  need(proof['passed']and proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and proof['guestSHA256']==current.GUEST_SHA,
       'Actual current independently source-qualified native build')
  need(proof['currentContinuousSceneFIFOProjectionGroundAndShadowDisableAccepted']and proof['completeCurrentStateRowsEqualIndependentQualifiedReference']and
       proof['threeOverlappingNativeRGBStagesExactlyEqual']and proof['newNextCPURGBRecaptured']and proof['actualSemanticFaultsRejected']==21 and
       len(proof['actualNativePixelFaultsRejected'])==2 and len(proof['actualNativeAPIPhaseFaults'])==3 and
       proof['actualNativeReviewPanels']==3 and not proof['fullAudioAcceptance']and not proof['fullArtAcrossAllArenasAccepted']and not proof['fullPortAcceptance'],
       'Complete finite current FIFO/floor/shadow/source/pixel/phase controls; no broader claim')
  for p,h in proof['inputHashes'].items():need(sha(p)==h,'Every actual capture/source/review/control input intact');pins[p]=h
  physical=proof['nativeFIFO']['nativePhysicalFreeze']
  need(physical['allActualFrozenIntegerWorldCoordinatesHeld']and physical['sourceNativeGroundingAndShadowDisableAccepted']and
       physical['frozenWholeAndLegShadowCopies']==0 and physical['lastPreFreezeShadowDraw']==physical['nativeShadowDisableFrame']==physical['origin']+56,
       'Original stock shadow disable and held ground positions, not fabricated corpse shadows')
  terminal=proof['actualWindowsTerminal'];need(terminal['nativeExit']==0 and terminal['actualWindowsIdentity']['ProcessId']==terminal['pid'],
       'Actual Windows process creation/executable/full command and native terminal before cleanup')
  native=proof['actualOriginalNativeRawTransport']['wholeOriginalShatterStateMatrix']
  need(native['actualSubsequentMatchVerified']and native['identity']==(17 if fighter=='kano'else 18)and native['side']==side,'True owned victim and next CPU match')
  folder=(ROOT/f'audit_v{6183 if fighter=="sonya"and side==1 else 6178}_current_subzero_{fighter}_p{side}_native_scene_ram').resolve()
  need(folder.parent==ROOT.resolve(),'Exact terminal target in user-named working directory')
  targets.extend(p for p in folder.iterdir()if p.is_file()and p.suffix in('.json','.log'))
  cases.append(dict(fighter=fighter,side=side,proof=str(path),sha256=sha(path),actualNativeFields=proof['exactNativeFields'],
    actualRGBPixels=proof['exactNativeRGBPixels'],actualVictimFields=physical['actualVictimFields'],nativeShadowDisableFrame=physical['nativeShadowDisableFrame'],
    actualPreFreezeOwnedShadowCopies=physical['actualPreFreezeOwnedShadowCopies'],sourceBoundProjections=proof['nativeFIFO']['sourceBoundProjections'],
    actualSemanticFaultsRejected=21,actualNativeAPIPhaseFaultsRejected=3,actualNativePixelFaultsRejected=2,
    actualNextCPUMatchFrame=native['actualNextCPUMatchFrame'],nativeReview=proof['nativeReview'],actualReviewPanelsViewedAndPixelBound=3,
    actualWindowsTerminal=terminal,actualRawTransportRowsInTrace=6,rawTransportIndependentlyQualified=True))
 need(sum(c['actualNativeFields']for c in cases)==2670 and sum(c['actualRGBPixels']for c in cases)==271272000 and
      sum(c['actualVictimFields']for c in cases)==2550,'Every finite current field/pixel accounted')
 failures=[]
 for version,fighter,side,reason in((6181,'kano',1,'Harness incorrectly demanded unused horizontal velocity zero'),
   (6186,'kano',1,'Harness classified six original guest/GFX/RGB protocol records as state rows'),
   (6190,'kano',1,'Harness compared original pre-render screen bitmap with same-callback post-render snapshot'),
   (6190,'kano',2,'Same source API phase mismatch'),(6190,'sonya',2,'Same source API phase mismatch')):
  p=ROOT/f'audit_v{version}_current_subzero_{fighter}_p{side}_scene_checked/report.json';r=json.loads(p.read_text())
  need(not r['passed']and not r['fullPortAcceptance'],'Executed failed predicate/report retained')
  pins[str(p.resolve())]=sha(p);failures.append(dict(report=str(p),reason=reason,nativeGameFailure=False))
 failed_folder=(ROOT/'audit_v6178_current_subzero_sonya_p1_native_scene_ram').resolve()
 failed_report=ROOT/'audit_v6179_current_subzero_sonya_p1_scene_observed/report.json'
 failed=json.loads(failed_report.read_text());terminal=json.loads((failed_folder/'native_terminal.json').read_text())
 need(not failed['passed']and terminal['nativeExit']==0 and terminal['actualWindowsIdentity']['ProcessId']==terminal['pid'],
      'Initial native SonyaP1 finished; genuine early stock palette caused host observer failure')
 for p in failed_folder.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 pins[str(failed_report.resolve())]=sha(failed_report)
 targets.extend(p for p in failed_folder.iterdir()if p.is_file()and p.suffix in('.json','.log'))
 failures.append(dict(report=str(failed_report),reason='Early attract Cage palette outside original observer whitelist; native game completed without failure',
                      actualWindowsTerminal=terminal,nativeGameFailure=False,successor=str(ROOT/'audit_v6184_current_subzero_sonya_p1_scene_observed/report.json')))
 preboot=ROOT/'audit_v6188_subzero_capture_scope_failure/report.json';need(not json.loads(preboot.read_text())['passed'],'Preserve pre-boot source-anchor failure')
 pins[str(preboot.resolve())]=sha(preboot)
 failures.append(dict(report=str(preboot),reason='Correction source-anchor indentation failed before native boot',nativeBoots=0,nativeGameFailure=False))
 current.expected()
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Delivered current playtest unchanged');pins[str(archive.resolve())]=sha(archive)
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual native process census empty before exact completed-file compression')
 need(len(targets)==len(set(targets))and all(str(p.resolve())in pins for p in targets),'Only exact unique hash-bound completed JSON/log targets')
 before={str(p):storage.allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in pins.items()),'Lossless terminal-only LZX preserves every logical source/evidence/release hash')
 after={str(p):storage.allocated(p)for p in targets}
 audit=previous['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Natural finishers'))
 item['status']+=' Current Sub-Zero continuous earned freeze-and-shatter scenes now qualify both true own IDs17/18 in both physical slots:2670consecutive complete source-replayed native fields,271272000displayed RGB pixels, complete FIFO/cache/descriptor/palette/physical-owner/camera/grounding and source-native shadow behavior. Own compressed shadows draw before freeze and the original FF8C25C0 flag clear disables them at origin+56; raw frozen whole/leg art cannot silently publish an extra shadow. Integer coordinates remain held on native floor even with original unused collision VX words. All impact fields, including native paused render fields, and held final winner pages remain accounted without forced clearing.84actual FIFO/physical/shadow faults,12native API-phase faults and8actual VRAM/RGB faults rejected. Every current native state/input/health/opcode/effect/retirement/next-CPU row equals the independent current sparse proof; all four screen-bitmap RGB event records equal its baseline, while12overlapping whole RGB images equal the fixed preceding video-snapshot field. The two APIs intentionally differ in same-callback render phase; no nearest-frame lookup or pixel substitution. All12new native review panels visually inspected and pixel-bound. Original failed sources/reports and early-attract palette collection failure retained; no ROM edit. Finite normal DeadPool scene only: normal-health freeze, full audio, alternate costumes/arenas/CPU/overlap/other consumers and integrated release remain open.'
 item['evidence'].extend(dict(path=c['proof'],sha256=c['sha256'])for c in cases)
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',parentAdditiveJournal=str(PARENT),
   remaining=previous['remaining'],requirementAudit=audit,newInputHashes=pins,cases=cases,
   previousGoalTurnClassification='no progress: gratitude-only reply; revalidated actual outstanding handles/results before continuing',
   thisTurnClassification='progress: four current continuous native scenes fully qualified; source-specific collector assumptions corrected; terminal storage reduced',
   actualCurrentVictimContexts=4,actualNormallyEarnedKOs=8,actualContinuousNativeFields=2670,actualDisplayedRGBPixels=271272000,
   actualPhysicalVictimFields=2550,actualNextCPUMatches=4,actualNativeReviewPanelsViewedAndPixelBound=12,
   actualNewSemanticFaultsRejected=84,actualNativeAPIPhaseFaultsRejected=12,actualNativePixelFaultsRejected=8,
   failedHostChecksRetained=failures,terminalOnlyFilesLosslesslyCompressed=len(targets),logicalBytes=sum(p.stat().st_size for p in targets),
   allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),allocatedBytesReclaimed=sum(before.values())-sum(after.values()),
   actualBefore=before,actualAfter=after,compressionOutput=result.stdout,nativeGameChanges=0,newNativeBootsStartedThisContinuation=0,
   observedNativeTerminals=5,acceptedNativeContinuousCaptures=4,newBuildCopies=0,newSourceDirectoryCopies=0,filesDeleted=0,
   separateRawRasterROMOrAudioFilesWritten=0,originalRawProtocolEmbeddedInPreservedTrace=True,currentReleaseZIPUnchanged=True,
   currentDeclaredDeadPoolContinuousSceneAndNativeGroundShadowDisableAccepted=True,normalHealthFreezeAccepted=False,
   fullArtAcrossAllArenasAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,
   nextActions=['Qualify current normal-health Subzero ice/thaw/control and native floor-shadow observations',
                'Complete remaining finisher/cinematic audio and arena/CPU/overlap consumers',
                'Final combined selection/ladder/names/moves/audio regression, dependency-aware cleanup and matching release'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive full-scope continuous Subzero checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','requirementAudit','newInputHashes','actualBefore','actualAfter','compressionOutput')},indent=2),flush=True)
