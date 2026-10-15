"""Exact whole current RAM frames backed by retained native PNGs for review.

No new raster files; historical runtime acceptance is not transferred.
All 400x254 actual current RGB pixels must equal the pinned PNG bytes.
"""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import capture_launch_candidate_ui as host
ROOT,need,sha=host.ROOT,host.need,host.sha
OUT=ROOT/'audit_launch_candidate_ui_image_backing'

def verify(cases):
 need(not OUT.exists(),'Fresh exact visual-backing receipt')
 accepted=ROOT/'audit_launch_candidate_ui_checked/report.json';proof=json.loads(accepted.read_text())
 need(proof['passed']and proof['currentBothSlotSelectionLadderFirstMatchPixelsAccepted'],'Actual current whole UI pixel/state qualification, not historical runtime')
 old_path=ROOT/'audit_v3198_native_morph_shadow_ui_checked/report.json';old=json.loads(old_path.read_text())
 need(old['passed'],'Original unchanged PNG provenance')
 pins={str(accepted):sha(accepted),str(old_path):sha(old_path),str(Path(__file__).resolve()):sha(__file__)};frames=[]
 for fighter,side in host.faults.CASES:
  key=f'{fighter}_p{side}';folder,text,images=cases[key]
  for frame in(986,1288,1874):
   name=f'ui_{frame:04d}.png';path=ROOT/f'audit_v3196_ui_{key}'/'snap'/name
   need(sha(path)==old['inputHashes'][str(path)],'Exact preserved original native PNG provenance')
   rgb=np.asarray(Image.open(path).convert('RGB'))
   need(rgb.shape==(254,400,3)and np.array_equal(images[name],rgb),'Every current full-frame RGB pixel equals pinned image backing, no tolerance/crop/old-runtime substitute')
   pins[str(path)]=sha(path)
   frames.append(dict(case=key,actualNativeFrame=frame,backing=str(path),wholeNativePixels=101600,
                      actualRGBSHA256=hashlib.sha256(images[name].tobytes()).hexdigest().upper()))
 need(all(sha(p)==h for p,h in pins.items()),'All backing and current proof bytes unchanged')
 report=dict(passed=True,candidate=host.current.NAME,actualCurrentFrames=frames,totalCurrentNativePixels=1219200,inputHashes=pins,
             oldPNGOnlyProvidesExactVisualBacking=True,historicalRuntimeAcceptanceTransferred=False,newNativeBoots=0,newRasterFiles=0,
             newBuilds=0,newROMCopies=0,newZIPs=0,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite image-backing proof')
 print(json.dumps(dict(passed=True,currentWholeFrames=len(frames),totalCurrentNativePixels=report['totalCurrentNativePixels'])),flush=True)
 return report
