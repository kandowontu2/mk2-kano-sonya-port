"""Whole actual pre-Shao chronology: only policy labels may differ."""
import json,re,subprocess
from pathlib import Path
import verify_current_campaign_shao_ring_retreat_v3491 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
OLD=ROOT/'audit_v3462_current_sonya_natural_guarded_highkick_campaign'
NEW=ROOT/'audit_v3490_current_sonya_natural_ring_retreat_campaign'
OUT=ROOT/'audit_v3493_current_ring_campaign_prefix_checked'

def exact(a,b):need(a==b,'Every original pre-Shao native record/field/input/pixel-observer row exact after policy-label normalization only')

def main():
    need(not OUT.exists(),'Immutable whole-prefix evidence')
    pins={}
    def accept(relative):
        path=ROOT/relative;proof=json.loads(path.read_text())
        need(proof['passed'] and proof['bounded_campaign_evidence_proven'] and not proof['fullPortAcceptance'],
             'Actual whole terminal current campaign accepted first')
        for file,digest in proof['inputHashes'].items():
            key=str(Path(file).resolve());need(key not in pins or pins[key]==digest,'Consistent actual source/capture byte')
            pins[key]=digest
        pins[str(path.resolve())]=sha(path);return proof
    before=accept('audit_v3474_current_sonya_guarded_highkick_campaign_checked/report.json')
    after=accept('audit_v3494_current_sonya_ring_campaign_checked/report.json')
    need(before['current3172WholeGuestAndCampaignAccepted'] and after['current3172WholeGuestAndCampaignAccepted']
         and before['player']==after['player']=='sonya','Same actual current native fighter and build')
    oldlog=(OLD/'run.log').read_text(encoding='utf-8-sig');newlog=(NEW/'run.log').read_text(encoding='utf-8-sig')
    rows=native.old.parse(newlog,1,'sonya')
    first=next(r['frame']for r in rows if r['tag']=='BOSS_FIELD' and r['stage']==16)
    need(first==100927,'Same actual native Kintaro-to-Shao boundary')
    def prefix(log,policy):
        return [line.replace('policy='+policy,'policy=normalized_pre_shao')for line in log.splitlines()
            if line.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r' frame=(\d+)',line)[1])<first]
    a=prefix(oldlog,'shao_guarded_highkick');b=prefix(newlog,'shao_ring_retreat');exact(a,b)
    need(len(a)>100000,'Non-vacuous complete original native chronology including drawing rows')
    index=next(i for i,line in enumerate(b)if line.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '))
    faults=[]
    for label in ('missing_actual_native_field','changed_actual_own_identity','changed_actual_health'):
        changed=list(b)
        if label=='missing_actual_native_field':changed.pop(index)
        elif label=='changed_actual_own_identity':changed[index]=changed[index].replace('human_id=18','human_id=1',1)
        else:changed[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',changed[index],count=1)
        need(changed!=b,'Non-vacuous actual native chronological fault')
        try:exact(a,changed)
        except ValueError as error:
            need('Every original pre-Shao native record'in str(error),'Specific complete native chronological rejection');faults.append(label)
        else:raise ValueError('Changed actual native chronology accepted')
    exact(a,b)
    for file in (Path(__file__),Path(native.__file__),ROOT/'audit_v3489_current_shao_ring_source_checked/report.json'):
        pins[str(file.resolve())]=sha(file)
    for file,digest in pins.items():need(sha(file)==digest,'Every actual bound source/capture byte unchanged')
    value=dict(passed=True,wholeActualPreShaoRecords=len(a),actualFirstShaoField=first,
        onlyPolicyLabelsNormalized=True,originalKintaroTrajectoryNotIndependentStrategyCoverage=True,
        qualifiedActualChronologyFaults=faults,samePathWholeChronologyPositiveAccepted=True,
        actualSourceOrCaptureChanged=False,fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless full-prefix report compression')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
