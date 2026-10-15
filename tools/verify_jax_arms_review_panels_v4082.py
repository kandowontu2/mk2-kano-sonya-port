"""Bind all44 essential arm-rip review panels to actual full native RGB hashes."""
import hashlib,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
from PIL import Image
import run_jax_arms_native_scene_v4074 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4083_jax_arms_native_review_panels_checked'

def run():
    need(not OUT.exists(),'Fresh immutable contact-sheet binding')
    matrix=capture.OUT/'report.json';value=json.loads(matrix.read_text())
    need(value['passed']and len(value['cases'])==4,'All four actual continuous native arm-rip contexts')
    pins={str(matrix):sha(matrix),str(Path(__file__).resolve()):sha(__file__),str(Path(capture.__file__)):sha(capture.__file__)};cases=[]
    for case in value['cases']:
        fighter,side=case['fighter'],case['side'];folder=ROOT/f'audit_v4075_jax_arms_{fighter}_p{side}_native_scene_ram'
        image=capture.REVIEW/f'{fighter}-p{side}-native-arms-review.png'
        a=np.asarray(Image.open(image).convert('RGB'));need(a.shape==(1668,800,3),'Exact11-panel native review layout')
        visible=folder/'visible_digests.json';records=folder/'continuous_scene_records.json'
        rows=json.loads(visible.read_text());scene=json.loads(records.read_text());meta=json.loads((folder/'result.json').read_text())
        digests={int(re.search(r'_(\d+)\.png$',r['file']).group(1)):r['rgbSHA256']for r in rows}
        need(len(digests)==608 and meta['modelExactFields']==meta['observedRGBFields']==len(scene)==608 and not meta['modelErrors'],'Every actual field source/RGB replay exact')
        panels=[];frames=list(sorted(case['actualPhaseFrames'].items()))+[('native_WIN_page',scene[-1]['frame'])]
        need(len(frames)==11 and set(case['actualPhaseFrames'])=={f'{k}_{p}'for k in('body','arms')for p in range(5)},'All ten actual body/arm phases plus final native WIN page')
        for index,(phase,frame)in enumerate(frames):
            x,y=(index%2)*400,(index//2)*278;raw=a[y+24:y+278,x:x+400].tobytes();digest=hashlib.sha256(raw).hexdigest().upper()
            need(digest==digests[frame],'Every full essential panel exactly actual native RGB, no composite/draw/recolour/reposition')
            panels.append(dict(phase=phase,frame=frame,actualNativeRGBSHA256=digest,exactNativeRGBPixels=101600))
        for p in(image,visible,records,folder/'result.json'):pins[str(p)]=sha(p)
        cases.append(dict(fighter=fighter,side=side,essentialNativeReview=str(image),actualPanels=panels,exactRGBPixels=1117600))
    return dict(passed=True,actualContexts=4,exactNativePanels=44,exactNativePanelPixels=4470400,cases=cases,inputHashes=pins,
        nativeReviewAssetsAreOriginalPresentedFrames=True,aestheticAcceptance=False,stockVictimCornerPlacementComparisonAccepted=False,allArenaFinisherAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable panel report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Panel report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
