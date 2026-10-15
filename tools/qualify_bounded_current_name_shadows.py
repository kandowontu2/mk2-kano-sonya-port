"""Actual four-slot native name face and offset shadow pixels, no new captures."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_source_sync as sync

def masks(ui,identity,side):
    sw,sh=ui[4],ui[5];colors=int.from_bytes(ui[6:8],'little')
    names=8+2*(colors*2+sw*sh);width,height=ui[names:names+2]
    offset=names+2+(identity-17)*width*height
    face=np.frombuffer(ui[offset:offset+width*height],dtype=np.uint8).reshape(height,width)[:10]>48
    occupied=np.where(face)[1];face=face[:,occupied.min():occupied.max()+1]
    visible=np.pad(face,((0,0),(0,1)));edge=np.zeros(visible.shape,dtype=bool)
    edge[:,1:]|=visible[:,:-1];edge[1:,1:]|=visible[:-1,:-1];edge&=~visible
    return visible,edge,29 if side==1 else 367-visible.shape[1]

def gate(image,face,edge,x):
    assert image.shape==(254,400,3)
    area=image[30:40,x:x+face.shape[1]]
    assert np.all(area[edge]==np.array([66,0,0],dtype=np.uint8))
    assert np.all((area[face,0]>150)&(area[face,1]>100)&(area[face,2]<100))
    return dict(nameFacePixels=int(face.sum()),nativeDarkShadowPixels=int(edge.sum()),shadowRGB=[66,0,0],left=x,top=30)

out=sync.ROOT/'audit_bounded_current_name_shadows_checked';assert not out.exists()
proof_path=sync.ROOT/'audit_bounded_current_ui_review_checked/report.json';proof=json.loads(proof_path.read_text());assert proof['passed']
ui_path=sync.ROOT/'roms/mk2ks/mk2ks.ui';ui=ui_path.read_bytes();results={}
for fighter,identity in (('kano',17),('sonya',18)):
    for side in (1,2):
        key=f'{fighter}P{side}';folder=sync.ROOT/f'audit_bounded_current_ui_select_{fighter}_p{side}_runtime'
        image_path=folder/'snap/ui_1814.png';assert sync.sha(image_path)==proof['results'][key]['imageSHA256']['ui_1814.png']
        assert sync.sha(folder/'run.log')==proof['results'][key]['logSHA256']
        image=np.asarray(Image.open(image_path).convert('RGB'));face,edge,x=masks(ui,identity,side)
        positive=gate(image,face,edge,x);faults=[]
        for fault in ('missing_shadow','shifted_name'):
            bad=image.copy()
            if fault=='missing_shadow':bad[30:40,x:x+face.shape[1]][edge]=[0,255,0]
            else:bad[30:40,x:x+face.shape[1]]=np.roll(bad[30:40,x:x+face.shape[1]],1,axis=1)
            try:gate(bad,face,edge,x)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Actual name raster fault accepted')
        results[key]=dict(**positive,rejectedFaults=faults,imageSHA256=sync.sha(image_path))
report=dict(passed=True,results=results,sourceSync=sync.verify(),uiSHA256=sync.sha(ui_path),priorProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),scope='First native fight frame in all four slots matches whole name face and native offset shadow model. Does not accept all fade/win/finisher phases or finished release.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,nativeNameShadowsVerified=True)))
