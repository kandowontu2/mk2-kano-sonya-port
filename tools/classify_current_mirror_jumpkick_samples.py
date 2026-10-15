"""Sparse LIVE observations only; no attribution of unsampled exact hit frames."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_jumpkick_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
rows=chronology.load(folder/'run.log')
live=[r for r in rows['LIVE'] if r['stage']=='5' and r['human']=='18:18' and r['cpu']=='18:18']
assert live
actions=Counter();cpu_actions=Counter();air=[];health=[]
for row in live:
    own,other=map(int,row['actions'].split(','))
    actions[own]+=1;cpu_actions[other]+=1
    x,y=map(int,row['hpos'].split(','));cx,cy=map(int,row['cpos'].split(','))
    height=int(row['hfloor'])-y
    if height>8:
        air.append(dict(frame=int(row['frame']),action=own,height=height,gap=abs(x-cx)))
    health.append(dict(frame=int(row['frame']),values=list(map(int,row['health'].split(',')))))
assert actions[512]+actions[779]>0,'No sampled native jump'
assert actions[1025]>0,'No sampled native air kick'
report=dict(passedSampleClassification=True,logSHA256=sync.sha(folder/'run.log'),
 sampledMirrorFields=len(live),humanActionCounts=dict(actions),cpuActionCounts=dict(cpu_actions),
 sampledAirborneFields=len(air),sampledAirKickFields=actions[1025],
 airborneGapRange=[min(r['gap'] for r in air),max(r['gap'] for r in air)],
 firstAirborneSamples=air[:12],lastHealthSamples=health[-10:],
 exactJumpActivationCountProven=False,exactDamageAttributionProven=False,
 campaignClear=False,fullPortAccepted=False,
 priorReportCorrection='sampledAirKickStates used STATE, which has no action. LIVE contains paired native actions; use this report instead for action observations.')
out=sync.ROOT/'audit_current_mirror_jumpkick_samples'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
