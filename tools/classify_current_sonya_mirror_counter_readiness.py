"""Initial stance versus actual attack/throw windows; no parser-semantic claim."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_standing_counter_runtime'
out=sync.ROOT/'audit_current_sonya_mirror_counter_readiness'
assert not out.exists()
rows=chronology.load(folder/'run.log')
starts=[];previous=None
for r in rows['MIRROR_STANDING_ACTION']:
    current=(r['p1_main'],r['actions'].split(',')[0])
    if current[1]=='259' and current!=previous:starts.append(r)
    previous=current
groups={};windows=[]
for request in rows.get('MIRROR_STANDING_COUNTER',[]):
    frame=int(request['frame'])
    own=[r for r in starts if frame<=int(r['frame'])<frame+32]
    states=[r for r in rows['MIRROR_STANDING_ACTION'] if frame<=int(r['frame'])<frame+32]
    throws=[r for r in states if r['actions'].split(',')[1]=='1287']
    initial=request['action']
    group=groups.setdefault(initial,dict(requests=0,withStandingKick=0,withObservedCpuThrow=0))
    group['requests']+=1;group['withStandingKick']+=bool(own);group['withObservedCpuThrow']+=bool(throws)
    windows.append(dict(request=request,nativeKickStartAges=[int(r['frame'])-frame for r in own],firstObservedThrowAge=int(throws[0]['frame'])-frame if throws else None,actionChanges=states))
out.mkdir();(out/'report.json').write_text(json.dumps(dict(observationCompleted=True,byInitialHumanAction=groups,requestWindows=windows,logSHA256=sync.sha(folder/'run.log'),exactNativeParserRejectReasonProven=False,fullPortAccepted=False),indent=2))
print(json.dumps(groups))
