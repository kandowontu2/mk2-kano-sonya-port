"""Additive current P2 campaign verdict and bounded lossless evidence compression."""
import datetime,json,subprocess
from pathlib import Path
import verify_current_kano_p2_campaign_v5623 as verification
ROOT,need,sha=verification.ROOT,verification.need,verification.sha
OUT=ROOT/'audit_v5626_current_kano_p2_campaign_progress'

def run():
 need(not OUT.exists(),'Fresh immutable additive journal')
 previous=ROOT/'audit_v5620_stock_port_baraka_cue_sources_qualified/progress.json'
 parent=json.loads(previous.read_text())
 report_path=verification.OUT/'report.json'
 report=json.loads(report_path.read_text())
 need(report['passed']and report['actualNaturalCurrentKanoP2BossesOwnEndingAttractAccepted']and
  report['case']['unassisted_clear_proven']and len(report['actualNativeAndRAMProofFaultsRejected'])==18,
  'Entire true-ID/native/physical-boss/own-ending/attract gate and all18actual faults')
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All executed sources and terminal evidence intact')
 folder=verification.capture.OUT
 files=[p for p in folder.rglob('*')if p.is_file()]
 need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in files),'No raw guest/RGB/audio or automatic native PNG')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':
   '994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Existing public launcher and ZIP unchanged')
 case=report['case']
 pins={str(p.resolve()):sha(p)for p in[previous,report_path,Path(__file__).resolve(),
  Path(verification.__file__).resolve(),Path(verification.capture.__file__).resolve(),*files,*public]}
 progress=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  goalStatus='active',remaining=parent['remaining'],parentAdditiveJournal=str(previous),
  previousGoalTurnClassification='no progress: acknowledgment only; current build, prior proof and absence of live native jobs revalidated before the next safe native run',
  thisGoalTurnClassification='progress: fresh current5219 Kano P2 genuine button-only campaign; every initialized guest byte independently checked in RAM; complete true-ID/selection/native schedules/morph/health/paid-continue/winner/boss-input/own-ending/300attract grammar accepted with18effective faults; no older/P1 chronology substituted',
  wholeCampaignProof=str(report_path),capture=str(folder),candidate=verification.current.NAME,
  physicalSlot=2,trueIdentity=17,actualStages=case['stages_reached'],
  actualNativeAttractFollowThroughFields=report['actualAttractFollowThroughFields'],
  actualNativeAndRAMProofFaultsRejected=report['actualNativeAndRAMProofFaultsRejected'],
  completeUncompressedLogBytes=report['completeUncompressedLogBytes'],
  completeUncompressedLogSHA256=report['completeUncompressedLogSHA256'],
  actualNewNativeBoots=1,actualGuestBytesComparedInRAM=1048576,
  actualNativeCacheGlobalStores=report['actualNativeCacheGlobalStores'],
  actualPersistedFiles=[dict(path=str(p.relative_to(folder)),bytes=p.stat().st_size)for p in files],
  rawGuestRGBPCMFilesWritten=0,automaticNativeTimedBootPNGs=0,newBuilds=0,deletedFiles=0,
  publicPlayableChanged=False,publicZIPChanged=False,sourceInputs=pins,
  fullP2EndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,
  next='Current Sonya P2 physical-policy qualification and actual complete native campaign; all five original remaining groups stay in scope')
 OUT.mkdir();path=OUT/'progress.json'
 path.write_text(json.dumps(progress,indent=2)+'\n')
 sealed=[p for p in folder.rglob('*')if p.is_file()and p.suffix in('.json','.log','.cfg')]+[
  report_path,path,Path(__file__).resolve(),Path(verification.__file__).resolve(),Path(verification.capture.__file__).resolve()]
 before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded evidence compression target')
  result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(result.returncode==0,'Lossless compression succeeded '+str(p))
 need(all(sha(p)==h for p,h in before.items())and all(sha(p)==h for p,h in pins.items()),
  'All sealed/public source and evidence bytes preserved through compression')
 print(json.dumps({k:v for k,v in progress.items()if k not in('sourceInputs','actualPersistedFiles')},indent=2),flush=True)
 return progress

if __name__=='__main__':run()
