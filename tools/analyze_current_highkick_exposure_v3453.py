"""Ordered actual Sonya incoming-health exposure, not inferred CPU action branches."""
import json,subprocess
from collections import Counter,defaultdict
from pathlib import Path
import verify_current_campaign_shao_highkick_v3440 as native
import diagnose_current_boss_damage_action_order_v2385 as ordered
ROOT=native.ROOT;need=native.need;sha=native.sha
CASE=ROOT/'audit_v3426_current_sonya_natural_defensive_leg_highkick_campaign'
PROOF=ROOT/'audit_v3446_current_sonya_defensive_leg_campaign_checked/report.json'
OUT=ROOT/'audit_v3454_current_highkick_incoming_exposure'

def main():
    need(not OUT.exists(),'Immutable actual exposure diagnostic')
    proof=json.loads(PROOF.read_text());need(proof['passed'] and not proof['unassisted_clear_proven'],
        'Actual whole source/input/state/campaign verified, not a clear')
    logpath=CASE/'run.log';need(sha(logpath)==proof['inputHashes'][str(logpath)],'Actual accepted log unchanged')
    rows=native.old.parse(logpath.read_text(encoding='utf-8-sig'),1,'sonya')
    fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
    keys=defaultdict(set)
    for r in rows:
        if r['tag']=='INPUT' and r['frame']in fields:keys[r['frame']].add(r['button'])
    current=None;incoming=[]
    for r in rows:
        f=fields.get(r['frame'])
        if r['tag']=='BOSS_FIELD':
            current=dict(frame=r['frame'],actor=r['human_actor'],main=r['human_main'],action=r['human_action'])
        elif r['tag']=='BOSS_ACTION' and f:
            need(current is not None and current['frame']==r['frame']
                 and current['actor']==r['actor'] and current['main']==r['main']
                 and current['action']==r['before'],'Exact ordered original own action-store chain')
            current['action']=r['after']
        elif r['tag']=='HEALTH' and f and f['stage']==16 and r['slot']==1 and r['pc']==0xff836700
             and r['after']<r['before'] and r['a8']==f['cpu_actor'] and r['a13']==f['cpu_main']:
            need(current is not None and current['frame']==r['frame'] and current['actor']==f['human_actor']
                 and current['main']==f['human_main'],'Exact own action at incoming original collision store')
            incoming.append(dict(frame=r['frame'],damage=r['before']-r['after'],actualOwnAction=current['action'],
                gap=f['gap'],height=f['height'],guardIntent='Block'in keys[r['frame']],
                cpuActionPreInputOnly=f['cpu_action']))
    need(incoming,'Actual native incoming Shao damage exists')
    outgoing=[r for r in ordered.classify(rows,1)if r['stage']==16]
    groups=defaultdict(lambda:dict(stores=0,damage=0,guardIntentStores=0,guardIntentDamage=0))
    for r in incoming:
        g=groups[f"{r['actualOwnAction']:04X}"];g['stores']+=1;g['damage']+=r['damage']
        if r['guardIntent']:g['guardIntentStores']+=1;g['guardIntentDamage']+=r['damage']
    histogram=Counter(r['damage']for r in incoming)
    pins=dict(proof['inputHashes']);pins[str(PROOF.resolve())]=sha(PROOF)
    pins[str(Path(__file__).resolve())]=sha(__file__);pins[str(Path(ordered.__file__).resolve())]=sha(ordered.__file__)
    for file,digest in pins.items():need(sha(file)==digest,'Actual source/native inputs/game/capture unchanged')
    value=dict(passed=True,actualIncomingStores=len(incoming),actualIncomingDamage=sum(r['damage']for r in incoming),
        ownActualActionAtIncomingCollision=groups,incomingDamageHistogram=dict(histogram),
        actualOutgoingStores=len(outgoing),actualOutgoingDamage=sum(r['damage']for r in outgoing),
        outgoingPreInputGapHistogram=dict(Counter(fields[r['frame']]['gap']for r in outgoing)),
        incomingGuardIntentNotAssumedNativeBlock=True,cpuActionOnlyPreInputNotActualDamageWriterTrace=True,
        controllerFailureNotCharacterDefect=True,controllerImprovementAccepted=False,gameOrCaptureChanged=False,
        fullPortAcceptance=False,inputHashes=pins,
        nextAction='Use ordered own-state exposure and successful contact ranges before a new physical controller. Never infer native CPU attack branches or working block solely from planned inputs/pre-input CPU state; do not change game power/difficulty from losses.')
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless exposure report compression')
    print(json.dumps({k:v for k,v in value.items()if k not in ('inputHashes','outgoingPreInputGapHistogram')},indent=2),flush=True)

if __name__=='__main__':main()
