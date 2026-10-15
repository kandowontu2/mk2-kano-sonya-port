"""Original MK2 body push during the captured natural Bicycle release.

One existing3172 CPU Sonya18/human Kano17 contact, not all moves or arenas.
Reconstruct actual multipart vertical bounds and the original close-body
branches. Both horizontal integrations are checked until own ready; victim
integration continues through its landing and grounded recovery. No game edit.
"""
import json
import re
import struct
import traceback
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import native_cpu_bicycle_hit_contract_v3317 as phase
import verify_human_projectile_display_v1352 as art
import inspect_current_cpu_knife_raster_v1975 as raster
import verify_current_cpu_launch_jump_v3319 as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_v3338_native_bicycle_release_push_checked'
need=prior.need
MASK=0xffffffff

def signed(v):
    return v-0x100000000 if v&0x80000000 else v

def push(x1,x2,bounds1,bounds2,request1,request2,suppression,old1,old2):
    # FF827DF0..FF827E60: shrink BOTH full multipart vertical envelopes by48.
    overlap=bounds1[0]<=bounds2[1]-0x30 and bounds2[0]<=bounds1[1]-0x30
    gap=abs(x1-x2)
    need(gap<0x130,'Bounded release never takes unverified maximum-separation translation')
    if overlap and gap<0x3d:
        # FF8285F0 skips publication while the decremented suppression is nonzero.
        if suppression:return old1,old2,'suppressed'
        a,b=(-0x30000,0x30000) if x1<=x2 else (0x30000,-0x30000)
        return a,b,'repel'
    a,b=request1,request2
    if overlap and gap<0x40 and not suppression:
        # FF827EC0..FF828240: an actor moving toward the other shares half
        # its requested velocity; opposing requests publish zero on both.
        if a and ((a>0 and x1<x2)or(a<0 and x1>x2)):
            if a*b<0:return 0,0,'opposed'
            return a>>1,a>>1,'shared_p1'
        if b and ((b>0 and x2<x1)or(b<0 and x2>x1)):
            if a*b<0:return 0,0,'opposed'
            return b>>1,b>>1,'shared_p2'
    return a,b,'requested'

