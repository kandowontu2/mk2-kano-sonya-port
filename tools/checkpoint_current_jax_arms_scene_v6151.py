"""Current arm-rip own scenes and six genuine stock profiles; full-scope journal.

Bind all44 own and36 stock review panels to actual native pixels. Finite
normal Dead Pool art/profile assessment only, not universal arena/audio
acceptance. Preserve failed pre-game whitelist controls, then compact exact
terminal traces without deleting evidence or making build/package copies.
"""
import hashlib,json,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from PIL import Image
import checkpoint_current_kitana_scene_v6121 as storage
ROOT,need,sha,current=storage.ROOT,storage.need,storage.sha,storage.current
PARENT=ROOT/'audit_v6140_current_jax_clap_native_scene_progress/progress.json'
PROOF=ROOT/'audit_v6145_current_jax_arms_scene_checked/report.json'
STOCK=ROOT/'audit_v6157_current_jax_arms_stock_profiles_checked/report.json'
OUT=ROOT/'audit_v6152_current_jax_arms_native_scene_progress'

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text());stock=json.loads(STOCK.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,'All original requirement groups remain open')
 need(proof['passed']and proof['actualContexts']==4 and proof['exactNativeFields']==2432 and proof['exactRGBPixels']==247091200 and
      proof['actualSemanticFaultsRejected']==140 and proof['actualNativePixelTargetFaultsRejected']==8 and
      proof['currentEarnedArmsStateFullSceneFIFOPropProjectionGroundingShadowAndCleanupAccepted']and
      not proof['fullAudioAcceptance']and not proof['fullPortAcceptance'],'Entire current own state/scene/FIFO/prop/shadow matrix accepted')
 need(stock['passed']and stock['actualStockContexts']==6 and stock['actualAddedCharacterContexts']==0 and
      stock['actualNativePanels']==36 and stock['actualNativePanelPixels']==3657600 and stock['actualSemanticFaultsRejected']==42 and
      stock['currentNativeStockPositionProfilesAndHeldPageObserved']and not stock['fullStockSceneReplayAccepted']and
      not stock['allStockFinisherFidelityAccepted']and not stock['fullPortAcceptance'],'Actual current six-stock table/placement/held-page and36native panel controls')
 pins={str(p):sha(p)for p in(PARENT,PROOF,STOCK,Path(__file__).resolve(),Path(storage.__file__).resolve())}
 for matrix in(proof,stock):
  for p,h in matrix['inputHashes'].items():need(sha(p)==h,'All current executed source/native/panel evidence intact');pins[p]=h
 guest=current.expected()
 # Native X offsets come from independently stock-qualified original tables,
 # not an ad-hoc screen-position or crop correction. Sonya/Jax share y4 too.
 positions={i:int.from_bytes(guest[0xfba50+i*4:0xfba54+i*4],'little')for i in(1,4,11,17,18)}
 need(all(positions[i]&65535==0xff70 for i in(1,11,17,18))and positions[4]&65535==0xff88 and
      positions[11]==positions[18]==0x0004ff70,'Actual relevant stock/own position profiles; whole stock rows previously source-qualified')
 panels=[];folders=[]
 for c in proof['cases']:
  need(c['actualWindowsTerminal']['nativeExit']==0,'Real current own native exit precedes cleanup')
  folder=(ROOT/f"audit_v6142_current_jax_arms_{c['fighter']}_p{c['side']}_native_scene_ram").resolve();folders.append(folder)
  observed=json.loads((ROOT/f"audit_v6143_current_jax_arms_{c['fighter']}_p{c['side']}_scene_observed/report.json").read_text())
  records=json.loads((folder/'continuous_scene_records.json').read_text());visible=json.loads((folder/'visible_digests.json').read_text())
  rgb={int(re.search(r'_(\d+)\.png$',r['file']).group(1)):r['rgbSHA256']for r in visible}
  atlas=np.asarray(Image.open(c['nativeReview']).convert('RGB'));need(atlas.shape==(1668,800,3),'One actual own eleven-panel native atlas')
  frames=list(sorted(observed['actualPhaseFrames'].items()))+[('native_WIN_page',records[-1]['frame'])]
  need(len(frames)==11 and set(observed['actualPhaseFrames'])=={f'{k}_{p}'for k in('body','arms')for p in range(5)},'Every actual own body/arm phase plus held page')
  for index,(phase,frame)in enumerate(frames):
   x,y=index%2*400,index//2*278
   digest=hashlib.sha256(atlas[y+24:y+278,x:x+400].tobytes()).hexdigest().upper()
   need(digest==rgb[frame],'Every whole own review panel exactly actual native displayed pixels; no crop/reposition/substitution')
   panels.append(dict(fighter=c['fighter'],side=c['side'],phase=phase,frame=frame,rgbSHA256=digest))
 for c in stock['cases']:
  need(c['actualWindowsTerminal']['nativeExit']==0,'Real actual stock native exit precedes cleanup')
  folders.append(Path(c['essentialNativeReview']).parent.parent.resolve())
 # Preserve the two exact failed boot observations. This was an unsupported
 # physical-controller whitelist label, before first guest/RGB observation;
 # successors allow stock Jax11 without a guest/state write.
 failures=[]
 for side in(1,2):
  folder=(ROOT/f'audit_v6154_current_jax_arms_stock_jax_p{side}_corner_ram').resolve()
  meta=json.loads((folder/'result.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
  rp=ROOT/f'audit_v6155_current_jax_arms_stock_jax_p{side}_corner_observed/report.json'
  need(not json.loads(rp.read_text())['passed']and meta['exit_code']==terminal['nativeExit']==3 and
       meta['guestSHA256']is None and meta['actualNativeRGBFrames']==0 and
       'mk2ks_stock_fatality_v1021_RAM_image_sink:5: assertion failed!'in(folder/'stderr.log').read_text(),
       'Exact before-first-frame controller whitelist failure retained, not a gameplay/ROM failure')
  for p,h in meta['inputHashes'].items():need(sha(p)==h,'Failed-control actual inputs intact');pins[p]=h
  for p in folder.iterdir():
   if p.is_file():pins[str(p.resolve())]=sha(p)
  pins[str(rp)]=sha(rp);folders.append(folder)
  failures.append(dict(side=side,pid=terminal['pid'],nativeExit=3,guestObserved=False,nativeRGBFrames=0,
                       cause='Original physical controller allowed only17/18/1/4 victim labels; stock Jax11 extension added in successor',
                       originalFailedCapture=str(folder),successor=f'audit_v6161_current_jax_arms_stock_jax_p{side}_corner_ram'))
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Current delivered playtest ZIP unchanged');pins[str(archive)]=sha(archive)
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual current native emulator census empty before terminal compression')
 targets=[]
 for folder in folders:
  need(folder.parent==ROOT.resolve(),'Resolved exact terminal path stays inside user-named workspace')
  for p in folder.iterdir():
   if p.is_file():
    need(p.suffix in('.json','.log')and str(p.resolve())in pins,'Only already hash-bound terminal metadata/traces')
    targets.append(p)
 before={str(p):storage.allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in pins.items()),'Exact LZX preserves all executed/evidence logical bytes')
 after={str(p):storage.allocated(p)for p in targets}
 audit=previous['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Natural finishers'))
 item['status']+=' Current Jax arm-rip now qualifies four true own-character/physical-slot contexts: eight normally collision-earned KOs, full original command/table/completion and true-victim prop palette/register/stack grammar, all40owned body/arm phases,2432continuous native fields and247091200displayed RGB pixels. Complete native physical FIFO/components/projection/grounding/compressed-shadow, two genuine ID0 detached props, all original four-field prop cadence/descriptor/normal palette/DMA and exact teardown/held-page behavior verified.140actual semantic and8actual native RGB/VRAM faults rejected. All44own review panels native-bound and visually inspected. Six real current stock Kitana/LiuKang/Jax controls add36native-bound reviewed panels and42actual semantic faults. Relevant stock FF70 horizontal profiles show original edge clipping and armless standing/held-page behavior, unlike the different Kitana FF88 profile; no invented position/clear-screen fix applied. Sonya/Jax share the whole0004FF70 position row. Two original stock-Jax test boots failed before guest/RGB observation because the physical selector whitelist lacked Jax; failed sources/reports retained and true-Jax readonly-selector successors passed. Finite normal DeadPool art/profile assessment only. Independent prop world/camera ledger, wider arenas/alternate costumes/audio/other consumers and integrated whole-port acceptance remain open.'
 item['evidence'].extend([dict(path=str(PROOF),sha256=sha(PROOF)),dict(path=str(STOCK),sha256=sha(STOCK))])
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',
     parentAdditiveJournal=str(PARENT),remaining=previous['remaining'],requirementAudit=audit,newInputHashes=pins,
     previousGoalTurnClassification='progress: four current Jax head-clap scenes and complete state/FIFO/shadow checks qualified',
     thisTurnClassification='progress: current own arm-rip scenes and six relevant stock profiles qualified;80native review panels inspected; exact terminal compression',
     actualOwnContexts=4,actualCurrentStockContexts=6,exactNativeOwnFields=2432,exactNativeOwnRGBPixels=247091200,
     actualNativeOwnReviewPanels=44,actualNativeStockReviewPanels=36,actualNativeStockPanelPixels=3657600,
     actualSemanticFaultsRejected=182,actualNativePixelTargetFaultsRejected=8,finiteNativeOwnArtAndStockProfileReviewAccepted=True,
     actualOwnReviewedPanels=panels,actualStockPositionRows=positions,failedBeforeGameplayControlsRetained=failures,
     separatePropWorldCameraLedgerAccepted=False,universalOwnCornerArtPositionAccepted=False,fullStockSceneReplayAccepted=False,
     terminalOnlyFilesLosslesslyCompressed=len(targets),logicalBytes=sum(p.stat().st_size for p in targets),
     allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),allocatedBytesReclaimed=sum(before.values())-sum(after.values()),
     actualBefore=before,actualAfter=after,compressionOutput=result.stdout,nativeGameChanges=0,newNativeBootsStarted=12,
     successfulNativeOwnBoots=4,successfulNativeStockBoots=6,failedNativeBeforeGameplayBoots=2,
     newBuildCopies=0,newSourceDirectoryCopies=0,rawMediaFilesWritten=0,filesDeleted=0,currentReleaseZIPUnchanged=True,
     fullGoalComplete=False,fullAudioAcceptance=False,fullPortAcceptance=False,
     nextActions=['Exercise current Subzero finisher victims and remaining cinematic consumers',
                  'Complete native finisher/stage audio and broader arena/CPU/KO/overlap coverage',
                  'Run final integrated selection-to-gameplay and matching release audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh full-scope current arm-rip/profile checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('requirementAudit','newInputHashes','actualOwnReviewedPanels','actualBefore','actualAfter','compressionOutput')},indent=2),flush=True)
