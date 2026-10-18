"""Physical approach/throw requests and observed native activation, not wins."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def check_ready(row):
    assert row['ownHeight']==row['enemyHeight']=='0'
    assert int(row['ownFlags'])&0x1c==int(row['enemyFlags'])&0x1c==0
    assert row['projectile']=='0' and int(row['enemyAction']) not in (0x10,0x20c)
    assert row['away']==row['block']==row['down']=='0'

def request_case(index,frame):
    row=index[frame];check_ready(row)
    assert row['phase']=='throw' and row['ownAction']=='771'
    assert row['toward']==row['lp']=='1' and int(row['distance'])<=60
    later=[index[frame+delta] for delta in range(1,9) if frame+delta in index]
    activated=any(row['ownAction']=='1287' for row in later)
    return dict(frame=frame,distance=int(row['distance']),followingObservedFields=len(later),
                throwObservedWithin8=activated if activated or len(later)==8 else None)

def inspect(name):
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
    result=subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],
                          capture_output=True,text=True,creationflags=flags)
    assert result.returncode==0,result.stderr[-3000:]
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert '--campaign-kano-sub-normal-throw' in receipt['testArguments']
    rows=list(csv.DictReader((folder/'sub_normal_throw.csv').open()))
    index={int(row['frame']):row for row in rows}
    assert rows and len(index)==len(rows)
    for row in rows:
        assert row['phase'] in ('guard','approach','prepare','throw')
        if row['phase']!='guard':check_ready(row)
        if row['phase']=='approach':assert row['toward']=='1' and row['lp']=='0' and int(row['distance'])>60
        if row['phase']=='prepare':assert row['toward']==row['lp']=='0' and int(row['distance'])<=60
    requests=[request_case(index,int(row['frame'])) for row in rows if row['phase']=='throw']
    assert all(b['frame']-a['frame']>=12 for a,b in zip(requests,requests[1:]))
    evidence=[Path(__file__),PORT/'audit_campaign_run.py',BASE/'test_wolf_baseline.py',
              BASE/'mk2-rebuild-main/srcp/KSTHROW.ASM']
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','campaign.csv','CAMPAIGN_AUDIT.json','sub_normal_throw.csv'))
    report=dict(run=name,scope='Finite physical normal-throw campaign requests, not a winning strategy',
        cases=requests,requestCount=len(requests),activationsObservedWithin8=sum(case['throwObservedWithin8'] is True for case in requests),
        incompleteWindows=sum(case['throwObservedWithin8'] is None for case in requests),
        approachRequestedFields=sum(row['phase']=='approach' for row in rows),
        nativeCampaignWinCertified=False,fullPortVerified=False,
        pins={str(path):hashlib.sha256(path.read_bytes()).hexdigest().upper() for path in evidence})
    (folder/'SUB_NORMAL_THROW_DIAGNOSTIC.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in ('cases','pins')},indent=2))

if __name__=='__main__':inspect(sys.argv[1])
