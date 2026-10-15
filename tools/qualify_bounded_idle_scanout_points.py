"""Bind finite owned bottom-row source points to completed native RGB fields."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def check(r,fighter):
    assert int(r['frame'])==int(r['source_frame'])+1
    assert r['id']=={'1':str(fighter),'2':'4'}[r['slot']]
    control=int(r['control'],16);adr=int(r['dpyadr'],16)
    assert control&0xc000==0xc000 and control&0x3fc==16
    assert int(r['vsb'])-int(r['veb'])==254
    effective=(adr+254*16)&65535;assert effective==int(r['effective'],16)
    address=effective if control&0x400 else effective^0xfffc
    assert int(r['row'])==(address>>4)&511
    assert int(r['display_y'])==int(r['dma_y'])-int(r['row'])
    assert int(r['display_x'])==int(r['dma_x'])-int(r['column'])
    assert 0<=int(r['display_x'])<400 and 0<=int(r['display_y'])<254
    assert r['expected']==r['actual'] and r['match']=='1'

def main():
    root=sync.ROOT;results={};rejects=[]
    for fighter,id in (('sonya',18),('kano',17)):
        case=root/f'audit_bounded_{fighter}_idle_scanout_delayed_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        points=[];endpoints={}
        for line in text.splitlines():
            if '_IDLE_SCANPOINT ' not in line:continue
            r=dict(re.findall(r'(\w+)=([^\s]+)',line));check(r,id);points.append(r)
            key=(int(r['source_frame']),int(r['slot']))
            endpoints[key]=max(endpoints.get(key,-1),int(r['display_y']))
        assert len(points)==60 and len(endpoints)==30
        diffs=[endpoints[(f,1)]-endpoints[(f,2)] for f in sorted({f for f,s in endpoints})]
        assert diffs==[0]*15
        for key,value in [('actual','FFFFFF'),('frame','9999'),('display_y','0'),('id','1')]:
            mutant=dict(points[0]);mutant[key]=value
            try:check(mutant,id)
            except AssertionError:rejects.append(fighter+'_'+key)
            else:raise AssertionError('Ineffective fault '+key)
        for r in points:check(r,id)
        results[fighter]=dict(rgbBottomPoints=60,displayedMaximumPointDifference=diffs,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_idle_scanout_points_checked';out.mkdir(exist_ok=False)
    report=dict(passed=True,results=results,rejectedFaults=rejects,
        finiteIdleBottomPointAlignmentProven=True,allBottomRowPixelsProven=False,
        allAnimationAlignmentProven=False,fullGoalComplete=False,sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,matchedRgbPoints=120,rejectedFaults=len(rejects))))

if __name__=='__main__':main()
