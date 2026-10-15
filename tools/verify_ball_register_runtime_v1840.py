"""Causal native callback/timer/body-limit proof from untouched physical inputs."""
import argparse,json,re
from pathlib import Path
import verify_human_special_matrix as human
import verify_human_special_negative_v4 as recoil
import verify_ball_register_source_v1837 as current
from verify_human_special_phases_v1767 import sha
HEX={'at','op','mask','pc','actor','main','owner','a8','a9','a13','a1','a2','a3','a5','a6','a7','b4','status','callback','value','a0','a4','sp'}

def need(ok,msg):
    if not ok:raise ValueError(msg)

def rows(log,tag):
    out=[]
    for line in log.splitlines():
        if not line.startswith('MK2_BALL_BOUND_'+tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for k,v in row.items():
            if k!='assistance':row[k]=int(v,16 if k in HEX else 10)
        out.append(row)
    return out

def verify(log,side):
    state=human.verify_log(log,'ball',side,False);rebound=recoil.verify_rebound(log,side,False)
    field=human.rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in field}
    result=human.rows(log,'RESULT')[0]
    oldlog=(current.ROOT/f'audit_v1806_human_ball_p{side}_render/run.log').read_text(encoding='utf-8-sig')
    gates=rows(log,'GATE');entries=rows(log,'ENTRY');timers=rows(log,'TIMER');native=rows(log,'NATIVE');exits=rows(log,'EXIT')
    need(gates and len(gates)==len(entries)==len(exits),'Every actual callback entry has its gate')
    exit_by={r['frame']:r for r in exits};need(len(exit_by)==len(exits),'One restored return per callback');entry_by={r['frame']:r for r in entries};need(len(entry_by)==len(entries),'One native callback per field')
    cutoff=next(r['frame']for r in gates if r['a5']>=304)
    normalized=lambda t:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line)for line in t.splitlines()if line.startswith('MK2_HSPECIAL_')and int(re.search(r'\bframe=(\d+)',line)[1])<=cutoff]
    need(normalized(log)==normalized(oldlog),'Every physical/native event unchanged until first real boundary threshold')
    old_by={(r['frame'],r['slot']):r for r in human.rows(oldlog,'FIELD')}
    for f in range(state['entry'],state['recovered']+1):
        for s in(1,2):
            for key in('id','roster','owner','actor','main','hp','y','floor','vy','gravity','action','pose','flags','body','trail'):
                need(by[f,s][key]==old_by[f,s][key],'Unchanged native vertical/choreography/identity/health field '+key)
    refreshes=[r for r in timers if r['pc']==0xfffe2140]
    for g in gates:
        e=entry_by[g['frame']];z=exit_by[g['frame']];own=by[g['frame'],side]
        need(e['at']==0xfffe2000 and e['op']==0x098f and e['pc']==0xfffe2010 and e['mask']==65535,'Exact native saved-actor callback entry')
        need(g['at']==0xfffe2070 and g['op']==0xc805 and g['pc']==0xfffe2080 and g['mask']==65535,'Exact native carry decision')
        need(g['writes']==e['writes']==0 and g['assistance']==e['assistance']=='none','Read-only causal observation')
        need(g['id']==e['id']==17 and g['actor']==g['owner']==own['actor']and g['main']==own['main'],'True owned Kano process throughout callback')
        need(g['a8']==by[g['frame'],1]['actor']and g['a9']==by[g['frame'],2]['actor']and g['sp']==e['sp']-224,'Original helper uses both real fighters while seven caller registers are saved')
        need(z['at']in(0xfffe20c0,0xfffe2140)and z['pc']==z['at']+16 and z['op']==0x0960 and z['mask']==65535 and z['writes']==0,'Exact original return after restored caller state')
        need(all(e[k]==z[k]for k in('actor','main','owner','id','a1','a2','a3','a4','a5','a8','a9','sp'))and z['a0']==3,'Every helper-clobbered caller register and stack restored; A0 retains original three')
        need(g['callback']==e['callback']==z['callback']==0xffffdd00,'Original native callback pointer retained')
        need(g['a5']==abs(g['x1']-g['x2'])and bool(g['status']&0x40000000)==(g['a5']<304),'Original physical helper distance and original carry threshold')
        actual=[r for r in refreshes if r['frame']==g['frame']]
        need(len(actual)==int(g['a5']<304),'Timer refresh exactly iff original native distance is below limit')
        for r in actual:need(r['at']==0x010619d0 and r['value']==3 and r['mask']==65535 and r['a8']==g['actor']and r['a13']==g['main'],'Actual owned bounded timer store')
    stopped=[g for g in gates if g['a5']>=304];need(stopped and any(g['repel']==0 for g in stopped),'Suppression actually expires while rebound remains active')
    decisions=[r for r in native if r['at']==0xff828300 and r['b4']==0 and r['a5']>=304]
    positions=[r for r in native if r['at']==0xff828740 and r['frame']>=cutoff and r['a2']not in(r['x1'],r['x2'])]
    need(decisions and positions,'Original body process actually reaches its distance gate and integer correction')
    corrections=[]
    for r in positions:
        own=by[r['frame'],1]if r['a8']==by[r['frame'],1]['actor']else by[r['frame'],2]
        need(r['a8']==own['actor']and r['pc']==0xff828750 and r['op']==0xb048 and r['mask']==65535,'Original position-store instruction on a real physical actor')
        before=r['x1']if r['a8']==by[r['frame'],1]['actor']else r['x2']
        after=r['a2']&65535;corrections.append(abs(after-before))
    need(max(corrections)<=12,'Native correction is small and continuous, not old late 54-pixel return')
    moving=[r for r in field if r['slot']==side and r['action']==0x602]
    after_limit=[r for r in moving if r['frame']>=cutoff+3]
    need(after_limit and max(abs(r['x']-by[r['frame'],3-side]['x'])for r in after_limit)<=307,'Original 304-pixel rule and three-pixel native slack hold after expiry')
    need(any(r['vx']==0 for r in after_limit),'Original outward velocity clamp actually stops rebound at limit')
    for f in range(result['recovered'],result['frame']+1):
        need(by[f,side]['id']==by[f,side]['roster']==17,'Stable real identity through ordinary follow-up')
    return dict(passed=True,side=side,state=state,recoil=rebound,firstBoundaryField=cutoff,
      actualCallbackEntries=len(entries),actualNativeThresholdDecisions=len(gates),actualTimerRefreshes=len(refreshes),
      nativeLimitDecisions=len(decisions),nativePositionCorrections=len(corrections),largestNativeCorrection=max(corrections),
      maximumPostExpiryReboundGap=max(abs(r['x']-by[r['frame'],3-side]['x'])for r in after_limit),
      originalDamageVerticalMotionPosesTimingAndFirstTwentyRecoilFieldsUnchanged=True,
      sourceBoundNativeLimitAppliedDuringRebound=True,actorAndAnimationIteratorPreserved=True,allHelperClobberedCallerRegistersAndStackPreserved=True,fullPortAcceptance=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();need(not args.output.exists(),'Never overwrite evidence')
    meta=json.loads((args.folder/'result.json').read_text(encoding='utf-8-sig'))
    try:report=verify((args.folder/'run.log').read_text(encoding='utf-8-sig'),meta['side'])
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    report['inputHashes']={str(args.folder/'run.log'):sha(args.folder/'run.log'),str(Path(__file__)):sha(__file__)}
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