def verify(log,guest,payload,typed):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for low,high in ((0xff827c40,0xff828b10),(0xff831ac0,0xff831bf0),(0xff876be0,0xff876d00)):
        a,b=(low-0xff800000)//8,(high-0xff800000)//8
        need(guest[a:b]==original[a:b],'Original complete body-push/bounds/request/facing code unchanged')
    # The source-assembled Bicycle refresh stores3 at the original global;
    # it does not rewrite the original body-push process itself.
    need(struct.unpack_from('<7H',guest,0xf3b80)==(0x09e0,3,0,0x0580,0x19d0,0x0106,0x0960),
         'Original three-tick Bicycle suppression refresh')
    by={r['frame']:r for r in phase.native.ledgers.pair.rows(log,'FIELD')}
    caches=defaultdict(list)
    for line in log.splitlines():
        if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_CACHE_PART '):
            values=re.findall(r'(\w+)=([^\s]+)',line)
            need(len(values)==len(dict(values)),'Unambiguous native cache fields')
            row={k:v if k in ('fighter','assistance')else int(v,16 if k in ('source','command')else 10)
                 for k,v in values}
            caches[row['frame'],row['slot'],row['event']].append(row)
    release,ready,vland,vend=(typed[k]for k in ('release','ready','victimLanding','victimReady'))
    sign=-1 if by[release]['facing']&16 else 1
    branches=Counter();records=[];components=0
    for frame in range(release+1,ready+1):
        a,r=by[frame-1],by[frame]
        need(r['xraw']==(a['xraw']+a['vx'])&MASK and r['vxraw']==(a['vxraw']+a['vvx'])&MASK,
             'Both exact horizontal fixed-point integrations through own ready')
        bounds={}
        for slot,prefix,ykey in ((1,'v','vypos'),(2,'','y')):
            parts=art.group(dict(pose=r[prefix+'pose'],facing=r[prefix+'facing']),payload,guest)
            observed=[values for (f,s,e),values in caches.items()if (f,s)==(frame-1,slot)]
            need(bool(observed),'Every released field has actual previous-tick native cache publication')
            for values in observed:
                need(len(values)==len(parts) and all(all(actual[k]==expected[k]for k in expected)
                     for actual,expected in zip(values,parts)),
                     'Every actual release cache part equals complete ROM composite')
                components+=len(values)
            y=r[ykey]
            bounds[slot]=(min(y-p['dy']for p in parts),max(y-p['dy']+p['height']for p in parts))
        # Last float iteration refreshes3 before the original process decrements
        # it. Subsequently no Bicycle refresh is permitted during released fall.
        expected_suppression=max(0,3-(frame-release))
        need(r['suppression']==expected_suppression,'Exact three-tick original release suppression decay')
        # Release victim requests4 toward the same facing as the attack; own
        # reverse intro retains float request1 until its separately proven drop.
        request1=sign*0x40000
        request2=sign*0x10000 if frame<=typed['fall']else 0
        v1,v2,branch=push(r['vxpos'],r['x'],bounds[1],bounds[2],request1,request2,
                          expected_suppression,signed(a['vvx']),signed(a['vx']))
        need((r['vvx'],r['vx'])==(v1&MASK,v2&MASK),'Every source-derived original release velocity publication')
        branches[branch]+=1
        records.append(dict(frame=frame,branch=branch,gap=abs(r['x']-r['vxpos']),
                            victimBounds=bounds[1],ownBounds=bounds[2],victimVX=v1,ownVX=v2))
    # Once own control returns the native CPU may walk; do not guess its new
    # requested speed. The still-hurt victim stays outside close/max push range.
    for frame in range(ready+1,vend+1):
        a,r=by[frame-1],by[frame]
        need(0x40<=abs(r['x']-r['vxpos'])<0x130 and r['suppression']==0,
             'Independent victim recovery remains outside both body-push thresholds')
        need(r['vxraw']==(a['vxraw']+a['vvx'])&MASK,'Every released victim horizontal integration through its ready')
        need(r['vvx']==(sign*0x40000&MASK if frame<vland else 0),
             'Original victim requested velocity then separate grounded zero')
    need(branches['suppressed']==2 and branches['repel']==2 and branches['shared_p2']==1,
         'Actual release exercises suppression, two repulsions and the shared-speed branch')
    return dict(passed=True,release=release,ownReady=ready,victimReady=vend,
                ownHorizontalFields=ready-release,victimHorizontalFields=vend-release,
                completeSourceBoundCacheParts=components,branches=dict(branches),records=records,
                capturedReleaseHorizontalAccepted=True,allBodyPushBranchesAccepted=False,
                allCPUOrKOOrArenasAccepted=False,fullPortAcceptance=False)

def run():
    proof_path=prior.OUT/'report.json';proof=json.loads(proof_path.read_text())
    need(proof['passed'] and proof['actualNativeBicycleContactDamageAndSeparateRecoveryAccepted'] and
         not proof['fullHorizontalNativePushReplayAccepted'],'Existing intact bounded contact proof')
    pins=dict(proof['inputHashes']);pins[str(proof_path)]=prior.current.assembly.sha(proof_path)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (path,wanted),actual in zip(pins.items(),pool.map(prior.current.assembly.sha,pins)):
            need(actual==wanted,'Every prior executed whole-guest/state/input proof pin unchanged')
    case=ROOT/prior.CASE
    log=(case/'run.log').read_text(encoding='utf-8-sig');guest=(case/'guest_maincpu.bin').read_bytes()
    payload=(ROOT/prior.current.current.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    typed=phase.verify(log,guest)
    need(typed==proof['case']['phase'],'Complete existing startup/contact/vertical/separate-recovery checks retained')
    result=verify(log,guest,payload,typed)
    pins[str(Path(__file__).resolve())]=prior.current.assembly.sha(__file__)
    result.update(inputHashes=pins,gameBytesChanged=False,newCaptureOrBuild=False,scope=__doc__)
    return result

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite executed evidence')
    try:result=run()
    except Exception as error:result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ('inputHashes','records')},indent=2),flush=True)
    raise SystemExit(0 if result['passed']else 1)
