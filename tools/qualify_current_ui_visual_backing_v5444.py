"""Whole current displayed-frame bytes bind existing PNGs for visual review.

No new raster files or emulator boots. Current RAM native frames were already
source/native-stock pixel-qualified; old PNGs are only exact byte backing.
"""
import datetime,hashlib,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
from PIL import Image
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5443_current_ui_audio_storage_progress/progress.json'
OUT=ROOT/'audit_v5445_current_ui_visual_progress'
INSPECTED=(('kano_p1',986),('sonya_p2',986),('sonya_p1',1288),('kano_p2',1874),('sonya_p1',1874))

def run():
 current.expected();parent=json.loads(PARENT.read_text());need(parent['passed'],'Actual completed current combined UI/name audio/storage checkpoint')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 old_path=ROOT/'audit_v3198_native_morph_shadow_ui_checked/report.json';old=json.loads(old_path.read_text())
 need(old['passed']and old['currentBothSlotSelectionLadderFirstMatchAccepted'],'Previously qualified immutable image backing, not transferred old runtime acceptance')
 frames=[]
 for key in('kano_p1','sonya_p1','kano_p2','sonya_p2'):
  path=ROOT/'audit_v5440_current_ui_audio_ram'/f'{key}_samples'/'run.log'
  need(sha(path)==pins[str(path)],'Actual just-executed current full displayed pixel digest trace')
  log=path.read_text();rows={r['filename']:r for line in log.splitlines()if line.startswith('MK2_UA_RGB_DIGEST ')for r in[dict(re.findall(r'(\w+)=([^\s]+)',line))]}
  for frame in(986,1288,1874):
   name=f'ui_{frame:04d}.png';backing=ROOT/f'audit_v3196_ui_{key}'/'snap'/name
   need(sha(backing)==old['inputHashes'][str(backing)],'Original previously qualified retained native PNG unchanged')
   rgb=np.asarray(Image.open(backing).convert('RGB'));need(rgb.shape==(254,400,3),'Unscaled complete native frame backing')
   raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=rgb[:,:,::-1];raw[:,:,3]=255
   digest=hashlib.sha256(raw.tobytes()).hexdigest().upper()
   need(digest==rows[name]['sha256'],'Every actual current displayed RGB32 byte matches selected pinned backing; no crop/tolerance/old-runtime substitute')
   frames.append(dict(case=key,actualNativeFrame=frame,backing=str(backing),actualDisplayedRGB32SHA256=digest,
    completeNativePixels=101600,mainAgentVisuallyInspected=(key,frame)in INSPECTED))
   pins[str(backing)]=sha(backing)
 for p in(old_path,Path(__file__).resolve()):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All original source/capture/public bytes stable after visual backing qualification')
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'No native process still running')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),cases=parent['cases'],actualCurrentDisplayedFrameBackings=frames,
  previousGoalTurnClassification=parent['previousGoalTurnClassification'],
  thisGoalTurnClassification=parent['thisGoalTurnClassification']+'; twelve whole actual current frames bound byte-exact to existing image backing and five actual native selection/ladder/match frames visually inspected',
  currentBothSlotSelectionLadderFirstMatchPixelsAccepted=True,completeObservedNativeSelectionNamesAudioAccepted=True,
  actualCurrentUIStatePixelFaultMethods=parent['actualCurrentUIStatePixelFaultMethods'],
  actualCurrentSelectionAudioFaultsRejected=parent['actualCurrentSelectionAudioFaultsRejected'],
  currentTurnRetainedEvidenceAllocatedBytes=parent['currentTurnRetainedEvidenceAllocatedBytes'],
  actualCompleteCurrentDisplayedFrameBytesQualified=12*406400,actualCompleteFrameBackings=12,mainAgentActualFramesVisuallyInspected=5,
  finiteVisualReview='Kano P1 and Sonya P2 selection show native player-number/cursor/portrait/stance presentation; Sonya ladder reveal contains only native small ladder icon, no full CSS portrait or pose; Kano P2 and Sonya P1 are their real match sprites with name shadows and visible native floor shadows. This is finite inspection, not canonical artistic or all-arena/all-phase acceptance.',
  newNativeBoots=0,newBuilds=0,newDeletedFiles=0,newRasterFiles=0,newAudioFiles=0,
  noNativeProcessStillLive=True,publicPlayableChanged=False,refreshedReleaseZIP=False,
  canonicalArtisticFidelityAccepted=False,allAudioContextsAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction=parent['nextAction'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive current native displayed-frame visual checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','actualCurrentDisplayedFrameBackings')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
