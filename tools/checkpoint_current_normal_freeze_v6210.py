"""Complete current ordinary freeze journal, actual pixel faults, bounded LZX.

Keep the full five-group objective, seven genuine current terminals and all
native sources/records/reviews. Only terminal hash-bound JSON/logs compressed.
Ordinary freeze is distinct from the native fatality shadow-disable policy.
"""
import hashlib,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from PIL import Image
import checkpoint_current_kitana_scene_v6121 as storage
ROOT,need,sha,current=storage.ROOT,storage.need,storage.sha,storage.current
PARENT=ROOT/'audit_v6196_current_subzero_native_scene_progress/progress.json'
PROOF=ROOT/'audit_v6209_current_normal_subzero_freeze_checked/report.json'
OUT=ROOT/'audit_v6211_current_normal_subzero_freeze_progress'

def native_panels(atlas,records):
 need(atlas.shape==(556,800,3)and len(records)==4,'Four complete actual native event panels in one bounded atlas')
 for i,r in enumerate(records):
  x,y=i%2*400,i//2*278
  need(hashlib.sha256(atlas[y+24:y+278,x:x+400].tobytes()).hexdigest().upper()==r['actualRGBSHA256'],
       'Every actual native review pixel equals the captured native RGB target')
 return True

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,'Entire original objective remains active')
 need(proof['passed']and proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and proof['guestSHA256']==current.GUEST_SHA and
      proof['actualCurrentOwnCharacterSlotCases']==4 and proof['actualCurrentStockControls']==2 and proof['actualFreshRepeats']==1 and
      proof['actualOrdinaryFields']==proof['actualPairedShadowFields']==4907 and proof['actualSemanticFaultsRejected']==138 and
      proof['actualNativePanelFaultsRejected']==12 and proof['actualSourceNativeRawHandShadowCopies']==1260 and
      proof['actualNativeReviewPanels']==28 and proof['actualEventRGBPixels']==2844800 and proof['allNativePanelsPixelBound']and
      proof['currentSonyaP1RepeatEveryNativeRowStreamAndRGBIdentical']and proof['completeCurrentOrdinaryFreezeThawControlsAnd701NativeShadowFieldsAccepted']and
      proof['originalSourceNativeRawHandStepsAccepted']and not proof['fullAudioAcceptance']and not proof['continuousNativeRGBReplayAccepted']and
      not proof['fullArtAcrossAllArenasAccepted']and not proof['fullPortAcceptance'],'Whole finite current ordinary native state/shadow/source/pixel/repeat matrix intact')
 pins={str(p.resolve()):sha(p)for p in(PARENT,PROOF,Path(__file__),Path(storage.__file__))}
 for p,h in proof['inputHashes'].items():need(sha(p)==h,'Every current source/native/review/control input unchanged');pins[p]=h
 current.expected();targets=[];cases=[];pixel_faults=[]
 configurations=[(c['fighter'],c['side'],6200,6201)for c in proof['cases']]+[('sonya',1,6203,6204)]
 for fighter,side,folder_version,report_version in configurations:
  folder=(ROOT/f'audit_v{folder_version}_current_normal_subzero_{fighter}_p{side}').resolve()
  report_path=ROOT/f'audit_v{report_version}_current_normal_subzero_{fighter}_p{side}_observed/report.json'
  r=json.loads(report_path.read_text());t=json.loads((folder/'native_terminal.json').read_text())
  need(folder.parent==ROOT.resolve()and r['passed']and r['nativeExit']==t['nativeExit']==0 and r['actualWindowsTerminal']==t and
       t['actualWindowsIdentity']['ProcessId']==t['pid']and Path(t['actualWindowsIdentity']['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
       'mk2ks_current_normal_freeze_shadow_v6198.lua'in t['actualWindowsIdentity']['CommandLine'],'All seven actual native creation/executable/full commands and terminal records before cleanup')
  records=json.loads((folder/'rgb_memory_proofs.json').read_text())
  need(records==r['actualScenes'],'Complete native records unchanged before actual pixel negative controls')
  atlas=np.asarray(Image.open(r['nativeReview']).convert('RGB'));native_panels(atlas,records)
  # Change actual decoded native target pixels, NOT expected hashes or
  # report inventory. These are separate from the12 transport-digest faults.
  for index in(0,1):
   changed=atlas.copy();x,y=index%2*400,index//2*278;changed[y+24,x,0]^=1
   try:native_panels(changed,records)
   except ValueError as error:pixel_faults.append(dict(fighter=fighter,side=side,version=folder_version,panel=index,
                                                      actualNativeRGBByteChanged=True,expectedRecordsChanged=False,rejectedBy=str(error)))
   else:raise ValueError('Actual native pixel bit fault admitted')
  need(native_panels(atlas,records),'Uncached whole native pixel positive restored after target-bit corruptions')
  cases.append(dict(fighter=fighter,side=side,version=folder_version,actualWindowsTerminal=t,nativeReview=r['nativeReview'],
                    reviewSHA256=sha(r['nativeReview']),actualNativeReviewPanelsViewedAndPixelBound=4))
  targets.extend(p for p in folder.iterdir()if p.is_file()and p.suffix in('.json','.log'))
  targets.append(report_path)
 need(len(cases)==7 and len(pixel_faults)==14,'All28actual native panels and14real target-bit corruptions qualified')
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Actual delivered current release unchanged');pins[str(archive.resolve())]=sha(archive)
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual current native process census empty before terminal-only compression')
 need(len(targets)==len(set(targets))and all(str(p.resolve())in pins for p in targets),'Only exact unique hash-bound completed records compressed')
 before={str(p):storage.allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in pins.items()),'Lossless LZX preserves every logical native/source/review/release hash')
 after={str(p):storage.allocated(p)for p in targets}
 audit=previous['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Complete native-feeling moves'))
 item['status']+=' Current ordinary-health Sub-Zero ice/thaw/control sequence now qualifies four true own-character/physical-slot contexts, two actual current stock Kitana/LiuKang controls and a fresh SonyaP1 repeat. All4907continuous native physical fields and paired shadow fields,701per run, retain correct actual IDs/owners/full161health/native floors. Original160field freeze uses native0505ice palette and shadow eligibility; natural thaw restores own palette, then physical movement and high punch work and complete. Every shadow component, native descriptor/flip/cache/world/camera/ground projection, entire independently reconstructed compressed stream and original DMA source/pen/caller/cadence qualified throughout all701fields, not just four snapshots. The original raw11x18Sub-Zero ice hand remains raw; whole original kernel/disassembly independently qualifies its unconditional signed header scanner and all1260actual quarter-height source-step copies, including duplicate tails, with no imported raw admission. All138semantic faults (original126plus12continuous-window/raw-step faults),12RGBtransport-digest faults and14actual native RGB target-bit corruptions rejected. All28native event panels visually inspected and pixel-bound,2,844,800event pixels; four new native stages in each main case equal the protected whole baseline, and every repeat row/stream/native stage exactly matches the first current Sonya run. Superseded quadratic host verifier was intentionally stopped after identity confirmation; all seven native games had already finished and were not restarted or interrupted. Exact ordered DMA indexing and RAM-only aliasing of proven equal inventories preserve every check. Ordinary frozen actors retain shadows; the earlier finisher intentionally disables them at its stock native flag transition. No game edit justified. Finite DeadPool human sequence only: continuous whole-scene RGB/audio, alternate arenas/costumes/CPU/repeated/KO/overlap/other consumers and final integrated release remain open.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',parentAdditiveJournal=str(PARENT),
  remaining=previous['remaining'],requirementAudit=audit,newInputHashes=pins,cases=cases,
  previousGoalTurnClassification='progress: current continuous earned Subzero scenes qualified and exact terminal storage reduced',
  thisTurnClassification='progress: seven current ordinary-health freeze/thaw/control and full701field native shadow captures qualified, actual pixels fault-tested and terminal storage reduced',
  actualCurrentOwnCharacterSlotCases=4,actualCurrentStockControls=2,actualFreshSonyaP1Repeats=1,actualNativeTerminals=7,
  actualOrdinaryFields=4907,actualPairedShadowFields=4907,actualNormalIceFields=1120,actualProjectionParts=proof['actualProjectionParts'],
  actualSourceBoundCompressedShadowCopies=proof['actualSourceBoundCompressedShadowCopies'],actualSourceNativeRawHandShadowCopies=1260,
  actualSemanticFaultsRejected=138,actualNativeRGBTransportFaultsRejected=12,actualNativeRGBPixelFaultsRejected=14,actualNativePixelFaults=pixel_faults,
  actualNativeReviewPanelsViewedAndPixelBound=28,actualNativeEventRGBPixels=2844800,terminalOnlyFilesLosslesslyCompressed=len(targets),
  logicalBytes=sum(p.stat().st_size for p in targets),allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),
  allocatedBytesReclaimed=sum(before.values())-sum(after.values()),actualBefore=before,actualAfter=after,compressionOutput=result.stdout,
  nativeGameChanges=0,newNativeBootsStarted=7,newBuildCopies=0,newSourceDirectoryCopies=0,separateRawMediaFilesWritten=0,filesDeleted=0,
  nativeGameProcessesInterrupted=0,supersededHostVerifierInterrupted=1,currentReleaseZIPUnchanged=True,
  currentDeclaredNormalFreezeThawControlsAndFullNativeShadowLedgerAccepted=True,
  continuousFullSceneRGBReplayAccepted=False,fullArtAcrossAllArenasAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,
  nextActions=['Complete native finisher/victim audio and remaining cinematic consumers',
               'Broader arena/CPU/repeated/KO/overlap move and shadow regression',
               'Final combined selection/ladder/names/moves/audio verification and matching release/cleanup audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive current ordinary ice/full-shadow checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','requirementAudit','newInputHashes','actualBefore','actualAfter','compressionOutput','actualNativePixelFaults')},indent=2),flush=True)
