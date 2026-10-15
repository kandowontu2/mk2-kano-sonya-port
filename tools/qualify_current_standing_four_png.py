"""Four current physical idle captures; does not substitute rectangles for visible soles."""
import json,re,struct,copy
import verify_native_source_sync as sync

def fields(line):return dict(re.findall(r'(\w+)=([^ ]+)',line))
def gate(cases):
    assert len(cases)==4 and sum(c['pngBytes']for c in cases)<=262144
    for c in cases:
        assert c['dimensions']==[400,254]and 0<c['pngBytes']<=65536
        assert c['terminal']['exitCode']==0 and c['terminal']['limitReason']is None
        assert c['terminal']['elapsedSeconds']<90 and c['terminal']['peakWorkingSetBytes']<=320*1024**2
        assert len(c['actors'])==2 and c['completeFrame']==c['captureFrame']
        for n,a in enumerate(c['actors'],1):
            expected=c['id'] if n==c['side'] else 4
            assert int(a['frame'])==c['captureFrame']and int(a['slot'])==n
            assert int(a['mode'])==2 and int(a['state'])==1 and int(a['hp'])>0
            assert int(a['id'])==int(a['roster'])==expected and a['owner']==a['actor']
            assert a['y']==a['floor']and int(a['action'])==771
            assert all(int(a[k],16)==0 for k in ('vx','vy','gravity','trail'))
            q=[p for p in c['projections']if int(p['slot'])==n]
            assert q and all(int(p['frame'])==c['captureFrame']and p['actor']==a['actor']and p['pose']==a['pose']and p['pc']=='FF8042B0'for p in q)

def main():
    sync.verify();root=sync.ROOT;cases=[]
    for identity,side in ((17,1),(17,2),(18,1),(18,2)):
        folder=root/f'audit_current_standing_{identity}_p{side}_runtime';log=(folder/'run.log').read_text();lines=log.splitlines()
        capture=[fields(l)for l in lines if '_CAPTURE 'in l];complete=[fields(l)for l in lines if '_COMPLETE 'in l]
        assert len(capture)==len(complete)==1
        png=folder/'standing.png';raw=png.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        cases.append(dict(id=identity,side=side,path=str(folder),png=str(png),pngBytes=len(raw),pngSHA256=sync.sha(png),dimensions=list(struct.unpack('>II',raw[16:24])),logSHA256=sync.sha(folder/'run.log'),terminal=json.loads((folder/'terminal.json').read_text()),captureFrame=int(capture[0]['frame']),completeFrame=int(complete[0]['frame']),arena=int(capture[0]['arena']),actors=[fields(l)for l in lines if '_FIELD 'in l],projections=[fields(l)for l in lines if '_PROJECTION 'in l]))
    gate(cases);faults=[]
    for label,mutate in [('wrong ownedidentity',lambda x:x[0]['actors'][0].update(id='1')),('wrong floor',lambda x:x[0]['actors'][0].update(floor='0')),('dead actor',lambda x:x[0]['actors'][0].update(hp='0')),('staleprojection frame',lambda x:x[0]['projections'][0].update(frame='1')),('wrong pose',lambda x:x[0]['projections'][0].update(pose='0')),('wrongcamera-linked actor',lambda x:x[0]['projections'][0].update(actor='0')),('extra PNGbudget',lambda x:x[0].update(pngBytes=262145))]:
        bad=copy.deepcopy(cases);mutate(bad)
        try:gate(bad)
        except AssertionError:faults.append(label)
        else:raise AssertionError('Fault admitted:'+label)
    bad=copy.deepcopy(cases);bad[0]['completeFrame']+=1
    try:gate(bad)
    except AssertionError:faults.append('mismatched completion field')
    else:raise AssertionError('Fault admitted:completion field')
    out=root/'audit_current_standing_four_png_v2_checked';assert not out.exists();out.mkdir()
    report=dict(passed=True,cases=cases,pngCount=4,pngTotalBytes=sum(c['pngBytes']for c in cases),effectiveFaultsRejected=faults,physicalTwoHumanOwnedIdleSameFrameProjectionProven=True,opaqueVisibleSoleParityAccepted=False,scope='Finite current physical standing capture binding. Actual PNG opaque foot placement still requires review; native floor/projection rectangles alone do not prove visible sole alignment. Not all poses, arenas, CPU, KO or whole port acceptance.')
    report['manualCurrentStandingVisualReview']={'reviewer':'root','allFourImagesReviewed':True,'bothCharactersBothSlotsVisiblyGroundedAgainstStockKitana':True,'selectorPoseAndPortraitLeaksObserved':False,'lifebarNamesAndShadowsNativeAppearance':True,'approximateSoleRow':228,'exactOpaquePixelRowAutomaticallyMeasured':False,'scope':'Parent independently viewed the four actual current PNGs. Finite standing visual acceptance only, not all arenas/animation/CPU/KO.'}
    report['finiteCurrentStandingManualVisualAcceptance']=True
    (out/'report.json').write_text(json.dumps(report,indent=2));print(out)

if __name__=='__main__':main()
